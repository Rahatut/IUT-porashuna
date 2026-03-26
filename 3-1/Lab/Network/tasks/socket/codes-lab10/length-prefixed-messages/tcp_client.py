import socket  # Provides TCP sockets.
import struct  # Packs/unpacks fixed-size binary headers.
import sys  # Reads optional host from command-line arguments.

HOST = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'  # Default to local server if host is omitted.
PORT = 7007  # Must match the server port.


def recv_all(sock, n):
    data = b''  # TCP is a byte stream, so we accumulate until we have exactly n bytes.
    while len(data) < n:
        chunk = sock.recv(n - len(data))  # Ask only for the remaining bytes.
        if not chunk:
            return None  # Peer closed before full frame arrived.
        data += chunk
    return data  # Safe to parse/use because byte count is exact.


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4 TCP client socket.
client.connect((HOST, PORT))  # Establishes a single persistent connection to the server.

for msg in ["hello", "this is a longer message", "bye"]:
    data = msg.encode()  # Convert text to bytes because sockets send bytes, not str.
    frame = struct.pack('!I', len(data)) + data  # Prefix payload with 4-byte big-endian length.
    client.sendall(frame)  # sendall avoids partial-send handling in user code.

    hdr = recv_all(client, 4)  # Always read exactly one frame header.
    if hdr is None:
        print("Server closed")
        break

    (length,) = struct.unpack('!I', hdr)  # Decode declared payload length.
    resp = recv_all(client, length)  # Read exactly one framed payload.
    if resp is None:
        print("Server closed mid-response")
        break

    print("Echo:", resp.decode())  # Decode bytes back to text for display.

client.close()  # Release local socket resources and send TCP FIN.
