"""Sanity tests for src/app/queries.py — run against the real processed DW.

Not a full test suite; the point is cheap evidence that "it runs" claims are
backed by something, per the project's working agreement. Requires
data/processed/olist_dw.db to exist (python src/etl/run_etl.py first).

Usage:
    pytest tests/ -q
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src" / "app"))
sys.path.insert(0, str(REPO / "src" / "dss"))

import queries as q  # noqa: E402

DB_MISSING = not (REPO / "data" / "processed" / "olist_dw.db").exists()
pytestmark = pytest.mark.skipif(DB_MISSING, reason="run `python src/etl/run_etl.py` first")


def test_kpi_summary_sane():
    kpi = q.kpi_summary()
    assert kpi["revenue"] > 0
    assert kpi["orders"] > 0
    assert 0 <= kpi["avg_review"] <= 5
    assert 0 <= kpi["pct_late"] <= 100


def test_monthly_revenue_window_matches_brief():
    mr = q.monthly_revenue("2017-01", "2018-08")
    assert len(mr) == 20  # TASKS_VY.md: 20 full months in this window
    assert mr["year_month"].min() == "2017-01"
    assert mr["year_month"].max() == "2018-08"
    assert (mr["revenue"] > 0).all()


def test_rollup_sums_to_monthly_total():
    yearly = q.rollup_by_year()["revenue"].sum()
    monthly = q.monthly_revenue("2016-01", "2018-12")["revenue"].sum()
    assert yearly == pytest.approx(monthly, rel=1e-6)


def test_drilldown_covers_all_quarters_present():
    years = q.available_years()
    dd = q.drilldown_by_month(years[-1])
    assert dd["quarter"].nunique() >= 1
    assert (dd["revenue"] > 0).all()


def test_slice_by_category_nonempty():
    years = q.available_years()
    sl = q.slice_by_category(years[-1], top_n=5)
    assert 0 < len(sl) <= 5


def test_dice_requires_real_filters_and_is_parameterized():
    states = q.available_states()[:2]
    cats = q.available_categories()[:2]
    dc = q.dice_states_categories(states, cats)
    assert set(dc["customer_state"]).issubset(set(states))
    assert set(dc["category_en"]).issubset(set(cats))


def test_delivery_vs_review_only_delivered_orders():
    dvr = q.delivery_vs_review()
    assert set(dvr["delivery"]) <= {"late", "on_time_or_early"}
    # late deliveries should score noticeably worse than on-time (TASKS_VY.md finding)
    late = dvr.loc[dvr.delivery == "late", "avg_review"].iloc[0]
    on_time = dvr.loc[dvr.delivery == "on_time_or_early", "avg_review"].iloc[0]
    assert late < on_time


def test_delivery_late_rate_in_range():
    rate = q.delivery_late_rate()
    assert 0 <= rate <= 100


def test_category_revenue_summary_used_by_whatif():
    summary = q.category_revenue_summary()
    assert len(summary) > 0
    assert (summary["revenue"] > 0).all()


def test_customer_order_history_grain_is_one_row_per_order():
    oh = q.customer_order_history()
    assert oh.duplicated(subset=["customer_key", "order_id"]).sum() == 0
