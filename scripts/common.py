"""Shared loaders for the camera scans."""
from pathlib import Path
import jpholiday
import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
FEEDS = {
    "station": ("fukui-station-east-entrance", "Person"),
    "tojinbo": ("tojinbo-shotaro", "Person"),
    "rl1": ("rainbow-line-parking-lot-1-gate", "LicensePlate"),
    "rl2": ("rainbow-line-parking-lot-2-gate", "LicensePlate"),
}
REGIONS = {
    "Fukui": ["Fukui"],
    "Hokuriku": ["Ishikawa", "Toyama", "Niigata"],
    "Kansai": ["Shiga", "Kyoto", "Osaka", "Hyogo", "Nara", "Wakayama"],
    "Chubu": ["Aichi", "Gifu", "Mie", "Shizuoka", "Nagano", "Yamanashi"],
    "Kanto": ["Tokyo", "Kanagawa", "Saitama", "Chiba", "Ibaraki", "Tochigi", "Gunma"],
}


def load(level, site, cls):
    return pd.read_parquet(DATA / f"{level}_{site}_{cls}.parquet")


def fivemin(key):
    site, cls = FEEDS[key]
    return load("5min", site, cls)


def daily_counts():
    """Daily totals from 5-min bins; zero days and days with <80% of bins are NaN (outage)."""
    out = {}
    for k in FEEDS:
        d = fivemin(k).set_index("t0")["count"]
        g = d.groupby(d.index.normalize())
        tot, n = g.sum(), g.size()
        tot[n < 0.8 * 288] = np.nan
        out[k] = tot
    # A zero day is an outage or a closure, except at overflow lot 2, which is
    # legitimately empty on quiet days while lot 1 is counting.
    for k in out:
        z = out[k] == 0
        if k == "rl2":
            z &= ~(out["rl1"] > 0)
        out[k][z] = np.nan
    df = pd.DataFrame(out)
    df.index.name = "date"
    return df.asfreq("D")


def daytype(idx):
    idx = pd.DatetimeIndex(idx)
    hol = np.array([jpholiday.is_holiday(d.date()) for d in idx])
    wk = idx.dayofweek >= 5
    return pd.Series(np.where(hol, "holiday", np.where(wk, "weekend", "weekday")), index=idx)


def daily_weather(site, h0=9, h1=17, source="openmeteo"):
    """Daytime (h0..h1 inclusive) weather per day. source: openmeteo or jma."""
    prefix = "weather" if source == "openmeteo" else "jma"
    w = pd.read_parquet(DATA / f"{prefix}_{site}.parquet").set_index("t0")
    w = w[(w.index.hour >= h0) & (w.index.hour <= h1)]
    g = w.groupby(w.index.normalize())
    return pd.DataFrame({
        "rain_mm": g["precipitation"].sum(min_count=6),
        "snow_cm": g["snowfall"].sum(),
        "wind_ms": g["wind_speed_10m"].mean(),
        "gust_ms": g["wind_gusts_10m"].max(),
        "temp_c": g["temperature_2m"].mean(),
        "sun_h": g["sunshine_duration"].sum(min_count=6) / 3600,
    })


WX_SITE = {"station": "station", "tojinbo": "tojinbo", "rl1": "rainbow", "rl2": "rainbow"}
