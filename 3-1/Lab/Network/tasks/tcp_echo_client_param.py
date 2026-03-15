import sys
import socket

server_ip = sys.argv[1]  # Usage: python3 tcp_echo_client.py 192.168.1.10
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, 6006))

for msg in [b"Hello, TCP!", b"Message 2", b"Final msg"]:
    client.sendall(msg)
    data = client.recv(1024)
    print("Echo:", data)

input("Press ENTER here to close the connection and exit ... ")
client.close()
