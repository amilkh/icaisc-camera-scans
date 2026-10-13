# ICAISC camera scans

Local exploratory analysis of the Fukui open AI-camera data (code4fukui, pinned at b89bc2c, data to 2026-10-10) for the ICAISC 2027 paper.

- `scripts/build_data.py` builds `data/*.parquet` (gitignored) from `~/active/fukui-kanko-people-flow-data` with `git archive`.
- `scripts/scanNN.py` writes `out/scanNN.md`.
- Python: `.venv/bin/python` (uv).

Covered separately in the paper repository, so not repeated here: cold-start hourly forecasting against history length, face age and gender against the FTAS survey, Tojinbo face-share drift, outage counts, the 7-day and 12-month production backtests.

## Data and licence

Camera counts: code4fukui/fukui-kanko-people-flow-data (MIT), pinned at b89bc2c. Weather: JMA station observations and the Open-Meteo archive and previous-runs API. Code: MIT.
