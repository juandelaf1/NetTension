import streamlit as st
from utils.data_loader import load_fact_observed, load_hhi, filter_by_year, get_kpis
from components.charts import nsi_vs_arpu_scatter, hhi_chart_echarts
from components.kpi_card import kpi_row
from components.filters import render_sidebar
from utils.calculations import calculate_network_stress_metrics
from utils.i18n import t, lang
from components.explain_popup import CLICK_FORMAT, maybe_popup


def filter_by_hhi_year(hhi_df, year_range):
    yr_min, yr_max = year_range
    return hhi_df[(hhi_df["year"] >= yr_min) & (hhi_df["year"] <= yr_max)]


def render():
    L = lang()
    filters = render_sidebar()
    kpis = get_kpis()
    fact = filter_by_year(load_fact_observed(), filters["year_range"])
    hhi = filter_by_hhi_year(load_hhi(), filters["year_range"])
    stress = calculate_network_stress_metrics(fact)

    first_hhi = hhi["hhi"].iloc[0] if len(hhi) > 0 else 0
    last_hhi = hhi["hhi"].iloc[-1] if len(hhi) > 0 else 0
    hhi_change = last_hhi - first_hhi

    # ── OPENING: The counterintuitive finding ──
    st.markdown(f"""
    <div class="story-chapter coral">
      <span class="chapter-badge">Capítulo 2</span>
      <h2 class="chapter-title">{t('network_stress.title', L)}</h2>
      <p class="chapter-subtitle">{t('network_stress.subtitle', L)}</p>
    </div>
    """, unsafe_allow_html=True)

    # ── SHOWCASE: The paradox ──
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown(f"""
        <div class="showcase-stat">
          <div class="number amber">{first_hhi:.0f} → {last_hhi:.0f}</div>
          <div class="label">📊 HHI: {'less concentration' if L == 'en' else 'menos concentración'} ({hhi_change:+.0f})</div>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <div class="showcase-stat">
          <div class="number coral">{stress['nsi_current']:.4f}</div>
          <div class="label">📶 NSI ({'network stress' if L == 'en' else 'estrés de red'})</div>
        </div>
        """, unsafe_allow_html=True)
    with col_c:
        st.markdown(f"""
        <div class="showcase-stat">
          <div class="number blue">€{stress['arpu_current']*1e6:,.2f}</div>
          <div class="label">💳 ARPU</div>
        </div>
        """, unsafe_allow_html=True)



    # ── KPI Cards ──
    kpi_row([
        dict(label=t("network_stress.kpi_hhi", L), value=f"{last_hhi:.0f}",
             delta=f"{hhi_change:+.0f} vs 2005", delta_color="positive" if hhi_change < 0 else "negative",
             icon="📊", help_text=t("network_stress.kpi_hhi_desc", L), color="amber"),
        dict(label=t("network_stress.kpi_nsi", L), value=f"{stress['nsi_current']:.4f}",
             delta=f"vs 2005", delta_color="negative",
             icon="📶", help_text=t("network_stress.kpi_nsi_desc", L), color="coral"),
        dict(label=t("network_stress.kpi_arpu", L), value=f"€{stress['arpu_current']*1e6:,.2f}",
             delta=f"vs 2005", delta_color="negative",
             icon="💳", help_text=t("network_stress.kpi_arpu_desc", L), color="coral"),
        dict(label=t("network_stress.kpi_lines", L), value=f"{stress['lines_current']:,.0f}",
             delta="total accesos" if L == "es" else "total accesses", delta_color="neutral",
             icon="📡", help_text=t("network_stress.kpi_lines_desc", L), color="teal"),
    ])

    # ── HHI CHART ──
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown(f'<div class="chart-title">📊 {t("network_stress.hhi_title", L)}</div>', unsafe_allow_html=True)
        from streamlit_echarts import st_echarts
        result_hhi = st_echarts(options=hhi_chart_echarts(hhi, L), height="400px", events={"click": CLICK_FORMAT}, key="hhi")
        maybe_popup("hhi", result_hhi, "hhi")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── NSI vs ARPU animated scatter ──
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown(f'<div class="chart-title">🎯 {t("network_stress.nsi_title", L)}</div>', unsafe_allow_html=True)
        fig2 = nsi_vs_arpu_scatter(fact, L)
        result_nsi = st.plotly_chart(fig2, width="stretch", config={"displayModeBar": False}, on_select="rerun", key="nsi_arpu")
        if result_nsi and result_nsi.selection and result_nsi.selection.points:
            pt = result_nsi.selection.points[0]
            click_data = {"name": pt.get("x"), "value": pt.get("y"), "seriesName": "NSI vs ARPU"}
            maybe_popup("nsi_arpu", click_data, "nsi_arpu")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── THE BIG INSIGHT: H2 refuted ──
    st.markdown(f"""
    <div class="insight-box violet">
      <b>🔬 {t('network_stress.key_insight_title', L)}:</b> {t('network_stress.key_insight', L)}
    </div>
    """, unsafe_allow_html=True)

    # ── "ONE MORE THING" ──
    st.markdown(f"""
    <div class="insight-box coral">
      <b>🎯 {t('network_stress.transition', L)}</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:right;padding:0.5rem 1rem;margin-top:0.5rem;font-size:0.9rem;color:#8B949E;font-style:italic;border-top:1px solid rgba(255,255,255,0.04);">
      {t('network_stress.transition', L)} <span style="color:#CF3B30;">→</span>
    </div>
    """, unsafe_allow_html=True)

    from utils.export import download_button
    col1, col2 = st.columns(2)
    with col1:
        download_button(hhi, "nettension_hhi.csv")
    with col2:
        download_button(fact[["trimestre_dt", "nsi", "revenue_per_line"]], "nettension_nsi_arpu.csv")
