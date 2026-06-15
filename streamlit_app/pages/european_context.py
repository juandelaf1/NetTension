import streamlit as st
from utils.data_loader import load_eu_context
from components.charts import eu_benchmark_bar
from components.filters import render_sidebar
from components.tables import render_aggrid

def render():
    render_sidebar()
    eu = load_eu_context()
    
    st.markdown("""
    <div class="section-header">
      <h2 class="section-title">European Context</h2>
      <span class="section-subtitle">EU vs USA vs Asia · Benchmarking (ETNO, GSMA, Sandvine)</span>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">💰 CAPEX Per Capita (EUR)</div>', unsafe_allow_html=True)
        fig1 = eu_benchmark_bar(eu, "CAPEX", "CAPEX per capita")
        st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📱 Mobile ARPU (EUR/month)</div>', unsafe_allow_html=True)
        fig2 = eu_benchmark_bar(eu, "ARPU", "Mobile ARPU")
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📡 5G Adoption</div>', unsafe_allow_html=True)
        fig3 = eu_benchmark_bar(eu, "5G", "5G Adoption")
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📊 Market Indicators</div>', unsafe_allow_html=True)
        
        sub = eu[eu["indicator"].str.contains("Video|Big 6|ROCE|real growth", case=False, na=False)]
        for _, row in sub.iterrows():
            st.markdown(f"**{row['indicator']}**: {row['value']} {row['unit']}")
            st.markdown(f"<small>{row['source']}</small>", unsafe_allow_html=True)
            st.markdown("---")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📋 Full Benchmark Database</div>', unsafe_allow_html=True)
    render_aggrid(eu, key="eu_context", height=400)
    st.markdown('</div>', unsafe_allow_html=True)
    
    from utils.export import download_button
    download_button(eu, "nettension_eu_context.csv")