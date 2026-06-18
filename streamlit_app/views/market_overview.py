import streamlit as st
import pandas as pd
from utils.data_loader import load_fact_observed, get_kpis, filter_by_year
from components.charts import traffic_revenue_stacked_echarts
from components.kpi_card import kpi_row
from components.filters import render_sidebar
from utils.i18n import t, lang
from components.explain_popup import CLICK_FORMAT, maybe_popup


def _render_echarts_scissors(fact: pd.DataFrame, L: str) -> None:
    categories = fact["trimestre_dt"].dt.strftime("%Y Q%q").tolist()
    traffic = fact["data_traffic_index"].round(1).tolist()
    revenue = fact["revenue_index"].round(1).tolist()
    gap = [(t - r) for t, r in zip(traffic, revenue)]
    t_traffic = t("charts.traffic_index", L)
    t_revenue = t("charts.revenue_index", L)
    t_gap = t("charts.gap", L)
    t_click = t("charts.click_value", L)

    options = {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "cross", "label": {"backgroundColor": "#161B22"}},
            "formatter": f"""function(params) {{
                let tip = '<b>' + params[0].axisValue + '</b><br/>';
                let tv = params[0].value, rv = params[1].value, gv = params[2].value;
                tip += params[0].marker + ' {t_traffic}: <b>' + tv.toFixed(1) + '</b> (2005=100)<br/>';
                tip += params[1].marker + ' {t_revenue}: <b>' + rv.toFixed(1) + '</b> (2005=100)<br/>';
                tip += '<hr style="margin:4px 0"/>';
                tip += '✂️ {t_gap}: <b>' + gv.toFixed(1) + ' pp</b><br/>';
                tip += '<span style="font-size:0.75rem;color:#8B949E;">{t_click}: ' + gv.toFixed(1) + ' pp</span>';
                return tip;
            }}"""
        },
        "legend": {
            "data": ["📈 " + t_traffic, "💰 " + t_revenue, "✂️ " + t_gap],
            "textStyle": {"color": "#8B949E", "fontSize": 12},
            "top": 5,
        },
        "grid": {"left": "3%", "right": "4%", "bottom": "8%", "containLabel": True, "top": "18%"},
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": categories,
            "axisLine": {"lineStyle": {"color": "rgba(255,255,255,0.08)"}},
            "axisLabel": {"color": "#8B949E", "rotate": 45, "fontSize": 10},
            "splitLine": {"show": False},
        },
        "yAxis": [
            {
                "type": "value",
                "name": t_traffic + " (2005 = 100)",
                "nameTextStyle": {"color": "#D97724", "fontSize": 11},
                "axisLine": {"lineStyle": {"color": "#D97724"}},
                "splitLine": {"lineStyle": {"color": "rgba(255,255,255,0.04)", "type": "dashed"}},
                "axisLabel": {"color": "#8B949E"},
            },
            {
                "type": "value",
                "name": t_revenue + " (2005 = 100)",
                "nameTextStyle": {"color": "#CF3B30", "fontSize": 11},
                "axisLine": {"lineStyle": {"color": "#CF3B30"}},
                "splitLine": {"show": False},
                "axisLabel": {"color": "#8B949E"},
            },
        ],
        "series": [
            {
                "name": "📈 " + t_traffic,
                "type": "line",
                "smooth": True,
                "symbol": "circle",
                "symbolSize": 4,
                "data": traffic,
                "lineStyle": {"color": "#D97724", "width": 3},
                "itemStyle": {"color": "#D97724"},
                "areaStyle": {"color": "rgba(217,119,36,0.08)"},
                "markPoint": {
                    "data": [
                        {"type": "max", "name": t("charts.max", L)},
                        {"type": "min", "name": t("charts.min", L)},
                    ]
                },
            },
            {
                "name": "💰 " + t_revenue,
                "type": "line",
                "smooth": True,
                "yAxisIndex": 1,
                "symbol": "diamond",
                "symbolSize": 6,
                "data": revenue,
                "lineStyle": {"color": "#CF3B30", "width": 3, "type": "dashed"},
                "itemStyle": {"color": "#CF3B30"},
                "areaStyle": {"color": "rgba(207,59,48,0.08)"},
            },
            {
                "name": "✂️ " + t_gap,
                "type": "bar",
                "yAxisIndex": 0,
                "data": gap,
                "itemStyle": {
                    "color": {
                        "type": "linear",
                        "x": 0, "y": 0, "x2": 0, "y2": 1,
                        "colorStops": [
                            {"offset": 0, "color": "rgba(217,119,36,0.6)"},
                            {"offset": 1, "color": "rgba(207,59,48,0.3)"},
                        ],
                    }
                },
                "barWidth": "40%",
            },
        ],
    }
    ev_key = "scissors"
    from streamlit_echarts import st_echarts
    result = st_echarts(options=options, height="500px", events={"click": CLICK_FORMAT}, key=ev_key)
    maybe_popup("scissors", result, ev_key)


def render():
    L = lang()
    filters = render_sidebar()
    kpis = get_kpis()
    fact = filter_by_year(load_fact_observed(), filters["year_range"])

    # ── OPENING: Bold keynote-style headline ──
    st.markdown(f"""
    <div class="story-chapter">
      <span class="chapter-badge">{t('market_overview.title', L)}</span>
      <h2 class="chapter-title">{t('market_overview.scissors_title', L).split(':')[0]}</h2>
      <p class="chapter-subtitle">{t('market_overview.subtitle', L)}</p>
    </div>
    """, unsafe_allow_html=True)

    # ── DATASET OVERVIEW ──
    n_rows = len(fact)
    yr_min = int(fact["year"].min())
    yr_max = int(fact["year"].max())
    n_cols = len(fact.columns)
    traffic_max = fact["data_traffic"].max()
    revenue_total = fact["revenue"].sum()
    st.markdown(f"""
    <div style="display:flex;flex-wrap:wrap;gap:0.5rem;margin-bottom:1.5rem;align-items:center;">
      <span class="data-badge">📦 {n_rows} {t('market_overview.quarter_col', L)} · {n_cols} {'variables' if L == 'es' else 'variables'}</span>
      <span class="data-badge">📅 {yr_min}–{yr_max}</span>
      <span class="data-badge">📊 CNMC · Eurostat · ETNO · GSMA</span>
      <span class="data-badge">🔬 5 {'hipótesis' if L == 'es' else 'hypotheses'}</span>
    </div>
    """, unsafe_allow_html=True)

    # ── SHOWCASE: Two dramatic stats side by side ──
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown(f"""
        <div class="showcase-stat">
          <div class="number teal">+{kpis['traffic_cagr']*100:.0f}%</div>
          <div class="label">📈 {t('market_overview.kpi_traffic_cagr', L)} / {'año' if L == 'es' else 'year'}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <div class="showcase-stat">
          <div class="number coral">{kpis['rev_cagr']*100:.1f}%</div>
          <div class="label">💰 {t('market_overview.kpi_rev_cagr', L)} / {'año' if L == 'es' else 'year'}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_c:
        st.markdown(f"""
        <div class="showcase-stat">
          <div class="number amber">✂️ {kpis['cagr_gap']*100:.1f} pp</div>
          <div class="label">⚠ {t('market_overview.kpi_cagr_gap', L)}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── KPI Cards ──
    kpi_row([
        dict(label=t("market_overview.kpi_traffic_cagr", L), value=f"{kpis['traffic_cagr']:.1%}",
             delta=t("market_overview.traffic_cagr_delta", L), delta_color="positive",
             icon="📈", sparkline_data=fact["data_traffic_index"].tail(20).tolist(),
             help_text=t("market_overview.kpi_traffic_cagr_desc", L), color="teal"),
        dict(label=t("market_overview.kpi_rev_cagr", L), value=f"{kpis['rev_cagr']:.1%}",
             delta=t("market_overview.rev_cagr_delta", L), delta_color="negative",
             icon="💰", sparkline_data=fact["revenue_index"].tail(20).tolist(),
             help_text=t("market_overview.kpi_rev_cagr_desc", L), color="coral"),
        dict(label=t("market_overview.kpi_cagr_gap", L), value=f"{kpis['cagr_gap']:.1%}",
             delta=t("market_overview.cagr_gap_delta", L), delta_color="negative",
             icon="✂️", sparkline_data=(fact["data_traffic_index"] - fact["revenue_index"]).tail(20).tolist(),
             help_text=t("market_overview.kpi_cagr_gap_desc", L), color="amber"),
        dict(label=t("market_overview.kpi_avg_arpu", L), value=f"€{kpis['avg_arpu']*1e6:,.0f}/line",
             delta=t("market_overview.arpu_delta", L), delta_color="negative",
             icon="💳", sparkline_data=fact["revenue_per_line"].tail(20).tolist(),
             help_text=t("market_overview.kpi_avg_arpu_desc", L), color="coral"),
    ])

    # ── THE BIG CHART: Scissors ECharts ──
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    _render_echarts_scissors(fact, L)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── INSIGHT BOX: The takeaway ──
    cagr_gap_pct = kpis['cagr_gap'] * 100
    st.markdown(f"""
    <div class="insight-box coral">
      <b>🔑 {t('market_overview.kpi_cagr_gap', L)}:</b> {t('market_overview.kpi_cagr_gap_desc', L)}
    </div>
    """, unsafe_allow_html=True)

    # ── SECONDARY CHART: Traffic volume ──
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="chart-title">📦 {t("market_overview.traffic_volume_title", L)}</div>', unsafe_allow_html=True)
    from streamlit_echarts import st_echarts
    result2 = st_echarts(options=traffic_revenue_stacked_echarts(fact, L), height="400px", events={"click": CLICK_FORMAT}, key="traffic_vol")
    maybe_popup("traffic_volume", result2, "traffic_vol")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── "ONE MORE THING" ──
    st.markdown(f"""
    <div class="insight-box amber" style="margin-top:1rem;">
      <b>🎯 {t('market_overview.title', L)}:</b> {t('market_overview.subtitle', L)}
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:right;padding:0.5rem 1rem;margin-top:0.5rem;font-size:0.9rem;color:#8B949E;font-style:italic;border-top:1px solid rgba(255,255,255,0.04);">
      {t('market_overview.transition', L)} <span style="color:#D97724;">→</span>
    </div>
    """, unsafe_allow_html=True)

    from utils.export import download_button
    download_button(fact, "nettension_market_overview.csv")
