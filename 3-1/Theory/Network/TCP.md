## Core TCP Questions

| **Question** | **Answer** |
|--------------|------------|
| What type of protocol is TCP? | TCP is a **connection-oriented, reliable transport protocol**. |
| Why is TCP called connection-oriented? | Because it establishes a connection using a **three-way handshake** before data transfer. |
| What is a TCP segment? | A **unit of data** consisting of header + data. |
| What is the size of TCP header? | **Minimum:** 20 bytes <br> **Maximum:** 60 bytes |
| Why does TCP use sequence numbers? | To ensure **ordered delivery** and detect **lost/duplicate segments**. |
| What is acknowledgment (ACK)? | A signal confirming **successful receipt of data**. |
| How does TCP ensure reliability? | Using **ACKs, retransmissions, sequence numbers, and checksum**. |
| What happens if a segment is lost? | It is **retransmitted** after timeout or 3 duplicate ACKs. |
| What is flow control in TCP? | Prevents sender from overwhelming receiver using **window size (rwnd)**. |
| What is congestion control? | Prevents **network overload** using cwnd and algorithms. |
| What is sliding window? | Technique allowing multiple bytes to be sent before receiving ACKs. |
| What is rwnd? | **Receiver window size** (receiver capacity). |
| What is cwnd? | **Congestion window size** (network capacity). |
| Effective window size? | **min(cwnd, rwnd)** |
| Does TCP preserve message boundaries? | **No**, it is **byte-oriented**. |
| What is MSS? | Maximum Segment Size (data only, no header). |

---

## Connection Management

| **Question** | **Answer** |
|--------------|------------|
| Explain three-way handshake. | SYN → SYN+ACK → ACK |
| Why is 3-way handshake needed? | To **synchronize sequence numbers** and avoid duplicates. |
| Why not 2-way handshake? | May accept **old duplicate requests**. |
| What is connection termination? | Done using **FIN handshake (3 or 4 steps)**. |
| What is half-close? | One side closes, other continues sending. |
| Why TIME-WAIT state? | To handle **delayed packets** and ensure ACK delivery. |

---

## TCP States

| **Question** | **Answer** |
|--------------|------------|
| What is ESTABLISHED state? | Data transfer phase. |
| FIN received in ESTABLISHED? | Send ACK → **CLOSE-WAIT** |
| Close requested? | Send FIN → **FIN-WAIT-1** |
| FIN-WAIT-1 + ACK received? | → **FIN-WAIT-2** |
| FIN received in FIN-WAIT-2? | Send ACK → **TIME-WAIT** |
| CLOSE-WAIT state? | Waiting for application to close |
| LAST-ACK state? | Waiting for final ACK |
| TIME-WAIT state? | Wait before closing connection |

---

## Reliability & Error Control

| **Question** | **Answer** |
|--------------|------------|
| What is checksum? | Used for **error detection** |
| What happens to corrupted segments? | Discarded and retransmitted |
| What is cumulative ACK? | ACK confirms all bytes up to a point |
| What are duplicate ACKs? | Indicate possible **packet loss** |
| What is fast retransmission? | Retransmit after **3 duplicate ACKs** |

---

## Congestion Control

| **Question** | **Answer** |
|--------------|------------|
| What are TCP congestion phases? | Slow Start, Congestion Avoidance, Detection |
| Why exponential growth in slow start? | Quickly utilize bandwidth |
| Why linear growth later? | Avoid sudden congestion |
| What happens on timeout? | Restart **slow start** |
| What happens on 3 duplicate ACKs? | Fast recovery |

---

## Timers

| **Question** | **Answer** |
|--------------|------------|
| What is RTT? | Round Trip Time |
| What is RTO? | Retransmission Timeout |
| Why multiple timers? | Handle retransmission, persistence, keepalive, termination |
| What is keepalive timer? | Checks if connection is alive |
| What is persistence timer? | Prevents deadlock when rwnd = 0 |

---

## Advanced TCP Concepts

| **Question** | **Answer** |
|--------------|------------|
| What is byte-oriented protocol? | Data treated as continuous stream |
| What is segmentation? | Breaking data into segments |
| What is piggybacking? | Sending ACK with data |
| What is SACK? | Selective acknowledgment of segments |
| What is Nagle’s algorithm? | Combines small packets |
| What is silly window syndrome? | Sending very small segments |

---

## Numerical / Logic-Based Questions

| **Question** | **Answer** |
|--------------|------------|
| If ISN = 1000, what is seq of SYN? | **1000** |
| ACK after SYN? | **1001** |
| Data = 500 bytes, next ACK? | **1501** |
| Window = 5000, unACKed = 2000 → allowed? | **3000 bytes** |
| SYN consumes sequence number? | **Yes (1)** |
| FIN consumes sequence number? | **Yes (1)** |

---

## Conceptual Edge Cases

| **Question** | **Answer** |
|--------------|------------|
| Can TCP deliver out-of-order data? | **No**, it buffers |
| What if ACK is lost? | Segment retransmitted |
| What if FIN is lost? | Retransmitted |
| Can TCP duplicate packets? | Yes, but duplicates are discarded |
| Why TCP slower than UDP? | Due to reliability mechanisms |

---

## Security & Special Cases

| **Question** | **Answer** |
|--------------|------------|
| What is SYN flooding? | Attack using many incomplete connections |
| How prevent SYN flood? | SYN cookies |
| What is simultaneous open? | Both sides send SYN |
| What is simultaneous close? | Both sides send FIN |

---

## Application-Based Questions

| **Question** | **Answer** |
|--------------|------------|
| Why TCP used in FTP/HTTP? | Requires reliability |
| Why not TCP for real-time apps? | Delay due to retransmission |
| When is TCP preferred? | Large, reliable data transfer |
| When is TCP disadvantage? | Real-time systems (delay sensitive) |

---

## Efficiency Questions

| **Question** | **Answer** |
|--------------|------------|
| Data = 20 bytes, header = 20 bytes → efficiency? | 50% |
| Include IP (20 bytes)? | 20 / 60 = **33.3%** |
| Include Ethernet (18 bytes)? | 20 / 78 ≈ **25.6%** |

---

## Final Summary

- TCP = **Reliable, connection-oriented**
- Uses **FSM + sliding window**
- Provides:
  - Flow control
  - Congestion control
  - Error control
- Slower than UDP but **guarantees delivery**

## Advanced TCP Conceptual Q&A (Exam-Level)

| **Question** | **Answer** |
|--------------|------------|
| Why does TCP use a 3-way handshake instead of 2-way? | To prevent **old duplicate connection requests** and ensure both sides agree on initial sequence numbers. |
| What problem occurs if sequence numbers are not randomized? | Attackers can **predict sequence numbers** → leads to session hijacking. |
| Why does SYN consume one sequence number? | SYN is treated as a **virtual byte** to synchronize sequence spaces. |
| Why does FIN also consume one sequence number? | FIN represents **end of data stream**, so it occupies one sequence space. |
| Why is TCP byte-oriented instead of message-oriented? | To provide **flexibility and efficient streaming** without message boundaries. |
| If TCP ensures reliability, why are duplicate packets still possible? | Network duplication or retransmissions may occur; TCP **detects & discards duplicates**. |
| Why does TCP not send ACK for every segment separately? | Uses **cumulative ACKs** to reduce overhead. |
| What happens if an ACK is lost? | Sender retransmits data after timeout; receiver discards duplicates. |
| Why is cumulative ACK sometimes inefficient? | Cannot indicate **which specific segment is lost** (fixed by SACK). |
| Why does TCP buffer out-of-order segments? | To **maintain in-order delivery** to application. |
| Why doesn't TCP immediately retransmit on first duplicate ACK? | Could be due to **reordering**, not loss → waits for 3 duplicate ACKs. |

---

##  Flow Control & Window Tricks

| **Question** | **Answer** |
|--------------|------------|
| Why does TCP use sliding window instead of stop-and-wait? | Improves **throughput** by allowing multiple segments in transit. |
| What happens if receiver advertises window = 0? | Sender stops sending → uses **persistence timer** to probe. |
| What is the danger of zero window without persistence timer? | **Deadlock** (sender waits forever). |
| Why can sender not always send full window size? | Limited by **min(cwnd, rwnd)** |
| If rwnd >> cwnd, what limits transmission? | **cwnd (network capacity)** |
| If cwnd >> rwnd, what limits transmission? | **rwnd (receiver capacity)** |
| Why is flow control not enough to prevent congestion? | Flow control handles receiver, not **network congestion**. |

---

##  Congestion Control Deep Tricks

| **Question** | **Answer** |
|--------------|------------|
| Why does slow start use exponential growth? | Quickly reach available bandwidth. |
| Why is exponential growth dangerous? | Can **overshoot capacity → congestion** |
| Why switch to linear growth later? | To **stabilize transmission rate** |
| Difference between timeout vs 3 duplicate ACK reaction? | Timeout = severe congestion → reset cwnd <br> 3 dup ACK = mild → fast recovery |
| Why is timeout considered worse than duplicate ACK? | Indicates **no packets getting through** |
| What is AIMD? | Additive Increase, Multiplicative Decrease |
| Why multiplicative decrease? | Quickly reduce load during congestion |
| Can TCP cause congestion collapse? | Yes, due to **excess retransmissions** |

---

##  Reliability Edge Cases

| **Question** | **Answer** |
|--------------|------------|
| Can TCP lose data despite reliability? | Only if connection breaks permanently |
| What if retransmitted packet also gets lost? | Retransmitted again after timeout |
| Why does TCP not use negative acknowledgments? | Uses **duplicate ACKs instead** |
| Can ACKs be lost without issue? | Yes, handled via retransmission |
| What happens if both data and ACK are lost? | Sender times out and retransmits |
| Why is checksum still needed if reliability exists? | To detect **bit errors** before retransmission |

---

##  Connection Management Traps

| **Question** | **Answer** |
|--------------|------------|
| Why is TIME-WAIT needed? | To ensure **delayed packets don’t corrupt new connection** |
| Why is TIME-WAIT = 2 × MSL? | To cover full round-trip packet lifetime |
| What happens if TIME-WAIT is skipped? | Old packets may interfere with new connection |
| Why can server avoid TIME-WAIT sometimes? | Client usually enters TIME-WAIT |
| What is half-open connection? | One side thinks connection exists, other does not |
| What causes half-open connections? | Crash or network failure |

---

##  Tricky Behavior Questions

| **Question** | **Answer** |
|--------------|------------|
| Can TCP send data before connection is fully established? | **No** |
| Can TCP receive data after sending FIN? | Yes (**half-close**) |
| Can TCP reorder packets? | Internally yes, but delivers in order |
| Can TCP send empty segments? | Yes (ACK-only segments) |
| Why does TCP delay ACK sometimes? | To allow **piggybacking** |
| What is piggybacking benefit? | Reduces overhead |

---

##  Numerical / Logic Traps

| **Question** | **Answer** |
|--------------|------------|
| Seq = 1000, data = 200 → next seq? | **1200** |
| ACK = 1200 means? | Bytes up to 1199 received |
| Window = 4000, sent = 2500 → remaining? | **1500 bytes** |
| 3 duplicate ACKs → action? | **Fast retransmit** |
| Timeout → action? | Restart slow start |
| SYN seq = x → ACK = ? | **x + 1** |
| FIN seq = y → ACK = ? | **y + 1** |

---

##  Conceptual Comparisons

| **Question** | **Answer** |
|--------------|------------|
| Why TCP slower than UDP? | Due to **ACKs, retransmission, congestion control** |
| Why TCP not used in live streaming? | Retransmission causes **delay** |
| Why TCP good for file transfer? | Ensures **complete and ordered delivery** |
| Why TCP cannot support multicast? | It is **point-to-point connection-based** |

---

##  Ultra-Tricky Exam Questions

| **Question** | **Answer** |
|--------------|------------|
| Can TCP ACK a packet it hasn’t received? | Yes (duplicate ACK for last in-order byte) |
| Why 3 duplicate ACKs, not 2? | To avoid false retransmission due to reordering |
| What happens if duplicate ACKs keep coming? | Sender keeps fast retransmitting (until recovery) |
| Why does TCP not shrink window abruptly? | To avoid instability |
| Can TCP window size become zero? | Yes (receiver full) |
| Why is TCP full-duplex? | Both sides send/receive independently |
| What happens if application reads data slowly? | Receiver window shrinks → sender slows |

---

##  Final Memory Triggers

- TCP = **Reliable + Ordered + Controlled**
- Uses:
  - Sequence numbers
  - ACKs
  - Sliding window
  - Congestion control
- Key risks:
  - Delay
  - Overhead
  - Complexity
