"""Baseline: each model reads each case with no hint, RUNS times. Resumable: existing answers are skipped.

Usage: .venv/bin/python scripts/07_baseline.py MODEL RUNS   (run one process per model, in parallel)
Writes data/baseline/<model>/<case>_r<k>.json with {"raw", "parsed", "time"}.
"""
import json
import pathlib
import sys
import time

import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from llm_cli import ask, parse  # noqa: E402


def main(model, runs):
    cases = pd.read_csv("data/cases/candidates.csv").case_id
    out = pathlib.Path("data/baseline") / model
    out.mkdir(parents=True, exist_ok=True)
    streak = 0                                        # consecutive failures: quota is out, so stop instead of
    for k in range(1, runs + 1):                      # writing empty answers (rerun later; parsed answers are kept)
        for cid in cases:
            f = out / f"{cid}_r{k}.json"
            if f.exists() and json.loads(f.read_text())["parsed"]:
                continue
            raw = ""
            for attempt in range(3):                  # empty output = tool hiccup or rate limit, not an answer
                try:
                    raw = ask(model, f"data/images/{cid}.png")
                except Exception as e:                # timeout
                    raw = ""
                    print(model, cid, k, "error", type(e).__name__, flush=True)
                if parse(raw):
                    break
                time.sleep(30 * (attempt + 1))
            f.write_text(json.dumps({"raw": raw, "parsed": parse(raw), "time": time.strftime("%Y-%m-%dT%H:%M:%S")},
                                    ensure_ascii=False, indent=1))
            p = parse(raw) or {}
            print(model, cid, f"r{k}", p.get("diagnosis", "UNPARSED"), p.get("stemi", ""), flush=True)
            streak = 0 if p else streak + 1
            if streak >= 5:
                sys.exit(f"{model}: 5 failures in a row (quota?), stopping; rerun later to fill the gaps")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
    gaps = [f for f in (pathlib.Path("data/baseline") / sys.argv[1]).glob("*.json") if not json.loads(f.read_text())["parsed"]]
    if gaps:
        sys.exit(f"{len(gaps)} unparsed answers remain for {sys.argv[1]}; rerun to fill them")
