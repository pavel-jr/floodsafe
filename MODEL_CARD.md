# FloodSafe prototype

This repository now includes a trained ML baseline and a runnable map dashboard. The supplied files cannot support a supervised contamination predictor: none contains drinking-water samples, contamination outcomes, or aligned rainfall and infrastructure measurements. No contamination labels were fabricated.

## Run

From this folder:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m floodsafe.model
.venv/bin/streamlit run app.py
```

The current workspace already has the virtual environment and trained artifact.

## What is learned

A regularized multiclass logistic regression predicts the catalog's overall flood severity (Moderate, High, Very High, Catastrophic), conditional on an assumed flood event. Inputs: coordinates, calendar month, country and flood type. It excludes casualties, damage, summaries and response narratives because they describe outcomes. Only Flash Flood and River Flood records are included; cyclones and other hazards are excluded.

The two CSV catalogs overlap. Israel IDs are normalized before deduplication, with the regional catalog retained first. All records before 2018 train the evaluation model, and all records from 2018 onward form the chronological test set. The majority-class classifier is evaluated on the same split. Model settings are fixed; no tuning uses the test set. The final saved pipeline is subsequently refitted on all flood records, so reported test metrics describe the earlier evaluation fit rather than a new independent test of the saved fit.

See `artifacts/metrics.json` for measured results and source hashes, `artifacts/holdout_predictions.csv` for every test prediction and `artifacts/training_flood_events.csv` for deduplicated inputs. A small curated disaster catalog is not representative of all flood events. Individual event IDs are deduplicated; separate IDs associated with the same regional weather system may still be correlated. Geographic generalization has not been tested. National hazard profiles are descriptive reference material and are not training features.

## What is simulated

The dashboard has twelve approximate Israeli locations with invented flood exposure, sewage exposure, water-source vulnerability and pipe vulnerability. The sampling-priority index is an assumed rule:

```
F = min(100, initial_flood_exposure * scenario_multiplier)
priority = (0.35*F + 0.30*S + 0.20*W + 0.15*P) * F/100
```

All factors use a 0–100 scale. The exposure gate ensures zero flood exposure produces zero flood-related priority. Thresholds are illustrative: Lower <=30, Elevated >30–60, High >60. This index is not an ML output or a probability. The historical ML output is shown separately and never used as a contamination label. The rainfall multiplier represents an assumption; the historical dataset has no consistent rainfall feature from which a rainfall response can be learned. Internet access is required for map basemap tiles.

## Data needed for contamination ML

`templates/water_quality_training.csv` provides a header-only acquisition schema. Collect timestamped samples across regions and flood events, including uncontaminated samples. Define the target explicitly, for example whether an independently specified laboratory threshold is exceeded in the 24 hours after prediction. Preserve sample units, lab detection limits, source provenance and prediction timestamps. All input features must be available at prediction time; outcome measurements must come later. Group validation by flood event, reserve future events, and assess generalization to held-out regions. Avoid repeated samples of the same event crossing splits. The existing severity classifier cannot substitute for these labels.

## Checks

```sh
.venv/bin/python -m unittest discover -s tests -v
```

Checks cover deduplication, outcome-feature exclusion, zero-exposure and monotonic scenario behavior, saved-model inference and Streamlit interaction without exceptions. These are software checks, not scientific validation of contamination forecasting.

## Batch ML inference

```sh
.venv/bin/python -m floodsafe.predict templates/prediction_input.csv artifacts/example_predictions.csv
```

The example locations are scenario inputs. Outputs are historical flood severity categories, never contamination forecasts.

## Initial measured performance

There are 38 unique flood events: 21 before 2018 and 17 from 2018 onward. Held-out accuracy is 29.4% versus 23.5% for the majority baseline; macro F1 is 0.185 versus 0.095. This is weak performance, with no correctly classified Moderate or Very High test examples. The available data do not establish useful operational predictive skill. No contamination accuracy can be measured because contamination outcomes are absent.

## GitHub Pages version

`docs/` contains a static dashboard with Leaflet/OpenStreetMap and JavaScript inference from exported model coefficients. Regenerate `docs/data.json` after training with `.venv/bin/python export_web.py`. Browser inference was compared with Python across 288 combinations of location, month and flood type; all predicted classes matched. Scenario scores were also checked against Python.

The Pages workflow publishes only `docs/`. Configure repository Pages source as GitHub Actions. The intended public repository is `pavel-jr/floodsafe`. Local static preview: `python3 -m http.server 8502 --directory docs`.
