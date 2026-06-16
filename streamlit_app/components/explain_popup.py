import streamlit as st

def maybe_popup(chart_type: str, result, ev_key: str):
    ll = {"Español": "es", "English": "en"}
    L = ll.get(st.session_state.get("lang_radio"), "es")
    dk = f"_d_{ev_key}"
    lk = f"_l_{ev_key}"
    new_data = result and isinstance(result, dict) and result != st.session_state.get(dk)
    lang_switched = L != st.session_state.get(lk)
    if new_data:
        st.session_state[dk] = result
        st.session_state[lk] = L
        render_popup(chart_type, result, L)
    elif lang_switched and result and isinstance(result, dict):
        st.session_state[lk] = L
        render_popup(chart_type, result, L)

CLICK_FORMAT = (
    "function(p) { return {name: p.name, value: p.value, seriesName: p.seriesName}; }"
)

def render_popup(chart_type: str, click_data: dict, L: str):
    info = _CONTENT.get(chart_type)
    if not info:
        return
    title = info["title"].get(L, info["title"]["es"])
    with st.popover(f"📖 {title}", use_container_width=True):
        name = click_data.get("name", "")
        value = click_data.get("value", "")
        series = click_data.get("seriesName", "")
        st.caption(f"📌 {name} · {series}: **{value}**")
        st.divider()
        for section in info["sections"]:
            heading = section["heading"].get(L, section["heading"]["es"])
            body_raw = section["body"].get(L, section["body"]["es"])
            body = body_raw.format(name=name, value=value, series=series)
            st.markdown(f"**{heading}**")
            st.markdown(body)
            if "caption" in section:
                cap = section["caption"].get(L, section["caption"]["es"])
                st.caption(cap)
            st.divider()

_CONTENT = {
    "scissors": {
        "title": {"es": "El Efecto Tijera", "en": "The Scissors Effect"},
        "sections": [
            {
                "heading": {"es": "¿Qué significa este valor?", "en": "What does this value mean?"},
                "body": {
                    "es": "El **Índice de Tráfico** (teal) y el **Índice de Ingresos** (coral) están indexados a 2005=100.\n\n• **{series}** en **{name}** = **{value}**\n• Cuando el tráfico sube y los ingresos bajan, la brecha (barras ámbar) se ensancha. Esa divergencia es el **Efecto Tijera**.",
                    "en": "The **Traffic Index** (teal) and **Revenue Index** (coral) are indexed to 2005=100.\n\n• **{series}** in **{name}** = **{value}**\n• When traffic rises and revenue falls, the gap (amber bars) widens. That divergence is the **Scissors Effect**.",
                },
            },
            {
                "heading": {"es": "Implicación", "en": "Implication"},
                "body": {
                    "es": "Cada punto porcentual de brecha representa tráfico no monetizado. Si la tendencia continúa, los operadores no podrán sostener la inversión en red.",
                    "en": "Each percentage point of gap represents unmonetized traffic. If the trend continues, operators won't be able to sustain network investment.",
                },
                "caption": {"es": "Fuente: CNMC Datos de Mercado", "en": "Source: CNMC Market Data"},
            },
        ],
    },
    "traffic_volume": {
        "title": {"es": "Volumen de Tráfico", "en": "Traffic Volume"},
        "sections": [
            {
                "heading": {"es": "¿Qué significa este valor?", "en": "What does this value mean?"},
                "body": {
                    "es": "Muestra el **volumen absoluto** de tráfico de datos (teal) y voz (azul) por trimestre.\n\n• **{series}** en **{name}** = **{value}**\n• El tráfico de datos domina crecientemente sobre la voz.",
                    "en": "Shows the **absolute volume** of data traffic (teal) and voice (blue) per quarter.\n\n• **{series}** in **{name}** = **{value}**\n• Data traffic increasingly dominates voice.",
                },
            },
            {
                "heading": {"es": "Tendencia", "en": "Trend"},
                "body": {
                    "es": "Crecimiento exponencial impulsado por video streaming (YouTube, Netflix) y plataformas OTT (WhatsApp, TikTok). La voz pierde peso relativo año a año.",
                    "en": "Exponential growth driven by video streaming (YouTube, Netflix) and OTT platforms (WhatsApp, TikTok). Voice shrinks in relative share year over year.",
                },
                "caption": {"es": "Fuente: CNMC Datos de Mercado", "en": "Source: CNMC Market Data"},
            },
        ],
    },
    "hhi": {
        "title": {"es": "Índice HHI de Concentración", "en": "HHI Concentration Index"},
        "sections": [
            {
                "heading": {"es": "¿Qué significa este valor?", "en": "What does this value mean?"},
                "body": {
                    "es": "El **HHI** mide la concentración del mercado (0-10.000).\n\n• **{series}** en **{name}** = **{value}**\n• **<1.000:** mercado competitivo\n• **1.000–2.500:** concentración moderada\n• **>2.500:** altamente concentrado",
                    "en": "**HHI** measures market concentration (0-10,000).\n\n• **{series}** in **{name}** = **{value}**\n• **<1,000:** competitive market\n• **1,000–2,500:** moderate concentration\n• **>2,500:** highly concentrated",
                },
            },
            {
                "heading": {"es": "¿Por qué importa?", "en": "Why does it matter?"},
                "body": {
                    "es": "H2 planteaba que la concentración causa el Efecto Tijera. Pero el HHI **bajó** mientras la brecha **subió**. La concentración no es la causa — el problema es estructural del modelo TELCO.",
                    "en": "H2 hypothesized that concentration causes the Scissors Effect. But HHI **dropped** while the gap **rose**. Concentration isn't the cause — the problem is structural to the TELCO business model.",
                },
                "caption": {"es": "Fuente: CNMC Datos de Mercado · Líneas punteadas: umbrales DOJ/FTC", "en": "Source: CNMC Market Data · Dashed lines: DOJ/FTC thresholds"},
            },
        ],
    },
    "nsi_arpu": {
        "title": {"es": "NSI vs ARPU", "en": "NSI vs ARPU"},
        "sections": [
            {
                "heading": {"es": "¿Qué significa este valor?", "en": "What does this value mean?"},
                "body": {
                    "es": "Cada punto es un trimestre. **Eje X:** NSI (presión sobre la red), **Eje Y:** ARPU (ingreso por línea).\n\n• **{series}** en **{name}** = **{value}**\n• El tamaño del punto = número de líneas activas.",
                    "en": "Each dot is one quarter. **X-axis:** NSI (network pressure), **Y-axis:** ARPU (revenue per line).\n\n• **{series}** in **{name}** = **{value}**\n• Dot size = active lines count.",
                },
            },
            {
                "heading": {"es": "Correlación negativa", "en": "Negative correlation"},
                "body": {
                    "es": "A medida que el NSI sube (más estrés de red), el ARPU tiende a bajar. Esto confirma la **paradoja TELCO**: más uso de la red → menos ingresos por usuario.",
                    "en": "As NSI rises (more network stress), ARPU tends to fall. This confirms the **TELCO paradox**: more network usage → less revenue per user.",
                },
                "caption": {"es": "Fuente: CNMC · Usa el slider de año para ver la evolución", "en": "Source: CNMC · Use the year slider to see evolution"},
            },
        ],
    },
    "capex": {
        "title": {"es": "CAPEX Per Cápita", "en": "CAPEX Per Capita"},
        "sections": [
            {
                "heading": {"es": "¿Qué significa este valor?", "en": "What does this value mean?"},
                "body": {
                    "es": "**Inversión en infraestructura** por habitante en EUR.\n\n• **{name}** = **{value}**\n• Europa invierte ~118€, EE.UU. ~226€. Casi la mitad.",
                    "en": "**Infrastructure investment** per capita in EUR.\n\n• **{name}** = **{value}**\n• Europe invests ~€118, the US ~€226. Almost half.",
                },
            },
            {
                "heading": {"es": "Implicación regulatoria", "en": "Regulatory implication"},
                "body": {
                    "es": "Sin inversión equivalente, Europa no podrá cerrar la brecha digital ni cumplir los objetivos de la Década Digital 2030. El Fair Share liberaría recursos para inversión.",
                    "en": "Without equivalent investment, Europe can't close the digital divide or meet Digital Decade 2030 targets. Fair Share would free resources for investment.",
                },
                "caption": {"es": "Fuente: ETNO State of Digital Communications 2025", "en": "Source: ETNO State of Digital Communications 2025"},
            },
        ],
    },
    "arpu": {
        "title": {"es": "ARPU Móvil", "en": "Mobile ARPU"},
        "sections": [
            {
                "heading": {"es": "¿Qué significa este valor?", "en": "What does this value mean?"},
                "body": {
                    "es": "**Ingreso promedio por línea móvil** en EUR/mes.\n\n• **{name}** = **{value}**\n• El ARPU europeo es ~3x menor que el de USA.",
                    "en": "**Average revenue per mobile line** in EUR/month.\n\n• **{name}** = **{value}**\n• European ARPU is ~3x lower than the US.",
                },
            },
            {
                "heading": {"es": "¿Por qué importa?", "en": "Why does it matter?"},
                "body": {
                    "es": "El ARPU bajo limita la capacidad de inversión de los operadores europeos. Es la otra cara del Efecto Tijera: más tráfico, mismos ingresos.",
                    "en": "Low ARPU limits European operators' investment capacity. It's the other side of the Scissors Effect: more traffic, same revenue.",
                },
                "caption": {"es": "Fuente: ETNO State of Digital Communications 2025", "en": "Source: ETNO State of Digital Communications 2025"},
            },
        ],
    },
    "g5_gauge": {
        "title": {"es": "Adopción 5G", "en": "5G Adoption"},
        "sections": [
            {
                "heading": {"es": "¿Qué significa este valor?", "en": "What does this value mean?"},
                "body": {
                    "es": "**{value}** de las conexiones móviles son 5G.\n\n• El indicador mide adopción real (suscriptores 5G / total), no cobertura.\n• La cobertura 5G en Europa es alta (>80%), pero la adopción va más lenta.",
                    "en": "**{value}** of mobile connections are 5G.\n\n• This measures actual adoption (5G subscribers / total), not coverage.\n• 5G coverage in Europe is high (>80%), but adoption is slower.",
                },
            },
            {
                "heading": {"es": "Objetivo 2030", "en": "2030 Target"},
                "body": {
                    "es": "La Década Digital Europea fija el objetivo de **100% de cobertura 5G** para 2030. La adopción debe acelerarse para justificar la inversión en infraestructura.",
                    "en": "The European Digital Decade sets a **100% 5G coverage** target for 2030. Adoption must accelerate to justify infrastructure investment.",
                },
                "caption": {"es": "Fuente: EU 5G Observatory 2025", "en": "Source: EU 5G Observatory 2025"},
            },
        ],
    },
    "fair_share_before": {
        "title": {"es": "Sin Fair Share", "en": "Without Fair Share"},
        "sections": [
            {
                "heading": {"es": "Escenario actual", "en": "Current scenario"},
                "body": {
                    "es": "**Brecha: {value}**\n\nSin intervención, la divergencia entre tráfico e ingresos sigue creciendo. Los operadores asumen todo el coste de la red mientras las plataformas OTT usan la infraestructura sin contribuir.",
                    "en": "**Gap: {value}**\n\nWithout intervention, the divergence between traffic and revenue keeps growing. Operators bear all network costs while OTT platforms use the infrastructure without contributing.",
                },
            },
        ],
    },
    "fair_share_after": {
        "title": {"es": "Con Fair Share", "en": "With Fair Share"},
        "sections": [
            {
                "heading": {"es": "Impacto de la política", "en": "Policy impact"},
                "body": {
                    "es": "**Brecha restante: {value}**\n\nCon la contribución OTT simulada, la brecha se reduce significativamente. Los parámetros actuales de la simulación se ajustan desde la barra lateral.",
                    "en": "**Remaining gap: {value}**\n\nWith the simulated OTT contribution, the gap is significantly reduced. Current simulation parameters are adjustable from the sidebar.",
                },
            },
        ],
    },
    "scenarios": {
        "title": {"es": "Comparativa de Escenarios", "en": "Scenario Comparison"},
        "sections": [
            {
                "heading": {"es": "¿Qué significa este valor?", "en": "What does this value mean?"},
                "body": {
                    "es": "**{series}** en **{name}** = **{value}**\n\n• **Gap (rojo):** brecha sin cerrar\n• **Closed (verde):** brecha que se cierra\n• **Remaining (ámbar):** lo que persiste",
                    "en": "**{series}** in **{name}** = **{value}**\n\n• **Gap (red):** unclosed gap\n• **Closed (green):** gap that gets closed\n• **Remaining (amber):** what persists",
                },
            },
        ],
    },
}
