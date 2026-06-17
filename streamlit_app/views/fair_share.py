import streamlit as st
import pandas as pd
from utils.data_loader import get_kpis
from utils.calculations import calculate_fair_share_impact
from components.filters import render_sidebar
from components.kpi_card import kpi_row
from utils.i18n import t, lang
import plotly.graph_objects as go
from components.explain_popup import CLICK_FORMAT, maybe_popup


def _gauge_chart(value: float, max_val: float, color: str, label: str):
    options = {
        "series": [{
            "type": "gauge",
            "startAngle": 200,
            "endAngle": -20,
            "center": ["50%", "55%"],
            "radius": "85%",
            "min": 0,
            "max": max_val,
            "splitNumber": 4,
            "progress": {
                "show": True,
                "width": 16,
                "roundCap": True,
                "itemStyle": {"color": color},
            },
            "pointer": {"show": False},
            "axisLine": {
                "lineStyle": {"width": 16, "color": [[1, "rgba(255,255,255,0.06)"]]},
            },
            "axisTick": {"show": False},
            "splitLine": {"show": False},
            "axisLabel": {"show": False},
            "detail": {
                "valueAnimation": True,
                "formatter": "{value}" + (" pp" if "pp" in label else "%"),
                "color": "#ECEFF1",
                "fontSize": 28,
                "fontWeight": "bold",
                "offsetCenter": [0, "30%"],
            },
            "title": {
                "offsetCenter": [0, "65%"],
                "fontSize": 13,
                "color": "#90A4AE",
            },
            "data": [{"value": round(value, 1), "name": label}],
        }]
    }
    return options


def render():
    L = lang()
    filters = render_sidebar()
    kpis = get_kpis()

    impact = calculate_fair_share_impact(
        kpis["cagr_gap"], filters["ott_pct"],
        filters["capex_relief"], filters["traffic_adj"]
    )

    # ── OPENING ──
    st.markdown(f"""
    <div class="story-chapter emerald">
      <span class="chapter-badge">Capítulo 4</span>
      <h2 class="chapter-title">{t('fair_share.title', L)}</h2>
      <p class="chapter-subtitle">{t('fair_share.subtitle', L)}</p>
    </div>
    """, unsafe_allow_html=True)

    # ── THE PROBLEM STATEMENT ──
    st.markdown("""
    <div class="insight-box coral">
      <b>⚠ El problema está claro:</b> El tráfico crece +12.000%, los ingresos no. La red se estrella.
      Los operadores invierten la mitad que EE.UU. Alguien tiene que pagar por la red que todos usamos.
    </div>
    """, unsafe_allow_html=True)

    # ── SIDE-BY-SIDE: Before vs After gauges ──
    original_gap_pp = kpis["cagr_gap"] * 100
    adjusted_gap_pp = impact["total_gap_pp"]
    gauge_max = max(original_gap_pp, adjusted_gap_pp, 10)

    col_before, col_arrow, col_after = st.columns([5, 1, 5])

    with col_before:
        st.markdown('<div class="chart-container" style="text-align:center;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.9rem;color:#FF5252;font-weight:700;text-transform:uppercase;letter-spacing:1px;">❌ Sin Fair Share</div>', unsafe_allow_html=True)
        from streamlit_echarts import st_echarts
        r_before = st_echarts(options=_gauge_chart(original_gap_pp, gauge_max, "#FF5252", ""), height="220px", events={"click": CLICK_FORMAT}, key="fs_before")
        maybe_popup("fair_share_before", r_before, "fs_before")
        st.markdown(f'<div style="font-size:1.3rem;color:#FF5252;font-weight:700;">Brecha: {original_gap_pp:.1f} pp</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.8rem;color:#637381;">El gap sigue creciendo. La red colapsa.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_arrow:
        st.markdown("""
        <div style="display:flex;align-items:center;justify-content:center;height:100%;font-size:2.5rem;color:#FFD740;">
          →
        </div>
        """, unsafe_allow_html=True)

    with col_after:
        st.markdown('<div class="chart-container" style="text-align:center;">', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:0.9rem;color:#00BFA5;font-weight:700;text-transform:uppercase;letter-spacing:1px;">✅ Con Fair Share ({filters["ott_pct"]*100:.0f}% OTT)</div>', unsafe_allow_html=True)
        remaining = max(impact["remaining_gap_pp"], 0)
        from streamlit_echarts import st_echarts
        r_after = st_echarts(options=_gauge_chart(remaining, gauge_max, "#00BFA5", ""), height="220px", events={"click": CLICK_FORMAT}, key="fs_after")
        maybe_popup("fair_share_after", r_after, "fs_after")
        st.markdown(f'<div style="font-size:1.3rem;color:#00BFA5;font-weight:700;">Brecha restante: {remaining:.1f} pp</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:0.8rem;color:#637381;">Se cierra {impact["gap_closed_pp"]:.0f} pp con Fair Share</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

    # ── OTT TRAFFIC DONUT ──
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="chart-title">📊 {t("fair_share.ott_share_title", L)}</div>', unsafe_allow_html=True)
    from components.charts import ott_donut_echarts
    from streamlit_echarts import st_echarts
    donut_result = st_echarts(options=ott_donut_echarts(), height="320px", events={"click": CLICK_FORMAT}, key="ott_donut")
    maybe_popup("ott_donut", donut_result, "ott_donut")
    st.markdown(f'<div style="font-size:0.75rem;color:#637381;text-align:center;">{t("fair_share.ott_share_caption", L)}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── IMPACT METRICS ──
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="chart-title" style="font-size:1rem;">📊 {t("fair_share.scenario_title", L)}</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="kpi-card coral" style="text-align:center;padding:1rem;">
          <div class="kpi-label">📐 {t('fair_share.gap_cagr', L)}</div>
          <div class="kpi-value">{kpis['cagr_gap']*100:.1f} pp</div>
          <div class="kpi-delta negative" style="font-size:0.75rem;">{t('fair_share.gap_cagr_desc', L)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="kpi-card emerald" style="text-align:center;padding:1rem;">
          <div class="kpi-label">✅ {t('fair_share.gap_closed', L)}</div>
          <div class="kpi-value">{impact['gap_closed_pp']:.1f} pp</div>
          <div class="kpi-delta positive" style="font-size:0.75rem;">{filters['ott_pct']*100:.0f}% OTT contribution</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="kpi-card teal" style="text-align:center;padding:1rem;">
          <div class="kpi-label">📉 {t('fair_share.remaining_gap', L)}</div>
          <div class="kpi-value">{max(impact['remaining_gap_pp'], 0):.1f} pp</div>
          <div class="kpi-delta neutral" style="font-size:0.75rem;">{t('fair_share.remaining_gap_desc', L)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="kpi-card amber" style="text-align:center;padding:1rem;">
          <div class="kpi-label">🔧 {t('fair_share.capex_savings', L)}</div>
          <div class="kpi-value">{impact['capex_savings_pct']:.0f}%</div>
          <div class="kpi-delta neutral" style="font-size:0.75rem;">{filters['capex_relief']*100:.0f}% CAPEX relief</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── SCENARIO COMPARISON CHART ──
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="chart-title">📈 {t("fair_share.comparison_title", L)}</div>', unsafe_allow_html=True)

    scenarios = pd.DataFrame([
        {"Scenario": t("fair_share.baseline", L), "Gap pp": original_gap_pp,
         "Closed pp": 0, "Remaining pp": original_gap_pp},
        {"Scenario": t("fair_share.ott_scenario", L).format(filters['ott_pct']*100), "Gap pp": adjusted_gap_pp,
         "Closed pp": impact["gap_closed_pp"], "Remaining pp": impact["remaining_gap_pp"]},
        {"Scenario": t("fair_share.ott_capex_scenario", L).format(filters['capex_relief']*100), "Gap pp": adjusted_gap_pp,
         "Closed pp": impact["gap_closed_pp"] + impact["capex_savings_pct"],
         "Remaining pp": max(0, adjusted_gap_pp - impact["gap_closed_pp"] - impact["capex_savings_pct"])},
    ])

    fig = go.Figure()
    fig.add_trace(go.Bar(name="🔴 Gap (pp)", x=scenarios["Scenario"], y=scenarios["Gap pp"],
                         marker_color="#FF5252",
                         hovertemplate="Gap: %{y:.1f} pp<extra></extra>"))
    fig.add_trace(go.Bar(name="🟢 Closed (pp)", x=scenarios["Scenario"], y=scenarios["Closed pp"],
                         marker_color="#00E676",
                         hovertemplate="Closed: %{y:.1f} pp<extra></extra>"))
    fig.add_trace(go.Bar(name="🟡 Remaining (pp)", x=scenarios["Scenario"], y=scenarios["Remaining pp"],
                         marker_color="#FFD740",
                         hovertemplate="Remaining: %{y:.1f} pp<extra></extra>"))
    fig.update_layout(barmode="group", height=380,
                      yaxis_title="Percentage Points",
                      hovermode="x unified")
    from components.charts import apply_corporate_style
    s_click = st.plotly_chart(apply_corporate_style(fig), width="stretch", config={"displayModeBar": False}, on_select="rerun", key="scenarios_chart")
    if s_click and s_click.selection and s_click.selection.points:
        pt = s_click.selection.points[0]
        maybe_popup("scenarios", {"name": pt.get("x", ""), "value": pt.get("y", ""), "seriesName": pt.get("legendgroup", "")}, "scenarios_chart")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── THE CALL TO ACTION ──
    st.markdown("""
    <div class="insight-box emerald">
      <b>🎯 La conclusión es inevitable:</b> Con una contribución OTT del <b>30%</b> y alivio CAPEX del <b>20%</b>,
      la brecha se reduce drásticamente. El sector respira. La red se sostiene.
      <b>Fair Share no es un impuesto. Es inversión en infraestructura digital europea.</b>
    </div>
    """, unsafe_allow_html=True)

    # ── LIMITATIONS ──
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="chart-title">⚠️ {t("fair_share.limitations_title", L)}</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:0.85rem;color:#90A4AE;">
      <p>{t('fair_share.limitations', L)}</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:right;padding:0.5rem 1rem;margin-top:0.5rem;font-size:0.9rem;color:#90A4AE;font-style:italic;border-top:1px solid rgba(255,255,255,0.04);">
      {t('fair_share.transition', L)} <span style="color:#00E676;">→</span>
    </div>
    """, unsafe_allow_html=True)
