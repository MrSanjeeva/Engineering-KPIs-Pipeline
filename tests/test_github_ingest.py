import pathlib
import polars as pl


def test_github_events():
    f = pathlib.Path("data/raw/github_events.parquet")
    assert f.exists(), "run ingest/github_pull.py first"
    df = pl.read_parquet(f)
    assert len(df) > 0
    assert {"id", "state", "merged"}.issubset(df.columns)
