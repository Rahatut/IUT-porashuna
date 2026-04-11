
## Core UDP Questions

| **Question** | **Answer** |
|--------------|------------|
| If UDP is unreliable, why does it still include a checksum? | Checksum is for **error detection** (not reliability). UDP detects corruption but does not retransmit lost/corrupted data. |
| Why use port numbers without a connection? | Port numbers enable **process-to-process delivery** (multiplexing/demultiplexing), even without a connection. |
| Can UDP guarantee ordered delivery? | **No.** Only if the **application layer** implements ordering. |
| Why doesn’t UDP always cause congestion collapse? | Many UDP apps send **small/controlled traffic** or implement their own congestion control. |
| What if sender is faster than receiver? | Packets may be **dropped at receiver or network buffers** due to overflow. |
| Why does ICMP handle port errors? | UDP has no error-reporting; **ICMP provides feedback**. |
| In what type of application is connectionless service an advantage? Why? | Short request-response apps (e.g., DNS). **Avoids connection setup overhead** and reduces delay. |
| Why does connection-oriented service introduce more delay? | Requires connection establishment/termination (multiple packet exchanges). |
| When is connectionless service a disadvantage? | For long messages: packets may arrive out of order and can't be easily reassembled. |
| Why is UDP suitable for DNS but not SMTP? | DNS: small, quick messages → UDP is efficient. SMTP: large messages → needs reliability → TCP is better. |
| Why is UDP not suitable for long messages? | Messages must be split; parts may arrive out of order or be lost. |
| What does lack of error control mean in UDP? | UDP does **not retransmit** lost/corrupted packets. |
| Why can lack of error control be an advantage? | Avoids retransmission delays — important for real-time apps. |
| Why must applications handle out-of-order packets? | UDP does not provide ordering; application must reorder data. |
| Why does UDP not provide congestion control? | Designed to be simple/lightweight; leaves control to applications. |
| How can TCP worsen congestion? | Retransmits lost packets, increasing network traffic. |
| Why is UDP suitable for request-response communication? | Only one message exchange needed; connection setup unnecessary. |
| How does UDP support multiple processes? | Uses **port numbers** to identify different applications. |
| How does UDP perform demultiplexing? | Uses **destination port number** to deliver data to correct process. |
| What is the minimum and maximum size of a UDP datagram? | **Minimum:** 8 bytes (header only) <br> **Maximum:** 65,535 bytes |
| If a UDP datagram has a total length of 100 bytes, how many bytes are actual data? | Data = 100 − 8 = **92 bytes** |
| A UDP message carries 16 bytes of data. Calculate efficiency at UDP level. | $\text{Efficiency} = \frac{16}{16 + 8} = \frac{16}{24} = 66.67\%$ |
| Same as above, but include IP header (20 bytes). Find efficiency. | $\text{Efficiency} = \frac{16}{16 + 8 + 20} = \frac{16}{44} = 36.36\%$ |
| Same scenario, include Ethernet header (18 bytes). Find efficiency. | $\text{Efficiency} = \frac{16}{16 + 8 + 20 + 18} = \frac{16}{62} \approx 25.8\%$ |
| A UDP datagram is 2000 bytes. If the network MTU is 1500 bytes, what happens? | IP will **fragment the UDP datagram** to fit MTU. |
| A UDP packet arrives with destination port 53. What type of application is likely receiving it? | Port 53 → **DNS application** |
| Client IP: 10.0.0.1, Port: 5000 <br> Server IP: 8.8.8.8, Port: 53 <br> Write the socket pair. | (10.0.0.1 : 5000) → (8.8.8.8 : 53) |
| UDP length field = 60 bytes. Find header and data size. | Header = 8 bytes <br> Data = 60 − 8 = **52 bytes** |
| If 5 UDP packets are sent and 2 are lost, what does the receiver do? | Receiver **does nothing** (no retransmission). Lost packets are ignored. |

---

## Advanced UDP Conceptual Questions

**1. Why does UDP not guarantee delivery even though the underlying IP layer also provides best-effort service?**  
> Both UDP and IP are best-effort. UDP does not add any reliability mechanisms over IP, so delivery is not guaranteed.

**2. Explain how UDP achieves process-to-process communication without maintaining connection state.**  
> UDP uses **port numbers** to identify processes, enabling direct delivery without maintaining connection state.

**3. Why is UDP suitable for multicasting but TCP is not?**  
> UDP supports **one-to-many communication (multicasting)**. TCP is strictly one-to-one (connection-oriented).

**4. Explain why UDP may lead to packet duplication.**  
> Due to retransmissions at lower layers or network duplication, UDP may deliver duplicate packets.

**5. Why is UDP header size fixed, and how does this impact performance?**  
> UDP header is fixed (8 bytes) for simplicity and speed → lower overhead and faster processing.

**6. If UDP has no flow control, how can a receiver avoid being overwhelmed?**  
> Receiver may:
> - Drop packets
> - Use buffering
> - Apply application-level flow control

**7. Why is UDP preferred in routing protocols like RIP?**  
> Routing protocols (like RIP) require fast updates and can tolerate some loss → UDP is suitable.

**8. Explain how UDP can be used in applications that require reliability.**  
> Applications can add:
> - Sequence numbers
> - ACKs
> - Retransmissions

**9. Why is it difficult to implement congestion control at the application layer over UDP?**  
> Application lacks full network visibility, making congestion detection and control difficult.

**10. Explain the role of the pseudoheader in UDP checksum calculation.**  
> Pseudoheader includes IP addresses to detect errors in source/destination addressing.

---

| **Question**                                                                                                          | **Answer**                                                                                                                 |
| --------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| If UDP is unreliable, why does it still include a checksum?                                                           | Checksum is for **error detection** (not reliability). UDP detects corruption but does not retransmit lost/corrupted data. |
| Why use port numbers without a connection?                                                                            | Port numbers enable **process-to-process delivery** (multiplexing/demultiplexing), even without a connection.              |
| Can UDP guarantee ordered delivery?                                                                                   | **No.** Only if the **application layer** implements ordering.                                                             |
| Why doesn’t UDP always cause congestion collapse?                                                                     | Many UDP apps send **small/controlled traffic** or implement their own congestion control.                                 |
| What if sender is faster than receiver?                                                                               | Packets may be **dropped at receiver or network buffers** due to overflow.                                                 |
| Why does ICMP handle port errors?                                                                                     | UDP has no error-reporting; **ICMP provides feedback**.                                                                    |
| In what type of application is connectionless service an advantage? Why?                                              | Short request-response apps (e.g., DNS). **Avoids connection setup overhead** and reduces delay.                           |
| Why does connection-oriented service introduce more delay?                                                            | Requires connection establishment/termination (multiple packet exchanges).                                                 |
| When is connectionless service a disadvantage?                                                                        | For long messages: packets may arrive out of order and can't be easily reassembled.                                        |
| Why is UDP suitable for DNS but not SMTP?                                                                             | DNS: small, quick messages → UDP is efficient. SMTP: large messages → needs reliability → TCP is better.                   |
| Why is UDP not suitable for long messages?                                                                            | Messages must be split; parts may arrive out of order or be lost.                                                          |
| What does lack of error control mean in UDP?                                                                          | UDP does **not retransmit** lost/corrupted packets.                                                                        |
| Why can lack of error control be an advantage?                                                                        | Avoids retransmission delays — important for real-time apps.                                                               |
| Why must applications handle out-of-order packets?                                                                    | UDP does not provide ordering; application must reorder data.                                                              |
| Why does UDP not provide congestion control?                                                                          | Designed to be simple/lightweight; leaves control to applications.                                                         |
| How can TCP worsen congestion?                                                                                        | Retransmits lost packets, increasing network traffic.                                                                      |
| Why is UDP suitable for request-response communication?                                                               | Only one message exchange needed; connection setup unnecessary.                                                            |
| How does UDP support multiple processes?                                                                              | Uses **port numbers** to identify different applications.                                                                  |
| How does UDP perform demultiplexing?                                                                                  | Uses **destination port number** to deliver data to correct process.                                                       |
| What is the minimum and maximum size of a UDP datagram?                                                               | **Minimum:** 8 bytes (header only) <br> **Maximum:** 65,535 bytes                                                          |
| If a UDP datagram has a total length of 100 bytes, how many bytes are actual data?                                    | Data = 100 − 8 = **92 bytes**                                                                                              |
| A UDP message carries 16 bytes of data. Calculate efficiency at UDP level.                                            | $\text{Efficiency} = \frac{16}{16 + 8} = \frac{16}{24} = 66.67\%$                                                          |
| Same as above, but include IP header (20 bytes). Find efficiency.                                                     | $\text{Efficiency} = \frac{16}{16 + 8 + 20} = \frac{16}{44} = 36.36\%$                                                     |
| Same scenario, include Ethernet header (18 bytes). Find efficiency.                                                   | $\text{Efficiency} = \frac{16}{16 + 8 + 20 + 18} = \frac{16}{62} \approx 25.8\%$                                           |
| A UDP datagram is 2000 bytes. If the network MTU is 1500 bytes, what happens?                                         | IP will **fragment the UDP datagram** to fit MTU.                                                                          |
| A UDP packet arrives with destination port 53. What type of application is likely receiving it?                       | Port 53 → **DNS application**                                                                                              |
| Client IP: 10.0.0.1, Port: 5000 <br> Server IP: 8.8.8.8, Port: 53 <br> Write the socket pair.                         | (10.0.0.1 : 5000) → (8.8.8.8 : 53)                                                                                         |
| UDP length field = 60 bytes. Find header and data size.                                                               | Header = 8 bytes <br> Data = 60 − 8 = **52 bytes**                                                                         |
| If 5 UDP packets are sent and 2 are lost, what does the receiver do?                                                  | Receiver **does nothing** (no retransmission). Lost packets are ignored.                                                   |
| Why does UDP not guarantee delivery even though the underlying IP layer also provides best-effort service?            | Both UDP and IP are best-effort. UDP does not add any reliability mechanisms over IP, so delivery is not guaranteed.       |
| Explain how UDP achieves process-to-process communication without maintaining connection state.                       | UDP uses **port numbers** to identify processes, enabling direct delivery without maintaining connection state.            |
| Why is UDP suitable for multicasting but TCP is not?                                                                  | UDP supports **one-to-many communication (multicasting)**. TCP is strictly one-to-one (connection-oriented).               |
| Explain why UDP may lead to packet duplication.                                                                       | Due to retransmissions at lower layers or network duplication, UDP may deliver duplicate packets.                          |
| Why is UDP header size fixed, and how does this impact performance?                                                   | UDP header is fixed (8 bytes) for simplicity and speed → lower overhead and faster processing.                             |
| If UDP has no flow control, how can a receiver avoid being overwhelmed?                                               | Receiver may: <br> - Drop packets <br> - Use buffering <br> - Apply application-level flow control                         |
| Why is UDP preferred in routing protocols like RIP?                                                                   | Routing protocols (like RIP) require fast updates and can tolerate some loss → UDP is suitable.                            |
| Explain how UDP can be used in applications that require reliability.                                                 | Applications can add: <br> - Sequence numbers <br> - ACKs <br> - Retransmissions                                           |
| Why is it difficult to implement congestion control at the application layer over UDP?                                | Application lacks full network visibility, making congestion detection and control difficult.                              |
| Explain the role of the pseudoheader in UDP checksum calculation.                                                     | Pseudoheader includes IP addresses to detect errors in source/destination addressing.                                      |
| A video streaming application uses UDP. Suddenly, packet loss increases. What will be the visible effect to the user? | User sees glitches, missing frames, or brief quality drops.                                                                |
| A DNS server switches from UDP to TCP. What changes in performance and behavior would you expect?                     | - Increased delay (connection setup) <br> - Improved reliability <br> - More overhead                                      |
| A UDP-based application starts experiencing high delay. What could be the possible reasons?                           | - Network congestion <br> - Buffering delays <br> - Application processing delay                                           |
| If a UDP packet arrives out of order, what actions are possible at the application layer?                             | Application may: <br> - Reorder packets <br> - Drop out-of-order packets                                                   |
| A system receives UDP packets faster than it can process them. What happens internally?                               | Packets are dropped due to buffer overflow.                                                                                |
| A UDP datagram carries 500 bytes of data. Calculate efficiency at UDP level.                                          | $\text{Efficiency} = \frac{500}{500 + 8} \approx 98.4\%$                                                                   |
| A UDP datagram has total length 1200 bytes. Find header and data size.                                                | Header = 8 bytes <br> Data = 1200 − 8 = **1192 bytes**                                                                     |
| If an application sends 100 UDP packets of 100 bytes each, how much total header overhead is added?                   | Header per packet = 8 bytes <br> Total overhead = 100 × 8 = **800 bytes**                                                  |
| A UDP datagram of size 3000 bytes is sent over a network with MTU = 1000 bytes. How many fragments are created?       | Total = 3000 bytes, MTU = 1000 <br> Fragments ≈ **3 fragments**                                                            |
| If UDP header = 8 bytes and IP header = 20 bytes, what percentage of a 200-byte packet is overhead?                   | Overhead = 8 + 20 = 28 bytes <br> $\text{Overhead \%} = \frac{28}{200} = 14\%$                                             |
| Can UDP packets arrive faster than they are sent? Explain.                                                            | No. Packets cannot arrive faster than sent, but may appear bursty due to buffering.                                        |
| Is it possible for UDP to deliver duplicate packets? Why?                                                             | Yes, due to duplication in the network.                                                                                    |
| If the checksum is optional in UDP, what happens if it is disabled?                                                   | Errors may go undetected → corrupted data may be delivered.                                                                |
| Can UDP guarantee that no packets are lost in a perfect network? Explain.                                             | Yes, if the network is perfect (no loss, no errors).                                                                       |
| Why does UDP not reorder packets even if it detects disorder?                                                         | UDP does not maintain state or sequence numbers → cannot reorder packets.                                                  |
