# Scan 10: warning cut-offs as staffing operating points (three days ahead, forecast weather)

Same models and test year as Tables V and VI. Cut-off = predicted probability at or above which a warning is issued. Call-outs = warnings per 30 test days; missed = busy days with no warning.

## Rainbow Line: overflow lot 2 in use (>= 20 plates)

297 test days, 69 busy (23%).

| cut-off | flagged | precision | recall | missed busy days | call-outs per 30 days |
|---|---|---|---|---|---|
| 0.3 | 75 | 0.69 | 0.75 | 17 | 7.6 |
| 0.4 | 66 | 0.74 | 0.71 | 20 | 6.7 |
| 0.5 | 50 | 0.80 | 0.58 | 29 | 5.1 |
| 0.6 | 41 | 0.83 | 0.49 | 35 | 4.1 |
| 0.7 | 32 | 0.81 | 0.38 | 43 | 3.2 |

## Fukui Station: top-20% day

338 test days, 100 busy (30%).

| cut-off | flagged | precision | recall | missed busy days | call-outs per 30 days |
|---|---|---|---|---|---|
| 0.3 | 111 | 0.74 | 0.82 | 18 | 9.9 |
| 0.4 | 91 | 0.77 | 0.70 | 30 | 8.1 |
| 0.5 | 73 | 0.81 | 0.59 | 41 | 6.5 |
| 0.6 | 46 | 0.85 | 0.39 | 61 | 4.1 |
| 0.7 | 31 | 0.84 | 0.26 | 74 | 2.8 |

## Tojinbo: top-20% day

352 test days, 107 busy (30%).

| cut-off | flagged | precision | recall | missed busy days | call-outs per 30 days |
|---|---|---|---|---|---|
| 0.3 | 104 | 0.85 | 0.82 | 19 | 8.9 |
| 0.4 | 93 | 0.87 | 0.76 | 26 | 7.9 |
| 0.5 | 80 | 0.85 | 0.64 | 39 | 6.8 |
| 0.6 | 64 | 0.88 | 0.52 | 51 | 5.5 |
| 0.7 | 42 | 0.90 | 0.36 | 69 | 3.6 |

## Rainbow Line lot 1: top-20% day

296 test days, 118 busy (40%).

| cut-off | flagged | precision | recall | missed busy days | call-outs per 30 days |
|---|---|---|---|---|---|
| 0.3 | 116 | 0.72 | 0.71 | 34 | 11.8 |
| 0.4 | 94 | 0.79 | 0.63 | 44 | 9.5 |
| 0.5 | 80 | 0.84 | 0.57 | 51 | 8.1 |
| 0.6 | 62 | 0.89 | 0.47 | 63 | 6.3 |
| 0.7 | 46 | 0.93 | 0.36 | 75 | 4.7 |

