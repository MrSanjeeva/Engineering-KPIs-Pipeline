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

# ------------------------------------------------------------------
# Ensure Viewer (read‑only) user exists and has the Viewer role
# ------------------------------------------------------------------
/usr/local/bin/superset fab create-user \
  --username  "${VIEWER_USERNAME:=viewer}" \
  --firstname "${VIEWER_FIRSTNAME:=Read}" \
  --lastname  "${VIEWER_LASTNAME:=Only}" \
  --email     "${VIEWER_EMAIL:=viewer@example.com}" \
  --password  "${VIEWER_PASSWORD:=changeme123}" || true

# Grant the Viewer role if not already assigned
python - <<'PY'
import os
from superset import security_manager, db

viewer_name = os.environ.get("VIEWER_USERNAME", "viewer")
viewer_role = security_manager.find_role("Viewer")
user = security_manager.find_user(username=viewer_name)

if viewer_role and user and viewer_role not in user.roles:
    user.roles.append(viewer_role)
    db.session.commit()
PY

# Import dashboards (idempotent)
if [ -f /app/superset_bundle.zip ]; then
  /usr/local/bin/superset import-dashboards \
    --path /app/superset_bundle.zip \
    --username "${ADMIN_USERNAME}" || true
fi

exec /usr/bin/run-server.sh