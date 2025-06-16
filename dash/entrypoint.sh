#!/bin/bash
set -e

# Upgrade DB schema
superset db upgrade

# Create admin user
superset fab create-admin \
  --username "${ADMIN_USERNAME:-admin}" \
  --firstname "${ADMIN_FIRSTNAME:-Admin}" \
  --lastname "${ADMIN_LASTNAME:-User}" \
  --email "${ADMIN_EMAIL:-admin@example.com}" \
  --password "${ADMIN_PASSWORD:-Sup3rSet!42}" || true

# Initialize default roles, permissions, dashboards etc.
superset init

# Start the Superset server
exec /usr/bin/run-server.sh