"""Batch historical flood severity inference: python -m floodsafe.predict input.csv output.csv."""
import argparse
import joblib
import pandas as pd
from floodsafe.model import ROOT, FEATURES


def main():
    parser = argparse.ArgumentParser(description='Predict historical flood severity, NOT contamination')
    parser.add_argument('input_csv')
    parser.add_argument('output_csv')
    args = parser.parse_args()
    data = pd.read_csv(args.input_csv)
    missing = set(FEATURES) - set(data.columns)
    if missing:
        parser.error(f'Missing input columns: {sorted(missing)}')
    for column, lower, upper in [('latitude',-90,90),('longitude',-180,180),('month',1,12)]:
        if not pd.to_numeric(data[column], errors='coerce').between(lower,upper).all():
            parser.error(f'{column} must be numeric and between {lower} and {upper}')
        data[column] = pd.to_numeric(data[column])
    if not data.disaster_type.isin(['Flash Flood','River Flood']).all():
        parser.error('disaster_type must be Flash Flood or River Flood')
    model = joblib.load(ROOT/'artifacts/flood_severity.joblib')['pipeline']
    data['predicted_flood_severity'] = model.predict(data[FEATURES])
    data['output_scope'] = 'Historical severity only; not contamination'
    data.to_csv(args.output_csv, index=False)
    print(f'Wrote {len(data)} historical severity predictions to {args.output_csv}')


if __name__ == '__main__':
    main()
