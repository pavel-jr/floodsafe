import unittest
import joblib
from streamlit.testing.v1 import AppTest
from floodsafe.model import ROOT, FEATURES, load_floods
from floodsafe.scenario import demo_locations, score_locations


class PipelineTests(unittest.TestCase):
    def test_no_duplicate_events_or_nonfloods(self):
        data = load_floods()
        self.assertTrue(data.canonical_id.is_unique)
        self.assertEqual(set(data.disaster_type), {'Flash Flood','River Flood'})
        self.assertFalse(set(FEATURES) & {'summary','fatalities','severity_level','emergency_response'})

    def test_scenario_monotonic_and_zero(self):
        low = score_locations(demo_locations(), 0).set_index('location').sort_index()
        middle = score_locations(demo_locations(), 1).set_index('location').sort_index()
        high = score_locations(demo_locations(), 2).set_index('location').sort_index()
        self.assertTrue((low.priority_score == 0).all())
        self.assertTrue((high.priority_score >= middle.priority_score).all())
        self.assertTrue(high.priority_score.between(0,100).all())
        with self.assertRaises(ValueError):
            score_locations(demo_locations(), -1)

    def test_artifact_and_unknown_country(self):
        bundle = joblib.load(ROOT / 'artifacts/flood_severity.joblib')
        x = load_floods()[FEATURES].head(1).copy()
        x['country'] = 'Unseen'
        self.assertEqual(len(bundle['pipeline'].predict(x)),1)

    def test_dashboard_and_scenario_change(self):
        app = AppTest.from_file(str(ROOT/'app.py')).run(timeout=30)
        self.assertEqual(len(app.exception),0)
        app.slider[0].set_value(0.).run()
        self.assertEqual(len(app.exception),0)
        self.assertEqual(app.metric[0].value,'0')
        app.slider[0].set_value(2.).run()
        self.assertEqual(len(app.exception),0)
        self.assertGreater(int(app.metric[0].value),0)
        next(w for w in app.selectbox if w.label == 'Inspect a location').select('Eilat').run()
        self.assertEqual(len(app.exception),0)


if __name__ == '__main__':
    unittest.main()
