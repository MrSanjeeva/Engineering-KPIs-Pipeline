# Engineering KPIs Pipeline

[![CI](https://github.com/MrSanjeeva/Engineering-KPIs-Pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/MrSanjeeva/Engineering-KPIs-Pipeline/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](LICENSE)

<!-- Add this when the dashboard is live:
[![Superset](https://img.shields.io/badge/Live%20Dashboard-eng--kpis.onrender.com-orange)](https://eng-kpis.onrender.com)
-->

**Purpose —** Daily-refreshed pipeline that ingests GitHub & Jira activity, stores it in a DuckDB lake, derives DORA+quality KPIs (MTTR, deployment frequency, change-failure rate, flaky-test index), and surfaces them in an Apache Superset dashboard.

---

## Features

- GitHub REST/GraphQL (PRs & builds) – 90‑day look‑back
- Jira Cloud incidents
- **Lake & Modeling**
  - DuckDB single-file database (`data/observatory.duckdb`)
  - Polars/SQL models create KPI tables
- **KPI Suite**
  - Mean Time to Recover (MTTR)
  - Deployment frequency
  - Change-failure rate
  - Flaky-test index
- **Dashboard (Superset)**
  - MTTR trend, deploy-freq bar, flaky heatmap, team radar _(to be deployed)_
  - Public URL on Render free tier
- **CI / Data refresh**
  - GitHub Actions: unit tests on every push
  - Scheduled 06:05 UTC job regenerates data & KPIs

---

## Quick Start (local)

```bash
git clone https://github.com/MrSanjeeva/Engineering-KPIs-Pipeline.git
cd Engineering-KPIs-Pipeline
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 1 · Auth tokens (set once per shell)
export GH_PAT=xxxxxxxxxxxxxxxxxxxxxxxxxxxx          # GitHub Personal Access Token
export JIRA_BASE=https://<your-site>.atlassian.net   # Jira cloud site
export JIRA_EMAIL=you@example.com                   # Atlassian account email
export JIRA_TOKEN=ATATyourToken12345                # Jira API token

# 2 · Ingest data (90‑day look‑back)
python ingest/github_pull.py
python ingest/jira_pull.py          # optional—skips if creds not set

# 3 · Build DuckDB lake & KPIs
python models/build_kpis.py

# 4 · Explore
duckdb data/observatory.duckdb      # open interactive SQL shell
```

## Live Demo

_Coming soon — Superset dashboard will be hosted at_

`https://eng-kpis.onrender.com`

## Architecture

_Data lineage from API to dashboard_

```mermaid
graph LR
    GH[GitHub API] --> ING[Ingest jobs]
    JI[Jira API]  --> ING
    ING --> DUCK[(observatory.duckdb)]
    DUCK --> KPI[KPI tables]
    KPI --> BI[Superset Dashboard]
```

## Roadmap

- [x] GitHub ingest with unit test
- [x] Jira ingest with unit test
- [ ] KPI models in DuckDB (`kpi_daily`, `deploy_freq`, `flaky_index`)
- [ ] Superset Docker compose & local dashboard
- [ ] Render deploy + README badge
- [ ] Automated daily data refresh

## License

This project is licensed under the MIT License
