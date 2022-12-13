from mininet.net import Containernet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from _thread import start_new_thread

def hostRunCMD(h, _cmd):
    h.cmd(_cmd)

if __name__=="__main__":
    net = Containernet(controller=None)

    net.addController(name='ryu', controller=RemoteController, ip='127.0.0.1', port=6633)

    # create hosts
    h1 = net.addHost('h1', ip='10.0.0.1', dimage="ubuntu:trusty")
    h2 = net.addHost('h2', ip='10.0.0.2', dimage="ubuntu:trusty")
    h3 = net.addHost('h3', ip='10.0.0.3', dimage="ubuntu:trusty")
    h4 = net.addHost('h4', ip='10.0.0.4', dimage="ubuntu:trusty")
    h5 = net.addHost('h5', ip='10.0.0.5', dimage="ubuntu:trusty")
    h6 = net.addHost('h6', ip='10.0.0.6', dimage="ubuntu:trusty")
    h7 = net.addHost('h7', ip='10.0.0.7', dimage="ubuntu:trusty")
    h8 = net.addHost('h8', ip='10.0.0.8', dimage="ubuntu:trusty")
    h9 = net.addHost('h9', ip='10.0.0.9', dimage="ubuntu:trusty")
    h10 = net.addHost('h10', ip='10.0.0.10', dimage="ubuntu:trusty")
    h11 = net.addHost('h11', ip='10.0.0.11', dimage="ubuntu:trusty")
    h12 = net.addHost('h12', ip='10.0.0.12', dimage="ubuntu:trusty")
    h13 = net.addHost('h13', ip='10.0.0.13', dimage="ubuntu:trusty")
    h14 = net.addHost('h14', ip='10.0.0.14', dimage="ubuntu:trusty")
    h15 = net.addHost('h15', ip='10.0.0.15', dimage="ubuntu:trusty")
    h16 = net.addHost('h16', ip='10.0.0.16', dimage="ubuntu:trusty")

    # create switch
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')

    # create a link between 2 devices
    net.addLink(s1, h1)
    net.addLink(s1, h2)
    net.addLink(s1, h3)
    net.addLink(s1, h4)

    net.addLink(s2, h5)
    net.addLink(s2, h6)
    net.addLink(s2, h7)
    net.addLink(s2, h8)

    net.addLink(s3, h9)
    net.addLink(s3, h10)
    net.addLink(s3, h11)
    net.addLink(s3, h12)

    net.addLink(s4, h13)
    net.addLink(s4, h14)
    net.addLink(s4, h15)
    net.addLink(s4, h16)

    net.addLink(s1, s2)
    net.addLink(s3, s4)
    net.addLink(s2, s3)


    # start network
    net.start()
    start_new_thread(hostRunCMD, (h11,"python3 udp_server.py",))
    from time import sleep
    sleep(0.5)
    start_new_thread(hostRunCMD, (h1,"python3 udp_normal.py",))
    start_new_thread(hostRunCMD, (h2,"python3 udp_normal.py",))
    start_new_thread(hostRunCMD, (h3,"python3 udp_normal.py",))
    start_new_thread(hostRunCMD, (h4,"python3 udp_normal.py",))
    start_new_thread(hostRunCMD, (h5,"python3 udp_normal.py",))
    start_new_thread(hostRunCMD, (h6,"python3 udp_normal.py",))
    start_new_thread(hostRunCMD, (h7,"python3 udp_normal.py",))
    start_new_thread(hostRunCMD, (h8,"python3 udp_spoof.py",)) # attack host
    start_new_thread(hostRunCMD, (h9,"python3 udp_normal.py",))
    start_new_thread(hostRunCMD, (h10,"python3 udp_normal.py",))
    start_new_thread(hostRunCMD, (h12,"python3 udp_normal.py",))
    start_new_thread(hostRunCMD, (h13,"python3 udp_normal.py",))
    start_new_thread(hostRunCMD, (h14,"python3 udp_normal.py",))
    start_new_thread(hostRunCMD, (h15,"python3 udp_normal.py",))
    start_new_thread(hostRunCMD, (h16,"python3 udp_normal.py",))
    CLI(net)
    # stop network
    net.stop()