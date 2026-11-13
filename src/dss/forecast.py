"""
DSS component 5.1 — Monthly revenue forecast.

Data: monthly revenue, 2017-01..2018-08 (20 points; see docs/data_contract.md and
TASKS_VY.md for why the series is cut to this window — 2016 only has 3 scattered
months and 2018-09 only has 1 order).

LIMITATION (state this in the report/UI, do not oversell): the series is short
(20 months) and does not cover two full seasonal cycles, so a seasonal model
cannot be reliably fit or validated. We therefore compare a naive baseline
against Holt's linear trend method (no seasonal component) rather than a full
seasonal Holt-Winters model.

Usage:
    python src/dss/forecast.py
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src" / "app"))

TEST_SIZE = 4  # hold out the last 4 months (2018-05..2018-08) for evaluation


@dataclass
class ForecastResult:
    history: pd.DataFrame          # year_month, revenue (full series used)
    train_months: list[str]
    test_months: list[str]
    naive_pred: np.ndarray         # predictions on the test window
    holt_pred: np.ndarray
    naive_mae: float
    naive_mape: float
    holt_mae: float
    holt_mape: float
    holt_forecast_next: float      # 1-step-ahead forecast past the end of history
    holt_forecast_ci: tuple[float, float]


def _mae(y_true, y_pred) -> float:
    return float(np.mean(np.abs(np.asarray(y_true) - np.asarray(y_pred))))


def _mape(y_true, y_pred) -> float:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    return float(np.mean(np.abs((y_true - y_pred) / y_true)) * 100)


def _naive_moving_average_forecast(train: np.ndarray, horizon: int, window: int = 3) -> np.ndarray:
    """Baseline: repeat the average of the last `window` training months for every
    step of the horizon (a flat, trend-free forecast)."""
    level = train[-window:].mean()
    return np.full(horizon, level)


def load_series(db_path: Path | None = None) -> pd.DataFrame:
    import queries as q  # local import: src/app/queries.py is the only DB access point
    df = q.monthly_revenue_series_for_forecast() if db_path is None else \
        q.monthly_revenue("2017-01", "2018-08")
    return df[["year_month", "revenue"]].sort_values("year_month").reset_index(drop=True)


def run_forecast(df: pd.DataFrame | None = None, test_size: int = TEST_SIZE) -> ForecastResult:
    if df is None:
        df = load_series()
    if len(df) <= test_size:
        raise ValueError(f"Cần nhiều hơn {test_size} tháng dữ liệu để chia train/test.")

    revenue = df["revenue"].to_numpy(dtype=float)
    months = df["year_month"].tolist()
    train, test = revenue[:-test_size], revenue[-test_size:]
    train_months, test_months = months[:-test_size], months[-test_size:]

    # ---- Baseline: moving-average (flat) forecast ----
    naive_pred = _naive_moving_average_forecast(train, horizon=test_size)

    # ---- Holt's linear trend method (no seasonal component: series too short) ----
    holt_model = ExponentialSmoothing(train, trend="add", seasonal=None,
                                       initialization_method="estimated").fit()
    holt_pred = holt_model.forecast(test_size)

    # ---- Refit on the FULL series for the actual next-month forecast + a rough 95% CI
    full_model = ExponentialSmoothing(revenue, trend="add", seasonal=None,
                                       initialization_method="estimated").fit()
    next_point = float(full_model.forecast(1)[0])
    resid_std = float(np.std(full_model.resid, ddof=1))
    ci = (next_point - 1.96 * resid_std, next_point + 1.96 * resid_std)

    return ForecastResult(
        history=df, train_months=train_months, test_months=test_months,
        naive_pred=naive_pred, holt_pred=np.asarray(holt_pred),
        naive_mae=_mae(test, naive_pred), naive_mape=_mape(test, naive_pred),
        holt_mae=_mae(test, holt_pred), holt_mape=_mape(test, holt_pred),
        holt_forecast_next=next_point, holt_forecast_ci=ci,
    )


if __name__ == "__main__":
    r = run_forecast()
    print("Train:", r.train_months[0], "..", r.train_months[-1], f"({len(r.train_months)} tháng)")
    print("Test :", r.test_months, "\n")
    print(f"{'model':<28}{'MAE':>14}{'MAPE (%)':>12}")
    print(f"{'Baseline (moving avg)':<28}{r.naive_mae:>14,.2f}{r.naive_mape:>12.2f}")
    print(f"{'Holt linear trend':<28}{r.holt_mae:>14,.2f}{r.holt_mape:>12.2f}")
    print(f"\nDự báo tháng kế tiếp sau {r.history.year_month.iloc[-1]}: "
          f"{r.holt_forecast_next:,.2f} (95% CI: {r.holt_forecast_ci[0]:,.2f} .. {r.holt_forecast_ci[1]:,.2f})")
    print("\nLưu ý: chuỗi chỉ có 20 tháng, chưa đủ 2 chu kỳ mùa vụ -> không dùng mô hình mùa vụ, "
          "độ tin cậy dự báo dài hạn thấp.")
