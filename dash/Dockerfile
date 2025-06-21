# Start from Superset official image (ARM-aware)
FROM apache/superset:3.0.0

USER root
# Install the DuckDB SQLAlchemy dialect + engine binary
RUN pip install --no-cache-dir duckdb-engine==0.10.0 duckdb==1.3.0
USER superset

# finalize
COPY data/observatory.duckdb /app/observatory.duckdb

COPY dash/superset_config.py /app/pythonpath/superset_config.py

# Superset initialization
RUN superset fab create-admin \
    --username ${ADMIN_USERNAME} \
    --firstname ${ADMIN_FIRSTNAME} \
    --lastname ${ADMIN_LASTNAME} \
    --email ${ADMIN_EMAIL} \
    --password ${ADMIN_PASSWORD} || true

RUN superset db upgrade && \
    superset init

# Import dashboards
COPY superset/superset_bundle.zip /app/
RUN superset import-dashboards --path /app/superset_bundle.zip || echo "Import failed"
