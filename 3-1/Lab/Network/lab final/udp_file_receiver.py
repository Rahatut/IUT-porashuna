import socket
import struct
import sys

PORT = int(sys.argv[1])
out = sys.argv[2]
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', PORT))

TYPE_DATA = 0
TYPE_ACK = 1
TYPE_FIN = 2

with open(out, 'wb') as fo:
    expected = 0
    while True:
        data, addr = sock.recvfrom(2048)

        if len(data) < 4:
            continue  

        pkt_type, pkt_seq, pkt_len = struct.unpack('!BBH', data[:4])
        payload = data[4:4+pkt_len]

        if pkt_type == TYPE_FIN:
            print("Transfer complete")
            ack = struct.pack('!BB', TYPE_FIN, 0)
            sock.sendto(ack, addr)
            break

        if pkt_type == TYPE_DATA and pkt_seq == expected:
            fo.write(payload)
            ack = struct.pack('!BB', TYPE_ACK, pkt_seq)
            sock.sendto(ack, addr)
            expected = 1 - expected
        else:
            last_seq = 1 - expected
            ack = struct.pack('!BB', TYPE_ACK, last_seq)
            sock.sendto(ack, addr)
sock.close()