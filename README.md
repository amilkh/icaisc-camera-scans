# ICAISC camera scans

Local exploratory analysis of the Fukui open AI-camera data (code4fukui, pinned at b89bc2c, data to 2026-10-10) for the ICAISC 2027 paper.

- `scripts/build_data.py` builds `data/*.parquet` (gitignored) from `~/active/fukui-kanko-people-flow-data` with `git archive`.
- `scripts/scanNN.py` writes `out/scanNN.md`.
- Python: `.venv/bin/python` (uv).

Covered separately in the paper repository, so not repeated here: cold-start hourly forecasting against history length, face age and gender against the FTAS survey, Tojinbo face-share drift, outage counts, the 7-day and 12-month production backtests.

## Data and licence

Camera counts: code4fukui/fukui-kanko-people-flow-data (MIT), pinned at b89bc2c. Weather: JMA station observations and the Open-Meteo archive and previous-runs API. Code: MIT.


## Cold start

`coldstart/` holds the cold-start experiment (Table VII, Fig. 4) by Mohammed Sohail, with its outputs. The classical baselines at a true h-day lead (`scan05.py` section C) and the outage rule in `scan06.py` are also his.

`scripts/sohail_classical.py`, `scripts/sohail_faces_plates.py` and their outputs `out/sohail_*.md` are his first standalone versions of those two fixes, run before the active-hours window was frozen (1df9f93). They are superseded: the paper uses `scan05.py` section C (`out/20261013_review_fixes.md`) and `scan06.py` (`out/20261013_rainbow_faces_plates.md`), so small differences between the files are expected.

## Weather notes

JMA observations come from the DHDE study files plus monthly pages fetched with `fetch_jma_monthly.py` from that repository; `get_jma.py` merges them and treats the main station's "--" rain marker as zero. Open-Meteo observed weather and the previous-runs forecast archive are fetched by `get_weather.py` and `get_forecasts.py`. The active-hours window is estimated from pre-test counts only (`common.active_hours`).
