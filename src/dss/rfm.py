"""
DSS component 5.2 — RFM + K-Means customer segmentation.

TRAP (see TASKS_VY.md 5.2): only ~2,913 / 95,420 customers (~3%) have placed 2+ orders,
so Frequency computed the usual way is (almost) always 1 and a quantile split (qcut) on
it is meaningless. Fix: replace the classic F with
  (a) a BINARY repeat-purchase flag (1 order vs >=2 orders), and
  (b) the customer's average review score, which carries real behavioural signal that
      a frequency-of-1 column cannot.
Clustering features are therefore: Recency, Monetary, repeat_flag, avg_review.

Reference date for Recency: 2018-09-03 (one month after the last order in the
2017-01..2018-08 analysis window), matching TASKS_VY.md.

Usage:
    python src/dss/rfm.py
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src" / "app"))

REFERENCE_DATE = pd.Timestamp("2018-09-03")
FEATURES = ["recency_days", "monetary", "repeat_flag", "avg_review"]
SEGMENT_NAMES = {
    # Assigned at runtime from cluster centers (see _name_segments); kept here only
    # as the vocabulary the report/dashboard should use.
    "high_value": "Khách giá trị cao",
    "new": "Khách mới",
    "dormant": "Khách ngủ đông",
    "regular": "Khách thường xuyên",
}


@dataclass
class RFMResult:
    table: pd.DataFrame            # per-customer features + cluster + segment_name
    k: int
    silhouette: float
    elbow_inertias: dict[int, float]
    silhouette_scores: dict[int, float]
    segment_profile: pd.DataFrame  # mean features + size per segment
    segment_actions: dict[str, str]


def build_customer_features(order_history: pd.DataFrame | None = None,
                             reference_date: pd.Timestamp = REFERENCE_DATE) -> pd.DataFrame:
    """One row per customer_key: recency_days, monetary, repeat_flag, avg_review."""
    if order_history is None:
        import queries as q  # the only DB access point
        order_history = q.customer_order_history()

    oh = order_history.copy()
    oh["purchase_date"] = pd.to_datetime(oh["purchase_date"])

    grouped = oh.groupby("customer_key").agg(
        last_purchase=("purchase_date", "max"),
        monetary=("order_value", "sum"),
        n_orders=("order_id", "nunique"),
        avg_review=("avg_review", "mean"),
    ).reset_index()

    grouped["recency_days"] = (reference_date - grouped["last_purchase"]).dt.days
    grouped["repeat_flag"] = (grouped["n_orders"] >= 2).astype(int)
    # a small number of customers have no review at all (NULL review_score for every order)
    grouped["avg_review"] = grouped["avg_review"].fillna(grouped["avg_review"].median())
    return grouped[["customer_key", "recency_days", "monetary", "n_orders",
                     "repeat_flag", "avg_review"]]


SILHOUETTE_SAMPLE_SIZE = 5000  # silhouette_score is O(n^2); ~96k customers needs subsampling


def choose_k(X_scaled: np.ndarray, k_range=range(2, 7), random_state: int = 42):
    inertias, sil_scores = {}, {}
    for k in k_range:
        km = KMeans(n_clusters=k, n_init=10, random_state=random_state).fit(X_scaled)
        inertias[k] = km.inertia_
        sil_scores[k] = silhouette_score(
            X_scaled, km.labels_,
            sample_size=min(SILHOUETTE_SAMPLE_SIZE, len(X_scaled)),
            random_state=random_state) if k > 1 else np.nan
    return inertias, sil_scores


def _name_segments(profile: pd.DataFrame) -> dict[int, str]:
    """Business naming, in priority order:
    1) highest repeat_flag share (clearly repeat buyers, who also spend the most
       monetary) -> "Khách giá trị cao".
    2) among the remaining (one-time buyers, where recency/monetary barely differ
       -- avg_review is what actually separates them): highest avg_review ->
       "Khách mới" (satisfied first-time buyers, worth nurturing toward a 2nd
       order); lowest avg_review -> "Khách ngủ đông" (unhappy one-time buyers,
       least likely to return without a win-back push).
    3) anything left over (only happens for K > 3) -> "Khách thường xuyên".
    """
    names: dict[int, str] = {}
    remaining = set(profile.index)

    high_value = profile.loc[list(remaining)].sort_values(
        ["repeat_flag", "monetary"], ascending=False).index[0]
    names[high_value] = SEGMENT_NAMES["high_value"]
    remaining.discard(high_value)

    if remaining:
        ranked = profile.loc[list(remaining)].sort_values("avg_review", ascending=False)
        happiest = ranked.index[0]
        names[happiest] = SEGMENT_NAMES["new"]
        remaining.discard(happiest)

    if remaining:
        unhappiest = profile.loc[list(remaining)].sort_values("avg_review", ascending=True).index[0]
        names[unhappiest] = SEGMENT_NAMES["dormant"]
        remaining.discard(unhappiest)

    for c in remaining:
        names[c] = SEGMENT_NAMES["regular"]
    return names


SEGMENT_ACTIONS = {
    SEGMENT_NAMES["high_value"]: "Chăm sóc VIP: ưu đãi độc quyền, giao hàng ưu tiên, giữ chân trước khi họ rời đi.",
    SEGMENT_NAMES["new"]: "Khách hài lòng ở đơn đầu nhưng chưa quay lại: gửi voucher cho đơn thứ 2, "
                          "gợi ý sản phẩm liên quan để biến thành khách mua lại.",
    SEGMENT_NAMES["dormant"]: "Khách không hài lòng ở đơn đầu: khảo sát lý do, chiến dịch win-back/giảm giá "
                              "để tránh mất khách vĩnh viễn.",
    SEGMENT_NAMES["regular"]: "Duy trì bằng chương trình khách hàng thân thiết, nhắc mua theo mùa vụ.",
}


def run_rfm(order_history: pd.DataFrame | None = None, k: int | None = None,
            random_state: int = 42) -> RFMResult:
    feats = build_customer_features(order_history)
    X = feats[FEATURES].to_numpy(dtype=float)
    X_scaled = StandardScaler().fit_transform(X)

    inertias, sil_scores = choose_k(X_scaled)
    chosen_k = k or max(sil_scores, key=sil_scores.get)  # best silhouette in [2..6]
    chosen_k = max(3, min(4, chosen_k))  # keep within the 3-4 range requested in the brief

    km = KMeans(n_clusters=chosen_k, n_init=10, random_state=random_state).fit(X_scaled)
    feats = feats.copy()
    feats["cluster"] = km.labels_
    final_sil = silhouette_score(
        X_scaled, km.labels_,
        sample_size=min(SILHOUETTE_SAMPLE_SIZE, len(X_scaled)), random_state=random_state)

    profile = feats.groupby("cluster")[FEATURES].mean()
    profile["size"] = feats.groupby("cluster").size()
    profile["pct"] = (profile["size"] / len(feats) * 100).round(1)

    name_map = _name_segments(profile)
    feats["segment_name"] = feats["cluster"].map(name_map)
    profile["segment_name"] = profile.index.map(name_map)

    return RFMResult(
        table=feats, k=chosen_k, silhouette=final_sil,
        elbow_inertias=inertias, silhouette_scores=sil_scores,
        segment_profile=profile.reset_index(),
        segment_actions=SEGMENT_ACTIONS,
    )


if __name__ == "__main__":
    pd.set_option("display.width", 140)
    result = run_rfm()
    print(f"K chọn = {result.k} (silhouette = {result.silhouette:.3f})\n")
    print("Elbow (inertia theo K):")
    for kk, v in result.elbow_inertias.items():
        print(f"  K={kk}: inertia={v:,.1f}  silhouette={result.silhouette_scores[kk]:.3f}")
    print("\nHồ sơ từng phân khúc:")
    print(result.segment_profile.to_string(index=False))
    print("\nHành động đề xuất:")
    for seg, action in result.segment_actions.items():
        if seg in result.segment_profile.segment_name.values:
            print(f"  - {seg}: {action}")
    print("\nLưu ý: F (tần suất) được thay bằng cờ nhị phân mua lại + điểm đánh giá TB, "
          "vì ~97% khách hàng chỉ có 1 đơn nên F liên tục không chia phân vị được.")
