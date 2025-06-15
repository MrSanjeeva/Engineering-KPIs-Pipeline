import polars as pl
import requests
import datetime as dt
import pathlib
import os
TOKEN = os.getenv("GH_PAT")

#!/usr/bin/env python
"""
github_pull.py ── Fetch last 90‑day PR metadata & save to Parquet.

Usage:
    # Locally
    export GH_PAT=ghp_xxxxxx
    export GITHUB_REPO="MrSanjeeva/engineering-kpis-pipeline"   # optional
    python ingest/github_pull.py
"""


TOKEN = os.getenv("GH_PAT")
assert TOKEN, "Set env var GH_PAT with your GitHub Personal Access Token"

# ← adjust default
REPO = os.getenv("GITHUB_REPO", "MrSanjeeva/engineering-kpis-pipeline")
SINCE = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=90)).isoformat()
HEAD = {"Authorization": f"token {TOKEN}"}

items: list[dict] = []
url = (
    f"https://api.github.com/repos/{REPO}/pulls"
    f"?state=all&per_page=100&sort=created&direction=desc"
)

while url and len(items) < 1000:  # hard‑limit for demo
    r = requests.get(url, headers=HEAD, timeout=20)
    r.raise_for_status()
    data = r.json()
    for pr in data:
        if pr["created_at"] < SINCE:
            url = None
            break
        items.append(
            {
                "id": pr["number"],
                "state": pr["state"],
                "merged": pr["merged_at"] is not None,
                "created": pr["created_at"],
                "closed": pr["closed_at"],
            }
        )
    url = r.links.get("next", {}).get("url")

out = pathlib.Path("data/raw/github_events.parquet")
out.parent.mkdir(parents=True, exist_ok=True)
pl.DataFrame(items).write_parquet(out)
print(f"Saved {len(items)} rows → {out}")
