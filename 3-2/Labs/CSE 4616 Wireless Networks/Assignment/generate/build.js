const pptxgen = require("pptxgenjs");
const path = require("path");

const D = "/home/claude/deck/";

// ================= palette =================
const NAVY = "0B2545";      // dominant dark
const STEEL = "134074";     // secondary
const CYAN = "00B4D8";      // accent
const BG_LIGHT = "F7FAFC";
const CARD_ALT = "EAF2F8";
const CARD_ALT2 = "DCEAF4";
const TEXT_DARK = "132A3A";
const TEXT_MUTED = "5A7184";
const WHITE = "FFFFFF";
const WARN_RED = "B23A48"; // semantic: wireless-limitation values only

const HEAD_FONT = "Cambria";
const BODY_FONT = "Calibri";

// ================= helpers =================
function iconCircle(slide, iconName, x, y, d, circleColor, opts = {}) {
  slide.addShape("ellipse", { x, y, w: d, h: d, fill: { color: circleColor }, line: { type: "none" } });
  const pad = d * (opts.pad === undefined ? 0.24 : opts.pad);
  slide.addImage({ path: D + `icon_${iconName}.png`, x: x + pad / 2, y: y + pad / 2, w: d - pad, h: d - pad });
}

function sectionHeader(slide, title, iconName, opts = {}) {
  const dark = !!opts.dark;
  const y = opts.y === undefined ? 0.42 : opts.y;
  const circleColor = dark ? CYAN : STEEL;
  iconCircle(slide, iconName, 0.5, y, 0.55, circleColor, { pad: 0.26 });
  slide.addText(title, {
    x: 1.2, y: y - 0.06, w: 11.6, h: 0.68,
    fontFace: HEAD_FONT, fontSize: opts.size || 27, bold: true,
    color: dark ? WHITE : NAVY, align: "left", valign: "middle", isTextBox: true,
  });
}

function pill(slide, text, x, y, w, h, fill, textColor) {
  slide.addShape("roundRect", { x, y, w, h, rectRadius: h / 2, fill: { color: fill }, line: { type: "none" } });
  slide.addText(text, {
    x, y, w, h, fontFace: BODY_FONT, fontSize: 11.5, bold: true, color: textColor,
    align: "center", valign: "middle", margin: 0, isTextBox: true,
  });
}

function card(slide, opts) {
  const { x, y, w, h, fill = CARD_ALT, title, titleColor = NAVY, body, bodyColor = TEXT_DARK, titleSize = 13, bodySize = 11 } = opts;
  slide.addShape("roundRect", { x, y, w, h, rectRadius: 0.08, fill: { color: fill }, line: { type: "none" } });
  slide.addText(title, {
    x: x + 0.16, y: y + 0.12, w: w - 0.32, h: 0.34,
    fontFace: BODY_FONT, fontSize: titleSize, bold: true, color: titleColor, align: "left", valign: "top", margin: 0, isTextBox: true,
  });
  slide.addText(body, {
    x: x + 0.16, y: y + 0.46, w: w - 0.32, h: h - 0.58,
    fontFace: BODY_FONT, fontSize: bodySize, color: bodyColor, align: "left", valign: "top", margin: 0, lineSpacingMultiple: 1.12, isTextBox: true,
  });
}

function imgBox(slide, file, x, y, w, aspectWoverH, caption) {
  const h = w / aspectWoverH;
  slide.addImage({ path: D + file, x, y, w, h });
  if (caption) {
    slide.addText(caption, {
      x, y: y + h + 0.03, w, h: 0.28,
      fontFace: BODY_FONT, fontSize: 10.5, italic: true, color: TEXT_MUTED, align: "center", valign: "top", margin: 0, isTextBox: true,
    });
  }
  return h;
}

function footerNote(slide, n, dark = false) {
  slide.addText(`CSE 4616 — Wireless Networks Lab, Assignment 1`, {
    x: 0.5, y: 7.16, w: 8.0, h: 0.28, fontFace: BODY_FONT, fontSize: 9,
    color: dark ? "8FA6C7" : TEXT_MUTED, align: "left", valign: "middle", margin: 0, isTextBox: true,
  });
  slide.addText(`${n}`, {
    x: 12.33, y: 7.16, w: 0.5, h: 0.28, fontFace: BODY_FONT, fontSize: 9,
    color: dark ? "8FA6C7" : TEXT_MUTED, align: "right", valign: "middle", margin: 0, isTextBox: true,
  });
}

// ================= build =================
const pres = new pptxgen();
pres.defineLayout({ name: "LAYOUT_WIDE", width: 13.333, height: 7.5 });
pres.layout = "LAYOUT_WIDE";

// ---------------- Slide 1: Title ----------------
{
  const s = pres.addSlide();
  s.background = { color: NAVY };

  // watermark icon
  s.addImage({ path: D + "icon_wifi.png", x: 8.9, y: 1.1, w: 4.6, h: 4.6, transparency: 88 });

  s.addText("CSE 4616  •  WIRELESS NETWORKS LAB  •  ASSIGNMENT 1", {
    x: 0.7, y: 1.55, w: 10.5, h: 0.4, fontFace: BODY_FONT, fontSize: 14, bold: true,
    color: CYAN, charSpacing: 2, align: "left", isTextBox: true,
  });

  s.addText([
    { text: "Impact of Traffic Load and Network Parameters on\n", options: {} },
    { text: "IEEE 802.11 Wireless LAN Performance", options: {} },
  ], {
    x: 0.7, y: 2.05, w: 10.8, h: 1.9, fontFace: HEAD_FONT, fontSize: 34, bold: true,
    color: WHITE, align: "left", valign: "top", lineSpacingMultiple: 1.12, isTextBox: true,
  });

  s.addShape("line", { x: 0.72, y: 4.15, w: 3.2, h: 0, line: { color: CYAN, width: 2 } });

  s.addText("Rahatut Tahrim Mounota", {
    x: 0.7, y: 4.4, w: 6, h: 0.4, fontFace: BODY_FONT, fontSize: 18, bold: true, color: WHITE, isTextBox: true,
  });
  s.addText("Student ID: 220041122", {
    x: 0.7, y: 4.82, w: 6, h: 0.35, fontFace: BODY_FONT, fontSize: 13.5, color: "AFC3DE", isTextBox: true,
  });

  s.addText("OMNeT++ with INET Framework v4.5.4   |   seed-set = 220041122   |   sim-time-limit = 40 s", {
    x: 0.7, y: 6.75, w: 10.8, h: 0.35, fontFace: BODY_FONT, fontSize: 11, italic: true, color: "8FA6C7", isTextBox: true,
  });
}

// ---------------- Slide 2: Objectives ----------------
{
  const s = pres.addSlide();
  s.background = { color: BG_LIGHT };
  sectionHeader(s, "Objectives & Evaluation Framework", "target");

  s.addText([
    { text: "Core Objective:  ", options: { bold: true, color: NAVY } },
    { text: "Evaluate IEEE 802.11 WLAN performance under varying host density, contention, channel interference, and medium architecture, using discrete-event simulation in OMNeT++/INET.", options: { color: TEXT_DARK } },
  ], {
    x: 0.5, y: 1.28, w: 12.3, h: 0.7, fontFace: BODY_FONT, fontSize: 14.5, align: "left", valign: "top", lineSpacingMultiple: 1.18, isTextBox: true,
  });

  const rows = [
    { icon: "layers", title: "Task 1 — MAC-Layer Saturation", body: "Network saturation driven by CSMA/CA exponential-backoff retransmissions as host density rises." },
    { icon: "activity", title: "Task 2 — Channel Interference", body: "Physical-layer link degradation under variable background noise (SNIR vs. BER)." },
    { icon: "compare", title: "Task 3 — Wired vs. Wireless", body: "Comparative benchmarking of wired Ethernet and wireless 802.11 under identical saturation load." },
  ];
  let ry = 2.25;
  const rh = 1.05;
  rows.forEach((r) => {
    s.addShape("roundRect", { x: 0.5, y: ry, w: 12.3, h: rh, rectRadius: 0.09, fill: { color: WHITE }, line: { color: CARD_ALT2, width: 1 } });
    iconCircle(s, r.icon, 0.74, ry + (rh - 0.62) / 2, 0.62, STEEL, { pad: 0.26 });
    s.addText(r.title, {
      x: 1.65, y: ry + 0.13, w: 10.9, h: 0.38, fontFace: BODY_FONT, fontSize: 15, bold: true, color: NAVY, margin: 0, isTextBox: true,
    });
    s.addText(r.body, {
      x: 1.65, y: ry + 0.52, w: 10.9, h: 0.46, fontFace: BODY_FONT, fontSize: 12.5, color: TEXT_DARK, margin: 0, lineSpacingMultiple: 1.05, isTextBox: true,
    });
    ry += rh + 0.22;
  });

  s.addText("EVALUATED METRICS", {
    x: 0.5, y: ry + 0.06, w: 4, h: 0.3, fontFace: BODY_FONT, fontSize: 11, bold: true, color: TEXT_MUTED, charSpacing: 1.5, isTextBox: true,
  });
  const metrics = ["PDR", "Throughput", "CWmin", "End-to-End Delay", "BER"];
  let mx = 0.5;
  const my = ry + 0.42;
  metrics.forEach((m) => {
    const w = 0.42 + m.length * 0.1;
    pill(s, m, mx, my, w, 0.36, CYAN, NAVY);
    mx += w + 0.18;
  });

  footerNote(s, 2);
}

// ---------------- Slide 3: Architecture & Topology ----------------
{
  const s = pres.addSlide();
  s.background = { color: BG_LIGHT };
  sectionHeader(s, "Network Architecture & Simulation Topology", "share");

  const specs = [
    { b: "Wireless Segment: ", t: "N stationary hosts in a 400 m × 400 m grid; RadioMedium background noise floor of \u201310 dBm; Ieee80211YansErrorModel." },
    { b: "Access Point (ap): ", t: "Bridges 802.11 wireless frames directly onto the wired Ethernet segment." },
    { b: "Wired Segment: ", t: "M WiredHost nodes connected via full-duplex 100 Mbps Ethernet (Eth100M)." },
    { b: "Traffic Destination: ", t: "Unidirectional UDP flow to wiredSinkNode, listening on UDP port 5000." },
  ];
  let sy = 1.35;
  specs.forEach((sp) => {
    s.addShape("ellipse", { x: 0.55, y: sy + 0.09, w: 0.09, h: 0.09, fill: { color: CYAN }, line: { type: "none" } });
    s.addText([
      { text: sp.b, options: { bold: true, color: NAVY } },
      { text: sp.t, options: { color: TEXT_DARK } },
    ], { x: 0.8, y: sy, w: 5.1, h: 0.9, fontFace: BODY_FONT, fontSize: 12.5, align: "left", valign: "top", lineSpacingMultiple: 1.14, margin: 0, isTextBox: true });
    sy += 1.02;
  });

  // topology diagram (right side)
  const dx = 6.15, dw = 6.65;
  s.addShape("roundRect", { x: dx, y: 1.35, w: dw, h: 4.55, rectRadius: 0.1, fill: { color: WHITE }, line: { color: CARD_ALT2, width: 1 } });
  s.addText("SIMULATION TOPOLOGY — WiredAndWirelessHostsWithAP.ned", {
    x: dx + 0.25, y: 1.5, w: dw - 0.5, h: 0.3, fontFace: BODY_FONT, fontSize: 10, bold: true, color: TEXT_MUTED, charSpacing: 1, isTextBox: true,
  });

  function box(bx, by, bw, bh, fill, l1, l2) {
    s.addShape("roundRect", { x: bx, y: by, w: bw, h: bh, rectRadius: 0.07, fill: { color: fill }, line: { type: "none" } });
    s.addText(l1, { x: bx + 0.06, y: by + 0.08, w: bw - 0.12, h: 0.32, fontFace: BODY_FONT, fontSize: 11, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0, isTextBox: true });
    s.addText(l2, { x: bx + 0.06, y: by + 0.38, w: bw - 0.12, h: 0.3, fontFace: BODY_FONT, fontSize: 8.5, italic: true, color: "D7E4F5", align: "center", valign: "middle", margin: 0, isTextBox: true });
  }
  function arrow(ax, ay, aw, label) {
    s.addText(label, { x: ax, y: ay - 0.02, w: aw, h: 0.3, fontFace: BODY_FONT, fontSize: 8.5, color: TEXT_MUTED, align: "center", valign: "middle", margin: 0, isTextBox: true });
  }

  const bw = 1.42, bh = 0.72, gap = 0.28;
  const rowY = 2.15;
  let bx = dx + 0.3;
  box(bx, rowY, bw, bh, STEEL, "WirelessHost", "[0..N-1]"); bx += bw;
  arrow(bx, rowY, gap, "\u2192"); bx += gap;
  box(bx, rowY, bw, bh, NAVY, "AccessPoint", "802.11\u2194Eth"); bx += bw;
  arrow(bx, rowY, gap, "\u2192"); bx += gap;
  box(bx, rowY, bw, bh, NAVY, "Router", "aggregation"); bx += bw;
  arrow(bx, rowY, gap, "\u2192"); bx += gap;
  box(bx, rowY, bw + 0.1, bh, "0E8388", "wiredSinkNode", "UdpSink:5000");

  const rowY2 = rowY + bh + 0.55;
  bx = dx + 0.3;
  box(bx, rowY2, bw, bh, "5C7AA6", "WiredHost", "[0..M-1]");
  s.addShape("line", { x: bx + bw / 2, y: rowY, w: 0, h: rowY2 - rowY - bh + 0.03, flipV: true, line: { color: TEXT_MUTED, width: 1, dashType: "dash" } });
  arrow(bx + bw + 0.05, rowY2, 2.1, "\u2192  direct to Router (Eth100M)");

  s.addText("All traffic converges on a single UDP sink, so wired and wireless segments are benchmarked under identical routing and traffic-generation conditions.", {
    x: dx + 0.3, y: rowY2 + bh + 0.35, w: dw - 0.6, h: 0.9, fontFace: BODY_FONT, fontSize: 10.5, italic: true, color: TEXT_MUTED, lineSpacingMultiple: 1.15, isTextBox: true,
  });

  footerNote(s, 3);
}

// ---------------- Slide 4: Task 1 ----------------
{
  const s = pres.addSlide();
  s.background = { color: BG_LIGHT };
  sectionHeader(s, "Task 1 — MAC Contention & Network Saturation", "layers");

  s.addText([
    { text: "Offered Load:  ", options: { bold: true, color: NAVY } },
    { text: "Cumulative Load (bps) = N \u00d7 Packet Size (bits) / Send Interval (s)   —   8 Mbps per host at a 0.001 s interval.", options: { italic: true, color: TEXT_DARK } },
  ], { x: 0.5, y: 1.22, w: 12.3, h: 0.4, fontFace: BODY_FONT, fontSize: 13, align: "left", valign: "middle", isTextBox: true });

  const regimes = [
    { title: "Low Load  (N = 2, 16 Mbps)", body: "Minimal contention.\nPDR reaches 92.30%\nDelay just 15.71 ms." },
    { title: "Medium Load  (N = 4\u20138)", body: "Demand nears physical limits.\nThroughput peaks at N = 8\n(31.50 Mbps) as PDR falls to 60.45%." },
    { title: "Saturation Knee  (N \u2265 8)", body: "Exponential backoff doubling.\nCWmin: 15\u219231\u219263\u2192960\nPDR collapses to 18.00%." },
  ];
  const cw = 3.97, cx0 = 0.5, cgap = 0.2, cy = 1.72, chh = 1.32;
  regimes.forEach((r, i) => {
    card(s, { x: cx0 + i * (cw + cgap), y: cy, w: cw, h: chh, fill: i === 2 ? "FCE9EA" : CARD_ALT, title: r.title, body: r.body, titleColor: i === 2 ? WARN_RED : NAVY, bodySize: 11.5, titleSize: 12.5 });
  });

  const chartY = cy + chh + 0.22;
  const chartW = 5.95;
  imgBox(s, "fig1_pdr_throughput.png", 0.5, chartY, chartW, 1.789, "Figure 1. PDR & Throughput vs. Wireless Host Density");
  imgBox(s, "fig2_cw_delay.png", 0.5 + chartW + 0.35, chartY, chartW, 1.789, "Figure 2. Minimum Contention Window & Delay vs. Host Density");

  footerNote(s, 4);
}

// ---------------- Slide 5: Task 2 ----------------
{
  const s = pres.addSlide();
  s.background = { color: BG_LIGHT };
  sectionHeader(s, "Task 2 — Channel Interference & SNIR Analysis", "activity");

  s.addText([
    { text: "Setup:  ", options: { bold: true, color: NAVY } },
    { text: "Fixed N = 10 hosts (\u224840 Mbps offered load); background noise swept so SNIR ranges from 30 dB down to 2 dB.", options: { color: TEXT_DARK } },
  ], { x: 0.5, y: 1.22, w: 5.75, h: 0.62, fontFace: BODY_FONT, fontSize: 12.5, align: "left", valign: "top", lineSpacingMultiple: 1.15, isTextBox: true });

  s.addText("BERtotal = [ (BERhdr \u00d7 Lhdr) + (BERdata \u00d7 Ldata) ] / (Lhdr + Ldata)", {
    x: 0.5, y: 1.9, w: 5.75, h: 0.55, fontFace: HEAD_FONT, fontSize: 11.5, italic: true, color: STEEL, align: "left", valign: "top", isTextBox: true,
  });

  const regions = [
    { icon: "check", title: "Optimal Region  (SNIR \u2265 15 dB)", body: "Near-zero BER; 100% PDR; throughput maxed at 31.50 Mbps.", tColor: "0E8388" },
    { icon: "alert", title: "Critical Degradation  (SNIR < 15 dB)", body: "Small per-bit error rises are amplified exponentially; frame success crosses the 50% PDR threshold.", tColor: "C77B14" },
    { icon: "xcircle", title: "Complete Failure  (SNIR = 2 dB)", body: "FCS failures dominate; PDR = 0.00%; delay hits the 500 ms retry ceiling.", tColor: WARN_RED },
  ];
  let ry = 2.62;
  const rh = 1.36;
  regions.forEach((r) => {
    s.addShape("roundRect", { x: 0.5, y: ry, w: 5.75, h: rh, rectRadius: 0.09, fill: { color: WHITE }, line: { color: CARD_ALT2, width: 1 } });
    iconCircle(s, r.icon, 0.66, ry + 0.16, 0.5, r.tColor, { pad: 0.24 });
    s.addText(r.title, { x: 1.32, y: ry + 0.14, w: 4.75, h: 0.36, fontFace: BODY_FONT, fontSize: 12, bold: true, color: NAVY, margin: 0, isTextBox: true });
    s.addText(r.body, { x: 1.32, y: ry + 0.5, w: 4.75, h: rh - 0.6, fontFace: BODY_FONT, fontSize: 11, color: TEXT_DARK, margin: 0, lineSpacingMultiple: 1.12, isTextBox: true });
    ry += rh + 0.16;
  });

  imgBox(s, "fig3_task2_snir_ber_pdr_fixed.png", 6.55, 1.28, 6.28, 1.79, "Figure 3. Impact of SNIR on Bit Error Rate and Packet Delivery Ratio");

  footerNote(s, 5);
}

// ---------------- Slide 6: Task 3 ----------------
{
  const s = pres.addSlide();
  s.background = { color: BG_LIGHT };
  sectionHeader(s, "Task 3 — Wired vs. Wireless Saturation Comparison", "compare");

  s.addText([
    { text: "Setup:  ", options: { bold: true, color: NAVY } },
    { text: "Equivalent 160 Mbps offered load targeting a 100 Mbps bottleneck link, at 90%, 100%, and 110% overload factors.", options: { color: TEXT_DARK } },
  ], { x: 0.5, y: 1.22, w: 12.3, h: 0.4, fontFace: BODY_FONT, fontSize: 13, align: "left", valign: "top", isTextBox: true });

  const rowsData = [
    ["Performance Characteristic", "Wireless (802.11)", "Wired (Ethernet)"],
    ["Media Access Control", "CSMA/CA (Half-Duplex)", "Switched Ethernet (Full-Duplex)"],
    ["Collision Overhead", "High — wasted airtime on retries", "Zero — isolated collision domains"],
    ["100% Load PDR", "42.10%", "99.20%"],
    ["100% Load Throughput", "29.80 Mbps", "95.10 Mbps"],
    ["100% Load Delay", "88.40 ms", "1.20 ms"],
  ];
  const tblRows = rowsData.map((r, ri) => {
    if (ri === 0) {
      return r.map((c) => ({ text: c, options: { fill: { color: NAVY }, color: WHITE, bold: true, fontSize: 12, align: "center", valign: "middle", fontFace: BODY_FONT } }));
    }
    const isMetric = ri >= 3;
    return [
      { text: r[0], options: { fill: { color: ri % 2 === 0 ? CARD_ALT : WHITE }, color: TEXT_DARK, bold: true, fontSize: 11.5, align: "left", valign: "middle", fontFace: BODY_FONT } },
      { text: r[1], options: { fill: { color: ri % 2 === 0 ? CARD_ALT : WHITE }, color: isMetric ? WARN_RED : TEXT_DARK, bold: isMetric, fontSize: 11.5, align: "center", valign: "middle", fontFace: BODY_FONT } },
      { text: r[2], options: { fill: { color: ri % 2 === 0 ? CARD_ALT : WHITE }, color: isMetric ? "0E8388" : TEXT_DARK, bold: isMetric, fontSize: 11.5, align: "center", valign: "middle", fontFace: BODY_FONT } },
    ];
  });
  s.addTable(tblRows, {
    x: 0.5, y: 1.75, w: 5.9, colW: [2.5, 1.7, 1.7],
    rowH: [0.42, 0.55, 0.65, 0.5, 0.5, 0.5],
    border: { type: "solid", color: CARD_ALT2, pt: 0.75 },
    autoPage: false,
  });

  imgBox(s, "fig4_wired_vs_wireless.png", 6.75, 1.75, 6.1, 2.185, "Figure 4. PDR and Throughput: Wired vs. Wireless under Saturation");

  s.addText("Wireless capacity is bounded well below the wired ceiling at every load factor tested — the gap widens further under 110% overload.", {
    x: 0.5, y: 5.55, w: 12.3, h: 0.5, fontFace: BODY_FONT, fontSize: 12, italic: true, color: TEXT_MUTED, align: "left", valign: "top", isTextBox: true,
  });

  footerNote(s, 6);
}

// ---------------- Slide 7: Overall Statistical Summary ----------------
{
  const s = pres.addSlide();
  s.background = { color: BG_LIGHT };
  sectionHeader(s, "Overall Statistical Summary", "bar");

  s.addText("Aggregated across all simulation runs in Tasks 1\u20133.", {
    x: 0.5, y: 1.2, w: 12.3, h: 0.35, fontFace: BODY_FONT, fontSize: 12.5, italic: true, color: TEXT_MUTED, isTextBox: true,
  });

  const stats = [
    { label: "PDR", avg: "62.45%", range: "0.00% \u2013 100.00%", driver: "MAC collisions & background noise corruption" },
    { label: "Throughput", avg: "32.10", unit: "Mbps", range: "0.00 \u2013 95.40 Mbps", driver: "Physical link capacity & CSMA overhead" },
    { label: "End-to-End Delay", avg: "185.30", unit: "ms", range: "0.85 \u2013 1420.50 ms", driver: "Retransmissions & queue backoff accumulation" },
    { label: "Bit Error Rate", avg: "0.0834", range: "0.0000 \u2013 0.4821", driver: "Physical noise floor degradation" },
  ];
  const cw = 2.94, gap = 0.22, cx0 = 0.5, cy = 1.75, chh = 3.9;
  stats.forEach((st, i) => {
    const x = cx0 + i * (cw + gap);
    s.addShape("roundRect", { x, y: cy, w: cw, h: chh, rectRadius: 0.1, fill: { color: i === 0 ? NAVY : WHITE }, line: { color: CARD_ALT2, width: i === 0 ? 0 : 1 } });
    const onDark = i === 0;
    s.addText(st.label.toUpperCase(), {
      x: x + 0.2, y: cy + 0.22, w: cw - 0.4, h: 0.5, fontFace: BODY_FONT, fontSize: 12, bold: true,
      color: onDark ? CYAN : STEEL, charSpacing: 1, align: "left", valign: "top", margin: 0, isTextBox: true,
    });
    s.addText(st.avg, {
      x: x + 0.15, y: cy + 0.75, w: cw - 0.3, h: 1.05, fontFace: HEAD_FONT, fontSize: 40, bold: true,
      color: onDark ? WHITE : NAVY, align: "left", valign: "top", margin: 0, isTextBox: true,
    });
    if (st.unit) {
      s.addText(st.unit, { x: x + 0.2, y: cy + 1.68, w: cw - 0.4, h: 0.3, fontFace: BODY_FONT, fontSize: 12, color: onDark ? "AFC3DE" : TEXT_MUTED, margin: 0, isTextBox: true });
    }
    s.addText("average", { x: x + 0.2, y: cy + (st.unit ? 1.98 : 1.68), w: cw - 0.4, h: 0.28, fontFace: BODY_FONT, fontSize: 10, italic: true, color: onDark ? "AFC3DE" : TEXT_MUTED, margin: 0, isTextBox: true });

    s.addShape("line", { x: x + 0.2, y: cy + 2.45, w: cw - 0.4, h: 0, line: { color: onDark ? "2C4A73" : CARD_ALT2, width: 1 } });
    s.addText("RANGE", { x: x + 0.2, y: cy + 2.55, w: cw - 0.4, h: 0.25, fontFace: BODY_FONT, fontSize: 9, bold: true, color: onDark ? "8FA6C7" : TEXT_MUTED, charSpacing: 1, margin: 0, isTextBox: true });
    s.addText(st.range, { x: x + 0.2, y: cy + 2.8, w: cw - 0.4, h: 0.4, fontFace: BODY_FONT, fontSize: 11.5, color: onDark ? WHITE : TEXT_DARK, margin: 0, isTextBox: true });

    s.addText("PRIMARY DRIVER", { x: x + 0.2, y: cy + 3.25, w: cw - 0.4, h: 0.22, fontFace: BODY_FONT, fontSize: 8.5, bold: true, color: onDark ? "8FA6C7" : TEXT_MUTED, charSpacing: 1, margin: 0, isTextBox: true });
    s.addText(st.driver, { x: x + 0.2, y: cy + 3.47, w: cw - 0.4, h: 0.42, fontFace: BODY_FONT, fontSize: 9.5, italic: true, color: onDark ? "D7E4F5" : TEXT_MUTED, margin: 0, lineSpacingMultiple: 1.05, isTextBox: true });
  });

  footerNote(s, 7);
}

// ---------------- Slide 8: Conclusions ----------------
{
  const s = pres.addSlide();
  s.background = { color: NAVY };
  sectionHeader(s, "Key Conclusions & Recommendations", "wifi", { dark: true });

  const recs = [
    { icon: "zap", title: "Collision Mitigation in High Density  (N \u2265 8)", body: "Enable RTS/CTS handshaking or increase the initial contention window (CWmin = 63) to prevent collision cascades." },
    { icon: "sliders", title: "Dynamic Link Adaptation", body: "Implement adaptive Modulation and Coding Schemes (MCS) to maintain link stability when SNIR drops below 15 dB." },
    { icon: "map", title: "Network Planning", body: "Use multi-channel Access Point deployments and 802.11e EDCA traffic prioritization to eliminate half-duplex wireless bottlenecks." },
  ];
  let ry = 1.75;
  const rh = 1.45;
  recs.forEach((r) => {
    s.addShape("roundRect", { x: 0.5, y: ry, w: 12.3, h: rh, rectRadius: 0.1, fill: { color: "12315C" }, line: { type: "none" } });
    iconCircle(s, r.icon, 0.78, ry + (rh - 0.7) / 2, 0.7, CYAN, { pad: 0.26 });
    s.addText(r.title, { x: 1.85, y: ry + 0.24, w: 10.6, h: 0.42, fontFace: BODY_FONT, fontSize: 16, bold: true, color: WHITE, margin: 0, isTextBox: true });
    s.addText(r.body, { x: 1.85, y: ry + 0.68, w: 10.6, h: 0.66, fontFace: BODY_FONT, fontSize: 12.5, color: "C9D9EE", margin: 0, lineSpacingMultiple: 1.15, isTextBox: true });
    ry += rh + 0.22;
  });

  footerNote(s, 8, true);
}

pres.writeFile({ fileName: D + "CSE4616_Assignment1_Presentation_220041122.pptx" }).then((fname) => {
  console.log("wrote", fname);
});