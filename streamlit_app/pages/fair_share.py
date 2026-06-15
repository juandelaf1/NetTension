import streamlit as st
import pandas as pd
from utils.data_loader import get_kpis
from utils.calculations import calculate_fair_share_impact
from components.filters import render_sidebar
from components.kpi_card import kpi_row

def render():
    filters = render_sidebar()
    kpis = get_kpis()
    
    impact = calculate_fair_share_impact(
        kpis["cagr_gap"], filters["ott_pct"], 
        filters["capex_relief"], filters["traffic_adj"]
    )
    
    st.markdown("""
    <div class="section-header">
      <h2 class="section-title">Fair Share What-If Simulator</h2>
      <span class="section-subtitle">OTT contribution · CAPEX relief · Traffic growth scenarios</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background:#FFF8E1;padding:1rem;border-radius:8px;border-left:4px solid #F2C811;margin-bottom:1.5rem;">
      <p style="margin:0;font-size:0.9rem;color:#1A1A2E;">
        Use the <b>sidebar sliders</b> to simulate regulatory scenarios. Adjust OTT contribution percentage,
        CAPEX relief from network sharing, and expected future traffic growth.
        <a href="https://berec.europa.eu" target="_blank">BEREC report</a> on Fair Share (2025).
      </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">🎯 Scenario Impact</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("CAGR Gap", f"{kpis['cagr_gap']:.1%}", 
                  delta="Current divergence", delta_color="off")
    with col2:
        st.metric("Gap Closed", f"{impact['gap_closed_pp']:.1f} pp",
                  delta=f"{filters['ott_pct']*100:.0f}% OTT contribution", delta_color="normal")
    with col3:
        st.metric("Remaining Gap", f"{impact['remaining_gap_pp']:.1f} pp",
                  delta=f"after OTT + CAPEX relief", delta_color="inverse")
    with col4:
        st.metric("CAPEX Savings", f"{impact['capex_savings_pct']:.0f}%",
                  delta=f"{filters['capex_relief']*100:.0f}% relief factor", delta_color="normal")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📈 Scenario Comparison</div>', unsafe_allow_html=True)
    
    scenarios = pd.DataFrame([
        {"Scenario": "Baseline (no policy)", "Gap pp": kpis["cagr_gap"] * 100, 
         "Closed pp": 0, "Remaining pp": kpis["cagr_gap"] * 100},
        {"Scenario": f"{filters['ott_pct']*100:.0f}% OTT", "Gap pp": kpis["cagr_gap"] * 100,
         "Closed pp": impact["gap_closed_pp"], "Remaining pp": impact["remaining_gap_pp"]},
        {"Scenario": f"OTT + {filters['capex_relief']*100:.0f}% Capex", "Gap pp": kpis["cagr_gap"] * 100,
         "Closed pp": impact["gap_closed_pp"] + impact["capex_savings_pct"],
         "Remaining pp": kpis["cagr_gap"] * 100 - impact["gap_closed_pp"] - impact["capex_savings_pct"]},
    ])
    
    col1, col2 = st.columns([2, 1])
    with col1:
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Gap", x=scenarios["Scenario"], y=scenarios["Gap pp"],
                            marker_color="#C62828", hovertemplate="Gap: %{y:.1f} pp<extra></extra>"))
        fig.add_trace(go.Bar(name="Closed", x=scenarios["Scenario"], y=scenarios["Closed pp"],
                            marker_color="#2E7D32", hovertemplate="Closed: %{y:.1f} pp<extra></extra>"))
        fig.add_trace(go.Bar(name="Remaining", x=scenarios["Scenario"], y=scenarios["Remaining pp"],
                            marker_color="#F2C811", hovertemplate="Remaining: %{y:.1f} pp<extra></extra>"))
        fig.update_layout(barmode="group", height=350, 
                          title_text="Gap Closure by Scenario", 
                          yaxis_title="Percentage Points")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    
    with col2:
        st.markdown("#### Policy Levers")
        st.markdown(f"""
        - **OTT Contribution**: {filters['ott_pct']*100:.0f}%
        - **CAPEX Relief**: {filters['capex_relief']*100:.0f}%
        - **Traffic Adjustment**: {filters['traffic_adj']:+.0%}
        - **Model**: Simplified linear
        - **Reference**: BEREC 2025, ETNO 2025
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">⚠️ Limitations</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.85rem;color:#546E7A;">
      <p>This is a simplified model based on public data (ETNO State of Digital Comms 2025, BEREC report).
      Real outcomes depend on regulatory implementation, market structure, and operator behavior.
      The model assumes linear relationships for transparency.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)