#!/bin/sh
# Reproduce every table and figure in the paper from the pinned open data.
# Needs: a clone of code4fukui/fukui-kanko-people-flow-data (PF_REPO), Python 3.12,
# `pip install -r requirements.txt`, and network for Open-Meteo and JMA.
set -e
cd "$(dirname "$0")/scripts"
P=${PYTHON:-../.venv/bin/python}
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
$P fig_timeseries.py      # Fig. 2
$P fig_leadtime.py        # Fig. 3
# Cold start (Table VII, Fig. 4): see coldstart/README.md
