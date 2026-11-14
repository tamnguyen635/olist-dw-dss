"""Shared fixtures.

Two kinds of data are used by the test-suite:

* a tiny hand-made Olist-shaped dataset (``mini_raw`` / ``mini_tables`` / ``mini_db``)
  where every expected value is worked out by hand -> unit tests of the ETL rules;
* the real warehouse ``data/processed/olist_dw.db`` (``dw``) -> integrity,
  reconciliation, OLAP and application tests.
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pandas as pd
import pytest

REPO = Path(__file__).resolve().parents[1]
for sub in ("etl", "app", "dss", "olap"):
    sys.path.insert(0, str(REPO / "src" / sub))

DB = REPO / "data" / "processed" / "olist_dw.db"
RAW = REPO / "data" / "raw"
SCHEMA = REPO / "src" / "sql" / "01_schema.sql"

needs_dw = pytest.mark.skipif(not DB.exists(), reason="run `python src/etl/run_etl.py` first")
needs_raw = pytest.mark.skipif(
    not (RAW / "olist_order_items_dataset.csv").exists(), reason="raw CSVs not in data/raw")


@pytest.fixture(scope="session")
def dw():
    if not DB.exists():
        pytest.skip("warehouse not built")
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    yield con
    con.close()


# ------------------------------------------------------------------ mini data
def _write(path: Path, rows: list[dict]) -> None:
    pd.DataFrame(rows).to_csv(path, index=False)


@pytest.fixture(scope="session")
def mini_raw(tmp_path_factory) -> Path:
    """Scenario (all values hand-checked in tests/test_etl_unit.py):

    person u1 has two customer_ids (c1 in SP for o1, c2 in RJ for o2) -> 1 customer row, latest city = RJ
    o1  delivered, 2 items (100+10, 50+5), pays credit_card 30 + voucher 135 -> main = voucher,
        reviews 5 and 3 -> 4.0, delivered 10.5 days after purchase, 4.5 days early
    o2  delivered 5 days late, product without category, boleto 40, no review
    o3  canceled (person u2), 1 item, credit_card 20 in 3 installments, review 1
    o4  has no items at all -> must be dropped
    """
    d = tmp_path_factory.mktemp("raw")
    _write(d / "olist_customers_dataset.csv", [
        dict(customer_id="c1", customer_unique_id="u1", customer_zip_code_prefix="01001", customer_city="sao paulo", customer_state="SP"),
        dict(customer_id="c2", customer_unique_id="u1", customer_zip_code_prefix="20000", customer_city="rio", customer_state="RJ"),
        dict(customer_id="c3", customer_unique_id="u2", customer_zip_code_prefix="30000", customer_city="bh", customer_state="MG"),
        dict(customer_id="c4", customer_unique_id="u3", customer_zip_code_prefix="40000", customer_city="salvador", customer_state="BA"),
    ])
    _write(d / "olist_orders_dataset.csv", [
        dict(order_id="o1", customer_id="c1", order_status="delivered", order_purchase_timestamp="2017-01-10 00:00:00",
             order_delivered_customer_date="2017-01-20 12:00:00", order_estimated_delivery_date="2017-01-25 00:00:00"),
        dict(order_id="o2", customer_id="c2", order_status="delivered", order_purchase_timestamp="2017-03-05 00:00:00",
             order_delivered_customer_date="2017-03-20 00:00:00", order_estimated_delivery_date="2017-03-15 00:00:00"),
        dict(order_id="o3", customer_id="c3", order_status="canceled", order_purchase_timestamp="2017-03-06 10:00:00",
             order_delivered_customer_date=None, order_estimated_delivery_date="2017-03-30 00:00:00"),
        dict(order_id="o4", customer_id="c4", order_status="processing", order_purchase_timestamp="2017-03-07 10:00:00",
             order_delivered_customer_date=None, order_estimated_delivery_date="2017-03-31 00:00:00"),
    ])
    _write(d / "olist_order_items_dataset.csv", [
        dict(order_id="o1", order_item_id=1, product_id="p1", seller_id="s1", price=100.0, freight_value=10.0),
        dict(order_id="o1", order_item_id=2, product_id="p2", seller_id="s1", price=50.0, freight_value=5.0),
        dict(order_id="o2", order_item_id=1, product_id="p3", seller_id="s2", price=40.0, freight_value=0.0),
        dict(order_id="o3", order_item_id=1, product_id="p1", seller_id="s2", price=20.0, freight_value=0.0),
    ])
    _write(d / "olist_order_payments_dataset.csv", [
        dict(order_id="o1", payment_sequential=1, payment_type="credit_card", payment_installments=1, payment_value=30.0),
        dict(order_id="o1", payment_sequential=2, payment_type="voucher", payment_installments=1, payment_value=135.0),
        dict(order_id="o2", payment_sequential=1, payment_type="boleto", payment_installments=1, payment_value=40.0),
        dict(order_id="o3", payment_sequential=1, payment_type="credit_card", payment_installments=3, payment_value=20.0),
    ])
    _write(d / "olist_order_reviews_dataset.csv", [
        dict(review_id="r1", order_id="o1", review_score=5),
        dict(review_id="r2", order_id="o1", review_score=3),
        dict(review_id="r3", order_id="o3", review_score=1),
    ])
    _write(d / "olist_products_dataset.csv", [
        dict(product_id="p1", product_category_name="cama_mesa_banho", product_name_lenght=10, product_description_lenght=100,
             product_photos_qty=1, product_weight_g=500, product_length_cm=10, product_height_cm=10, product_width_cm=10),
        dict(product_id="p2", product_category_name="pc_gamer", product_name_lenght=10, product_description_lenght=100,
             product_photos_qty=1, product_weight_g=500, product_length_cm=10, product_height_cm=10, product_width_cm=10),
        dict(product_id="p3", product_category_name=None, product_name_lenght=None, product_description_lenght=None,
             product_photos_qty=None, product_weight_g=None, product_length_cm=None, product_height_cm=None, product_width_cm=None),
    ])
    _write(d / "olist_sellers_dataset.csv", [
        dict(seller_id="s1", seller_zip_code_prefix="01310", seller_city="sao paulo", seller_state="SP"),
        dict(seller_id="s2", seller_zip_code_prefix="22000", seller_city="rio", seller_state="RJ"),
    ])
    _write(d / "product_category_name_translation.csv", [
        dict(product_category_name="cama_mesa_banho", product_category_name_english="bed_bath_table"),
    ])
    return d


@pytest.fixture(scope="session")
def mini_tables(mini_raw):
    import run_etl
    return run_etl.transform(run_etl.extract(mini_raw))


@pytest.fixture(scope="session")
def mini_db(mini_tables, tmp_path_factory):
    """Mini warehouse. Quality checks intentionally fail (expect 112,650 rows) -> swallow that."""
    import run_etl
    db = tmp_path_factory.mktemp("db") / "mini.db"
    try:
        run_etl.load(mini_tables, db, SCHEMA)
    except SystemExit:
        pass
    con = sqlite3.connect(db)
    yield con
    con.close()
