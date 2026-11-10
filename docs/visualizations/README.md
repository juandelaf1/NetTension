# Visualizaciones y resultados (registro)

NetTension ya dispone de plataforma de visualización: **Streamlit** (`streamlit_app/`). Este directorio registra **evidencias trazables y reproducibles** de vistas y resultados clave (sin duplicar la app ni inventar capturas).

> **Estado:** registro preparado. Las capturas manuales de la app se incorporan aquí cuando se generen de forma reproducible (ver checklist).

## Estructura

- `docs/visualizations/captures/` — capturas representativas (PNG/WebP optimizados), una por vista/resultado relevante.
- `docs/visualizations/CAPTURE_LOG.md` — bitácora de capturas (metadatos mínimos por artefacto).
- `reports/results/` — salidas tabulares de KPIs/consultas SQL versionadas (`sql/*.sql`) exportadas desde DuckDB.
- `reports/quality/` — reportes de calidad de datos (`data_quality_report.json|md`).

## Reproducibilidad (paso a paso)

1. **Datos procesados (ETL):**
   ```bash
   python -m src.pipeline.etl_pipeline
   ```
   Genera/actualiza salidas procesadas y, si aplica, reporte de calidad.
2. **Exportación DuckDB + resultados SQL:**
   ```bash
   python -m src.pipeline.export_duckdb
   ```
   Crea/actualiza `data/processed/net_tension.duckdb` y exporta resultados de consultas en `sql/` (p. ej. a `reports/results/` según pipeline).
3. **Calidad de datos (opcional, explícito):**
   ```bash
   python -m src.quality.data_quality
   ```
4. **App interactiva (capturas):**
   ```bash
   streamlit run streamlit_app/app.py
   ```
   Navega a las vistas clave y captura con configuración consistente (ver checklist).

## Checklist de capturas manuales (reproducibles)

### Configuración recomendada
- **Navegador:** Chromium/Chrome o Edge, ventana limpia (sin extensiones que alteren UI), zoom 100%.
- **Viewport sugerido:** `1440×900` (desktop) o `1280×720` para consistencia; opcional adicional móvil `390×844` si aporta.
- **Tema/idioma:** registrar (p. ej. tema oscuro según `streamlit_app/.streamlit/config.toml`, idioma ES/EN).
- **Estado de datos:** indicar commit/tag y si se usaron outputs regenerados (`etl_pipeline` + `export_duckdb`) o snapshot existente.
- **Formato:** PNG (preferido) o WebP, optimizado; evitar archivos pesados innecesarios.

### Vistas clave sugeridas (Streamlit)
Capturar solo lo que evidencie resultados/hipótesis o funcionamiento relevante:

| ID | Página (código) | Vista sugerida | Evidencia/relación |
|---|---|---|---|
| `01` | `views/market_overview.py` | Visión de mercado / KPIs principales (Scissors Effect) | H1 / resumen ejecutivo |
| `02` | `views/network_stress.py` | Estrés de red (NSI, concentración/elasticidad según vista) | H2/H4/H6 |
| `03` | `views/european_context.py` | Contexto europeo/comparativo | H5 / contexto macro |
| `04` | `views/fair_share.py` | Simulador Fair Share (escenario base o ilustrativo) | Modelo/escenario (no predictivo) |
| `05` | `views/evolution_strategy.py` | Evolución y estrategia (tendencias) | Soporte a hipótesis/resultados |
| `06` | `views/about.py` *(opcional)* | Metodología/fuentes/limitaciones en app | Trazabilidad y alcance |

> Ajusta la selección si alguna vista no está disponible con los datos locales; registra el motivo en `CAPTURE_LOG.md`.

### Convención de nombres
Guardar en `docs/visualizations/captures/`:
- `NN_<page>_<kpi-o-vista>_<lang>_<viewport>.png`
  - Ej.: `01_market-overview_scissors-effect_es_1440x900.png`

## Metadatos mínimos por artefacto
Registrar en [`CAPTURE_LOG.md`](CAPTURE_LOG.md) para cada captura:

- **Archivo:** ruta relativa
- **Fecha:** YYYY-MM-DD
- **Commit/tag:** hash o tag del repo
- **Página/vista e hipótesis/KPI:** qué ilustra
- **Fuente de datos:** parquet/DuckDB y período/corte si aplica
- **Idioma, viewport, tema:** configuración de captura
- **Comando(s) de regeneración:** ETL/export/app
- **Notas:** filtros aplicados, limitaciones o si es escenario ilustrativo

## Plantilla rápida (entrada de bitácora)

```md
### <NN> <título corto>
- Archivo: `docs/visualizations/captures/<nombre>.png`
- Fecha: YYYY-MM-DD
- Commit: `<hash>`
- Página/vista: `<page>` — <descripción>
- Hipótesis/KPI: <H# / KPI>
- Fuente de datos: `data/processed/*.parquet` / `data/processed/net_tension.duckdb` (período: ...)
- Config: idioma=<es|en>, viewport=<WxH>, tema=<dark|light>
- Regeneración: `python -m src.pipeline.etl_pipeline && python -m src.pipeline.export_duckdb && streamlit run streamlit_app/app.py`
- Notas: <filtros/escenario/limitaciones>
```

## Buenas prácticas
- Registrar solo visualizaciones que evidencien resultados/hipótesis o cambios concretos.
- No incluir datos sensibles ni binarios innecesarios; preferir pocas capturas representativas y optimizadas.
- Si el contenido es un **escenario/modelo** (p. ej. Fair Share), etiquetarlo explícitamente como ilustrativo/no predictivo.
