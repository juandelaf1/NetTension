import streamlit as st
from utils.data_loader import load_fact_observed

def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">📅 Periodo</div>', unsafe_allow_html=True)
        
        fact = load_fact_observed()
        years = sorted(fact["year"].unique())
        year_range = st.slider("Año", min_value=min(years), max_value=max(years), value=(min(years), max(years)), step=1)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">🏢 Operadores</div>', unsafe_allow_html=True)
        
        operator_groups = ["All", "Incumbent", "Competitor", "Regional", "Other"]
        selected_groups = st.multiselect("Grupo", operator_groups, default=["All"])
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">⚙️ Fair Share Simulator</div>', unsafe_allow_html=True)
        
        ott_pct = st.slider("OTT Contribution %", 0, 50, 15, 1, help="% de contribución OTT a costes de red") / 100
        capex_relief = st.slider("CAPEX Relief %", 0, 50, 20, 1, help="% reducción CAPEX por eficiencias") / 100
        traffic_adj = st.slider("Traffic Growth Adj.", -30, 30, 0, 1, help="Ajuste crecimiento tráfico futuro (pp)") / 100
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.caption("NetTension v1.0 • Data: CNMC + Eurostat • Jun 2026")
        
        return {
            "year_range": year_range,
            "operator_groups": selected_groups,
            "ott_pct": ott_pct,
            "capex_relief": capex_relief,
            "traffic_adj": traffic_adj,
        }