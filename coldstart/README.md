# Cold start (Table VII, Fig. 4)

Code and outputs by Mohammed Sohail (Oct 2026). `cold_start.py` hides all counts before a
simulated installation date, trains on 3 to 365 days of hourly history, and forecasts the
next day's 24 hourly counts over ten 28-day windows (20 Dec 2025 to 25 Sep 2026) at Fukui
Station and Tojinbo.

Run from the repo root after `scripts/build_data.py`, `get_jma.py` and `get_forecasts.py`:

    python coldstart/cold_start.py

Inputs, shared with the scans: `data/5min_<site>_Person.parquet` (code4fukui counts at
b89bc2c), `data/jma_<site>.parquet` (JMA hourly observations, hour starting) and
`data/fcst7_<site>.parquet` (Open-Meteo previous-runs forecasts; the day-ahead
`previous_day1` columns are used for the ex-ante variant `blend_fcst`).

Shrinkage weight: w = min(n / 56, 1), where n is the number of days of history, so the
shrunk model equals ridge from 56 days on.

The peak threshold for the hourly peak F1 is fixed: the 90th percentile of daytime
(08:00 to 19:00) hours in calendar 2025. `cold_start_peak_f1.csv` gives the mean peak F1 per site,
model and history length; the best values (0.43 at Fukui Station, 0.63 at Tojinbo, both
gradient boosting) are the "about 0.4 and 0.6" in Section V-D.

Outage rule: cold start uses its own hourly rule. A day is excluded if its total is zero,
if fewer than 20 hours have counts, or if its total is under 15% of the trailing 28-day
median. This differs from the daily scans' rule (at least 80% of the 288 five-minute bins),
because the hourly models need whole days with a plausible level.

Outputs: `cold_start_results.csv` (per window and history length), `cold_start_peak_f1.csv`
(hourly peak F1), `cold_start_ci.csv`
(pooled WAPE and weekly block-bootstrap intervals for shrunk minus naive, for the
observed-weather, no-weather and forecast-weather variants), `cold_start.pdf/png`
(Fig. 4).

`get_cold_start_forecasts.py` is the earlier standalone forecast download used before the
script switched to `data/fcst7_<site>.parquet`; it is kept for reference only.
