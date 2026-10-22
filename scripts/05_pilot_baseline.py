"""Pilot: do CLI-accessible MLLMs agree to read our ECG images, and how do they answer (no hint)?

Runs each case through:
  codex exec (ChatGPT account): gpt-5.6-sol, gpt-6-astra  -- image attached with -i
  agy -p (Antigravity):         gemini-3.8-flash-high     -- agent opens the file with view_file
  claude -p (Claude Code):      claude-sonnet-5-5, claude-opus-5-5 -- fresh session, Read tool only,
                                run from a temp dir so no project memory or answer key is in reach
These are agent CLIs, not raw APIs: their system prompts are not ours, so the pilot only checks
feasibility (refusals, format, rough accuracy). The study itself should use the APIs.
Usage: .venv/bin/python scripts/05_pilot_baseline.py OUT_DIR CASE_ID [CASE_ID ...]
       PILOT_MODELS=claude-sonnet-5-5,claude-opus-5-5 ... to run a subset (results.csv is then named per subset)
Writes OUT_DIR/<model>/<case>.json (parsed answer or raw text) and OUT_DIR/results.csv.
"""
import csv
import json
import pathlib
import re
import shutil
import subprocess
import sys
import os
import tempfile

LABELS = ("normal, atrial fibrillation, LBBB, RBBB, WPW, 1st degree AV block, "
          "anterior MI, inferior MI, lateral MI, LVH, other")
TASK = ("It is a 12-lead ECG (25 mm/s, 10 mm/mV). Read the ECG and give the single main diagnosis. "
        f"Choose exactly one of: {LABELS}. Also state whether ST elevation meets STEMI criteria (yes/no). "
        'Do not modify any files. Reply ONLY with JSON: {"diagnosis": "...", "stemi": "yes|no", "rationale": "one sentence"}')
MODELS = {"gpt-5.6-sol": "codex", "gpt-6-astra": "codex", "gemini-3.8-flash-high": "agy",
          "claude-sonnet-5-5": "claude", "claude-opus-5-5": "claude"}


def ask(model, tool, image):
    with tempfile.TemporaryDirectory() as ws:
        img = pathlib.Path(ws) / "ecg.png"
        shutil.copy(image, img)
        if tool == "codex":
            out = pathlib.Path(ws) / "out.txt"
            subprocess.run(["codex", "exec", "-m", model, "-i", str(img), "--skip-git-repo-check", "--ephemeral",
                            "-s", "read-only", "-o", str(out), "The attached image is ecg.png. " + TASK],
                           cwd=ws, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=600)
            return out.read_text() if out.exists() else ""
        if tool == "claude":
            r = subprocess.run(["claude", "-p", f"Look at the image file {img}. " + TASK, "--model", model,
                                "--allowed-tools", "Read", "--add-dir", ws],
                               cwd=ws, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=600)
            return r.stdout
        # Without the last sentence Gemini tries to analyse the PNG with Python; headless agy denies the
        # command and returns an empty answer (pilot 2026-10-15). We want a visual read, so code is ruled out.
        r = subprocess.run(["agy", "-p", f"Look at the image file {img}. " + TASK +
                            " Answer from visual inspection of the image only; do not run any commands or code.", "--model", model,
                            "--add-dir", ws, "--print-timeout", "300s"],
                           cwd=ws, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=600)
        return r.stdout


def parse(text):
    m = re.search(r"\{.*\}", text, re.S)
    try:
        return json.loads(m.group(0)) if m else None
    except json.JSONDecodeError:
        return None


def main(out_dir, cases):
    out = pathlib.Path(out_dir)
    key = {r["case_id"]: r for r in csv.DictReader(open("data/cases/candidates.csv"))}
    rows = []
    pick = os.environ.get("PILOT_MODELS")
    models = {m: t for m, t in MODELS.items() if not pick or m in pick.split(",")}
    for model, tool in models.items():
        (out / model).mkdir(parents=True, exist_ok=True)
        for cid in cases:
            raw = ask(model, tool, f"data/images/{cid}.png")
            ans = parse(raw)
            (out / model / f"{cid}.json").write_text(json.dumps({"raw": raw, "parsed": ans}, ensure_ascii=False, indent=1))
            rows.append({"model": model, "case_id": cid, "ptbxl_group": key[cid]["group"],
                         "diagnosis": (ans or {}).get("diagnosis", "UNPARSED"), "stemi": (ans or {}).get("stemi", ""),
                         "rationale": (ans or {}).get("rationale", raw.strip()[:200])})
            print(model, cid, key[cid]["group"], "->", rows[-1]["diagnosis"], rows[-1]["stemi"], flush=True)
    name = "results.csv" if not pick else f"results_{pick.replace(',', '+')}.csv"
    with open(out / name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
