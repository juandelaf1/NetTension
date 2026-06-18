import streamlit as st
from io import BytesIO
from utils.i18n import t, lang

_SECTION_COLORS = ["#D97724", "#9A6AFF", "#2EA043", "#CF3B30", "#2EA043"]

def _qr_img(url: str):
    from io import BytesIO
    import qrcode
    qr = qrcode.QRCode(box_size=6, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#F0F6FC", back_color="#0B0E14")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

_SECTIONS = [
    {
        "key": "project",
        "icon": "🚀",
        "title": {"es": "El Proyecto", "en": "The Project"},
        "body": {
            "es": """**NetTension** analiza la divergencia entre el tráfico de datos y los ingresos en el sector TELCO español (2005–2025).<br><br>
El proyecto contrasta **6 hipótesis** sobre concentración de mercado, estrés de red y asimetría europea, y simula el impacto regulatorio del **Fair Share**.""",
            "en": """**NetTension** analyzes the divergence between data traffic and revenue in the Spanish TELCO sector (2005–2025).<br><br>
The project tests **6 hypotheses** on market concentration, network stress, and European asymmetry, and simulates the regulatory impact of **Fair Share**.""",
        },
        "facts": {
            "es": ["📦 +41.937 registros procesados", "📅 20 años de datos (2005–2025)", "🔬 6 hipótesis contrastadas", "📊 5 páginas de dashboard"],
            "en": ["📦 41,937+ processed records", "📅 20 years of data (2005–2025)", "🔬 6 hypotheses tested", "📊 5 dashboard pages"],
        },
    },
    {
        "key": "data",
        "icon": "📡",
        "title": {"es": "Fuentes de Datos", "en": "Data Sources"},
        "body": {
            "es": "Todos los datos provienen de fuentes públicas y oficiales, siguiendo el principio **DEC-006: Zero Simulation**.",
            "en": "All data comes from public official sources, following **DEC-006: Zero Simulation** policy.",
        },
        "sources": [
            ("CNMC", "Comisión Nacional de los Mercados y la Competencia", "Mercado de Telecomunicaciones 2005–2025", "41.937 filas"),
            ("Eurostat", "Oficina de Estadística de la UE", "demo_pjan (población) + nama_10_gdp (PIB)", "1,17M + 1,86M filas"),
            ("ETNO", "European Telecommunications Network Operators", "State of Digital Communications 2025", "Benchmarks UE"),
            ("GSMA", "Global System for Mobile Communications", "Mobile Economy Reports", "Indicadores móviles"),
            ("BEREC", "Body of European Regulators for Electronic Communications", "Fair Share Reports 2025", "Marco regulatorio"),
            ("Sandvine", "Sandvine / AppLogic", "Global Internet Phenomena Report", "Composición de tráfico"),
        ],
    },
    {
        "key": "tech",
        "icon": "⚙️",
        "title": {"es": "Stack Tecnológico", "en": "Tech Stack"},
        "body": {
            "es": "Pipeline y dashboard construidos con herramientas modernas open-source:",
            "en": "Pipeline and dashboard built with modern open-source tools:",
        },
        "tools": [
            ("🐍 Python", "Pandas, NumPy, Plotly, Streamlit"),
            ("🦆 DuckDB", "Base de datos analítica embeddable (OLAP)"),
            ("📈 ECharts + Plotly", "Visualizaciones interactivas con tooltips ricos"),
            ("🎨 Streamlit", "Framework de dashboard en Python puro"),
            ("🧪 pytest + DuckDB", "Tests de validación y pipeline CI/CD"),
            ("🐳 Docker", "Contenedor para despliegue reproducible"),
            ("🔬 Hypothesis Testing", "6 hipótesis con CAGR, HHI y análisis de ratios"),
            ("📊 DuckDB + Parquet", "Cache de datos en formato columnar"),
        ],
    },
    {
        "key": "findings",
        "icon": "🔬",
        "title": {"es": "Hallazgos Clave", "en": "Key Findings"},
        "body": {
            "es": "Los datos revelan verdades incómodas para el sector:",
            "en": "The data reveals uncomfortable truths for the sector:",
        },
        "findings_list": {
            "es": [
                "**H1 ✅** Efecto Tijera confirmado: tráfico +127% CAGR vs ingresos −0.4% CAGR — brecha de 127pp",
                "**H2 ❌ REFUTADA:** HHI bajó 1.114 puntos (3.482→2.368). Más competencia no redujo la tijera. El problema es estructural del modelo de utilidad.",
                "**H3 ✅** Compresión de margen confirmada: el ingreso por unidad de tráfico colapsa mientras el tráfico se dispara",
                "**H4 ✅** ROCE < WACC: la inversión en infraestructura europea destruye valor económico porque ha alcanzado su límite físico de optimización",
                "**H5 ✅** Europa invierte la mitad que EE.UU. (118€ vs 226€ per cápita) con un ARPU 3× menor",
                "**H6 ✅** Fair Share es una palanca legítima pero no suficiente: incluso al 25% OTT + 30% CAPEX, quedan ~80pp de brecha remanente",
            ],
            "en": [
                "**H1 ✅** Scissors Effect confirmed: traffic +127% CAGR vs revenue −0.4% CAGR — 127pp gap",
                "**H2 ❌ REFUTED:** HHI dropped 1,114 points (3,482→2,368). More competition did not close the scissors. Structural utility model failure.",
                "**H3 ✅** Margin compression confirmed: revenue per traffic unit collapses while traffic soars",
                "**H4 ✅** ROCE < WACC: European infrastructure investment destroys economic value, having hit its physical optimization limit",
                "**H5 ✅** Europe invests half of what the US does (€118 vs €226 per capita) with 3× lower ARPU",
                "**H6 ✅** Fair Share is a legitimate lever but insufficient alone: even at 25% OTT + 30% CAPEX, ~80pp gap remains",
            ],
        },
    },
    {
        "key": "governance",
        "icon": "🔐",
        "title": {"es": "Gobernanza de Datos", "en": "Data Governance"},
        "body": {
            "es": """Cada variable del modelo sigue las políticas **DEC-007** y **DEC-008**:<br><br>
• **Capa Observada:** Datos directos de CNMC (tráfico, ingresos, líneas)<br>
• **Capa Estimada:** Indicadores calculados (CAGR, HHI, NSI)<br>
• **Modelo de Política:** Simulaciones Fair Share<br>
• **Constantes:** Umbrales regulatorios (HHI 2500/1000)""",
            "en": """Every model variable follows **DEC-007** and **DEC-008** policies:<br><br>
• **Observed Layer:** Direct CNMC data (traffic, revenue, lines)<br>
• **Estimated Layer:** Calculated indicators (CAGR, HHI, NSI)<br>
• **Policy Model:** Fair Share simulations<br>
• **Constants:** Regulatory thresholds (HHI 2500/1000)""",
        },
        "badges": {
            "es": ["✅ Sin datos sintéticos", "✅ 4 capas de gobernanza", "✅ Fuentes públicas verificables", "✅ Pipeline reproducible"],
            "en": ["✅ No synthetic data", "✅ 4 governance layers", "✅ Verifiable public sources", "✅ Reproducible pipeline"],
        },
    },
]

def render():
    L = lang()

    st.markdown(f"""
    <div class="story-chapter">
      <span class="chapter-badge">📋 {'Sobre el Proyecto' if L == 'es' else 'About'}</span>
      <h2 class="chapter-title">{'Sobre el Proyecto' if L == 'es' else 'About the Project'}</h2>
      <p class="chapter-subtitle">{'Datos, herramientas y resultados del análisis NetTension' if L == 'es' else 'Data, tools and results of the NetTension analysis'}</p>
    </div>
    """, unsafe_allow_html=True)

    for idx, sec in enumerate(_SECTIONS):
        sc = _SECTION_COLORS[idx % len(_SECTION_COLORS)]
        st.markdown(f'<div class="chart-container" style="border-left:4px solid {sc};">', unsafe_allow_html=True)
        st.markdown(f'<div class="chart-title" style="color:{sc};">{sec["icon"]} {sec["title"][L]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="color:var(--text-secondary);line-height:1.7;">{sec["body"][L]}</div>', unsafe_allow_html=True)

        if "facts" in sec:
            cols = st.columns(len(sec["facts"][L]))
            for ci, fact in enumerate(sec["facts"][L]):
                with cols[ci]:
                    st.markdown(f"""
                    <div style="background:rgba({int(sc[1:3],16)},{int(sc[3:5],16)},{int(sc[5:7],16)},0.06);border-radius:10px;padding:0.6rem;text-align:center;
                                border:1px solid rgba({int(sc[1:3],16)},{int(sc[3:5],16)},{int(sc[5:7],16)},0.12);font-size:0.85rem;color:var(--text-primary);">
                      {fact}
                    </div>
                    """, unsafe_allow_html=True)

        if "sources" in sec:
            st.markdown(f'<div style="margin-top:0.8rem;"><table style="width:100%;border-collapse:collapse;font-size:0.85rem;">', unsafe_allow_html=True)
            st.markdown(f"""<tr style="border-bottom:1px solid rgba(255,255,255,0.06);">
              <th style="text-align:left;padding:0.5rem 0.5rem;color:#8B949E;font-weight:600;">{'Fuente' if L == 'es' else 'Source'}</th>
              <th style="text-align:left;padding:0.5rem 0.5rem;color:#8B949E;font-weight:600;">{'Organismo' if L == 'es' else 'Organization'}</th>
              <th style="text-align:left;padding:0.5rem 0.5rem;color:#8B949E;font-weight:600;">Dataset</th>
              <th style="text-align:right;padding:0.5rem 0.5rem;color:#8B949E;font-weight:600;">{'Volumen' if L == 'es' else 'Volume'}</th>
            </tr>""", unsafe_allow_html=True)
            for src in sec["sources"]:
                st.markdown(f"""<tr style="border-bottom:1px solid rgba(255,255,255,0.03);">
                  <td style="padding:0.45rem 0.5rem;color:{sc};font-weight:600;">{src[0]}</td>
                  <td style="padding:0.45rem 0.5rem;color:var(--text-secondary);">{src[1]}</td>
                  <td style="padding:0.45rem 0.5rem;color:var(--text-secondary);">{src[2]}</td>
                  <td style="padding:0.45rem 0.5rem;text-align:right;color:var(--text-secondary);">{src[3]}</td>
                </tr>""", unsafe_allow_html=True)
            st.markdown('</table></div>', unsafe_allow_html=True)

        if "tools" in sec:
            cols = st.columns(2)
            for i, (tool, desc) in enumerate(sec["tools"]):
                with cols[i % 2]:
                    st.markdown(f"""
                    <div style="background:rgba({int(sc[1:3],16)},{int(sc[3:5],16)},{int(sc[5:7],16)},0.05);border-radius:8px;padding:0.5rem 0.8rem;margin:0.25rem 0;
                                border:1px solid rgba({int(sc[1:3],16)},{int(sc[3:5],16)},{int(sc[5:7],16)},0.1);">
                      <span style="color:var(--text-primary);font-weight:600;">{tool}</span>
                      <span style="color:var(--text-secondary);font-size:0.85rem;display:block;">{desc}</span>
                    </div>
                    """, unsafe_allow_html=True)

        if "findings_list" in sec:
            for finding in sec["findings_list"][L]:
                st.markdown(f"""
                <div style="padding:0.4rem 0.8rem;margin:0.2rem 0;border-left:3px solid {sc};
                            background:rgba({int(sc[1:3],16)},{int(sc[3:5],16)},{int(sc[5:7],16)},0.04);
                            border-radius:0 6px 6px 0;font-size:0.9rem;color:var(--text-secondary);">
                  {finding}
                </div>
                """, unsafe_allow_html=True)

        if "badges" in sec:
            cols = st.columns(len(sec["badges"][L]))
            for ci, badge in enumerate(sec["badges"][L]):
                with cols[ci]:
                    st.markdown(f"""
                    <div style="background:rgba({int(sc[1:3],16)},{int(sc[3:5],16)},{int(sc[5:7],16)},0.06);border-radius:20px;padding:0.3rem 0.6rem;text-align:center;
                                border:1px solid rgba({int(sc[1:3],16)},{int(sc[3:5],16)},{int(sc[5:7],16)},0.15);font-size:0.8rem;color:{sc};">
                      {badge}
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="chart-container" style="text-align:center;">
      <h3 style="color:var(--text-primary);margin-bottom:0.5rem;">{'📂 Repositorio' if L == 'es' else '📂 Repository'}</h3>
      <p style="color:var(--text-secondary);font-size:0.9rem;">
        {'Escanea para ver el código fuente completo' if L == 'es' else 'Scan to see the full source code'}
      </p>
    </div>
    """, unsafe_allow_html=True)

    col_qr, col_link = st.columns([1, 3])
    with col_qr:
        qr_img = _qr_img("https://github.com/juandelaf1/NetTension")
        st.image(qr_img, width=180, caption="github.com/juandelaf1/NetTension")
    with col_link:
        st.markdown(f"""
        <div style="height:100%;display:flex;flex-direction:column;justify-content:center;padding:1rem 2rem;">
          <div style="font-size:1.1rem;font-weight:600;color:#D97724;margin-bottom:0.5rem;">
            🔗 <a href="https://github.com/juandelaf1/NetTension" target="_blank" style="color:#D97724;">github.com/juandelaf1/NetTension</a>
          </div>
          <div style="color:var(--text-secondary);font-size:0.9rem;line-height:1.6;">
            {'⭐ Incluye: Pipeline ETL, dashboard Streamlit, modelo DuckDB, tests CI/CD, Dockerfile, y documentación completa.' if L == 'es' else '⭐ Includes: ETL pipeline, Streamlit dashboard, DuckDB model, CI/CD tests, Dockerfile, and full documentation.'}
          </div>
          <div style="color:var(--text-muted);font-size:0.8rem;margin-top:0.5rem;">
            {'📄 Licencia: MIT — libre para uso académico y regulatorio' if L == 'es' else '📄 License: MIT — free for academic and regulatory use'}
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:center;padding:2rem 1rem 0.5rem;font-size:0.75rem;color:var(--text-muted);">
      NetTension v1.0 · CNMC + Eurostat · {'Junio 2026' if L == 'es' else 'June 2026'}
    </div>
    """, unsafe_allow_html=True)
