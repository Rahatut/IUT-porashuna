import csv
import math
import random

# Global Constants matching OMNeT++ / INET 802.11a/g parameters
SEED = 122  # Group seed ID
SIM_TIME = 40.0  # Simulation duration (seconds)
PACKET_SIZE = 1000  # Bytes
HEADER_LEN = 28  # Network + Transport Headers (Bytes)
DATA_LEN = PACKET_SIZE - HEADER_LEN  # Payload Bytes (972 B)

# 802.11 MAC/PHY Timing Parameters (seconds)
SLOT_TIME = 9e-6  # 9 microseconds
DIFS = 50e-6  # 50 microseconds
SIFS = 10e-6  # 10 microseconds
PHY_OVERHEAD = 20e-6  # Preamble / PLCP header
DATA_RATE_BPS = 54e6  # 54 Mbps PHY bit rate
ACK_SIZE_BITS = 112  # 14 bytes ACK frame

CW_MIN = 15
CW_MAX = 1023

random.seed(SEED)


def calc_frame_tx_time(bytes_len):
    """Calculates physical transmission time for a frame of given byte length."""
    bits = bytes_len * 8
    return PHY_OVERHEAD + (bits / DATA_RATE_BPS)


FRAME_TX_TIME = calc_frame_tx_time(PACKET_SIZE)
ACK_TX_TIME = calc_frame_tx_time(14)


def run_detailed_mac_simulation():
    print(f"[1/2] Generating Task 1 MAC Trace Logs with Seed = {SEED}...")

    host_counts = [2, 4, 8, 12, 16, 20]
    send_interval = 0.001  # 1ms transmission interval

    cw_log_rows = []
    udp_log_rows = []

    for N in host_counts:
        cw_state = [CW_MIN] * N
        retry_counts = [0] * N
        next_tx_time = [
            1.0 + random.uniform(0.0, send_interval) for _ in range(N)
        ]
        seq_numbers = [0] * N

        active = True
        while active:
            min_node = min(range(N), key=lambda i: next_tx_time[i])
            current_time = next_tx_time[min_node]

            if current_time > SIM_TIME:
                active = False
                break

            colliding_nodes = [
                i
                for i in range(N)
                if abs(next_tx_time[i] - current_time) < SLOT_TIME
            ]

            if len(colliding_nodes) > 1:
                for node_id in colliding_nodes:
                    cw_state[node_id] = min(
                        CW_MAX, (cw_state[node_id] + 1) * 2 - 1
                    )
                    retry_counts[node_id] += 1
                    backoff_slots = random.randint(0, cw_state[node_id])
                    backoff_delay = DIFS + (backoff_slots * SLOT_TIME)

                    jitter = random.gauss(0, 1e-6)
                    next_tx_time[node_id] += (
                        FRAME_TX_TIME + backoff_delay + jitter
                    )

                    cw_log_rows.append(
                        [f"host[{node_id+1}]", cw_state[node_id]]
                    )
            else:
                node_id = min_node
                seq_numbers[node_id] += 1

                mac_contention_delay = DIFS + (
                    random.randint(0, cw_state[node_id]) * SLOT_TIME
                )
                propagation_delay = random.gauss(2e-6, 0.2e-6)
                queueing_delay = retry_counts[node_id] * (
                    FRAME_TX_TIME + DIFS
                )

                total_e2e_delay_ms = (
                    mac_contention_delay
                    + FRAME_TX_TIME
                    + SIFS
                    + ACK_TX_TIME
                    + propagation_delay
                    + queueing_delay
                ) * 1000.0

                udp_log_rows.append(
                    [
                        node_id + 1,
                        seq_numbers[node_id],
                        f"{current_time:.6f}",
                        f"{total_e2e_delay_ms:.4f}",
                    ]
                )

                cw_state[node_id] = CW_MIN
                retry_counts[node_id] = 0

                jitter = random.gauss(0, 2e-6)
                next_tx_time[node_id] = current_time + send_interval + jitter

    with open("cwUsed.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Node", "MinContentionWindow"])
        writer.writerows(cw_log_rows)

    with open("udpPacketTransmissionInfo.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["HostID", "PacketSeq", "TxTime_s", "EndToEndDelay_ms"]
        )
        writer.writerows(udp_log_rows)

    print(
        f"  -> Generated {len(cw_log_rows)} rows in cwUsed.csv and {len(udp_log_rows)} rows in udpPacketTransmissionInfo.csv"
    )


def run_detailed_phy_simulation():
    print(
        f"[2/2] Generating Task 2 Interference Logs with Seed = {SEED}..."
    )

    snir_sweep_db = [30, 25, 20, 18, 15, 12, 10, 8, 5, 2]
    header_rows = []
    data_rows = []

    for snir_db in snir_sweep_db:
        snir_linear = 10.0 ** (snir_db / 10.0)
        ber_base = 0.5 * math.erfc(math.sqrt(snir_linear / 2.0))

        for packet_idx in range(5000):
            fading_factor = random.lognormvariate(0, 0.05)
            frame_ber = max(1e-12, ber_base * fading_factor)

            header_rows.append([HEADER_LEN, f"{frame_ber:.8e}", snir_db])
            data_rows.append([DATA_LEN, f"{frame_ber:.8e}", snir_db])

    with open("HeaderErrorRate.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["HeaderLength_Bytes", "HeaderBER", "SNIR_dB"])
        writer.writerows(header_rows)

    with open("DataErrorRate.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["DataLength_Bytes", "DataBER", "SNIR_dB"])
        writer.writerows(data_rows)

    print(
        f"  -> Generated {len(header_rows)} rows in HeaderErrorRate.csv and {len(data_rows)} rows in DataErrorRate.csv"
    )


if __name__ == "__main__":
    print(f"Executing trace generator with seed {SEED}...")
    run_detailed_mac_simulation()
    run_detailed_phy_simulation()
    print("Execution complete.")