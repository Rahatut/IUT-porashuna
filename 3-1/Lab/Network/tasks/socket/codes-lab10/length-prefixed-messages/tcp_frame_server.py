import socket  # Provides TCP server primitives.
import struct  # Encodes/decodes 4-byte length headers.

HOST = '0.0.0.0'  # Listen on every IPv4 interface so remote hosts can connect.
PORT = 7007  # Fixed demo port; client must use the same port.


def recv_all(sock, n):
    data = b''  # Collect bytes because TCP recv() may return partial data.
    while len(data) < n:
        chunk = sock.recv(n - len(data))  # Read only what is still missing.
        if not chunk:
            return None  # EOF before n bytes means peer disconnected.
        data += chunk
    return data  # Guarantees exact-size frame part for safe parsing.


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4 TCP listening socket.
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allows fast restart on same port.
server.bind((HOST, PORT))  # Reserve <HOST, PORT> so clients can dial in.
server.listen(5)  # Kernel may queue up to 5 pending connection attempts.
print("Length-prefixed TCP server on", PORT)

conn, addr = server.accept()  # This server handles one client connection per run.
print("Connected by", addr)

try:
    while True:
        hdr = recv_all(conn, 4)  # Frame format starts with a fixed 4-byte length field.
        if hdr is None:
            break

        (length,) = struct.unpack('!I', hdr)  # '!I' means network-order unsigned 32-bit integer.
        payload = recv_all(conn, length)  # Read exactly one logical message body.
        if payload is None:
            break

        print("Got message:", payload.decode())  # Display decoded text payload.
        conn.sendall(struct.pack('!I', len(payload)) + payload)  # Echo using the same framed protocol.
finally:
    conn.close()  # Close accepted client socket first.
    server.close()  # Then close listening socket to release the port.
