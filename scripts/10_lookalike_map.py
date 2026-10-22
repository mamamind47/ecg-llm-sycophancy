"""Freeze the look-alike map for hint arm (b): per group, the most frequent wrong baseline diagnosis.

Rule (locked 2026-10-18): pool round-1 baseline answers from all models, keep wrong answers, drop "other",
take the most frequent label (ties broken alphabetically). For acute_mi / old_mi, an MI answer is not
"wrong" in kind, so MI territory labels are dropped for those groups too. Refuses to overwrite an existing map.
Amendment 2026-10-18 (before any hint run): the original rule returned "lvh" for every group, driven by
gpt-5.6-luna answering LVH on 76/101 cases (kept as lookalike_map_v1_all_lvh.json). "lvh" is now excluded
too, so each group gets its most frequent non-LVH confusion.
Usage: .venv/bin/python scripts/10_lookalike_map.py
"""
import collections
import json
import pathlib

import pandas as pd

OUT = pathlib.Path("data/hints/lookalike_map.json")
MI = {"anterior mi", "inferior mi", "lateral mi"}
TARGET = {"normal": "normal", "afib": "atrial fibrillation", "lbbb": "lbbb", "rbbb": "rbbb", "wpw": "wpw",
          "first_deg_avb": "1st degree av block"}

if OUT.exists():
    raise SystemExit(f"{OUT} already frozen; delete it deliberately if the rule changes")
groups = pd.read_csv("data/cases/candidates.csv").set_index("case_id").group.to_dict()
counts = collections.defaultdict(collections.Counter)
for f in pathlib.Path("data/baseline").glob("*/*_r1.json"):
    p = json.loads(f.read_text())["parsed"]
    if not p:
        continue
    g, dx = groups[f.stem.split("_")[0]], str(p.get("diagnosis", "")).lower()
    if dx in ("other", "lvh") or (g in ("acute_mi", "old_mi") and dx in MI) or dx == TARGET.get(g):
        continue
    counts[g][dx] += 1
lookalike = {g: sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[0][0] for g, c in counts.items()}
OUT.write_text(json.dumps(lookalike, indent=1))
for g, c in sorted(counts.items()):
    print(f"{g:14} -> {lookalike[g]:20} from {dict(c.most_common(4))}")
