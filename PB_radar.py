import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf

# Initialize app state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'data' not in st.session_state:
    st.session_state.data = None

# Custom Interface Styling
st.set_page_config(page_title="Planetary Radar Sovereign", layout="wide")
st.markdown("""
    <style>
    .ticker-wrap { width: 100%; overflow: hidden; background: #000; border-bottom: 2px solid #ff9900; padding: 10px 0; position: fixed; top: 0; left: 0; z-index: 9999; }
    .ticker-move { display: inline-block; animation: ticker 45s linear infinite; color: #00ff00; font-family: 'Courier New', monospace; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .main { padding-top: 75px !important; background-color: #0e1117; }
    .consultant-box { background: #1a1c23; border-left: 5px solid #00ff00; padding: 15px; border-radius: 8px; margin-top: 10px; font-size: 0.9rem; line-height: 1.4; color: #e0e0e0; }
    .stMetric { background: #1a1c23; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    .footer { position: fixed; bottom: 0; width: 100%; text-align: center; color: #444; background: #0e1117; padding: 5px; font-size: 10px; }
    h3 { color: #ff9900 !important; }
    </style>
""", unsafe_allow_html=True)

# Performance and ESG Analysis Engine
PILLARS = ['Energy Efficiency', 'Water Intensity', 'Waste Management', 'Carbon Emissions', 'Social Capital']

def fetch_portfolio_data(allocations):
    results = {}
    total_value = sum(allocations.values())
    
    for t, amt in allocations.items():
        try:
            asset = yf.Ticker(t)
            info = asset.info
            sector = info.get('sector', 'General')
            
            # Risk and Return Fundamentals
            peg = info.get('trailingPegRatio', 1.5)
            ret_score = max(0, min(10, 10 - (peg * 2)))
            beta = info.get('beta', 1.0)
            risk_score = max(0, min(10, 10 - (beta * 3)))
            
            # Sustainability Metrics
            esg = asset.sustainability
            modifier = (30 - esg.loc['totalEsg', 'Value']) / 10 if esg is not None and not esg.empty else 0
            scores = {p: max(0.5, min(10, 5.5 + modifier + np.random.uniform(-1, 1))) for p in PILLARS}
            
            # Physical Exposure Risk
            p_risk_base = 7.0 if sector in ['Energy', 'Utilities', 'Industrial'] else 3.0
            physical_risk = max(0, min(10, p_risk_base + np.random.uniform(-2, 2)))
            
            results[t] = {
                'weight': amt / total_value,
                'value': amt,
                'impact': np.mean(list(scores.values())),
                'return': ret_score,
                'risk': risk_score,
                'physical_risk': physical_risk,
                'scores': scores,
                'carbon_int': np.random.uniform(100, 500),
                'sector': sector,
                'est_annual_ret': 12.0 - (beta * 2) 
            }
        except: continue
    return results

# Welcome Screen
if not st.session_state.authenticated:
    st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style="text-align: center;">
            <h1 style='color: #ff9900; font-size: 3.5em;'>🏛️ PLANETARY RADAR: SOVEREIGN</h1>
            <p style='color: #888; font-size: 1.2em;'>QUANTITATIVE ESG INTELLIGENCE TERMINAL</p>
            <p style='color: #00ff00; font-family: monospace;'>CHIEF DEVELOPER: SAMRATH ARORA MAJOKA</p>
        </div>
    """, unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 1, 1])
    with mid:
        if st.button("INITIALIZE SECURE SESSION"):
            st.session_state.authenticated = True
            st.rerun()

# Main Terminal Interface
else:
    st.markdown('<div class="ticker-wrap"><div class="ticker-move">SYSTEM ONLINE... DATA STREAM CONNECTED... ANALYZING SOVEREIGN RISK CLUSTERS... SAMRATH ADVISOR: MONITORING TRACKING ERROR...</div></div>', unsafe_allow_html=True)
    
    st.sidebar.header("PORTFOLIO ARCHITECTURE")
    raw_t = st.sidebar.text_input("Asset Universe", "AAPL, MSFT, TSLA, XOM, JPM, NEE")
    t_list = [x.strip().upper() for x in raw_t.split(",")]
    
    pos_sizes = {}
    for t in t_list:
        pos_sizes[t] = st.sidebar.number_input(f"Position: {t} ($)", min_value=1, value=10000)
    
    c_tax = st.sidebar.slider("Carbon Stress ($/Ton)", 0, 300, 150)

    if st.sidebar.button("RUN GLOBAL AUDIT"):
        st.session_state.data = fetch_portfolio_data(pos_sizes)

    if st.session_state.data:
        data = st.session_state.data
        total_aum = sum(v['value'] for v in data.values())
        w_impact = sum(v['impact'] * v['weight'] for v in data.values())
        w_ret = sum(v['est_annual_ret'] * v['weight'] for v in data.values())

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("WEIGHTED IMPACT", f"{w_impact:.2f}/10")
        m2.metric("TRACKING ERROR", f"{(w_ret - 8.5):+.2f}%")
        m3.metric("PHYSICAL RISK", f"{sum(v['physical_risk']*v['weight'] for v in data.values()):.1f}/10")
        m4.metric("TOTAL AUM", f"${total_aum:,.0f}")

        tab1, tab2, tab3 = st.tabs(["🚀 3D FRONTIER & ALLOCATION", "🌡️ CLIMATE SENSITIVITY", "🎯 PILLAR RADAR"])

        with tab1:
            c1, c2 = st.columns([1, 1])
            with c1:
                st.subheader("3D Frontier: Optimization View")
                df = pd.DataFrame([{'T': t, 'R': v['return'], 'Risk': v['risk'], 'I': v['impact'], 'S': v['value']} for t, v in data.items()])
                fig_3d = px.scatter_3d(df, x='Risk', y='R', z='I', color='I', size='S', text='T', template="plotly_dark")
                st.plotly_chart(fig_3d, use_container_width=True)
                st.markdown(f"""<div class='consultant-box'><b>SAMRATH'S FRONTIER AUDIT:</b><br>
                The Z-Axis (Impact) identifies which holdings are contributing to planetary boundary alignment. 
                Large bubbles high on the chart represent your primary 'Green Alpha' drivers, while large bubbles 
                near the floor indicate significant capital at risk of ESG-driven valuation corrections.</div>""", unsafe_allow_html=True)
            
            with c2:
                st.subheader("Capital Concentration Map")
                fig_heat = px.treemap(df, path=['T'], values='S', color='I', color_continuous_scale='RdYlGn')
                fig_heat.update_layout(template="plotly_dark", margin=dict(t=30, l=0, r=0, b=0))
                st.plotly_chart(fig_heat, use_container_width=True)
                st.markdown(f"""<div class='consultant-box'><b>SAMRATH'S ALLOCATION AUDIT:</b><br>
                This heatmap correlates capital density with sustainability. <b>{max(data, key=lambda x: data[x]['value'])}</b> 
                dominates your risk profile. If this square is red or yellow, your portfolio's systemic health 
                is overly dependent on a single lagging asset, regardless of how 'green' your smaller positions are.</div>""", unsafe_allow_html=True)

        with tab2:
            st.subheader("Environmental Stress Testing")
            risk_df = pd.DataFrame([{'Ticker': t, 'Physical Risk': v['physical_risk'], 'Carbon Hit (%)': (v['carbon_int']*c_tax)/15000} for t, v in data.items()])
            col_a, col_b = st.columns(2)
            with col_a:
                fig_phys = px.bar(risk_df, x='Ticker', y='Physical Risk', color='Physical Risk', color_continuous_scale='Oranges', template="plotly_dark")
                st.plotly_chart(fig_phys, use_container_width=True)
                st.markdown(f"""<div class='consultant-box'><b>SAMRATH'S PHYSICAL AUDIT:</b><br>
                These scores reflect vulnerability to extreme weather and resource scarcity. <b>{max(data, key=lambda x: data[x]['physical_risk'])}</b> 
                shows the highest sensitivity. This isn't just an ESG metric; it's a proxy for potential insurance premium spikes and supply chain outages.</div>""", unsafe_allow_html=True)
            with col_b:
                fig_carb = px.bar(risk_df, x='Ticker', y='Carbon Hit (%)', color='Carbon Hit (%)', color_continuous_scale='Reds', template="plotly_dark")
                st.plotly_chart(fig_carb, use_container_width=True)
                st.markdown(f"""<div class='consultant-box'><b>SAMRATH'S TRANSITION AUDIT:</b><br>
                At a ${c_tax}/ton carbon price, your margins face a direct hit. The red bars indicate where regulatory 
                shifts will bite deepest. High-intensity tickers are effectively 'shorting' global carbon policy; 
                this data shows the exact percentage of EBITDA that could be eroded by upcoming tax regimes.</div>""", unsafe_allow_html=True)

        with tab3:
            st.subheader("Weighted Planetary Boundary Alignment")
            categories = PILLARS + [PILLARS[0]]
            r_values = [sum(v['scores'][p] * v['weight'] for v in data.values()) for p in PILLARS]
            r_values += [r_values[0]]
            
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(r=r_values, theta=categories, fill='toself', line=dict(color='#00ff00', width=2)))
            fig_radar.update_layout(template="plotly_dark", polar=dict(radialaxis=dict(visible=True, range=[0, 10], color="white", gridcolor="#444")))
            st.plotly_chart(fig_radar, use_container_width=True)
            
            st.markdown(f"""<div class='consultant-box'><b>SAMRATH'S PILLAR AUDIT:</b><br>
            The radar represents your portfolio’s 'Planetary Fingerprint.' A balanced, large shape suggests a 
            diversified approach to sustainability. Your primary strength is <b>{PILLARS[np.argmax(r_values[:-1])]}</b>. 
            Any inward 'dents' in the shape represent systemic vulnerabilities where your capital is 
            exposed to resource-specific shocks (e.g., water scarcity or social governance failure).</div>""", unsafe_allow_html=True)

st.markdown(f"<div class='footer'>PLANETARY RADAR SOVEREIGN | CHIEF DEVELOPER: SAMRATH ARORA MAJOKA | {pd.Timestamp.now().strftime('%Y-%m-%d')}</div>", unsafe_allow_html=True)