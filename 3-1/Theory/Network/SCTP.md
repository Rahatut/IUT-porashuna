##  SCTP Advanced Conceptual Q&A

| **Question** | **Answer** |
|--------------|------------|
| What type of protocol is SCTP? | **Message-oriented, reliable, connection-oriented (association-based)** protocol |
| What is an SCTP connection called? | **Association** |
| How is SCTP different from TCP? | SCTP is **message-oriented + multistream + multihoming**, TCP is byte-oriented |
| What is a chunk in SCTP? | Basic unit carrying **control or data** inside a packet |
| Can a DATA chunk carry multiple messages? | **No**, one chunk = one message |
| Can a message span multiple chunks? | **Yes (fragmentation)** |

---

##  Identifiers (VERY IMPORTANT)

| **Question** | **Answer** |
|--------------|------------|
| What is TSN? | **Transmission Sequence Number** (for reliability) |
| What is SI? | **Stream Identifier** (identifies stream) |
| What is SSN? | **Stream Sequence Number** (order within stream) |
| Why 3 identifiers? | To support **multistreaming + ordering + reliability** |

---

##  Flow Control Deep Concepts

| **Question** | **Answer** |
|--------------|------------|
| What is rwnd? | Receiver window size |
| What is inTransit? | Bytes sent but not yet acknowledged |
| When can sender send data? | If **rwnd − inTransit > 0** |
| What happens if rwnd = 0? | Sender is **blocked** (except probe cases) |
| Why is sender blocked even if it has data? | Receiver buffer is full |
| What happens after SACK with rwnd = 0? | Sender **stops transmission** |

---

##  SACK (Selective ACK) Tricks

| **Question** | **Answer** |
|--------------|------------|
| What does SACK contain? | cumTSN, gap blocks, duplicates, rwnd |
| What is cumTSN? | Last **in-order received chunk** |
| What are gap ACK blocks? | Out-of-order received chunks |
| Why report duplicates? | Helps sender detect **retransmission issues** |
| Are control chunks acknowledged? | Not by SACK; use **other control chunks** |

---

##  Receiver-Side Behavior

| **Question** | **Answer** |
|--------------|------------|
| Does receiver store out-of-order chunks? | **Yes** |
| What happens to duplicates? | **Discarded but tracked** |
| Why leave gaps in buffer? | To preserve ordering |
| When is SACK sent immediately? | Out-of-order or duplicate chunks |
| What is winSize? | Available buffer space |

---

##  Sender-Side Behavior

| **Question** | **Answer** |
|--------------|------------|
| How many queues at sender? | **Two: sending + retransmission** |
| Which queue has priority? | **Retransmission queue** |
| What are outstanding chunks? | Sent but not yet acknowledged |
| What is curTSN? | Next chunk to send |
| Are retransmission chunks counted in inTransit? | **No (assumed lost)** |

---

##  SACK Processing (VERY TRICKY)

| **Question** | **Answer** |
|--------------|------------|
| What happens to chunks ≤ cumTSN? | Removed from queues |
| What happens to chunks in gap blocks? | Removed (considered received) |
| Do duplicates affect sender? | **No direct effect** |
| What happens to rwnd after SACK? | Updated using advertised value |
| What happens when timer expires? | Chunks → retransmission queue |

---

##  Sending Data Logic

| **Question** | **Answer** |
|--------------|------------|
| When can sender send chunks? | If data exists AND **rwnd − inTransit allows** |
| Which chunks sent first? | **Retransmission queue first** |
| Can both queues be mixed? | Sometimes yes (implementation dependent) |
| What limits packet size? | **MTU + rwnd − inTransit** |
| Are outstanding chunks resent immediately? | **No** |

---

##  Retransmission Mechanisms

| **Question** | **Answer** |
|--------------|------------|
| What triggers retransmission? | Timer expiry OR 4 missing reports |
| Why 4 SACKs (not 3 like TCP)? | SCTP design choice (more robust detection) |
| What is RTO based on? | RTT, RTT variation |
| Does SCTP use Karn’s algorithm? | **Yes** |
| In multihoming, RTO? | Separate RTO per path |

---

##  SACK Generation Rules (IMPORTANT)

| **Question** | **Answer** |
|--------------|------------|
| When must SACK be sent? | When sending DATA |
| If no data to send? | Send SACK within **~500 ms** |
| Minimum SACK frequency? | At least **one per two packets** |
| Out-of-order arrival? | Send SACK **immediately** |
| Duplicate chunks? | Report immediately via SACK |

---

##  Congestion Control

| **Question** | **Answer** |
|--------------|------------|
| Does SCTP use TCP-like congestion control? | **Yes** |
| Phases? | Slow start, congestion avoidance, detection |
| What is special in SCTP? | **Separate cwnd per path (multihoming)** |
| What is ECN? | Explicit congestion notification |
| What are ECNE & CWR? | Signals for congestion handling |

---

##  Security Concepts

| **Question** | **Answer** |
|--------------|------------|
| What prevents SYN flood-like attacks? | **Cookie mechanism** |
| What is verification tag? | Prevents insertion attacks |
| Why 4-way handshake? | More secure than TCP |

---

##  Association Management

| **Question** | **Answer** |
|--------------|------------|
| How many steps in establishment? | **4 (INIT, INIT-ACK, COOKIE-ECHO, COOKIE-ACK)** |
| How many steps in termination? | **3 (SHUTDOWN based)** |
| What is COOKIE-WAIT state? | Waiting for INIT-ACK |
| What is COOKIE-ECHOED state? | Waiting for COOKIE-ACK |
| What is ESTABLISHED? | Data transfer phase |

---

##  Ultra-Tricky Concepts

| **Question** | **Answer** |
|--------------|------------|
| Why SCTP better than TCP for multimedia? | **Multistreaming avoids head-of-line blocking** |
| Why multihoming useful? | Provides **fault tolerance** |
| Can SCTP avoid head-of-line blocking? | **Yes (per stream)** |
| Why message-oriented important? | Preserves **message boundaries** |
| Why SCTP complex? | Supports multiple advanced features |

---

##  Exam Trap Questions

| **Question** | **Answer** |
|--------------|------------|
| Can SCTP send when rwnd = 0? | Only special probe cases |
| Are retransmission chunks in-flight? | **No** |
| Does SCTP reorder data? | Maintains order per stream |
| Can duplicate chunks be delivered? | **No** |
| Does SCTP acknowledge control chunks via SACK? | **No** |

---

##  Final Memory Triggers

- SCTP = **TCP + UDP + Advanced Features**
- Key features:
  - Multistreaming
  - Multihoming
  - Message-oriented
- Uses:
  - TSN (reliability)
  - SI/SSN (stream control)
  - SACK (advanced ACK)
