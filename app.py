from pathlib import Path
import joblib
import pandas as pd
import streamlit as st
from floodsafe.model import FEATURES
from floodsafe.scenario import demo_locations, score_locations, WEIGHTS

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title='FloodSafe', page_icon='💧', layout='wide')
st.title('FloodSafe')
st.caption('Flood investigation planning prototype · SIMULATED CONTAMINATION PRIORITIES')
st.warning('No contamination observations exist in the supplied data. The map shows an assumed sampling-priority index, not measured contamination, safety advice, or a 24-hour forecast.')
path = ROOT / 'artifacts/flood_severity.joblib'
if not path.exists():
    st.error('Train the model first: python -m floodsafe.model')
    st.stop()
bundle = joblib.load(path)
with st.sidebar:
    st.header('Simulated flood scenario')
    rainfall = st.slider('Rainfall / flood exposure multiplier (assumption)', 0., 2., 1., .05)
    month = st.selectbox('Event month (historical ML input)', list(range(1,13)), index=9)
    st.caption('Rainfall changes the assumed priority score. The ML model has no rainfall training data.')
ranked = score_locations(demo_locations(), rainfall)
a,b,c = st.columns(3)
a.metric('High-priority demo locations', int((ranked.tier == 'High').sum()))
b.metric('Locations monitored', len(ranked))
c.metric('Unique historical flood events', bundle['report']['unique_flood_events'])
left,right = st.columns([1.5,1])
with left:
    colors = {'High':'#dc2626','Elevated':'#f59e0b','Lower':'#16a34a'}
    points = ranked.assign(color=ranked.tier.astype(str).map(colors), size=ranked.priority_score*6+100)
    st.map(points, latitude='latitude', longitude='longitude', color='color', size='size')
    st.caption('Red: >60 · Amber: >30–60 · Green: 0–30. Illustrative thresholds. Select a location below to inspect it.')
with right:
    name = st.selectbox('Inspect a location', ranked.location.tolist())
    row = ranked[ranked.location == name].iloc[0]
    st.subheader(f'{name} — {row.tier} priority')
    st.metric('Assumed sampling-priority index / 100', row.priority_score)
    st.bar_chart(pd.DataFrame({'Scenario factors (0–100)': {k: row[k] for k in WEIGHTS}}))
    st.write('Suggested demo action: prioritise sampling and inspect exposed infrastructure.' if row.tier == 'High' else 'Suggested demo action: consider this location in the sampling plan.')
    st.caption('All sewage, source, pipe and flood-exposure values are invented for this demonstration.')
st.subheader('Sampling queue — simulated')
st.dataframe(ranked[['location','priority_score','tier', *WEIGHTS]], hide_index=True, width='stretch')
st.download_button('Download scenario CSV', ranked.to_csv(index=False), 'simulated_sampling_priorities.csv', 'text/csv')
with st.expander('Historical ML model: separate flood-severity estimate and evaluation', expanded=True):
    hazard = st.selectbox('Assumed flood type for selected location', ['Flash Flood','River Flood'])
    inputs = pd.DataFrame([dict(latitude=row.latitude, longitude=row.longitude, month=month, country='Israel', disaster_type=hazard)])
    predicted = bundle['pipeline'].predict(inputs[FEATURES])[0]
    st.write(f'Historical classifier output for {name}: **{predicted} flood severity** (conditional on a flood).')
    st.caption('This output is independent of the simulated priority score. It does not predict contamination or flood occurrence.')
    report = bundle['report']
    st.write(f"Chronological holdout: {report['train_events']} training events, {report['test_events']} test events.")
    st.dataframe(pd.DataFrame({k: {m:v for m,v in report[k].items() if m in ['accuracy','balanced_accuracy','macro_f1']} for k in ['model','majority_baseline']}))
    st.json(report)
