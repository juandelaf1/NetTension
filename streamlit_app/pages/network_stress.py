import streamlit as st
from utils.data_loader import load_fact_observed, load_hhi, filter_by_year, get_kpis
from components.charts import hhi_chart, nsi_vs_arpu_scatter
from components.kpi_card import kpi_row
from components.filters import render_sidebar
from utils.calculations import calculate_network_stress_metrics

def filter_by_hhi_year(hhi_df, year_range):
    yr_min, yr_max = year_range
    return hhi_df[(hhi_df["year"] >= yr_min) & (hhi_df["year"] <= yr_max)]

def render():
    filters = render_sidebar()
    kpis = get_kpis()
    fact = filter_by_year(load_fact_observed(), filters["year_range"])
    hhi = filter_by_hhi_year(load_hhi(), filters["year_range"])
    stress = calculate_network_stress_metrics(fact)
    
    st.markdown("""
    <div class="section-header">
      <h2 class="section-title">Network Stress Analysis</h2>
      <span class="section-subtitle">HHI · NSI · Infrastructure Elasticity</span>
    </div>
    """, unsafe_allow_html=True)
    
    kpi_row([
        dict(label="HHI (2025)", value=f"{kpis['hhi_2025']:.0f}",
             delta=f"{kpis['hhi_delta']:+.0f} vs 2005", delta_color="positive", icon="📊"),
        dict(label="NSI (current)", value=f"{stress['nsi_current']:,.0f}",
             delta=f"{stress['nsi_growth']:.0%} growth", delta_color="negative", icon="📶"),
        dict(label="ARPU (current)", value=f"€{stress['arpu_current']:,.2f}",
             delta=f"{stress['arpu_decline']:.0%} decline", delta_color="negative", icon="💳"),
        dict(label="Active Lines", value=f"{stress['lines_current']:,.0f}",
             delta="total accesses", delta_color="neutral", icon="📡"),
    ])
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📊 HHI Trend with Concentration Bands</div>', unsafe_allow_html=True)
        fig1 = hhi_chart(hhi)
        st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})
        st.markdown("""
        <div style="display:flex;gap:1rem;font-size:0.8rem;color:#546E7A;">
          <span>HHI 2005: <b>3,482</b> (Highly Concentrated)</span>
          <span>HHI 2025: <b>2,368</b> (Moderate)</span>
          <span>Change: <b>-1,114</b> (deconcentration)</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🎯 NSI vs ARPU (animated by year)</div>', unsafe_allow_html=True)
        fig2 = nsi_vs_arpu_scatter(fact)
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📋 Key Insight</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#F0F4F8;padding:1.25rem;border-radius:8px;border-left:4px solid #003366;">
      <p style="margin:0;color:#1A1A2E;font-size:0.95rem;">
        <b>H2 refuted:</b> Concentration decreased (HHI -1,114) yet the Scissors Effect worsened.
        The problem is <b>structural to the telecom business model</b>, not a market power issue.
        Neither monopoly nor competition resolves the traffic/revenue asymmetry.
      </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    from utils.export import download_button
    col1, col2 = st.columns(2)
    with col1:
        download_button(hhi, "nettension_hhi.csv")
    with col2:
        download_button(fact[["trimestre_dt","nsi","revenue_per_line"]], "nettension_nsi_arpu.csv")