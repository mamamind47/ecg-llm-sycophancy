#!/bin/sh
# Wait until a wall-clock time, then (re)run the GPT baselines up to N rounds; only missing/unparsed answers are redone.
# Usage: nohup caffeinate -i sh scripts/run_codex_at.sh "YYYY-MM-DD HH:MM" ROUNDS > log 2>&1 &
cd "$(dirname "$0")/.." || exit 1
target=$(date -j -f "%Y-%m-%d %H:%M" "$1" +%s)
while [ "$(date +%s)" -lt "$target" ]; do sleep 60; done
echo "start $(date)"
.venv/bin/python scripts/07_baseline.py gpt-5.6-sol "$2" > data/baseline/log_gpt-5.6-sol_fill.txt 2>&1 &
.venv/bin/python scripts/07_baseline.py gpt-5.6-luna "$2" > data/baseline/log_gpt-5.6-luna_fill.txt 2>&1 &
.venv/bin/python scripts/07_baseline.py gpt-6-astra "$2" > data/baseline/log_gpt-6-astra_fill.txt 2>&1
wait
echo "done $(date)"
