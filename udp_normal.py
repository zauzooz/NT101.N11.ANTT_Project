import socket
from time import sleep
BUFFER_SIZE = 1024

msg = b"this is normal packet."
udpSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
for i in range(0, 50):
    udpSocket.sendto(msg, ("10.0.0.11",9696))
    msg, addr = udpSocket.recvfrom(BUFFER_SIZE)
    print(f"from {addr}: " + msg.decode("utf-8"))
    sleep(0.3)
