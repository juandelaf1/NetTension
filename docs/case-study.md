# NetTension — Technical Case Study

## Problem
Telecom markets show tension between sustained traffic growth and pressure on revenues/margins. The goal of this project is to analyze that dynamic in a **traceable, reproducible** way using public data, testing predefined hypotheses rather than presenting ad-hoc claims.

## Decisions
- **Public, attributable data:** use CNMC (and selected Eurostat) sources with explicit provenance (`data/SOURCES.yaml`, pipeline outputs).
- **Reproducible pipeline:** ETL in Python/Pandas producing processed datasets and a DuckDB artifact for analysis.
- **Auditable logic:** version SQL queries in `sql/` for KPI/validation outputs instead of embedding all logic as opaque steps.
- **Quality gates on processed data:** run data-quality checks (`src/quality/data_quality.py`) and persist reports in `reports/quality/`.
- **Inspectable presentation:** expose results through exported tables (`reports/results/`) and a Streamlit app (`streamlit_app/`) with a visualization evidence registry (`docs/visualizations/`).

## Trade-offs
- **Scope vs fidelity:** focus on available public (primarily CNMC/Spain) data; broader EU modeling or causal attribution is limited by data coverage.
- **Illustrative scenarios vs prediction:** outputs support structured analysis and communication, but are **not** predictive forecasts of market outcomes.
- **Simplicity vs full platformization:** prioritize reproducible artifacts and clarity over a complex production orchestration stack.

## Evidence
- **Versioned SQL & results:** `sql/` and exported outputs in `reports/results/` (generated via `python -m src.pipeline.export_duckdb`).
- **Data quality:** `reports/quality/data_quality_report.json|md` (e.g. checks passing on processed outputs at time of generation).
- **Automated checks:** unit tests (e.g. KPI engine) and CI workflow (`.github/workflows/ci.yml`).
- **Visualization:** Streamlit app and capture guidance/log in `docs/visualizations/` (manual, reproducible captures when added).

## Limits & learnings
- **Limits:** illustrative/non-predictive framing; dependent on source definitions and completeness; excludes regulatory/merger/competitive actions not represented in data.
- **Learnings:** making hypotheses, SQL, quality checks, and result artifacts explicit improves trust and reviewability; separating reproducible evidence from narrative reduces ambiguity for portfolio readers.
