
## Core Concepts

|Question|Answer|
|---|---|
|Can two processes on the same host communicate using sockets?|No. They use **inter-process communication (IPC)**, not network sockets.|
|If an application uses UDP, can it still achieve reliability?|Yes, but **reliability must be implemented at the application layer**.|
|Does the application layer guarantee data delivery?|No. It **depends on the transport layer (TCP/UDP)**.|
|Can an application directly control the network layer?|No. It only interacts via the **transport layer through sockets**.|

---

## Client-Server vs P2P Traps

|Question|Answer|
|---|---|
|Can a P2P system have client and server processes?|Yes. A peer can act as **both client and server simultaneously**.|
|Is a server always a powerful machine?|No. It is defined by its **role (always-on service provider)**, not hardware.|
|Can a client act as a server in client-server architecture?|No, roles are **strictly separated** in pure client-server models.|
|Why is P2P considered self-scalable?|Because **each new peer adds both load and capacity**.|

---

##  Socket & Addressing Traps

|Question|Answer|
|---|---|
|If two processes have the same port number, will conflict occur?|No, if they are on **different hosts (different IPs)**.|
|Can two processes on the same host use the same port?|No, **port numbers must be unique per host per protocol**.|
|Is IP address sufficient for process identification?|No, requires **IP + port number**.|
|What happens if a message arrives at correct IP but wrong port?|It is **discarded (no matching process)**.|

---

##  Protocol Design Traps

|Question|Answer|
|---|---|
|Can two applications communicate without a defined protocol?|No, both sides must follow a **common protocol definition**.|
|Is message format important if both ends understand data?|Yes, **syntax must be standardized** for interoperability.|
|Can proprietary protocols interoperate with open protocols?|Generally no, unless **explicitly designed for compatibility**.|
|What happens if semantics are misunderstood?|Communication becomes **logically incorrect even if delivery succeeds**.|

---

##  Transport Requirement Traps

|Question|Answer|
|---|---|
|Can a real-time app use TCP?|Yes, but **performance may degrade due to delay**.|
|Can a file transfer app use UDP?|Yes, but it must implement **its own reliability mechanisms**.|
|Does high throughput guarantee low delay?|No, throughput and delay are **independent metrics**.|
|Are all applications sensitive to delay?|No, only **real-time applications** are delay-sensitive.|

---

##  TCP vs UDP Traps

|Question|Answer|
|---|---|
|Does UDP have zero overhead?|No, it has **minimal but non-zero overhead**.|
|Is UDP always faster than TCP?|Not always; depends on **network conditions and application design**.|
|Can TCP lose data?|No, it ensures **reliable delivery**, but may retransmit.|
|Does UDP guarantee order?|No, packets may arrive **out of order**.|

---

##  HTTP Tricky Concepts

|Question|Answer|
|---|---|
|If HTTP is stateless, how do websites remember users?|Using **cookies or other mechanisms**.|
|Does stateless mean no memory at all?|Only at **protocol level**, not at application level.|
|Can HTTP work without TCP?|No, HTTP **relies on TCP for transport** (except newer versions like QUIC-based HTTP/3).|
|Is each HTTP request independent?|Yes, in **stateless HTTP design**.|

---

##  Persistent vs Non-Persistent HTTP

|Question|Answer|
|---|---|
|Does persistent HTTP eliminate RTT delay?|No, it **reduces but does not eliminate RTT**.|
|Can non-persistent HTTP use parallel connections?|Yes, browsers often open **multiple parallel TCP connections**.|
|Is persistent HTTP always faster?|Generally yes, but depends on **network and server behavior**.|
|Does one TCP connection mean one object always?|No, only in **non-persistent HTTP**.|

---

##  Cookies & State Traps

|Question|Answer|
|---|---|
|Are cookies stored on server only?|No, stored on **client (browser) and server database**.|
|Can cookies exist without backend database?|Limited use; meaningful tracking requires **server-side mapping**.|
|Do cookies violate HTTP statelessness?|No, they **work around it**, not violate it.|
|Can users disable cookies?|Yes, which may break **session-based services**.|

---

##  Advanced Traps (Very Likely in Exams)

|Question|Answer|
|---|---|
|If TCP provides reliability, why do applications still need logic?|For **application-specific correctness (e.g., ordering, semantics)**.|
|Can an application require both low delay and reliability?|Yes, but it's a **design trade-off** (hard to achieve perfectly).|
|Why is HTTP called an application-layer protocol if it uses TCP?|Because it defines **application-level message exchange**, not transport.|
|Can multiple applications share one TCP connection?|Generally no, each connection is tied to **specific socket pair**.|

---

# Final Trap Summary (Memory Boost)

- Socket ≠ Process → it is an **interface**
    
- IP alone ≠ identification → need **port**
    
- HTTP stateless ≠ no memory → cookies exist
    
- UDP unreliable ≠ unusable → app can add reliability
    
- TCP reliable ≠ fast → may introduce delay
    
- P2P ≠ no structure → still has roles
    


---

##  Deep Core Concepts

|Question|Answer|
|---|---|
|Why is the application layer independent of the network core?|Because applications run only on **end systems**, enabling rapid development without modifying network infrastructure.|
|Can two applications communicate without using sockets?|No, sockets are the **mandatory interface to the transport layer**.|
|Why is protocol design critical in application layer?|Because both ends must **agree on syntax, semantics, and timing rules** for correct communication.|

---

##  Subtle Process-Level Traps

|Question|Answer|
|---|---|
|Why is IP address alone insufficient for process communication?|Because multiple processes run on the same host; **port numbers distinguish them**.|
|What happens if two applications use the same port on the same host?|It causes a **binding conflict**, preventing one application from running.|
|Can a process act as both client and server simultaneously?|Yes, especially in **P2P architectures**.|

---

##  Architecture-Level Insights

|Question|Answer|
|---|---|
|Why is P2P considered scalable despite lack of central control?|Because each new peer contributes **both resources and demand**.|
|What is the biggest drawback of P2P systems?|**Dynamic membership and management complexity**.|
|Why are client-server systems easier to manage?|Due to **centralized control and predictable server behavior**.|

---

##  Transport Interaction Traps

|Question|Answer|
|---|---|
|Why doesn’t the application layer ensure reliability?|Reliability is delegated to the **transport layer (e.g., TCP)**.|
|Why might an application avoid TCP despite needing reliability?|Because TCP may introduce **delay due to retransmissions and congestion control**.|
|Can UDP-based applications be reliable?|Yes, if reliability is **implemented at the application level**.|

---

##  HTTP Deep Understanding

|Question|Answer|
|---|---|
|Why is HTTP designed as stateless?|To ensure **simplicity, scalability, and fault tolerance**.|
|What problem arises from statelessness?|Inability to track **user sessions across requests**.|
|Why is TCP necessary for HTTP?|HTTP relies on TCP for **reliable and ordered data delivery**.|

---

##  Persistent vs Non-Persistent (Trap Concepts)

|Question|Answer|
|---|---|
|Why is non-persistent HTTP inefficient?|Each object requires a **new TCP connection (high RTT overhead)**.|
|Does persistent HTTP eliminate delay?|No, it **reduces connection overhead but still incurs RTT delays**.|
|Why do browsers open parallel TCP connections?|To **reduce total page load time** in non-persistent HTTP.|

---

##  Cookies & State (Very Tricky)

|Question|Answer|
|---|---|
|Do cookies make HTTP stateful?|No, they **simulate state at application level**.|
|Where is cookie information stored?|In both **client (browser) and server database**.|
|Why are cookies considered a privacy concern?|They enable **tracking of user behavior across sessions and sites**.|

---

##  Application Requirements (Deep Logic)

|Question|Answer|
|---|---|
|Why can multimedia applications tolerate loss but not delay?|Because **timeliness is more critical than perfect accuracy**.|
|Why do file transfer applications require reliability?|Because **data integrity is essential**.|
|What is the trade-off between throughput and delay?|Higher throughput does not guarantee **lower latency**.|

---

##  Protocol Design Edge Cases

|Question|Answer|
|---|---|
|What happens if message syntax is correct but semantics are wrong?|Communication succeeds technically but **fails logically**.|
|Why must protocols define timing rules?|To ensure **proper coordination of message exchange**.|
|Can two systems communicate with different protocol versions?|Only if **backward compatibility is supported**.|

---

##  Advanced Insight 

|Question|Answer|
|---|---|
|Why is application-layer flexibility both an advantage and a risk?|It allows innovation but may cause **incompatibility and security issues**.|
|Why is UDP still widely used despite no reliability?|Because some applications prioritize **speed and low latency over correctness**.|
|Why is layering important in networking?|It provides **modularity, abstraction, and easier troubleshooting**.|

---

# Final Mental Traps (Must Remember)

- Stateless ≠ no memory → cookies exist
    
- Socket ≠ port → socket is interface
    
- TCP reliable ≠ fast
    
- UDP unreliable ≠ useless
    
- IP identifies host, not process
    
- Delivery success ≠ communication correctness
    

---
