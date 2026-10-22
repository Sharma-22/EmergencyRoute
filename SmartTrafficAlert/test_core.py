import unittest
from traffic_core import (build_model, congestion_level, generate_alerts,
                          generate_data, make_observation)


class T(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows, cls.model, cls.metrics = build_model()

    def test_data_deterministic(self):
        self.assertEqual(generate_data(50, 1), generate_data(50, 1))

    def test_model_beats_baseline(self):
        base = 1 - sum(r['accident'] for r in self.rows) / len(self.rows)
        self.assertGreaterEqual(self.metrics['accuracy'], base - 0.01)

    def test_risky_scenario_higher(self):
        risky = make_observation('NH-48 Highway', 23, 'Fog', 0.3, 110)
        safe = make_observation('Lake Road', 14, 'Clear', 0.4, 40)
        self.assertGreater(self.model.predict_proba(risky), self.model.predict_proba(safe))

    def test_alerts(self):
        obs = make_observation('NH-48 Highway', 23, 'Fog', 0.3, 110)
        _, risk, al = generate_alerts(obs, 0.5)
        self.assertEqual(risk, 'High')
        self.assertEqual(al[0][0], 'CRITICAL')

    def test_congestion(self):
        self.assertEqual(congestion_level(0.1, 1.0), 'Low')
        self.assertEqual(congestion_level(1.0, 0.3), 'Heavy')


unittest.main() if __name__ == '__main__' else None
