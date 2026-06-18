import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.data_loader import load_eu_context
from components.charts import apply_corporate_style, eu_comparison_chart
from components.filters import render_sidebar
from components.tables import render_aggrid
from utils.i18n import t, lang
from components.explain_popup import CLICK_FORMAT, maybe_popup


def _bar_chart(df: pd.DataFrame, keyword: str, label_key: str, color_map: dict) -> go.Figure:
    sub = df[df["indicator"].str.contains(keyword, case=False, na=False)].copy()
    sub["value_num"] = pd.to_numeric(sub["value"], errors="coerce")
    sub = sub.dropna(subset=["value_num"]).sort_values("value_num", ascending=True)

    colors = []
    for i in sub["indicator"]:
        matched = False
        for region, c in color_map.items():
            if region.lower() in i.lower():
                colors.append(c)
                matched = True
                break
        if not matched:
            colors.append("#9A6AFF")

    labels = [i.replace(keyword, "").replace("()", "").strip() for i in sub["indicator"]]

    fig = go.Figure(go.Bar(
        y=labels,
        x=sub["value_num"],
        orientation="h",
        marker=dict(
            color=colors,
            line=dict(color="rgba(255,255,255,0.3)", width=1),
        ),
        text=[f"<b>{v:,.1f}</b> {u}" for v, u in zip(sub["value_num"], sub["unit"])],
        textposition="outside",
        textfont=dict(size=15, color="#FFFFFF"),
        hovertemplate="<b>%{y}</b><br>%{x:,.1f} %{customdata}<extra></extra>",
        customdata=sub["unit"],
    ))

    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        height=max(220, len(sub) * 60),
        margin=dict(l=10, r=10, t=10, b=20),
        yaxis=dict(tickfont=dict(size=14, color="#E0E6ED")),
        xaxis=dict(tickfont=dict(size=13, color="#8B949E")),
    )
    return apply_corporate_style(fig)


def _echarts_5g_gauge(row):
    value = float(row["value"])
    options = {
        "series": [
            {
                "type": "gauge",
                "startAngle": 220,
                "endAngle": -40,
                "center": ["50%", "55%"],
                "radius": "85%",
                "min": 0,
                "max": 100,
                "splitNumber": 5,
                "progress": {
                    "show": True,
                    "width": 18,
                    "roundCap": True,
                    "itemStyle": {
                        "color": {
                            "type": "linear",
                            "x": 0, "y": 0, "x2": 1, "y2": 0,
                            "colorStops": [
                                {"offset": 0, "color": "#D97724"},
                                {"offset": 0.5, "color": "#9A6AFF"},
                                {"offset": 1, "color": "#CF3B30"},
                            ],
                        }
                    },
                },
                "pointer": {"show": False},
                "axisLine": {
                    "lineStyle": {"width": 18, "color": [[1, "rgba(255,255,255,0.08)"]]},
                },
                "axisTick": {"show": False},
                "splitLine": {"show": False},
                "axisLabel": {"show": False},
                "detail": {
                    "valueAnimation": True,
                    "formatter": "{value}%",
                    "color": "#FFFFFF",
                    "fontSize": 32,
                    "fontWeight": "bold",
                    "offsetCenter": [0, "30%"],
                },
                "title": {
                    "offsetCenter": [0, "65%"],
                    "fontSize": 14,
                    "color": "#8B949E",
                },
                "data": [{"value": value, "name": row["indicator"]}],
            }
        ]
    }
    return options


def _key_metric_card(label: str, value: str, icon: str, color: str):
    st.markdown(f"""
    <div style="background:rgba(18,22,32,0.7);border-radius:12px;padding:1.2rem 1rem;
                border-left:4px solid {color};margin-bottom:0.5rem;
                backdrop-filter:blur(4px);">
      <div style="font-size:0.75rem;color:#8B949E;text-transform:uppercase;letter-spacing:0.5px;">
        {icon} {label}
      </div>
      <div style="font-size:1.8rem;font-weight:700;color:#FFFFFF;margin-top:0.3rem;">
        {value}
      </div>
    </div>
    """, unsafe_allow_html=True)


def render():
    try:
        L = lang()
        render_sidebar()
        eu = load_eu_context()

        st.markdown(f"""
        <div class="story-chapter" style="border-color:rgba(154,106,255,0.3);">
          <span class="chapter-badge">{t('european_context.title' if L == 'en' else 'european_context.title', L)}</span>
          <h2 class="chapter-title">{t('european_context.title', L)}</h2>
          <p class="chapter-subtitle">{t('european_context.subtitle', L)}</p>
        </div>
        """, unsafe_allow_html=True)

        region_colors = {
            "eu": "#D97724",
            "europe": "#D97724",
            "usa": "#CF3B30",
            "us": "#CF3B30",
            "south korea": "#D97724",
            "japan": "#9A6AFF",
        }

        # ── ROW 1: EU vs World comparison chart ──
        st.markdown(f"""
        <div style="font-size:0.85rem;color:#D97724;text-transform:uppercase;letter-spacing:1px;
                    margin-bottom:0.3rem;">🌍 {t("european_context.comparison_title", L)}</div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_comp = eu_comparison_chart(eu, L)
        if fig_comp is not None:
            st.plotly_chart(fig_comp, width="stretch", config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

        # ── ROW 2: Key Metrics + 5G Gauge ──
        col3, col4 = st.columns([1.2, 0.8])
        with col3:
            st.markdown(f"""
            <div style="font-size:0.85rem;color:#9A6AFF;text-transform:uppercase;letter-spacing:1px;
                        margin-bottom:0.5rem;">📊 {t("european_context.market_indicators_title", L)}</div>
            """, unsafe_allow_html=True)

            metrics = [
                ("EU Mobile Revenue", "€163 Bn", "💰", "#D97724"),
                ("EU Operator CAPEX", "€57.9 Bn", "🔧", "#D97724"),
                ("Mobile → EU GDP", "5.0%", "📈", "#2EA043"),
                ("EU ROCE", "5.9%", "📊", "#9A6AFF"),
                ("Revenue Growth (2023)", "-4.4%", "📉", "#CF3B30"),
            ]
            rows = [metrics[i:i+3] for i in range(0, len(metrics), 3)]
            for row in rows:
                cols = st.columns(len(row))
                for ci, (label, val, icon, color) in enumerate(row):
                    with cols[ci]:
                        _key_metric_card(label, val, icon, color)

            # Market structure table
            st.markdown('<div class="chart-container" style="margin-top:0.8rem;">', unsafe_allow_html=True)
            sub = eu[eu["indicator"].str.contains("Video|Big 6|ROCE|real growth", case=False, na=False)]
            for _, r in sub.iterrows():
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                            padding:0.4rem 0;border-bottom:1px solid rgba(255,255,255,0.05);">
                  <span style="color:#8B949E;font-size:0.9rem;">{r['indicator']}</span>
                  <span style="color:#FFFFFF;font-weight:600;font-size:1.1rem;">
                    {r['value']} <span style="color:#8B949E;font-size:0.75rem;">{r['unit']}</span>
                  </span>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:0.7rem;color:#637381;margin-top:-0.3rem;margin-bottom:0.3rem;">{r["source"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div style="font-size:0.85rem;color:#D97724;text-transform:uppercase;letter-spacing:1px;
                        margin-bottom:0.3rem;">📡 {t("european_context.5g_title", L)}</div>
            """, unsafe_allow_html=True)
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            # 5G adoption gauge for current year
            current_5g = eu[eu["indicator"].str.contains("5G Adoption.*2024", case=False, na=False)]
            projected_5g = eu[eu["indicator"].str.contains("5G Adoption.*2030", case=False, na=False)]
            if not current_5g.empty:
                from streamlit_echarts import st_echarts
                g5_result = st_echarts(options=_echarts_5g_gauge(current_5g.iloc[0]), height="280px", events={"click": CLICK_FORMAT}, key="g5_gauge")
                maybe_popup("g5_gauge", g5_result, "g5_gauge")
                st.markdown(f"""
                <div style="text-align:center;font-size:0.85rem;color:#8B949E;margin-top:-1rem;">
                  {t('european_context.5g_coverage_label', L)}: <span style="color:#FFFFFF;">{eu[eu['indicator'].str.contains('5G population', case=False, na=False)]['value'].values[0]:.1f}%</span>
                  <span style="display:block;font-size:0.75rem;color:#637381;">Source: EU 5G Observatory 2025</span>
                </div>
                """, unsafe_allow_html=True)
            if not projected_5g.empty:
                st.markdown(f"""
                <div style="text-align:center;margin-top:0.8rem;padding:0.6rem;background:rgba(217,119,36,0.08);border-radius:8px;
                            border:1px solid rgba(217,119,36,0.15);">
                  <span style="color:#8B949E;font-size:0.8rem;">🎯 2030 Projection</span><br>
                  <span style="color:#D97724;font-size:2rem;font-weight:700;">{projected_5g.iloc[0]['value']:.0f}%</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Mobile subscribers & internet gap mini-cards
            subs_row = eu[eu["indicator"].str.contains("Subscribers", case=False, na=False)]
            gap_row = eu[eu["indicator"].str.contains("usage gap", case=False, na=False)]
            st.markdown('<div class="chart-container" style="margin-top:0.5rem;">', unsafe_allow_html=True)
            if not subs_row.empty:
                r = subs_row.iloc[0]
                _key_metric_card("Mobile Subscribers", f"{r['value']:.0f}M", "📡", "#D97724")
            if not gap_row.empty:
                r = gap_row.iloc[0]
                _key_metric_card("Internet Usage Gap", f"{r['value']:.1f}%", "🌐", "#CF3B30")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div style="text-align:right;padding:0.5rem 1rem;margin-top:0.5rem;font-size:0.9rem;color:#8B949E;font-style:italic;border-top:1px solid rgba(255,255,255,0.04);">
          {t('european_context.transition', L)} <span style="color:#9A6AFF;">→</span>
        </div>
        """, unsafe_allow_html=True)

        from utils.export import download_button
        download_button(eu, "nettension_eu_context.csv")

    except Exception as e:
        st.error(f"❌ **{'Error en página Contexto Europeo' if L == 'es' else 'Error in European Context page'}:** `{type(e).__name__}: {e}`")
        st.exception(e)
