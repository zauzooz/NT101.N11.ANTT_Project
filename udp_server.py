import socket
import multiprocessing
BUFFER_SIZE = 1024

udpServer = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

udpServer.bind(("10.0.0.11", 9696))

def server_run():
    while(True):
        msg_rcv, addr = udpServer.recvfrom(BUFFER_SIZE)
        # print(f"from {addr}: " + msg_rcv.decode("utf-8"))
        udpServer.sendto(msg_rcv, addr)

if __name__=="__main__":
    p = multiprocessing.Process(target=server_run)
    p.start()
    p.join(50)
    if p.is_alive():
        p.terminate()