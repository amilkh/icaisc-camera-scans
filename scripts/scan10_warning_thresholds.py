"""Scan 10: operating points for the overflow-lot warning (Rainbow Line lot 2, three days
ahead, forecast weather). The paper reports one cut-off (probability 0.5). For a staffing
decision the operator chooses the cut-off, so this sweeps it and reports, per cut-off, the
days flagged, precision, recall, missed busy days and call-outs per 30 days. Also the
top-20% warnings at the three sites. Writes ../out/20261018_warning_thresholds.md.
"""
import numpy as np
import pandas as pd
import scan03 as s3
from sklearn.linear_model import LogisticRegression

L = []
def p(x=""): L.append(x); print(x, flush=True)

def probs(k, label, mode, h=3):
    """Out-of-sample probabilities and labels, as in scan03.busy_eval."""
    f = s3.frame(k)
    if label == "lot2":
        f["rl2"] = s3.D["rl2"]
    obs = f[s3.WX]
    Xtr = s3.design(f, h, None if mode == "calendar" else obs)
    Xte = s3.design(f, h, None if mode == "calendar" else s3.forecast_weather(s3.WX_SITE[k], h))
    P, Y = [], []
    for monday in pd.date_range(s3.START, f.index.max(), freq="W-MON"):
        cutoff = monday - pd.Timedelta(days=h)
        if label == "lot2":
            lab = (f["rl2"] >= 20).where(f["rl2"].notna())
        else:
            lab = (f["y"] >= f.loc[f.index < cutoff, "y"].quantile(0.8)).where(f["y"].notna())
        tr = (Xtr.index < cutoff) & Xtr.notna().all(1) & lab.notna()
        mdl = LogisticRegression(max_iter=3000).fit(Xtr[tr], lab[tr].astype(int))
        idx = f.loc[monday: monday + pd.Timedelta(days=6)].index
        te = Xte.loc[idx].notna().all(1) & lab.loc[idx].notna()
        if te.any():
            P.append(pd.Series(mdl.predict_proba(Xte.loc[idx][te])[:, 1], index=idx[te])); Y.append(lab.loc[idx][te])
    return pd.concat(P), pd.concat(Y).astype(int)

p("# Scan 10: warning cut-offs as staffing operating points (three days ahead, forecast weather)\n")
p("Same models and test year as Tables V and VI. Cut-off = predicted probability at or above which a warning is issued. "
  "Call-outs = warnings per 30 test days; missed = busy days with no warning.\n")
CUTS = [0.3, 0.4, 0.5, 0.6, 0.7]
for k, label, name in [("rl1", "lot2", "Rainbow Line: overflow lot 2 in use (>= 20 plates)"),
                       ("station", "top", "Fukui Station: top-20% day"), ("tojinbo", "top", "Tojinbo: top-20% day"),
                       ("rl1", "top", "Rainbow Line lot 1: top-20% day")]:
    pr, yb = probs(k, label, "forecast")
    p(f"## {name}\n")
    p(f"{len(yb)} test days, {int(yb.sum())} busy ({yb.mean():.0%}).\n")
    p("| cut-off | flagged | precision | recall | missed busy days | call-outs per 30 days |"); p("|---|---|---|---|---|---|")
    for c in CUTS:
        hit = pr >= c; tp = int((hit & (yb == 1)).sum())
        p(f"| {c:.1f} | {int(hit.sum())} | {tp / max(hit.sum(), 1):.2f} | {tp / max(yb.sum(), 1):.2f} | {int(yb.sum()) - tp} | {30 * hit.sum() / len(yb):.1f} |")
    p()
open("../out/20261018_warning_thresholds.md", "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
