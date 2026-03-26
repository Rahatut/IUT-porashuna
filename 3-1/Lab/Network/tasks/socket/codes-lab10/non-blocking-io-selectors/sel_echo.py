import selectors
import socket

sel = selectors.DefaultSelector()

def accept(sock):
    conn, addr = sock.accept()
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read_conn)

def read_conn(conn):
    data = conn.recv(1024)
    if data:
        conn.sendall(data)  # echo
    else:
        sel.unregister(conn)
        conn.close()

sock = socket.socket()
sock.bind(('0.0.0.0', 9009))
sock.listen()
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

print("Selector-based server on 9009")
while True:
    events = sel.select()
    for key, _ in events:
        callback = key.data
        callback(key.fileobj)