"""Scan 6: Rainbow Line with faces and plates combined.
Gate cameras count plates (vehicles) and faces (people in or near vehicles).
Build three daily series for lots 1+2: plates, faces, and a combined people
index (faces where available, else plates x median faces-per-plate), and run
the weather effect, 1/3-day forecasts and busy-day warnings on each.
Writes ../out/20261013_rainbow_faces_plates.md.
"""
import warnings
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import roc_auc_score
import scan03 as s3
from common import DATA, daily_weather, daytype, load

warnings.filterwarnings("ignore")
L = []
def p(x=""): L.append(x)
def tbl(df, fmt="{:.2f}"):
    cols = [str(c) for c in df.columns]
    p("| " + " | ".join([df.index.name or ""] + cols) + " |"); p("|" + "---|" * (len(cols) + 1))
    for i, r in df.iterrows():
        p("| " + " | ".join([str(i)] + [fmt.format(v) if isinstance(v, (float, np.floating)) else str(v) for v in r]) + " |")
    p()

def daily(site, cls):
    d = load("5min", site, cls).set_index("t0")["count"]
    g = d.groupby(d.index.normalize()); tot, n = g.sum(), g.size()
    tot[n < 0.8 * 288] = np.nan
    return tot
S1, S2 = "rainbow-line-parking-lot-1-gate", "rainbow-line-parking-lot-2-gate"
plates = daily(S1, "LicensePlate").add(daily(S2, "LicensePlate"), fill_value=0)
faces = daily(S1, "Face").add(daily(S2, "Face"), fill_value=0)
df = pd.DataFrame({"plates": plates, "faces": faces}).asfreq("D")
# outage: both zero
out = (df["plates"] == 0) & (df["faces"] == 0)
df[out] = np.nan
ratio = (df["faces"] / df["plates"].replace(0, np.nan))
p("# Rainbow Line: faces and plates combined (lots 1 + 2)\n")
p(f"Valid days {df.dropna().shape[0]}. Median faces per plate {ratio.median():.2f} (IQR {ratio.quantile(.25):.2f} to {ratio.quantile(.75):.2f}); daily correlation plates vs faces r = {df['plates'].corr(df['faces']):.2f}, log r = {np.log1p(df['plates']).corr(np.log1p(df['faces'])):.2f}.\n")
df["combined"] = df["faces"].where(df["faces"] > 0, df["plates"] * ratio.median())
df["sum"] = df["plates"] + df["faces"]

# A. weather effects
p("## A. Weather effect (JMA Mihama), % change per unit\n")
w = daily_weather("rainbow", source="jma")
rows = []
for col in ["plates", "faces", "combined"]:
    f = pd.DataFrame({"ly": np.log1p(df[col])}).join(w).dropna()
    dt = daytype(f.index); f["dow"] = f.index.dayofweek.astype(str); f["hol"] = (dt.values == "holiday").astype(int); f["ym"] = f.index.to_period("M").astype(str)
    m = smf.ols("ly ~ C(dow) + hol + C(ym) + rain_mm + gust_ms + sun_h + temp_c", f).fit(cov_type="HAC", cov_kwds={"maxlags": 7})
    eff = lambda v, k: f"{100*(np.exp(m.params[v]*k)-1):+.0f} (±{196*m.bse[v]*k:.0f})"
    rows.append({"series": col, "days": int(m.nobs), "10 mm rain": eff("rain_mm", 10), "+5 m/s wind": eff("gust_ms", 5), "+3 h sun": eff("sun_h", 3), "+5 C": eff("temp_c", 5), "R2": m.rsquared})
tbl(pd.DataFrame(rows).set_index("series"))

# B. forecasts and warnings, reuse scan03 machinery by monkeypatching the target
p("## B. Forecasts (WAPE %, within ±30%) and 3-day busy warnings, forecast weather at issue time\n")
rows = []
orig = s3.D.copy()
for col in ["plates", "faces", "combined"]:
    s3.D = orig.copy(); s3.D["rl1"] = df[col]
    r = {"series": col}
    for h in [1, 3]:
        P = {m: s3.run("rl1", h, m) for m in ["calendar", "forecast"]}
        y = P["calendar"][1]
        idx = P["calendar"][0].index.intersection(P["forecast"][0].index); idx = idx[y.loc[idx].notna() & (y.loc[idx] > 0)]
        yy = y.loc[idx].values
        for m in P:
            e = np.abs(P[m][0].loc[idx].values - yy)
            r[f"{h}d {m}"] = f"{100*e.sum()/yy.sum():.1f} ({(e/yy<0.3).mean():.2f})"
    for mode in ["calendar", "forecast"]:
        b = s3.busy_eval("rl1", "top", mode, h=3)
        r[f"busy AUC ({mode})"] = b["AUC [95% CI]"].split(" ")[0]; r[f"prec ({mode})"] = f"{b['precision']:.2f}"
    rows.append(r)
s3.D = orig
tbl(pd.DataFrame(rows).set_index("series"))
open("../out/20261013_rainbow_faces_plates.md", "w").write("\n".join(L)); print("\n".join(L))
