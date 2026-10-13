"""Archived Open-Meteo forecasts issued 1 to 7 days before each hour
(previous-runs API), for an honest ex-ante test of the weather models."""
import json, time, urllib.request
import pandas as pd
from common import DATA
from get_weather import SITES

BASE = ["precipitation", "temperature_2m", "wind_gusts_10m", "sunshine_duration"]
for k, (lat, lon) in SITES.items():
    out = DATA / f"fcst7_{k}.parquet"
    if out.exists():
        continue
    hourly = ",".join(f"{v}_previous_day{d}" for v in BASE for d in range(1, 8))
    url = ("https://previous-runs-api.open-meteo.com/v1/forecast?"
           f"latitude={lat}&longitude={lon}&start_date=2025-09-01&end_date=2026-10-10"
           f"&hourly={hourly}&timezone=Asia%2FTokyo&wind_speed_unit=ms")
    for attempt in range(5):
        try:
            h = json.load(urllib.request.urlopen(url, timeout=180))["hourly"]; break
        except Exception as e:
            print(k, "retry", attempt, e); time.sleep(20 * (attempt + 1))
    df = pd.DataFrame(h).rename(columns={"time": "t0"}); df["t0"] = pd.to_datetime(df["t0"])
    df.to_parquet(out, index=False)
    print(k, len(df), "null %", (df.drop(columns="t0").isna().mean() * 100).round(1).to_dict())
