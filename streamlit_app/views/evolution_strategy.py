import streamlit as st
import pandas as pd
from components.filters import render_sidebar
from utils.i18n import t, lang

QUICK_WINS = [
    {
        "title_es": "Elasticidad Precio Banda Ancha",
        "title_en": "Broadband Price Elasticity",
        "icon": "📈",
        "question_es": "¿Qué tan sensible es el tráfico al precio por GB?",
        "question_en": "How sensitive is traffic to price per GB?",
        "method_es": "Regresión log-log: log(traffic) ~ log(revenue_per_traffic) + tendencia",
        "method_en": "Log-log regression: log(traffic) ~ log(revenue_per_traffic) + trend",
        "variables": "revenue_per_traffic, data_traffic, trimestre",
        "difficulty_es": "Baja",
        "difficulty_en": "Low",
        "priority_es": "Alta",
        "priority_en": "High",
        "value_es": "Demostrar qué tan esencial es la conectividad",
        "value_en": "Demonstrate how essential connectivity is",
    },
    {
        "title_es": "Sustitución Voz → Datos",
        "title_en": "Voice → Data Substitution",
        "icon": "🔄",
        "question_es": "¿La voz está siendo canibalizada por datos?",
        "question_en": "Is voice being cannibalized by data?",
        "method_es": "Correlación cruzada + cointegración (Engle-Granger)",
        "method_en": "Cross-correlation + cointegration (Engle-Granger)",
        "variables": "voice_traffic, data_traffic, trimestre",
        "difficulty_es": "Baja",
        "difficulty_en": "Low",
        "priority_es": "Alta",
        "priority_en": "High",
        "value_es": "Explicar colapso de ingresos de voz",
        "value_en": "Explain voice revenue collapse",
    },
    {
        "title_es": "Índice de Presión Regulatoria",
        "title_en": "Regulatory Pressure Index",
        "icon": "⚖️",
        "question_es": "¿Cuánto impacto tiene la regulación en el estrés de red?",
        "question_en": "How much impact does regulation have on network stress?",
        "method_es": "Difference-in-Differences con ventana de eventos",
        "method_en": "Difference-in-Differences with event window",
        "variables": "Eventos regulatorios (1/0) + revenue, HHI, tráfico",
        "difficulty_es": "Media",
        "difficulty_en": "Medium",
        "priority_es": "Alta",
        "priority_en": "High",
        "value_es": "Medir impacto regulatorio cuantitativamente",
        "value_en": "Quantify regulatory impact",
    },
]

HYPOTHESES = [
    {
        "id": "H7",
        "title_es": "Incumbente vs Competidores",
        "title_en": "Incumbent vs Competitors",
        "prediction_es": "Telefónica muestra menor elasticidad ingreso-tráfico que competidores → estructura de costes fijos altos + mayor poder de mercado residual.",
        "prediction_en": "Telefónica shows lower revenue-traffic elasticity than competitors → high fixed cost structure + greater residual market power.",
        "variables": "operador, ingresos_por_operador, trafico, group",
    },
    {
        "id": "H8",
        "title_es": "Convergencia Fijo-Móvil",
        "title_en": "Fixed-Mobile Convergence",
        "prediction_es": "Operadores con oferta convergente (fijo+móvil) tienen menor ARPU churn y mayor data_traffic per subscriber que los mono-producto.",
        "prediction_en": "Operators with convergent offers (fixed+mobile) have lower ARPU churn and higher data traffic per subscriber than mono-product players.",
        "variables": "operador, ARPU, churn, data_traffic, tipo_oferta",
    },
    {
        "id": "H9",
        "title_es": "Estacionalidad del Tráfico",
        "title_en": "Traffic Seasonality",
        "prediction_es": "El tráfico de datos muestra estacionalidad anual (picos Q4, valles Q1) atenuada con la penetración de smartphones.",
        "prediction_en": "Data traffic shows annual seasonality (Q4 peaks, Q1 troughs) attenuated with smartphone penetration.",
        "variables": "data_traffic, trimestre, penetración_smartphone",
    },
    {
        "id": "H10",
        "title_es": "Asimetría Norte-Sur Europeo",
        "title_en": "European North-South Asymmetry",
        "prediction_es": "España muestra mayor ratio NSI/ARPU que Alemania o Francia → justifica diferentes políticas regulatorias (Fair Share más urgente en Sur).",
        "prediction_en": "Spain shows higher NSI/ARPU ratio than Germany or France → justifies different regulatory policies (Fair Share more urgent in the South).",
        "variables": "NSI, ARPU, país, trimestre",
    },
]

MODELOS = [
    {"Modelo (ES)": "Previsión Tráfico", "Modelo (EN)": "Traffic Forecast", "Input": "Series temporales 2005-2024", "Output": "Tráfico 2025-2030", "Técnica": "ARIMA/SARIMA/Prophet"},
    {"Modelo (ES)": "Predicción HHI", "Modelo (EN)": "HHI Prediction", "Input": "revenue_por_operador histórico", "Output": "HHI a 4 trimestres", "Técnica": "LSTM o VAR"},
    {"Modelo (ES)": "Churn de Operadores", "Modelo (EN)": "Operator Churn", "Input": "market_share, entradas/salidas", "Output": "Probabilidad entrada nuevo operador", "Técnica": "Modelos de supervivencia"},
    {"Modelo (ES)": "Déficit de Inversión", "Modelo (EN)": "Investment Gap", "Input": "tráfico, ingresos, CAPEX proxy", "Output": "CapEx requerido para mantener red", "Técnica": "Regresión ridge"},
    {"Modelo (ES)": "Cluster Países EU", "Modelo (EN)": "EU Country Clusters", "Input": "CNMC España + Eurostat otros", "Output": "Grupos por estrés de red", "Técnica": "K-means + PCA"},
]

SIMULACIONES = [
    {"Simulación (ES)": "Fair Share Avanzado", "Simulación (EN)": "Advanced Fair Share", "Descripción (ES)": "Elasticidad tráfico al precio OTT con escenarios 0.1, 0.5, 0.9", "Descripción (EN)": "Traffic elasticity to OTT price with 0.1, 0.5, 0.9 scenarios", "Datos": "Sandvine Big 6 = 50% tráfico"},
    {"Simulación (ES)": "Net Neutrality Relajada", "Simulación (EN)": "Relaxed Net Neutrality", "Descripción (ES)": "Zero-rating, fast lanes → impacto en ARPU, NSI y bienestar", "Descripción (EN)": "Zero-rating, fast lanes → impact on ARPU, NSI and welfare", "Datos": "Escenarios contrafactuales"},
    {"Simulación (ES)": "Consumo Energético", "Simulación (EN)": "Energy Consumption", "Descripción (ES)": "NSI verde: huella de carbono por GB", "Descripción (EN)": "Green NSI: carbon footprint per GB", "Datos": "OPEX/línea como proxy"},
    {"Simulación (ES)": "SIM Swap y Fraude", "Simulación (EN)": "SIM Swap & Fraud", "Descripción (ES)": "Portabilidad + operadores → riesgo fraude SIM swap", "Descripción (EN)": "Portability + operators → SIM swap fraud risk", "Datos": "Variables de portabilidad"},
]

ROADMAPS = {
    "Corto Plazo (6M)": {
        "es": "Corto Plazo (6M)", "en": "Short Term (6M)",
        "items": [
            "M1 — Quick Wins (H7-H10, elasticidad, sustitución)",
            "M1 — CI/CD estable, tests en Docker",
            "M2 — Modelo predictivo tráfico (Prophet)",
            "M2 — Fair Share Simulator v2 (no-lineal)",
            "M3 — Dashboard Streamlit v2 (multi-país)",
            "M3 — Primer paper: Scissors Effect",
            "M4 — Landing page + Fair Share Calculator",
            "M5 — Reuniones con CNMC/ETNO",
            "M6 — Release v2.0: multi-país + predictivo",
        ],
    },
    "Medio Plazo (12M)": {
        "es": "Medio Plazo (12M)", "en": "Medium Term (12M)",
        "items": [
            "M7 — Integrar Italia (AGCOM), Portugal (ANACOM)",
            "M8 — Dashboard SaaS MVP (3 países)",
            "M9 — Segundo paper: H2 refutada",
            "M9 — Zero-Touch API v1",
            "M10 — Caso de uso: inversor PE",
            "M11 — Pilot con NRA real",
            "M12 — Release v3.0: 5 países + predicción",
        ],
    },
    "Visión SaaS (24M)": {
        "es": "Visión SaaS (24M)", "en": "SaaS Vision (24M)",
        "items": [
            "T1-Q1 — 8 países EU (top operadores)",
            "T1-Q2 — Fair Share Impact Report (ETNO)",
            "T1-Q3 — SaaS lanzamiento comercial",
            "T1-Q4 — 12 países, API pública",
            "T2-Q1 — Paper Network Stress Index aceptado",
            "T2-Q2 — Cliente consultoría NRA confirmado",
            "T2-Q3 — Producto SaaS en 3 NRAs",
            "T2-Q4 — Revenue recurrente > €100K ARR",
        ],
    },
}

MONETIZACION = pd.DataFrame({
    "Stream (ES)": ["Consultoría (informes)", "SaaS (licencias NRA)", "API (desarrolladores)", "Fair Share Calculator", "Total"],
    "Stream (EN)": ["Consulting (reports)", "SaaS (NRA licenses)", "API (developers)", "Fair Share Calculator", "Total"],
    "Año 1 / Year 1": ["€15K", "€0", "€0", "€0", "€15K"],
    "Año 2 / Year 2": ["€40K", "€30K", "€5K", "€0 (lead gen)", "€75K"],
    "Año 3 / Year 3": ["€80K", "€120K", "€20K", "€10K (premium)", "€230K"],
})

CONSULTING = pd.DataFrame({
    "Cliente / Client": ["CNMC / NRA", "Telefónica", "ETNO", "Comisión Europea (DG CONNECT)", "Inversores (Private Equity)", "Consultoras (BCG, McKinsey)"],
    "Servicio / Service": [
        "Extensión a más años/mercados",
        "Benchmarking frente a competidores",
        "Informe Fair Share con datos propios",
        "Estudio de estrés de red EU",
        "Due diligence de mercado TELCO",
        "Input para proyectos TELCO",
    ],
    "Valor / Value €": ["€15-30K", "€10-20K", "€25-50K", "€50-100K", "€5-15K", "€3-10K/licencia"],
})

PUBLICACIONES = pd.DataFrame({
    "Paper": [
        "Scissors Effect in Telecom",
        "H2 Refutation: Structural Problem",
        "Network Stress Index",
        "Fair Share Elasticity Model",
    ],
    "Revista / Journal": [
        "Telecommunications Policy",
        "Journal of Regulatory Economics",
        "IEEE Access",
        "Information Economics & Policy",
    ],
    "Cuartil / Quartile": ["Q1", "Q1", "Q2", "Q1"],
    "Prob. / Prob.": ["60%", "30%", "80%", "40%"],
})


def render_quick_wins():
    L = lang()
    st.markdown(f'<p style="color:#90A4AE;font-size:0.9rem;margin-bottom:1.5rem;">{t("evolution_strategy.quick_wins_intro", L)}</p>', unsafe_allow_html=True)

    cols = st.columns(len(QUICK_WINS))
    for col, qw in zip(cols, QUICK_WINS):
        with col:
            title = qw[f"title_{L}"]
            question = qw[f"question_{L}"]
            method = qw[f"method_{L}"]
            difficulty = qw[f"difficulty_{L}"]
            priority = qw[f"priority_{L}"]
            st.markdown(f"""
            <div class="premium-card">
              <div style="font-size:1.5rem;margin-bottom:0.5rem;">{qw["icon"]}</div>
              <h3 style="color:#FFFFFF;font-size:1rem;font-weight:600;margin:0 0 0.5rem;">{title}</h3>
              <p style="color:#90A4AE;font-size:0.8rem;margin:0 0 0.75rem;">{question}</p>
              <hr style="border-color:rgba(255,255,255,0.08);margin:0.5rem 0;">
              <div style="font-size:0.75rem;color:#637381;">
                <p style="margin:0.25rem 0;"><b style="color:#00BFA5;">{t('evolution_strategy.method_label', L)}:</b> {method}</p>
                <p style="margin:0.25rem 0;"><b style="color:#00BFA5;">{t('evolution_strategy.variables_label', L)}:</b> {qw["variables"]}</p>
                <p style="margin:0.25rem 0;">
                  <span style="background:rgba(0,191,165,0.15);padding:2px 8px;border-radius:4px;color:#00BFA5;font-weight:600;">{difficulty}</span>
                  <span style="background:rgba(255,82,82,0.15);padding:2px 8px;border-radius:4px;color:#FF5252;font-weight:600;margin-left:0.5rem;">{priority}</span>
                </p>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(f'<h3 style="color:#FFFFFF;font-size:1.1rem;margin:2rem 0 1rem;">🧪 {t("evolution_strategy.new_hypotheses", L)}</h3>', unsafe_allow_html=True)

    for h in HYPOTHESES:
        is_pink = h["id"] in ("H7", "H10")
        cls = 'highlight-box pink' if is_pink else 'highlight-box'
        title = h[f"title_{L}"]
        prediction = h[f"prediction_{L}"]
        st.markdown(f"""
        <div class="{cls}">
          <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.5rem;">
            <span style="background:{"#FF5252" if is_pink else "#00BFA5"};color:#090D1A;font-weight:700;font-size:0.7rem;padding:2px 8px;border-radius:4px;">{h["id"]}</span>
            <strong style="color:#FFFFFF;">{title}</strong>
          </div>
          <p style="color:#90A4AE;font-size:0.85rem;margin:0.25rem 0;"><b>{t('evolution_strategy.method_label', L)}:</b> {prediction}</p>
          <p style="color:#556677;font-size:0.75rem;margin:0.25rem 0 0;"><b>{t('evolution_strategy.variables_label', L)}:</b> {h["variables"]}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f'<div class="insight-box">📌 <b>{t("evolution_strategy.next_action", L)}</b></div>', unsafe_allow_html=True)


def render_modelos():
    L = lang()
    st.markdown(f'<p style="color:#90A4AE;font-size:0.9rem;margin-bottom:1.5rem;">{t("evolution_strategy.models_intro", L)}</p>', unsafe_allow_html=True)

    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown(f'<h4 style="color:#00BFA5;font-size:0.9rem;margin:0 0 1rem;">📊 {t("evolution_strategy.models_title", L)}</h4>', unsafe_allow_html=True)
    model_col = f"Modelo ({'ES' if L == 'es' else 'EN'})"
    modelos_df = pd.DataFrame(MODELOS)
    display_df = modelos_df[[model_col, "Input", "Output", "Técnica"]].rename(columns={model_col: "Modelo" if L == "es" else "Model"})
    st.table(display_df)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f'<h3 style="color:#FFFFFF;font-size:1.1rem;margin:2rem 0 1rem;">🔬 {t("evolution_strategy.simulations_title", L)}</h3>', unsafe_allow_html=True)

    sim_col = f"Simulación ({'ES' if L == 'es' else 'EN'})"
    desc_col = f"Descripción ({'ES' if L == 'es' else 'EN'})"
    for sim in SIMULACIONES:
        st.markdown(f"""
        <div class="premium-card" style="margin-bottom:1rem;">
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
              <h4 style="color:#FFFFFF;font-size:0.95rem;margin:0 0 0.25rem;">{sim[sim_col]}</h4>
              <p style="color:#90A4AE;font-size:0.85rem;margin:0;">{sim[desc_col]}</p>
            </div>
            <span style="background:rgba(0,191,165,0.1);color:#00BFA5;font-size:0.7rem;padding:4px 10px;border-radius:4px;white-space:nowrap;">{sim["Datos"]}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f'<div class="insight-box">💡 <b>{t("evolution_strategy.opportunity", L)}</b></div>', unsafe_allow_html=True)


def render_roadmap():
    L = lang()
    st.markdown(f'<p style="color:#90A4AE;font-size:0.9rem;margin-bottom:0.5rem;">{t("evolution_strategy.roadmap_intro", L)}</p>', unsafe_allow_html=True)

    horizon_options = list(ROADMAPS.keys())
    horizon_labels = [ROADMAPS[k][L] for k in horizon_options]
    horizon = st.select_slider(
        t("evolution_strategy.roadmap_horizon", L),
        options=horizon_options,
        format_func=lambda x: ROADMAPS[x][L],
        value="Corto Plazo (6M)",
        key="roadmap_slider",
    )

    milestones = ROADMAPS[horizon]["items"]

    st.markdown(f"""
    <div class="premium-card" style="margin-top:1rem;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;">
        <h3 style="color:#00BFA5;font-size:1.1rem;margin:0;">🗺️ {ROADMAPS[horizon][L]}</h3>
        <span style="background:rgba(0,191,165,0.15);color:#00BFA5;font-weight:600;font-size:0.75rem;padding:4px 12px;border-radius:20px;">{len(milestones)} hitos</span>
      </div>
      <div style="position:relative;padding-left:1.5rem;">
        <div style="position:absolute;left:0;top:0;bottom:0;width:2px;background:linear-gradient(to bottom,#00BFA5,rgba(255,255,255,0.08));"></div>
    """, unsafe_allow_html=True)

    for i, milestone in enumerate(milestones):
        st.markdown(f"""
        <div style="position:relative;padding:0 0 1rem 1rem;border-left:2px solid transparent;margin-left:-1px;">
          <div style="position:absolute;left:-7px;top:4px;width:12px;height:12px;border-radius:50%;background:{"#00BFA5" if i < 3 else "#1A2236"};border:2px solid #00BFA5;"></div>
          <p style="color:#{"FFFFFF" if i < 3 else "8899AA"};font-size:0.85rem;margin:0;font-weight:{"600" if i < 3 else "400"};">{milestone}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
      </div>
    </div>
    """, unsafe_allow_html=True)

    meta_key = {"Corto Plazo (6M)": "meta_short", "Medio Plazo (12M)": "meta_medium", "Visión SaaS (24M)": "meta_long"}
    st.markdown(f"""
    <div class="insight-box">
      🎯 <b>{t('evolution_strategy.roadmap_horizon', L)} {ROADMAPS[horizon][L]}:</b> {t('evolution_strategy.' + meta_key[horizon], L)}
    </div>
    """, unsafe_allow_html=True)


def render_monetizacion():
    L = lang()
    st.markdown(f'<p style="color:#90A4AE;font-size:0.9rem;margin-bottom:1.5rem;">{t("evolution_strategy.monetization_intro", L)}</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown(f'<h4 style="color:#00BFA5;font-size:0.9rem;margin:0 0 1rem;">💰 {t("evolution_strategy.revenue_title", L)}</h4>', unsafe_allow_html=True)
        stream_col = f"Stream ({'ES' if L == 'es' else 'EN'})"
        year_cols = ["Año 1 / Year 1", "Año 2 / Year 2", "Año 3 / Year 3"]
        display_df = MONETIZACION[[stream_col] + year_cols].rename(columns={stream_col: "Stream"})
        st.dataframe(display_df, width="stretch", hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="premium-card" style="margin-top:1rem;">', unsafe_allow_html=True)
        st.markdown(f'<h4 style="color:#00BFA5;font-size:0.9rem;margin:0 0 1rem;">📚 {t("evolution_strategy.publications_title", L)}</h4>', unsafe_allow_html=True)
        pub_cols = ["Paper", f"Revista / Journal", f"Cuartil / Quartile", f"Prob. / Prob."]
        pub_rename = {"Paper": "Paper", f"Revista / Journal": "Journal" if L == "en" else "Revista",
                      f"Cuartil / Quartile": "Quartile" if L == "en" else "Cuartil",
                      f"Prob. / Prob.": "Prob."}
        display_pub = PUBLICACIONES[pub_cols].rename(columns=pub_rename)
        st.dataframe(display_pub, width="stretch", hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown(f'<h4 style="color:#00BFA5;font-size:0.9rem;margin:0 0 1rem;">🏢 {t("evolution_strategy.consulting_title", L)}</h4>', unsafe_allow_html=True)
        cons_cols = ["Cliente / Client", "Servicio / Service", "Valor / Value €"]
        cons_rename = {"Cliente / Client": "Client" if L == "en" else "Cliente",
                       "Servicio / Service": "Service" if L == "en" else "Servicio",
                       "Valor / Value €": "Value €" if L == "en" else "Valor €"}
        display_cons = CONSULTING[cons_cols].rename(columns=cons_rename)
        st.dataframe(display_cons, width="stretch", hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="premium-card" style="margin-top:1rem;">', unsafe_allow_html=True)
        st.markdown(f'<h4 style="color:#00BFA5;font-size:0.9rem;margin:0 0 0.75rem;">🚀 {t("evolution_strategy.saas_title", L)}</h4>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:0.85rem;color:#90A4AE;">
          <p style="margin:0.5rem 0;"><b style="color:#FFFFFF;">NetTension SaaS</b><br>{t('evolution_strategy.saas_desc', L)}</p>
          <p style="margin:0.5rem 0;"><b style="color:#FFFFFF;">Fair Share Calculator</b><br>{t('evolution_strategy.fsc_desc', L)}</p>
          <p style="margin:0.5rem 0;"><b style="color:#FFFFFF;">API Regulatoria</b><br>{t('evolution_strategy.api_desc', L)}</p>
          <hr style="border-color:rgba(255,255,255,0.08);margin:0.75rem 0;">
          <p style="margin:0.5rem 0;color:#637381;"><b>{t('evolution_strategy.diff_title', L)}:</b> <b style="color:#FF5252;">{t('evolution_strategy.diff_text', L)}</b></p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


def render():
    render_sidebar()
    L = lang()

    st.markdown(f"""
    <div class="story-chapter violet">
      <span class="chapter-badge">Capítulo 5</span>
      <h2 class="chapter-title">{t('evolution_strategy.title', L)}</h2>
      <p class="chapter-subtitle">{t('evolution_strategy.subtitle', L)}</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        f"⚡ {t('evolution_strategy.tab_quick_wins', L)}",
        f"🔮 {t('evolution_strategy.tab_models', L)}",
        f"🗺️ {t('evolution_strategy.tab_roadmap', L)}",
        f"💼 {t('evolution_strategy.tab_monetization', L)}",
    ])

    with tab1:
        render_quick_wins()
    with tab2:
        render_modelos()
    with tab3:
        render_roadmap()
    with tab4:
        render_monetizacion()

    # ── Methodology & Sources ──
    with st.expander(f"📋 {t('governance.register_title', L)}", expanded=False):
        from utils.data_loader import load_sources
        sources = load_sources()
        cols = ["source_name", "governance_layer", "confidence", "source_type", "rows"]
        display_cols = [c for c in cols if c in sources.columns]
        st.dataframe(sources[display_cols], width="stretch", hide_index=True, height=250)
        st.markdown(f"""
        <div style="font-size:0.8rem;color:#90A4AE;margin-top:0.5rem;">
          <p><b>🔬 {t('governance.methodology_title', L)}</b></p>
          <p>{t('governance.methodology_pipeline', L)}</p>
          <p>{t('governance.methodology_dashboard', L)}</p>
          <p><b>⚠️ {t('governance.bias_title', L)}</b></p>
          <ul style="margin:0.25rem 0;padding-left:1.2rem;">
            <li>{t('governance.bias_geographic', L)}</li>
            <li>{t('governance.bias_source', L)}</li>
            <li>{t('governance.bias_model', L)}</li>
          </ul>
        </div>
        """, unsafe_allow_html=True)
