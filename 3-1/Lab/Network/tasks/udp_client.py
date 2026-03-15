import socket
import time

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a 1 second timeout for blocking socket operations
sock.settimeout(1.0)

# Define server address as localhost on port 5005
server_addr = ('localhost', 5005)

# ---- Single message exchange ----
message = 'Hello, UDP Server'
# Encode the string to bytes and send to the server
sock.sendto(message.encode('utf-8'), server_addr)
try:
    # Wait for up to 1024 bytes response
    data, _ = sock.recvfrom(1024)
    print("Echo:", data)
except socket.timeout:
    print("No response, server may be down.")

# --- Multiple messages with retry and RTT ----
rtts = []  # to store round-trip times

# sending 5 messages with max 3 retries
for i in range(5):
    text = f"Msg {i}".encode('utf-8')
    attempts = 0
    while attempts < 3:
        start = time.time()  # start RTT timer
        sock.sendto(text, server_addr)  # send datagram
        try:
            data, _ = sock.recvfrom(1024)  # wait for echo
            elapsed = time.time() - start
            rtts.append(elapsed)
            print(f"Response {i}: {data} (RTT={elapsed:.3f}s)")
            break
        except socket.timeout:
            attempts += 1
            print(f"Retry {attempts} for message {i}")
            time.sleep(0.5)  # brief pause between messages

sock.close()
