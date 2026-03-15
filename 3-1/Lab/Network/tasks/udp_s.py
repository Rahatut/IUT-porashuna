import socket, time
import threading

# Create UDP server socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


sock.bind(('0.0.0.0', 5005))
print("UDP server listening on port 5005...")

try:
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Received {data!r} from {addr}")
        sock.sendto(data, addr)


except KeyboardInterrupt:
    print("\nShutting down server.")
    sock.close()