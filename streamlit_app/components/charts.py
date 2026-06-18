import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from utils.i18n import t

CORPORATE_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        font=dict(family="system-ui, -apple-system, Segoe UI, sans-serif", size=12, color="#F0F6FC"),
        title=dict(font=dict(size=14, color="#F0F6FC", weight=600), x=0.02, xanchor="left"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=56, r=24, t=48, b=48),
        xaxis=dict(
            showgrid=True, gridcolor="rgba(255,255,255,0.03)", zeroline=False,
            tickfont=dict(size=11, color="#8B949E"),
            title_font=dict(size=12, color="#8B949E"),
            linecolor="rgba(255,255,255,0.06)", linewidth=1, mirror=True,
            automargin=True,
        ),
        yaxis=dict(
            showgrid=True, gridcolor="rgba(255,255,255,0.03)", zeroline=False,
            tickfont=dict(size=11, color="#8B949E"),
            title_font=dict(size=12, color="#8B949E"),
            linecolor="rgba(255,255,255,0.06)", linewidth=1, mirror=True,
            automargin=True,
        ),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            font=dict(size=11, color="#8B949E"), bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(255,255,255,0.06)", borderwidth=0, itemwidth=60,
        ),
        hoverlabel=dict(
            bgcolor="#161B22", bordercolor="#262F41", font_size=12,
            font_family="SF Mono, Cascadia Code, Consolas, monospace",
            font_color="#F0F6FC", namelength=-1,
        ),
        hovermode="x unified",
        colorway=["#D97724", "#CF3B30", "#2EA043", "#9A6AFF", "#8B949E"],
    )
)

DARK_PLOTLY_CONFIG = {"displayModeBar": False, "responsive": True, "scrollZoom": False, "modeBarButtons": []}


def apply_corporate_style(fig: go.Figure) -> go.Figure:
    fig.update_layout(template=CORPORATE_TEMPLATE)
    fig.update_xaxes(
        automargin=True,
        gridcolor="rgba(255,255,255,0.03)",
        zerolinecolor="rgba(255,255,255,0.06)",
    )
    fig.update_yaxes(
        automargin=True,
        gridcolor="rgba(255,255,255,0.03)",
        zerolinecolor="rgba(255,255,255,0.06)",
    )
    for t_obj in fig.data:
        if hasattr(t_obj, "hovertemplate") and t_obj.hovertemplate:
            t_obj.hovertemplate = t_obj.hovertemplate.replace("<extra></extra>", "<extra></extra>")
    return fig


def hhi_chart_echarts(df: pd.DataFrame, L: str = "es") -> dict:
    categories = df["trimestre_dt"].dt.strftime("%Y Q%q").tolist()
    hhi_values = df["hhi"].round(1).tolist()
    t_hhi = t("charts.hhi", L)
    t_bands = t("charts.concentration_bands", L)
    t_high = t("charts.highly_concentrated", L)
    t_mod = t("charts.moderate", L)
    t_comp = t("charts.competitive", L)
    t_high_desc = t("charts.high_market_power", L)
    t_mod_desc = t("charts.some_concentration", L)
    t_comp_desc = t("charts.fragmented", L)

    return {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "cross", "label": {"backgroundColor": "#161B22", "borderColor": "#262F41"}},
            "backgroundColor": "#161B22",
            "borderColor": "#262F41",
            "borderWidth": 1,
            "padding": [10, 14],
            "formatter": f"""function(params) {{
                var v = params[0].value;
                var cls = v >= 2500 ? '{t_high}' : (v >= 1000 ? '{t_mod}' : '{t_comp}');
                var c = v >= 2500 ? '#CF3B30' : (v >= 1000 ? '#D97724' : '#2EA043');
                var desc = v >= 2500 ? '{t_high_desc}'
                    : (v >= 1000 ? '{t_mod_desc}'
                    : '{t_comp_desc}');
                return '<div style=\"font-size:0.85rem;color:#8B949E;margin-bottom:6px;\">' + params[0].axisValue + '</div>'
                    + '<div style=\"display:flex;justify-content:space-between;gap:24px;font-size:0.9rem;\">'
                    + '<span style=\"color:#F0F6FC;\">{t_hhi}</span>'
                    + '<span style=\"color:#F0F6FC;font-weight:600;font-family:SF Mono,Cascadia Code,Consolas,monospace;\">' + v.toFixed(1) + '</span>'
                    + '</div>'
                    + '<div style=\"margin-top:4px;padding-top:6px;border-top:1px solid #262F41;\">'
                    + '<span style=\"color:' + c + ';font-size:0.8rem;\">' + cls + '</span>'
                    + '<br/><span style=\"color:#8B949E;font-size:0.75rem;\">' + desc + '</span>'
                    + '</div>';
            }}""",
        },
        "grid": {"left": "5%", "right": "6%", "bottom": "10%", "containLabel": True, "top": "12%"},
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": categories,
            "axisLine": {"lineStyle": {"color": "#262F41"}},
            "axisLabel": {"color": "#8B949E", "rotate": 30, "fontSize": 10, "interval": "auto"},
            "splitLine": {"show": False},
        },
        "yAxis": {
            "type": "value",
            "name": t_hhi,
            "min": 0,
            "max": 4000,
            "nameTextStyle": {"color": "#8B949E", "fontSize": 11},
            "axisLine": {"lineStyle": {"color": "#262F41"}},
            "splitLine": {"lineStyle": {"color": "#21262D", "type": "dashed"}},
            "axisLabel": {"color": "#8B949E"},
            "minInterval": 500,
        },
        "series": [
            {
                "name": t_hhi,
                "type": "line",
                "smooth": True,
                "symbol": "circle",
                "symbolSize": 5,
                "data": hhi_values,
                "lineStyle": {"color": "#D97724", "width": 2},
                "itemStyle": {"color": "#D97724"},
                "areaStyle": {"color": "rgba(217,119,36,0.15)"},
                "markPoint": {
                    "data": [
                        {"type": "max", "name": t("charts.max", L)},
                        {"type": "min", "name": t("charts.min", L)},
                    ]
                },
                "markLine": {
                    "silent": True,
                    "data": [
                        {"yAxis": 2500, "lineStyle": {"color": "rgba(207,59,48,0.35)", "type": "dashed"}},
                        {"yAxis": 1000, "lineStyle": {"color": "rgba(46,160,67,0.35)", "type": "dashed"}},
                    ],
                    "label": {"show": False},
                },
            },
            {
                "name": t_bands,
                "type": "bar",
                "barWidth": "100%",
                "silent": True,
                "data": [{"value": v, "itemStyle": {
                    "color": "rgba(207,59,48,0.03)" if v >= 2500 else ("rgba(217,119,36,0.02)" if v >= 1000 else "rgba(46,160,67,0.02)")
                }} for v in hhi_values],
                "z": 0,
            },
        ],
    }


def traffic_revenue_stacked_echarts(df: pd.DataFrame, L: str) -> dict:
    categories = df["trimestre_dt"].dt.strftime("%Y Q%q").tolist()
    data_traffic = df["data_traffic"].round(1).tolist()
    has_voice = "voice_traffic" in df.columns and df["voice_traffic"].sum() > 0
    voice_traffic = df["voice_traffic"].round(1).tolist() if has_voice else []
    t_data = t("charts.data_traffic", L)
    t_voice = t("charts.voice_traffic", L)

    series = [
        {
            "name": t_data,
            "type": "line",
            "data": data_traffic,
            "smooth": True,
            "symbol": "none",
            "lineStyle": {"width": 2, "color": "#D97724"},
            "areaStyle": {"color": "rgba(217,119,36,0.25)", "origin": "auto"},
            "itemStyle": {"color": "#D97724"},
            "emphasis": {"focus": "series"},
        }
    ]
    if has_voice and sum(voice_traffic) > 0:
        series.append({
            "name": t_voice,
            "type": "line",
            "data": voice_traffic,
            "smooth": True,
            "symbol": "none",
            "lineStyle": {"width": 2, "color": "#CF3B30"},
            "areaStyle": {"color": "rgba(207,59,48,0.25)", "origin": "auto"},
            "itemStyle": {"color": "#CF3B30"},
            "emphasis": {"focus": "series"},
        })

    return {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "cross"},
            "backgroundColor": "#161B22",
            "borderColor": "#262F41",
            "borderWidth": 1,
            "padding": [10, 14],
            "formatter": f"""function(params) {{
                var tip = '<div style=\"font-size:0.85rem;color:#8B949E;margin-bottom:6px;\">' + params[0].axisValue + '</div>';
                params.forEach(function(p) {{
                    var v = Number(p.value);
                    tip += '<div style=\"display:flex;justify-content:space-between;gap:24px;font-size:0.85rem;\">'
                        + '<span>' + p.marker + ' ' + p.seriesName + '</span>'
                        + '<span style=\"font-family:SF Mono,Cascadia Code,Consolas,monospace;color:#F0F6FC;\">' + v.toFixed(1) + ' TB</span>'
                        + '</div>';
                }});
                return tip;
            }}""",
        },
        "legend": {
            "data": [s["name"] for s in series],
            "textStyle": {"color": "#8B949E", "fontSize": 11},
            "top": 5,
            "icon": "roundRect",
            "itemWidth": 12,
            "itemHeight": 3,
        },
        "grid": {"left": "5%", "right": "6%", "bottom": "10%", "containLabel": True, "top": "14%"},
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": categories,
            "axisLine": {"lineStyle": {"color": "#262F41"}},
            "axisLabel": {"color": "#8B949E", "rotate": 30, "fontSize": 10, "interval": "auto"},
            "splitLine": {"show": False},
        },
        "yAxis": {
            "type": "value",
            "name": t("charts.traffic_volume", L) + " (TB)",
            "nameTextStyle": {"color": "#8B949E", "fontSize": 11},
            "axisLine": {"lineStyle": {"color": "#262F41"}},
            "splitLine": {"lineStyle": {"color": "#21262D", "type": "dashed"}},
            "axisLabel": {"color": "#8B949E", "formatter": "{value} TB"},
        },
        "series": series,
    }


def ott_donut_echarts(L: str = "es") -> dict:
    return {
        "tooltip": {
            "trigger": "item",
            "backgroundColor": "#161B22",
            "borderColor": "#262F41",
            "borderWidth": 1,
            "padding": [10, 14],
            "formatter": """function(params) {
                return '<div style=\"display:flex;justify-content:space-between;gap:20px;font-size:0.85rem;\">'
                    + '<span>' + params.marker + ' ' + params.name + '</span>'
                    + '<span style=\"font-family:SF Mono,Cascadia Code,Consolas,monospace;color:#F0F6FC;\">' + Number(params.percent).toFixed(1) + '%</span>'
                    + '</div>';
            }""",
        },
        "legend": {
            "orient": "vertical", "right": "3%", "top": "center",
            "textStyle": {"color": "#8B949E", "fontSize": 11},
            "icon": "circle",
            "itemWidth": 8,
            "itemHeight": 8,
        },
        "series": [
            {
                "name": t("charts.traffic_share", L),
                "type": "pie",
                "radius": ["50%", "72%"],
                "avoidLabelOverlap": True,
                "center": ["32%", "50%"],
                "label": {
                    "show": True,
                    "position": "outside",
                    "formatter": "{b}\n{d}%",
                    "color": "#8B949E",
                    "fontSize": 11,
                    "lineHeight": 14,
                },
                "emphasis": {"label": {"show": True, "fontSize": 13, "fontWeight": "600", "color": "#F0F6FC"}},
                "data": [
                    {"value": 65, "name": t("fair_share.video_share", L), "itemStyle": {"color": "#2EA043"}},
                    {"value": 35, "name": t("fair_share.other_traffic", L), "itemStyle": {"color": "rgba(46,160,67,0.12)"}},
                ],
            },
            {
                "name": t("charts.ott_share", L),
                "type": "pie",
                "radius": ["50%", "72%"],
                "avoidLabelOverlap": True,
                "center": ["80%", "50%"],
                "label": {
                    "show": True,
                    "position": "outside",
                    "formatter": "{b}\n{d}%",
                    "color": "#8B949E",
                    "fontSize": 11,
                    "lineHeight": 14,
                },
                "emphasis": {"label": {"show": True, "fontSize": 13, "fontWeight": "600", "color": "#F0F6FC"}},
                "data": [
                    {"value": 50, "name": t("fair_share.big6_share", L), "itemStyle": {"color": "#CF3B30"}},
                    {"value": 50, "name": t("fair_share.other_platforms", L), "itemStyle": {"color": "rgba(207,59,48,0.12)"}},
                ],
            },
        ],
    }


def eu_comparison_chart(df: pd.DataFrame, L: str = "es") -> go.Figure:
    def _clean_region(indicator: str, keyword: str) -> str:
        for prefix in ["EU", "USA", "South Korea", "Japan"]:
            if indicator.startswith(prefix):
                return prefix
        return indicator.replace(keyword, "").strip().replace("()", "").strip()

    data = []
    for _, r in df.iterrows():
        ind = r["indicator"]
        val = pd.to_numeric(r["value"], errors="coerce")
        if pd.isna(val):
            continue
        if "per capita" in ind:
            data.append({"metric": t("charts.capex_per_capita", L), "region": _clean_region(ind, "CAPEX per capita"), "value": val})
        elif "ARPU" in ind and "Mobile ARPU" in ind:
            data.append({"metric": t("charts.arpu_month", L), "region": _clean_region(ind, "Mobile ARPU"), "value": val})

    comp = pd.DataFrame(data)
    if comp.empty:
        return None

    eu_val = comp[comp["region"] == "EU"]
    eu_capex = eu_val[eu_val["metric"].str.contains("CAPEX")]["value"].values
    eu_arpu = eu_val[eu_val["metric"].str.contains("ARPU")]["value"].values
    eu_capex_base = eu_capex[0] if len(eu_capex) > 0 else 1
    eu_arpu_base = eu_arpu[0] if len(eu_arpu) > 0 else 1

    comp["normalized"] = comp.apply(
        lambda r: (r["value"] / eu_capex_base * 100) if "CAPEX" in r["metric"] else (r["value"] / eu_arpu_base * 100),
        axis=1
    )

    region_order = ["EU", "USA", "South Korea", "Japan"]
    comp["order"] = comp["region"].apply(lambda r: region_order.index(r) if r in region_order else 99)
    comp = comp.sort_values(["metric", "order"])

    fig = go.Figure()
    for metric in comp["metric"].unique():
        sub = comp[comp["metric"] == metric]
        colors = ["#D97724" if r == "EU" else "#8B949E" for r in sub["region"]]
        fig.add_trace(go.Bar(
            name=metric,
            x=sub["region"],
            y=sub["normalized"].round(1),
            marker_color=colors,
            text=[f"{v:.1f}%" for v in sub["normalized"]],
            textposition="outside",
            textfont=dict(size=11, color="#8B949E"),
            hovertemplate="<b>%{x}</b><br>%{y:.1f}% of EU level<br>" + t("charts.click_value", L) + ": %{customdata}<extra></extra>",
            customdata=[f"{v:.1f}" for v in sub["value"]],
        ))

    fig.add_hline(
        y=100, line_dash="dash", line_color="rgba(255,255,255,0.2)",
        annotation_text=t("charts.eu_level", L),
        annotation_font_color="#8B949E", annotation_font_size=11,
    )

    fig.update_layout(
        barmode="group",
        height=360,
        yaxis_title=t("charts.pct_of_eu_level", L),
        xaxis=dict(tickfont=dict(size=11, color="#E0E6ED"), automargin=True),
        yaxis=dict(tickfont=dict(size=11, color="#8B949E"), range=[0, max(comp["normalized"]) * 1.30], automargin=True),
        legend=dict(font=dict(size=11, color="#8B949E"), orientation="h",
                    yanchor="bottom", y=1.02, xanchor="right", x=1, itemwidth=60),
        margin=dict(l=10, r=10, t=35, b=25),
        hovermode="x unified",
    )
    return apply_corporate_style(fig)


def nsi_vs_arpu_scatter(df: pd.DataFrame, L: str = "es") -> go.Figure:
    df = df.dropna(subset=["nsi", "revenue_per_line"]).copy()
    df["year_str"] = df["year"].astype(str)

    x_min = df["nsi"].min() * 0.9
    x_max = df["nsi"].max() * 1.1
    y_min = max(0, df["revenue_per_line"].min() * 0.85)
    y_max = df["revenue_per_line"].max() * 1.15

    fig = px.scatter(
        df, x="nsi", y="revenue_per_line",
        animation_frame="year_str",
        size="total_lines", size_max=40,
        color="year",
        color_continuous_scale=[[0, "#171D2A"], [0.3, "#2EA043"], [0.6, "#D97724"], [1, "#CF3B30"]],
        log_x=True,
        range_x=[x_min, x_max],
        range_y=[y_min, y_max],
        labels={
            "nsi": t("charts.nsi_label", L),
            "revenue_per_line": t("charts.arpu_label", L),
            "year_str": t("charts.year", L),
            "total_lines": t("charts.total_lines", L),
        },
        hover_data={"trimestre_dt": "|%Y Q%q", "total_lines": ":,.1f", "year_str": False},
    )

    fig.update_traces(
        marker=dict(line=dict(width=1, color="white"), opacity=0.8),
        hovertemplate="<b>%{customdata[0]}</b><br>NSI: %{x:,.1f}<br>ARPU: EUR %{y:,.2f}<br>"
        + t("charts.total_lines", L) + ": %{customdata[1]:,.1f}<extra></extra>",
    )

    fig.update_layout(
        title=dict(text=t("charts.network_stress_title", L), font=dict(size=13)),
        coloraxis_showscale=False,
        hovermode="closest",
        xaxis=dict(automargin=True),
        yaxis=dict(automargin=True),
    )
    return apply_corporate_style(fig)
