# Scan 02: weather sensitivity and staffing-forecast skill

Data: camera counts @ b89bc2c; weather from the Open-Meteo archive (daytime 09:00 to 17:00), chosen because it is global and so runs unchanged for Madinah. Outage days are excluded.

## A. Weather effect on daily counts

OLS on log counts with day-of-week, holiday and year-month fixed effects, HAC errors (lag 7). Effects are % change in the daily count.

| feed | n days | per 10 mm rain | per +5 m/s peak gust | per +3 h sun | per +5 °C | R² |
|---|---|---|---|---|---|---|
| Fukui Station (people) | 642 | -1.2% (±3.2) | +0.8% (±3.0) | +0.9% (±1.9) | +2.7% (±2.8) | 0.68 |
| Tojinbo (people) | 641 | -14.6% (±6.4) | -4.5% (±5.3) | +6.3% (±3.1) | +11.5% (±4.9) | 0.72 |
| Rainbow Line lot 1 (cars) | 607 | -36.9% (±14.2) | -3.4% (±5.8) | +10.9% (±6.6) | +16.1% (±9.3) | 0.63 |

± is an approximate 95% interval.

## B. Daily forecast skill, rolling origin (weekly refit, test 2025-10-13 to 2026-10-10)

Models: *naive* = same weekday last week; *calendar* = ridge on day-of-week, holiday, month and the latest available lags; *calendar + weather* adds the day's observed weather as a stand-in for a perfect forecast. *Within ±30%* is the share of days whose error is under 30%, close to the operator's '70% accuracy three days ahead'.

| feed | h | model | days | WAPE % | within ±30% |
|---|---|---|---|---|---|
| Fukui Station (people) | 1d | naive | 340 | 19.28 | 0.84 |
| Fukui Station (people) | 1d | calendar | 338 | 11.88 | 0.95 |
| Fukui Station (people) | 1d | calendar+weather | 338 | 12.20 | 0.94 |
| Fukui Station (people) | 3d | naive | 340 | 19.28 | 0.84 |
| Fukui Station (people) | 3d | calendar | 338 | 14.43 | 0.90 |
| Fukui Station (people) | 3d | calendar+weather | 338 | 14.75 | 0.90 |
| Tojinbo (people) | 1d | naive | 356 | 36.47 | 0.54 |
| Tojinbo (people) | 1d | calendar | 353 | 23.29 | 0.73 |
| Tojinbo (people) | 1d | calendar+weather | 353 | 21.52 | 0.75 |
| Tojinbo (people) | 3d | naive | 356 | 36.47 | 0.54 |
| Tojinbo (people) | 3d | calendar | 352 | 27.16 | 0.65 |
| Tojinbo (people) | 3d | calendar+weather | 352 | 25.34 | 0.68 |
| Rainbow Line lot 1 (cars) | 1d | naive | 301 | 41.78 | 0.44 |
| Rainbow Line lot 1 (cars) | 1d | calendar | 295 | 33.95 | 0.51 |
| Rainbow Line lot 1 (cars) | 1d | calendar+weather | 295 | 26.80 | 0.64 |
| Rainbow Line lot 1 (cars) | 3d | naive | 301 | 41.78 | 0.44 |
| Rainbow Line lot 1 (cars) | 3d | calendar | 296 | 38.50 | 0.40 |
| Rainbow Line lot 1 (cars) | 3d | calendar+weather | 296 | 31.28 | 0.54 |

## C. Busy-day warning three days ahead

A busy day is a day in the site's top 20% (training-period threshold). For Rainbow Line, also *lot 2 in use* (≥20 plates at the overflow lot), which is what triggers the shuttle and extra staff. Logistic regression on the same features, same rolling origin.

| trigger | features | test days | busy share | AUC | precision | recall |
|---|---|---|---|---|---|---|
| Fukui Station (people): top 20% day | calendar | 338 | 0.30 | 0.92 | 0.79 | 0.63 |
| Tojinbo (people): top 20% day | calendar | 352 | 0.30 | 0.91 | 0.82 | 0.64 |
| Rainbow Line lot 1 (cars): top 20% day | calendar | 296 | 0.40 | 0.81 | 0.78 | 0.45 |
| Rainbow Line: lot 2 in use | calendar | 297 | 0.23 | 0.87 | 0.60 | 0.55 |
| Fukui Station (people): top 20% day | calendar+weather | 338 | 0.30 | 0.91 | 0.77 | 0.58 |
| Tojinbo (people): top 20% day | calendar+weather | 352 | 0.30 | 0.93 | 0.86 | 0.62 |
| Rainbow Line lot 1 (cars): top 20% day | calendar+weather | 296 | 0.40 | 0.90 | 0.92 | 0.52 |
| Rainbow Line: lot 2 in use | calendar+weather | 297 | 0.23 | 0.91 | 0.84 | 0.61 |

## D. Counts outside opening hours (Rainbow Line road open about 08:00 to 18:00)

| feed | plates 19:00 to 07:00 | share of all |
|---|---|---|
| rl1 | 852.000 | 0.007 |
| rl2 | 51.000 | 0.004 |
