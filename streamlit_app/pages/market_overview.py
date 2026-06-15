import streamlit as st
import pandas as pd
from utils.data_loader import load_fact_observed, get_kpis, filter_by_year
from utils.data_loader import load_dim_operator
from components.charts import scissors_chart, traffic_revenue_stacked
from components.kpi_card import kpi_row
from components.filters import render_sidebar

def render():
    filters = render_sidebar()
    kpis = get_kpis()
    fact = filter_by_year(load_fact_observed(), filters["year_range"])
    
    st.markdown("""
    <div class="section-header">
      <h2 class="section-title">Market Overview</h2>
      <span class="section-subtitle">Scissors Effect · Traffic vs Revenue divergence (Spain 2005–2025)</span>
    </div>
    """, unsafe_allow_html=True)
    
    kpi_row([
        dict(label="Traffic CAGR", value=f"{kpis['traffic_cagr']:.1%}",
             delta="+127%/yr vs 2005", delta_color="positive", icon="📈",
             sparkline_data=fact["data_traffic_index"].tail(20).tolist()),
        dict(label="Revenue CAGR", value=f"{kpis['rev_cagr']:.1%}",
             delta="−0.4%/yr vs 2005", delta_color="negative", icon="💰",
             sparkline_data=fact["revenue_index"].tail(20).tolist()),
        dict(label="CAGR Gap", value=f"{kpis['cagr_gap']:.1%}",
             delta="127.4 pp divergence", delta_color="negative", icon="✂️",
             sparkline_data=(fact["data_traffic_index"] - fact["revenue_index"]).tail(20).tolist()),
        dict(label="Avg ARPU", value=f"€{kpis['avg_arpu']:,.0f}/line",
             delta="−83% since 2005", delta_color="negative", icon="💳",
             sparkline_data=fact["revenue_per_line"].tail(20).tolist()),
    ])
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📊 Scissors Effect: Traffic Index vs Revenue Index</div>', unsafe_allow_html=True)
    fig = scissors_chart(fact)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📈 Traffic & Voice Volume</div>', unsafe_allow_html=True)
        fig2 = traffic_revenue_stacked(fact)
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📋 Recent Quarters</div>', unsafe_allow_html=True)
        detail = fact[["trimestre_dt", "data_traffic", "revenue", "total_lines", "revenue_per_line"]].tail(8).copy()
        detail["trimestre_dt"] = detail["trimestre_dt"].dt.strftime("%Y Q%q")
        detail.columns = ["Quarter", "Traffic", "Revenue", "Lines", "ARPU"]
        for _, row in detail.iterrows():
            st.markdown(f"**{row['Quarter']}** · Traffic: {row['Traffic']:,.0f} · Rev: €{row['Revenue']:,.0f}")
            st.markdown(f"Lines: {row['Lines']:,.0f} · ARPU: €{row['ARPU']:,.2f}")
            st.markdown("---" if _ < len(detail) - 1 else "")
        st.markdown('</div>', unsafe_allow_html=True)
    
    from utils.export import download_button
    download_button(fact, "nettension_market_overview.csv")