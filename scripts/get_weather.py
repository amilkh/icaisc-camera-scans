"""Hourly weather per site from the Open-Meteo archive (global, no key), so the
same pipeline runs unchanged for Madinah."""
import json, time, urllib.request
import pandas as pd
from common import DATA

SITES = {  # approximate camera locations
    "station": (36.062, 136.223),
    "tojinbo": (36.238, 136.125),
    "rainbow": (35.597, 135.885),
}
VARS = "temperature_2m,precipitation,snowfall,wind_speed_10m,wind_gusts_10m,sunshine_duration,cloud_cover"

def main():
  for k, (lat, lon) in SITES.items():
      url = ("https://archive-api.open-meteo.com/v1/archive?"
             f"latitude={lat}&longitude={lon}&start_date=2024-12-20&end_date=2026-10-10"
             f"&hourly={VARS}&timezone=Asia%2FTokyo&wind_speed_unit=ms")
      out = DATA / f"weather_{k}.parquet"
      if out.exists():
          continue
      for attempt in range(5):
          try:
              h = json.load(urllib.request.urlopen(url, timeout=120))["hourly"]
              break
          except Exception as e:
              print(k, "retry", attempt, e); time.sleep(20 * (attempt + 1))
      df = pd.DataFrame(h).rename(columns={"time": "t0"})
      df["t0"] = pd.to_datetime(df["t0"])
      df.to_parquet(out, index=False)
      print(k, len(df), df.t0.min(), df.t0.max(), df.isna().sum().sum(), "NaN")


if __name__ == "__main__":
    main()
