import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

CORPORATE_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        font=dict(family="Inter, Segoe UI, sans-serif", size=12, color="#ECEFF1"),
        title=dict(font=dict(size=15, color="#FFFFFF", family="Inter"), x=0.02, xanchor="left"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=60, r=30, t=60, b=60),
        xaxis=dict(
            showgrid=True, gridcolor="rgba(255,255,255,0.04)", zeroline=False,
            tickfont=dict(size=11, color="#90A4AE"),
            title_font=dict(size=12, color="#90A4AE"),
            linecolor="rgba(255,255,255,0.08)", linewidth=1, mirror=True
        ),
        yaxis=dict(
            showgrid=True, gridcolor="rgba(255,255,255,0.04)", zeroline=False,
            tickfont=dict(size=11, color="#90A4AE"),
            title_font=dict(size=12, color="#90A4AE"),
            linecolor="rgba(255,255,255,0.08)", linewidth=1, mirror=True
        ),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
            font=dict(size=11, color="#90A4AE"), bgcolor="rgba(17,24,39,0.9)",
            bordercolor="rgba(255,255,255,0.06)", borderwidth=1
        ),
        hoverlabel=dict(
            bgcolor="#1A2236", bordercolor="rgba(255,255,255,0.1)", font_size=12,
            font_family="Inter", font_color="#ECEFF1"
        ),
        colorway=["#00BFA5", "#FF5252", "#FFD740", "#536DFE", "#7C4DFF", "#00E676", "#FF9100", "#90A4AE"],
    )
)

DARK_PLOTLY_CONFIG = {"displayModeBar": False, "responsive": True}

def apply_corporate_style(fig: go.Figure) -> go.Figure:
    fig.update_layout(template=CORPORATE_TEMPLATE)
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.04)", zerolinecolor="rgba(255,255,255,0.08)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.04)", zerolinecolor="rgba(255,255,255,0.08)")
    fig.update_traces(hovertemplate=fig.data[0].hovertemplate.replace("<extra></extra>", "<extra></extra>") if fig.data else None)
    return fig

def hhi_chart_echarts(df: pd.DataFrame) -> dict:
    categories = df["trimestre_dt"].dt.strftime("%Y Q%q").tolist()
    hhi_values = df["hhi"].round(0).tolist()
    first_hhi = hhi_values[0] if hhi_values else 0
    last_hhi = hhi_values[-1] if hhi_values else 0

    classifications = []
    for v in hhi_values:
        if v >= 2500:
            classifications.append("🔴 Highly Concentrated")
        elif v >= 1000:
            classifications.append("🟡 Moderate")
        else:
            classifications.append("🟢 Competitive")

    return {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "cross", "label": {"backgroundColor": "#1A2236"}},
            "formatter": """function(params) {
                let v = params[0].value;
                let cls = v >= 2500 ? '🔴 Highly Concentrated' : (v >= 1000 ? '🟡 Moderate' : '🟢 Competitive');
                let desc = v >= 2500 ? 'High market power, low competition' : (v >= 1000 ? 'Some concentration, competitive pressure' : 'Fragmented market, high competition');
                let tip = '<b>' + params[0].axisValue + '</b><br/>';
                tip += params[0].marker + ' HHI: <b>' + v.toFixed(0) + '</b><br/>';
                tip += '<span style="color:' + (v >= 2500 ? '#FF5252' : (v >= 1000 ? '#FFD740' : '#00E676')) + ';">' + cls + '</span><br/>';
                tip += '<span style="font-size:0.75rem;color:#90A4AE;">' + desc + '</span>';
                return tip;
            }"""
        },
        "grid": {"left": "3%", "right": "4%", "bottom": "8%", "containLabel": True, "top": "15%"},
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": categories,
            "axisLine": {"lineStyle": {"color": "rgba(255,255,255,0.08)"}},
            "axisLabel": {"color": "#90A4AE", "rotate": 45, "fontSize": 10},
            "splitLine": {"show": False},
        },
        "yAxis": {
            "type": "value",
            "name": "HHI",
            "min": 0,
            "max": 4000,
            "nameTextStyle": {"color": "#FFD740", "fontSize": 11},
            "axisLine": {"lineStyle": {"color": "rgba(255,255,255,0.08)"}},
            "splitLine": {"lineStyle": {"color": "rgba(255,255,255,0.04)", "type": "dashed"}},
            "axisLabel": {"color": "#90A4AE"},
        },
        "series": [
            {
                "name": "HHI",
                "type": "line",
                "smooth": True,
                "symbol": "circle",
                "symbolSize": 6,
                "data": hhi_values,
                "lineStyle": {"color": "#FFD740", "width": 3, "shadowBlur": 10, "shadowColor": "rgba(255,215,64,0.3)"},
                "itemStyle": {"color": "#FFD740"},
                "areaStyle": {"color": "rgba(255,215,64,0.05)"},
                "markPoint": {
                    "data": [
                        {"type": "max", "name": "Max"},
                        {"type": "min", "name": "Min"},
                    ]
                },
                "markLine": {
                    "silent": True,
                    "data": [
                        {"yAxis": 2500, "lineStyle": {"color": "rgba(255,82,82,0.4)", "type": "dashed"}},
                        {"yAxis": 1000, "lineStyle": {"color": "rgba(0,230,118,0.4)", "type": "dashed"}},
                    ],
                    "label": {"show": False},
                },
            },
            {
                "name": "Concentration Bands",
                "type": "bar",
                "barWidth": "100%",
                "silent": True,
                "data": [{"value": v, "itemStyle": {
                    "color": "rgba(255,82,82,0.06)" if v >= 2500 else ("rgba(255,215,64,0.04)" if v >= 1000 else "rgba(0,230,118,0.03)")
                }} for v in hhi_values],
                "z": 0,
            },
        ],
    }

def traffic_revenue_stacked_echarts(df: pd.DataFrame) -> dict:
    categories = df["trimestre_dt"].dt.strftime("%Y Q%q").tolist()
    data_traffic = df["data_traffic"].round(0).tolist()
    has_voice = "voice_traffic" in df.columns and df["voice_traffic"].sum() > 0
    voice_traffic = df["voice_traffic"].round(0).tolist() if has_voice else []

    series = [
        {
            "name": "📦 Data Traffic",
            "type": "line",
            "stack": "total",
            "data": data_traffic,
            "smooth": True,
            "symbol": "none",
            "lineStyle": {"width": 0},
            "areaStyle": {"color": "rgba(0,191,165,0.6)", "origin": "auto"},
            "itemStyle": {"color": "#00BFA5"},
            "emphasis": {"focus": "series"},
        }
    ]
    if has_voice and sum(voice_traffic) > 0:
        series.append({
            "name": "📞 Voice Traffic",
            "type": "line",
            "stack": "total",
            "data": voice_traffic,
            "smooth": True,
            "symbol": "none",
            "lineStyle": {"width": 0},
            "areaStyle": {"color": "rgba(83,109,254,0.5)", "origin": "auto"},
            "itemStyle": {"color": "#536DFE"},
            "emphasis": {"focus": "series"},
        })

    return {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "cross"},
            "formatter": """function(params) {
                let tip = '<b>' + params[0].axisValue + '</b><br/>';
                let total = 0;
                params.forEach(function(p) {
                    tip += p.marker + ' ' + p.seriesName + ': <b>' + Number(p.value).toLocaleString() + '</b><br/>';
                    total += Number(p.value);
                });
                tip += '<hr style="margin:4px 0"/>';
                tip += '📊 Total: <b>' + total.toLocaleString() + '</b>';
                return tip;
            }"""
        },
        "legend": {
            "data": [s["name"] for s in series],
            "textStyle": {"color": "#90A4AE", "fontSize": 12},
            "top": 5,
        },
        "grid": {"left": "3%", "right": "4%", "bottom": "8%", "containLabel": True, "top": "15%"},
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": categories,
            "axisLine": {"lineStyle": {"color": "rgba(255,255,255,0.08)"}},
            "axisLabel": {"color": "#90A4AE", "rotate": 45, "fontSize": 10},
            "splitLine": {"show": False},
        },
        "yAxis": {
            "type": "value",
            "name": "Traffic Volume",
            "nameTextStyle": {"color": "#90A4AE", "fontSize": 11},
            "axisLine": {"lineStyle": {"color": "rgba(255,255,255,0.08)"}},
            "splitLine": {"lineStyle": {"color": "rgba(255,255,255,0.04)", "type": "dashed"}},
            "axisLabel": {"color": "#90A4AE"},
        },
        "series": series,
    }


def ott_donut_echarts() -> dict:
    return {
        "tooltip": {"trigger": "item", "formatter": "{b}: {c}% ({d}%)"},
        "legend": {
            "orient": "vertical", "right": "5%", "top": "center",
            "textStyle": {"color": "#90A4AE", "fontSize": 12},
        },
        "series": [
            {
                "name": "Traffic Share",
                "type": "pie",
                "radius": ["50%", "75%"],
                "avoidLabelOverlap": True,
                "center": ["35%", "50%"],
                "label": {"show": False},
                "emphasis": {"label": {"show": True, "fontSize": 14, "fontWeight": "bold", "color": "#FFFFFF"}},
                "data": [
                    {"value": 65, "name": "🎬 Video", "itemStyle": {"color": "#00BFA5"}},
                    {"value": 35, "name": "🌐 Other Traffic", "itemStyle": {"color": "rgba(0,191,165,0.25)"}},
                ],
            },
            {
                "name": "OTT Share",
                "type": "pie",
                "radius": ["50%", "75%"],
                "avoidLabelOverlap": True,
                "center": ["80%", "50%"],
                "label": {"show": False},
                "emphasis": {"label": {"show": True, "fontSize": 14, "fontWeight": "bold", "color": "#FFFFFF"}},
                "data": [
                    {"value": 50, "name": "🏢 Big 6 (Google, Meta, Netflix, etc.)", "itemStyle": {"color": "#FF5252"}},
                    {"value": 50, "name": "📡 Other Platforms", "itemStyle": {"color": "rgba(255,82,82,0.2)"}},
                ],
            },
        ],
    }


def eu_comparison_chart(df: pd.DataFrame) -> go.Figure:
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
            data.append({"metric": "CAPEX per capita (EUR)", "region": _clean_region(ind, "CAPEX per capita"), "value": val})
        elif "ARPU" in ind and "Mobile ARPU" in ind:
            data.append({"metric": "ARPU (EUR/month)", "region": _clean_region(ind, "Mobile ARPU"), "value": val})

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
        colors = ["#00BFA5" if r == "EU" else "#536DFE" for r in sub["region"]]
        fig.add_trace(go.Bar(
            name=metric,
            x=sub["region"],
            y=sub["normalized"].round(0),
            marker_color=colors,
            text=[f"{v:.0f}%" for v in sub["normalized"]],
            textposition="outside",
            textfont=dict(size=13, color="#FFFFFF"),
            hovertemplate="<b>%{x}</b><br>%{y:.0f}% of EU level<br>Actual: %{customdata}<extra></extra>",
            customdata=[f"{v:.1f}" for v in sub["value"]],
        ))

    fig.add_hline(y=100, line_dash="dash", line_color="rgba(255,255,255,0.3)", annotation_text="EU = 100%", annotation_font_color="#90A4AE")

    fig.update_layout(
        barmode="group",
        height=320,
        yaxis_title="% of EU level",
        yaxis=dict(tickfont=dict(size=12, color="#90A4AE"), range=[0, max(comp["normalized"]) * 1.25]),
        xaxis=dict(tickfont=dict(size=13, color="#E0E6ED")),
        legend=dict(font=dict(size=11, color="#90A4AE"), orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=10, r=10, t=40, b=20),
        hovermode="x unified",
    )
    return apply_corporate_style(fig)

def nsi_vs_arpu_scatter(df: pd.DataFrame) -> go.Figure:
    df = df.dropna(subset=["nsi", "revenue_per_line"]).copy()
    df["year_str"] = df["year"].astype(str)

    x_min = df["nsi"].min() * 0.9
    x_max = df["nsi"].max() * 1.1
    y_min = max(0, df["revenue_per_line"].min() * 0.85)
    y_max = df["revenue_per_line"].max() * 1.15

    fig = px.scatter(
        df, x="nsi", y="revenue_per_line",
        animation_frame="year_str",
        size="total_lines", size_max=45,
        color="year",
        color_continuous_scale=[[0, "#1A2236"], [0.3, "#536DFE"], [0.6, "#00BFA5"], [1, "#FFD740"]],
        log_x=True,
        range_x=[x_min, x_max],
        range_y=[y_min, y_max],
        labels={
            "nsi": "Network Stress Index (log scale) ↑ more pressure",
            "revenue_per_line": "Revenue per Line (ARPU) €",
            "year_str": "Year",
            "total_lines": "Total Lines"
        },
        hover_data={"trimestre_dt": "|%Y Q%q", "total_lines": ":,.0f", "year_str": False}
    )

    fig.update_traces(
        marker=dict(line=dict(width=1, color="white"), opacity=0.85),
        hovertemplate="<b>%{customdata[0]}</b><br>NSI: %{x:,.0f}<br>ARPU: €%{y:,.2f}<br>Lines: %{customdata[1]:,.0f}<extra></extra>"
    )

    fig.update_layout(
        title=dict(text="Network Stress vs ARPU — each dot = one quarter", font=dict(size=13)),
        coloraxis_showscale=False,
        hovermode="closest",
    )
    return apply_corporate_style(fig)
