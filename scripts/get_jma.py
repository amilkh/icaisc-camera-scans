"""Merge JMA hourly observations (AMeDAS / main stations) into data/jma_<site>.parquet.

Base: the cleaned files from the DHDE study (to early Mar 2026). Extension:
monthly files fetched with fetch_jma_monthly.py (already in the clean schema)
into data/jma/<station>_rawdata.
Columns are renamed to the Open-Meteo names so daily_weather() works on both.
"""
import glob
from pathlib import Path
import pandas as pd
from common import DATA

HG = Path.home() / "active/hokuriku-tourism-ai-governance/jma"
COLS = ["timestamp", "snow_depth_cm", "snowfall_1h_cm", "temp_c", "precip_1h_mm",
        "sun_1h_h", "wind_speed_ms", "weather_type", "humidity_pct"]

STATIONS = {"station": "fukuicity", "tojinbo": "mikuni", "rainbow": "mihama"}

if not HG.exists():
    # The merged files data/jma_<site>.parquet are committed (JMA observations are public
    # data; see README "Weather notes"), so a fresh clone can skip this step.
    missing = [s for s in STATIONS if not (DATA / f"jma_{s}.parquet").exists()]
    print("JMA source files not found; using the committed data/jma_*.parquet" + (f" (missing: {missing})" if missing else ""))
    raise SystemExit(1 if missing else 0)

for site, st in STATIONS.items():
    base = pd.read_csv(HG / f"jma_{st}_hourly_8.csv", parse_dates=["timestamp"])
    raws = sorted(glob.glob(str(DATA / "jma" / f"{st}_rawdata" / "*.csv")))
    new = pd.concat([pd.read_csv(f, parse_dates=["timestamp"]) for f in raws], ignore_index=True)
    df = pd.concat([base[COLS], new[COLS]]).sort_values("timestamp")
    df = df.drop_duplicates("timestamp", keep="last")
    df["t0"] = pd.to_datetime(df["timestamp"]) - pd.Timedelta(hours=1)  # JMA stamps the hour ending
    out = pd.DataFrame({
        "t0": df["t0"],
        "temperature_2m": pd.to_numeric(df["temp_c"], errors="coerce"),
        "precipitation": pd.to_numeric(df["precip_1h_mm"], errors="coerce"),
        "snowfall": pd.to_numeric(df["snowfall_1h_cm"], errors="coerce"),
        "wind_speed_10m": pd.to_numeric(df["wind_speed_ms"], errors="coerce"),
        "wind_gusts_10m": pd.to_numeric(df["wind_speed_ms"], errors="coerce"),  # no gusts in this export; max hourly mean used
        "sunshine_duration": pd.to_numeric(df["sun_1h_h"], errors="coerce") * 3600,
    })
    # Main stations print "--" (no precipitation observed) rather than 0, which parses as NaN.
    has_obs = out["temperature_2m"].notna()
    out.loc[has_obs, "precipitation"] = out.loc[has_obs, "precipitation"].fillna(0.0)
    out.to_parquet(DATA / f"jma_{site}.parquet", index=False)
    print(site, st, len(out), out.t0.min(), out.t0.max(),
          "missing %:", (out.drop(columns="t0").isna().mean() * 100).round(1).to_dict())
