# EDA Summary — EU Digital Sovereignty Dashboard

Generated: 2026-06-09

## 1. CNMC Datos Generales

| Property | Value |
|---|---|
| File | `cnmc_datos_generales_2005T1_2025T4.csv` |
| Rows (excl header) | 3,319 |
| Columns | 14 |
| Format | Normalized (long) — each row is a concept/operator/quarter combination |
| Delimiter | `;` |
| Encoding | ISO-8859-1 |
| License | CC-BY-SA-4.0 |

### Columns
`_id`, `trimestre`, `pais`, `tipo_de_mercado`, `servicio`, `concepto`, `operador`, `tipo_de_ingreso`, `tipo_de_paquete`, `unidades`, `ingresos`, `ingresos_por_operador`, `empleados_por_operador`, `paquetes`

### Key Findings
- Covers quarters 2005T1 through 2025T4
- `concepto` field contains metric names like "Numero de empleados", "Ingresos", "Ingresos por operador", etc.
- `operador` includes many entities: Canal Sur (RTVA), Telefonica, Vodafone, Orange, MasMovil, Euskaltel, etc.
- Numeric values stored as strings with decimal commas (e.g., `973.00000`)
- `N/A` used as null placeholder
- First row example: `_id=1, trimestre=2005T1, pais=España, concepto=Número de empleados, operador=Canal Sur (RTVA), empleados_por_operador=973.00000`

---

## 2. CNMC Mercados (5 files)

| File | Rows (excl header) | Size |
|---|---|---|
| `cnmc_mercados_2005_2009.csv` | 7,809 | 1.8 MB |
| `cnmc_mercados_2010_2014.csv` | 2.5 MB | |
| `cnmc_mercados_2015_2019.csv` | 2.6 MB | |
| `cnmc_mercados_2020_2024.csv` | 10,900 | 2.6 MB |
| `cnmc_mercados_2025T1_2025T4.csv` | 485 KB | |

All 5 files share the **identical 48-column schema** (verified from 2020-2024):

### Columns
`_id`, `trimestre`, `pais`, `tipo_de_mercado`, `servicio`, `concepto`, `operador`, `tipo_de_ingreso`, `tipo_de_cliente`, `segmento`, `tipo_de_trafico`, `tipo_de_contrato`, `tipo_de_linea`, `tipo_de_mensaje`, `tipo_de_trafico_de_mensaje`, `tecnologia_de_acceso`, `velocidad_baf`, `tipo_de_oferta`, `tipo_de_tarifa`, `tipo_de_ce_minorista`, `tipo_de_circuito`, `tipo_de_emision`, `tipo_de_operador`, `tipo_de_medio`, `tipo_de_publicidad`, `tipo_de_contratacion`, `tipo_servicio_audiovisual_mayorista`, `tipo_de_ba_may`, `tipo_de_interconexion`, `tipo_de_tarificacion_en_interconexion`, `tipo_de_ambito`, `tipo_de_acceso_de_infraestructuras`, `unidades`, `ingresos`, `ingresos_por_operador`, `clientes`, `clientes_por_operador`, `lineas_o_accesos`, `tasa_de_penetracion`, `lineas_o_accesos_por_operador`, `portabilidades`, `trafico`, `trafico_por_operador`, `mensajes`, `mensajes_por_operador_1`, `trafico_de_datos`, `circuitos`, `publicidad`, `contrataciones`

### Key Findings
- Dimension columns (tipo_de_\*) provide high granularity: by service, technology, client type, traffic type, contract type, line type, access technology, speed, offer type, tariff, etc.
- Measure columns include: `ingresos`, `clientes`, `lineas_o_accesos`, `tasa_de_penetracion`, `portabilidades`, `trafico`, `mensajes`, `trafico_de_datos`, `circuitos`, `publicidad`, `contrataciones`
- Can be stacked/union-merged into a single Mercados table (2005-2025)
- `tasa_de_penetracion` is a calculated rate (per 100 inhabitants), useful for per-capita metrics
- `lineas_o_accesos` is the main subscriber/subscription count variable
- `trafico` likely in minutes for voice, MB for data depending on service type

---

## 3. Eurostat ISOC_TF (Fixed Broadband Internet Traffic)

| Property | Value |
|---|---|
| File | `eurostat_isoc_tf.json` |
| Format | JSON-stat v2.0 |
| Source | ESTAT |
| Updated | 2025-08-11 |
| Dimensions | freq (1), unit (2), geo (29), time (15) |
| Series count | 1 × 2 × 29 × 15 = 870 values |

### Key Findings
- 29 geographical areas (not full EU27 — missing ~10 countries)
- 15 time periods (likely 2010-2024)
- 2 units (probably GB/month and TB or similar)
- Only fixed broadband traffic — not mobile
- Limited coverage for EU-wide analysis
- Values: 0.0415 to 2.4+ (interpretation depends on unit)

---

## 4. Eurostat demo_pjan (Population)

| Property | Value |
|---|---|
| File | `eurostat_demo_pjan.tsv.gz` |
| Format | SDMX-TSV (compact) |
| Rows | 17,746 |
| Dimensions | freq, unit, age, sex, geo |
| Time columns | 1960 → 2025 (66 years) |

### Column Structure
Dimensions: `freq`, `unit`, `age`, `sex`, `geo\TIME_PERIOD` (pipe-separated from years 1960-2025)

### Key Findings
- All EU/EEA countries covered
- Age groups from TOTAL to single-year and 5-year bands
- Both sexes: T (total), M (male), F (female)
- Unit: usually PS (persons)
- SDMX-TSV format requires transpose: dimensions as rows, years as columns
- Flags may be appended with space separator (e.g., `12345.6 p`)

---

## 5. Eurostat nama_10_gdp (GDP)

| Property | Value |
|---|---|
| File | `eurostat_nama_10_gdp.tsv.gz` |
| Format | SDMX-TSV (compact) |
| Rows | 36,507 |
| Dimensions | freq, unit, na_item, geo |
| Time columns | 1975 → 2025 (51 years) |

### Column Structure
Dimensions: `freq`, `unit`, `na_item`, `geo\TIME_PERIOD` (pipe-separated from years 1975-2025)

### Key Findings
- Full EU27 + candidate countries
- `na_item` includes GDP at market prices (B1GQ) and many sub-components
- Units: CP_MEUR (current prices, millions EUR), CLV15_MEUR (chain-linked volumes, 2015 reference)
- ~36K rows × 51 time columns = high cardinality
- Same SDMX-TSV transpose requirement as demo_pjan

---

## Summary: Variable Coverage Assessment

| Variable Area | CNMC Mercados | CNMC Datos Generales | ISOC_TF | demo_pjan | nama_10_gdp |
|---|---|---|---|---|---|
| Revenue/Ingresos | Yes (ingresos) | Yes (ingresos) | No | No | Yes (GDP) |
| Investment/CAPEX | No | No (no explicit CAPEX) | No | No | No |
| Broadband subscriptions | Yes (lineas_o_accesos) | No | No | No | No |
| Mobile subscriptions | Yes (lineas_o_accesos) | No | No | No | No |
| Traffic (fixed) | Yes (trafico) | No | Yes | No | No |
| Traffic (mobile) | Yes (trafico) | No | No | No | No |
| Employees | No | Yes (empleados_por_operador) | No | No | No |
| Population | No | No | No | Yes | No |
| GDP per capita | No | No | No | Yes | Yes |
| Bundling | No | Yes (paquetes) | No | No | No |
| Portability | Yes (portabilidades) | No | No | No | No |

**Next phase**: Map CNMC columns to dashboard model variables, design ETL for stacked Mercados table, and load into Power BI as Fact_Observed_Data.
