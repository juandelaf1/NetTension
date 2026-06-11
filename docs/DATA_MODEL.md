# NetTension — Power BI Data Model Specification

## Quick Start (5 minutos)

### 1. Importar datos
```
Power BI Desktop → Obtener datos → Parquet → Seleccionar TODOS estos archivos:
  data/processed/fact_observed_agg.parquet   (tabla principal)
  data/processed/dim_time.parquet            (dimensión tiempo)
  data/processed/dim_operator.parquet        (dimensión operadores)
  data/processed/dim_service.parquet         (dimensión servicios)
  data/processed/dim_geography.parquet       (dimensión geografía)
  data/processed/fact_eurostat_es.parquet    (PIB/población)
  data/processed/kpi_hhi.parquet             (HHI trimestral)
  data/processed/dim_eu_context.parquet      (benchmarks UE)
```

### 2. Crear relaciones (Vista Modelo)

| Tabla 1 | Cardinalidad | Tabla 2 | Columna de unión |
|---------|-------------|---------|-----------------|
| fact_observed_agg | * → 1 | dim_time | trimestre_dt → time_key |
| fact_observed_agg | * → 1 | dim_operator | (no hay FK directa — para drill-down usar cnmc_mercados_clean) |
| fact_observed_agg | * → 1 | dim_service | (no hay FK directa) |
| fact_eurostat_es | * → 1 | dim_time | year → year |
| kpi_hhi | * → 1 | dim_time | trimestre_dt → time_key |

### 3. Crear medidas DAX
Copia-pega todas las medidas de la sección "DAX Measures" abajo.

### 4. Crear parámetros What-If (Página 4)
```
Modelado → Nuevo parámetro → What-If:
  1. "OTT Contribution"     | 0% – 50% | Incremento: 1 | Default: 0
  2. "CAPEX Shock"          | -20% – 20% | Incremento: 1 | Default: 0
  3. "Traffic Growth Mult." | 0.5x – 3.0x | Incremento: 0.1 | Default: 1.0
```

### 5. Construir 5 páginas (ver layouts abajo)

---

## Architecture: Star Schema

## Table Definitions

### Fact_Observed (CNMC Mercados)
Source: `data/processed/cnmc_mercados_clean.parquet`

| Column | Type | Description |
|--------|------|-------------|
| trimestre_dt | Date | Period start date (2005-01-01) |
| operador | String | Operator name |
| servicio | String | Service type |
| concepto | String | Metric type |
| ingresos | Float | Revenue (Mn EUR) |
| ingresos_por_operador | Float | Revenue by operator (Mn EUR) |
| trafico | Float | Voice traffic (minutes) |
| trafico_de_datos | Float | Data traffic (GB/TB) |
| lineas_o_accesos | Float | Total active lines |
| lineas_o_accesos_por_operador | Float | Active lines by operator |
| portabilidades | Float | Number portings |
| tecnologia_de_acceso | String | Access technology (FTTH, xDSL, etc.) |

### Dim_Time
Generated from `trimestre_dt` in Power BI or created as lookup table.

| Column | Type | Description |
|--------|------|-------------|
| time_key | Date | First day of quarter |
| year | Int | 2005–2025 |
| quarter | Int | 1–4 |
| year_quarter | String | "2005 Q1" |
| year_label | String | "2005" |

### Dim_Operator
From distinct operators in Fact_Observed.

| Column | Type | Description |
|--------|------|-------------|
| operator_key | String | Operator name |
| operator_group | String | Group classification (Incumbent, Competitor, Wholesale, Regional, Other) |
| is_incumbent | Boolean | True if Movistar/Telefónica |

### Dim_Service
From distinct service/concept combinations.

| Column | Type | Description |
|--------|------|-------------|
| service_key | String | servicio + concepto |
| servicio | String | Retail, wholesale, etc. |
| concepto | String | Metric name |
| market_type | String | Minorista / Mayorista |
| category | String | Voice, Data, Access, Audiovisual |

### Dim_Geography
| Column | Type | Description |
|--------|------|-------------|
| geography_key | String | Country code (ES) |
| pais | String | Country name |
| geo_code | String | Eurostat code (ES) |
| region | String | EU, EFTA, etc. |

### Fact_Eurostat
Source: `data/processed/eurostat_demo_pjan_tidy.parquet`, `eurostat_nama_10_gdp_tidy.parquet`

| Column | Type | Description |
|--------|------|-------------|
| time_period | Int | Year |
| geo | String | Country code |
| population | Float | Population count |
| gdp_meur | Float | GDP (million EUR, current prices) |
| gdp_per_capita | Float | GDP per capita (EUR) |

### Fact_KPI
Pre-computed KPIs for dashboard charts.

| Column | Type | Description |
|--------|------|-------------|
| trimestre_dt | Date | Period |
| hhi | Float | Herfindahl-Hirschman Index |
| nsi | Float | Network Stress Index |
| revenue_per_traffic | Float | Revenue per data unit |
| traffic_per_line | Float | Data traffic per active line |
| revenue_per_line | Float | Revenue per active line |

## DAX Measures

```dax
-- ============================================================
-- CORE METRICS
-- ============================================================

-- Total Revenue (Mn EUR)
Total Revenue = SUM(Fact_Observed[ingresos])

-- Total Data Traffic
Total Data Traffic = SUM(Fact_Observed[trafico_de_datos])

-- Total Voice Traffic
Total Voice Traffic = SUM(Fact_Observed[trafico])

-- Total Active Lines
Total Lines = SUM(Fact_Observed[lineas_o_accesos])

-- Data Traffic per Line (NSI)
Network Stress Index = 
    DIVIDE(
        [Total Data Traffic],
        [Total Lines],
        0
    )

-- Revenue per Data Unit
Revenue per Traffic Unit = 
    DIVIDE(
        [Total Revenue],
        [Total Data Traffic],
        0
    )

-- ============================================================
-- HHI (Herfindahl-Hirschman Index)
-- ============================================================
HHI = 
    VAR RevenueByOperator = 
        SUMMARIZE(
            Fact_Observed,
            Dim_Operator[operator_key],
            "OpRevenue", SUM(Fact_Observed[ingresos_por_operador])
        )
    VAR TotalRevenue = SUMX(RevenueByOperator, [OpRevenue])
    VAR ShareSquared = 
        SUMX(
            RevenueByOperator,
            DIVIDE([OpRevenue], TotalRevenue, 0) ^ 2
        )
    RETURN
        ShareSquared * 10000

-- ============================================================
-- CAGR CALCULATION (using time intelligence)
-- ============================================================
CAGR Traffic = 
    VAR FirstPeriod = FIRSTDATE(Dim_Time[time_key])
    VAR LastPeriod = LASTDATE(Dim_Time[time_key])
    VAR FirstValue = 
        CALCULATE(
            [Total Data Traffic],
            Dim_Time[time_key] = FirstPeriod,
            ALL(Dim_Time)
        )
    VAR LastValue = 
        CALCULATE(
            [Total Data Traffic],
            Dim_Time[time_key] = LastPeriod,
            ALL(Dim_Time)
        )
    VAR Years = DATEDIFF(FirstPeriod, LastPeriod, YEAR)
    RETURN
        IF(
            FirstValue > 0 && LastValue > 0 && Years > 0,
            (LastValue / FirstValue) ^ (1 / Years) - 1,
            BLANK()
        )

CAGR Revenue = 
    VAR FirstPeriod = FIRSTDATE(Dim_Time[time_key])
    VAR LastPeriod = LASTDATE(Dim_Time[time_key])
    VAR FirstValue = 
        CALCULATE(
            [Total Revenue],
            Dim_Time[time_key] = FirstPeriod,
            ALL(Dim_Time)
        )
    VAR LastValue = 
        CALCULATE(
            [Total Revenue],
            Dim_Time[time_key] = LastPeriod,
            ALL(Dim_Time)
        )
    VAR Years = DATEDIFF(FirstPeriod, LastPeriod, YEAR)
    RETURN
        IF(
            FirstValue > 0 && LastValue > 0 && Years > 0,
            (LastValue / FirstValue) ^ (1 / Years) - 1,
            BLANK()
        )

-- ============================================================
-- SCISSORS EFFECT (Traffic vs Revenue indexed to 100)
-- ============================================================
Traffic Index (Base=100) = 
    VAR BaseValue = 
        CALCULATE(
            [Total Data Traffic],
            Dim_Time[year] = MIN(Dim_Time[year]),
            ALL(Dim_Time)
        )
    RETURN
        DIVIDE([Total Data Traffic], BaseValue, 0) * 100

Revenue Index (Base=100) = 
    VAR BaseValue = 
        CALCULATE(
            [Total Revenue],
            Dim_Time[year] = MIN(Dim_Time[year]),
            ALL(Dim_Time)
        )
    RETURN
        DIVIDE([Total Revenue], BaseValue, 0) * 100

-- ============================================================
-- MACRO CONTRIBUTION
-- ============================================================
Macro Contribution Ratio = 
    DIVIDE(
        [Total Revenue] * 1000000,  -- Convert Mn EUR to EUR
        SUM(Fact_Eurostat[gdp_meur]) * 1000000,
        0
    )

-- ============================================================
-- DIGITAL DENSITY
-- ============================================================
Digital Density (per 100 pop) = 
    VAR TotalPop = SUM(Fact_Eurostat[population])
    RETURN
        DIVIDE([Total Lines], TotalPop, 0) * 100

-- ============================================================
-- WHAT-IF PARAMETER MEASURES (Fair Share Simulator)
-- ============================================================
Fair Share CAPEX Relief = 
    -- CAPEX_required from ETNO: €174bn by 2030 (€17.4bn/year)
    VAR CAPEX_Annual_Bn = 17.4  -- billion EUR
    VAR OTT_Share = 
        DIVIDE(
            SELECTEDVALUE(Scenario_FairShare[ott_contribution_pct], 0),
            100
        )
    RETURN
        CAPEX_Annual_Bn * OTT_Share

Revenue Impact with Fair Share = 
    [Total Revenue] + [Fair Share CAPEX Relief] * 1000  -- Convert Bn to Mn

-- ============================================================
-- MARKET CONCENTRATION CLASSIFICATION
-- ============================================================
Market Concentration Level = 
    SWITCH(
        TRUE(),
        [HHI] < 1000, "Competitive",
        [HHI] <= 2500, "Moderately Concentrated",
        "Highly Concentrated"
    )
```

## Dashboard Page Layout

### Page 1: Market Overview (España)
```
┌──────────────────────────────────────────────────────────┐
│  Header: NetTension — EU Telecom Market Stress Model     │
│  KPI Cards: Revenue | Traffic | HHI | CAGR Gap          │
├────────────────┬────────────────┬───────────────────────┤
│ Traffic vs Rev │  HHI Over Time │  Revenue by Service   │
│ (Index 100)    │  (Line Chart)  │  (Treemap/Bar)        │
│ (Line Chart)   │                │                       │
├────────────────┴────────────────┴───────────────────────┤
│  Filters: Year Range | Service Type | Operator           │
└──────────────────────────────────────────────────────────┘
```

### Page 2: Network Stress & Infrastructure
```
┌──────────────────────────────────────────────────────────┐
│  Header: Network Stress & Infrastructure Pressure        │
│  KPI: NSI | Revenue/Traffic | CAGR Traffic | CAGR Rev    │
├────────────────┬────────────────┬───────────────────────┤
│ Network Stress │  Lines by Tech │  Revenue per Traffic   │
│ Index Over Time│  (Stacked Area)│  Unit (Line Chart)     │
├────────────────┴────────────────┴───────────────────────┤
│  Data Traffic Growth (Year-over-Year %)                  │
│  (Column Chart with trendline)                           │
└──────────────────────────────────────────────────────────┘
```

### Page 3: European Context & Regulatory Crossroads
```
┌──────────────────────────────────────────────────────────┐
│  Header: European Regulatory Crossroads                  │
├────────────┬──────────────────┬─────────────────────────┤
│ EU vs USA  │ 5G Adoption by   │ Investment per Capita    │
│ ARPU       │ Country (Map)    │ (Bar Chart)              │
│ (Bar Chart)│                  │                          │
├────────────┴──────────────────┴─────────────────────────┤
│  Key Regulatory Milestones Timeline                      │
│  2020: EU 5G Toolbox | 2023: BEREC Fair Share Report    │
│  2025: DNA Proposal Art.189 | 2026: Debate continues     │
└──────────────────────────────────────────────────────────┘
```

### Page 4: Fair Share Simulator (What-If)
```
┌──────────────────────────────────────────────────────────┐
│  Header: Scenario Simulator — Fair Share Impact          │
├────────────────────────┬────────────────────────────────┤
│  Controls:             │  Output Charts:                 │
│  OTT Contribution: 0%  │  Revenue Impact (Before/After)  │
│     [====●=========]   │  Investment Gap Closure %       │
│  CAPEX Shock: 0%       │  Traffic Growth Scenarios       │
│     [====●=========]   │                                  │
│  Traffic Growth: 1.0x  │                                  │
│     [====●=========]   │                                  │
├────────────────────────┴────────────────────────────────┤
│  Scenario Comparison Table (Base vs Policy vs Mixed)     │
└──────────────────────────────────────────────────────────┘
```

### Page 5: Governance & Bias Audit
```
┌──────────────────────────────────────────────────────────┐
│  Header: Governance, Methodology & Bias Audit            │
├────────────────────────┬────────────────────────────────┤
│ Data Source Inventory  │ Governance Layer Legend         │
│ (Table: Source, Layer,  │  OBSERVED (green)              │
│  Confidence, Reproduc.)│  ESTIMATED (yellow)             │
│                        │  POLICY_MODEL (orange)          │
│                        │  CONSTANT (gray)                │
├────────────────────────┴────────────────────────────────┤
│  Limitations & Known Issues                              │
│  • CNMC methodology change ~2012 in data traffic        │
│  • Eurostat ISOC_TF: fixed broadband only, no mobile    │
│  • Sandvine data: vendor methodology, not peer-reviewed │
│  • Huawei market share: paywalled (Strand Consult)      │
└──────────────────────────────────────────────────────────┘
```

## Detailed Page Build Instructions

### Page 1: Market Overview
Objetivo: Mostrar el Efecto Tijera (tráfico vs ingresos) y KPIs principales.

| Visual | Tipo | Datos |
|--------|------|-------|
| KPI Cards (4) | Card | Total Revenue, Total Data Traffic, HHI, CAGR Gap |
| Scissors Effect | Line Chart | X: dim_time[year_quarter], Y: Traffic Index e Revenue Index |
| HHI Timeline | Line Chart | X: dim_time[year_quarter], Y: kpi_hhi[hhi] |
| YoY Traffic Growth | Column Chart | X: dim_time[year], Y: % cambio anual de tráfico |
| Slicers (top) | Slicer | dim_time[year] (range), dim_time[quarter] |

### Page 2: Network Stress
Objetivo: Presión sobre la infraestructura por operador y tecnología.

| Visual | Tipo | Datos |
|--------|------|-------|
| NSI over time | Line Chart | X: year_quarter, Y: fact_observed_agg[nsi] |
| Revenue per Traffic | Line Chart | X: year_quarter, Y: fact_observed_agg[revenue_per_traffic] |
| Revenue per Line | Area Chart | X: year_quarter, Y: fact_observed_agg[revenue_per_line] |
| Data Traffic by Operator | Bar Chart | (usar cnmc_mercados_clean si está importada) |

### Page 3: European Context
Objetivo: Comparativa UE vs USA vs Asia usando datos ETNO/GSMA.

| Visual | Tipo | Datos |
|--------|------|-------|
| ARPU Comparison | Bar Chart | dim_eu_context, filtrar por "ARPU" |
| CAPEX per capita | Bar Chart | dim_eu_context, filtrar por "CAPEX" |
| Key Indicators | Table | dim_eu_context[indicator, value, unit, source] |
| Regulatory Timeline | Text box | Hitos: 2020 5G Toolbox → 2023 BEREC → 2025 DNA Art.189 |

### Page 4: Fair Share Simulator
Objetivo: Simular impacto de contribución OTT, shock CAPEX y crecimiento.

This page uses the What-If parameters created earlier.

| Visual | Tipo | Datos |
|--------|------|-------|
| Slicers (3) | What-If Slider | OTT Contribution, CAPEX Shock, Traffic Growth |
| Revenue Impact | Gauge | Measure: [Revenue Impact with Fair Share] |
| Investment Gap | Gauge | Measure: [Fair Share CAPEX Relief] |
| Scenario Table | Table | Comparativa Base vs Policy vs Mixed |

### Page 5: Governance & Bias Audit
Objetivo: Transparencia metodológica y limitaciones.

| Visual | Tipo | Datos |
|--------|------|-------|
| Data Sources | Table | Crear tabla manual con: Source, Layer, Confidence, Reproducible |
| Governance Legend | Shape | 4 recuadros de colores: OBSERVED/ESTIMATED/POLICY_MODEL/CONSTANT |
| Limitations | Text box | Lista de limitaciones conocidas (cambio metodología 2012, ISOC_TF sin móvil, Sandvine no peer-reviewed) |

## DAX Measures

All DAX measures are defined in the section above. Import them into Power BI using:
```
Modelado → Nueva medida → Pegar código DAX
```

## Power BI Setup Instructions

1. Open Power BI Desktop → New file
2. Get Data → Parquet → Navigate to `data/processed/` → Select ALL .parquet files → Load
3. Model view → Create relationships per Quick Start table above
4. Modeling → New parameter → Create 3 What-If parameters
5. Copy all DAX measures from section above
6. Build 5 pages per layouts above
7. File → Publish → Power BI Service → Get embed URL
8. Share link as public (or embed for portfolio)
