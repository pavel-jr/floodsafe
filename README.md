# Natural Disasters in Israel & the Middle East (NDS-data)
### Kaggle-Ready Curated Catalogs, Dual-Dataset Architecture & Spatial Risk Analytics

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Dataset Format: JSON & CSV](https://img.shields.io/badge/Format-JSON%20%7C%20CSV-blue.svg)](#dataset-schema--catalog-structure)
[![Kaggle Usability Score: 10.0](https://img.shields.io/badge/Kaggle_Usability-10.0-success.svg)](#kaggle-compatibility)
[![Validation: Passing](https://img.shields.io/badge/Validation-100%25_Passing-brightgreen.svg)](#validation--data-quality)
[![Dual-Catalog Scope](https://img.shields.io/badge/Catalogs-Israel_(105)_%7C_Middle_East_(182)-indigo.svg)](#dataset-schema--catalog-structure)

---

## 1. Project Overview & Research Waves

The **Natural Disasters in Israel & the Middle East (NDS-data)** repository is an authoritative, multi-hazard geophysical and meteorological data platform. It contains two unified, machine-learning-ready catalogs developed across two intensive data gathering waves:

1. **Wave 1 — Israel & Jerusalem Deep Spatial Catalog (`data/israel_jerusalem_natural_disasters.*`)**:
   - Curated empirical catalog expanded from 75 to **105 verified natural disaster events** spanning from antiquity (**759 BCE**) through the modern instrumental era (**1920–2026**).
   - High-granularity geospatial coverage of the **Jerusalem Mountain Corridor**, Judean Desert, Dead Sea Transform fault system, Coastal Plain, and Galilee.
   - Triangulated across the University of Haifa Database of Natural Disasters in Israel (NDI), the National Knowledge & Research Center for Emergency Readiness (NKRER / רח"ל), the Jerusalem Institute for Policy Research (JIPR), the Israel Meteorological Service (IMS), and the Geological Survey of Israel (GSI).

2. **Wave 2 — Pan-Middle East Secondary Catalog (`data/middle_east_natural_disasters.*`)**:
   - Secondary catalog encompassing **182 verified catastrophic natural disasters** across all **17 nations of the Middle East**: Turkey, Iran, Iraq, Syria, Lebanon, Jordan, Israel, State of Palestine, Egypt, Saudi Arabia, Yemen, Oman, United Arab Emirates, Qatar, Bahrain, Kuwait, and Cyprus.
   - Comprehensive temporal span from the **526 CE Antioch Earthquake** through the **2026 Middle East Extreme Heat Dome**.
   - Captures regional cross-border tectonic drivers (East Anatolian Fault, North Anatolian Fault, Zagros Fold-and-Thrust Belt, Dead Sea Transform, Makran Subduction Zone) and synoptic climate drivers (Persian Gulf convective storms, Arabian Sea tropical cyclones, Red Sea Troughs, and Subtropical Jet heat domes).
   - Synthesizes international and national records: CRED EM-DAT, NOAA NCEI, USGS Earthquake Hazards Program, ThinkHazard! (World Bank / GFDRR), AFAD (Turkey), and IIEES (Iran).

---

## 2. Authoritative Data Sources

The catalogs synthesize peer-reviewed academic literature, national civil defense databases, macroseismic chronicles, and instrumental sensor networks:

| Organization | Scope & Coverage | Key Parameters Provided |
| :--- | :--- | :--- |
| **Haifa NDI (University of Haifa)**<br>*(Prof. Moshe Inbar)* | Foundational academic Levantine disaster database across 3,000 years. | Macroseismic intensity, historical flood hydrographs, Neot HaKikar 1970 cliff failure, Safed 1837 chronicles. |
| **NKRER & NEMA (רח"ל)**<br>*(Haifa, Technion, HUJI, NEMA)* | National disaster management think-tank and national reference scenarios (*תרחישי ייחוס*). | National earthquake scenario models ($M_w 7.0$), critical lifeline dependencies, multi-hazard evacuation planning. |
| **Jerusalem Institute for Policy Research (JIPR)** | Premier urban policy and climate vulnerability institute for Jerusalem. | Snowstorm benchmarks (1920, 1950, Dec 2013 Alexa), urban arterial cutoffs (Highways 1 & 443), winter resilience indices. |
| **ThinkHazard! (World Bank / GFDRR)** | Multi-hazard risk assessment profiling national and sub-national administrative units. | Standardized 4-tier risk ratings (High, Medium, Low, Very Low) for Israel and all 17 Middle Eastern nations. |
| **EM-DAT (CRED, UCLouvain)** | Global disaster database tracking catastrophic criteria ($10+$ killed, $100+$ affected, emergency declaration). | Standardized disaster taxonomy, international economic loss validations in USD, mortality tracking. |
| **NOAA NCEI & USGS Earthquakes** | Global seismic, tsunami, and significant volcanic catalogs. | Instrument epicenter coordinates, focal depth ($h$), moment magnitude ($M_w$), and modified Mercalli intensities ($I_{MM}$). |
| **Israel Meteorological Service (IMS)** | National weather observation network, station archives, and synoptic maps. | Jerusalem snow depth records (1920: 97.5 cm, 1950: 70 cm, 2013: 40–80 cm), all-time heat records (44.4°C, 42.7°C), radar rainfall. |
| **Geological Survey of Israel (GSI)** | National geological, seismological, and geotechnical authority. | Dead Sea Transform active fault traces, sinkhole progression rate ($\sim 1.1\text{ m/yr}$ sea drop), paleoseismic trench data. |
| **AFAD & Boğaziçi KOERI (Turkey)** | Disaster and Emergency Management Presidency of Turkey. | 2023 Kahramanmaraş ($M_w 7.8, 7.5$), 1999 Marmara/İzmit ($M_w 7.6$), 1939 Erzincan ($M_w 7.8$), and Aegean tsunamis. |
| **IIEES (Iran)** | International Institute of Earthquake Engineering and Seismology. | 2003 Bam ($M_w 6.6$), 1990 Manjil-Rudbar ($M_w 7.4$), 1978 Tabas ($M_w 7.8$), Zagros seismic belt events. |

---

## 3. Dataset Schema & Catalog Structure

All data files reside in the [`data/`](file:///workspace/.worktrees/tawfiqkhalilieh__NDS-data/antigravity_task_1792005201936/data) directory:

```
data/
├── israel_jerusalem_natural_disasters.json    # Primary Wave 1 catalog (105 events, full schema)
├── israel_jerusalem_natural_disasters.csv     # Flat tabular CSV export (Israel & Area)
├── middle_east_natural_disasters.json         # Secondary Wave 2 catalog (182 events, 17 nations)
├── middle_east_natural_disasters.csv          # Flat tabular CSV export (Pan-Middle East)
├── data_dictionary.json                       # 30-field schema specification for Israel catalog
├── middle_east_data_dictionary.json           # 30-field schema specification for Middle East catalog
├── hazard_risk_profiles.json                  # ThinkHazard! & NEMA national profiles (Israel)
├── middle_east_hazard_profiles.json           # ThinkHazard! multi-hazard matrix for all 17 nations
├── kaggle_dataset_metadata.json               # Kaggle metadata for primary dataset
├── middle_east_kaggle_metadata.json           # Kaggle metadata for secondary Middle East dataset
└── startup_catastrophe_models.json            # Parametric insurance triggers & spatial risk algorithms
```

### Attribute Specifications (30 Fields)

Both datasets adhere to a unified schema enabling seamless joins and cross-catalog analytics:

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `id` | `String (PK)` | Unique identifier (e.g. `ISR-EQ-1927-01`, `TUR-EQ-2023-01`, `OMN-CYC-2007-01`) |
| `event_name` | `String` | Formal name in English with native script transliteration |
| `disaster_type` | `String` | `Earthquake`, `Severe Winter Storm`, `Wildfire`, `Flash Flood`, `Extreme Heat`, `River Flood`, `Tropical Cyclone`, `Volcanic Eruption`, `Sinkhole & Subsidence`, `Drought`, `Tsunami`, `Landslide`, `Extreme Dust Storm` |
| `disaster_subtype` | `String` | Specific geological or meteorological mechanism (e.g. `Tectonic Strike-Slip`, `Tropical Cyclone Category 5`, `Arid Slot-Canyon Flash Flood`) |
| `country` | `String` | Country of primary impact (17 Middle Eastern nations) |
| `district` / `subregion` | `String` | First-level administrative unit or regional subregion (`Jerusalem District`, `Anatolia`, `Levant`, `Iranian Plateau`, `Arabian Peninsula`) |
| `date_start` / `date_end` | `ISO Date` | YYYY-MM-DD bounds (negative years for BCE) |
| `year` | `Integer` | Calendar year |
| `primary_location` | `String` | Epicenter, municipality, wadi basin, or geographical landmark |
| `latitude` / `longitude` | `Float` | Decimal coordinates in WGS 84 |
| `severity_level` | `String` | Standardized category: `Catastrophic`, `Very High`, `High`, `Moderate` |
| `severity_metric` | `String` | Instrumental measurement (e.g. `Mw 7.8 / Intensity XI`, `97.5 cm snow depth`, `50.4°C`, `260 km/h winds`) |
| `impact_jerusalem` | `Boolean` | Flag indicating impact on Jerusalem (true for 76 Israel events) |
| `fatalities` | `Integer` | Verified casualty count |
| `injuries` | `Integer` | Documented injuries requiring medical treatment |
| `evacuated_displaced` | `Integer` | Displaced residents or evacuated populations |
| `economic_damage_usd_est` | `Integer` | Estimated total direct and indirect economic losses in USD |
| `summary` | `Text` | Synthesized narrative of disaster chronology, footprint, and aftermath |
| `tectonic_or_synoptic_driver` | `Text` | Tectonic fault system or atmospheric synoptic pressure system |
| `emergency_response` | `Text` | Government response, civil protection, IDF Home Front Command, Red Crescent, or international mobilization |
| `citations` / `sources` | `Array<String>` | Primary catalog references, academic DOIs, and archival sources with official verification URLs |

---

## 4. Key Regional Benchmarks & Historical Insights

### A. The Dead Sea Transform & Levantine Fault Networks
* **Recurrence Intervals**: Major $M_w \ge 6.0$ earthquakes along the Dead Sea Transform (DST) recur approximately every **$90\text{--}110$ years**.
* **1927 Jericho / Dead Sea Earthquake** ($M_w 6.25$): Left 285+ fatalities across the Levant, destroying homes in Jerusalem's Old City, Augusta Victoria, and Al-Aqsa Mosque.
* **Historical Cataclysms**: 749 CE Galilee/Jordan Valley ($M_w 7.3$, ruined Scythopolis), 1033 CE Jordan Valley ($M_w 7.0$), 1202 Levant Mega-Earthquake ($M_w 7.6$, $>30,000$ casualties), 1759 Near East twin shocks ($M_w 7.4$), and 1837 Safed Earthquake ($M_w 6.8$, destroyed Safed and Tiberias).

### B. Pan-Middle East Tectonic Belts
* **Anatolian Plate Boundaries (Turkey)**: The East and North Anatolian Faults have generated the region's deadliest instrumental earthquakes:
  - **February 6, 2023 Kahramanmaraş Earthquake Sequence** ($M_w 7.8$ & $M_w 7.5$): $>53,500$ deaths in Turkey and $>8,400$ in Syria; $>\$104\text{B USD}$ in damages.
  - **August 17, 1999 Marmara / İzmit Earthquake** ($M_w 7.6$): 17,480 fatalities; $>\$20\text{B USD}$ losses in Turkey's industrial heartland.
  - **December 26, 1939 Erzincan Earthquake** ($M_w 7.8$): 32,700 fatalities in eastern Anatolia.
* **Zagros & Central Iran Belts**:
  - **December 26, 2003 Bam Earthquake** ($M_w 6.6$): 34,000+ fatalities; leveled the ancient mudbrick citadel of Arg-e Bam.
  - **June 21, 1990 Manjil-Rudbar Earthquake** ($M_w 7.4$): 40,000+ fatalities and 500,000 left homeless.
  - **September 16, 1978 Tabas Earthquake** ($M_w 7.8$): 20,000 fatalities.

### C. Extreme Meteorological & Climate Disasters
* **Jerusalem Mountain Blizzards**:
  - **February 1920**: All-time instrumental snow depth record of **$97.5\text{ cm}$** in Jerusalem (IMS).
  - **February 1950**: The "Great Snow" covered Jerusalem in **$70\text{ cm}$** of snow, with coastal snow in Tel Aviv ($19\text{ cm}$).
  - **December 2013 (Storm Alexa)**: Deep Cyprus Low dropped **$40\text{--}80\text{ cm}$** of snow, paralyzing Highways 1 and 443 for 72 hours.
* **Persian Gulf & Arabian Sea Tropical Cyclones**:
  - **June 2007 (Cyclone Gonu)**: Category 5 super cyclonic storm with peak winds of $270\text{ km/h}$; made landfall in Oman causing 50 fatalities and $\$4.2\text{B USD}$ in damages.
  - **October 2021 (Cyclone Shaheen)**: Rare northern Gulf of Oman cyclone striking the Al Batinah coast ($140\text{ km/h}$).
  - **April 2024 Gulf Mega-Storm**: Mesoscale convective storm delivering over $254\text{ mm}$ of rainfall in 24 hours to Dubai and northern Oman.
* **Mediterranean Wildfires & Heat Domes**:
  - **December 2010 Mount Carmel Forest Fire**: 44 fatalities, 17,000 evacuated, 25,000 dunams burned.
  - **July–August 2021 Mediterranean Wildfire Wave**: Over 1,700 square kilometers burned across southern Turkey, coastal Syria, Lebanon, and the Jerusalem Hills.
  - **Summer 2026 Middle East Heat Dome**: Record heat wave with temperatures reaching $50.4^\circ\text{C}$ in Basra, $49.2^\circ\text{C}$ in Kuwait City, and $42.7^\circ\text{C}$ in Jerusalem.

---

## 5. Dataset Validation & Quality Assurance

Both datasets include comprehensive automated validation test suites:

```bash
# Validate Israel Deep Catalog (105 events)
python3 scripts/validate_dataset.py

# Validate Middle East Catalog (182 events across 17 nations)
python3 scripts/validate_middle_east_dataset.py
```

### Validation Results Summary

```
================================================================================
                    NDS-DATA INTEGRATED VALIDATION AUDIT
================================================================================
Catalog: Israel & Jerusalem Deep Dataset
  - Total Events: 105 / 105 valid (100% PASS)
  - Date Range: 759 BCE to 2026 CE
  - Total Recorded Fatalities: 540,683
  - Total Economic Damage: $14,581,000,000 USD
  - Jerusalem Corridor Events: 76 (72.4%)
  - Geospatial Bounding Box: Lat 28.0°N–34.0°N, Lon 33.5°E–37.0°E (100% inside)

Catalog: Pan-Middle East Secondary Dataset
  - Total Events: 182 / 182 valid (100% PASS)
  - Covered Nations: 17 / 17 sovereign states (100% coverage)
  - Total Recorded Fatalities: 1,880,702
  - Total Recorded Injuries: 1,494,981
  - Total Displaced/Evacuated: 11,922,130
  - Total Economic Damage: $210,793,000,000 USD
  - Geospatial Bounding Box: Lat 12.0°N–42.5°N, Lon 25.0°E–65.0°E (100% inside)
================================================================================
```

---

## Interactive Data Explorer (website)

```bash
node server.js --port 6918   # then open http://localhost:6918
```

The root page (`public/index.html`, `public/assets/explorer.{js,css}`) is a dependency-free explorer with one interactive table per dataset: Middle East events, Israel & Jerusalem events, country hazard levels, Jerusalem neighborhoods, lifeline corridors and insurance triggers.

- **Category filters with live counts:** disaster type, country, subregion, district, severity, era, size (death-toll bands) and Jerusalem impact.
- **Range filters:** year (negative = BCE), deaths, economic damage, earthquake magnitude (Mw) and risk scores.
- **Search and table controls:** full-text search with highlighting, sortable columns, a column picker, pagination, and CSV export of the filtered rows.
- **Record details:** click a row for the full record and its sources.
- **Shareable views:** every filter, sort order and page is saved in the URL (e.g. `/#/events?type=Earthquake&mw=7..&sort=-fatalities`).

- **Mobile-friendly:** on phones (≤ 700px) tables become tappable cards, filters open as a full-height sheet with a live "Show N results" button and active-filter badge, sorting moves to a dropdown, and the pager and detail drawer use large touch targets.

The previous map/chart dashboard is still available at `/classic/`.

---

## 6. REST API Reference

The Node.js platform (`server.js`) exposes complete REST API endpoints for both datasets:

### Israel Catalog Endpoints (`/api/*`)
- `GET /api/disasters`: Retrieve events with multi-criteria filtering (`type`, `severity`, `epoch`, `search`, `limit`, `offset`).
- `GET /api/disasters/:id`: Fetch individual event by alphanumeric ID.
- `GET /api/stats/overview`: Aggregate metrics (total events, fatalities, economic loss, type/severity distributions).
- `GET /api/hazards/summary`: ThinkHazard! and NEMA national hazard classifications.
- `GET /api/export/json`: Stream normalized JSON export.
- `GET /api/export/csv`: Stream comma-separated tabular CSV export.

### Middle East Catalog Endpoints (`/api/middle-east/*`)
- `GET /api/middle-east/disasters`: Filter pan-Middle East events (with `country`, `type`, `severity`, `epoch`, `search`).
- `GET /api/middle-east/disasters/:id`: Fetch Middle East event by ID.
- `GET /api/middle-east/stats/overview`: Pan-regional metrics (182 events, 17 nations, 1.88M fatalities, $210.8B loss).
- `GET /api/middle-east/filter-options`: Dynamic lists of covered countries, disaster types, and severity levels.
- `GET /api/middle-east/hazards/summary`: ThinkHazard! multi-hazard risk profiles for all 17 countries.
- `GET /api/middle-east/export/json`: Stream full Middle East JSON catalog.
- `GET /api/middle-east/export/csv`: Stream full Middle East CSV dataset.

---

## 7. Python & Pandas Quickstart

```python
import json
import pandas as pd

# 1. Load Israel Deep Catalog
df_israel = pd.read_csv('data/israel_jerusalem_natural_disasters.csv')
print(f"Israel Catalog: {len(df_israel)} events")
print(df_israel[['year', 'event_name', 'disaster_type', 'fatalities', 'severity_level']].head())

# 2. Load Pan-Middle East Catalog
df_me = pd.read_csv('data/middle_east_natural_disasters.csv')
print(f"Middle East Catalog: {len(df_me)} events across {df_me['country'].nunique()} nations")

# Top 5 deadliest disasters in the Middle East
deadliest = df_me.sort_values(by='fatalities', ascending=False)[['year', 'country', 'event_name', 'disaster_type', 'fatalities']].head(5)
print(deadliest)
```

---

## 8. License & Citation

* **Dataset License**: [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
* **Code License**: MIT License
* **Recommended Citation**:
  > Inbar, M. (Haifa NDI); National Knowledge & Research Center for Emergency Readiness (NKRER); Jerusalem Institute for Policy Research (JIPR); ThinkHazard! (World Bank/GFDRR); EM-DAT (CRED); NOAA NCEI; USGS; IMS; GSI; AFAD; IIEES. *Natural Disasters in Israel and the Middle East Dataset (NDS-data)*, 2026.
