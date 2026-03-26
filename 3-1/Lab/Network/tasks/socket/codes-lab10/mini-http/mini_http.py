import os  # Needed for safe path joins and script-relative directories.
import socket  # Provides low-level TCP server/client networking APIs.

HOST = '127.0.0.1'  # IPv4 loopback only; reachable from this machine, not external hosts.
PORT = 8080  # Common non-privileged development port for local HTTP testing.
WEBROOT = os.path.join(os.path.dirname(__file__), 'www')  # Resolve from file location, not shell cwd.


def handle(conn):
    """
    Handle one client HTTP request.
    Reads until the end of HTTP headers (\r\n\r\n),
    parses the request line, and serves a file.
    """
    req = b''  # Buffer raw request bytes until we see the end of headers.

    # HTTP headers end at a blank line (\r\n\r\n), so read until that marker appears.
    while b'\r\n\r\n' not in req:
        chunk = conn.recv(1024)  # Read in chunks to support variable header size.
        if not chunk:
            return  # Client closed early; no complete request to process.
        req += chunk

    # First line is enough for this tiny server: "METHOD /path HTTP/1.1".
    first_line = req.split(b'\r\n', 1)[0].decode(errors='replace')

    try:
        method, path, version = first_line.split()  # Validates expected 3-token request line.
    except ValueError:
        return  # Malformed start line; ignore instead of crashing.

    path = path.lstrip('/')  # Convert URL path into a relative file path.
    if path == '':
        path = 'index.html'  # Default document when browser requests "/".

    full_path = os.path.join(WEBROOT, path)  # Map requested resource to filesystem.

    if os.path.isfile(full_path):
        with open(full_path, 'rb') as f:
            body = f.read()  # Read entire static file to send as HTTP body.

        # Minimal valid success response: status line, content length, blank line, body.
        response = (
            b"HTTP/1.0 200 OK\r\n"
            + b"Content-Length: " + str(len(body)).encode() + b"\r\n"
            + b"\r\n"
            + body
        )
    else:
        # Return an explicit 404 when file is missing.
        response = (
            b"HTTP/1.0 404 Not Found\r\n"
            + b"Content-Length: 0\r\n"
            + b"\r\n"
        )

    conn.sendall(response)  # sendall() guarantees the full response is transmitted.


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create an IPv4 TCP listening socket.
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow quick restart on same port.
server.bind((HOST, PORT))  # Attach socket to local address and port.
server.listen(5)  # Start accepting connections; queue up to 5 pending clients.

print(f"Mini HTTP server running on http://{HOST}:{PORT}")

while True:
    conn, addr = server.accept()  # Block until a client connects.
    try:
        handle(conn)  # Handle one request at a time (sequential server model).
    finally:
        conn.close()  # Always close socket to avoid leaks even on errors.
