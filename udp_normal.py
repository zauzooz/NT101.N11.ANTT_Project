import socket
from time import sleep
import multiprocessing
BUFFER_SIZE = 1024

def client_handler():
    msg = b"this is normal packet."
    udpSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    for i in range(0, 50):
        udpSocket.sendto(msg, ("10.0.0.11",9696))
        msg, addr = udpSocket.recvfrom(BUFFER_SIZE)
        print(f"from {addr}: " + msg.decode("utf-8"))
        sleep(0.3)

if __name__=="__main__":
    p = multiprocessing.Process(target=client_handler)
    p.start()
    p.join(15)
    if p.is_alive():
        p.terminate()