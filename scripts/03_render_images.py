"""Render PTB-XL 500 Hz records as standard 12-lead paper ECG images.

Layout: 3x4 grid (I aVR V1 V4 / II aVL V2 V5 / III aVF V3 V6), 2.5 s per column,
plus a 10 s lead-II rhythm strip. Paper 25 mm/s, 10 mm/mV, 1 mm / 5 mm grid, 1 mV calibration pulse.
No diagnosis, report text or patient data is printed on the image.
Usage: .venv/bin/python scripts/03_render_images.py
Output: data/images/<case_id>.png
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import wfdb

MM_PER_S, MM_PER_MV = 25.0, 10.0
DPI = 200
LAYOUT = [["I", "AVR", "V1", "V4"], ["II", "AVL", "V2", "V5"], ["III", "AVF", "V3", "V6"]]
LABEL = {"AVR": "aVR", "AVL": "aVL", "AVF": "aVF"}
ROW_GAP = 30.0                         # mm between baselines
CAL_W = 10.0                           # mm reserved on the left for the calibration pulse
W = CAL_W + 10 * MM_PER_S + 5          # page width, mm
H = ROW_GAP * 3 + 30                   # page height, mm (rhythm-strip baseline 15 mm above the bottom)


def draw_grid(ax):
    for x in np.arange(0, W + 0.01, 1):
        ax.axvline(x, color="#f4c2c2", lw=0.3 if x % 5 else 0.8, zorder=0)
    for y in np.arange(0, H + 0.01, 1):
        ax.axhline(y, color="#f4c2c2", lw=0.3 if y % 5 else 0.8, zorder=0)


def draw_cal(ax, y0):
    ax.plot([1, 3, 3, 7, 7, 9], [y0, y0, y0 + MM_PER_MV, y0 + MM_PER_MV, y0, y0], color="k", lw=0.8)


def render(record_path, out_png):
    rec = wfdb.rdrecord(record_path)
    sig = {n.upper(): rec.p_signal[:, i] for i, n in enumerate(rec.sig_name)}
    fs = rec.fs
    fig = plt.figure(figsize=(W / 25.4, H / 25.4), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    draw_grid(ax)

    for r, row in enumerate(LAYOUT):
        y0 = H - 15 - r * ROW_GAP
        draw_cal(ax, y0)
        for c, lead in enumerate(row):
            a, b = int(c * 2.5 * fs), int((c + 1) * 2.5 * fs)
            x = CAL_W + np.arange(a, b) / fs * MM_PER_S
            ax.plot(x, y0 + sig[lead][a:b] * MM_PER_MV, color="k", lw=0.6)
            ax.text(CAL_W + c * 2.5 * MM_PER_S + 1, y0 + 6, LABEL.get(lead, lead), fontsize=7)
            if c:  # lead-change tick, as printed by most machines
                ax.plot([x[0]] * 2, [y0 - 2, y0 + 2], color="k", lw=0.6)

    y0 = H - 15 - 3 * ROW_GAP          # rhythm strip
    draw_cal(ax, y0)
    x = CAL_W + np.arange(len(sig["II"])) / fs * MM_PER_S
    ax.plot(x, y0 + sig["II"] * MM_PER_MV, color="k", lw=0.6)
    ax.text(CAL_W + 1, y0 + 6, "II", fontsize=7)
    ax.text(W - 60, 3, "25 mm/s   10 mm/mV", fontsize=6)
    fig.savefig(out_png, dpi=DPI)
    plt.close(fig)


def main():
    cases = pd.read_csv("data/cases/candidates.csv")
    os.makedirs("data/images", exist_ok=True)
    for _, r in cases.iterrows():
        out = f"data/images/{r.case_id}.png"
        if not os.path.exists(out):
            render(f"data/ptbxl/{r.filename_hr}", out)
    print(len(cases), "images in data/images/")


if __name__ == "__main__":
    main()
