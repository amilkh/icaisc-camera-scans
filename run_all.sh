#!/bin/sh
# Reproduce every table and figure in the paper from the pinned open data.
# Needs: Python 3.12, `pip install -r requirements.txt`, git and network. build_data.py
# clones code4fukui/fukui-kanko-people-flow-data into data/pf_repo unless PF_REPO or
# ~/active/fukui-kanko-people-flow-data exists; JMA observations are committed as
# data/jma_*.parquet (get_jma.py rebuilds them only where the source files exist).
set -e
cd "$(dirname "$0")/scripts"
P=${PYTHON:-../.venv/bin/python}
case $P in /*) ;; *) P=$(cd "$(dirname "$P")" && pwd)/$(basename "$P");; esac   # absolute, for the cd below
$P build_data.py          # data/*.parquet from the pinned commit b89bc2c
$P get_weather.py         # Open-Meteo archive (observed)
$P get_forecasts.py       # Open-Meteo previous-runs API, leads 1 to 7
$P get_jma.py             # JMA station observations (see README)
$P scan01.py              # Table I, plate origins, lot-2 activation
$P scan02.py jma          # Table II
$P scan02.py openmeteo    # Open-Meteo comparison in the text
$P scan03.py              # Tables III and V
$P scan04.py              # Fig. 3 and busy-day AUC by lead
$P scan05.py              # Tables IV and VI, nested tuning
$P scan06.py              # faces vs plates paragraph
$P scan07.py              # window sensitivity, faces recall
$P scan08_data_facts.py   # Data-section facts (outages, detections per visitor, faces)
$P scan09_faces_warning_counts.py  # faces warning day counts
$P fig_timeseries.py      # Fig. 2
$P fig_leadtime.py        # Fig. 3
cd .. && $P coldstart/cold_start.py   # cold start (Table VI/VII, Fig. 4); see coldstart/README.md
