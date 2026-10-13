# Literature from the ChatGPT search (11 Oct 2026)

All 18 DOIs below resolve on Crossref (checked 11 Oct). Only Bi 2020 was already in the paper bibliography. PMLR, CVF and PMC items were not Crossref-checked. Open each paper before citing it.

| Theme | First author, year | Title (short) | DOI |
|---|---|---|---|
| Counter validity | Wang 2021 | NWPU-Crowd benchmark | 10.1109/TPAMI.2020.3013269 |
| Counter validity | Determe 2022 | Monitoring large crowds with WiFi | 10.1109/JSYST.2021.3139756 |
| Counter validity | (PMC9575879) 2022 | Counting people in a CCTV region of interest | PMC9575879 |
| Face bias | Buolamwini 2018 | Gender Shades | PMLR v81 |
| Face bias | Kärkkäinen 2021 | FairFace | WACV 2021 |
| Face bias | Antipov 2016 | Children-specialised age estimation | CVPRW 2016 |
| Face bias | Moschoglou 2017 | AgeDB | CVPRW 2017 |
| **Plates** | **Bian 2025** | **AI licence-plate recognition, Shirakawa-go** | 10.37020/jgtr.10.2_129 |
| Parking | Yang 2019 | Parking occupancy, weather, 30 min | 10.1016/j.trc.2019.08.010 |
| Parking | Provoost 2020 | Parking occupancy via ML in the web of things | 10.1016/j.iot.2020.100301 |
| Parking | Lyu 2024 | On-street parking occupancy, LSTM | 10.1016/j.jtte.2022.05.004 |
| Hourly forecasting | Zheng 2021 | Multi-attraction hourly forecasting | 10.1016/j.annals.2021.103271 |
| Daily forecasting | Bi 2020 | Daily volume at attractions (in bib) | 10.1016/j.annals.2020.102923 |
| Cold start | Li 2021 | Transferability, stacked LSTM | 10.1016/j.trc.2021.102977 |
| Cold start | Li 2022 | Network-scale knowledge transfer | 10.1016/j.trc.2022.103719 |
| Cold start | Wang 2026 | Few-shot traffic flow, GCN | 10.1016/j.aej.2026.04.045 |
| Weather | Zou 2023 | Weather and activity, Guangzhou phone data | 10.1016/j.uclim.2023.101700 |
| Weather | Madden 2023 | Recreational trail foot traffic | 10.1016/j.jort.2023.100701 |
| Weather | Wanner 2024 | Weather and attraction choice experiment | 10.1016/j.jort.2024.100837 |
| Saudi | Al-Nabhan 2021 | IoT crowd management, Mina | 10.1109/ACCESS.2021.3099531 |
| Saudi | Nadeem 2021 | Missing persons in Madinah, IoT | 10.1109/MAJICC53071.2021.9526244 |
| Saudi | Gbban 2025 | Walkability in Al-Madinah | 10.1007/s43995-025-00182-5 |
| Saudi | Louie 2026 | Intangible heritage in Madinah | 10.3390/land15060993 |

## What it changes for us

1. **Bian 2025 is the closest prior work to the plate scan.** It already covers plate origin, rental cars and parking timing at Shirakawa-go. Our plate analysis can't claim to be first. What we can add: two years of data, origin mix on busy versus quiet days, and the threshold at which car park 2 starts to fill.
2. **Plates count gate passages, not occupancy.** Present the car-park-2 threshold as observed activation, not as capacity. A registration prefecture isn't proof of where the driver lives, and a rental car isn't proof of a foreign visitor.
3. **Cold start is its recommended headline,** and it is covered separately. Zheng 2021 and Li 2021 are the comparators to add to his bib.
4. **Weather by site type** (Zou 2023, Madden 2023) matches the earlier finding that weather matters at Tojinbo but not at the station. Next scan: weather by feed, including the car parks.
