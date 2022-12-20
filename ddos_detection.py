#!/usr/bin/ python3
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ipv4
from ryu.lib.packet import arp
from ryu.lib.packet import ether_types
import pickle

HASH_TABLE = {}
RECORDS = []
WINDOW_SIZE = 10
COUNTER = 0
I = 0
ALERT_COUNTER = 0
STANDARD_NORMAL_TRAFFIC = pickle.load('./value_setting/standart_normal_traffic.pkl')
THRESHOLD_1 = pickle.load('./value_setting/threshold1.pkl')
THRESHOLD_2 = pickle.load('./value_setting/threshold2.pkl')

# THRESHOLD_1=1.070907926513757
# THRESHOLD_2=0.6382744025394036
# STANDARD_NORMAL_TRAFFIC=[0.6515550195600632, 0.5249001582967918, 0.561533313148384, 0.13929057462790978, 1.5229352167401133, 1.3147547655313476, 1.2710661227219147, 1.465342190882962, 1.881773382340798, 1.3774352247834831]

class Switch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(Switch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.datapath = []

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)
    
    def Shanon_Entropy(capture):
        from fractions import Fraction
        from math import log2
        entropy = 0
        for key in capture:
            proba = Fraction(capture[key]/WINDOW_SIZE)
            entropy += -1*proba*log2(proba)
        return entropy

    def detect_ddos_attack(self, record):
        global ALERT_COUNTER
        global I
        try:
            h = self.Shanon_Entropy(record)
            id = abs(STANDARD_NORMAL_TRAFFIC[I] -  h)
            if id >= THRESHOLD_2 and h <= THRESHOLD_1:
                ALERT_COUNTER = ALERT_COUNTER + 1
                if ALERT_COUNTER == 3:
                    self.logger.info("-------------------- DDOS ATTACK IS DETECTED --------------------")
                    exit(0)
            else:
                ALERT_COUNTER = 0
            I = I + 1
        except:
            pass


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        global HASH_TABLE
        global COUNTER
        global RECORDS
        global I

        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        _arp = pkt.get_protocols(arp.arp)
        _ipv4 = pkt.get_protocols(ipv4.ipv4)

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return

        mac_dst = eth.dst
        mac_src = eth.src

        dpid = format(datapath.id, "d").zfill(16)
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("packet in %s %s %s %s", dpid, mac_src, mac_dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][mac_src] = in_port

        if _arp != []:
            COUNTER += 1
            ip_dst = _arp[0].dst_ip
            if ip_dst not in HASH_TABLE:
                HASH_TABLE[ip_dst] = 1
            else:
                HASH_TABLE[ip_dst] += 1
        elif _ipv4 != []:
            COUNTER += 1
            ip_dst = _ipv4[0].dst
            if ip_dst not in HASH_TABLE:
                HASH_TABLE[ip_dst] = 1
            else:
                HASH_TABLE[ip_dst] += 1
        
        if COUNTER == WINDOW_SIZE:
            RECORDS.append(HASH_TABLE)
            self.detect_ddos_attack(HASH_TABLE)
            HASH_TABLE = {}
            COUNTER = 0

        if mac_dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][mac_dst]
        else:
            out_port = ofproto.OFPP_FLOOD
                
        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=mac_dst)
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions)
        
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)
    