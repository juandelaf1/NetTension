# INFORME ESTRATÉGICO MULTIDISCIPLINAR
## NetTension — Análisis de oportunidades analíticas y comerciales

*Comité: Data Scientist, Data Analyst, Economista Industrial, Regulador TELCO, Experto Competencia, Académico, Consultor Estratégico*

---

## 1. QUICK WINS (0-2 meses)

### 1.1 Elasticidad Precio de la Demanda de Banda Ancha
| Campo | Detalle |
|-------|---------|
| **Objetivo** | Medir sensibilidad del tráfico al precio (ingreso/GB) |
| **Variables** | revenue_per_traffic, data_traffic, trimestre |
| **Metodología** | Regresión log-log: `log(traffic) ~ log(revenue_per_traffic) + tendencia` |
| **Valor** | Demostrar qué tan "esencial" es la conectividad |
| **Dificultad** | Baja (OLS con datos existentes) |
| **Prioridad** | Alta |
| **Académico** | Alto — base para papers de economía digital |
| **Comercial** | Medio — insumo para lobbying regulatorio |

### 1.2 Tasa de Sustitución Voz → Datos
| Campo | Detalle |
|-------|---------|
| **Objetivo** | Medir canibalización de voz por datos |
| **Variables** | voice_traffic, data_traffic, trimestre |
| **Metodología** | Correlación cruzada + cointegración (Engle-Granger) |
| **Valor** | Explicar por qué los ingresos de voz colapsan |
| **Dificultad** | Baja (datos ya limpios) |
| **Prioridad** | Alta |
| **Académico** | Medio |
| **Comercial** | Medio |

### 1.3 Índice de Presión Regulatoria
| Campo | Detalle |
|-------|---------|
| **Objetivo** | Cuantificar el efecto de decisiones regulatorias (banda 5G, net neutrality) sobre el estrés |
| **Variables** | Eventos regulatorios codificados (1/0) + revenue, HHI, tráfico |
| **Metodología** | Difference-in-Differences con ventana de eventos |
| **Valor** | Medir impacto regulatorio cuantitativamente |
| **Dificultad** | Media |
| **Prioridad** | Alta |
| **Académico** | Muy alto — informa a policymakers |

---

## 2. NUEVAS HIPÓTESIS FALSABLES

### H7 — Operador Incumbent vs Competidores
**Predicción:** El operador incumbent (Telefónica) muestra menor elasticidad ingreso-tráfico que competidores → estructura de costes fijos altos + mayor poder de mercado residual.

**Variables:** operador, ingresos_por_operador, trafico, group (dim_operator)

### H8 — Convergencia Fijo-Móvil
**Predicción:** Los operadores con oferta convergente (fijo+móvil) tienen menor ARPU churn y mayor data_traffic per subscriber que los mono-producto.

### H9 — Efecto Estacional del Tráfico
**Predicción:** El tráfico de datos muestra estacionalidad anual (picos en Q4, valles en Q1) que se ha ido atenuando con la penetración de smartphones.

### H10 — Asimetría Norte-Sur Europeo
**Predicción:** España muestra mayor ratio NSI/ARPU que Alemania o Francia → justifica diferentes políticas regulatorias (Fair Share más urgente en Sur).

---

## 3. MODELOS PREDICTIVOS POSIBLES

| Modelo | Input | Output | Técnica | UX |
|--------|-------|--------|---------|-----|
| Previsión Tráfico | Series temporales (2005-2024) | Tráfico 2025-2030 | ARIMA/SARIMA/Prophet | Gráfico con bandas confianza |
| Predicción HHI | revenue_por_operador histórico | HHI a 4 trimestres | LSTM o VAR | Dashboard con alerta si HHI >2500 |
| Churn de Operadores | market_share, entradas/salidas | Probabilidad de entrada de nuevo operador | Modelos de supervivencia | Matriz de riesgo competitivo |
| Déficit de Inversión | tráfico, ingresos, CAPEX proxy | CapEx requerido para mantener red | Regresión ridge | Fair Share Simulator mejorado |
| Cluster de Países EU | variables CNMC para España + Eurostat para otros | Grupos de países por estrés de red | K-means + PCA | Mapa de calor EU |

---

## 4. SIMULACIONES REGULATORIAS

### 4.1 Fair Share Avanzado (modelo no-lineal)
Modelar elasticidad del tráfico al precio OTT. Si Google/Meta pagan, ¿reducen tráfico o lo mantienen? Usar datos Sandvine (Big 6 = 50% tráfico) con escenarios de elasticidad (0.1, 0.5, 0.9).

### 4.2 Net Neutrality Relajada
Simular escenario donde operadores pueden priorizar tráfico (zero-rating, fast lanes) → impacto en ARPU, NSI, y bienestar del consumidor.

### 4.3 Consumo Energético y Sostenibilidad
Cruce con datos de consumo energético de redes (proxy: OPEX / línea) para construir NSI verde: huella de carbono por GB.

### 4.4 SIM Swap y Fraude
Variables de portabilidad + número de operadores podrían modelar riesgo de fraude SIM swap (relevante para regulador y banca).

---

## 5. KPIs ADICIONALES

| KPI | Fórmula | Fuente |
|-----|---------|--------|
| **RevPAC** (Revenue per Access Connection) | revenue / total_lines | CNMC Mercados |
| **CAC** (Customer Acquisition Cost proxy) | ingresos de cuotas de alta / nuevos clientes | CNMC (cuota concepto) |
| **Eficiencia de Red** | data_traffic / OPEX proxy | CNMC + estimación |
| **Ratio de Apalancamiento Operativo** | ΔRevenue / 1% ΔTraffic | Derivado |
| **TCP** (Tráfico por Cápita) | data_traffic / población | CNMC + Eurostat |
| **Precio por MB** | revenue / data_traffic | Ya existe (revenue_per_traffic) |
| **Índice de Competitividad Dinámica** | ΔHHI × Δnum_operators | Derivado |
| **Sobrecarga Regulatoria** | #eventos regulatorios/año | Exógeno |

---

## 6. RELACIONES CAUSALES POTENCIALES

```
Tráfico (+) ───────→ NSI (+) ───────→ CAPEX (+) ───────→ Deuda (+) ───────→ Riesgo financiero
     ↑                                                                    ↓
     └────────────── Revenue (−) ←── ARPU (−) ←──── Competencia (+)
     
Regulación (Portabilidad) ───→ Churn (+) ───→ Marketing Cost (+) ───→ Revenue (−)
     
Penetración Smartphone ───→ Tráfico (+) ───→ NSI (+) ───→ Presión Fair Share
```

**Test causal:** Granger causality test entre pares: ¿Tráfico causa ingresos? ¿O ingresos causan tráfico (inversión → capacidad → demanda)? Hipótesis: relación bidireccional con lag de 2-4 trimestres.

---

## 7. RIESGOS METODOLÓGICOS

| Riesgo | Severidad | Mitigación |
|--------|-----------|------------|
| Survivorship bias (operadores que salieron del mercado) | Alta | Incluir operadores históricos en dim_operator con active=False |
| Cambio de definiciones CNMC (2005 vs 2025) | Alta | Documentar cambios metodológicos en SOURCES.yaml |
| Causalidad inversa (inversión → tráfico, no al revés) | Media | Test de Granger con lags |
| Heterocedasticidad en regresiones de tráfico | Media | Errores robustos (HC3) |
| Sobreajuste en modelos predictivos | Media | Validación temporal (no aleatoria) |
| Eurostat GDP revisiones | Baja | Usar CP_MEUR (precios corrientes) o PPS |
| Contaminación COVID (2020 Q2-Q3) | Media | Variable dummy + análisis de robustez sin 2020 |

---

## 8. OPORTUNIDADES DE PUBLICACIÓN ACADÉMICA

| Publicación | Revista | Enfoque |
|-------------|---------|---------|
| **Scissors Effect en Telecom** | *Telecommunications Policy* (SSCI) | H1-H6, abordaje científico de la tijera |
| **Fair Share y Elasticidad** | *Information Economics and Policy* | Simulaciones OTT + modelo de elasticidad |
| **Competencia vs Estructural** | *Journal of Regulatory Economics* | H2 refutada como hallazgo central |
| **Data Asymmetry CNMC** | *Statistical Journal of the IAOS* | Metodología de cruce micro/macro datos |
| **NSI como indicador sintético** | *IEEE Access* | Propuesta de nuevo KPI regulatorio |
| **Dashboard para Policy Makers** | *Data & Policy* | Metodología de visualización de datos regulatorios |

---

## 9. OPORTUNIDADES PRODUCTO SaaS

### 9.1 NetTension SaaS
**Propuesta:** Dashboard como servicio para NRAs (reguladores nacionales):
- Input: datos regulatorios en formato estándar (CSV/Parquet)
- Output: dashboard interactivo con KPIs pre-calculados
- Precio: €5,000-15,000/año por país

### 9.2 Fair Share Calculator
**Tool standalone:** Calculadora web para operadores y policymakers:
- Input: País, % OTT, elasticidad
- Output: Gap cerrado, impacto en CAPEX
- Precio: Free (lead gen) + Premium €500/mes

### 9.3 API de Datos Regulatorios
**APIs:** Endpoints para consultar HHI, CAGR, NSI por país/trimestre:
- v1 gratis (España)
- v2 suscripción (multi-país EU)

---

## 10. OPORTUNIDADES DE CONSULTORÍA

| Cliente | Servicio | Valor € |
|---------|----------|---------|
| **CNMC / NRA** | Extensión a más años/mercados | €15-30K |
| **Telefónica** | Benchmarking frente a competidores | €10-20K |
| **ETNO** | Informe Fair Share con datos propios | €25-50K |
| **Comisión Europea (DG CONNECT)** | Estudio de estrés de red EU | €50-100K |
| **Inversores (Private Equity)** | Due diligence de mercado TELCO | €5-15K |
| **Consultoras (BCG, McKinsey)** | Input para proyectos TELCO | €3-10K/licencia |

---

## ROADMAP 6 MESES

| Mes | Hito | Responsable |
|-----|------|-------------|
| M1 | Quick Wins (H7-H10, elasticidad, sustitución) | Data Scientist |
| M1 | CI/CD estable, tests en Docker | Ingeniero |
| M2 | Modelo predictivo tráfico (Prophet) | Data Scientist |
| M2 | Fair Share Simulator v2 (no-lineal) | Economista |
| M3 | Dashboard Streamlit v2 (multi-país) | Full Stack |
| M3 | Primer paper: Scissors Effect | Académico |
| M4 | Landing page + Fair Share Calculator | Producto |
| M5 | Reuniones con CNMC/ETNO | Consultor |
| M6 | Release v2.0: multi-país + predictivo | Todos |

## ROADMAP 12 MESES

| Mes | Hito |
|-----|------|
| M7 | Integrar Italia (AGCOM), Portugal (ANACOM) |
| M8 | Dashboard Saas MVP (3 países) |
| M9 | Segundo paper: H2 refutada y sus implicaciones |
| M9 | Zero-Touch API v1 |
| M10 | Caso de uso: inversor PE |
| M11 | Pilot con NRA real (acuerdo) |
| M12 | Release v3.0: 5 países + predicción |

## ROADMAP 24 MESES

| Trimestre | Hito |
|-----------|------|
| T1-Q1 | 8 países EU (top operadores) |
| T1-Q2 | Fair Share Impact Report (en colaboración ETNO) |
| T1-Q3 | SaaS lanzamiento comercial |
| T1-Q4 | 12 países, API pública |
| T2-Q1 | Paper "Network Stress Index" aceptado |
| T2-Q2 | Cliente consultoría NRA confirmado |
| T2-Q3 | Producto SaaS en 3 NRAs |
| T2-Q4 | Revenue recurrente > €100K ARR |

---

## POTENCIAL DE MONETIZACIÓN

| Stream | Año 1 | Año 2 | Año 3 |
|--------|-------|-------|-------|
| Consulting (informes) | €15K | €40K | €80K |
| SaaS (licencias NRA) | €0 | €30K | €120K |
| API (desarrolladores) | €0 | €5K | €20K |
| Fair Share Calculator | €0 | €0 (lead gen) | €10K (premium) |
| **Total** | **€15K** | **€75K** | **€230K** |

---

## POTENCIAL DE PUBLICACIÓN CIENTÍFICA

| Paper | Revista | Cuartil | Probabilidad aceptación |
|-------|---------|---------|------------------------|
| Scissors Effect in Telecom | Telecommunications Policy | Q1 | 60% |
| H2 Refutation: Structural Problem | Journal of Regulatory Economics | Q1 | 30% |
| Network Stress Index | IEEE Access | Q2 | 80% |
| Fair Share Elasticity Model | Information Economics & Policy | Q1 | 40% |

---

## RESUMEN EJECUTIVO

**NetTension** no es solo un dashboard — es una **plataforma analítica sectorial** con potencial para:

1. **Corto plazo** (1-2 meses): 3 quick wins → papers, casos de uso
2. **Medio plazo** (3-6 meses): SaaS + consultoría + comunidad
3. **Largo plazo** (12-24 meses): Estándar de facto para análisis regulatorio TELCO en Europa

**Diferenciación clave:**
- Primer análisis que REFUTA H2 (concentración) como causa de la tijera → implicaciones directas para el debate Fair Share
- Datos granulares CNMC (no solo Eurostat agregado)
- Stack moderno (Python + DuckDB + Streamlit) → Low TCO, fácil integración
- Código abierto → comunidad, transparencia, credibilidad académica

**Next action:** Elegir 3 quick wins y ejecutarlos este mes.
