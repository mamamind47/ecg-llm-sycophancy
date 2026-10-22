# Hint experiment statistics, arm (b)

Responses scored: 458

## Wrong hints vs the no-hint control arm (n)

Control = the same baseline-correct cases re-asked without a hint (arm n). "Target" = the arm-(a) wrong target.

| Model | Sycophancy (= hinted target) | No hint: hit that target | Abandonment | No hint: abandonment |
|---|---|---|---|---|
| claude-opus-5-5 | 0.0% [0.0%, 3.4%] (0/108) | 5.6% [1.9%, 15.1%] (3/54) | 0.9% [0.2%, 5.1%] (1/108) | 7.4% [2.9%, 17.6%] (4/54) |
| claude-sonnet-5-5 | 5.8% [2.0%, 15.6%] (3/52) | 3.8% [0.7%, 18.9%] (1/26) | 21.2% [12.2%, 34.0%] (11/52) | 15.4% [6.2%, 33.5%] (4/26) |
| gemini-3.8-flash-high | 1.9% [0.3%, 9.8%] (1/54) | 11.1% [3.9%, 28.1%] (3/27) | 5.6% [1.9%, 15.1%] (3/54) | 7.4% [2.1%, 23.4%] (2/27) |
| gpt-5.6-luna | 0.0% [0.0%, 27.8%] (0/10) | 0.0% [0.0%, 43.4%] (0/5) | 70.0% [39.7%, 89.2%] (7/10) | 60.0% [23.1%, 88.2%] (3/5) |
| gpt-5.6-sol | 12.5% [4.3%, 31.0%] (3/24) | 16.7% [4.7%, 44.8%] (2/12) | 16.7% [6.7%, 35.9%] (4/24) | 0.0% [0.0%, 24.2%] (0/12) |
| gpt-6-astra | 0.0% [0.0%, 3.4%] (0/110) | 0.0% [0.0%, 6.5%] (0/55) | 2.7% [0.9%, 7.7%] (3/110) | 5.5% [1.9%, 14.9%] (3/55) |
| gpt-6.1-sol | 2.0% [0.6%, 7.0%] (2/100) | 0.0% [0.0%, 7.1%] (0/50) | 7.0% [3.4%, 13.7%] (7/100) | 2.0% [0.4%, 10.5%] (1/50) |

## Secondary drift estimate: held-out baseline run 3 (cases correct in runs 1-2)

| Model | Sycophancy (= hinted target) | Spontaneous hit of that target | Abandonment (no longer correct) | Spontaneous abandonment |
|---|---|---|---|---|
| claude-opus-5-5 | 0.0% [0.0%, 3.4%] (0/108) | 3.4% [1.0%, 11.7%] (2/58) | 0.9% [0.2%, 5.1%] (1/108) | 6.9% [2.7%, 16.4%] (4/58) |
| claude-sonnet-5-5 | 5.8% [2.0%, 15.6%] (3/52) | 3.4% [0.6%, 17.2%] (1/29) | 21.2% [12.2%, 34.0%] (11/52) | 10.3% [3.6%, 26.4%] (3/29) |
| gemini-3.8-flash-high | 1.9% [0.3%, 9.8%] (1/54) | 12.9% [5.1%, 28.9%] (4/31) | 5.6% [1.9%, 15.1%] (3/54) | 12.9% [5.1%, 28.9%] (4/31) |
| gpt-5.6-luna | 0.0% [0.0%, 27.8%] (0/10) | 0.0% [0.0%, 35.4%] (0/7) | 70.0% [39.7%, 89.2%] (7/10) | 28.6% [8.2%, 64.1%] (2/7) |
| gpt-5.6-sol | 12.5% [4.3%, 31.0%] (3/24) | 20.0% [7.0%, 45.2%] (3/15) | 16.7% [6.7%, 35.9%] (4/24) | 20.0% [7.0%, 45.2%] (3/15) |
| gpt-6-astra | 0.0% [0.0%, 3.4%] (0/110) | 0.0% [0.0%, 6.5%] (0/55) | 2.7% [0.9%, 7.7%] (3/110) | 0.0% [0.0%, 6.5%] (0/55) |
| gpt-6.1-sol | 2.0% [0.6%, 7.0%] (2/100) | 1.9% [0.3%, 9.8%] (1/54) | 7.0% [3.4%, 13.7%] (7/100) | 7.4% [2.9%, 17.6%] (4/54) |

## Sycophancy by hint style

| Model | lookalike-overconfidence |
|---|---|
| claude-opus-5-5 | 0.0% [0.0%, 3.4%] (0/108) |
| claude-sonnet-5-5 | 5.8% [2.0%, 15.6%] (3/52) |
| gemini-3.8-flash-high | 1.9% [0.3%, 9.8%] (1/54) |
| gpt-5.6-luna | 0.0% [0.0%, 27.8%] (0/10) |
| gpt-5.6-sol | 12.5% [4.3%, 31.0%] (3/24) |
| gpt-6-astra | 0.0% [0.0%, 3.4%] (0/110) |
| gpt-6.1-sol | 2.0% [0.6%, 7.0%] (2/100) |

## Thai vs English (paired, McNemar exact)

| Model | EN | TH | discordant EN-only / TH-only | p |
|---|---|---|---|---|
| claude-opus-5-5 | 0.0% [0.0%, 6.6%] (0/54) | 0.0% [0.0%, 6.6%] (0/54) | 0 / 0 | 1 |
| claude-sonnet-5-5 | 3.8% [0.7%, 18.9%] (1/26) | 7.7% [2.1%, 24.1%] (2/26) | 0 / 1 | 1 |
| gemini-3.8-flash-high | 3.7% [0.7%, 18.3%] (1/27) | 0.0% [0.0%, 12.5%] (0/27) | 1 / 0 | 1 |
| gpt-5.6-luna | 0.0% [0.0%, 43.4%] (0/5) | 0.0% [0.0%, 43.4%] (0/5) | 0 / 0 | 1 |
| gpt-5.6-sol | 8.3% [1.5%, 35.4%] (1/12) | 16.7% [4.7%, 44.8%] (2/12) | 1 / 2 | 1 |
| gpt-6-astra | 0.0% [0.0%, 6.5%] (0/55) | 0.0% [0.0%, 6.5%] (0/55) | 0 / 0 | 1 |
| gpt-6.1-sol | 0.0% [0.0%, 7.1%] (0/50) | 4.0% [1.1%, 13.5%] (2/50) | 0 / 2 | 0.5 |

## Pooled GEE logistic regression (exchangeable, clusters = model x case)

```
                                                                           OR     lo     hi      p
Intercept                                                        0.000000e+00    NaN    NaN    NaN
C(model, Treatment('claude-opus-5-5'))[T.claude-sonnet-5-5]      3.108193e+12    NaN    NaN    NaN
C(model, Treatment('claude-opus-5-5'))[T.gemini-3.8-flash-high]  8.829471e+11    NaN    NaN    NaN
C(model, Treatment('claude-opus-5-5'))[T.gpt-5.6-luna]           1.001000e+00    NaN    NaN    NaN
C(model, Treatment('claude-opus-5-5'))[T.gpt-5.6-sol]            7.323977e+12    NaN    NaN    NaN
C(model, Treatment('claude-opus-5-5'))[T.gpt-6-astra]            1.001000e+00    NaN    NaN    NaN
C(model, Treatment('claude-opus-5-5'))[T.gpt-6.1-sol]            1.067886e+12    NaN    NaN    NaN
C(lang, Treatment('en'))[T.th]                                   2.100000e+00  0.571  7.723  0.264
```