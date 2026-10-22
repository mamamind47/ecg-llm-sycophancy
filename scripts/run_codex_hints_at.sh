#!/bin/sh
# At a wall-clock time: finish GPT baselines, then hint arm (a) one run for each GPT model (cheapest first).
# Every step is resumable and stops itself on quota; rerun the same command later to fill gaps.
cd "$(dirname "$0")/.." || exit 1
target=$(date -j -f "%Y-%m-%d %H:%M" "$1" +%s)
while [ "$(date +%s)" -lt "$target" ]; do sleep 60; done
echo "start $(date)"
.venv/bin/python scripts/07_baseline.py gpt-6-astra 3 > data/baseline/log_gpt-6-astra_fill2.txt 2>&1
for m in gpt-5.6-luna gpt-5.6-sol gpt-6-astra; do
  n=$(grep -L '"parsed": null' data/baseline/$m/*_r3.json 2>/dev/null | wc -l | tr -d ' ')
  if [ "$n" != 101 ]; then echo "$m: baseline round 3 incomplete ($n/101), skipping hints"; continue; fi
  .venv/bin/python scripts/09_hints.py $m --arm a --runs 1 >> data/hints/log_$m.txt 2>&1
  echo "$m hints exit $? $(date)"
done
echo "done $(date)"
