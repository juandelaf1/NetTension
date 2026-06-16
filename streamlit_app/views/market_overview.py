import streamlit as st
import pandas as pd
from utils.data_loader import load_fact_observed, get_kpis, filter_by_year
from components.charts import traffic_revenue_stacked_echarts
from components.kpi_card import kpi_row
from components.filters import render_sidebar
from utils.i18n import t, lang
from streamlit_echarts import st_echarts
from components.explain_popup import CLICK_FORMAT, maybe_popup


def _render_echarts_scissors(fact: pd.DataFrame) -> None:
    categories = fact["trimestre_dt"].dt.strftime("%Y Q%q").tolist()
    traffic = fact["data_traffic_index"].round(1).tolist()
    revenue = fact["revenue_index"].round(1).tolist()
    gap = [(t - r) for t, r in zip(traffic, revenue)]

    options = {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "cross", "label": {"backgroundColor": "#1A2236"}},
            "formatter": """function(params) {
                let tip = '<b>' + params[0].axisValue + '</b><br/>';
                let t = params[0].value, r = params[1].value, g = params[2].value;
                tip += params[0].marker + ' Traffic: <b>' + t.toFixed(1) + '</b> (2005=100)<br/>';
                tip += params[1].marker + ' Revenue: <b>' + r.toFixed(1) + '</b> (2005=100)<br/>';
                tip += '<hr style="margin:4px 0"/>';
                tip += '✂️ Gap: <b>' + g.toFixed(1) + ' pp</b><br/>';
                tip += '<span style="font-size:0.75rem;color:#90A4AE;">';
                if (g > 0) {
                    tip += '⚠ El tráfico crece ' + g.toFixed(1) + ' pp más que los ingresos';
                } else {
                    tip += '📊 Ingresos y tráfico alineados';
                }
                tip += '</span>';
                return tip;
            }"""
        },
        "legend": {
            "data": ["📈 Traffic Index", "💰 Revenue Index", "✂️ Gap"],
            "textStyle": {"color": "#90A4AE", "fontSize": 12},
            "top": 5,
        },
        "grid": {"left": "3%", "right": "4%", "bottom": "8%", "containLabel": True, "top": "18%"},
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": categories,
            "axisLine": {"lineStyle": {"color": "rgba(255,255,255,0.08)"}},
            "axisLabel": {"color": "#90A4AE", "rotate": 45, "fontSize": 10},
            "splitLine": {"show": False},
        },
        "yAxis": [
            {
                "type": "value",
                "name": "Traffic Index (2005 = 100)",
                "nameTextStyle": {"color": "#00BFA5", "fontSize": 11},
                "axisLine": {"lineStyle": {"color": "#00BFA5"}},
                "splitLine": {"lineStyle": {"color": "rgba(255,255,255,0.04)", "type": "dashed"}},
                "axisLabel": {"color": "#90A4AE"},
            },
            {
                "type": "value",
                "name": "Revenue Index (2005 = 100)",
                "nameTextStyle": {"color": "#FF5252", "fontSize": 11},
                "axisLine": {"lineStyle": {"color": "#FF5252"}},
                "splitLine": {"show": False},
                "axisLabel": {"color": "#90A4AE"},
            },
        ],
        "series": [
            {
                "name": "📈 Traffic Index",
                "type": "line",
                "smooth": True,
                "symbol": "circle",
                "symbolSize": 4,
                "data": traffic,
                "lineStyle": {"color": "#00BFA5", "width": 3, "shadowBlur": 10, "shadowColor": "rgba(0,191,165,0.3)"},
                "itemStyle": {"color": "#00BFA5"},
                "areaStyle": {"color": "rgba(0,191,165,0.05)"},
                "markPoint": {
                    "data": [
                        {"type": "max", "name": "Max"},
                        {"type": "min", "name": "Min"},
                    ]
                },
            },
            {
                "name": "💰 Revenue Index",
                "type": "line",
                "smooth": True,
                "yAxisIndex": 1,
                "symbol": "diamond",
                "symbolSize": 6,
                "data": revenue,
                "lineStyle": {"color": "#FF5252", "width": 3, "type": "dashed", "shadowBlur": 10, "shadowColor": "rgba(255,82,82,0.3)"},
                "itemStyle": {"color": "#FF5252"},
                "areaStyle": {"color": "rgba(255,82,82,0.05)"},
            },
            {
                "name": "✂️ Gap",
                "type": "bar",
                "yAxisIndex": 0,
                "data": gap,
                "itemStyle": {
                    "color": {
                        "type": "linear",
                        "x": 0, "y": 0, "x2": 0, "y2": 1,
                        "colorStops": [
                            {"offset": 0, "color": "rgba(255,215,64,0.6)"},
                            {"offset": 1, "color": "rgba(255,82,82,0.3)"},
                        ],
                    }
                },
                "barWidth": "40%",
            },
        ],
    }
    ev_key = "scissors"
    result = st_echarts(options=options, height="500px", events={"click": CLICK_FORMAT}, key=ev_key)
    maybe_popup("scissors", result, ev_key)


def render():
    L = lang()
    filters = render_sidebar()
    kpis = get_kpis()
    fact = filter_by_year(load_fact_observed(), filters["year_range"])

    # ── OPENING: Bold keynote-style headline ──
    st.markdown("""
    <div class="story-chapter">
      <span class="chapter-badge">Capítulo 1</span>
      <h2 class="chapter-title">El Efecto Tijera</h2>
      <p class="chapter-subtitle">El tráfico de datos se dispara, los ingresos se estancan. Esta divergencia es la crisis estructural del sector TELCO.</p>
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
      <span class="data-badge">📦 {n_rows} registros · {n_cols} variables</span>
      <span class="data-badge">📅 {yr_min}–{yr_max}</span>
      <span class="data-badge">📊 Fuente: CNMC · Eurostat · ETNO · GSMA</span>
      <span class="data-badge">🔬 5 hipótesis contrastadas</span>
    </div>
    """, unsafe_allow_html=True)

    # ── SHOWCASE: Two dramatic stats side by side ──
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown(f"""
        <div class="showcase-stat">
          <div class="number teal">+{kpis['traffic_cagr']*100:.0f}%</div>
          <div class="label">📈 CAGR Tráfico / año</div>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <div class="showcase-stat">
          <div class="number coral">{kpis['rev_cagr']*100:.1f}%</div>
          <div class="label">💰 CAGR Ingresos / año</div>
        </div>
        """, unsafe_allow_html=True)
    with col_c:
        st.markdown(f"""
        <div class="showcase-stat">
          <div class="number amber">✂️ {kpis['cagr_gap']*100:.1f} pp</div>
          <div class="label">⚠ Brecha de divergencia</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

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
    _render_echarts_scissors(fact)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── INSIGHT BOX: The takeaway ──
    st.markdown("""
    <div class="insight-box coral">
      <b>🔑 La conclusión es demoledora:</b> Por cada €1 que el sector ingresaba en 2005, hoy sigue ingresando ~€1.
      Pero la red transporta <b>+12.000% más tráfico</b>. El modelo de negocio no solo está roto — está <b>empeorando cada trimestre</b>.
    </div>
    """, unsafe_allow_html=True)

    # ── SECONDARY CHART: Traffic volume ──
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="chart-title">📦 {t("market_overview.traffic_volume_title", L)}</div>', unsafe_allow_html=True)
    result2 = st_echarts(options=traffic_revenue_stacked_echarts(fact), height="400px", events={"click": CLICK_FORMAT}, key="traffic_vol")
    maybe_popup("traffic_volume", result2, "traffic_vol")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── "ONE MORE THING" ──
    st.markdown("""
    <div class="insight-box amber" style="margin-top:1rem;">
      <b>🎯 One more thing:</b> Si esta brecha sigue creciendo, en 2030 el sector necesitará <b>el doble de inversión</b>
      para mantener la misma calidad de red. <b>Fair Share no es opcional: es la única salida.</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:right;padding:0.5rem 1rem;margin-top:0.5rem;font-size:0.9rem;color:#90A4AE;font-style:italic;border-top:1px solid rgba(255,255,255,0.04);">
      {t('market_overview.transition', L)} <span style="color:#00BFA5;">→</span>
    </div>
    """, unsafe_allow_html=True)

    from utils.export import download_button
    download_button(fact, "nettension_market_overview.csv")
