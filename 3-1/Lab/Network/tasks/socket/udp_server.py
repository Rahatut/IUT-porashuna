import socket
import threading

# Create UDP server socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Allow address reuse
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind(('0.0.0.0', 5005))
print("UDP server listening on port 5005...")

# Handler for each incoming message
def handle_request(data, addr):
    print(f"Received {data!r} from {addr}")
    sock.sendto(data, addr)

try:
    while True:
        data, addr = sock.recvfrom(1024)
        # Spawn a new thread per request for concurrent handling
        threading.Thread(target=handle_request, args=(data, addr), daemon=True).start()
except KeyboardInterrupt:
    print("\nShutting down server.")

sock.close()