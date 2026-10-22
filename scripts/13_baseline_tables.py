"""Results tables for the cases and the no-hint baseline (3 runs x 6 models).

Writes analysis/baseline_tables.md: case characteristics, accuracy by group (mean of 3 runs), run-to-run
stability, false STEMI calls, LVH over-calls, and the number of baseline-correct cases per model.
Usage: .venv/bin/python scripts/13_baseline_tables.py
"""
import importlib
import json
import pathlib
import sys

import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).parent))
score = importlib.import_module("08_score_baseline")
ORDER = ["claude-opus-5-5", "gpt-6-astra", "gemini-3.8-flash-high", "claude-sonnet-5-5", "gpt-6.1-sol", "gpt-6-luna", "gpt-5.6-sol", "gpt-5.6-luna"]
NAME = {"claude-opus-5-5": "Opus", "gpt-6-astra": "Astra", "gemini-3.8-flash-high": "Gemini",
        "claude-sonnet-5-5": "Sonnet", "gpt-6.1-sol": "6.1-sol", "gpt-6-luna": "6-luna", "gpt-5.6-sol": "5.6-sol", "gpt-5.6-luna": "5.6-luna"}
GROUPS = ["normal", "acute_mi", "old_mi", "afib", "lbbb", "rbbb", "wpw", "first_deg_avb"]
GNAME = {"normal": "Normal", "acute_mi": "Acute-stage MI", "old_mi": "Old MI", "afib": "Atrial fibrillation",
         "lbbb": "LBBB", "rbbb": "RBBB", "wpw": "WPW", "first_deg_avb": "First-degree AV block"}

cases = pd.read_csv("data/cases/candidates.csv")
df = pd.concat([score.score(r).assign(run=r) for r in "123"])
dx = []
for m in ORDER:
    for f in pathlib.Path("data/baseline", m).glob("*.json"):
        p = json.loads(f.read_text())["parsed"]
        cid, r = f.stem.split("_r")
        dx.append({"model": m, "case_id": cid, "run": r, "dx": str(p["diagnosis"]).lower()})
dx = pd.DataFrame(dx)
out = []

out.append("**Table 3. Cases.**\n\n| Group | n | Age, median (IQR) | Female |\n|---|---:|---|---:|")
for g in GROUPS:
    c = cases[cases.group == g]
    q = c.age.quantile([.25, .5, .75])
    out.append(f"| {GNAME[g]} | {len(c)} | {q[.5]:.0f} ({q[.25]:.0f}–{q[.75]:.0f}) | {(c.sex == 'F').sum()} |")

out.append("\n**Table 4. Baseline accuracy (% correct, mean of three runs). Opus = Claude Opus 5.5, Astra = GPT-6-astra, Gemini = Gemini 3.8 Flash, Sonnet = Claude Sonnet 5.5, 6.1-sol = GPT-6.1-sol, 6-luna = GPT-6-luna, 5.6-sol/5.6-luna = GPT-5.6-sol/luna.**\n")
out.append("| Group (n) | " + " | ".join(NAME[m] for m in ORDER) + " |")
out.append("|---" + "|---:" * len(ORDER) + "|")
for g in GROUPS:
    n = (cases.group == g).sum()
    out.append(f"| {GNAME[g]} ({n}) | " + " | ".join(
        f"{df[(df.model == m) & (df.group == g)].correct.mean():.0%}" for m in ORDER) + " |")
out.append("| **All (101)** | " + " | ".join(f"**{df[df.model == m].correct.mean():.0%}**" for m in ORDER) + " |")
rows = {
    "Same answer, 3/3 runs": lambda m: f"{(dx[dx.model == m].groupby('case_id').dx.nunique() == 1).sum()}/101",
    "Baseline-correct cases": lambda m: f"{(df[df.model == m].groupby('case_id').correct.sum() == 3).sum()}",
    "STEMI called, non-acute": lambda m: f"{df[(df.model == m) & (df.group != 'acute_mi')].said_stemi.mean():.0%}",
    "STEMI called, acute MI": lambda m: f"{df[(df.model == m) & (df.group == 'acute_mi')].said_stemi.mean():.0%}",
    "LVH as main answer": lambda m: f"{(dx[dx.model == m].dx == 'lvh').mean():.0%}",
}
for k, f in rows.items():
    out.append(f"| {k} | " + " | ".join(f(m) for m in ORDER) + " |")
text = "\n".join(out)
pathlib.Path("analysis/baseline_tables.md").write_text(text + "\n")
print(text)
