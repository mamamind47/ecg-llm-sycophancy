#!/bin/sh
# Rerun a resumable step until it finishes cleanly, waiting out quota limits.
# The step must exit 0 when complete and non-zero when it stopped early (09_hints.py / 07_baseline.py do).
# Usage: nohup caffeinate -i sh scripts/run_until_done.sh LOG -- CMD ARGS... &
cd "$(dirname "$0")/.." || exit 1
log=$1; shift; [ "$1" = "--" ] && shift
for attempt in $(seq 1 40); do                     # 40 x 20 min = about 13 h of waiting at most
  echo "== attempt $attempt $(date)" >> "$log"
  "$@" >> "$log" 2>&1 && { echo "== complete $(date)" >> "$log"; exit 0; }
  sleep 1200
done
echo "== gave up $(date)" >> "$log"; exit 1
