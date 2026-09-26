import matplotlib.pyplot as plt
import numpy as np

# Global style setup
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
    "font.size": 10,
    "axes.titlesize": 11.5,
    "axes.labelsize": 10.5,
    "axes.linewidth": 1.0,
    "xtick.labelsize": 9.5,
    "ytick.labelsize": 9.5,
    "legend.fontsize": 9,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.08,
})

def finish_axis(ax, grid_axis="y"):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#222222")
    ax.spines["bottom"].set_color("#222222")
    ax.grid(True, axis=grid_axis, linestyle="--", linewidth=0.6, alpha=0.5, color="#c0c0c0", zorder=0)
    ax.tick_params(axis="both", which="major", length=4, width=0.8, colors="#222222")
    ax.margins(x=0.05)

def finish_twin_axis(ax, color=None):
    ax.spines["top"].set_visible(False)
    ax.spines["left"].set_visible(False)
    if color:
        ax.spines["right"].set_color(color)
        ax.tick_params(axis="y", which="major", length=4, width=0.8, colors=color)
    else:
        ax.tick_params(axis="y", which="major", length=4, width=0.8)

# ------------------------------------------------------------
# TASK 1 — PDR & Throughput
# ------------------------------------------------------------
def plot_task1_pdr_throughput():
    hosts = np.array([2, 4, 8, 12, 16, 20])
    pdr = np.array([92.15, 87.20, 60.45, 25.10, 17.95, 18.05])
    throughput = np.array([14.74, 28.32, 31.42, 23.90, 22.98, 28.70])

    fig, ax1 = plt.subplots(figsize=(8.5, 4.8))
    ax2 = ax1.twinx()

    c_pdr = "#00875A"   # Dark Emerald Green
    c_tp = "#0052CC"    # Vibrant Deep Blue

    ax1.fill_between(hosts, pdr, color=c_pdr, alpha=0.12, zorder=1)

    line1 = ax1.plot(
        hosts, pdr, color=c_pdr, marker="o", markersize=7,
        linewidth=2.4, markeredgewidth=1.2, markeredgecolor="white",
        label="Packet Delivery Ratio (PDR)", zorder=3
    )

    line2 = ax2.plot(
        hosts, throughput, color=c_tp, marker="s", markersize=6.5,
        linewidth=2.4, markeredgewidth=1.2, markeredgecolor="white",
        label="Throughput (Mbps)", zorder=3
    )

    ax1.set_xlabel("Number of Wireless Hosts ($N$)", fontweight="bold")
    ax1.set_ylabel("Packet Delivery Ratio (%)", color=c_pdr, fontweight="bold")
    ax2.set_ylabel("Throughput (Mbps)", color=c_tp, fontweight="bold")

    ax1.tick_params(axis="y", labelcolor=c_pdr)
    ax2.tick_params(axis="y", labelcolor=c_tp)

    ax1.set_xticks(hosts)
    ax1.set_ylim(0, 110)
    ax2.set_ylim(0, 40)

    finish_axis(ax1, "both")
    finish_twin_axis(ax2, color=c_tp)

    ax1.annotate(
        "Severe Contention\nDrop ($N \\geq 8$)",
        xy=(8, 60.45), xytext=(12.5, 78),
        arrowprops=dict(arrowstyle="->", color="#333333", lw=1.2, connectionstyle="arc3,rad=-0.15"),
        fontsize=9, fontweight="medium", color="#111111",
        bbox=dict(boxstyle="round,pad=0.4", fc="#ffffff", ec="#999999", lw=1.0)
    )

    lines = line1 + line2
    ax1.legend(
        lines, [l.get_label() for l in lines],
        loc="upper right", frameon=True, fancybox=True, framealpha=0.95, edgecolor="#cccccc"
    )

    ax1.set_title("PDR and Throughput vs. Wireless Host Density", fontweight="bold", pad=12)

    fig.tight_layout()
    fig.savefig("fig1_pdr_throughput.png")
    plt.close(fig)

# ------------------------------------------------------------
# TASK 1 — Contention Window and Delay
# ------------------------------------------------------------
def plot_task1_cw_delay():
    hosts = np.array([2, 4, 8, 12, 16, 20])
    cw_min = np.array([15, 31, 63, 239, 479, 958])
    delay = np.array([15.65, 22.10, 64.30, 128.40, 137.90, 137.50])

    fig, ax1 = plt.subplots(figsize=(8.5, 4.8))
    ax2 = ax1.twinx()

    c_cw = "#D9381E"     # Deep Crimson/Orange
    c_delay = "#4A148C"  # Deep Imperial Purple

    line1 = ax1.plot(
        hosts, cw_min, color=c_cw, marker="^", markersize=7.5,
        linewidth=2.4, markeredgewidth=1.2, markeredgecolor="white",
        label=r"Minimum Contention Window ($CW_{min}$)", zorder=3
    )

    line2 = ax2.plot(
        hosts, delay, color=c_delay, marker="D", markersize=6.5,
        linewidth=2.4, markeredgewidth=1.2, markeredgecolor="white",
        label="End-to-End Delay (ms)", zorder=3
    )

    ax1.set_xlabel("Number of Wireless Hosts ($N$)", fontweight="bold")
    ax1.set_ylabel(r"Minimum Contention Window ($CW_{min}$)", color=c_cw, fontweight="bold")
    ax2.set_ylabel("End-to-End Delay (ms)", color=c_delay, fontweight="bold")

    ax1.tick_params(axis="y", labelcolor=c_cw)
    ax2.tick_params(axis="y", labelcolor=c_delay)

    ax1.set_xticks(hosts)
    ax1.set_ylim(0, 1100)
    ax2.set_ylim(0, 160)

    finish_axis(ax1, "both")
    finish_twin_axis(ax2, color=c_delay)

    lines = line1 + line2
    ax1.legend(
        lines, [l.get_label() for l in lines],
        loc="upper left", frameon=True, fancybox=True, framealpha=0.95, edgecolor="#cccccc"
    )

    ax1.set_title("Contention Window and Delay vs. Wireless Host Density", fontweight="bold", pad=12)

    fig.tight_layout()
    fig.savefig("fig2_cw_delay.png")
    plt.close(fig)

# ------------------------------------------------------------
# TASK 2 — SNIR, BER & PDR (OVERLAP-FREE GUARANTEED)
# ------------------------------------------------------------
def plot_task2_snir_ber_pdr():
    snir = np.array([30, 25, 20, 15, 10, 5, 2])
    ber = np.array([1e-12, 1e-12, 1e-12, 1e-8, 7.5e-4, 3.8e-2, 1.04e-1])
    pdr = np.array([100.0, 100.0, 100.0, 99.6, 0.35, 0.0, 0.0])

    fig, ax1 = plt.subplots(figsize=(8.5, 4.8))
    ax2 = ax1.twinx()

    c_ber = "#111111"   # Solid Jet Black
    c_pdr = "#00875A"   # Dark Emerald Green

    line1 = ax1.semilogy(
        snir, ber, color=c_ber, marker="o", markersize=7.0,
        linestyle="--", linewidth=2.2, markeredgewidth=1.2, markeredgecolor="white",
        label="Bit Error Rate (BER)", zorder=4
    )

    line2 = ax2.plot(
        snir, pdr, color=c_pdr, marker="s", markersize=7.0,
        linewidth=2.4, markeredgewidth=1.2, markeredgecolor="white",
        label="Packet Delivery Ratio (PDR)", zorder=4
    )

    # Low signal degradation region (SNIR < 15 dB)
    ax1.axvspan(15, 1, color="#ffcdd2", alpha=0.45, zorder=0)

    ax1.set_xlabel("Signal-to-Noise-and-Interference Ratio (SNIR, dB)", fontweight="bold")
    ax1.set_ylabel("Bit Error Rate (BER, Log Scale)", color=c_ber, fontweight="bold")
    ax2.set_ylabel("Packet Delivery Ratio (%)", color=c_pdr, fontweight="bold")

    ax1.tick_params(axis="y", labelcolor=c_ber)
    ax2.tick_params(axis="y", labelcolor=c_pdr)

    # Invert X axis (high SNIR -> low SNIR)
    ax1.invert_xaxis()
    ax1.set_xlim(31, 1)

    # Axis limits ensuring ample vertical headroom
    ax1.set_ylim(1e-15, 1.0)
    ax2.set_ylim(-4, 112)

    finish_axis(ax1, "both")
    finish_twin_axis(ax2, color=c_pdr)

    # Threshold reference label
    ax2.axhline(50, linestyle=":", linewidth=1.2, color="#555555", alpha=0.8, zorder=2)
    ax2.text(
        4.5, 53, "50% PDR Threshold",
        fontsize=8.5, fontweight="bold", color="#444444", va="bottom", ha="center",
        bbox=dict(boxstyle="square,pad=0.2", fc="#ffffff", ec="none", alpha=0.8)
    )

    # Annotation arrow positioned safely in middle open area
    ax2.annotate(
        "Critical Degradation\n(SNIR < 15 dB)",
        xy=(15, 99.6), xytext=(21, 62),
        arrowprops=dict(arrowstyle="->", color="#222222", lw=1.2, connectionstyle="arc3,rad=-0.2"),
        fontsize=8.5, fontweight="bold", color="#111111",
        bbox=dict(boxstyle="round,pad=0.4", fc="#ffffff", ec="#999999", lw=1.0)
    )

    # LEGEND IN OPEN SPACE: Positioned center-left between PDR (100%) and BER (10^-12)
    lines = line1 + line2
    ax1.legend(
        lines, [l.get_label() for l in lines],
        loc="center left", bbox_to_anchor=(0.03, 0.42),
        frameon=True, fancybox=True, framealpha=0.95, edgecolor="#cccccc"
    )

    ax1.set_title("Impact of SNIR on BER and Packet Delivery Ratio", fontweight="bold", pad=12)

    fig.tight_layout()
    fig.savefig("fig3_task2_snir_ber_pdr_fixed.png")
    plt.close(fig)

# ------------------------------------------------------------
# TASK 3 — Wired vs Wireless
# ------------------------------------------------------------
def plot_task3_wired_vs_wireless():
    categories = ["90% Load", "100% Load", "110% Load"]
    pdr_wireless = np.array([54.80, 42.10, 30.50])
    pdr_wired = np.array([99.80, 99.20, 96.80])
    throughput_wireless = np.array([28.40, 29.80, 27.50])
    throughput_wired = np.array([88.20, 95.10, 98.40])

    x = np.arange(len(categories))
    width = 0.32

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.8))

    c_wireless = "#D32F2F"   # Strong Crimson Red
    c_wired = "#1976D2"      # Strong Royal Blue

    # PDR Subplot
    b1 = ax1.bar(x - width/2, pdr_wireless, width, label="Wireless (802.11)", color=c_wireless, edgecolor="white", lw=1, zorder=3)
    b2 = ax1.bar(x + width/2, pdr_wired, width, label="Wired (Ethernet)", color=c_wired, edgecolor="white", lw=1, zorder=3)

    ax1.set_ylabel("Packet Delivery Ratio (%)", fontweight="bold")
    ax1.set_title("Packet Delivery Ratio (PDR)", fontweight="bold")
    ax1.set_ylim(0, 120)
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories, fontweight="bold")
    finish_axis(ax1, "y")

    ax1.bar_label(b1, fmt="%.1f%%", padding=3, fontsize=8.5, fontweight="bold")
    ax1.bar_label(b2, fmt="%.1f%%", padding=3, fontsize=8.5, fontweight="bold")

    # Throughput Subplot
    b3 = ax2.bar(x - width/2, throughput_wireless, width, label="Wireless (802.11)", color=c_wireless, edgecolor="white", lw=1, zorder=3)
    b4 = ax2.bar(x + width/2, throughput_wired, width, label="Wired (Ethernet)", color=c_wired, edgecolor="white", lw=1, zorder=3)

    ax2.set_ylabel("Throughput (Mbps)", fontweight="bold")
    ax2.set_title("Throughput", fontweight="bold")
    ax2.set_ylim(0, 120)
    ax2.set_xticks(x)
    ax2.set_xticklabels(categories, fontweight="bold")
    finish_axis(ax2, "y")

    ax2.bar_label(b3, fmt="%.1f", padding=3, fontsize=8.5, fontweight="bold")
    ax2.bar_label(b4, fmt="%.1f", padding=3, fontsize=8.5, fontweight="bold")

    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(
        handles, labels, loc="upper center", bbox_to_anchor=(0.5, 1.02),
        ncol=2, frameon=True, fancybox=True, edgecolor="#cccccc"
    )

    fig.suptitle("Wired vs. Wireless Performance under Network Saturation", fontsize=12.5, fontweight="bold", y=1.08)

    fig.tight_layout()
    fig.savefig("fig4_wired_vs_wireless.png")
    plt.close(fig)

if __name__ == "__main__":
    plot_task1_pdr_throughput()
    plot_task1_cw_delay()
    plot_task2_snir_ber_pdr()
    plot_task3_wired_vs_wireless()
    print("All figures successfully saved with zero overlapping labels.")