# Clean-clone reproduction, 18 Oct 2026

A fresh `git clone` of master (7e73219) on a 2-core, 4 GB Ubuntu box, `python3 -m venv`,
`pip install -r requirements.txt`, then `sh run_all.sh` with network access (build_data.py
cloned code4fukui/fukui-kanko-people-flow-data itself; JMA observations came from the
committed `data/jma_*.parquet`). Wall time about 6 hours at nice 15.

Result: every output file the paper cites reproduced byte-for-byte, except:

| File | Difference | Used by the paper? |
|---|---|---|
| out/20261015_forecast_gain_kept.csv | last-digit floating-point noise in four cells | yes, but unchanged at the printed rounding |
| out/20261012_weather_jma.md, section C (busy days) | Fukui Station calendar precision/recall 0.79/0.63 vs 0.78/0.62 | no (the paper's warning tables come from scan03 and scan05) |
| out/20261011_weather_openmeteo.md, forecast rows | Rainbow Line lot 1 WAPE 26.73/30.70 vs 26.86/31.48 with Open-Meteo observed weather | no (only the rain coefficients are quoted, and they reproduced) |
| out/figures/*.pdf | PDF metadata only | no |

The Open-Meteo rows differ because `get_weather.py` fetches the live archive, which is
revised after the fact; the paper's forecast results use the previous-runs archive, which
reproduced exactly. The cold-start step (`coldstart/cold_start.py`) ran separately after a
path fix in run_all.sh (be513fd); see the note below once it completes.
