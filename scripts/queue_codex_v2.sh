#!/bin/sh
# Codex queue after the CLI update (2026-10-19): newest everyday models first, 5.6 extra runs last.
# gpt-6-luna is run separately on a second account (share/luna_kit), so it is not in this queue.
# Every step retries through quota limits (run_until_done.sh) and resumes where it stopped.
cd "$(dirname "$0")/.." || exit 1
W="sh scripts/run_until_done.sh"
# 1. wait until gpt-6.1-sol answers at all (quota reset 2026-10-20 01:03)
until .venv/bin/python -c 'import sys; sys.path.insert(0,"scripts"); import llm_cli; sys.exit(0 if llm_cli.parse(llm_cli.ask("gpt-6.1-sol","data/images/E002.png")) else 1)'; do sleep 1200; done
echo "gpt-6.1-sol available $(date)"
# 2. baselines for the new everyday models
for m in gpt-6.1-sol; do $W data/baseline/log_$m.txt -- .venv/bin/python scripts/07_baseline.py $m 3; done
# 3. no-hint control for every GPT model (cheap; astra waits for its arm-a run in the other wrapper only for comparability)
for m in gpt-6.1-sol gpt-5.6-luna gpt-5.6-sol gpt-6-astra; do $W data/hints/log_n_$m.txt -- .venv/bin/python scripts/09_hints.py $m --arm n; done
# 4. arm (a), 3 runs, for the new everyday models
for m in gpt-6.1-sol; do $W data/hints/log_$m.txt -- .venv/bin/python scripts/09_hints.py $m --arm a --runs 3; done
# 5. arm (b) for every GPT model
for m in gpt-6.1-sol gpt-5.6-luna gpt-5.6-sol gpt-6-astra; do $W data/hints/log_$m.txt -- .venv/bin/python scripts/09_hints.py $m --arm b; done
# 6. lowest priority: arm (a) runs 2-3 for the older 5.6 models
for m in gpt-5.6-luna gpt-5.6-sol; do $W data/hints/log_$m.txt -- .venv/bin/python scripts/09_hints.py $m --arm a --runs 3; done
echo "queue v2 done $(date)"
