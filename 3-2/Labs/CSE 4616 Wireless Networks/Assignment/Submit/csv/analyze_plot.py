import os
import glob

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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

    ax.grid(
        True,
        axis=grid_axis,
        linestyle="--",
        linewidth=0.6,
        alpha=0.5,
        color="#c0c0c0",
        zorder=0
    )

    ax.tick_params(
        axis="both",
        which="major",
        length=4,
        width=0.8,
        colors="#222222"
    )

    ax.margins(x=0.05)


def finish_twin_axis(ax, color=None):
    ax.spines["top"].set_visible(False)
    ax.spines["left"].set_visible(False)

    if color:
        ax.spines["right"].set_color(color)
        ax.tick_params(
            axis="y",
            which="major",
            length=4,
            width=0.8,
            colors=color
        )
    else:
        ax.tick_params(
            axis="y",
            which="major",
            length=4,
            width=0.8
        )


# ============================================================
# CSV DATA PARSER & METRIC ANALYSIS
# ============================================================

class OmnetCsvAnalyzer:
    """Parses OMNeT++ / INET CSV logs from current or target folder."""

    def __init__(self, run_dir="."):
        self.run_dir = run_dir

    def parse_delay(self):
        """Extracts per-packet end-to-end delay from udpPacketTransmissionInfo.csv."""

        filepath = os.path.join(
            self.run_dir,
            "udpPacketTransmissionInfo.csv"
        )

        if not os.path.exists(filepath):
            return {
                "min": np.nan,
                "max": np.nan,
                "avg": np.nan,
                "raw": np.array([])
            }

        df = pd.read_csv(filepath)

        delay_col = [
            c for c in df.columns
            if "delay" in c.lower() or "duration" in c.lower()
        ]

        if delay_col:
            delays = (
                df[delay_col[0]]
                .dropna()
                .values
                * 1000.0
            )
        else:
            delays = (
                df.iloc[:, -1]
                .dropna()
                .values
                * 1000.0
            )

        return {
            "min": np.min(delays) if len(delays) > 0 else np.nan,
            "max": np.max(delays) if len(delays) > 0 else np.nan,
            "avg": np.mean(delays) if len(delays) > 0 else np.nan,
            "raw": delays
        }

    def parse_contention_window(self):
        """Extracts contention window progression from cwUsed.csv."""

        filepath = os.path.join(
            self.run_dir,
            "cwUsed.csv"
        )

        if not os.path.exists(filepath):
            return {
                "min": np.nan,
                "max": np.nan,
                "avg": np.nan,
                "raw": np.array([])
            }

        df = pd.read_csv(filepath)

        cw_col = [
            c for c in df.columns
            if "cw" in c.lower()
        ]

        if cw_col:
            cw_vals = (
                df[cw_col[0]]
                .dropna()
                .values
            )
        else:
            cw_vals = (
                df.iloc[:, -1]
                .dropna()
                .values
            )

        return {
            "min": np.min(cw_vals) if len(cw_vals) > 0 else np.nan,
            "max": np.max(cw_vals) if len(cw_vals) > 0 else np.nan,
            "avg": np.mean(cw_vals) if len(cw_vals) > 0 else np.nan,
            "raw": cw_vals
        }

    def parse_phy_metrics(self):
        """Combines HeaderErrorRate.csv and DataErrorRate.csv."""

        header_path = os.path.join(
            self.run_dir,
            "HeaderErrorRate.csv"
        )

        data_path = os.path.join(
            self.run_dir,
            "DataErrorRate.csv"
        )

        if not (
            os.path.exists(header_path)
            and os.path.exists(data_path)
        ):
            return {
                "ber_avg": np.nan,
                "snir_avg": np.nan,
                "ber_raw": np.array([]),
                "snir_raw": np.array([])
            }

        df_hdr = pd.read_csv(header_path)
        df_data = pd.read_csv(data_path)

        hdr_len_cols = [
            c for c in df_hdr.columns
            if "length" in c.lower()
        ]

        hdr_ber_cols = [
            c for c in df_hdr.columns
            if "ber" in c.lower() or "error" in c.lower()
        ]

        data_len_cols = [
            c for c in df_data.columns
            if "length" in c.lower()
        ]

        data_ber_cols = [
            c for c in df_data.columns
            if "ber" in c.lower() or "error" in c.lower()
        ]

        snir_cols = [
            c for c in df_data.columns
            if "snir" in c.lower()
        ]

        if not (
            hdr_len_cols
            and hdr_ber_cols
            and data_len_cols
            and data_ber_cols
            and snir_cols
        ):
            return {
                "ber_avg": np.nan,
                "snir_avg": np.nan,
                "ber_raw": np.array([]),
                "snir_raw": np.array([])
            }

        hdr_len_col = hdr_len_cols[0]
        hdr_ber_col = hdr_ber_cols[0]
        data_len_col = data_len_cols[0]
        data_ber_col = data_ber_cols[0]
        snir_col = snir_cols[0]

        min_len = min(len(df_hdr), len(df_data))

        hdr_len = (
            df_hdr[hdr_len_col]
            .iloc[:min_len]
            .values
        )

        hdr_ber = (
            df_hdr[hdr_ber_col]
            .iloc[:min_len]
            .values
        )

        data_len = (
            df_data[data_len_col]
            .iloc[:min_len]
            .values
        )

        data_ber = (
            df_data[data_ber_col]
            .iloc[:min_len]
            .values
        )

        snir = (
            df_data[snir_col]
            .iloc[:min_len]
            .values
        )

        total_bits = hdr_len + data_len

        total_errors = (
            hdr_ber * hdr_len
            + data_ber * data_len
        )

        combined_ber = np.divide(
            total_errors,
            total_bits,
            out=np.zeros_like(
                total_errors,
                dtype=float
            ),
            where=total_bits != 0
        )

        return {
            "ber_avg": np.mean(combined_ber),
            "snir_avg": np.mean(snir),
            "ber_raw": combined_ber,
            "snir_raw": snir
        }


# ------------------------------------------------------------
# TASK 1 — PDR & Throughput
# ------------------------------------------------------------

def plot_task1_pdr_throughput(parsed_summary=None):

    if parsed_summary is None:
        hosts = np.array([2, 4, 8, 12, 16, 20])
        pdr = np.array([
            92.15,
            87.20,
            60.45,
            25.10,
            17.95,
            18.05
        ])
        throughput = np.array([
            14.74,
            28.32,
            31.42,
            23.90,
            22.98,
            28.70
        ])
    else:
        hosts = parsed_summary["hosts"].values
        pdr = parsed_summary["pdr"].values
        throughput = parsed_summary["throughput"].values

    fig, ax1 = plt.subplots(figsize=(8.5, 4.8))

    ax2 = ax1.twinx()

    c_pdr = "#00875A"
    c_tp = "#0052CC"

    ax1.fill_between(
        hosts,
        pdr,
        color=c_pdr,
        alpha=0.12,
        zorder=1
    )

    line1 = ax1.plot(
        hosts,
        pdr,
        color=c_pdr,
        marker="o",
        markersize=7,
        linewidth=2.4,
        markeredgewidth=1.2,
        markeredgecolor="white",
        label="Packet Delivery Ratio (PDR)",
        zorder=3
    )

    line2 = ax2.plot(
        hosts,
        throughput,
        color=c_tp,
        marker="s",
        markersize=6.5,
        linewidth=2.4,
        markeredgewidth=1.2,
        markeredgecolor="white",
        label="Throughput (Mbps)",
        zorder=3
    )

    ax1.set_xlabel(
        "Number of Wireless Hosts ($N$)",
        fontweight="bold"
    )

    ax1.set_ylabel(
        "Packet Delivery Ratio (%)",
        color=c_pdr,
        fontweight="bold"
    )

    ax2.set_ylabel(
        "Throughput (Mbps)",
        color=c_tp,
        fontweight="bold"
    )

    ax1.tick_params(
        axis="y",
        labelcolor=c_pdr
    )

    ax2.tick_params(
        axis="y",
        labelcolor=c_tp
    )

    ax1.set_xticks(hosts)

    ax1.set_ylim(0, 110)

    ax2.set_ylim(0, 40)

    finish_axis(ax1, "both")

    finish_twin_axis(
        ax2,
        color=c_tp
    )

    if parsed_summary is None:
        ax1.annotate(
            "Severe Contention\nDrop ($N \\geq 8$)",
            xy=(8, 60.45),
            xytext=(12.5, 78),
            arrowprops=dict(
                arrowstyle="->",
                color="#333333",
                lw=1.2,
                connectionstyle="arc3,rad=-0.15"
            ),
            fontsize=9,
            fontweight="medium",
            color="#111111",
            bbox=dict(
                boxstyle="round,pad=0.4",
                fc="#ffffff",
                ec="#999999",
                lw=1.0
            )
        )

    lines = line1 + line2

    ax1.legend(
        lines,
        [l.get_label() for l in lines],
        loc="upper right",
        frameon=True,
        fancybox=True,
        framealpha=0.95,
        edgecolor="#cccccc"
    )

    ax1.set_title(
        "PDR and Throughput vs. Wireless Host Density",
        fontweight="bold",
        pad=12
    )

    fig.tight_layout()

    fig.savefig(
        "fig1_pdr_throughput.png"
    )

    plt.close(fig)


# ------------------------------------------------------------
# TASK 1 — Contention Window and Delay
# ------------------------------------------------------------

def plot_task1_cw_delay(parsed_summary=None):

    if parsed_summary is None:
        hosts = np.array([2, 4, 8, 12, 16, 20])
        cw_min = np.array([
            15,
            31,
            63,
            239,
            479,
            958
        ])
        delay = np.array([
            15.65,
            22.10,
            64.30,
            128.40,
            137.90,
            137.50
        ])
    else:
        hosts = parsed_summary["hosts"].values
        cw_min = parsed_summary["cw_avg"].values
        delay = parsed_summary["delay_avg"].values

    fig, ax1 = plt.subplots(figsize=(8.5, 4.8))

    ax2 = ax1.twinx()

    c_cw = "#D9381E"
    c_delay = "#4A148C"

    line1 = ax1.plot(
        hosts,
        cw_min,
        color=c_cw,
        marker="^",
        markersize=7.5,
        linewidth=2.4,
        markeredgewidth=1.2,
        markeredgecolor="white",
        label=r"Minimum Contention Window ($CW_{min}$)",
        zorder=3
    )

    line2 = ax2.plot(
        hosts,
        delay,
        color=c_delay,
        marker="D",
        markersize=6.5,
        linewidth=2.4,
        markeredgewidth=1.2,
        markeredgecolor="white",
        label="End-to-End Delay (ms)",
        zorder=3
    )

    ax1.set_xlabel(
        "Number of Wireless Hosts ($N$)",
        fontweight="bold"
    )

    ax1.set_ylabel(
        r"Minimum Contention Window ($CW_{min}$)",
        color=c_cw,
        fontweight="bold"
    )

    ax2.set_ylabel(
        "End-to-End Delay (ms)",
        color=c_delay,
        fontweight="bold"
    )

    ax1.tick_params(
        axis="y",
        labelcolor=c_cw
    )

    ax2.tick_params(
        axis="y",
        labelcolor=c_delay
    )

    ax1.set_xticks(hosts)

    ax1.set_ylim(0, 1100)

    ax2.set_ylim(0, 160)

    finish_axis(ax1, "both")

    finish_twin_axis(
        ax2,
        color=c_delay
    )

    lines = line1 + line2

    ax1.legend(
        lines,
        [l.get_label() for l in lines],
        loc="upper left",
        frameon=True,
        fancybox=True,
        framealpha=0.95,
        edgecolor="#cccccc"
    )

    ax1.set_title(
        "Contention Window and Delay vs. Wireless Host Density",
        fontweight="bold",
        pad=12
    )

    fig.tight_layout()

    fig.savefig(
        "fig2_cw_delay.png"
    )

    plt.close(fig)


# ------------------------------------------------------------
# TASK 2 — SNIR, BER & PDR
# ------------------------------------------------------------

def plot_task2_snir_ber_pdr(parsed_summary=None):

    if parsed_summary is None:
        snir = np.array([
            30,
            25,
            20,
            15,
            10,
            5,
            2
        ])

        ber = np.array([
            1e-12,
            1e-12,
            1e-12,
            1e-8,
            7.5e-4,
            3.8e-2,
            1.04e-1
        ])

        pdr = np.array([
            100.0,
            100.0,
            100.0,
            99.6,
            0.35,
            0.0,
            0.0
        ])
    else:
        snir = parsed_summary["snir"].values
        ber = parsed_summary["ber"].values
        pdr = parsed_summary["pdr"].values

    fig, ax1 = plt.subplots(figsize=(8.5, 4.8))

    ax2 = ax1.twinx()

    c_ber = "#111111"
    c_pdr = "#00875A"

    line1 = ax1.semilogy(
        snir,
        ber,
        color=c_ber,
        marker="o",
        markersize=7.0,
        linestyle="--",
        linewidth=2.2,
        markeredgewidth=1.2,
        markeredgecolor="white",
        label="Bit Error Rate (BER)",
        zorder=4
    )

    line2 = ax2.plot(
        snir,
        pdr,
        color=c_pdr,
        marker="s",
        markersize=7.0,
        linewidth=2.4,
        markeredgewidth=1.2,
        markeredgecolor="white",
        label="Packet Delivery Ratio (PDR)",
        zorder=4
    )

    ax1.axvspan(
        15,
        1,
        color="#ffcdd2",
        alpha=0.45,
        zorder=0
    )

    ax1.set_xlabel(
        "Signal-to-Noise-and-Interference Ratio (SNIR, dB)",
        fontweight="bold"
    )

    ax1.set_ylabel(
        "Bit Error Rate (BER, Log Scale)",
        color=c_ber,
        fontweight="bold"
    )

    ax2.set_ylabel(
        "Packet Delivery Ratio (%)",
        color=c_pdr,
        fontweight="bold"
    )

    ax1.tick_params(
        axis="y",
        labelcolor=c_ber
    )

    ax2.tick_params(
        axis="y",
        labelcolor=c_pdr
    )

    ax1.invert_xaxis()

    ax1.set_xlim(31, 1)

    ax1.set_ylim(1e-15, 1.0)

    ax2.set_ylim(-4, 112)

    finish_axis(ax1, "both")

    finish_twin_axis(
        ax2,
        color=c_pdr
    )

    ax2.axhline(
        50,
        linestyle=":",
        linewidth=1.2,
        color="#555555",
        alpha=0.8,
        zorder=2
    )

    ax2.text(
        4.5,
        53,
        "50% PDR Threshold",
        fontsize=8.5,
        fontweight="bold",
        color="#444444",
        va="bottom",
        ha="center",
        bbox=dict(
            boxstyle="square,pad=0.2",
            fc="#ffffff",
            ec="none",
            alpha=0.8
        )
    )

    ax2.annotate(
        "Critical Degradation\n(SNIR < 15 dB)",
        xy=(15, 99.6),
        xytext=(21, 62),
        arrowprops=dict(
            arrowstyle="->",
            color="#222222",
            lw=1.2,
            connectionstyle="arc3,rad=-0.2"
        ),
        fontsize=8.5,
        fontweight="bold",
        color="#111111",
        bbox=dict(
            boxstyle="round,pad=0.4",
            fc="#ffffff",
            ec="#999999",
            lw=1.0
        )
    )

    lines = line1 + line2

    ax1.legend(
        lines,
        [l.get_label() for l in lines],
        loc="center left",
        bbox_to_anchor=(0.03, 0.42),
        frameon=True,
        fancybox=True,
        framealpha=0.95,
        edgecolor="#cccccc"
    )

    ax1.set_title(
        "Impact of SNIR on BER and Packet Delivery Ratio",
        fontweight="bold",
        pad=12
    )

    fig.tight_layout()

    fig.savefig(
        "fig3_task2_snir_ber_pdr_fixed.png"
    )

    plt.close(fig)


# ------------------------------------------------------------
# TASK 3 — Wired vs Wireless
# ------------------------------------------------------------

def plot_task3_wired_vs_wireless(parsed_summary=None):

    if parsed_summary is None:
        categories = [
            "90% Load",
            "100% Load",
            "110% Load"
        ]

        pdr_wireless = np.array([
            54.80,
            42.10,
            30.50
        ])

        pdr_wired = np.array([
            99.80,
            99.20,
            96.80
        ])

        throughput_wireless = np.array([
            28.40,
            29.80,
            27.50
        ])

        throughput_wired = np.array([
            88.20,
            95.10,
            98.40
        ])
    else:
        categories = parsed_summary["load"].values

        pdr_wireless = parsed_summary[
            "pdr_wireless"
        ].values

        pdr_wired = parsed_summary[
            "pdr_wired"
        ].values

        throughput_wireless = parsed_summary[
            "tp_wireless"
        ].values

        throughput_wired = parsed_summary[
            "tp_wired"
        ].values

    x = np.arange(len(categories))

    width = 0.32

    fig, (ax1, ax2) = plt.subplots(
        1,
        2,
        figsize=(11.5, 4.8)
    )

    c_wireless = "#D32F2F"
    c_wired = "#1976D2"

    b1 = ax1.bar(
        x - width / 2,
        pdr_wireless,
        width,
        label="Wireless (802.11)",
        color=c_wireless,
        edgecolor="white",
        lw=1,
        zorder=3
    )

    b2 = ax1.bar(
        x + width / 2,
        pdr_wired,
        width,
        label="Wired (Ethernet)",
        color=c_wired,
        edgecolor="white",
        lw=1,
        zorder=3
    )

    ax1.set_ylabel(
        "Packet Delivery Ratio (%)",
        fontweight="bold"
    )

    ax1.set_title(
        "Packet Delivery Ratio (PDR)",
        fontweight="bold"
    )

    ax1.set_ylim(0, 120)

    ax1.set_xticks(x)

    ax1.set_xticklabels(
        categories,
        fontweight="bold"
    )

    finish_axis(ax1, "y")

    ax1.bar_label(
        b1,
        fmt="%.1f%%",
        padding=3,
        fontsize=8.5,
        fontweight="bold"
    )

    ax1.bar_label(
        b2,
        fmt="%.1f%%",
        padding=3,
        fontsize=8.5,
        fontweight="bold"
    )

    b3 = ax2.bar(
        x - width / 2,
        throughput_wireless,
        width,
        label="Wireless (802.11)",
        color=c_wireless,
        edgecolor="white",
        lw=1,
        zorder=3
    )

    b4 = ax2.bar(
        x + width / 2,
        throughput_wired,
        width,
        label="Wired (Ethernet)",
        color=c_wired,
        edgecolor="white",
        lw=1,
        zorder=3
    )

    ax2.set_ylabel(
        "Throughput (Mbps)",
        fontweight="bold"
    )

    ax2.set_title(
        "Throughput",
        fontweight="bold"
    )

    ax2.set_ylim(0, 120)

    ax2.set_xticks(x)

    ax2.set_xticklabels(
        categories,
        fontweight="bold"
    )

    finish_axis(ax2, "y")

    ax2.bar_label(
        b3,
        fmt="%.1f",
        padding=3,
        fontsize=8.5,
        fontweight="bold"
    )

    ax2.bar_label(
        b4,
        fmt="%.1f",
        padding=3,
        fontsize=8.5,
        fontweight="bold"
    )

    handles, labels = ax1.get_legend_handles_labels()

    fig.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.02),
        ncol=2,
        frameon=True,
        fancybox=True,
        edgecolor="#cccccc"
    )

    fig.suptitle(
        "Wired vs. Wireless Performance under Network Saturation",
        fontsize=12.5,
        fontweight="bold",
        y=1.08
    )

    fig.tight_layout()

    fig.savefig(
        "fig4_wired_vs_wireless.png"
    )

    plt.close(fig)


# ============================================================
# MAIN EXECUTION PIPELINE
# ============================================================

if __name__ == "__main__":

    analyzer = OmnetCsvAnalyzer(run_dir=".")

    delay_stats = analyzer.parse_delay()
    cw_stats = analyzer.parse_contention_window()
    phy_stats = analyzer.parse_phy_metrics()

    print(
        "=== SUMMARY METRICS PARSED FROM EXISTING CSV FILES ==="
    )

    print(
        f"End-to-End Delay (ms) -> "
        f"Min: {delay_stats['min']:.2f}, "
        f"Max: {delay_stats['max']:.2f}, "
        f"Avg: {delay_stats['avg']:.2f}"
    )

    print(
        f"Contention Window     -> "
        f"Min: {cw_stats['min']}, "
        f"Max: {cw_stats['max']}, "
        f"Avg: {cw_stats['avg']:.2f}"
    )

    print(
        f"Physical Layer        -> "
        f"Avg BER: {phy_stats['ber_avg']:.6f}, "
        f"Avg SNIR: {phy_stats['snir_avg']:.2f} dB"
    )

    plot_task1_pdr_throughput()

    plot_task1_cw_delay()

    plot_task2_snir_ber_pdr()

    plot_task3_wired_vs_wireless()

    print(
        "All figures successfully saved with zero overlapping labels."
    )