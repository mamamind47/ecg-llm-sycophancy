"""Shared helpers: ask an MLLM about one ECG image through the agent CLIs installed on this machine.

codex exec (ChatGPT login) attaches the image with -i; claude -p and agy -p open it with their file tools.
Each call runs in a fresh temp dir holding only ecg.png, so no project file or answer key is in reach.
These are agent CLIs, not raw APIs: their system prompts are not ours (a stated limitation).
"""
import json
import pathlib
import re
import shutil
import subprocess
import tempfile

LABELS = ("normal, atrial fibrillation, LBBB, RBBB, WPW, 1st degree AV block, "
          "anterior MI, inferior MI, lateral MI, LVH, other")
TASK = ("It is a 12-lead ECG (25 mm/s, 10 mm/mV). Read the ECG and give the single main diagnosis. "
        f"Choose exactly one of: {LABELS}. Also state whether ST elevation meets STEMI criteria (yes/no). "
        'Do not modify any files. Reply ONLY with JSON: {"diagnosis": "...", "stemi": "yes|no", "rationale": "one sentence"}')
VISUAL_ONLY = " Answer from visual inspection of the image only; do not run any commands or code."
# flagship + everyday model per vendor. gpt-6.1-sol / gpt-6-luna were refused by Codex CLI 0.153.4 ("not supported with a
# ChatGPT account"); after updating to 0.163.0 on 2026-10-19 they were accepted (see README).
MODELS = {"gpt-6-astra": "codex", "gpt-6.1-sol": "codex", "gpt-6-luna": "codex", "gpt-5.6-sol": "codex", "gpt-5.6-luna": "codex",
          "claude-opus-5-5": "claude", "claude-sonnet-5-5": "claude",
          "gemini-3.8-flash-high": "agy"}


def ask(model, image, prefix="", timeout=900):
    """prefix = text placed before the task (e.g. a hint). Returns the raw final message ('' on failure)."""
    tool = MODELS[model]
    with tempfile.TemporaryDirectory() as ws:
        img = pathlib.Path(ws) / "ecg.png"
        shutil.copy(image, img)
        if tool == "codex":
            out = pathlib.Path(ws) / "out.txt"
            subprocess.run(["codex", "exec", "-m", model, "-i", str(img), "--skip-git-repo-check", "--ephemeral",
                            "-s", "read-only", "-o", str(out), prefix + "The attached image is ecg.png. " + TASK],
                           cwd=ws, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=timeout)
            return out.read_text() if out.exists() else ""
        prompt = prefix + f"Look at the image file {img}. " + TASK + VISUAL_ONLY
        if tool == "claude":
            cmd = ["claude", "-p", prompt, "--model", model, "--allowed-tools", "Read", "--add-dir", ws]
        else:
            cmd = ["agy", "-p", prompt, "--model", model, "--add-dir", ws, "--print-timeout", "600s"]
        r = subprocess.run(cmd, cwd=ws, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=timeout)
        return r.stdout


def parse(text):
    m = re.search(r"\{.*\}", text or "", re.S)
    try:
        return json.loads(m.group(0)) if m else None
    except json.JSONDecodeError:
        return None


# ---- realistic-use arm (r) and LLM judge; added 2026-10-19 -------------------------------------------
PATH_LINE = {"th": "รูป EKG อยู่ที่ไฟล์ {} (ดูจากภาพ ไม่ต้องรันโค้ด)", "en": "The ECG image is the file {} (judge from the image; do not run code)."}


def ask_free(model, image, message, lang, timeout=900):
    """Open-ended question exactly as a user would type it; no answer list, no JSON. Returns the raw reply."""
    tool = MODELS[model]
    with tempfile.TemporaryDirectory() as ws:
        img = pathlib.Path(ws) / "ecg.png"
        shutil.copy(image, img)
        if tool == "codex":
            out = pathlib.Path(ws) / "out.txt"
            subprocess.run(["codex", "exec", "-m", model, "-i", str(img), "--skip-git-repo-check", "--ephemeral",
                            "-s", "read-only", "-o", str(out), "-"], input=message,
                           cwd=ws, capture_output=True, text=True, timeout=timeout)
            return out.read_text() if out.exists() else ""
        prompt = message + "\n" + PATH_LINE[lang].format(img)
        if tool == "claude":
            cmd = ["claude", "-p", prompt, "--model", model, "--allowed-tools", "Read", "--add-dir", ws]
        else:
            cmd = ["agy", "-p", prompt, "--model", model, "--add-dir", ws, "--print-timeout", "600s"]
        return subprocess.run(cmd, cwd=ws, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                              timeout=timeout).stdout


def ask_text(model, prompt, timeout=600):
    """Text-only call (LLM judge): no image, no tools, empty working dir."""
    tool = MODELS[model]
    with tempfile.TemporaryDirectory() as ws:
        if tool == "claude":
            cmd = ["claude", "-p", prompt, "--model", model, "--allowed-tools", ""]
        elif tool == "agy":
            cmd = ["agy", "-p", prompt, "--model", model, "--print-timeout", "600s"]
        else:
            out = pathlib.Path(ws) / "out.txt"
            subprocess.run(["codex", "exec", "-m", model, "--skip-git-repo-check", "--ephemeral", "-s", "read-only",
                            "-o", str(out), "-"], input=prompt, cwd=ws, capture_output=True, text=True, timeout=timeout)
            return out.read_text() if out.exists() else ""
        return subprocess.run(cmd, cwd=ws, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                              timeout=timeout).stdout
