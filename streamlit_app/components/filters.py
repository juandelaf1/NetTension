import streamlit as st
from utils.data_loader import load_fact_observed

LABELS = {
    "es": {
        "period": "Periodo",
        "year": "Año",
        "fair_share": "Simulador Fair Share",
        "ott": "Contribución OTT %",
        "capex": "Reducción CAPEX %",
        "traffic": "Ajuste Tráfico %",
        "legend": "NetTension v1.0 • CNMC + Eurostat • Jun 2026",
    },
    "en": {
        "period": "Period",
        "year": "Year",
        "fair_share": "Fair Share Simulator",
        "ott": "OTT Contribution %",
        "capex": "CAPEX Relief %",
        "traffic": "Traffic Adjustment %",
        "legend": "NetTension v1.0 • CNMC + Eurostat • Jun 2026",
    },
}

def render_sidebar(lang=None) -> dict:
    if lang is None:
        lang = st.session_state.get("lang", "es")
    labels = LABELS.get(lang, LABELS["es"])
    L = lang
    help_period = "Filtra el periodo de análisis" if L == "es" else "Filter the analysis period"
    help_ott = "% de contribución OTT a costes de red" if L == "es" else "% OTT contribution to network costs"
    help_capex = "% reducción CAPEX por eficiencias" if L == "es" else "% CAPEX reduction through efficiencies"
    help_traffic = "Ajuste crecimiento tráfico futuro (puntos porcentuales)" if L == "es" else "Traffic growth adjustment (percentage points)"

    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown(f'<div class="sidebar-title">📅 {labels["period"]}</div>', unsafe_allow_html=True)

        fact = load_fact_observed()
        years = sorted(fact["year"].unique())
        year_range = st.slider(
            labels["year"],
            min_value=min(years),
            max_value=max(years),
            value=(min(years), max(years)),
            step=1,
            key="slider_year",
            help=help_period,
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown(f'<div class="sidebar-title">⚙️ {labels["fair_share"]}</div>', unsafe_allow_html=True)
        ott_pct = st.slider(
            labels["ott"],
            0, 50, 15, 1,
            key="slider_ott",
            help=help_ott,
        ) / 100
        capex_relief = st.slider(
            labels["capex"],
            0, 50, 20, 1,
            key="slider_capex",
            help=help_capex,
        ) / 100
        traffic_adj = st.slider(
            labels["traffic"],
            -30, 30, 0, 1,
            key="slider_traffic",
            help=help_traffic,
        ) / 100
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.caption(labels["legend"])

        return {
            "year_range": year_range,
            "ott_pct": ott_pct,
            "capex_relief": capex_relief,
            "traffic_adj": traffic_adj,
        }
