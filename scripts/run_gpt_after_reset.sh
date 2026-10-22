#!/bin/sh
# Wait for the Codex quota reset, then run the GPT baselines (round 1). Survives the Claude session closing.
# Usage: nohup caffeinate -i sh scripts/run_gpt_after_reset.sh "2026-10-18 05:50" > data/baseline/log_gpt_scheduled.txt 2>&1 &
cd "$(dirname "$0")/.." || exit 1
target=$(date -j -f "%Y-%m-%d %H:%M" "$1" +%s)
while [ "$(date +%s)" -lt "$target" ]; do sleep 60; done   # polls wall-clock, so a late wake-up still runs
echo "start $(date)"
.venv/bin/python scripts/07_baseline.py gpt-6-astra 1 > data/baseline/log_gpt-6-astra_resume.txt 2>&1 &
A=$!
.venv/bin/python scripts/07_baseline.py gpt-5.6-sol 1 > data/baseline/log_gpt-5.6-sol.txt 2>&1 &
S=$!
wait $A
ok=$(.venv/bin/python -c 'import sys; sys.path.insert(0,"scripts"); import llm_cli; print("yes" if llm_cli.parse(llm_cli.ask("gpt-5.6-luna","data/images/E002.png")) else "no")')
echo "gpt-5.6-luna available: $ok"
[ "$ok" = yes ] && .venv/bin/python scripts/07_baseline.py gpt-5.6-luna 1 > data/baseline/log_gpt-5.6-luna.txt 2>&1
wait $S
echo "done $(date)"
.venv/bin/python scripts/08_score_baseline.py 1
