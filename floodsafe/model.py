"""Historical flood severity classifier; NOT a contamination predictor."""
from pathlib import Path
import json
import hashlib
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, confusion_matrix

ROOT = Path(__file__).resolve().parents[1]
FEATURES = ['latitude', 'longitude', 'month', 'country', 'disaster_type']
NUMERIC = ['latitude', 'longitude', 'month']
CATEGORICAL = ['country', 'disaster_type']
LABELS = ['Moderate', 'High', 'Very High', 'Catastrophic']


def load_floods(root=ROOT):
    frames = []
    for name in ['middle_east_natural_disasters.csv', 'israel_jerusalem_natural_disasters.csv']:
        df = pd.read_csv(root / name)
        if 'country' not in df:
            df['country'] = 'Israel'
        df['source_file'] = name
        frames.append(df)
    data = pd.concat(frames, ignore_index=True)
    data['canonical_id'] = data['id'].str.replace(r'^ME-(?=ISR-)', '', regex=True)
    data = data.drop_duplicates('canonical_id')
    data = data[data.disaster_type.isin(['Flash Flood', 'River Flood'])].copy()
    data['month'] = pd.to_numeric(data.date_start.str.slice(5, 7), errors='coerce')
    if not data.severity_level.isin(LABELS).all():
        raise ValueError('Unknown severity target')
    return data.sort_values(['year', 'date_start', 'canonical_id']).reset_index(drop=True)


def make_model():
    numeric = Pipeline([('impute', SimpleImputer(strategy='median')), ('scale', StandardScaler())])
    categorical = Pipeline([('impute', SimpleImputer(strategy='most_frequent')),
                            ('encode', OneHotEncoder(handle_unknown='ignore'))])
    return Pipeline([('features', ColumnTransformer([('numeric', numeric, NUMERIC),
                                                     ('categorical', categorical, CATEGORICAL)])),
                     ('model', LogisticRegression(C=0.3, max_iter=2000, random_state=42))])


def metrics(y, pred):
    return {'accuracy': float(accuracy_score(y, pred)),
            'balanced_accuracy': float(balanced_accuracy_score(y, pred)),
            'macro_f1': float(f1_score(y, pred, labels=LABELS, average='macro', zero_division=0)),
            'confusion_matrix_labels': LABELS,
            'confusion_matrix': confusion_matrix(y, pred, labels=LABELS).tolist()}


def train(root=ROOT):
    data = load_floods(root)
    # Hold out complete calendar years; never randomly split overlapping catalog rows.
    train_df, test_df = data[data.year < 2018], data[data.year >= 2018]
    if len(train_df) < 8 or len(test_df) < 4:
        raise ValueError('Insufficient records for the fixed chronological evaluation')
    model = make_model().fit(train_df[FEATURES], train_df.severity_level)
    baseline = DummyClassifier(strategy='most_frequent').fit(train_df[FEATURES], train_df.severity_level)
    report = {
        'task': 'Historical flood-event severity classification, conditional on a flood occurring',
        'not_supported': ['drinking-water contamination prediction', '24-hour forecasts', 'flood occurrence probability'],
        'unique_flood_events': len(data), 'train_events': len(train_df), 'test_events': len(test_df),
        'split': 'Train years < 2018; test years >= 2018; duplicate Israel catalog IDs removed',
        'features': FEATURES, 'target': 'severity_level',
        'class_counts': data.severity_level.value_counts().to_dict(),
        'model': metrics(test_df.severity_level, model.predict(test_df[FEATURES])),
        'majority_baseline': metrics(test_df.severity_level, baseline.predict(test_df[FEATURES])),
        'limitations': ['Small, curated disaster-only sample; no non-event controls.',
                       'Severity labels describe overall disaster impact, not contamination.',
                       'No rainfall, flood depth, sewage proximity, water infrastructure or laboratory outcomes.',
                       'Catalog source claims were not independently verified.',
                       'Geographic transfer and probability calibration have not been validated.',
                       'Current hazard profiles excluded to avoid retrospective information leakage.'],
        'source_sha256': {name: hashlib.sha256((root/name).read_bytes()).hexdigest() for name in
                          ['middle_east_natural_disasters.csv', 'israel_jerusalem_natural_disasters.csv']}}
    output = root / 'artifacts'
    output.mkdir(exist_ok=True)
    holdout = test_df[['canonical_id', 'year', 'severity_level']].copy()
    holdout['predicted_severity'] = model.predict(test_df[FEATURES])
    holdout.to_csv(output / 'holdout_predictions.csv', index=False)
    # Refit deployment artifact only after recording untouched holdout evaluation.
    model.fit(data[FEATURES], data.severity_level)
    joblib.dump({'pipeline': model, 'features': FEATURES, 'report': report}, output / 'flood_severity.joblib')
    (output / 'metrics.json').write_text(json.dumps(report, indent=2))
    data.to_csv(output / 'training_flood_events.csv', index=False)
    return report


if __name__ == '__main__':
    print(json.dumps(train(), indent=2))
