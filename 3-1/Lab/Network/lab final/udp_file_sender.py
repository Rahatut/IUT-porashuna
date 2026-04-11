import socket
import struct
import time
import sys

DEST = (sys.argv[1], int(sys.argv[2]))
fname = sys.argv[3]
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)

seq = 0

TYPE_DATA = 0
TYPE_ACK = 1
TYPE_FIN = 2

with open(fname, 'rb') as f:
    while True:
        chunk = f.read(512)
        if not chunk:
            break
       
        pkt = struct.pack('!BBH', TYPE_DATA, seq, len(chunk)) + chunk

        retry = 0

        while retry <5:
            sock.sendto(pkt, DEST)

            try:
                data, _ = sock.recvfrom(8)
                if len(data) >= 2:
                    ack_type, ack_seq = struct.unpack('!BB', data[:2])
                    if ack_type == TYPE_ACK and ack_seq == seq:
                        seq = 1 - seq
                        break
            except socket.timeout:
                retry+=1
                print("Timeout, retransmit seq", seq)

            if retry==5:
                print("Max retransmission, transfer failed.")
                sock.close()
            
    fin_pkt = struct.pack('!BBH', TYPE_FIN, seq, 0)

    retry = 0

    while retry <5:
            sock.sendto(fin_pkt, DEST)

            try:
                data, _ = sock.recvfrom(8)
                if len(data) >= 2:
                    ack_type, ack_seq = struct.unpack('!BB', data[:2])
                    if ack_type == TYPE_ACK:
                        break
            except socket.timeout:
                retry+=1
                print("Timeout, retransmit seq", seq)

            if retry==5:
                print("Max retransmission, transfer failed.")
                sock.close()
    
sock.close()