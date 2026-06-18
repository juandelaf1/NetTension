# NetTension — Oral Presentation Script (7 minutes)

> Bilingual ES/EN · Defensa Módulo II · Junio 2026

---

## Slide 1: Opening (30s) — EN

> *Banner slide: NetTension logo + CAGR numbers*

"Good morning. European telecom operators face a structural paradox: **data traffic grows at +127% per year**, yet **revenue declines at −0.4% per year**. This is the Scissors Effect. Over 20 years, this gap is not a blip — it's a systemic failure of the connectivity business model.

NetTension is a neutral, data-driven framework that models this tension using **only observed data** from Spain's regulator CNMC and Eurostat. No simulations. No synthetic data. 41,937 rows of regulatory microdata. 3 million rows of macroeconomic data. Six hypotheses tested."

---

## Slide 2: The Problem (45s) — ES

> *Slide: "The Regulatory Crossroads" — diagram showing traffic↑, revenue→, CAPEX gap*

"El problema tiene tres dimensiones:

**Primero, la tijera tráfico-ingreso.** Si el tráfico crece al 127% anual y los ingresos no crecen, ¿cómo se financia el despliegue de 5G y fibra? La respuesta de Bruselas es el debate Fair Share: que Google, Netflix y Meta contribuyan a los costes de red.

**Segundo, la concentración.** Se asume que el mercado se concentra y eso es malo. Nuestros datos muestran lo contrario.

**Tercero, la asimetría de datos.** Eurostat publica estadísticas agregadas que ocultan realidades locales. Un policy maker que use solo Eurostat subestima sistemáticamente la presión sobre la red en el sur de Europa."

---

## Slide 3: Methodology & Data (45s) — EN

> *Slide: Architecture diagram (Data → ETL → Star Schema → Streamlit)*

"Methodology in one sentence: **Load real data, clean nothing away, compute every KPI with traceable governance.**

Four data layers:
- **Layer 1 — OBSERVED:** CNMC quarterly filings (2005–2025), 31 operators, 52 variables. Eurostat population and GDP.
- **Layer 2 — ESTIMATED:** Derived KPIs — HHI, CAGR, Network Stress Index. All from observed variables, no black boxes.
- **Layer 3 — POLICY_MODEL:** Fair Share scenario parameters from ETNO and GSMA benchmarks.
- **Layer 4 — CONSTANT:** Regulatory thresholds, HHI boundaries, documented inflation.

Every variable has: source, confidence level, review date, reproducibility flag. This is DEC-007/008 compliance."

---

## Slide 4: Results — Hypotheses 1–3 (1min 30s) — ES

> *Slide: 3 charts side by side — Scissors Effect, HHI timeline, Revenue per Traffic*

"Resultados. Seis hipótesis. Vamos por bloques.

**H1 — Efecto Tijera: CONFIRMADA.** El tráfico de datos crece a +127% CAGR. Los ingresos caen al −0.4%. La brecha es de 127 puntos porcentuales. Esto no es sostenible sin un cambio estructural.

**H2 — Ley de Concentración: REFUTADA.** Y esta es la sorpresa. El HHI bajó de 3.482 a 2.368. El mercado español se fragmentó, no se concentró. Más operadores compitiendo. ¿Y qué pasó con la tijera? Empeoró. Esto demuestra que el problema no es de monopolio. **Es estructural.**

**H3 — Asimetría del Dato: CONFIRMADA.** El revenue por unidad de tráfico colapsa a cero. El ARPU por línea cae un 83%. Los operadores transportan exponencialmente más datos por el mismo precio."

---

## Slide 5: Results — Hypotheses 4–6 (1min) — EN

> *Slide: 3 charts — NSI, Macro Contribution, Infrastructure Elasticity*

"H4 — Network Stress: CONFIRMED. Traffic per active line grows exponentially while revenue per line collapses. Infrastructure pressure is off the charts.

H5 — Macro Decline: CONFIRMED. Telecom went from 3.2% of Spain's GDP in 2005 to just 2.0% in 2025. A 39% decline in economic weight.

H6 — Infrastructure Elasticity: CONFIRMED. The margin between data transport cost and revenue per line compresses to near zero.

**The pattern is consistent across all six hypotheses: the telecom business model is under structural stress that competition alone cannot resolve.** "

---

## Slide 6: Policy Implications (1min) — ES

> *Slide: Fair Share Simulator mockup + EU vs USA ARPU comparison*

"¿Qué implica esto para la política europea?

**Fair Share es una palanca legítima.** Nuestro simulador What-If muestra que una contribución OTT del 10–20% podría cerrar entre el 15 y el 30% de la brecha de inversión. BEREC cuestiona la premisa del free-riding, pero el dato objetivo es que el tráfico de los seis grandes (Google, Meta, Netflix, Amazon, Apple, Microsoft) representa el 50% del tráfico global.

**El ARPU europeo es un tercio del estadounidense**: 14,8 EUR/mes frente a 41,7 EUR/mes. Con ese margen, es imposible mantener el ritmo de inversión.

**El riesgo de infraestructura china:** Strand Consult documenta que Huawei lidera el mercado de RAN 5G fuera de Norteamérica. La dependencia tecnológica es un riesgo geopolítico que el debate regulatorio no puede ignorar."

---

## Slide 7: Dashboard Demo (1min 15s) — EN

> *Live demo of Streamlit dashboard — 5 pages*

"Let me walk through the dashboard in 60 seconds.

**Page 1 — Market Overview:** The Scissors Effect in full view. Traffic index at 10,000+. Revenue index at 90. KPI cards show the CAGR gap in real time.

**Page 2 — Network Stress:** HHI timeline with color-coded concentration zones. Network Stress Index. Elasticity margins.

**Page 3 — European Context:** ARPU comparison across EU, USA, Japan, South Korea. CAPEX per capita. 5G adoption trajectories.

**Page 4 — Fair Share Simulator:** Three sliders. Move OTT contribution from 0% to 30%. Watch the investment gap close. What-if scenarios in real time.

**Page 5 — Governance & Bias Audit:** Every data source with its layer, confidence level, and limitations. Transparency by design.

The dashboard is deployed on Streamlit Cloud. Public access. Try it yourself."

---

## Slide 8: Conclusions & Q&A (30s) — ES

> *Slide: Summary table + "Thank you"*

"Para cerrar, tres ideas clave:

**Uno: La tijera tráfico-ingreso es real y empeora.** 127% vs −0.4%. No es un problema de competencia — H2 lo refuta — es estructural.

**Dos: Los datos granulares importan.** CNMC revela lo que Eurostat oculta. Las decisiones políticas basadas solo en agregados europeos son incompletas.

**Tres: Fair Share no es ideología, es ingeniería financiera.** Los números demuestran que la contribución OTT es una palanca viable para cerrar la brecha de inversión.

El dashboard está disponible en [URL]. Código y datos en github.com/juandelaf1/NetTension.

Preguntas."

---

## Timing Summary

| Section | Duration | Language |
|---------|----------|----------|
| Opening | 30s | EN |
| The Problem | 45s | ES |
| Methodology | 45s | EN |
| Results H1–H3 | 1min 30s | ES |
| Results H4–H6 | 1min | EN |
| Policy Implications | 1min | ES |
| Dashboard Demo | 1min 15s | EN |
| Closing | 30s | ES |
| **Total** | **~7min 15s** | — |
