"""CLI demo: python main.py"""
from traffic_core import (ROADS, analyze_traffic, build_model, generate_alerts,
                          make_observation)

rows, model, metrics = build_model()
print('=== Traffic analysis ===')
for road, s in analyze_traffic(rows)['roads'].items():
    print(f"{road:16} speed={s['avg_speed']:5} km/h  volume={s['avg_volume']}  accident_rate={s['accident_rate']:.1%}")
print('\n=== Model (held-out test) ===')
print(f"accuracy={metrics['accuracy']:.2%} precision={metrics['precision']:.2%} recall={metrics['recall']:.2%}")
print('feature weights:', [(f, round(w, 2)) for f, w in model.importance()])
print('\n=== Sample alerts ===')
for road, hour, weather, vol, spd in [('NH-48 Highway', 23, 'Fog', 0.3, 110), ('Market Street', 18, 'Rain', 1.0, 12), ('Lake Road', 14, 'Clear', 0.4, 42)]:
    obs = make_observation(road, hour, weather, vol, spd)
    p = model.predict_proba(obs)
    level, risk, alerts = generate_alerts(obs, p)
    print(f"\n{road} @ {hour}:00 {weather} -> traffic={level}, risk={risk} ({p:.0%})")
    for sev, msg in alerts:
        print(f"  [{sev}] {msg}")
