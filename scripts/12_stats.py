"""Statistics for the hint experiment (arm a by default).

1. Spontaneous drift (no hint): among cases a model read correctly in baseline runs 1 and 2, how often run 3
   is wrong, and how often run 3 lands on the arm-(a) wrong target by itself. This is the no-hint control for
   abandonment and sycophancy; selecting on runs 1-2 and scoring run 3 avoids selection-on-outcome bias.
2. Per model: sycophancy and abandonment under wrong hints, with Wilson 95% CIs, against that control.
3. Thai vs English: McNemar test on paired responses (same model, case, condition, run).
4. Correct hints: accuracy under a correct hint vs the spontaneous accuracy (the "contrarian" check).
5. Pooled GEE logistic regression (clusters = case within model): sycophancy ~ model + style + language.
Usage: .venv/bin/python scripts/12_stats.py [arm]  ->  prints tables; writes analysis/stats_<arm>.md
"""
import importlib
import json
import pathlib
import sys

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.contingency_tables import mcnemar
from statsmodels.stats.proportion import proportion_confint

sys.path.insert(0, str(pathlib.Path(__file__).parent))
score = importlib.import_module("08_score_baseline")
hints = importlib.import_module("11_analyze_hints")
hint_cfg = importlib.import_module("09_hints")


def ci(k, n):
    if n == 0:
        return "–"
    lo, hi = proportion_confint(k, n, method="wilson")
    return f"{k / n:.1%} [{lo:.1%}, {hi:.1%}] ({k}/{n})"


def spontaneous():
    """Held-out run 3 among cases correct in runs 1 and 2."""
    rows = []
    groups = pd.read_csv("data/cases/candidates.csv").set_index("case_id").group
    for d in sorted(pathlib.Path("data/baseline").iterdir()):
        if not d.is_dir():
            continue
        runs = {}
        for f in d.glob("*.json"):
            cid, r = f.stem.split("_r")
            p = json.loads(f.read_text())["parsed"]
            if p:
                runs.setdefault(cid, {})[r] = p
        for cid, rr in runs.items():
            if not all(k in rr for k in "123"):
                continue
            g = groups[cid]
            if score.correct(g, rr["1"]) and score.correct(g, rr["2"]):
                rows.append({"model": d.name, "case": cid,
                             "r3_correct": score.correct(g, rr["3"]),
                             "r3_hits_target": hints.matches_target(hint_cfg.wrong_target_a(g), rr["3"])})
    return pd.DataFrame(rows)


def no_hint_control():
    rows = []
    for f in pathlib.Path("data/hints/n").glob("*/*.json"):
        d = json.loads(f.read_text())
        if d["parsed"]:
            rows.append({"model": f.parent.name, "case": d["case"], "correct": score.correct(d["group"], d["parsed"]),
                         "hits_target": hints.matches_target(d["target"], d["parsed"])})
    return pd.DataFrame(rows, columns=["model", "case", "correct", "hits_target"])


def main(arm="a"):
    df = hints.load(arm)
    sp = spontaneous()
    out = [f"# Hint experiment statistics, arm ({arm})\n", f"Responses scored: {len(df)}\n"]

    ctrl = no_hint_control()
    out.append("## Wrong hints vs the no-hint control arm (n)\n")
    out.append("Control = the same baseline-correct cases re-asked without a hint (arm n). \"Target\" = the arm-(a) wrong target.\n")
    out.append("| Model | Sycophancy (= hinted target) | No hint: hit that target | Abandonment | No hint: abandonment |")
    out.append("|---|---|---|---|---|")
    for m in sorted(df.model.unique()):
        w = df[(df.model == m) & df.wrong_hint]
        c = ctrl[ctrl.model == m]
        out.append(f"| {m} | {ci(int(w.sycophantic.sum()), len(w))} | {ci(int(c.hits_target.sum()), len(c))} | "
                   f"{ci(int((~w.correct).sum()), len(w))} | {ci(int((~c.correct).sum()), len(c))} |")

    out.append("\n## Secondary drift estimate: held-out baseline run 3 (cases correct in runs 1-2)\n")
    out.append("| Model | Sycophancy (= hinted target) | Spontaneous hit of that target | Abandonment (no longer correct) | Spontaneous abandonment |")
    out.append("|---|---|---|---|---|")
    for m in sorted(df.model.unique()):
        w = df[(df.model == m) & df.wrong_hint]
        s = sp[sp.model == m]
        out.append(f"| {m} | {ci(int(w.sycophantic.sum()), len(w))} | {ci(int(s.r3_hits_target.sum()), len(s))} | "
                   f"{ci(int((~w.correct).sum()), len(w))} | {ci(int((~s.r3_correct).sum()), len(s))} |")

    out.append("\n## Sycophancy by hint style\n")
    styles = ["wrong-overconfidence", "wrong-recency", "wrong-consensus"] if arm == "a" else ["lookalike-overconfidence"]
    out.append("| Model | " + " | ".join(styles) + " |")
    out.append("|---" * (len(styles) + 1) + "|")
    for m in sorted(df.model.unique()):
        cells = []
        for st in styles:
            w = df[(df.model == m) & (df.condition == st)]
            cells.append(ci(int(w.sycophantic.sum()), len(w)))
        out.append(f"| {m} | " + " | ".join(cells) + " |")

    out.append("\n## Thai vs English (paired, McNemar exact)\n")
    out.append("| Model | EN | TH | discordant EN-only / TH-only | p |")
    out.append("|---|---|---|---|---|")
    files = []
    for f in pathlib.Path("data/hints", arm).glob("*/*.json"):
        d = json.loads(f.read_text())
        if d["parsed"] and not d["condition"].startswith("correct"):
            files.append({"model": f.parent.name, "case": d["case"], "condition": d["condition"],
                          "run": f.stem.rsplit("_r", 1)[1], "lang": d["lang"],
                          "syc": hints.matches_target(d["target"], d["parsed"])})
    pf = pd.DataFrame(files)
    for m in sorted(pf.model.unique()):
        pv = pf[pf.model == m].pivot_table(index=["case", "condition", "run"], columns="lang", values="syc", aggfunc="first").dropna()
        if pv.empty:
            continue
        en, th = pv["en"].astype(bool), pv["th"].astype(bool)
        b, c = int((en & ~th).sum()), int((~en & th).sum())
        p = mcnemar([[int((en & th).sum()), b], [c, int((~en & ~th).sum())]], exact=True).pvalue
        out.append(f"| {m} | {ci(int(en.sum()), len(en))} | {ci(int(th.sum()), len(th))} | {b} / {c} | {p:.3g} |")

    if arm == "a":
        out.append("\n## Correct hints vs no-hint accuracy (contrarian check)\n")
        out.append("| Model | Correct under correct hint | Spontaneous accuracy (held-out run 3) |")
        out.append("|---|---|---|")
        for m in sorted(df.model.unique()):
            c = df[(df.model == m) & ~df.wrong_hint]
            s = sp[sp.model == m]
            out.append(f"| {m} | {ci(int(c.correct.sum()), len(c))} | {ci(int(s.r3_correct.sum()), len(s))} |")

    out.append("\n## Pooled GEE logistic regression (exchangeable, clusters = model x case)\n")
    g = df[df.wrong_hint].copy()
    g["syc"] = g.sycophantic.astype(int)
    g["cluster"] = g.model + "_" + g.case
    try:
        fit = smf.gee("syc ~ C(model, Treatment('claude-opus-5-5')) + C(condition) + C(lang, Treatment('en'))",
                      groups="cluster", data=g, family=sm.families.Binomial(),
                      cov_struct=sm.cov_struct.Exchangeable()).fit()
        tab = pd.DataFrame({"OR": np.exp(fit.params), "lo": np.exp(fit.conf_int()[0]),
                            "hi": np.exp(fit.conf_int()[1]), "p": fit.pvalues}).round(3)
        out.append("```\n" + tab.to_string() + "\n```")
    except Exception as e:                            # rare events can make the fit fail; say so instead of hiding it
        out.append(f"GEE did not converge: {e}")

    text = "\n".join(out)
    pathlib.Path("analysis").mkdir(exist_ok=True)
    pathlib.Path(f"analysis/stats_{arm}.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "a")
