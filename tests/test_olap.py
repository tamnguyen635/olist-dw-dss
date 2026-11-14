"""The five OLAP operations: SQL file (src/sql/02_olap_queries.sql) and the dashboard query layer."""
from __future__ import annotations

import pandas as pd
import pytest

import olap_demo
import queries as q
from conftest import DB, REPO, needs_dw

pytestmark = needs_dw

SQL_FILE = REPO / "src" / "sql" / "02_olap_queries.sql"
EXCL = "('canceled','unavailable')"


@pytest.fixture(scope="module")
def res():
    return olap_demo.run(DB, SQL_FILE)


def scalar(dw, sql):
    return dw.execute(sql).fetchone()[0]


def total_revenue(dw):
    return scalar(dw, f"""SELECT SUM(price) FROM fact_sales f JOIN dim_order_status s USING(status_key)
                          WHERE s.order_status NOT IN {EXCL}""")


# ------------------------------------------------------------------ SQL script
def test_script_contains_all_five_operations_and_extras(res):
    assert {"rollup_year", "drilldown_month_2017", "slice_year_2017_by_category",
            "dice_sp_rj_top_categories", "pivot_category_by_year"} <= set(res)


def test_every_olap_query_returns_rows_without_nulls_in_keys(res):
    for name, df in res.items():
        assert len(df) > 0, name
        assert not df.iloc[:, 0].isna().any(), name


def test_rollup_total_equals_total_revenue(res, dw):
    assert res["rollup_year"].revenue.sum() == pytest.approx(total_revenue(dw), abs=1.0)


def test_rollup_orders_equals_distinct_non_canceled_orders(res, dw):
    n = scalar(dw, f"""SELECT COUNT(DISTINCT order_id) FROM fact_sales f JOIN dim_order_status s USING(status_key)
                       WHERE s.order_status NOT IN {EXCL}""")
    assert res["rollup_year"].orders.sum() == n


def test_rollup_years_are_2016_2017_2018(res):
    assert list(res["rollup_year"].year) == [2016, 2017, 2018]


def test_drilldown_months_sum_to_year_and_belong_to_right_quarter(res):
    dd = res["drilldown_month_2017"]
    ru = res["rollup_year"].set_index("year").revenue
    assert dd.revenue.sum() == pytest.approx(ru[2017], abs=1.0)
    assert len(dd) == 12
    for _, r in dd.iterrows():
        assert r.quarter == (int(r.year_month[5:7]) + 2) // 3


def test_slice_is_top10_sorted_descending(res):
    s = res["slice_year_2017_by_category"]
    assert len(s) == 10
    assert s.revenue.is_monotonic_decreasing


def test_dice_only_contains_chosen_states(res):
    d = res["dice_sp_rj_top_categories"]
    assert set(d.iloc[:, 0]) <= {"SP", "RJ"}


def test_pivot_row_total_equals_sum_of_year_columns(res):
    p = res["pivot_category_by_year"]
    assert {"y2016", "y2017", "y2018", "total"} <= set(p.columns)
    assert (p[["y2016", "y2017", "y2018"]].fillna(0).sum(axis=1) - p["total"]).abs().max() < 1.0


def test_payment_mix_sums_to_100_percent(res):
    assert res["payment_mix"]["pct"].sum() == pytest.approx(100, abs=0.5)


def test_payment_mix_has_credit_card_as_top_method(res):
    assert res["payment_mix"].sort_values("revenue", ascending=False).iloc[0].payment_type == "credit_card"


def test_late_deliveries_have_lower_review_than_on_time(res):
    d = res["delivery_vs_review"]
    assert len(d) == 2
    assert d.avg_review.max() - d.avg_review.min() > 1.0     # the what-if model relies on this gap
    late = d[d.delivery.str.contains("late|tr", case=False)].iloc[0]
    assert late.avg_review == d.avg_review.min()
    assert late.avg_delivery_days > d.avg_delivery_days.min()


# ------------------------------------------------------------------ query layer (dashboard)
def test_query_layer_agrees_with_sql_script(res):
    assert q.rollup_by_year().revenue.sum() == pytest.approx(res["rollup_year"].revenue.sum(), abs=1.0)


def test_kpi_revenue_matches_total(dw):
    assert q.kpi_summary()["revenue"] == pytest.approx(total_revenue(dw), abs=1.0)


def test_kpi_orders_excludes_canceled(dw):
    n = scalar(dw, f"""SELECT COUNT(DISTINCT order_id) FROM fact_sales f JOIN dim_order_status s USING(status_key)
                       WHERE s.order_status NOT IN {EXCL}""")
    assert q.kpi_summary()["orders"] == n


def test_dice_empty_selection_returns_empty_frame_not_error():
    assert q.dice_states_categories([], ["health_beauty"]).empty
    assert q.dice_states_categories(["SP"], []).empty


def test_dice_year_filter_is_a_subset():
    all_years = q.dice_states_categories(["SP"], ["health_beauty"]).revenue.sum()
    y2018 = q.dice_states_categories(["SP"], ["health_beauty"], 2018).revenue.sum()
    assert 0 < y2018 < all_years


def test_dice_is_safe_against_sql_injection():
    out = q.dice_states_categories(["SP'; DROP TABLE fact_sales; --"], ["health_beauty"])
    assert out.empty
    assert len(q.rollup_by_year()) == 3                       # table still there


def test_slice_unknown_year_returns_empty():
    assert q.slice_by_category(1999).empty


def test_delivery_late_rate_is_between_5_and_12_percent():
    assert 5 < q.delivery_late_rate() < 12                    # report quotes 7.9 %


def test_state_table_contains_the_three_big_states():
    st = q.revenue_review_by_state()
    assert {"SP", "RJ", "MG"} <= set(st.iloc[:, 0])


def test_sp_is_the_top_state_by_revenue():
    st = q.revenue_review_by_state()
    rev = [c for c in st.columns if "revenue" in c.lower()][0]
    assert st.sort_values(rev, ascending=False).iloc[0, 0] == "SP"


def test_delivery_queries_only_use_delivered_orders():
    """Guard for the 7 'canceled with delivery date' rows: delivery stats must equal delivered-only SQL."""
    import sqlite3
    con = sqlite3.connect(DB)
    n = con.execute("""SELECT COUNT(*) FROM fact_sales f JOIN dim_order_status s USING(status_key)
                       WHERE s.order_status='delivered' AND f.delay_days IS NOT NULL""").fetchone()[0]
    con.close()
    assert q.delivery_vs_review()["items"].sum() == n
