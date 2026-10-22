"""Smart Traffic & Accident Alert System - core logic (pure Python, no dependencies).

Pipeline: simulate data -> traffic analysis -> accident risk model (logistic
regression trained with gradient descent) -> rule-based alerts.
All data is SIMULATED; this is an educational prototype.
"""
import math
import random
from collections import defaultdict

ROADS = {
    'NH-48 Highway': {'limit': 90, 'lanes': 3},
    'City Square': {'limit': 40, 'lanes': 2},
    'Lake Road': {'limit': 50, 'lanes': 2},
    'Market Street': {'limit': 30, 'lanes': 1},
    'University Gate': {'limit': 40, 'lanes': 2},
}
WEATHER = ['Clear', 'Rain', 'Fog']
WEATHER_RISK = {'Clear': 0.0, 'Rain': 1.0, 'Fog': 1.4}
FEATURES = ['volume_ratio', 'speed_ratio', 'night', 'weather_risk', 'speeding']


def _risk_probability(volume_ratio, speed_ratio, night, weather_risk, speeding):
    """Hidden 'ground truth' used only to generate synthetic accident labels."""
    z = (-4.2 + 1.6 * volume_ratio + 1.2 * (1 - speed_ratio) + 1.1 * night
         + 0.9 * weather_risk + 1.8 * speeding)
    return 1 / (1 + math.exp(-z))


def generate_data(n=3000, seed=42):
    """Create simulated hourly road records with an accident label (0/1)."""
    rng = random.Random(seed)
    rows = []
    for _ in range(n):
        road = rng.choice(list(ROADS))
        info = ROADS[road]
        hour = rng.randrange(24)
        peak = hour in (8, 9, 10, 17, 18, 19, 20)
        night = 1 if hour >= 22 or hour <= 5 else 0
        weather = rng.choices(WEATHER, [0.65, 0.22, 0.13])[0]
        base = 0.85 if peak else (0.15 if night else 0.45)
        volume_ratio = max(0.02, min(1.4, rng.gauss(base, 0.15)))
        free = info['limit'] * (0.9 if night else 0.85)
        slow = (1 - 0.55 * min(volume_ratio, 1.2)) * (1 - 0.15 * WEATHER_RISK[weather])
        speed = max(5, rng.gauss(free * slow, 4) + (12 if night else 0))
        speed_ratio = speed / info['limit']
        speeding = 1 if speed_ratio > 1.0 else 0
        p = _risk_probability(volume_ratio, speed_ratio, night, WEATHER_RISK[weather], speeding)
        rows.append({'road': road, 'hour': hour, 'weather': weather,
                     'volume_ratio': round(volume_ratio, 3), 'speed': round(speed, 1),
                     'speed_ratio': round(speed_ratio, 3), 'night': night,
                     'weather_risk': WEATHER_RISK[weather], 'speeding': speeding,
                     'accident': 1 if rng.random() < p else 0})
    return rows


def congestion_level(volume_ratio, speed_ratio):
    score = 0.6 * volume_ratio + 0.4 * (1 - min(speed_ratio, 1))
    if score < 0.35:
        return 'Low'
    if score < 0.6:
        return 'Moderate'
    return 'Heavy'


def analyze_traffic(rows):
    """Per-road and per-hour aggregates for the dashboard."""
    by_road, by_hour = defaultdict(list), defaultdict(list)
    for r in rows:
        by_road[r['road']].append(r)
        by_hour[r['hour']].append(r)

    def avg(xs):
        return sum(xs) / len(xs) if xs else 0.0
    roads = {k: {'avg_speed': round(avg([r['speed'] for r in v]), 1),
                 'avg_volume': round(avg([r['volume_ratio'] for r in v]), 2),
                 'accident_rate': round(avg([r['accident'] for r in v]), 3),
                 'records': len(v)} for k, v in by_road.items()}
    hours = {h: {'avg_volume': round(avg([r['volume_ratio'] for r in v]), 2),
                 'accident_rate': round(avg([r['accident'] for r in v]), 3)}
             for h, v in sorted(by_hour.items())}
    return {'roads': roads, 'hours': hours}


class RiskModel:
    """Logistic regression with standardised features, trained by gradient descent."""

    def __init__(self):
        self.w = [0.0] * len(FEATURES)
        self.b = 0.0
        self.mu = [0.0] * len(FEATURES)
        self.sd = [1.0] * len(FEATURES)

    @staticmethod
    def _x(row):
        return [row[f] for f in FEATURES]

    def _norm(self, x):
        return [(v - m) / s for v, m, s in zip(x, self.mu, self.sd)]

    def fit(self, rows, epochs=300, lr=0.3):
        X = [self._x(r) for r in rows]
        n = len(X)
        self.mu = [sum(c) / n for c in zip(*X)]
        self.sd = [max(1e-9, math.sqrt(sum((v - m) ** 2 for v in c) / n))
                   for c, m in zip(zip(*X), self.mu)]
        Xn = [self._norm(x) for x in X]
        y = [r['accident'] for r in rows]
        for _ in range(epochs):
            gw, gb = [0.0] * len(self.w), 0.0
            for xi, yi in zip(Xn, y):
                err = self._sigmoid(sum(w * v for w, v in zip(self.w, xi)) + self.b) - yi
                for j, v in enumerate(xi):
                    gw[j] += err * v
                gb += err
            self.w = [w - lr * g / n for w, g in zip(self.w, gw)]
            self.b -= lr * gb / n
        return self

    @staticmethod
    def _sigmoid(z):
        z = max(-35, min(35, z))
        return 1 / (1 + math.exp(-z))

    def predict_proba(self, row):
        xn = self._norm(self._x(row))
        return self._sigmoid(sum(w * v for w, v in zip(self.w, xn)) + self.b)

    def evaluate(self, rows, threshold=0.30):
        tp = fp = tn = fn = 0
        for r in rows:
            pred = self.predict_proba(r) >= threshold
            if pred and r['accident']:
                tp += 1
            elif pred:
                fp += 1
            elif r['accident']:
                fn += 1
            else:
                tn += 1
        total = max(1, tp + fp + tn + fn)
        return {'accuracy': (tp + tn) / total,
                'precision': tp / (tp + fp) if tp + fp else 0.0,
                'recall': tp / (tp + fn) if tp + fn else 0.0,
                'confusion': {'tp': tp, 'fp': fp, 'tn': tn, 'fn': fn}}

    def importance(self):
        return sorted(zip(FEATURES, self.w), key=lambda t: -abs(t[1]))


def train_test_split(rows, test_ratio=0.25, seed=1):
    rows = rows[:]
    random.Random(seed).shuffle(rows)
    k = int(len(rows) * (1 - test_ratio))
    return rows[:k], rows[k:]


def risk_label(p):
    return 'High' if p >= 0.30 else 'Medium' if p >= 0.12 else 'Low'


def make_observation(road, hour, weather, volume_ratio, speed):
    info = ROADS[road]
    sr = speed / info['limit']
    return {'road': road, 'hour': hour, 'weather': weather, 'volume_ratio': volume_ratio,
            'speed': speed, 'speed_ratio': sr,
            'night': 1 if hour >= 22 or hour <= 5 else 0,
            'weather_risk': WEATHER_RISK[weather], 'speeding': 1 if sr > 1 else 0}


def generate_alerts(obs, probability):
    """Rule-based alerts from a live/simulated observation and the model risk."""
    alerts = []
    level = congestion_level(obs['volume_ratio'], obs['speed_ratio'])
    risk = risk_label(probability)
    if risk == 'High':
        alerts.append(('CRITICAL', f"High accident risk ({probability:.0%}) on {obs['road']}. Slow down and keep distance."))
    elif risk == 'Medium':
        alerts.append(('WARNING', f"Moderate accident risk ({probability:.0%}) on {obs['road']}. Drive carefully."))
    if level == 'Heavy':
        alerts.append(('WARNING', f"Heavy congestion on {obs['road']}. Consider an alternate route."))
    if obs['speeding']:
        alerts.append(('WARNING', f"Average speed {obs['speed']:.0f} km/h exceeds limit {ROADS[obs['road']]['limit']} km/h."))
    if obs['weather'] != 'Clear':
        alerts.append(('INFO', f"{obs['weather']} reduces visibility/grip. Reduce speed."))
    if obs['night']:
        alerts.append(('INFO', 'Night-time driving: stay alert, use headlights.'))
    if not alerts:
        alerts.append(('INFO', f"Roads look safe on {obs['road']}. Traffic: {level}."))
    return level, risk, alerts


def build_model(seed=42):
    rows = generate_data(seed=seed)
    train, test = train_test_split(rows)
    model = RiskModel().fit(train)
    return rows, model, model.evaluate(test)
