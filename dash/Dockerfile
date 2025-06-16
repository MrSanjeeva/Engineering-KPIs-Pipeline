# Start from Superset official image (ARM-aware)
FROM apache/superset:3.0.0

USER root
# Install the DuckDB SQLAlchemy dialect + engine binary
RUN pip install --no-cache-dir duckdb-engine==0.10.0 duckdb==1.3.0
USER superset

# Create the admin user at build time so we never rely on first-boot env vars
RUN superset fab create-admin \
    --username ${ADMIN_USERNAME:-admin} \
    --firstname ${ADMIN_FIRSTNAME:-Admin} \
    --lastname ${ADMIN_LASTNAME:-User} \
    --email ${ADMIN_EMAIL:-admin@example.com} \
    --password ${ADMIN_PASSWORD:-Sup3rSet!42} || true

# finalize
CMD ["/usr/bin/run-server.sh"]