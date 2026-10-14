"""Archived day-ahead Open-Meteo forecasts (previous-runs API, issued ~24 h before each
hour) for the two cold-start cameras, so the cold-start test can use the weather that was
actually forecast, as in the main ex-ante test (amil-scans/scripts/get_forecasts.py).

Downloads with curl (system certificate store), then writes
../data/weather/<node>_fcst_day1.csv  (timestamp = hour starting, Asia/Tokyo).
"""
import json
import subprocess
from pathlib import Path

import pandas as pd

WX = Path(__file__).resolve().parents[2] / "data" / "weather"
SITES = {"fukui_station": (36.062, 136.223), "tojinbo": (36.238, 136.125)}  # as in amil-scans

for node, (lat, lon) in SITES.items():
    raw = WX / f"{node}_fcst_day1.json"
    if not raw.exists():
        url = ("https://previous-runs-api.open-meteo.com/v1/forecast?"
               f"latitude={lat}&longitude={lon}&start_date=2025-11-01&end_date=2026-10-10"
               "&hourly=temperature_2m_previous_day1,precipitation_previous_day1&timezone=Asia%2FTokyo")
        subprocess.run(["curl", "-sS", "--fail", "--retry", "4", "-m", "180", "-o", str(raw), url], check=True)
    h = json.loads(raw.read_text())["hourly"]
    # Open-Meteo precipitation is the sum over the preceding hour; shift to hour starting like JMA.
    df = pd.DataFrame({"timestamp": pd.to_datetime(h["time"]) - pd.Timedelta(hours=1),
                       "fc_temp_c": h["temperature_2m_previous_day1"],
                       "fc_precip_1h_mm": h["precipitation_previous_day1"]})
    df.to_csv(WX / f"{node}_fcst_day1.csv", index=False)
    print(node, len(df), "rows,", df["timestamp"].min(), "to", df["timestamp"].max(),
          "null %", df.isna().mean().mul(100).round(1).to_dict())
