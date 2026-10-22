"""Sokolow-Lyon voltage (SV1 + max(RV5, RV6)) from a median beat, per case, to check the LVH over-call.

Median beat: R peaks detected on lead II, 10-s record at 500 Hz; window -300..+500 ms; baseline = median of the
PR segment (-120..-60 ms before R). R = max in +-60 ms of the peak, S = deepest point 0..+100 ms, both vs baseline.
Usage: .venv/bin/python scripts/18_voltage.py  -> analysis/voltage.csv and a summary on stdout
"""
import numpy as np
import pandas as pd
import wfdb
from scipy.signal import find_peaks

FS = 500


def median_beat(sig, peaks):
    lo, hi = int(0.3 * FS), int(0.5 * FS)
    beats = [sig[p - lo:p + hi] for p in peaks if p - lo >= 0 and p + hi <= len(sig)]
    return np.median(beats, axis=0), lo


def sokolow(path):
    rec = wfdb.rdrecord(f"data/ptbxl/{path}")
    names = [n.upper() for n in rec.sig_name]
    x = rec.p_signal
    det = None
    for lead in ("II", "V5", "I", "V6"):   # first lead with a clear, regular set of QRS peaks
        s = x[:, names.index(lead)]
        s = np.abs(s - np.median(s))
        peaks, _ = find_peaks(s, distance=int(0.3 * FS), prominence=0.5 * (np.percentile(s, 99.5) - np.median(s)))
        if 5 <= len(peaks) <= 25:
            det = peaks
            break
    peaks = det if det is not None else peaks
    out = {}
    for lead in ("V1", "V5", "V6"):
        b, z = median_beat(x[:, names.index(lead)], peaks)
        base = np.median(b[z - int(0.12 * FS):z - int(0.06 * FS)])
        out[f"R{lead}"] = float(b[z - int(0.06 * FS):z + int(0.06 * FS)].max() - base)
        out[f"S{lead}"] = float(base - b[z:z + int(0.10 * FS)].min())
    out["sokolow_mV"] = out["SV1"] + max(out["RV5"], out["RV6"])
    out["n_beats"] = len(peaks)
    return out


def main():
    cases = pd.read_csv("data/cases/candidates.csv")
    rows = [{"case_id": r.case_id, "group": r.group, **sokolow(r.filename_hr)} for r in cases.itertuples()]
    df = pd.DataFrame(rows)
    df.to_csv("analysis/voltage.csv", index=False)
    print(df.groupby("group").sokolow_mV.describe()[["count", "50%", "min", "max"]].round(2))
    print("normal cases >= 3.5 mV:", df[(df.group == "normal") & (df.sokolow_mV >= 3.5)].case_id.tolist())


if __name__ == "__main__":
    main()
