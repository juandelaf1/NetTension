# NetTension: Presentación 7 minutos (Storytelling)

## Estructura temporal

| Min | Sección | Qué dices | Qué muestras |
|-----|---------|-----------|--------------|
| 0:00-1:00 | Hook + Problema | El escenario | — |
| 1:00-2:30 | Metodología | El enfoque científico | Diagrama arquitectura |
| 2:30-4:30 | Resultados | Las 6 hipótesis | Dashboard en vivo |
| 4:30-6:00 | Fair Share | El simulador regulatorio | Dashboard What-If |
| 6:00-7:00 | Conclusión | Takeaway + preguntas | Footer slide |

---

## GUIÓN COMPLETO (ES con términos técnicos)

---

### 0:00 – 1:00 · HOOK + PROBLEMA

*(Pantalla: título "NetTension" + banner)*

**"Imagina que tu empresa vende un producto cuyo consumo crece 127% cada año.**
**Pero tus ingresos no solo no crecen: bajan 0.4% anual.**
**Eso es exactamente lo que ocurre en las telecos europeas desde hace 20 años."**

Ese fenómeno se llama **Scissors Effect** (efecto tijera): el tráfico de datos se dispara, los ingresos se estancan, y la brecha se abre cada trimestre. Esto no es un problema de una empresa o un país — es estructural, afecta a todo el sector, y está en el centro del debate regulatorio europeo sobre **Fair Share**: ¿deben Google, Netflix, Meta pagar por el uso que hacen de las redes?

**Nuestro proyecto, NetTension**, es un marco neutral de simulación de estrés de red. No especulamos: usamos datos reales del regulador español (CNMC) y de Eurostat para medir científicamente la tensión entre tráfico e ingresos. 41.937 filas de microdatos regulatorios, 1.8 millones de filas macroeconómicas, y 20 años de historia trimestral (2005-2025).

---

### 1:00 – 2:30 · METODOLOGÍA

*(Mostrar diagrama de arquitectura en README o slide)*

**"No inventamos datos. Todo es observado o estimado a partir de fuentes oficiales."**

Seguimos un **protocolo científico** con 3 pilares:

1. **DEC-006 (Zero Simulation)**: Cada variable traza a una fuente pública. Sin datos sintéticos.
2. **DEC-007 (Model Governance)**: Clasificamos cada variable en 4 capas:
   - `OBSERVED`: CNMC, Eurostat (datos directos)
   - `ESTIMATED`: HHI, CAGR, NSI (derivados)
   - `POLICY_MODEL`: Escenarios Fair Share
   - `CONSTANT`: Umbrales regulatorios (ej. HHI >2500 = concentrado)
3. **DEC-008 (Governance Metadata)**: Cada variable documentada con nivel de confianza, fecha de revisión, propietario, y referencia.

**Las 6 hipótesis que testeamos:**
- H1: Scissors Effect — el tráfico crece más que los ingresos
- H2: Market Concentration — el sector se concentra
- H3: Data Asymmetry — el ingreso por unidad colapsa
- H4: Network Stress — la presión por línea crece
- H5: Macro Decline — las telecos pesan menos en el PIB
- H6: Infrastructure Elasticity — los márgenes se comprimen

**Stack técnico:** Python ETL (pandas + DuckDB) → Parquet → Power BI (opcional) + Streamlit (dashboard interactivo). Datos en Kaggle para la comunidad.

---

### 2:30 – 4:30 · RESULTADOS

*(Abrir Streamlit dashboard: http://localhost:8501 o deploy)*

**"Vamos a los resultados. Y aquí viene lo interesante: 5 de 6 hipótesis se confirman, pero una se refuta — y esa refutación es el hallazgo más importante del proyecto."**

*(Navegar: Market Overview → Network Stress)*

**Página 1 – Market Overview (1 minuto):**
*(Mostrar gráfico de tijera con dos ejes)*
- Línea azul: tráfico de datos. Sube de 100 a 2.400 millones. **CAGR +127%**.
- Línea roja punteada: ingresos. Plana, incluso ligeramente decreciente. **CAGR −0.4%**.
- **Brecha: 127 puntos porcentuales.** Esto es la tijera. Insostenible sin nuevos modelos de ingresos.

Las tarjetas KPI arriba lo resumen: +127% tráfico, −0.4% ingresos, gap 127 pp, ARPU −83%.

**Página 2 – Network Stress (1 minuto):**
*(Mostrar HHI chart con bandas + scatter NSI vs ARPU)*
- **H2 refutada**: El HHI baja de 3.482 (altamente concentrado en 2005) a 2.368 (moderadamente concentrado en 2025). Cae −1.114 puntos.
- **¿Qué significa?** El sector NO se está concentrando. Hay más competencia. Y aún así la tijera empeora.
- **Conclusión clave**: El problema es **estructural**, no de monopolio. Ni la competencia ni la regulación antimonopolio resuelven la asimetría tráfico/ingreso.
- El scatter NSI vs ARPU muestra visualmente: el estrés de red crece exponencial (eje logarítmico), el ARPU colapsa.

**Gráfico animado**: Pulsa play — ves año a año cómo las burbujas (operadores) se desplazan a la derecha (más estrés) y abajo (menos ingresos).

---

### 4:30 – 6:00 · FAIR SHARE SIMULATOR

*(Navegar: Fair Share Simulator)*

**"Aquí pasamos del diagnóstico a la acción. ¿Qué pasaría si los OTT contribuyeran a los costes de red?"**

*(Mover sliders en vivo)*

**Escenario base**: Sin intervención, la brecha sigue abriéndose.

**Escenario con sliders:**
- **OTT Contribution 15%**: Cerramos ~19 pp de la brecha.
- **CAPEX Relief 20%**: Eficiencias en red compartida.
- **Ajuste tráfico**: Escenario optimista / pesimista.

Ejemplo real: Muevo OTT a 25%, CAPEX a 30% → cerramos ~35 pp de los 127. La brecha restante sigue siendo grande — esto demuestra que **Fair Share ayuda pero no resuelve todo**.

**El modelo está simplificado a propósito** (lineal, transparente). La vida real es más compleja — el informe BEREC 2025 cuestiona la premisa de free-riding — pero nuestro simulador permite al policy maker explorar escenarios sin caja negra.

---

### 6:00 – 7:00 · CONCLUSIÓN

**"Tres takeaways para el debate regulatorio:"**

1. **El problema es real y estructural.** 20 años de datos, 5 hipótesis confirmadas. La tijera tráfico/ingreso no es cíclica — es una tendencia de fondo.

2. **No es un problema de competencia.** H2 refutada: más competencia no resuelve la asimetría. El debate Fair Share no debe enmarcarse como "monopolio vs competencia", sino como **sostenibilidad del modelo de conectividad**.

3. **Los datos granulares importan.** Eurostat solo (macrodatos) NO captura la realidad que vemos en CNMC (microdatos). Las decisiones políticas basadas solo en estadísticas UE pueden subestimar el estrés en el sur de Europa.

**Próximos pasos:** Extender a otros países EU (Italia, Portugal, Grecia), incorporar CAPEX real por operador, y afinar el modelo Fair Share con elasticidades empíricas.

**"NetTension es código abierto, datos en Kaggle, dashboard interactivo. Todo reproducible, todo trazable. Porque el debate regulatorio necesita datos, no opiniones."**

**Preguntas.**

---

## SLIDES DE APOYO (opcional para la defensa)

### Slide 1: Portada
```
NetTension — Network Stress Simulation Framework
Juan de la Fuente · ThePower Business School · Jun 2026
```

### Slide 2: El problema
```
Tráfico: +127%/año  →  Ingresos: −0.4%/año  →  Gap: 127 pp
¿Deben Google/Netflix/Meta pagar por el uso de la red?
```

### Slide 3: Metodología
```
Fuentes: CNMC (41.937 rows) + Eurostat (3M rows)
Clasificación: OBSERVED / ESTIMATED / POLICY_MODEL / CONSTANT
6 hipótesis científicas
```

### Slide 4: Resultados
```
H1  Scissors Effect  →  CONFIRMED  (tráfico +127%, ingresos −0.4%)
H2  Concentration    →  REFUTED    (HHI 3.482 → 2.368, más competencia)
H3  Data Asymmetry   →  CONFIRMED  (ingreso/unidad colapsa)
H4  Network Stress   →  CONFIRMED  (NSI exponencial, ARPU cae)
H5  Macro Decline    →  CONFIRMED  (telecom/GDP: 3.2% → 2.0%)
H6  Elasticity       →  CONFIRMED  (márgenes comprimidos)
```

### Slide 5: Conclusión
```
1. Problema estructural, no cíclico
2. Competencia no lo resuelve → Fair Share es legítimo
3. Microdatos importan (CNMC > Eurostat solo)
```

### Slide 6: Dashboard QR
```
Código QR → https://nettension.streamlit.app
```

---

## CHECKLIST PRE-PRESENTACIÓN

- [ ] Streamlit corriendo local (`streamlit run streamlit_app/app.py`)
- [ ] O alternativo: deploy en Streamlit Cloud abierto en Chrome
- [ ] Power BI .pbip en carpeta por si preguntan
- [ ] Kaggle dataset abierto: kaggle.com/juandelaf/nettension
- [ ] GitHub repo abierto: github.com/juandelaf1/NetTension
- [ ] Cronómetro visible (7 min)
- [ ] Sliders Fair Share en posición NEUTRAL (15%, 20%, 0%)
- [ ] Animación NSI lista para play
- [ ] QR del dashboard en última slide para quien quiera explorar

---

## POSIBLES PREGUNTAS Y RESPUESTAS

**¿Por qué España y no toda Europa?**
Porque la CNMC ofrece datos más granulares que otras NRAs. España como caso de estudio dentro del marco regulatorio EU. Siguiente fase: extender a Italia, Portugal, Grecia.

**¿Fair Share es viable legalmente?**
BEREC 2025 cuestiona el free-riding, pero la Net Neutrality regulación EU permite mecanismos de contribución si son transparentes y no discriminatorios.

**¿Qué pasa con 5G?**
El capex 5G está incluido en los datos CNMC. El estrés es mayor porque 5G requiere más inversión para el mismo ingreso por usuario.

**¿Streamlit por qué y no Power BI?**
Ambos. Power BI para la entrega del módulo (obligatorio), Streamlit para portfolio público y reproducibilidad (código abierto, versionable).

**¿Los datos están actualizados?**
CNMC 2005T1-2025T4. Eurostat hasta 2025. Última revisión: Junio 2026.
