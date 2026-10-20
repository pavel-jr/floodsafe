"""Export the fitted linear classifier and demo scenarios for static hosting."""
import json
import joblib
from floodsafe.model import ROOT
from floodsafe.scenario import demo_locations

bundle = joblib.load(ROOT/'artifacts/flood_severity.joblib')
pre = bundle['pipeline'].named_steps['features']
model = bundle['pipeline'].named_steps['model']
num = pre.named_transformers_['numeric']
cat = pre.named_transformers_['categorical'].named_steps['encode']
data = dict(locations=demo_locations().to_dict(orient='records'), report=bundle['report'],
            model=dict(mean=num.named_steps['scale'].mean_.tolist(),
                       scale=num.named_steps['scale'].scale_.tolist(),
                       categories=[v.tolist() for v in cat.categories_],
                       coefficients=model.coef_.tolist(), intercept=model.intercept_.tolist(),
                       classes=model.classes_.tolist()))
(ROOT/'docs/data.json').write_text(json.dumps(data, indent=2))
