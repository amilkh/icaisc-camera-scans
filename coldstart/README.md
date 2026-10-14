# Cold start (Table VII, Fig. 4)

Code and outputs by Mohammed Sohail (Oct 2026), copied unchanged from the paper
repository. `cold_start.py` hides all counts before a simulated installation date,
trains on 3 to 365 days of hourly history, and forecasts the next day's 24 hourly
counts over ten 28-day windows (20 Dec 2025 to 25 Sep 2026) at Fukui Station and
Tojinbo. Inputs: the raw code4fukui hourly files at commit b89bc2c and JMA hourly
weather (`../data/weather/<node>_hourly.csv`, timestamp = hour starting);
`get_cold_start_forecasts.py` fetches the archived day-ahead Open-Meteo forecast for
the ex-ante variant.

Shrinkage weight: w = min(h / 1344, 1), where h is the number of observed training
hours (56 days x 24). With outage hours removed, w stays slightly below 1 at 56
nominal days, which is why `blend` and `ridge` differ slightly in that row of
`cold_start_ci.csv`.

Outputs: `cold_start_results.csv` (per window and history length),
`cold_start_ci.csv` (pooled WAPE and weekly block-bootstrap intervals for
shrunk minus naive), `cold_start.pdf/png` (Fig. 4).
