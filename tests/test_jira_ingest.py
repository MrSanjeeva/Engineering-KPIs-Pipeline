import pathlib
import polars as pl


def test_jira_issues():
    f = pathlib.Path("data/raw/jira_issues.parquet")
    assert f.exists(), "run ingest/jira_pull.py first"
    df = pl.read_parquet(f)
    assert len(df) > 0
    assert {"key", "created", "resolved"}.issubset(df.columns)
