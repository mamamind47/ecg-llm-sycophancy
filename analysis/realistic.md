# Arm r (realistic open-ended use)

Judged replies: 768

## Open-ended vs forced-choice (no remark)

| Model | Correct, open (r0) | Correct, forced choice (same cases) | LVH as conclusion, open | STEMI on non-acute, open |
|---|---|---|---|---|
| claude-opus-5-5 | 52% [42%–62%] (50/96) | 79% [68%–87%] (57/72) | 3% [1%–9%] (3/96) | 3% [1%–11%] (2/64) |
| claude-sonnet-5-5 | 42% [32%–52%] (40/96) | 46% [35%–57%] (33/72) | 14% [8%–22%] (13/96) | 0% [0%–6%] (0/64) |
| gemini-3.8-flash-high | 29% [21%–39%] (28/96) | 46% [35%–57%] (33/72) | 12% [7%–21%] (12/96) | 39% [28%–51%] (25/64) |
| gpt-6.1-sol | 50% [40%–60%] (48/96) | 64% [52%–74%] (46/72) | 8% [4%–16%] (8/96) | 5% [2%–13%] (3/64) |

## Does the remark pull the conclusion? (share landing on the remark's claim)

| Model | Lang | No remark (r0) | With remark (r1) | discordant r0-only / r1-only | McNemar p | Agrees with user (r1) |
|---|---|---|---|---|---|---|
| claude-opus-5-5 | th | 6% [2%–17%] (3/48) | 2% [0%–11%] (1/48) | 2 / 0 | 0.5 | 19% [10%–32%] (9/48) |
| claude-opus-5-5 | en | 4% [1%–14%] (2/48) | 4% [1%–14%] (2/48) | 1 / 1 | 1 | 17% [9%–30%] (8/48) |
| claude-sonnet-5-5 | th | 8% [3%–20%] (4/48) | 8% [3%–20%] (4/48) | 0 / 0 | 1 | 17% [9%–30%] (8/48) |
| claude-sonnet-5-5 | en | 6% [2%–17%] (3/48) | 6% [2%–17%] (3/48) | 1 / 1 | 1 | 12% [6%–25%] (6/48) |
| gemini-3.8-flash-high | th | 19% [10%–32%] (9/48) | 8% [3%–20%] (4/48) | 8 / 3 | 0.227 | 8% [3%–20%] (4/48) |
| gemini-3.8-flash-high | en | 21% [12%–34%] (10/48) | 6% [2%–17%] (3/48) | 9 / 2 | 0.0654 | 8% [3%–20%] (4/48) |
| gpt-6.1-sol | th | 4% [1%–14%] (2/48) | 4% [1%–14%] (2/48) | 2 / 2 | 1 | 12% [6%–25%] (6/48) |
| gpt-6.1-sol | en | 2% [0%–11%] (1/48) | 4% [1%–14%] (2/48) | 0 / 1 | 1 | 27% [17%–41%] (13/48) |

## Safety behaviour

| Model | Refers to clinician r0 → r1 | Hedges r0 → r1 |
|---|---|---|
| claude-opus-5-5 | 95% → 97% | 100% → 100% |
| claude-sonnet-5-5 | 94% → 83% | 100% → 100% |
| gemini-3.8-flash-high | 76% → 73% | 43% → 43% |
| gpt-6.1-sol | 100% → 100% | 100% → 100% |
