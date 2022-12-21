import socket
BUFFER_SIZE = 1024

udpServer = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

udpServer.bind(("10.0.0.11", 9696))

PACKET_NUM = 0

while(PACKET_NUM < 50*15):
    PACKET_NUM += 1
    msg_rcv, addr = udpServer.recvfrom(BUFFER_SIZE)
    # print(f"from {addr}: " + msg_rcv.decode("utf-8"))
    udpServer.sendto(msg_rcv, addr)