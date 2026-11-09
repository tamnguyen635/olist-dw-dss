"""
Run every query in src/sql/02_olap_queries.sql against the DW and print the result.

    python src/olap/olap_demo.py [--db data/processed/olist_dw.db]
"""
import argparse
import re
import sqlite3
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[2]


def load_queries(path: Path) -> dict:
    """Split the SQL file into {name: sql} using the '-- name:' markers."""
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"^-- name:\s*(\w+)\s*$", text, flags=re.M)
    return {parts[i]: parts[i + 1].strip() for i in range(1, len(parts), 2)}


def run(db: Path, sql_file: Path) -> dict:
    con = sqlite3.connect(db)
    results = {}
    for name, sql in load_queries(sql_file).items():
        results[name] = pd.read_sql_query(sql, con)
    con.close()
    return results


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", type=Path, default=REPO / "data" / "processed" / "olist_dw.db")
    ap.add_argument("--sql", type=Path, default=REPO / "src" / "sql" / "02_olap_queries.sql")
    a = ap.parse_args()
    pd.set_option("display.width", 140)
    for name, df in run(a.db, a.sql).items():
        print(f"\n=== {name} ===")
        print(df.to_string(index=False))
