import streamlit as st
from traffic_core import (ROADS, WEATHER, analyze_traffic, build_model,
                          generate_alerts, make_observation)

st.set_page_config(page_title='Smart Traffic & Accident Alert', page_icon='🚦', layout='wide')
st.title('🚦 Smart Traffic & Accident Alert System')
st.warning('Educational prototype: all data is simulated, not live traffic.')


@st.cache_resource
def load():
    return build_model()


rows, model, metrics = load()
an = analyze_traffic(rows)
tab1, tab2, tab3 = st.tabs(['Traffic analysis', 'Risk & alerts', 'Model'])
with tab1:
    st.subheader('Per-road summary')
    st.dataframe([{'road': k, **v} for k, v in an['roads'].items()])
    st.subheader('Average volume by hour')
    st.line_chart({h: v['avg_volume'] for h, v in an['hours'].items()})
    st.subheader('Accident rate by hour')
    st.bar_chart({h: v['accident_rate'] for h, v in an['hours'].items()})
with tab2:
    c1, c2 = st.columns(2)
    road = c1.selectbox('Road', list(ROADS))
    hour = c1.slider('Hour', 0, 23, 18)
    weather = c1.selectbox('Weather', WEATHER)
    vol = c2.slider('Traffic volume (capacity ratio)', 0.0, 1.4, 0.7)
    spd = c2.slider('Average speed (km/h)', 5, 130, 35)
    obs = make_observation(road, hour, weather, vol, float(spd))
    p = model.predict_proba(obs)
    level, risk, alerts = generate_alerts(obs, p)
    m1, m2, m3 = st.columns(3)
    m1.metric('Congestion', level)
    m2.metric('Accident risk', risk)
    m3.metric('Probability', f'{p:.0%}')
    for sev, msg in alerts:
        {'CRITICAL': st.error, 'WARNING': st.warning}.get(sev, st.info)(msg)
with tab3:
    st.write(f"Accuracy {metrics['accuracy']:.1%} · Precision {metrics['precision']:.1%} · Recall {metrics['recall']:.1%}")
    st.json(metrics['confusion'])
    st.bar_chart({f: w for f, w in model.importance()})
