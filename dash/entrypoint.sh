#!/bin/bash
set -e

# Copy DuckDB to writable tmp (optional)
cp -f /app/observatory.duckdb /tmp/observatory.duckdb || true
chmod 664 /tmp/observatory.duckdb || true

# Upgrade metadata DB
/usr/local/bin/superset db upgrade

# Create admin (idempotent)
/usr/local/bin/superset fab create-admin \
  --username "${ADMIN_USERNAME}" \
  --firstname "${ADMIN_FIRSTNAME}" \
  --lastname  "${ADMIN_LASTNAME}" \
  --email     "${ADMIN_EMAIL}" \
  --password  "${ADMIN_PASSWORD}" || true

# Init roles/permissions
/usr/local/bin/superset init

# Import dashboards (idempotent)
if [ -f /app/superset_bundle.zip ]; then
  /usr/local/bin/superset import-dashboards \
    --path /app/superset_bundle.zip \
    --username "${ADMIN_USERNAME}" || true
fi

exec /usr/bin/run-server.sh