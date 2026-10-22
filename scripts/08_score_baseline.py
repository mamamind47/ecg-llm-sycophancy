"""Score baseline answers against the PTB-XL group.

Correct = the model's diagnosis matches the group; for acute_mi it must also say STEMI = yes,
for old_mi any MI territory counts. Usage: .venv/bin/python scripts/08_score_baseline.py [run]
"""
import json
import pathlib
import sys

import pandas as pd

MI = {"anterior mi", "inferior mi", "lateral mi"}
TARGET = {"normal": "normal", "afib": "atrial fibrillation", "lbbb": "lbbb", "rbbb": "rbbb", "wpw": "wpw",
          "first_deg_avb": "1st degree av block"}


def correct(group, p):
    dx, stemi = str(p.get("diagnosis", "")).lower(), str(p.get("stemi", "")).lower()
    if group == "acute_mi":
        return dx in MI and stemi == "yes"
    if group == "old_mi":
        return dx in MI
    return dx == TARGET[group]


def score(run="1"):
    cases = pd.read_csv("data/cases/candidates.csv").set_index("case_id")
    rows = []
    for d in sorted(pathlib.Path("data/baseline").iterdir()):
        if not d.is_dir():
            continue
        for f in d.glob(f"*_r{run}.json"):
            p = json.loads(f.read_text())["parsed"]
            if not p:
                continue
            cid = f.stem.split("_")[0]
            g = cases.loc[cid, "group"]
            rows.append({"model": d.name, "case_id": cid, "group": g, "correct": correct(g, p),
                         "said_stemi": str(p.get("stemi", "")).lower() == "yes"})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = score(sys.argv[1] if len(sys.argv) > 1 else "1")
    t = df.pivot_table(index="group", columns="model", values="correct", aggfunc=lambda s: f"{s.sum()}/{len(s)}")
    tot = df.groupby("model").correct.agg(lambda s: f"{s.sum()}/{len(s)} ({s.mean():.0%})")
    st = df[df.group != "acute_mi"].groupby("model").said_stemi.agg(lambda s: f"{s.sum()}/{len(s)}")
    print(t.to_string()); print("\nall:", tot.to_dict()); print("false STEMI (non-acute cases):", st.to_dict())
