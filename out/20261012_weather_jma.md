# Scan 02: weather sensitivity and staffing-forecast skill

Data: camera counts @ b89bc2c; weather from JMA station observations (Fukui City, Mikuni AMeDAS, Mihama AMeDAS; peak wind is the highest hourly mean), daytime 09:00 to 17:00. Outage days are excluded.

## A. Weather effect on daily counts

OLS on log counts with day-of-week, holiday and year-month fixed effects, HAC errors (lag 7). Effects are % change in the daily count.

| feed | n days | per 10 mm rain | per +5 m/s peak wind | per +3 h sun | per +5 °C | R² |
|---|---|---|---|---|---|---|
| Fukui Station (people) | 642 | -3.2% (±2.6) | +3.2% (±5.3) | -0.4% (±1.6) | +2.4% (±2.7) | 0.68 |
| Tojinbo (people) | 639 | -8.9% (±4.5) | -9.9% (±7.4) | +5.2% (±3.0) | +13.1% (±4.4) | 0.72 |
| Rainbow Line lot 1 (cars) | 605 | -39.5% (±20.3) | -10.5% (±15.9) | +17.7% (±4.9) | +9.2% (±7.9) | 0.63 |

± is an approximate 95% interval.

## B. Daily forecast skill, rolling origin (weekly refit, test 2025-10-13 to 2026-10-10)

Models: *naive* = same weekday last week; *calendar* = ridge on day-of-week, holiday, month and the latest available lags; *calendar + weather* adds the day's observed weather as a stand-in for a perfect forecast. *Within ±30%* is the share of days whose error is under 30%, close to the operator's '70% accuracy three days ahead'.

| feed | h | model | days | WAPE % | within ±30% |
|---|---|---|---|---|---|
| Fukui Station (people) | 1d | naive | 340 | 19.28 | 0.84 |
| Fukui Station (people) | 1d | calendar | 338 | 11.88 | 0.95 |
| Fukui Station (people) | 1d | calendar+weather | 338 | 12.11 | 0.93 |
| Fukui Station (people) | 3d | naive | 340 | 19.28 | 0.84 |
| Fukui Station (people) | 3d | calendar | 338 | 14.43 | 0.90 |
| Fukui Station (people) | 3d | calendar+weather | 338 | 14.78 | 0.90 |
| Tojinbo (people) | 1d | naive | 356 | 36.47 | 0.54 |
| Tojinbo (people) | 1d | calendar | 353 | 23.29 | 0.73 |
| Tojinbo (people) | 1d | calendar+weather | 353 | 21.27 | 0.76 |
| Tojinbo (people) | 3d | naive | 356 | 36.47 | 0.54 |
| Tojinbo (people) | 3d | calendar | 352 | 27.16 | 0.65 |
| Tojinbo (people) | 3d | calendar+weather | 351 | 25.40 | 0.70 |
| Rainbow Line lot 1 (cars) | 1d | naive | 301 | 41.78 | 0.44 |
| Rainbow Line lot 1 (cars) | 1d | calendar | 295 | 33.95 | 0.51 |
| Rainbow Line lot 1 (cars) | 1d | calendar+weather | 294 | 29.18 | 0.61 |
| Rainbow Line lot 1 (cars) | 3d | naive | 301 | 41.78 | 0.44 |
| Rainbow Line lot 1 (cars) | 3d | calendar | 296 | 38.50 | 0.40 |
| Rainbow Line lot 1 (cars) | 3d | calendar+weather | 295 | 33.87 | 0.53 |

## C. Busy-day warning three days ahead

A busy day is a day in the site's top 20% (training-period threshold). For Rainbow Line, also *lot 2 in use* (≥20 plates at the overflow lot), which is what triggers the shuttle and extra staff. Logistic regression on the same features, same rolling origin.

| trigger | features | test days | busy share | AUC | precision | recall |
|---|---|---|---|---|---|---|
| Fukui Station (people): top 20% day | calendar | 338 | 0.30 | 0.92 | 0.79 | 0.63 |
| Tojinbo (people): top 20% day | calendar | 352 | 0.30 | 0.91 | 0.82 | 0.64 |
| Rainbow Line lot 1 (cars): top 20% day | calendar | 296 | 0.40 | 0.81 | 0.78 | 0.45 |
| Rainbow Line: lot 2 in use | calendar | 297 | 0.23 | 0.87 | 0.60 | 0.55 |
| Fukui Station (people): top 20% day | calendar+weather | 338 | 0.30 | 0.91 | 0.79 | 0.57 |
| Tojinbo (people): top 20% day | calendar+weather | 351 | 0.30 | 0.93 | 0.87 | 0.64 |
| Rainbow Line lot 1 (cars): top 20% day | calendar+weather | 295 | 0.40 | 0.88 | 0.88 | 0.54 |
| Rainbow Line: lot 2 in use | calendar+weather | 296 | 0.23 | 0.89 | 0.86 | 0.64 |

## D. Counts outside opening hours (Rainbow Line road open about 08:00 to 18:00)

| feed | plates 19:00 to 07:00 | share of all |
|---|---|---|
| rl1 | 852.000 | 0.007 |
| rl2 | 51.000 | 0.004 |
