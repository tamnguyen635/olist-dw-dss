"""Integrity + reconciliation of the REAL warehouse against the raw CSVs and the schema."""
from __future__ import annotations

import pandas as pd
import pytest

from conftest import RAW, needs_dw, needs_raw

pytestmark = needs_dw

DIMS = ["dim_date", "dim_customer", "dim_product", "dim_seller", "dim_payment_type", "dim_order_status"]


def one(con, sql):
    return con.execute(sql).fetchone()[0]


# ----------------------------------------------------------------- schema
def test_all_seven_tables_exist(dw):
    names = {r[0] for r in dw.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert set(DIMS + ["fact_sales"]) <= names


def test_fact_columns_match_data_contract(dw):
    cols = {r[1] for r in dw.execute("PRAGMA table_info(fact_sales)")}
    expected = {"sales_key", "order_id", "order_item_id", "purchase_date_key", "delivered_date_key",
                "customer_key", "product_key", "seller_key", "payment_type_key", "status_key",
                "price", "freight_value", "item_total", "payment_installments", "review_score",
                "delivery_days", "delay_days"}
    assert expected <= cols, expected - cols


def test_fact_has_six_foreign_keys_to_dimensions(dw):
    fks = dw.execute("PRAGMA foreign_key_list(fact_sales)").fetchall()
    assert len({f[2] for f in fks}) == 6
    assert len(fks) == 7           # dim_date is referenced twice (role-playing: purchase + delivery)


def test_indexes_exist_for_join_keys(dw):
    idx = {r[1] for r in dw.execute("PRAGMA index_list(fact_sales)")}
    assert {"ix_fact_purchase_date", "ix_fact_customer", "ix_fact_product",
            "ix_fact_seller", "ix_fact_status"} <= idx


def test_foreign_key_check_is_clean(dw):
    assert dw.execute("PRAGMA foreign_key_check").fetchall() == []


# ----------------------------------------------------------------- reconciliation with raw
@needs_raw
def test_fact_rows_equal_order_items_rows(dw):
    items = pd.read_csv(RAW / "olist_order_items_dataset.csv")
    assert one(dw, "SELECT COUNT(*) FROM fact_sales") == len(items)


@needs_raw
def test_sum_of_price_and_freight_reconcile_to_source(dw):
    items = pd.read_csv(RAW / "olist_order_items_dataset.csv")
    assert one(dw, "SELECT SUM(price) FROM fact_sales") == pytest.approx(items.price.sum(), abs=0.5)
    assert one(dw, "SELECT SUM(freight_value) FROM fact_sales") == pytest.approx(items.freight_value.sum(), abs=0.5)


@needs_raw
def test_distinct_orders_reconcile_to_source(dw):
    items = pd.read_csv(RAW / "olist_order_items_dataset.csv")
    assert one(dw, "SELECT COUNT(DISTINCT order_id) FROM fact_sales") == items.order_id.nunique()


@needs_raw
def test_customer_dimension_equals_distinct_real_persons(dw):
    c = pd.read_csv(RAW / "olist_customers_dataset.csv", dtype=str)
    assert one(dw, "SELECT COUNT(*) FROM dim_customer") == c.customer_unique_id.nunique()


@needs_raw
def test_dimension_sizes_reconcile_to_source(dw):
    assert one(dw, "SELECT COUNT(*) FROM dim_product") == len(pd.read_csv(RAW / "olist_products_dataset.csv"))
    assert one(dw, "SELECT COUNT(*) FROM dim_seller") == len(pd.read_csv(RAW / "olist_sellers_dataset.csv"))


@needs_raw
def test_status_mix_reconciles_to_orders_with_items(dw):
    o = pd.read_csv(RAW / "olist_orders_dataset.csv")
    items = pd.read_csv(RAW / "olist_order_items_dataset.csv", usecols=["order_id"])
    src = o[o.order_id.isin(items.order_id)].order_status.value_counts().to_dict()
    dwc = dict(dw.execute("""SELECT s.order_status, COUNT(DISTINCT f.order_id)
                             FROM fact_sales f JOIN dim_order_status s USING(status_key)
                             GROUP BY 1""").fetchall())
    assert dwc == src


# ----------------------------------------------------------------- key / uniqueness
def test_fact_natural_key_is_unique(dw):
    assert one(dw, """SELECT COUNT(*) FROM (SELECT order_id, order_item_id FROM fact_sales
                      GROUP BY 1,2 HAVING COUNT(*) > 1)""") == 0


@pytest.mark.parametrize("table,col", [
    ("dim_customer", "customer_unique_id"), ("dim_product", "product_id"),
    ("dim_seller", "seller_id"), ("dim_payment_type", "payment_type"),
    ("dim_order_status", "order_status"), ("dim_date", "full_date")])
def test_dimension_business_key_unique_and_not_null(dw, table, col):
    assert one(dw, f"SELECT COUNT(*) - COUNT(DISTINCT {col}) FROM {table}") == 0
    assert one(dw, f"SELECT COUNT(*) FROM {table} WHERE {col} IS NULL") == 0


def test_no_dimension_member_is_unused_except_known_cases(dw):
    """Every customer in dim_customer must have bought something (orders w/o items were dropped
    before dimensions are used) - tolerate small slack for persons whose only orders had no items."""
    unused = one(dw, """SELECT COUNT(*) FROM dim_customer c
                        WHERE NOT EXISTS (SELECT 1 FROM fact_sales f WHERE f.customer_key = c.customer_key)""")
    assert unused / one(dw, "SELECT COUNT(*) FROM dim_customer") < 0.01


# ----------------------------------------------------------------- dim_date
def test_dim_date_is_contiguous(dw):
    d = pd.read_sql_query("SELECT full_date FROM dim_date ORDER BY full_date", dw)
    days = pd.to_datetime(d.full_date)
    assert (days.diff().dropna() == pd.Timedelta(days=1)).all()


def test_dim_date_key_format_and_attributes(dw):
    bad = one(dw, """SELECT COUNT(*) FROM dim_date WHERE date_key !=
                     CAST(strftime('%Y%m%d', full_date) AS INTEGER)
                     OR year != CAST(strftime('%Y', full_date) AS INTEGER)
                     OR month != CAST(strftime('%m', full_date) AS INTEGER)
                     OR quarter != (month + 2) / 3
                     OR year_month != strftime('%Y-%m', full_date)""")
    assert bad == 0


def test_dim_date_covers_all_dates_used_by_fact(dw):
    assert one(dw, """SELECT COUNT(*) FROM fact_sales f LEFT JOIN dim_date d ON d.date_key = f.purchase_date_key
                      WHERE d.date_key IS NULL""") == 0


# ----------------------------------------------------------------- business rules
def test_item_total_equals_price_plus_freight(dw):
    assert one(dw, "SELECT COUNT(*) FROM fact_sales WHERE ABS(item_total - price - freight_value) > 0.001") == 0


def test_no_negative_money(dw):
    assert one(dw, "SELECT COUNT(*) FROM fact_sales WHERE price < 0 OR freight_value < 0") == 0


def test_review_score_in_range_1_to_5(dw):
    assert one(dw, "SELECT COUNT(*) FROM fact_sales WHERE review_score IS NOT NULL AND (review_score < 1 OR review_score > 5)") == 0


def test_non_delivered_rows_with_delivery_date_are_a_known_source_quirk(dw):
    """Olist itself has 6 *canceled* orders (7 item rows) that carry a delivery date.
    Harmless because every delivery metric filters status = 'delivered' (see test_olap.py),
    but it must stay tiny and limited to 'canceled'."""
    rows = dw.execute("""SELECT DISTINCT s.order_status FROM fact_sales f JOIN dim_order_status s USING(status_key)
                         WHERE s.order_status != 'delivered' AND f.delivered_date_key IS NOT NULL""").fetchall()
    assert {r[0] for r in rows} <= {"canceled"}
    assert one(dw, """SELECT COUNT(*) FROM fact_sales f JOIN dim_order_status s USING(status_key)
                      WHERE s.order_status != 'delivered' AND f.delivered_date_key IS NOT NULL""") <= 10


def test_every_delivered_row_has_delivery_date(dw):
    assert one(dw, """SELECT COUNT(*) FROM fact_sales f JOIN dim_order_status s USING(status_key)
                      WHERE s.order_status = 'delivered' AND f.delivered_date_key IS NULL""") <= 10


def test_delivered_orders_have_delivery_days_nonnegative(dw):
    assert one(dw, "SELECT COUNT(*) FROM fact_sales WHERE delivery_days < 0") == 0


def test_delay_days_is_consistent_with_delivery_date(dw):
    """delay_days > 0  <=>  delivered after the estimated date (sample the first 5,000 rows)."""
    rows = dw.execute("""SELECT delivery_days, delay_days FROM fact_sales
                         WHERE delay_days IS NOT NULL LIMIT 5000""").fetchall()
    assert rows and all(d >= 0 for d, _ in rows)


def test_installments_positive_when_present(dw):
    assert one(dw, "SELECT COUNT(*) FROM fact_sales WHERE payment_installments < 0") == 0


def test_every_product_has_english_category(dw):
    assert one(dw, "SELECT COUNT(*) FROM dim_product WHERE category_en IS NULL OR category_en = ''") == 0
    # the two categories missing from the Olist translation file must be translated by hand
    assert one(dw, "SELECT COUNT(*) FROM dim_product WHERE category_pt='pc_gamer' AND category_en='unknown'") == 0


def test_unknown_category_is_small(dw):
    n = one(dw, "SELECT COUNT(*) FROM dim_product WHERE category_en='unknown'")
    assert 0 < n < 1000


def test_published_headline_numbers_still_hold(dw):
    """Numbers quoted in report A / slides. If ETL changes, these must be updated on purpose."""
    assert one(dw, "SELECT COUNT(*) FROM fact_sales") == 112650
    assert one(dw, "SELECT COUNT(*) FROM dim_customer") == 96096
    assert one(dw, "SELECT COUNT(*) FROM dim_date") == 774
    assert round(one(dw, "SELECT SUM(price) FROM fact_sales"), 2) == 13591643.70
    assert round(one(dw, """SELECT SUM(price) FROM fact_sales f JOIN dim_order_status s USING(status_key)
                            WHERE s.order_status NOT IN ('canceled','unavailable')"""), 2) == 13494400.74
