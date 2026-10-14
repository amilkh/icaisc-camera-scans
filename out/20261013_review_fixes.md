# Review fixes (scan 05)

Test year 2025-10-13 to 2026-10-10, rolling origin with weekly refits; weather at test time is the archived Open-Meteo forecast issued h days before. *Lift* = precision ÷ base rate. *Brier (climatology)* is the score of always predicting the base rate; lower is better.

## A. Busy-day warnings under three definitions (3 days ahead)

| site | definition | weather | days | base rate | AUC | precision | recall | lift | Brier | Brier (climatology) |
|---|---|---|---|---|---|---|---|---|---|---|
| Fukui Station | rolling top 20% | none | 338 | 0.30 | 0.92 | 0.78 | 0.62 | 2.65 | 0.11 | 0.21 |
| Fukui Station | rolling top 20% | forecast | 338 | 0.30 | 0.92 | 0.81 | 0.59 | 2.73 | 0.11 | 0.21 |
| Fukui Station | fixed first-year top 20% | none | 338 | 0.31 | 0.93 | 0.85 | 0.63 | 2.75 | 0.10 | 0.21 |
| Fukui Station | fixed first-year top 20% | forecast | 338 | 0.31 | 0.93 | 0.87 | 0.62 | 2.82 | 0.11 | 0.21 |
| Fukui Station | same-month top 20% | none | 329 | 0.32 | 0.91 | 0.84 | 0.68 | 2.64 | 0.12 | 0.22 |
| Fukui Station | same-month top 20% | forecast | 329 | 0.32 | 0.89 | 0.80 | 0.63 | 2.55 | 0.12 | 0.22 |
| Tojinbo | rolling top 20% | none | 352 | 0.30 | 0.91 | 0.82 | 0.64 | 2.70 | 0.11 | 0.21 |
| Tojinbo | rolling top 20% | forecast | 352 | 0.30 | 0.93 | 0.85 | 0.64 | 2.80 | 0.10 | 0.21 |
| Tojinbo | fixed first-year top 20% | none | 352 | 0.33 | 0.91 | 0.88 | 0.74 | 2.64 | 0.10 | 0.22 |
| Tojinbo | fixed first-year top 20% | forecast | 352 | 0.33 | 0.93 | 0.91 | 0.68 | 2.73 | 0.09 | 0.22 |
| Tojinbo | same-month top 20% | none | 343 | 0.33 | 0.89 | 0.85 | 0.55 | 2.56 | 0.14 | 0.22 |
| Tojinbo | same-month top 20% | forecast | 343 | 0.33 | 0.90 | 0.90 | 0.61 | 2.70 | 0.12 | 0.22 |
| Rainbow Line lot 1 | rolling top 20% | none | 296 | 0.40 | 0.81 | 0.78 | 0.45 | 1.96 | 0.18 | 0.24 |
| Rainbow Line lot 1 | rolling top 20% | forecast | 296 | 0.40 | 0.87 | 0.84 | 0.57 | 2.10 | 0.15 | 0.24 |
| Rainbow Line lot 1 | fixed first-year top 20% | none | 296 | 0.50 | 0.78 | 0.79 | 0.58 | 1.57 | 0.20 | 0.25 |
| Rainbow Line lot 1 | fixed first-year top 20% | forecast | 296 | 0.50 | 0.87 | 0.88 | 0.66 | 1.74 | 0.16 | 0.25 |
| Rainbow Line lot 1 | same-month top 20% | none | 287 | 0.40 | 0.80 | 0.81 | 0.47 | 1.99 | 0.19 | 0.24 |
| Rainbow Line lot 1 | same-month top 20% | forecast | 287 | 0.40 | 0.82 | 0.92 | 0.50 | 2.28 | 0.17 | 0.24 |

## B. Car park 2 warning: label robustness (3 days ahead)

Ambiguous days (≥20 faces but <20 plates at gate 2): 51; on those days lot 1 median = 157 cars, against 341 on overflow days.

| label | weather | days | base rate | AUC | precision | recall | lift | Brier | Brier (climatology) |
|---|---|---|---|---|---|---|---|---|---|
| plates ≥20 (original) | none | 297 | 0.23 | 0.87 | 0.60 | 0.55 | 2.60 | 0.12 | 0.18 |
| plates ≥20 (original) | forecast | 297 | 0.23 | 0.89 | 0.80 | 0.58 | 3.44 | 0.10 | 0.18 |
| plates ≥20, ambiguous days removed | none | 286 | 0.24 | 0.89 | 0.66 | 0.62 | 2.74 | 0.11 | 0.18 |
| plates ≥20, ambiguous days removed | forecast | 286 | 0.24 | 0.90 | 0.79 | 0.65 | 3.27 | 0.10 | 0.18 |
| plates or faces ≥20 | none | 297 | 0.27 | 0.89 | 0.68 | 0.76 | 2.52 | 0.13 | 0.20 |
| plates or faces ≥20 | forecast | 297 | 0.27 | 0.88 | 0.74 | 0.65 | 2.76 | 0.12 | 0.20 |

## C. Classical baselines (WAPE %, within ±30% in brackets)

ETS: Holt-Winters on log counts, additive weekly seasonality, damped trend. SARIMAX(1,0,1)(1,0,1)7 on log counts with forecast weather as exogenous inputs. Both refit weekly on data up to the forecast origin; outage days are interpolated in training only.

| site | lead | days | naive | calendar | ridge + fcst wx | ETS | SARIMAX + fcst wx |
|---|---|---|---|---|---|---|---|
| Fukui Station | 1d | 338 | 19.3 (0.84) | 11.9 (0.95) | 12.0 (0.95) | 14.9 (0.90) | 16.7 (0.87) |
| Fukui Station | 3d | 338 | 19.3 (0.84) | 14.4 (0.90) | 14.6 (0.90) | 18.2 (0.85) | 18.1 (0.88) |
| Fukui Station | 7d | 340 | 19.3 (0.84) | 16.3 (0.89) | 16.2 (0.89) | 19.1 (0.81) | 18.3 (0.85) |
| Tojinbo | 1d | 353 | 36.2 (0.55) | 23.3 (0.73) | 21.6 (0.75) | 29.0 (0.62) | 28.1 (0.67) |
| Tojinbo | 3d | 352 | 36.3 (0.55) | 27.2 (0.65) | 26.0 (0.66) | 36.1 (0.61) | 27.6 (0.64) |
| Tojinbo | 7d | 356 | 36.5 (0.54) | 28.8 (0.63) | 26.7 (0.67) | 34.4 (0.53) | 31.8 (0.54) |
| Rainbow Line lot 1 | 1d | 295 | 41.5 (0.44) | 34.0 (0.51) | 27.6 (0.64) | 34.1 (0.53) | 32.2 (0.55) |
| Rainbow Line lot 1 | 3d | 296 | 41.7 (0.44) | 38.5 (0.40) | 32.1 (0.54) | 40.1 (0.44) | 38.2 (0.46) |
| Rainbow Line lot 1 | 7d | 299 | 41.4 (0.44) | 40.6 (0.37) | 37.3 (0.43) | 37.7 (0.48) | 40.2 (0.41) |

## D. Nested evaluation: tune on weeks 1 to 26, report on weeks 27 to 52

| site | lead | calendar | ridge + fcst wx (tuned) | GBM + fcst wx (tuned) | ridge alpha | DM p | DM p (Holm) |
|---|---|---|---|---|---|---|---|
| Fukui Station | 1d | 12.50 | 12.36 | 12.50 | 1.00 | 0.33 | 1.00 |
| Fukui Station | 3d | 16.17 | 16.20 | 17.38 | 0.10 | 0.88 | 1.00 |
| Fukui Station | 5d | 17.01 | 17.20 | 18.11 | 1.00 | 0.20 | 0.98 |
| Fukui Station | 7d | 17.76 | 18.17 | 19.11 | 10.00 | 0.61 | 1.00 |
| Tojinbo | 1d | 23.19 | 21.46 | 22.86 | 1.00 | 0.09 | 0.64 |
| Tojinbo | 3d | 28.78 | 26.87 | 25.15 | 1.00 | 0.07 | 0.59 |
| Tojinbo | 5d | 28.51 | 28.38 | 28.80 | 10.00 | 0.93 | 1.00 |
| Tojinbo | 7d | 28.30 | 26.19 | 26.58 | 10.00 | 0.12 | 0.70 |
| Rainbow Line lot 1 | 1d | 33.61 | 26.42 | 23.15 | 10.00 | 0.00 | 0.00 |
| Rainbow Line lot 1 | 3d | 39.15 | 30.23 | 28.72 | 10.00 | 0.00 | 0.00 |
| Rainbow Line lot 1 | 5d | 39.36 | 32.49 | 34.05 | 10.00 | 0.00 | 0.00 |
| Rainbow Line lot 1 | 7d | 40.40 | 36.26 | 37.45 | 1.00 | 0.03 | 0.30 |

Figures: out/figures/lead_time_wape.pdf
