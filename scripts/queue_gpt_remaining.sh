#!/bin/sh
# After astra arm (a) run 1 finishes: arm (b) for the three GPT models, then arm (a) runs 2-3 for the everyday GPTs.
# Decided 2026-10-19: flagship models (opus, astra) keep 1 run of arm (a); see README.
cd "$(dirname "$0")/.." || exit 1
while kill -0 "$1" 2>/dev/null; do sleep 60; done
W="sh scripts/run_until_done.sh"
for m in gpt-5.6-luna gpt-5.6-sol gpt-6-astra; do
  $W data/hints/log_$m.txt -- .venv/bin/python scripts/09_hints.py $m --arm b
done
for m in gpt-5.6-luna gpt-5.6-sol; do
  $W data/hints/log_$m.txt -- .venv/bin/python scripts/09_hints.py $m --arm a --runs 3
done
echo "queue done $(date)"
