# Classical baselines with a true h-day lead (rerun of scan05 C)

ETS and SARIMAX refit weekly on the same data as scan05; for each target day the fitted model is run over data up to d-h and forecasts h steps, as ridge does. WAPE %, share within ±30% in brackets. Days are the intersection of all models, as in scan05.

| site | lead | days | naive | calendar | ridge + fcst wx | ETS | SARIMAX + fcst wx |
|---|---|---|---|---|---|---|---|
| Fukui Station | 1d | 338 | 19.3 (0.84) | 11.9 (0.95) | 12.0 (0.95) | 11.9 (0.94) | 12.2 (0.92) |
| Fukui Station | 3d | 338 | 19.3 (0.84) | 14.4 (0.90) | 14.6 (0.90) | 16.1 (0.88) | 16.3 (0.88) |
| Fukui Station | 7d | 340 | 19.3 (0.84) | 16.3 (0.89) | 16.2 (0.89) | 18.2 (0.86) | 17.5 (0.87) |
| Tojinbo | 1d | 353 | 36.2 (0.55) | 23.3 (0.73) | 21.6 (0.75) | 25.8 (0.68) | 22.1 (0.72) |
| Tojinbo | 3d | 352 | 36.3 (0.55) | 27.2 (0.65) | 26.0 (0.66) | 32.7 (0.62) | 27.7 (0.66) |
| Tojinbo | 7d | 356 | 36.5 (0.54) | 28.8 (0.63) | 26.7 (0.67) | 34.8 (0.58) | 28.7 (0.59) |
| Rainbow Line lot 1 | 1d | 295 | 41.5 (0.44) | 34.0 (0.51) | 27.6 (0.64) | 32.0 (0.56) | 25.9 (0.64) |
| Rainbow Line lot 1 | 3d | 296 | 41.7 (0.44) | 38.5 (0.40) | 32.1 (0.54) | 36.0 (0.52) | 32.6 (0.52) |
| Rainbow Line lot 1 | 7d | 299 | 41.4 (0.44) | 40.6 (0.37) | 37.3 (0.43) | 37.9 (0.47) | 38.8 (0.40) |
