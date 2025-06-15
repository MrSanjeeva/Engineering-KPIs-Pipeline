# Start from Superset official image (ARM-aware)
FROM apache/superset:3.0.0

USER root
# Install the DuckDB SQLAlchemy dialect + engine binary
RUN pip install --no-cache-dir duckdb-engine==0.10.0 duckdb==1.3.0
USER superset