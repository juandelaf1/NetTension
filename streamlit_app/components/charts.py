import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

CORPORATE_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        font=dict(family="Inter, Segoe UI, sans-serif", size=12, color="#1A1A2E"),
        title=dict(font=dict(size=14, color="#003366", family="Inter"), x=0.02, xanchor="left"),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        margin=dict(l=60, r=30, t=50, b=50),
        xaxis=dict(
            showgrid=True, gridcolor="#F0F0F0", zeroline=False,
            tickfont=dict(size=11, color="#546E7A"),
            title_font=dict(size=12, color="#546E7A"),
            linecolor="#E0E0E0", linewidth=1, mirror=True
        ),
        yaxis=dict(
            showgrid=True, gridcolor="#F0F0F0", zeroline=False,
            tickfont=dict(size=11, color="#546E7A"),
            title_font=dict(size=12, color="#546E7A"),
            linecolor="#E0E0E0", linewidth=1, mirror=True
        ),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
            font=dict(size=11, color="#546E7A"), bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#E0E0E0", borderwidth=1
        ),
        hoverlabel=dict(
            bgcolor="#FFFFFF", bordercolor="#E0E0E0", font_size=11,
            font_family="Inter", font_color="#1A1A2E"
        ),
        colorway=["#005A9C", "#C62828", "#F2C811", "#2E7D32", "#546E7A", "#7B1FA2", "#E65100", "#00695C"],
        shapes=[dict(type="rect", xref="paper", yref="paper", x0=0, y0=0, x1=1, y1=1, line=dict(color="#E0E0E0", width=1))]
    )
)

def apply_corporate_style(fig: go.Figure) -> go.Figure:
    fig.update_layout(template=CORPORATE_TEMPLATE)
    return fig

def scissors_chart(df: pd.DataFrame) -> go.Figure:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(go.Scatter(
        x=df["trimestre_dt"], y=df["data_traffic_index"],
        name="Tráfico de datos (índice)", mode="lines+markers",
        line=dict(color="#005A9C", width=3), marker=dict(size=6),
        hovertemplate="%{x|%Y Q%q}<br>Tráfico: %{y:.0f}%<extra></extra>"
    ), secondary_y=False)
    
    fig.add_trace(go.Scatter(
        x=df["trimestre_dt"], y=df["revenue_index"],
        name="Ingresos (índice)", mode="lines+markers",
        line=dict(color="#C62828", width=3, dash="dot"), marker=dict(size=6, symbol="diamond"),
        hovertemplate="%{x|%Y Q%q}<br>Ingresos: %{y:.0f}%<extra></extra>"
    ), secondary_y=True)
    
    fig.update_xaxes(title_text="", showgrid=False)
    fig.update_yaxes(title_text="Tráfico índice (2005=100)", secondary_y=False, color="#005A9C")
    fig.update_yaxes(title_text="Ingresos índice (2005=100)", secondary_y=True, color="#C62828", showgrid=False)
    
    last_traffic = df["data_traffic_index"].iloc[-1]
    last_revenue = df["revenue_index"].iloc[-1]
    fig.add_annotation(
        x=df["trimestre_dt"].iloc[-1], y=last_traffic,
        text=f"Gap: {last_traffic - last_revenue:.0f} pp", showarrow=True,
        arrowhead=2, arrowcolor="#F2C811", bgcolor="#FFFFFF", bordercolor="#F2C811",
        font=dict(color="#003366", size=11)
    )
    
    return apply_corporate_style(fig)

def hhi_chart(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    
    fig.add_hrect(y0=2500, y1=4000, fillcolor="#C62828", opacity=0.08, line_width=0, 
                  annotation_text="Highly Concentrated", annotation_position="top left", 
                  annotation_font=dict(size=10, color="#C62828"))
    fig.add_hrect(y0=1000, y1=2500, fillcolor="#F2C811", opacity=0.08, line_width=0, 
                  annotation_text="Moderate", annotation_position="top left", 
                  annotation_font=dict(size=10, color="#B8860B"))
    fig.add_hrect(y0=0, y1=1000, fillcolor="#2E7D32", opacity=0.08, line_width=0, 
                  annotation_text="Competitive", annotation_position="top left", 
                  annotation_font=dict(size=10, color="#2E7D32"))
    
    fig.add_trace(go.Scatter(
        x=df["trimestre_dt"], y=df["hhi"],
        mode="lines+markers", name="HHI",
        line=dict(color="#F2C811", width=3), marker=dict(size=5),
        hovertemplate="%{x|%Y Q%q}<br>HHI: %{y:.0f}<br>Operadores: %{customdata[0]}<extra></extra>",
        customdata=df[["num_operators"]].values
    ))
    
    fig.update_layout(yaxis_title="HHI", xaxis_title="", hovermode="x unified")
    return apply_corporate_style(fig)

def nsi_vs_arpu_scatter(df: pd.DataFrame) -> go.Figure:
    fig = px.scatter(
        df, x="nsi", y="revenue_per_line",
        animation_frame="year", animation_group="trimestre_dt",
        size="total_lines", size_max=40,
        color="year", color_continuous_scale="Blues",
        log_x=True,
        labels={"nsi": "Network Stress Index (log)", "revenue_per_line": "ARPU (€/line)", "year": "Año"},
        hover_data={"trimestre_dt": "|%Y Q%q", "total_lines": ":,.0f"}
    )
    fig.update_traces(marker=dict(line=dict(width=1, color="white"), opacity=0.8))
    fig.update_layout(coloraxis_showscale=False)
    return apply_corporate_style(fig)

def eu_benchmark_bar(df: pd.DataFrame, keyword: str, title: str) -> go.Figure:
    sub = df[df["indicator"].str.contains(keyword, case=False, na=False)].copy()
    sub["value_num"] = pd.to_numeric(sub["value"], errors="coerce")
    sub = sub.dropna(subset=["value_num"]).sort_values("value_num", ascending=True)
    
    colors = ["#005A9C" if "EU" in str(i) or "Europe" in str(i) else "#546E7A" for i in sub["indicator"]]
    
    fig = go.Figure(go.Bar(
        y=sub["indicator"], x=sub["value_num"], orientation="h",
        marker=dict(color=colors, line=dict(color="white", width=1)),
        text=[f"{v:,.0f} {u}" for v, u in zip(sub["value_num"], sub["unit"])],
        textposition="outside", textfont=dict(size=11, color="#1A1A2E"),
        hovertemplate="%{y}<br>%{x:,.0f} %{customdata}<extra></extra>",
        customdata=sub["unit"]
    ))
    fig.update_layout(xaxis_title="", yaxis_title="", height=max(300, len(sub)*50))
    return apply_corporate_style(fig)

def traffic_revenue_stacked(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["trimestre_dt"], y=df["data_traffic"], name="Data Traffic",
        marker_color="#005A9C", hovertemplate="%{x|%Y Q%q}<br>Traffic: %{y:,.0f}<extra></extra>"
    ))
    fig.add_trace(go.Bar(
        x=df["trimestre_dt"], y=df["voice_traffic"], name="Voice Traffic",
        marker_color="#546E7A", hovertemplate="%{x|%Y Q%q}<br>Voice: %{y:,.0f}<extra></extra>"
    ))
    fig.update_layout(barmode="stack", yaxis_title="Traffic", xaxis_title="", hovermode="x unified")
    return apply_corporate_style(fig)