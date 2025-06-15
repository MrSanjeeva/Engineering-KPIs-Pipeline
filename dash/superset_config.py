import os
from datetime import timedelta

ROW_LIMIT = 5000               # default chart limit
SQLLAB_CTAS_SCHEMA = ""

# Make DuckDB discoverable by SQLAlchemy-driver string
# SQLALCHEMY_DATABASE_URI = "duckdb:////app/observatory.duckdb"

# Shorten default login session so the free container logs out quickly
SESSION_COOKIE_SAMESITE = "Lax"
PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
