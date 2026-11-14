"""Edge / contract tests for the DSS modules (complements tests/test_dss.py)."""
from __future__ import annotations

import numpy as np
import pytest

import forecast as fc
import rfm as rfm_mod
import whatif as wi
import queries as q
from conftest import needs_dw

pytestmark = needs_dw


# ---------------------------------------------------------------- forecast
def test_forecast_reports_baseline_and_holt_for_comparison():
    r = fc.run_forecast()
    assert r.naive_mape > 0 and r.holt_mape > 0
    assert np.isfinite([r.naive_mae, r.holt_mae, r.holt_forecast_next]).all()


def test_forecast_next_month_is_positive():
    assert fc.run_forecast().holt_forecast_next > 0


def test_forecast_is_deterministic():
    a, b = fc.run_forecast(), fc.run_forecast()
    assert a.holt_mae == b.holt_mae and a.naive_mae == b.naive_mae


def test_moving_average_baseline_unit():
    out = fc._naive_moving_average_forecast(np.array([10., 20., 30., 40.]), horizon=2, window=3)
    assert out[0] == pytest.approx(30.0)          # mean(20,30,40)
    assert len(out) == 2


def test_error_metrics_unit():
    assert fc._mae([100, 200], [110, 190]) == pytest.approx(10)
    assert fc._mape([100, 200], [110, 180]) == pytest.approx(10.0)


# ---------------------------------------------------------------- RFM
@pytest.fixture(scope="module")
def rfm_result():
    return rfm_mod.run_rfm()


def test_rfm_every_customer_in_exactly_one_segment(rfm_result):
    t = rfm_result.table
    assert t.segment_name.notna().all()
    assert int(rfm_result.segment_profile["size"].sum()) == len(t)
    assert t.index.is_unique or "customer_key" in t.columns


def test_rfm_is_deterministic_with_fixed_seed(rfm_result):
    b = rfm_mod.run_rfm()
    assert (rfm_result.table.cluster.values == b.table.cluster.values).all()


def test_rfm_k_is_3_or_4_and_each_segment_named_uniquely(rfm_result):
    assert rfm_result.k in (3, 4)
    names = rfm_result.segment_profile.segment_name.tolist()
    assert len(set(names)) == len(names) == rfm_result.k


def test_rfm_every_segment_has_a_recommended_action(rfm_result):
    assert set(rfm_result.segment_profile.segment_name) <= set(rfm_result.segment_actions)


def test_rfm_silhouette_is_in_valid_range(rfm_result):
    assert -1 <= rfm_result.silhouette <= 1
    assert set(rfm_result.silhouette_scores) == set(rfm_result.elbow_inertias)


def test_rfm_features_have_no_nan(rfm_result):
    assert not rfm_result.table[rfm_mod.FEATURES].isna().any().any()


def test_rfm_segment_names_are_not_misleading(rfm_result):
    """REVIEW_VY item 2: 'Khách mới' (new) and 'Khách ngủ đông' (dormant) have the SAME recency (~8 months),
    so those names are wrong. They differ only by review score."""
    p = rfm_result.segment_profile.set_index("segment_name")
    if "Khách mới" in p.index and "Khách ngủ đông" in p.index:
        gap = abs(p.loc["Khách mới", "recency_days"] - p.loc["Khách ngủ đông", "recency_days"])
        assert gap > 60, "'new' and 'dormant' segments have almost identical recency: rename them"


# ---------------------------------------------------------------- what-if delivery
def test_whatif_delivery_no_change_gives_zero_delta():
    r = wi.whatif_delivery(7.91, current_late_rate_pct=7.91)
    assert r.delta_avg_review == 0


def test_whatif_delivery_lower_late_rate_raises_review():
    assert wi.whatif_delivery(2, current_late_rate_pct=8).delta_avg_review > 0


def test_whatif_delivery_higher_late_rate_lowers_review():
    assert wi.whatif_delivery(15, current_late_rate_pct=8).delta_avg_review < 0


def test_whatif_delivery_bounds():
    assert wi.whatif_delivery(0, 8).projected_avg_review == pytest.approx(wi.REVIEW_SCORE_ON_TIME, abs=1e-3)
    assert wi.whatif_delivery(100, 8).projected_avg_review == pytest.approx(wi.REVIEW_SCORE_LATE, abs=1e-3)


@pytest.mark.parametrize("bad", [-1, 100.1, 250])
def test_whatif_delivery_rejects_out_of_range(bad):
    with pytest.raises(ValueError):
        wi.whatif_delivery(bad, current_late_rate_pct=8)


def test_whatif_constants_match_the_warehouse():
    """REVIEW_VY item 9: hard-coded constants must equal what the DW says."""
    d = q.delivery_vs_review().set_index("delivery").avg_review
    assert wi.REVIEW_SCORE_LATE == pytest.approx(d["late"], abs=0.01)
    assert wi.REVIEW_SCORE_ON_TIME == pytest.approx(d["on_time_or_early"], abs=0.01)


# ---------------------------------------------------------------- what-if promotion
def test_promotion_zero_discount_changes_nothing():
    r = wi.whatif_promotion("health_beauty", 0, 1.5, base_revenue=1000)
    assert r.projected_revenue == 1000 and r.delta_revenue == 0


def test_promotion_formula_hand_check():
    # base 1000, discount 10 %, elasticity 2 -> 1000 * 0.9 * 1.2 = 1080
    r = wi.whatif_promotion("x", 10, 2.0, base_revenue=1000)
    assert r.projected_revenue == pytest.approx(1080.0)
    assert r.delta_revenue_pct == pytest.approx(8.0)


def test_promotion_inelastic_demand_loses_revenue():
    assert wi.whatif_promotion("x", 20, 0.5, base_revenue=1000).delta_revenue < 0


def test_promotion_uses_warehouse_revenue_for_real_category():
    top = q.category_revenue_summary().iloc[0]
    r = wi.whatif_promotion(top.category_en, 10, 1.0)
    assert r.base_revenue == pytest.approx(float(top.revenue), abs=0.01)


def test_promotion_unknown_category_raises():
    with pytest.raises(ValueError):
        wi.whatif_promotion("not_a_category", 10, 1.0)


@pytest.mark.parametrize("disc,el", [(-1, 1), (101, 1), (10, -0.1)])
def test_promotion_rejects_invalid_inputs(disc, el):
    with pytest.raises(ValueError):
        wi.whatif_promotion("x", disc, el, base_revenue=100)
