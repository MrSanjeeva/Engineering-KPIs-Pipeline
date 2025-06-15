#!/usr/bin/env python
"""
build_kpis.py ── Load raw Parquet → observatory.duckdb, materialise KPI tables.

Tables created
  • cur_github   - raw GitHub PR data
  • cur_jira     - raw Jira Incident data
  • kpi_daily    - MTTR, deployment frequency, change-fail rate*
  • deploy_freq  - merged PRs per day
  • flaky_index  - toy flaky-test metric (placeholder)

Run after every ingest:
    python models/build_kpis.py
"""

import duckdb
import pathlib
import polars as pl
import datetime as dt

RAW_DIR = pathlib.Path("data/raw")
DB_PATH = pathlib.Path("data/observatory.duckdb")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

con = duckdb.connect(DB_PATH.as_posix())

# ---------- 1. Load / replace staging tables ----------
for f in RAW_DIR.glob("*.parquet"):
    tbl = f.stem.replace("github_events", "cur_github") \
                .replace("jira_issues",   "cur_jira")
    con.execute(
        f"CREATE OR REPLACE TABLE {tbl} AS SELECT * FROM read_parquet('{f}')")

# ---------- 2. Deployment frequency (merged PRs per day) ----------
con.execute("""
CREATE OR REPLACE TABLE deploy_freq AS
SELECT
  CAST(SUBSTR(created, 1, 10) AS DATE) AS day,
  COUNT(*) AS deploys
FROM cur_github
WHERE merged = TRUE
GROUP BY day
""")

# ---------- 3. Mean-time-to-recover (MTTR) ----------
con.execute("""
CREATE OR REPLACE TABLE kpi_daily AS
WITH incidents AS (
  SELECT
    CAST(SUBSTR(created ,1,10) AS DATE) AS start_day,
    CAST(SUBSTR(resolved,1,10) AS DATE) AS end_day,
    DATE_DIFF('second',
        CAST(created  AS TIMESTAMP),
        CAST(resolved AS TIMESTAMP)
    ) / 3600.0 AS ttr_hours
  FROM cur_jira
  WHERE resolved IS NOT NULL
)
SELECT
  end_day AS day,
  AVG(ttr_hours)          AS mttr_h,
  (SELECT COUNT(*) FROM deploy_freq WHERE day = end_day) AS deploys
FROM incidents
GROUP BY day
ORDER BY day;
""")

# ---------- 4. Flaky-test index (placeholder) ----------
con.execute("""
CREATE OR REPLACE TABLE flaky_index AS
SELECT day, RANDOM()*5  AS flaky_idx
FROM (SELECT DISTINCT day FROM kpi_daily)
""")

con.close()
print("Observatory.duckdb updated with KPI tables")
