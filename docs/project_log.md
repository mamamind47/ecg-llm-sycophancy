# ECG sycophancy: do multimodal LLMs follow a clinician's wrong hint? (started 2026-10-07)

Question: when a multimodal LLM reads a 12-lead ECG image correctly on its own, how often does it switch
to a wrong diagnosis after a clinician-style hint ("I think this is normal")? This matters most for
STEMI/OMI cases.

Team: Badeesorn (KMUTT). A faculty advisor is still needed.
Data plan: public ECGs only (PTB-XL). **Since 2026-10-18 the PTB-XL labels are the reference standard and no new human labels are collected**
(no clinician available to adjudicate). Acute vs old MI comes from PTB-XL `infarction_stadium`. No IRB needed.

## Status
- [x] Novelty scan (web 2026-10-07/08, Scopus 2026-10-09). No paper found that tests misleading hints on ECG images.
      See `related_work.md`.
- [x] Candidate pool v2 (2026-10-18): 96 clean PTB-XL ECGs across 8 groups, rendered as 12-lead paper images.
  v1 (2026-10-12) is archived in `data/cases/v1_2026-10-12/`. It was replaced before review began, because the
  2026-10-15 pilot showed ambiguous secondary labels (47 of 96 ECGs are in both versions).
- [x] v3 case set (2026-10-18): 101 cases, adding acute-stage MI (25) and old MI (10) by PTB-XL stage. Clinician review dropped;
  v1/v2 and the unused review package are archived in `data/cases/v1_2026-10-12/` and `data/cases/v2_2026-10-18/`.
- [x] Baseline round 1 done 2026-10-18 06:15 (606/606 parsed). Summary in Thai: `data/baseline/SUMMARY_TH.md`.
  Opus 62%, astra 56%, Gemini 43% (32/76 false STEMI), Sonnet 38%, 5.6-sol 31%, 5.6-luna 14%; all models over-call LVH.
- [ ] Baseline: `scripts/07_baseline.py MODEL RUNS` via agent CLIs, a flagship and an everyday model per vendor:
  gpt-6-astra + gpt-5.6-sol (+ gpt-5.6-luna if the ChatGPT login allows it), claude-opus-5-5 + claude-sonnet-5-5, gemini-3.8-flash-high.
  Score with `scripts/08_score_baseline.py RUN`. Codex quota ran out on 2026-10-18 at 01:2x; the GPT runs resume after 05:48.
  (`scripts/llm_cli.py`). Round 1 started 2026-10-18. Opus shares the user's Claude quota, so rounds are added one at a time.
- [ ] Hint arms on baseline-correct cases (decided 2026-10-18, before any hint run):
  - **(n) no-hint control (added 2026-10-19):** the same baseline-correct cases re-asked without a hint, 1 run per model,
    as the drift comparator for sycophancy/abandonment (`09_hints.py MODEL --arm n`; stats in `scripts/12_stats.py`).
  - **Runs actually used (amended 2026-10-19 for quota):** arm (a) 3 runs for gemini, sonnet, gpt-5.6-sol, gpt-5.6-luna;
    1 run for the flagships opus and astra. Their round-1 sycophancy was <=4%, where extra runs barely narrow the CI
    (opus 2/108, Wilson 95% about 0.5-6.5%). Arm (b) for all six. Runner: `scripts/run_until_done.sh` retries through quota limits.
  - **(a) primary, full design:** 3 wrong styles (overconfidence, recency, consensus) + 1 correct hint × Thai/English × 3 runs.
    Wrong target {X}: abnormal groups (afib, lbbb, rbbb, wpw, 1AVB, acute MI) → "normal ECG";
    normal and old MI → "acute MI (STEMI)". Measures both talking a model out of a finding and into a false STEMI.
  - **(b) secondary, light:** overconfidence style only × Thai/English × 1 run. {X} = the most frequent wrong
    baseline diagnosis for that group, pooled over all models, excluding "other" (ties broken alphabetically).
    Computed once from round-1 baseline and frozen in `data/hints/lookalike_map.json` before any hint run.
    RESULT: the rule gave "lvh" for every group (driven by gpt-5.6-luna; kept as `lookalike_map_v1_all_lvh.json`).
    AMENDED 2026-10-18 09:45, before any hint run: also exclude "lvh". New map: acute_mi/afib/1AVB/old_mi/wpw -> normal,
    lbbb/normal -> anterior MI, rbbb -> 1st degree AV block. 5 of 8 groups coincide with arm (a)'s "normal" target.
    Arm (b) runs after arm (a).
- [ ] Baseline rounds 2-3 (started 2026-10-18 09:45; astra from ~10:50 after the Codex reset). Then baseline-correct =
  correct in all 3 rounds (changed from 4/5 to save quota; decided before rounds 2-3 were seen).
  - Scripts: `scripts/09_hints.py MODEL --arm a|b`, map: `scripts/10_lookalike_map.py`. Only a test run so far (Sonnet, E006, 8 calls).
- [x] Paper draft v0.1 (2026-10-13): `paper/manuscript_draft.md` + `paper/references.bib`. Intro, related work and methods are written; results are [TBD].
  LaTeX: `paper/manuscript/` (elsarticle, XeLaTeX via tectonic, Thai font bundled). Run `python3 prepare.py && tectonic -X compile main.tex`; the markdown draft stays the source of truth. PDF copy for sharing: `share/ECG_sycophancy_paper_draft_v0.1.pdf`.
- [ ] **GPT-6 everyday models (2026-10-19):** Codex CLI 0.153.4 refused gpt-6.1-sol / gpt-6-sol / gpt-6-luna ("not supported with a
  ChatGPT account"), although the Codex app (client 0.162) listed them. After `codex update` to 0.163.0 the refusal became an ordinary
  quota message, so they look usable. The model list describes gpt-6-sol as "previous generation" and gpt-5.6-sol as "older generation",
  so the 5.6 models are two generations old. Queue `scripts/queue_codex_v2.sh` (from 2026-10-20 01:03): baseline 6.1-sol + 6-luna
  -> arm n for all GPT -> arm a for the new models -> arm b for all GPT -> 5.6 arm-a runs 2-3 last. Record the CLI version split in Methods.
- [x] **gpt-6-luna DONE 2026-10-19 22:48-23:29 on the second account** (Windows 11, Codex 0.162.0-alpha.17.2, 303/303 parsed;
  imported to `data/baseline/gpt-6-luna`, meta in `gpt-6-luna_run_meta.json`). Accuracy 1-5%, answering "other"/LVH about 95% of the time;
  0 cases correct 3/3, so arms n/a/b had no eligible cases. Old note: **gpt-6-luna on a second ChatGPT account (2026-10-19):** kit `share/luna_kit/ECG_luna_runner.zip` (Windows .bat; Codex >= 0.163;
  baseline x3 -> arm n -> arm a x3 -> arm b). Returns `luna_results.zip`: unzip into the repo root (it holds `data/baseline/gpt-6-luna`,
  `data/hints/*/gpt-6-luna`, `data/run_meta.json`). Report in Methods that this model's data came from a different account.
- [ ] **Realistic-use arm r (2026-10-19):** design `docs/realistic_substudy.md` (frozen); 24 cases `data/hints/r_cases.csv`;
  `scripts/15_realistic.py MODEL` (open-ended TH/EN, no answer list) -> `16_judge.py MODEL` (cross-vendor LLM judge, text only).
  Running for gemini, sonnet, opus (576 replies + 576 judgements). Then hand-label 20% for judge kappa.
- [ ] Re-scan arXiv/medRxiv before submission. Scopus lags preprints by months.

## Case inclusion rule (fixed 2026-10-12, before seeing any review)
The reviewer only reads the ECGs. We apply this rule to the returned sheet. A case is kept only if ALL of these hold:
1. image quality = yes
2. reviewer confidence ≥ 4
3. the reviewer's diagnosis agrees with the PTB-XL group (two independent sources)
4. MI cases: the reviewer's "ST elevation meets STEMI criteria" answer sets STEMI vs non-STEMI. MI cases are kept either way,
   but only STEMI = yes cases enter the STEMI analysis.
Cases that fail stay in the data, marked as excluded, and we report counts per reason.

## Pipeline
1. `scripts/01_scopus_scan.py`: literature scan (see below).
2. `scripts/02_select_cases.py`: candidate pool from PTB-XL v1.0.3. Folds 9-10 (human-validated), no noise or
   electrode flags, one target finding with no competing major finding, no ambiguous secondary statement (LVH voltage,
   IVCD outside LBBB, ischaemia/injury outside MI groups, "probable/possible" AF), seed 20261012.
   Groups (eligible pool → sampled): normal 1069→20, afib 32→10, lbbb 50→10, rbbb 16→10, wpw 13→8,
   first_deg_avb 16→8, anterior_mi 51→15, inferior_mi 53→15.
   Writes `data/cases/candidates.csv` (answer key) and `data/cases/review_sheet.csv` (blinded).
   Case IDs E001–E096 are shuffled, so neither filename nor order reveals the group.
3. `scripts/03_render_images.py`: 500 Hz record → 3×4 + lead-II rhythm strip, 25 mm/s, 10 mm/mV,
   200 dpi PNG in `data/images/`. No text other than lead names and scale.

   `scripts/06_label_flags.py` re-checks the pool for those labels (v2: 0 flagged).
4. `scripts/04_make_review_workbook.py`: blinded review package `share/ECG_review.zip` (Excel naming each image file, no hyperlinks; images; no answer key)
   for the clinician. Return the filled `ECG_review.xlsx` to `data/cases/`.

5. Analysis: `scripts/08_score_baseline.py` (baseline scoring), `11_analyze_hints.py` (hint scoring),
   `12_stats.py ARM` (Wilson CIs, arm-n control, McNemar TH/EN, pooled GEE -> `analysis/stats_<arm>.md`),
   `13_baseline_tables.py` (Tables 3-4 -> `analysis/baseline_tables.md`), `14_figures.py` (exports figure numbers/CSVs;
   the figures are drawn by TikZ/pgfplots in `paper/manuscript/figures/fig1_flow.tex` and `fig2_sycophancy.tex`).
   After new data: `12_stats.py a && 13_baseline_tables.py && 14_figures.py`, then rebuild the PDF.

Setup: `python3 -m venv .venv && .venv/bin/pip install wfdb pandas matplotlib`.
Raw records: `sh scripts/02b_download_records.sh` → `data/ptbxl/records500/` (git-ignored), from
`https://physionet.org/files/ptb-xl/1.0.3/<filename_hr>.{hea,dat}`.

Known limitation: PTB-XL MI labels do not separate acute from old MI, so STEMI status comes from the clinician review.

## Layout
- `scripts/01_scopus_scan.py`: the 4 Scopus queries (the query strings live in the script).
  The key is read from `~/.config/scopus/key`.
  Run: `SSL_CERT_FILE=/etc/ssl/cert.pem python3 scripts/01_scopus_scan.py data/scopus_YYYY-MM-DD`
- `data/scopus_2026-10-09/`: raw results (title, first author, source, date, DOI, citations).

| file | query | hits |
|---|---|---|
| `q1_ecg_sycophancy.csv` | ECG AND sycophan* | 0 |
| `q2_ecg_llm_misleading.csv` | ECG AND LLM AND (mislead*/anchor*/bias/persua*/adversarial/clinical context...) | 26 |
| `q3_medical_vlm_sycophancy.csv` | sycophan* AND medical AND (image/vision/multimodal) | 6 |
| `q4_ecg_llm_census.csv` | ECG AND LLM, 2023 onward | 476 |

## Target venues
medRxiv preprint first. Then AI in Medicine, then J Electrocardiology, then Int J Med Inform.
Report following TRIPOD-LLM.
