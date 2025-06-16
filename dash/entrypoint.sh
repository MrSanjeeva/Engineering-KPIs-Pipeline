#!/bin/bash
set -e

superset fab create-admin \
  --username "${ADMIN_USERNAME:-admin}" \
  --firstname "${ADMIN_FIRSTNAME:-Admin}" \
  --lastname "${ADMIN_LASTNAME:-User}" \
  --email "${ADMIN_EMAIL:-admin@example.com}" \
  --password "${ADMIN_PASSWORD:-Sup3rSet!42}" || true

# Run Superset
exec /usr/bin/run-server.sh