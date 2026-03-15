# --- SERVER SIDE ---
import socket

# 1. Create a new socket object using IPv4 and TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Bind the socket to all network interfaces ('0.0.0.0') on port 6006
server.bind(('0.0.0.0', 6006))

# 3. Put the socket into listening mode, with a backlog of 5 queued connections
server.listen(5)

# 4. Block and wait for an incoming connection; when one arrives, accept() returns a new socket object (conn) and the client address (addr)
conn, addr = server.accept()

# 5. Print the address of the newly connected client
print("Connected by", addr)

# 6. Enter an infinite loop to continually receive and echo data
while True:
    # 7. Read up to 1024 bytes from the client; blocks until data arrives
    data = conn.recv(1024)
    # 8. If no data was received, it means the client closed the connection - break out
    if not data:
        break
    # 9. Print what was received for debugging/logging
    print("Received:", data)
    # 10. Send the exact same bytes back to the client
    conn.sendall(data)

# 11. Close the client socket once done
conn.close()
