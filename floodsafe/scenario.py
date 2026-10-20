"""Explicitly assumed contamination sampling priorities, not learned outcomes."""
import pandas as pd

WEIGHTS = {'flood_exposure': .35, 'sewage_exposure': .30,
           'water_vulnerability': .20, 'pipe_vulnerability': .15}


def demo_locations():
    # Coordinates are approximate real locations. Every vulnerability value is invented.
    rows = [
        ('Nahariya',33.005,35.095,90,85,70,75), ('Haifa',32.794,34.99,65,70,55,65),
        ('Tiberias',32.795,35.531,75,60,85,60), ('Afula',32.609,35.289,70,65,70,60),
        ('Hadera',32.434,34.919,80,80,75,70), ('Netanya',32.321,34.853,65,60,60,65),
        ('Tel Aviv',32.085,34.782,85,90,65,85), ('Ashdod',31.804,34.655,75,70,65,70),
        ('Jerusalem',31.768,35.214,40,45,60,55), ('Beersheba',31.252,34.791,55,50,60,50),
        ('Ein Gedi',31.45,35.384,95,30,80,40), ('Eilat',29.558,34.952,65,35,55,40)]
    return pd.DataFrame(rows, columns=['location','latitude','longitude', *WEIGHTS])


def score_locations(locations, rainfall_multiplier=1.):
    if not 0 <= rainfall_multiplier <= 2:
        raise ValueError('Rainfall multiplier must be between 0 and 2')
    out = locations.copy()
    for name in WEIGHTS:
        if not out[name].between(0,100).all():
            raise ValueError(f'{name} must be between 0 and 100')
    out['flood_exposure'] = (out.flood_exposure * rainfall_multiplier).clip(0,100)
    # Exposure gates the score: a zero-flood scenario must not create flood-related alerts.
    contribution = pd.DataFrame({k: out[k]*w for k,w in WEIGHTS.items()})
    out['priority_score'] = (contribution.sum(axis=1) * out.flood_exposure / 100).round(1)
    out['tier'] = pd.cut(out.priority_score, [-1,30,60,100], labels=['Lower','Elevated','High'])
    out['main_driver'] = contribution.idxmax(axis=1)
    return out.sort_values('priority_score', ascending=False).reset_index(drop=True)
