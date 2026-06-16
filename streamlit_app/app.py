import sys
from pathlib import Path

import streamlit as st
from streamlit_option_menu import option_menu

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

st.set_page_config(
    page_title="NetTension — EU Network Stress Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/juandelaf1/NetTension",
        "Report a bug": "https://github.com/juandelaf1/NetTension/issues",
        "About": "NetTension v1.0 — Reducción de latencia en Streamlit"
    }
)

css_path = Path(__file__).parent / "assets" / "style.css"
if css_path.exists():
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

from views import market_overview, network_stress, european_context, fair_share, evolution_strategy, about

LANGUAGE_MAP = {"Español": "es", "English": "en"}
PAGE_ORDER = [
    "market_overview",
    "network_stress",
    "european_context",
    "fair_share",
    "evolution_strategy",
    "about",
]

PAGE_DEFINITIONS = {
    "market_overview": {
        "label": {"es": "Visión de Mercado", "en": "Market Overview"},
        "icon": "bar-chart",
        "render": market_overview.render,
    },
    "network_stress": {
        "label": {"es": "Estrés de Red", "en": "Network Stress"},
        "icon": "activity",
        "render": network_stress.render,
    },
    "european_context": {
        "label": {"es": "Contexto Europeo", "en": "European Context"},
        "icon": "globe",
        "render": european_context.render,
    },
    "fair_share": {
        "label": {"es": "Simulador Fair Share", "en": "Fair Share Simulator"},
        "icon": "sliders",
        "render": fair_share.render,
    },
    "evolution_strategy": {
        "label": {"es": "Evolución y Estrategia", "en": "Evolution & Strategy"},
        "icon": "graph-up-arrow",
        "render": evolution_strategy.render,
    },
    "about": {
        "label": {"es": "Sobre el Proyecto", "en": "About"},
        "icon": "info-circle",
        "render": about.render,
    },
}

with st.sidebar:
    st.markdown(
        """
        <div style="padding:1.25rem 1.25rem 0.5rem;text-align:center;">
          <h1 style="font-size:1.55rem;font-weight:800;color:#00BFA5;margin:0;letter-spacing:-0.5px;">NetTension</h1>
          <p style="font-size:0.78rem;color:#90A4AE;margin:0.35rem 0 0;letter-spacing:0.3px;">Network Stress & Fair Share Dashboard</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    language_label = st.radio(
        "Idioma",
        options=list(LANGUAGE_MAP.keys()),
        index=0,
        horizontal=True,
        key="lang_radio",
        help="Selecciona el idioma de la interfaz",
    )
    st.session_state["lang"] = LANGUAGE_MAP[language_label]

    selected_page = PAGE_ORDER[0]
    try:
        from streamlit_antd_components import sac
        menu_options = [
            {"key": key, "label": PAGE_DEFINITIONS[key]["label"][LANGUAGE_MAP[language_label]], "icon": PAGE_DEFINITIONS[key]["icon"]}
            for key in PAGE_ORDER
        ]
        selected_menu = sac.menu(
            items=menu_options,
            default_selected_keys=[PAGE_ORDER[0]],
            theme="dark",
            mode="inline",
            inline_collapsed=False,
        )
        if isinstance(selected_menu, dict) and "key" in selected_menu:
            selected_page = selected_menu["key"]
    except Exception:
        selected_label = option_menu(
            None,
            [PAGE_DEFINITIONS[key]["label"][LANGUAGE_MAP[language_label]] for key in PAGE_ORDER],
            icons=[PAGE_DEFINITIONS[key]["icon"] for key in PAGE_ORDER],
            menu_icon="signal",
            default_index=0,
            styles={
                "container": {"padding": "0.25rem", "background-color": "#1A2236"},
                "icon": {"color": "#00BFA5", "font-size": "1rem"},
                "nav-link": {
                    "font-size": "0.85rem",
                    "font-weight": "500",
                    "color": "#90A4AE",
                    "--hover-color": "#111827",
                    "padding": "0.6rem 1rem",
                },
                "nav-link-selected": {
                    "background-color": "#00BFA5",
                    "color": "#090D1A",
                    "font-weight": "600",
                },
            },
        )
        selected_page = next(
            key for key in PAGE_ORDER if PAGE_DEFINITIONS[key]["label"][LANGUAGE_MAP[language_label]] == selected_label
        )

    st.markdown(
        """
        <div style="padding:1rem 1.25rem;text-align:center;border-top:1px solid rgba(255,255,255,0.06);margin-top:1rem;">
          <p style="font-size:0.72rem;color:#637381;margin:0;">
            Data: CNMC + Eurostat • Jun 2026<br>
            <a href="https://github.com/juandelaf1/NetTension" target="_blank" style="color:#00BFA5;">github.com/juandelaf1/NetTension</a>
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Hero banner ──
st.markdown("""
<div class="hero-banner">
  <div class="hero-logo">NETTENSION</div>
  <div class="hero-tagline">European Telecom Network Stress &amp; Fair Share Analysis</div>
  <div class="hero-meta">CNMC · Eurostat · ETNO · GSMA · BEREC · Sandvine</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
  .hero-logo { font-size: 4rem !important; animation: gradientShift 3s ease infinite !important; background-size: 300% 300% !important; }
  .hero-banner { padding: 3rem 1rem 1.5rem !important; }
</style>
""", unsafe_allow_html=True)

PAGE_DEFINITIONS[selected_page]["render"]()
