#!/usr/bin/env python
"""
jira_pull.py ── Fetch last 90-day Jira issues (Incidents) and save to Parquet.

Prereqs
  • Env vars JIRA_EMAIL and JIRA_TOKEN
  • Env var JIRA_BASE = https://<your-site>.atlassian.net
Run locally
  export JIRA_EMAIL=you@example.com
  export JIRA_TOKEN=ATATYOuRT0K3N
  export JIRA_BASE=https://eng-kpis.atlassian.net
  python ingest/jira_pull.py
"""

import os
import pathlib
import datetime as dt
import requests
import polars as pl

BASE = os.getenv("JIRA_BASE")
EMAIL = os.getenv("JIRA_EMAIL")
TOKEN = os.getenv("JIRA_TOKEN")
assert BASE and EMAIL and TOKEN, "Set JIRA_BASE, JIRA_EMAIL, JIRA_TOKEN env vars"

HEAD = {"Accept": "application/json"}
AUTH = (EMAIL, TOKEN)
PROJECT = "EKP"
JQL = f'project = {PROJECT} AND issuetype = Incident ORDER BY created DESC'
SINCE = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=90)).date()

issues = []
start = 0
while True:
    params = {"jql": JQL, "startAt": start, "maxResults": 100}
    r = requests.get(f"{BASE}/rest/api/3/search", headers=HEAD,
                     params=params, auth=AUTH, timeout=30)
    r.raise_for_status()
    data = r.json()
    for itm in data["issues"]:
        # e.g. 2025-06-15T18:57:08.130+0100
        ts_created = itm["fields"]["created"]
        created_dt = dt.datetime.strptime(ts_created, "%Y-%m-%dT%H:%M:%S.%f%z")
        created = created_dt.date()
        if created < SINCE:
            break
        issues.append(
            {
                "key":      itm["key"],
                "summary":  itm["fields"]["summary"],
                "created":  itm["fields"]["created"],
                "resolved": itm["fields"].get("resolutiondate"),
                "priority": itm["fields"]["priority"]["name"] if itm["fields"]["priority"] else None,
            }
        )
    if start + 100 >= data["total"]:
        break
    start += 100

out = pathlib.Path("data/raw/jira_issues.parquet")
out.parent.mkdir(parents=True, exist_ok=True)
pl.DataFrame(issues).write_parquet(out)
print(f"Saved {len(issues)} rows → {out}")
