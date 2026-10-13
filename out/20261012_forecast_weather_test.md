# Scan 03: ex-ante forecasts with archived weather forecasts

Training uses observed weather; test predictions use the Open-Meteo forecast issued h days before (previous-runs API). Rolling origin, weekly refit, test 2025-10-13 to 2026-10-10. DM = Diebold-Mariano test on absolute errors, forecast-weather model against calendar only (negative t means weather helps). CI = 95% weekly block bootstrap of the WAPE change.

## A. Daily count forecasts

| site | h | days | WAPE calendar | WAPE +forecast wx | WAPE +observed wx | change (pts) [95% CI] | DM t (p) | within ±30%, forecast wx |
|---|---|---|---|---|---|---|---|---|
| Fukui Station | 1d | 338 | 11.88 | 12.13 | 12.17 | +0.3 [-0.0, +0.6] | +1.64 (0.101) | 0.95 |
| Fukui Station | 3d | 338 | 14.43 | 14.70 | 14.77 | +0.3 [-0.0, +0.6] | +1.77 (0.076) | 0.90 |
| Tojinbo | 1d | 353 | 23.29 | 21.53 | 21.56 | -1.8 [-3.3, -0.4] | -2.43 (0.015) | 0.75 |
| Tojinbo | 3d | 352 | 27.16 | 26.18 | 25.56 | -1.0 [-2.9, +0.8] | -1.08 (0.279) | 0.66 |
| Rainbow Line lot 1 | 1d | 295 | 33.95 | 27.65 | 27.05 | -6.3 [-9.0, -3.5] | -4.81 (0.000) | 0.62 |
| Rainbow Line lot 1 | 3d | 296 | 38.50 | 32.59 | 32.06 | -5.9 [-8.9, -3.0] | -4.00 (0.000) | 0.50 |

## B. Busy-day warnings three days ahead, with the forecast available at the time

| warning | weather | days | AUC [95% CI] | precision | recall |
|---|---|---|---|---|---|
| Fukui Station: top-20% day | none | 338 | 0.92 [0.89, 0.95] | 0.79 | 0.63 |
| Fukui Station: top-20% day | 3-day forecast | 338 | 0.91 [0.88, 0.95] | 0.79 | 0.56 |
| Tojinbo: top-20% day | none | 352 | 0.91 [0.87, 0.94] | 0.82 | 0.64 |
| Tojinbo: top-20% day | 3-day forecast | 352 | 0.93 [0.89, 0.96] | 0.86 | 0.64 |
| Rainbow Line: top-20% day | none | 296 | 0.81 [0.77, 0.86] | 0.78 | 0.45 |
| Rainbow Line: top-20% day | 3-day forecast | 296 | 0.86 [0.82, 0.90] | 0.82 | 0.54 |
| Rainbow Line: car park 2 in use | none | 297 | 0.87 [0.82, 0.92] | 0.60 | 0.55 |
| Rainbow Line: car park 2 in use | 3-day forecast | 297 | 0.88 [0.82, 0.93] | 0.80 | 0.54 |
