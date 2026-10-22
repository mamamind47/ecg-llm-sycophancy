# Do multimodal language models defer to a clinician's wrong ECG read?

Code, prompts and data for a controlled study of sycophancy in 12-lead ECG interpretation by multimodal large
language models (MLLMs). Eight models read 101 PTB-XL ECGs rendered as paper images; cases each model read correctly
were re-presented with a clinician-style wrong or correct hint, in Thai and English. A sub-study asked open-ended
questions with casual remarks, and a small spot-check covered consumer web chat apps.

Author: Badeesorn Sittikong, School of Information Technology, King Mongkut's University of Technology Thonburi.
Manuscript: `paper/manuscript_draft.md` (source) and `paper/supplementary.md`; LaTeX build in `paper/manuscript/`.

## Layout

| Path | Contents |
|---|---|
| `scripts/02_select_cases.py`, `02b_download_records.sh` | Case selection from PTB-XL (seed 20261012) and record download |
| `scripts/03_render_images.py` | Paper-ECG rendering (25 mm/s, 10 mm/mV, 200 dpi) |
| `scripts/07_baseline.py`, `08_score_baseline.py` | Baseline reads (3 runs) and scoring against PTB-XL groups |
| `scripts/09_hints.py`, `10_lookalike_map.py`, `11_analyze_hints.py`, `12_stats.py` | Hint arms a/b/n and statistics (Wilson CIs, McNemar, GEE) |
| `scripts/15_realistic.py`, `16_judge.py`, `17_analyze_realistic.py` | Open-ended arm r and cross-vendor LLM judge |
| `scripts/18_voltage.py` | Median-beat Sokolow-Lyon voltage |
| `scripts/19_label_workbook.py`, `20_label_agreement.py` | Hand-label sample and judge agreement (kappa) |
| `scripts/web_save.py` | Saves web-app spot-check replies |
| `scripts/llm_cli.py` | Calls to Codex CLI, Claude Code and Antigravity (fresh temp dir per call, image only) |
| `data/cases/candidates.csv` | The 101 cases with PTB-XL ids and groups |
| `data/images/` | Rendered ECG images E001-E101 |
| `data/baseline/`, `data/hints/{a,b,n,r,r_judged,web}/` | Raw model responses and judge verdicts |
| `analysis/` | Tables and statistics used in the paper |
| `docs/realistic_substudy.md` | Frozen design of the open-ended arm |

## Reproduce

1. Download PTB-XL v1.0.3 into `data/ptbxl/` (see `scripts/02b_download_records.sh`).
2. `python3 scripts/03_render_images.py` to re-render images (already included).
3. Model calls need the vendors' command-line agents and accounts; responses are included, so analyses can be rerun
   without them: `python3 scripts/12_stats.py a`, `scripts/13_baseline_tables.py`, `scripts/17_analyze_realistic.py`.

## Licence

Code MIT; data CC BY 4.0 (derived from PTB-XL, CC BY 4.0). See `LICENSE`.
