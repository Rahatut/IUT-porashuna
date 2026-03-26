import socket  # UDP networking for datagram receive/send.
import struct  # Parses and builds 4-byte sequence/ACK fields.
import sys  # Reads listen port and output file path from CLI args.

PORT = int(sys.argv[1])  # Local UDP port to listen on.
out = sys.argv[2]  # Destination file where received bytes are written.
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # IPv4 UDP receiver socket.
sock.bind(('0.0.0.0', PORT))  # Accept datagrams from any interface.

with open(out, 'wb') as fo:
    expected = 0  # Next in-order sequence number required for contiguous file reconstruction.
    while True:
        data, addr = sock.recvfrom(2048)  # One datagram contains one framed chunk.
        (seq,) = struct.unpack('!I', data[:4])  # First 4 bytes are sender sequence header.
        if seq == 0xFFFFFFFF:
            print("Transfer complete")
            sock.sendto(struct.pack('!I', 0xFFFFFFFF), addr)  # Optional confirmation of end marker.
            break

        payload = data[4:]  # Remaining bytes are file content for this chunk.
        if seq == expected:
            fo.write(payload)  # Commit only next in-order chunk to avoid corruption.
            sock.sendto(struct.pack('!I', seq), addr)  # ACK confirms exactly which chunk was accepted.
            expected += 1
        else:
            last = (expected - 1) if expected > 0 else 0xFFFFFFFF  # Duplicate/out-of-order packet path.
            sock.sendto(struct.pack('!I', last), addr)  # Re-ACK last good seq so sender retransmits missing one.

sock.close()  # Close socket after transfer loop exits.
