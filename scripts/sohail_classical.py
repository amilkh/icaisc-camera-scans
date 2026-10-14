"""Rerun of scan05 section C (classical baselines) with a true h-day lead.

In scan05, ETS and SARIMAX forecast the whole Monday to Sunday week from one origin
at Monday - h - 1, so a "1d" forecast for Sunday is really 8 days ahead, while ridge
uses z(d-h) for every target day. Here both keep the weekly parameter refit, but for
each target day d the fitted model is run over data up to d-h (parameters fixed) and
forecasts exactly h steps ahead, as ridge does. SARIMAX gets, for each future day,
the forecast issued that many days earlier; days with a missing forecast are skipped
instead of falling back to observed weather.
Writes ../out/sohail_classical_true_lead.md
"""
import time
import warnings
from pathlib import Path
import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX
import scan03 as s3

warnings.filterwarnings("ignore")
OUT = Path(__file__).resolve().parent.parent / "out"; OUT.mkdir(exist_ok=True)
START, END = s3.START, pd.Timestamp("2026-10-10")
DAY = pd.Timedelta(days=1)


def ets_known(series, res):
    """Run Holt-Winters with the weekly fit's parameters and initial states over a longer series."""
    pr = res.params
    m = ExponentialSmoothing(series, trend="add", damped_trend=True, seasonal="add", seasonal_periods=7,
                             initialization_method="known", initial_level=pr["initial_level"],
                             initial_trend=pr["initial_trend"], initial_seasonal=pr["initial_seasons"])
    return m.fit(smoothing_level=pr["smoothing_level"], smoothing_trend=pr["smoothing_trend"],
                 smoothing_seasonal=pr["smoothing_seasonal"], damping_trend=pr["damping_trend"], optimized=False)


def classical_true_lead(k, h, kind):
    f = s3.frame(k); ly = f["ly"].asfreq("D"); obs = f[s3.WX].asfreq("D")
    fc = {j: s3.forecast_weather(s3.WX_SITE[k], j).reindex(ly.index) for j in range(1, h + 1)}
    preds = {}
    for monday in pd.date_range(START, END, freq="W-MON"):
        fit_end = monday - pd.Timedelta(days=h) - DAY          # same training data as scan05
        hist = ly[:fit_end].interpolate(limit_direction="both")
        try:
            if kind == "ets":
                res = ExponentialSmoothing(hist.values, trend="add", damped_trend=True, seasonal="add",
                                           seasonal_periods=7).fit()
            else:
                ex = obs.loc[hist.index].interpolate(limit_direction="both").values
                res = SARIMAX(hist.values, exog=ex, order=(1, 0, 1), seasonal_order=(1, 0, 1, 7),
                              trend="c").fit(disp=False, maxiter=200)
        except Exception:
            continue
        for d in pd.date_range(monday, monday + pd.Timedelta(days=6)):
            if d > END:
                break
            avail = ly[:d - pd.Timedelta(days=h)].interpolate(limit_direction="both")   # known at issue time
            try:
                if kind == "ets":
                    fcv = ets_known(avail.values, res).forecast(h)
                else:
                    fut = pd.date_range(avail.index[-1] + DAY, periods=h)
                    exf = pd.DataFrame([fc[j].loc[t] for j, t in zip(range(1, h + 1), fut)])
                    if exf.isna().any().any():
                        continue
                    exh = obs.loc[avail.index].interpolate(limit_direction="both").values
                    fcv = res.apply(avail.values, exog=exh).forecast(h, exog=exf.values)
            except Exception:
                continue
            preds[d] = float(np.expm1(fcv[-1]))
    return pd.Series(preds)


L = []
def p(x=""): L.append(x); print(x, flush=True)

p("# Classical baselines with a true h-day lead (rerun of scan05 C)\n")
p("ETS and SARIMAX refit weekly on the same data as scan05; for each target day the fitted model is run "
  "over data up to d-h and forecasts h steps, as ridge does. WAPE %, share within ±30% in brackets. "
  "Days are the intersection of all models, as in scan05.\n")
rows = []
t0 = time.time()
for k in s3.FEEDS:
    for h in [1, 3, 7]:
        y = s3.frame(k)["y"]
        P = {"naive": y.shift(7)}
        P["calendar"], _ = s3.run(k, h, "calendar")
        P["ridge + fcst wx"], _ = s3.run(k, h, "forecast")
        P["ETS"] = classical_true_lead(k, h, "ets")
        P["SARIMAX + fcst wx"] = classical_true_lead(k, h, "sarimax")
        idx = None
        for v in P.values():
            ii = v.dropna().index
            idx = ii if idx is None else idx.intersection(ii)
        idx = idx[(idx >= START) & (idx <= END)]
        idx = idx[y.reindex(idx).notna() & (y.reindex(idx) > 0)]
        yy = y.reindex(idx)
        row = {"site": s3.NAMES[k], "lead": f"{h}d", "days": len(idx)}
        for m, v in P.items():
            e = (v.reindex(idx) - yy).abs()
            row[m] = f"{100 * e.sum() / yy.sum():.1f} ({(e / yy < 0.3).mean():.2f})"
        rows.append(row)
        print(k, h, "done", f"{time.time() - t0:.0f}s", flush=True)
C = pd.DataFrame(rows).set_index("site")
cols = [str(c) for c in C.columns]
p("| site | " + " | ".join(cols) + " |"); p("|" + "---|" * (len(cols) + 1))
for i, r in C.iterrows():
    p("| " + " | ".join([str(i)] + [str(v) for v in r]) + " |")
(OUT / "sohail_classical_true_lead.md").write_text("\n".join(L) + "\n")
