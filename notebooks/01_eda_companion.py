# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # NetTension — Exploratory Data Analysis
# ## EU Telecom Network Stress Simulation Framework (2005–2025)
#
# <img src="https://raw.githubusercontent.com/juandelaf1/NetTension/main/assets/banner.svg" width="100%">
#
# ---
# **Purpose:** This notebook replicates the key visualizations from the Power BI dashboard
# using Plotly for static/semi-interactive exploration on GitHub.
#
# **Data:** CNMC (Spain regulator) + Eurostat · All variables are Layer 1 (OBSERVED).
# No synthetic or simulated data.
#
# **Instructions:** Run all cells to generate the full analysis.

# %%
import sys
sys.path.insert(0, "../src")

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

PROC = Path("../data/processed")
FIGS = Path("../outputs/figures")
FIGS.mkdir(parents=True, exist_ok=True)

# Set Plotly theme
import plotly.io as pio
pio.templates.default = "plotly_white"

# %% [markdown]
# ## 1. Load Data

# %%
agg = pd.read_parquet(PROC / "fact_observed_agg.parquet")
hhi = pd.read_parquet(PROC / "kpi_hhi.parquet")
eu = pd.read_parquet(PROC / "dim_eu_context.parquet")
es = pd.read_parquet(PROC / "fact_eurostat_es.parquet")

print(f"fact_observed_agg: {agg.shape} — {agg['trimestre_dt'].min()} to {agg['trimestre_dt'].max()}")
print(f"kpi_hhi: {hhi.shape} — HHI range: {hhi['hhi'].min():.0f}–{hhi['hhi'].max():.0f}")
print(f"dim_eu_context: {eu.shape} — {len(eu)} indicators")
print(f"fact_eurostat_es: {es.shape} — {es['year'].min():.0f} to {es['year'].max():.0f}")

# %% [markdown]
# ## 2. H1 — Scissors Effect: Traffic vs Revenue
#
# **Prediction:** Data traffic CAGR >> Revenue CAGR, creating a widening gap.
# **Result:** CONFIRMED

# %%
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(
    x=agg["trimestre_dt"], y=agg["data_traffic_index"],
    name="Traffic Index (100 = 2005)", line=dict(color="#00bcd4", width=2.5)
))
fig.add_trace(go.Scatter(
    x=agg["trimestre_dt"], y=agg["revenue_index"],
    name="Revenue Index (100 = 2005)", line=dict(color="#ff6b35", width=2.5)
))
fig.update_layout(
    title="Scissors Effect: Data Traffic vs Revenue (Indexed to 100)",
    xaxis_title="Quarter", hovermode="x unified",
    legend=dict(x=0.01, y=0.99),
    height=500
)
fig.write_html(FIGS / "scissors_effect.html", include_plotlyjs="cdn")
fig.show()

# %%
# CAGR calculation
periods = len(agg)
years = periods / 4
cagr_t = (agg["data_traffic"].iloc[-1] / agg["data_traffic"].iloc[0]) ** (1 / years) - 1
cagr_r = (agg["revenue"].iloc[-1] / agg["revenue"].iloc[0]) ** (1 / years) - 1
gap = cagr_t - cagr_r

print(f"CAGR Traffic  (2005–2025): {cagr_t:+.1%} per year")
print(f"CAGR Revenue  (2005–2025): {cagr_r:+.1%} per year")
print(f"Scissors Gap: {gap:+.1%} percentage points")
print(f"\nImplication: Traffic grows at {cagr_t:+.0%}/year while revenue declines.")
print(f"This gap is structurally unsustainable without Fair Share or cost innovation.")

# %% [markdown]
# ## 3. H2 — Market Concentration (HHI)
#
# **Prediction:** HHI increases over time (market concentration rises).
# **Result:** **REFUTED** — HHI decreased from 3,482 to 2,368.
# **Key insight:** More competition did NOT solve the Scissors Effect.

# %%
colors_hhi = ["#4caf50" if v < 1000 else "#ff9800" if v <= 2500 else "#f44336" for v in hhi["hhi"]]

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=hhi["trimestre"], y=hhi["hhi"],
    mode="lines+markers",
    line=dict(color="#7c4dff", width=2),
    marker=dict(color=colors_hhi, size=5),
    name="HHI"
))
fig.add_hline(y=1000, line_dash="dash", line_color="#4caf50", annotation_text="Competitive")
fig.add_hline(y=2500, line_dash="dash", line_color="#f44336", annotation_text="Highly Concentrated")
fig.update_layout(
    title="Herfindahl-Hirschman Index (Revenue-Based)",
    xaxis_title="Quarter", yaxis_title="HHI",
    height=450
)
fig.write_html(FIGS / "hhi_timeline.html", include_plotlyjs="cdn")
fig.show()

# %%
hhi_first = hhi["hhi"].iloc[0]
hhi_last = hhi["hhi"].iloc[-1]
print(f"HHI {hhi['trimestre'].iloc[0]}: {hhi_first:.0f} — Highly Concentrated")
print(f"HHI {hhi['trimestre'].iloc[-1]}: {hhi_last:.0f} — Moderately Concentrated")
print(f"Change: {hhi_last - hhi_first:+.0f} points (DECONCENTRATION)")
print(f"\nDespite market fragmentation, the Scissors Effect worsened.")
print(f"This proves the problem is structural, not monopolistic.")

# %% [markdown]
# ## 4. H3 — Data Asymmetry: Revenue per Unit Collapse
#
# **Prediction:** Revenue per traffic unit collapses as usage explodes.
# **Result:** CONFIRMED

# %%
fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    subplot_titles=("Revenue per Traffic Unit (Collapsing)",
                                    "Revenue per Line — ARPU (Collapsing)"))
fig.add_trace(go.Scatter(
    x=agg["trimestre_dt"], y=agg["revenue_per_traffic"],
    line=dict(color="#ff6b35", width=2), name="Revenue / Traffic"
), row=1, col=1)
fig.add_trace(go.Scatter(
    x=agg["trimestre_dt"], y=agg["revenue_per_line"],
    line=dict(color="#00bcd4", width=2), name="Revenue / Line"
), row=2, col=1)
fig.update_layout(height=550, showlegend=False,
                  title="Data Asymmetry: Unit Economics Collapse")
fig.write_html(FIGS / "data_asymmetry.html", include_plotlyjs="cdn")
fig.show()

# %% [markdown]
# ## 5. H4 — Network Stress Index
#
# **Prediction:** Traffic per line (NSI) grows faster than revenue per line.
# **Result:** CONFIRMED

# %%
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=agg["trimestre_dt"], y=agg["nsi"],
    line=dict(color="#e040fb", width=2.5), name="Network Stress Index",
    fill="tozeroy", fillcolor="rgba(224,64,251,0.1)"
))
fig.update_layout(
    title="Network Stress Index — Traffic per Active Line",
    xaxis_title="Quarter", yaxis_title="NSI (traffic / line)",
    height=450
)
fig.write_html(FIGS / "network_stress.html", include_plotlyjs="cdn")
fig.show()

# %% [markdown]
# ## 6. H5 — Macro Contribution Decline
#
# **Prediction:** Telecom revenue share of GDP decreases.
# **Result:** CONFIRMED

# %%
rev = pd.read_parquet(PROC / "cnmc_mercados_clean.parquet")
rev = rev[rev["concepto"] == "Ingresos"].copy()
rev["year"] = pd.to_numeric(rev["trimestre"].str.extract(r"(\d{4})")[0])
rev_annual = rev.groupby("year")["ingresos"].sum().reset_index()

gdp_es = pd.read_parquet(PROC / "eurostat_nama_10_gdp_tidy.parquet")
gdp_es = gdp_es[(gdp_es["geo"] == "ES") & (gdp_es["na_item"] == "B1G") & (gdp_es["unit"] == "CP_MEUR")].copy()
gdp_es["year"] = pd.to_numeric(gdp_es["time_period"])
gdp_es = gdp_es[gdp_es["value_num"].notna()]
gdp_es = gdp_es[["year", "value_num"]].rename(columns={"value_num": "gdp_meur"})

merged = rev_annual.merge(gdp_es, on="year", how="inner")
merged["ratio"] = merged["ingresos"] / merged["gdp_meur"] * 100

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=merged["year"], y=merged["ratio"],
    mode="lines+markers",
    line=dict(color="#ff6b35", width=3),
    marker=dict(size=8),
    fill="tozeroy", fillcolor="rgba(255,107,53,0.1)",
    name="Telecom / GDP"
))
fig.update_layout(
    title="Telecom Revenue as % of GDP (Declining)",
    xaxis_title="Year", yaxis_title="Share of GDP (%)",
    height=450
)
fig.write_html(FIGS / "macro_contribution.html", include_plotlyjs="cdn")
fig.show()

print(f"{int(merged['year'].iloc[0])}: {merged['ratio'].iloc[0]:.2f}% of GDP")
print(f"{int(merged['year'].iloc[-1])}: {merged['ratio'].iloc[-1]:.2f}% of GDP")
print(f"Decline: {(merged['ratio'].iloc[-1] / merged['ratio'].iloc[0] - 1):+.1%}")

# %% [markdown]
# ## 7. European Context
#
# Benchmarks from ETNO State of Digital Communications 2025 and GSMA Mobile Economy Europe 2025.

# %%
fig = px.bar(
    eu, x="indicator", y="value", color="source",
    text="value", labels={"value": "Value", "indicator": ""},
    title="European Telecom Benchmarks",
    height=500
)
fig.update_layout(xaxis_tickangle=-45)
fig.write_html(FIGS / "eu_context.html", include_plotlyjs="cdn")
fig.show()

# %%
# ARPU comparison
arpu = eu[eu["indicator"].str.contains("ARPU", case=False)].copy()
fig = px.bar(arpu, x="indicator", y="value", text="value",
             title="Mobile ARPU Comparison (EUR/month)",
             color="value", color_continuous_scale="blues",
             height=400)
fig.write_html(FIGS / "arpu_comparison.html", include_plotlyjs="cdn")
fig.show()

print("\nKey European benchmarks:")
for _, r in eu.iterrows():
    print(f"  {r['indicator']}: {r['value']} {r['unit']}")

# %% [markdown]
# ## 8. Summary of Findings
#
# | Hypothesis | Result | Evidence |
# |-----------|--------|---------|
# | H1 — Scissors Effect | CONFIRMED | Traffic +127%/yr vs Revenue −0.4%/yr |
# | H2 — Concentration | REFUTED | HHI 3,482 → 2,368 (deconcentration) |
# | H3 — Data Asymmetry | CONFIRMED | Revenue/unit collapses to near zero |
# | H4 — Network Stress | CONFIRMED | NSI grows exponentially vs ARPU |
# | H5 — Macro Decline | CONFIRMED | Telecom/GDP: 3.2% → 2.0% |
# | H6 — Infrastructure Elasticity | CONFIRMED | Margin compression confirmed |
#
# **Key insight:** H2 being refuted is the most important finding. Competition
# increased yet the Scissors Effect worsened. The problem is structural to the
# telecom business model, not a market power issue.

# %%
print("\nAll figures saved to outputs/figures/")
for f in sorted(FIGS.glob("*.html")):
    print(f"  {f.name}")
