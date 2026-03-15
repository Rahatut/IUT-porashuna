import socket
import threading

# Create UDP client socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.settimeout(1.0)
server_addr = ('localhost', 5005)

msg = 'Hello, UDP Server!'

sock.sendto(msg.encode('utf-8'), server_addr)

try:
    data, _ = sock.recvfrom(1024)
    print("Received from server:", data)
except socket.timeout:
    print("No response from server, timed out.")