# Capture Log — NetTension (Streamlit)

Bitácora de evidencias visuales reproducibles. Añadir una entrada por captura incorporada en `docs/visualizations/captures/`.

> No registrar capturas inventadas. Completar fecha, commit y configuración reales al capturar.

## Entradas

<!-- Copiar la plantilla de abajo por cada captura -->

### NN Título corto
- **Archivo:** `docs/visualizations/captures/<nombre>.png`
- **Fecha:** YYYY-MM-DD
- **Commit:** `<hash>`
- **Página/vista:** `<views/...py>` — descripción breve
- **Hipótesis/KPI:** H# / KPI / resultado que evidencia
- **Fuente de datos:** `data/processed/*.parquet` o `data/processed/net_tension.duckdb` (período/corte: ...)
- **Config:** idioma=es|en, viewport=WxH, tema=dark|light, zoom=100%
- **Regeneración:** `python -m src.pipeline.etl_pipeline && python -m src.pipeline.export_duckdb && streamlit run streamlit_app/app.py`
- **Notas:** filtros, estado, o “escenario ilustrativo/no predictivo” si aplica
