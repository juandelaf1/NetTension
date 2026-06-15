FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

# Prod dependencies
COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

# Test dependencies
COPY requirements-test.txt .
RUN pip install --no-cache-dir -r requirements-test.txt

# Source code
COPY src/ src/
COPY tests/ tests/

# Config
COPY data/SOURCES.yaml data/
COPY pyproject.toml .

# Validate: run unit tests (doesn't need raw data)
RUN python -m pytest tests/ -v --no-header -q

CMD ["python", "-m", "pipeline.etl_pipeline"]
