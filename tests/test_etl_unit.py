"""Unit tests of the ETL rules on a tiny hand-made dataset (see conftest.mini_raw)."""
from __future__ import annotations

import pytest

import run_etl


def fact(mini_tables, order_id, item=1):
    f = mini_tables["fact_sales"]
    return f[(f.order_id == order_id) & (f.order_item_id == item)].iloc[0]


# ------------------------------------------------------------- extract
def test_extract_reports_missing_files(tmp_path):
    with pytest.raises(SystemExit) as e:
        run_etl.extract(tmp_path)
    assert "olist_orders_dataset.csv" in str(e.value)


def test_extract_keeps_zip_code_leading_zero(mini_raw):
    data = run_etl.extract(mini_raw)
    assert data["customers"].customer_zip_code_prefix.iloc[0] == "01001"


# ------------------------------------------------------------- grain / filtering
def test_fact_grain_is_one_row_per_order_item(mini_tables):
    f = mini_tables["fact_sales"]
    assert len(f) == 4
    assert not f.duplicated(["order_id", "order_item_id"]).any()


def test_orders_without_items_are_dropped(mini_tables):
    assert "o4" not in set(mini_tables["fact_sales"].order_id)


def test_canceled_orders_are_kept_in_fact(mini_tables):
    f = mini_tables["fact_sales"]
    st = mini_tables["dim_order_status"].set_index("status_key").order_status
    assert st[f[f.order_id == "o3"].status_key.iloc[0]] == "canceled"


# ------------------------------------------------------------- dim_customer
def test_customer_dimension_is_one_row_per_real_person(mini_tables):
    dc = mini_tables["dim_customer"]
    assert len(dc) == 3                        # u1, u2, u3
    assert dc.customer_unique_id.is_unique


def test_person_with_two_customer_ids_keeps_latest_location(mini_tables):
    dc = mini_tables["dim_customer"].set_index("customer_unique_id")
    assert dc.loc["u1", "customer_state"] == "RJ"   # c2 is the more recent order


def test_both_orders_of_same_person_share_one_customer_key(mini_tables):
    assert fact(mini_tables, "o1").customer_key == fact(mini_tables, "o2").customer_key
    assert fact(mini_tables, "o1").customer_key != fact(mini_tables, "o3").customer_key


# ------------------------------------------------------------- measures
def test_item_total_is_price_plus_freight(mini_tables):
    r = fact(mini_tables, "o1", 1)
    assert (r.price, r.freight_value, r.item_total) == (100.0, 10.0, 110.0)


def test_delivery_and_delay_days(mini_tables):
    r = fact(mini_tables, "o1")
    assert r.delivery_days == pytest.approx(10.5)
    assert r.delay_days == pytest.approx(-4.5)       # delivered early


def test_late_delivery_has_positive_delay(mini_tables):
    assert fact(mini_tables, "o2").delay_days == pytest.approx(5.0)


def test_not_delivered_order_has_null_delivery_measures(mini_tables):
    r = fact(mini_tables, "o3")
    assert r.delivery_days != r.delivery_days        # NaN
    import pandas as pd
    assert pd.isna(r.delivered_date_key)


def test_review_score_is_mean_of_order_reviews(mini_tables):
    assert fact(mini_tables, "o1").review_score == pytest.approx(4.0)   # (5+3)/2
    assert fact(mini_tables, "o1", 2).review_score == pytest.approx(4.0)


def test_order_without_review_gets_null_score(mini_tables):
    assert fact(mini_tables, "o2").review_score != fact(mini_tables, "o2").review_score


def test_main_payment_is_the_largest_value(mini_tables):
    pt = mini_tables["dim_payment_type"].set_index("payment_type_key").payment_type
    assert pt[fact(mini_tables, "o1").payment_type_key] == "voucher"
    assert pt[fact(mini_tables, "o2").payment_type_key] == "boleto"
    assert fact(mini_tables, "o3").payment_installments == 3


# ------------------------------------------------------------- dim_product
def test_category_translation_and_manual_extra(mini_tables):
    dp = mini_tables["dim_product"].set_index("product_id").category_en
    assert dp["p1"] == "bed_bath_table"
    assert dp["p2"] == "pc_gamer"                 # EXTRA_TRANSLATION


def test_missing_category_becomes_unknown(mini_tables):
    assert mini_tables["dim_product"].set_index("product_id").category_en["p3"] == "unknown"


# ------------------------------------------------------------- dim_date
def test_dim_date_is_contiguous_and_covers_purchase_and_delivery(mini_tables):
    dd = mini_tables["dim_date"]
    assert dd.date_key.min() == 20170110 and dd.date_key.max() == 20170320
    assert len(dd) == 70                           # 10 Jan .. 20 Mar 2017, inclusive
    f = mini_tables["fact_sales"]
    keys = set(dd.date_key)
    assert set(f.purchase_date_key) <= keys
    assert set(f.delivered_date_key.dropna().astype(int)) <= keys


def test_dim_date_attributes(mini_tables):
    r = mini_tables["dim_date"].set_index("date_key").loc[20170310]  # a Friday
    assert (r.year, r.month, r.quarter, r.day, r.year_month) == (2017, 3, 1, 10, "2017-03")
    assert r.day_name == "Friday" and r.is_weekend == 0
    assert mini_tables["dim_date"].set_index("date_key").loc[20170311].is_weekend == 1


def test_surrogate_keys_are_sequential(mini_tables):
    for t, k in [("dim_customer", "customer_key"), ("dim_product", "product_key"),
                 ("dim_seller", "seller_key")]:
        assert list(mini_tables[t][k]) == list(range(1, len(mini_tables[t]) + 1))


# ------------------------------------------------------------- load
def test_load_creates_all_tables_and_row_counts(mini_db):
    counts = {t: mini_db.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in
              ["fact_sales", "dim_customer", "dim_product", "dim_seller", "dim_date",
               "dim_payment_type", "dim_order_status"]}
    assert counts["fact_sales"] == 4
    assert counts["dim_customer"] == 3 and counts["dim_product"] == 3 and counts["dim_seller"] == 2
    assert counts["dim_payment_type"] == 3 and counts["dim_order_status"] == 3


def test_load_has_no_orphans(mini_db):
    assert mini_db.execute("PRAGMA foreign_key_check").fetchall() == []


def test_quality_check_fails_loudly_on_wrong_row_count(mini_db):
    """The mini warehouse has 4 fact rows, not 112,650 -> quality_checks must refuse it."""
    with pytest.raises(SystemExit):
        run_etl.quality_checks(mini_db)


def test_load_is_idempotent(mini_tables, tmp_path):
    db = tmp_path / "x.db"
    for _ in range(2):
        try:
            run_etl.load(mini_tables, db, run_etl.REPO / "src" / "sql" / "01_schema.sql")
        except SystemExit:
            pass
    import sqlite3
    con = sqlite3.connect(db)
    assert con.execute("SELECT COUNT(*) FROM fact_sales").fetchone()[0] == 4
    con.close()
