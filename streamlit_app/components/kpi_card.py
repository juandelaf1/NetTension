import streamlit as st
from typing import Optional, List
import plotly.graph_objects as go

def kpi_card(
    label: str,
    value: str | float,
    delta: Optional[str] = None,
    delta_color: str = "neutral",
    sparkline_data: Optional[List[float]] = None,
    help_text: Optional[str] = None,
    icon: Optional[str] = None
):
    """Tarjeta KPI profesional con sparkline opcional."""
    delta_class = f"kpi-delta {delta_color}" if delta else ""
    delta_html = f'<div class="{delta_class}">{delta}</div>' if delta else ""
    icon_html = f'<span style="font-size:1.2rem;margin-right:0.5rem;">{icon}</span>' if icon else ""
    
    sparkline_html = ""
    if sparkline_data:
        fig = go.Figure(go.Scatter(
            y=sparkline_data, mode='lines', 
            line=dict(color='#005A9C', width=2), 
            fill='tozeroy', fillcolor='rgba(0,90,156,0.1)'
        ))
        fig.update_layout(
            height=40, margin=dict(l=0,r=0,t=0,b=0), 
            xaxis=dict(visible=False), yaxis=dict(visible=False), 
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
        )
        sparkline_html = f'<div class="kpi-sparkline">{fig.to_html(include_plotlyjs=False, full_html=False)}</div>'
    
    html = f"""
    <div class="kpi-card" title="{help_text or ''}">
      <div class="kpi-label">{icon_html}{label}</div>
      <div class="kpi-value">{value}</div>
      {delta_html}
      {sparkline_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def kpi_row(cards: list):
    """Render multiple KPI cards in a row."""
    cols = st.columns(len(cards))
    for col, card in zip(cols, cards):
        with col:
            kpi_card(**card)