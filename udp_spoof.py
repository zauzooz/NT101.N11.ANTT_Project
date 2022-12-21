
from scapy.all import *
from random import randint
from time import sleep
import multiprocessing

def spoof_handler():
    for i in range(0, 50):
        pkt = IP(src=f"10.0.0.{randint(1,254)}",dst="10.0.0.11")/UDP(sport = randint(5000,9999),dport=9696)/Raw(load='this is spoof packet')
        send(pkt)
        sleep(0.025)

if __name__ == "__main__":
    p = multiprocessing.Process(target=spoof_handler)
    p.start()
    p.join(15)
    if p.is_alive():
        p.terminate()