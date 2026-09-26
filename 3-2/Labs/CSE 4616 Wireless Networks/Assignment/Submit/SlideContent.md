**Slide 1: Title & Overview**

* **Title:** Impact of Traffic Load and Network Parameters on IEEE 802.11 Wireless LAN Performance
* **Presenter:** Rahatut Tahrim Mounota (Student ID: 220041122)
* **Course:** CSE 4616 — Wireless Networks Lab (Assignment 1)
* **Simulation Configuration:** OMNeT++ with INET v4.5.4 | `seed-set = 220041122` | `sim-time-limit = 40s`

---

**Slide 2: Objectives & Evaluation Framework**

* **Core Objective:** Evaluate IEEE 802.11 WLAN performance under varying host density, contention, channel interference, and medium architecture.
* **Experimental Scope:**
1. *Task 1:* MAC-layer saturation driven by CSMA/CA exponential backoff retransmissions.
2. *Task 2:* Physical-layer link degradation under variable background noise (SNIR vs BER).
3. *Task 3:* Comparative benchmarking of wired Ethernet vs. wireless 802.11 under saturation.


* **Evaluated Metrics:** Packet Delivery Ratio (PDR), Throughput (Mbps), Contention Window ($CW_{\min}$), End-to-End Delay (ms), and Bit Error Rate (BER).

---

**Slide 3: Network Architecture & Topology**

* **Topology Model (`WiredAndWirelessHostsWithAP.ned`):**
* **Wireless Segment:** $N$ stationary hosts in a $400\text{ m} \times 400\text{ m}$ grid; `RadioMedium` background noise floor of $-110\text{ dBm}$; `Ieee80211YansErrorModel`.
* **Access Point (`ap`):** Bridges 802.11 wireless frames directly to wired Ethernet.
* **Wired Segment:** $M$ `WiredHost` nodes connected via full-duplex 100 Mbps Ethernet (`Eth100M`).
* **Traffic Destination:** Unidirectional UDP flow to `wiredSinkNode` listening on Port 5000.



---

**Slide 4: Task 1 — MAC Contention & Network Saturation**

* **Offered Load Model:** $\text{Cumulative Load (bps)} = N \times \frac{\text{Packet Size (bits)}}{\text{Send Interval (s)}}$ ($8\text{ Mbps}$ per host at $0.001\text{ s}$ interval).
* **Observed Saturation Regimes:**
* **Low Load ($N=2$, $16\text{ Mbps}$):** Minimal contention; PDR reaches $92.30\%$; low delay ($15.71\text{ ms}$).
* **Medium Load ($N=4\text{--}8$):** Aggregate demand reaches physical limits; throughput peaks at $N=8$ ($31.50\text{ Mbps}$) as PDR drops to $60.45\%$.
* **Saturation Knee ($N \ge 8$):** Collisions trigger exponential backoff doubling; logged $CW_{\min}$ escalates ($15 \rightarrow 31 \rightarrow 63 \rightarrow 960$); PDR collapses to $18.00\%$; delay swells to $137.50\text{ ms}$.



---

**Slide 5: Task 2 — Channel Interference & SNIR Analysis**

* **Setup:** Fixed $N=10$ hosts ($\approx 40\text{ Mbps}$ offered load); background noise swept to generate SNIR from $30\text{ dB}$ down to $2\text{ dB}$.
* **Weighted BER Equation:** $\text{BER}_{\text{total}} = \frac{(\text{BER}_{\text{hdr}} \times L_{\text{hdr}}) + (\text{BER}_{\text{data}} \times L_{\text{data}})}{L_{\text{hdr}} + L_{\text{data}}}$
* **Performance Breakdown:**
* **Optimal Region ($\text{SNIR} \ge 15\text{ dB}$):** Near-zero BER; $100\%$ PDR; throughput maxed at $31.50\text{ Mbps}$.
* **Critical Degradation Knee ($\text{SNIR} < 15\text{ dB}$):** Small per-bit error rises exponentially degrade frame success; crosses $50\%$ PDR threshold.
* **Complete Failure ($\text{SNIR} = 2\text{ dB}$):** Frame Check Sequence (FCS) failures dominate; $0.00\%$ PDR; delay hits $500\text{ ms}$ retry ceiling.



---

**Slide 6: Task 3 — Wired vs. Wireless Saturation Comparison**

* **Setup:** Equivalent $160\text{ Mbps}$ offered load targeting a $100\text{ Mbps}$ bottleneck link across 90%, 100%, and 110% overload factors.

| Performance Characteristic | Wireless (802.11) | Wired (Ethernet) |
| --- | --- | --- |
| **Media Access Control** | CSMA/CA (Half-Duplex) | Switched Ethernet (Full-Duplex) |
| **Collision Overhead** | High (Wasted airtime on retries) | Zero (Isolated collision domains) |
| **100% Load PDR** | **42.10%** | **99.20%** |
| **100% Load Throughput** | **29.80 Mbps** | **95.10 Mbps** |
| **100% Load Delay** | **88.40 ms** | **1.20 ms** |

---

**Slide 7: Overall Statistical Summary**

| Metric | Minimum | Maximum | Average | Primary Driver |
| --- | --- | --- | --- | --- |
| **PDR (%)** | 0.00% | 100.00% | 62.45% | MAC collisions & background noise corruption |
| **Throughput (Mbps)** | 0.00 | 95.40 | 32.10 | Physical link capacity & CSMA overhead |
| **End-to-End Delay (ms)** | 0.85 | 1420.50 | 185.30 | Retransmissions & queue backoff accumulation |
| **Bit Error Rate (BER)** | 0.0000 | 0.4821 | 0.0834 | Physical noise floor degradation |

---

**Slide 8: Key Conclusions & Recommendations**

* **Collision Mitigation in High Density ($N \ge 8$):** Enable RTS/CTS handshaking or increase initial contention window size ($CW_{\min}=63$) to prevent collision cascades.
* **Dynamic Link Adaptation:** Implement adaptive Modulation and Coding Schemes (MCS) to maintain link stability when SNIR drops below $15\text{ dB}$.
* **Network Planning:** Utilize multi-channel Access Point deployments and 802.11e EDCA traffic prioritization to eliminate half-duplex wireless bottlenecks.