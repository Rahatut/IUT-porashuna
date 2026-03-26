# --- CLIENT SIDE ---
import socket

# 1. Create a new socket object using IPv4 and TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Connect this socket to the server running on localhost port 6006
client.connect(('127.0.0.1', 6006))

# 3. Loop over a list of bytestrings to send
for msg in [b"Hello, TCP!", b"Message 2", b"Final msg"]:
    # a) Send the entire message to the server (blocks until sent)
    client.sendall(msg)
    # b) Wait for up to 1024 bytes of response from the server (the echo)
    data = client.recv(1024)
    # c) Print out what the server echoed back
    print("Echo:", data)

# 4. Close the client socket when all messages have been sent and echoed
input("Press ENTER here to close the connection and exit ... ")
client.close()
