FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

COPY src/ src/
COPY data/SOURCES.yaml data/
COPY pyproject.toml .

RUN python -m pipeline.export_powerbi
RUN python -m pipeline.export_duckdb

CMD ["python", "-m", "pipeline.etl_pipeline"]
