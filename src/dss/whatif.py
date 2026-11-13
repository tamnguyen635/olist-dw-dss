"""
DSS component 5.3 — what-if models.

Two sliders, two different epistemic statuses:
  1. Delivery -> satisfaction: driven by a REAL, measured relationship in the DW
     (late deliveries average review 2.55 vs 4.21 for on-time, see
     docs/data_contract.md / TASKS_VY.md). The output is a projection under the
     (reasonable) assumption that this average gap holds if the late rate changes.
  2. Promotion -> revenue: driven by a price elasticity of demand the USER supplies.
     This is an ASSUMPTION the user is testing, not a measured fact or a forecast.
     The UI/report must say so explicitly every time this model's output is shown.

Usage:
    python src/dss/whatif.py
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src" / "app"))

# Measured baselines (docs/data_contract.md convention: delivered orders only).
REVIEW_SCORE_LATE = 2.55
REVIEW_SCORE_ON_TIME = 4.21


@dataclass
class DeliveryWhatIfResult:
    current_late_rate_pct: float
    target_late_rate_pct: float
    current_avg_review: float
    projected_avg_review: float
    delta_avg_review: float


@dataclass
class PromotionWhatIfResult:
    category: str
    base_revenue: float
    discount_pct: float
    elasticity: float
    price_multiplier: float
    quantity_multiplier: float
    projected_revenue: float
    delta_revenue: float
    delta_revenue_pct: float


def current_late_rate() -> float:
    import queries as q
    return q.delivery_late_rate()


def whatif_delivery(target_late_rate_pct: float,
                     current_late_rate_pct: float | None = None) -> DeliveryWhatIfResult:
    """Nếu tỷ lệ giao trễ thay đổi từ `current_late_rate_pct` -> `target_late_rate_pct`,
    điểm đánh giá trung bình (toàn bộ đơn đã giao) dự kiến thay đổi bao nhiêu?

    Giả định: điểm TB của nhóm trễ (2.55) và nhóm đúng hạn (4.21) không đổi — chỉ
    tỷ trọng hai nhóm thay đổi. Đây là một phép nội suy tuyến tính đơn giản, không
    phải mô hình nhân quả đầy đủ (vẫn còn các yếu tố khác ảnh hưởng đến review).
    """
    if current_late_rate_pct is None:
        current_late_rate_pct = current_late_rate()
    if not 0 <= target_late_rate_pct <= 100:
        raise ValueError("target_late_rate_pct phải trong khoảng [0, 100]")

    def weighted_avg(late_pct: float) -> float:
        p = late_pct / 100.0
        return p * REVIEW_SCORE_LATE + (1 - p) * REVIEW_SCORE_ON_TIME

    current_avg = weighted_avg(current_late_rate_pct)
    projected_avg = weighted_avg(target_late_rate_pct)
    return DeliveryWhatIfResult(
        current_late_rate_pct=current_late_rate_pct,
        target_late_rate_pct=target_late_rate_pct,
        current_avg_review=round(current_avg, 4),
        projected_avg_review=round(projected_avg, 4),
        delta_avg_review=round(projected_avg - current_avg, 4),
    )


def whatif_promotion(category: str, discount_pct: float, elasticity: float,
                      base_revenue: float | None = None) -> PromotionWhatIfResult:
    """Nếu giảm giá `discount_pct`% cho danh mục `category`, với độ co giãn cầu theo
    giá do người dùng nhập (`elasticity`, quy ước dương = cầu tăng khi giá giảm),
    doanh thu dự kiến thay đổi bao nhiêu?

    Mô hình: %Δquantity = elasticity * %Δ(-price). Revenue_new = Revenue_base *
    (1 - discount) * (1 + elasticity * discount).

    GIẢ ĐỊNH DO NGƯỜI DÙNG ĐẶT — không phải số đo thực tế hay dự báo chắc chắn.
    """
    if not 0 <= discount_pct <= 100:
        raise ValueError("discount_pct phải trong khoảng [0, 100]")
    if elasticity < 0:
        raise ValueError("elasticity phải >= 0 (quy ước: cầu tăng khi giá giảm)")

    if base_revenue is None:
        import queries as q
        summary = q.category_revenue_summary()
        row = summary[summary.category_en == category]
        if row.empty:
            raise ValueError(f"Không tìm thấy danh mục '{category}' trong DW.")
        base_revenue = float(row.iloc[0]["revenue"])

    d = discount_pct / 100.0
    price_mult = 1 - d
    qty_mult = 1 + elasticity * d
    projected = base_revenue * price_mult * qty_mult
    return PromotionWhatIfResult(
        category=category, base_revenue=round(base_revenue, 2),
        discount_pct=discount_pct, elasticity=elasticity,
        price_multiplier=round(price_mult, 4), quantity_multiplier=round(qty_mult, 4),
        projected_revenue=round(projected, 2),
        delta_revenue=round(projected - base_revenue, 2),
        delta_revenue_pct=round((projected - base_revenue) / base_revenue * 100, 2),
    )


if __name__ == "__main__":
    cur = current_late_rate()
    print(f"Tỷ lệ giao trễ hiện tại: {cur:.2f}%\n")

    print("--- What-if: giảm giao trễ -> điểm hài lòng ---")
    for target in (cur, max(0, cur - 3), max(0, cur - 6), 0):
        r = whatif_delivery(target, current_late_rate_pct=cur)
        print(f"  trễ {r.target_late_rate_pct:5.2f}% -> điểm TB dự kiến {r.projected_avg_review:.3f} "
              f"(Δ so với hiện tại: {r.delta_avg_review:+.3f})")

    print("\n--- What-if: khuyến mãi theo danh mục -> doanh thu (GIẢ ĐỊNH người dùng đặt) ---")
    import queries as q
    top_cat = q.category_revenue_summary().iloc[0]["category_en"]
    for discount, elasticity in [(10, 1.0), (10, 2.0), (20, 1.5)]:
        r = whatif_promotion(top_cat, discount, elasticity)
        print(f"  [{top_cat}] giảm giá {discount}%, co giãn={elasticity} -> doanh thu "
              f"{r.base_revenue:,.0f} -> {r.projected_revenue:,.0f} ({r.delta_revenue_pct:+.2f}%)")
