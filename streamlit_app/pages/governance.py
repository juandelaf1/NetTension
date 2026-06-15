import streamlit as st
from utils.data_loader import load_sources
from components.filters import render_sidebar
from components.tables import render_governance_table

def render():
    render_sidebar()
    sources = load_sources()
    
    st.markdown("""
    <div class="section-header">
      <h2 class="section-title">Governance & Bias Audit</h2>
      <span class="section-subtitle">DEC-006/007/008 Compliance · Full Traceability</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📋 Data Governance Register</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.85rem;color:#546E7A;margin-bottom:1rem;">
      Every variable is classified per DEC-007/008: Observed, Estimated, Policy Model, or Constant.
      Click column headers to sort, use filters to narrow.
    </div>
    """, unsafe_allow_html=True)
    
    render_governance_table(sources)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🔬 Audit Principles</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:0.9rem;">
          <p><b>DEC-006 (Zero Simulation):</b> Every variable traces to a real public source.
          No synthetic or simulated data.</p>
          <p><b>DEC-007 (Model Governance):</b> 4-tier classification with physical table separation.</p>
          <p><b>DEC-008 (Governance Metadata):</b> Every variable includes: Governance_Layer,
          Confidence_Level, Review_Date, Review_Owner, Source_Type, Reproducible,
          Documentation_Reference.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">⚠️ Bias Disclosure</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:0.9rem;">
          <p><b>Geographic bias:</b> Spain only (case study). Conclusions may not generalize to other EU markets.</p>
          <p><b>Data source bias:</b> CNMC data reflects regulatory definitions.
          Eurostat GDP figures subject to revision.</p>
          <p><b>Model bias:</b> Fair Share what-if assumes linear relationships.
          Real elasticities may differ.</p>
          <p><b>Publication bias:</b> Sources (ETNO, GSMA) represent operator interests.
          Cross-referenced with BEREC for balance.</p>
          <p><b>Temporal bias:</b> Historical (2005-2025). Future projections uncertain.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📖 Methodology Summary</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.9rem;">
      <p><b>Data Pipeline:</b> CNMC Mercados (41,937 rows) + Eurostat demo_pjan (1.17M rows) + 
      Eurostat nama_10_gdp (1.86M rows). ETL in Python (pandas + DuckDB). 
      All transforms documented in <code>src/</code>.</p>
      <p><b>Hypothesis Testing:</b> 6 hypotheses tested with observed data. 
      Statistical significance assessed via CAGR, HHI, and ratio analysis.</p>
      <p><b>Dashboard:</b> Built with Streamlit + Plotly + DuckDB. 
      Source code at <a href="https://github.com/juandelaf1/NetTension">github.com/juandelaf1/NetTension</a>.</p>
      <p><b>Reproducibility:</b> <code>pip install -r requirements.txt && python -m src.pipeline.etl_pipeline</code></p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    from utils.export import download_button
    download_button(sources, "nettension_governance_register.csv")