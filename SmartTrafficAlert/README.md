# Smart Traffic & Accident Alert System

Mini project: traffic analysis, accident risk prediction and alerts (simulated data, pure Python + optional Streamlit UI).

## Modules
- `traffic_core.py` - data simulation, traffic analysis (per road/hour), logistic-regression risk model (from scratch), rule-based alerts.
- `main.py` - CLI demo. `app.py` - Streamlit dashboard. `test_core.py` - unit tests.

## Run
```
python3 main.py
python3 -m unittest test_core
pip install -r requirements.txt && streamlit run app.py
```

## How it works
1. Simulate hourly records (volume, speed, weather, night) with accident labels.
2. Analyse congestion and accident rate by road and hour.
3. Train logistic regression (features: volume, speed ratio, night, weather, speeding); risk Low/Medium/High at 12%/30% probability.
4. Alerts: CRITICAL/WARNING/INFO from risk, congestion, speeding, weather, night.

Limitations: synthetic data; not for real-world safety use. Future: real datasets, live APIs, SMS/app notifications, map view.
