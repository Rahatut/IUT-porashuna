import socket  # UDP sockets for datagram-based transport.
import struct  # Binary packing/unpacking for sequence and ACK headers.
import sys  # Reads destination host/port and input file from CLI args.

DEST = (sys.argv[1], int(sys.argv[2]))  # Receiver address: <host, udp_port>.
fname = sys.argv[3]  # Path of the local file to transmit.
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # IPv4 UDP sender socket.
sock.settimeout(0.5)  # Stop-and-wait retransmit timer (seconds).

seq = 0  # Monotonic sequence number, one value per file chunk.
with open(fname, 'rb') as f:
    while True:
        chunk = f.read(1024)  # Fixed payload size keeps framing simple.
        if not chunk:
            break  # EOF reached: data phase complete.
        pkt = struct.pack('!I', seq) + chunk  # Datagram format: 4-byte seq + payload.
        while True:
            sock.sendto(pkt, DEST)  # Send (or resend) current chunk until matching ACK arrives.
            try:
                data, _ = sock.recvfrom(8)  # ACK packet is expected to be very small.
                (ack,) = struct.unpack('!I', data[:4])  # ACK value identifies confirmed seq.
                if ack == seq:
                    seq += 1  # Advance window only on correct ACK (stop-and-wait reliability).
                    break
            except socket.timeout:
                print("Timeout, retransmit seq", seq)  # Lost packet/ACK triggers resend.

sock.sendto(struct.pack('!I', 0xFFFFFFFF), DEST)  # Sentinel sequence marks transfer end.
sock.close()  # Release socket resources.
