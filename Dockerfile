FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY data/SOURCES.yaml data/
COPY pyproject.toml .

RUN python -c "from transform.kpi_engine import *; print('KPI Engine OK')"

CMD ["python", "-m", "pipeline.etl_pipeline"]
