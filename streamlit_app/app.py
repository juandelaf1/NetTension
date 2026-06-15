import streamlit as st
from pathlib import Path
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="NetTension — EU Telecom Network Stress Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/juandelaf1/NetTension",
        "Report a bug": "https://github.com/juandelaf1/NetTension/issues",
        "About": "NetTension v1.0 — Network Stress Simulation Framework (2005-2025)"
    }
)

css_path = Path(__file__).parent / "assets" / "style.css"
if css_path.exists():
    with open(css_path) as f:
        st.html(f"<style>{f.read()}</style>")

with st.sidebar:
    st.markdown("""
    <div style="padding:1rem 1.25rem;text-align:center;">
      <h1 style="font-size:1.5rem;font-weight:800;color:#003366;margin:0;">NetTension</h1>
      <p style="font-size:0.75rem;color:#546E7A;margin:0.25rem 0 0;">Network Stress Simulation Framework</p>
    </div>
    """, unsafe_allow_html=True)
    
    selected = option_menu(
        None,
        ["Market Overview", "Network Stress", "European Context", "Fair Share Simulator", "Governance"],
        icons=["bar-chart", "activity", "globe", "sliders", "clipboard-data"],
        menu_icon="signal",
        default_index=0,
        styles={
            "container": {"padding": "0.25rem", "background-color": "#FFFFFF"},
            "icon": {"color": "#005A9C", "font-size": "1rem"},
            "nav-link": {
                "font-size": "0.85rem", "font-weight": "500",
                "color": "#546E7A", "--hover-color": "#F0F4F8",
                "padding": "0.6rem 1rem"
            },
            "nav-link-selected": {
                "background-color": "#003366", "color": "white",
                "font-weight": "600"
            },
        }
    )
    
    st.markdown("""
    <div style="padding:1rem 1.25rem;text-align:center;border-top:1px solid #E0E0E0;margin-top:1rem;">
      <p style="font-size:0.65rem;color:#9E9E9E;margin:0;">
        Data: CNMC + Eurostat • Jun 2026<br>
        <a href="https://github.com/juandelaf1/NetTension" target="_blank" style="color:#005A9C;">github.com/juandelaf1/NetTension</a>
      </p>
    </div>
    """, unsafe_allow_html=True)

if selected == "Market Overview":
    from pages.market_overview import render
    render()
elif selected == "Network Stress":
    from pages.network_stress import render
    render()
elif selected == "European Context":
    from pages.european_context import render
    render()
elif selected == "Fair Share Simulator":
    from pages.fair_share import render
    render()
elif selected == "Governance":
    from pages.governance import render
    render()