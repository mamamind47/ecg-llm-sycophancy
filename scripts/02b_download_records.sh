#!/bin/sh
# Download the 500 Hz PTB-XL records listed in data/cases/candidates.csv (about 12 MB, slow server).
# Usage: sh scripts/02b_download_records.sh
B=https://physionet.org/files/ptb-xl/1.0.3
.venv/bin/python -c 'import pandas as pd; print("\n".join(pd.read_csv("data/cases/candidates.csv").filename_hr))' |
while read f; do for ext in hea dat; do echo "$B/$f.$ext data/ptbxl/$f.$ext"; done; done |
xargs -P 6 -n 2 sh -c 'mkdir -p "$(dirname "$1")"; [ -s "$1" ] || curl -sSf --retry 3 -o "$1" "$0"'
echo "$(find data/ptbxl/records500 -name '*.dat' -size 120000c | wc -l) complete records"
