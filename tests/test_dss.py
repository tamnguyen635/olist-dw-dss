"""Sanity tests for the three src/dss/ modules — run against the real DW.

Focuses on the traps called out in docs/TASKS_VY.md: the RFM frequency-of-1
trap, the 20-month forecast window, and the two different epistemic statuses
of the what-if models (measured vs. user-supplied assumption).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src" / "app"))
sys.path.insert(0, str(REPO / "src" / "dss"))

import forecast as fc  # noqa: E402
import rfm as rfm_mod  # noqa: E402
import whatif as wi  # noqa: E402

DB_MISSING = not (REPO / "data" / "processed" / "olist_dw.db").exists()
pytestmark = pytest.mark.skipif(DB_MISSING, reason="run `python src/etl/run_etl.py` first")


def test_forecast_train_test_split_sizes():
    r = fc.run_forecast()
    assert len(r.train_months) + len(r.test_months) == len(r.history)
    assert len(r.test_months) == fc.TEST_SIZE
    assert r.history["year_month"].min() == "2017-01"
    assert r.history["year_month"].max() == "2018-08"


def test_forecast_errors_are_nonnegative_and_finite():
    r = fc.run_forecast()
    for v in (r.naive_mae, r.naive_mape, r.holt_mae, r.holt_mape):
        assert v >= 0
    assert r.holt_forecast_ci[0] <= r.holt_forecast_next <= r.holt_forecast_ci[1]


def test_rfm_frequency_trap_is_handled():
    """Guards against the exact trap in TASKS_VY.md 5.2: >=97% of customers have
    exactly one order, so "frequency" must not be used as a continuous feature."""
    feats = rfm_mod.build_customer_features()
    repeat_share = feats["repeat_flag"].mean()
    assert repeat_share < 0.10  # matches the ~3% figure in the brief
    assert set(feats["repeat_flag"].unique()) <= {0, 1}


def test_rfm_k_within_requested_range_and_segments_named():
    result = rfm_mod.run_rfm()
    assert 3 <= result.k <= 4
    assert result.table["segment_name"].notna().all()
    assert set(result.segment_profile["segment_name"]) == set(
        result.table["segment_name"].unique()
    )
    assert -1 <= result.silhouette <= 1


def test_whatif_delivery_uses_measured_baselines():
    r = wi.whatif_delivery(target_late_rate_pct=0)
    # 0% late -> averages converge to the measured on-time score exactly.
    assert r.projected_avg_review == pytest.approx(wi.REVIEW_SCORE_ON_TIME, abs=1e-6)
    with pytest.raises(ValueError):
        wi.whatif_delivery(target_late_rate_pct=150)


def test_whatif_promotion_zero_discount_is_a_no_op():
    import queries as q

    cat = q.category_revenue_summary().iloc[0]["category_en"]
    r = wi.whatif_promotion(cat, discount_pct=0, elasticity=1.5)
    assert r.projected_revenue == pytest.approx(r.base_revenue, rel=1e-9)
    with pytest.raises(ValueError):
        wi.whatif_promotion(cat, discount_pct=10, elasticity=-1)
