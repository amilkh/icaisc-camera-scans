"""Scan 4 (heavier, run on the seminar box): how far ahead can a site plan?
Lead times 1 to 7 days, all with the weather forecast issued at that lead.
Models: same-weekday naive, ridge (calendar), ridge + forecast weather,
gradient boosting + forecast weather. Busy-day AUC by lead.
Writes ../out/20261012_lead_time.md and ../out/20261012_lead_time.csv.
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
import scan03 as s3

L = []
def p(x=""): L.append(x)

def run_model(k, h, kind):
    f = s3.frame(k)
    obs = f[s3.WX]
    wx_tr = None if kind == "calendar" else obs
    wx_te = None if kind == "calendar" else s3.forecast_weather(s3.WX_SITE[k], h)
    Xtr, Xte = s3.design(f, h, wx_tr), s3.design(f, h, wx_te)
    preds = []
    for monday in pd.date_range(s3.START, f.index.max(), freq="W-MON"):
        cutoff = monday - pd.Timedelta(days=h)
        ok = (Xtr.index < cutoff) & Xtr.notna().all(1) & f["ly"].notna()
        if kind == "gbm":
            mdl = HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05, max_leaf_nodes=15,
                                                min_samples_leaf=10, random_state=0)
        else:
            from sklearn.linear_model import Ridge
            mdl = Ridge(alpha=1.0)
        mdl.fit(Xtr[ok], f["ly"][ok])
        idx = f.loc[monday: monday + pd.Timedelta(days=6)].index
        Xt = Xte.loc[idx]; good = Xt.notna().all(1)
        if good.any():
            preds.append(pd.Series(np.expm1(mdl.predict(Xt[good])), index=idx[good]))
    return pd.concat(preds), f["y"]

rows = []
for k in s3.FEEDS:
    for h in range(1, 8):
        P = {m: run_model(k, h, m) for m in ["calendar", "ridge_fcst", "gbm"]}
        y = P["calendar"][1]
        naive = y.shift(7) if h <= 7 else y.shift(14)
        common = P["calendar"][0].index
        for m in P:
            common = common.intersection(P[m][0].index)
        common = common[y.loc[common].notna() & (y.loc[common] > 0) & naive.loc[common].notna()]
        yy = y.loc[common].values
        allp = {"naive": naive.loc[common].values, **{m: P[m][0].loc[common].values for m in P}}
        for m, pr in allp.items():
            e = np.abs(pr - yy)
            rows.append({"site": s3.NAMES[k], "lead_days": h, "model": m, "days": len(common),
                         "wape": 100 * e.sum() / yy.sum(), "within30": (e / yy < 0.3).mean()})
        t, pv = s3.dm_test(pd.Series(allp["calendar"] - yy), pd.Series(allp["ridge_fcst"] - yy))
        rows[-2]["dm_t_vs_calendar"], rows[-2]["dm_p"] = t, pv
        print(k, h, "done", flush=True)
R = pd.DataFrame(rows); R.to_csv("../out/20261012_lead_time.csv", index=False)

p("# Scan 04: forecast skill by lead time (1 to 7 days), with the weather forecast available at each lead\n")
p("Rolling origin, weekly refit, test 2025-10-13 to 2026-10-10. WAPE in %. *ridge_fcst* = ridge with the Open-Meteo forecast issued that many days earlier; *gbm* = gradient boosting with the same inputs.\n")
for site, g in R.groupby("site", sort=False):
    w = g.pivot(index="lead_days", columns="model", values="wape")[["naive", "calendar", "ridge_fcst", "gbm"]].round(1)
    c = g.pivot(index="lead_days", columns="model", values="within30")["ridge_fcst"].round(2)
    w["within ±30% (ridge_fcst)"] = c
    dm = g[g.model == "ridge_fcst"].set_index("lead_days")["dm_p"].round(3)
    w["DM p, ridge_fcst vs calendar"] = dm
    p(f"## {site}\n")
    p("| lead (days) | " + " | ".join(w.columns) + " |"); p("|" + "---|" * (len(w.columns) + 1))
    for i, r in w.iterrows():
        p(f"| {i} | " + " | ".join(str(v) for v in r.values) + " |")
    p()

p("## Busy-day warning AUC by lead (ridge features + forecast weather, logistic)\n")
p("| warning | " + " | ".join(f"{h}d" for h in range(1, 8)) + " |"); p("|" + "---|" * 8)
for k, label, name in [("station", "top", "Fukui Station top-20%"), ("tojinbo", "top", "Tojinbo top-20%"),
                       ("rl1", "top", "Rainbow Line top-20%"), ("rl1", "lot2", "Rainbow Line car park 2 in use")]:
    cells = []
    for h in range(1, 8):
        r = s3.busy_eval(k, label, "forecast", h=h)
        cells.append(r["AUC [95% CI]"].split(" ")[0])
    p(f"| {name} | " + " | ".join(cells) + " |")
p()
open("../out/20261012_lead_time.md", "w").write("\n".join(L)); print("\n".join(L))
