# Pilot 2026-10-15: no-hint reads via agent CLIs

Case IDs refer to the **v1** pool (`data/cases/v1_2026-10-12/`), not the current v2 IDs.

One run per model and case, so the numbers are indicative only. Bold = matches the PTB-XL group. † = flagged by rule 0 (`label_flags.csv`).
These are agent CLIs (codex, agy, claude -p), not raw APIs. No model refused.

| Case | PTB-XL | gpt-6-astra | claude-opus-5-5 | gemini-3.8-flash-high | gpt-5.6-sol | claude-sonnet-5-5 |
|---|---|---|---|---|---|---|
| E001 | inferior_mi | **inferior MI (STEMI)** | anterior MI (STEMI) | anterior MI (STEMI) | other | normal |
| E002 | anterior_mi | LVH | LVH | **anterior MI (STEMI)** | LVH | LVH |
| E003 † | normal | LVH | LVH | anterior MI (STEMI) | LVH | LVH |
| E005 | rbbb | **RBBB** | **RBBB** | anterior MI (STEMI) | WPW | other |
| E009 | wpw | LVH | other | normal | LVH | normal |
| E011 † | afib | **atrial fibrillation** | normal | anterior MI (STEMI) | LVH | normal |
| E014 | lbbb | **LBBB** | **LBBB** | **LBBB** | WPW | LVH |
| E019 | first_deg_avb | **1st degree AV block** | normal | LVH | LVH | normal |
| **Match PTB-XL (8)** | | 5 | 2 | 2 | 0 | 0 |
| **Match, unflagged (6)** | | 4 | 2 | 2 | 0 | 0 |
| **Said STEMI** | | 1 | 1 | 5 | 0 | 0 |

Notes:
- Gemini via agy first returned empty output on 6/8 cases: it tried to run Python on the PNG and headless mode denied it. Rerun with a visual-inspection-only instruction.
- gpt-6.1-sol and gpt-6-sol are not available on the ChatGPT-account Codex login.
