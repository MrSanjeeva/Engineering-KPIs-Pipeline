import duckdb
import pathlib


def test_kpi_tables():
    db = duckdb.connect("data/observatory.duckdb")
    assert db.execute("SELECT COUNT(*) FROM kpi_daily").fetchone()[0] >= 1
    assert db.execute(
        "PRAGMA table_info(deploy_freq)").fetchall(), "deploy_freq missing"
    db.close()
