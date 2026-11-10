# Visualizaciones y resultados (registro)

NetTension ya dispone de plataforma de visualización: **Streamlit** (`streamlit_app/`). Este directorio registra evidencias **trazables y reproducibles** de vistas y resultados (sin duplicar la app).

## Estructura sugerida
- `docs/visualizations/` — capturas representativas de vistas clave (PNG/WebP optimizados), 1 por resultado/hipótesis relevante.
- `reports/results/` — salidas tabulares de KPIs/consultas SQL (`sql/*.sql`) exportadas desde DuckDB.
- `reports/visualizations/kpi/` — figuras estáticas de KPIs cuando aporten valor (opcional).
- `reports/quality/` — reporte de calidad de datos (`data_quality_report.json|md`).

## Metadatos mínimos por artefacto
- Fecha y commit/tag
- Fuente de datos (parquet/DuckDB, período)
- Página/hipótesis/KPI que ilustra
- Comando de regeneración

## Cómo regenerar (referencia)
1. `python -m src.pipeline.etl_pipeline` — genera parquets procesados (+ reporte de calidad si aplica).
2. `python -m src.pipeline.export_duckdb` — crea `data/processed/net_tension.duckdb` y ejecuta consultas versionadas en `sql/`.
3. `streamlit run streamlit_app/app.py` — visualización interactiva; capturar vistas clave con viewport/tema consistente.

> Registrar solo visualizaciones que evidencien resultados/hipótesis o cambios concretos. No incluir binarios pesados innecesarios ni datos sensibles.
