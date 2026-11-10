"""
SQL query layer for the Streamlit dashboard.

All functions read ONLY from the processed SQLite DW (data/processed/olist_dw.db),
per the data contract in docs/data_contract.md. No CSV is ever touched here.

Convention (see docs/data_contract.md):
  - revenue = SUM(price); orders with status in ('canceled', 'unavailable') are excluded
    from revenue/orders metrics (CANCELED_STATUSES below).
  - delivery/delay metrics only make sense for status = 'delivered'.
  - All filters use "?" placeholders, never string concatenation.
"""
import sqlite3
from pathlib import Path
from typing import Optional, Sequence

import pandas as pd

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "olist_dw.db"

CANCELED_STATUSES = ("canceled", "unavailable")


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    if not db_path.exists():
        raise FileNotFoundError(
            f"Không tìm thấy {db_path}. Chạy `python src/etl/run_etl.py` trước.")
    return sqlite3.connect(db_path)


def _read(sql: str, params: Sequence = (), db_path: Path = DB_PATH) -> pd.DataFrame:
    with get_connection(db_path) as con:
        return pd.read_sql_query(sql, con, params=params)


def _not_canceled_clause(alias: str = "s") -> str:
    placeholders = ",".join("?" * len(CANCELED_STATUSES))
    return f"{alias}.order_status NOT IN ({placeholders})"


# --------------------------------------------------------------------------- filters
def available_years() -> list[int]:
    df = _read("SELECT DISTINCT d.year FROM fact_sales f "
               "JOIN dim_date d ON f.purchase_date_key = d.date_key ORDER BY d.year")
    return df["year"].tolist()


def available_states() -> list[str]:
    df = _read("SELECT DISTINCT customer_state FROM dim_customer "
               "WHERE customer_state IS NOT NULL ORDER BY customer_state")
    return df["customer_state"].tolist()


def available_categories() -> list[str]:
    df = _read("SELECT DISTINCT category_en FROM dim_product "
               "WHERE category_en IS NOT NULL ORDER BY category_en")
    return df["category_en"].tolist()


# --------------------------------------------------------------------------- page 1: Tổng quan
def kpi_summary() -> dict:
    """Doanh thu, số đơn, giá trị đơn TB, điểm đánh giá TB, % giao trễ."""
    sql = f"""
        SELECT ROUND(SUM(f.price), 2)                                  AS revenue,
               COUNT(DISTINCT f.order_id)                               AS orders,
               ROUND(SUM(f.price) * 1.0 / COUNT(DISTINCT f.order_id), 2) AS avg_order_value,
               ROUND(AVG(f.review_score), 2)                            AS avg_review
        FROM fact_sales f
        JOIN dim_order_status s ON f.status_key = s.status_key
        WHERE {_not_canceled_clause()}
    """
    row = _read(sql, CANCELED_STATUSES).iloc[0].to_dict()

    delay_sql = """
        SELECT ROUND(100.0 * SUM(CASE WHEN f.delay_days > 0 THEN 1 ELSE 0 END) / COUNT(*), 2) AS pct_late
        FROM fact_sales f
        JOIN dim_order_status s ON f.status_key = s.status_key
        WHERE s.order_status = 'delivered' AND f.delay_days IS NOT NULL
    """
    row["pct_late"] = _read(delay_sql).iloc[0]["pct_late"]
    return row


def monthly_revenue(year_month_from: str = "2017-01", year_month_to: str = "2018-08") -> pd.DataFrame:
    sql = f"""
        SELECT d.year_month, ROUND(SUM(f.price), 2) AS revenue, COUNT(DISTINCT f.order_id) AS orders
        FROM fact_sales f
        JOIN dim_date d         ON f.purchase_date_key = d.date_key
        JOIN dim_order_status s ON f.status_key = s.status_key
        WHERE {_not_canceled_clause()}
          AND d.year_month BETWEEN ? AND ?
        GROUP BY d.year_month ORDER BY d.year_month
    """
    return _read(sql, (*CANCELED_STATUSES, year_month_from, year_month_to))


# --------------------------------------------------------------------------- page 2: OLAP
def rollup_by_year() -> pd.DataFrame:
    """ROLL-UP: monthly -> yearly revenue."""
    sql = f"""
        SELECT d.year, ROUND(SUM(f.price), 2) AS revenue, COUNT(DISTINCT f.order_id) AS orders
        FROM fact_sales f
        JOIN dim_date d         ON f.purchase_date_key = d.date_key
        JOIN dim_order_status s ON f.status_key = s.status_key
        WHERE {_not_canceled_clause()}
        GROUP BY d.year ORDER BY d.year
    """
    return _read(sql, CANCELED_STATUSES)


def drilldown_by_month(year: int) -> pd.DataFrame:
    """DRILL-DOWN: a chosen year -> quarter -> month."""
    sql = f"""
        SELECT d.quarter, d.year_month, ROUND(SUM(f.price), 2) AS revenue
        FROM fact_sales f
        JOIN dim_date d         ON f.purchase_date_key = d.date_key
        JOIN dim_order_status s ON f.status_key = s.status_key
        WHERE d.year = ? AND {_not_canceled_clause()}
        GROUP BY d.quarter, d.year_month ORDER BY d.year_month
    """
    return _read(sql, (year, *CANCELED_STATUSES))


def slice_by_category(year: int, top_n: int = 10) -> pd.DataFrame:
    """SLICE: fix year, view revenue by product category."""
    sql = f"""
        SELECT p.category_en, ROUND(SUM(f.price), 2) AS revenue, COUNT(*) AS items_sold
        FROM fact_sales f
        JOIN dim_date d         ON f.purchase_date_key = d.date_key
        JOIN dim_product p      ON f.product_key = p.product_key
        JOIN dim_order_status s ON f.status_key = s.status_key
        WHERE d.year = ? AND {_not_canceled_clause()}
        GROUP BY p.category_en
        ORDER BY revenue DESC LIMIT ?
    """
    return _read(sql, (year, *CANCELED_STATUSES, top_n))


def dice_states_categories(states: Sequence[str], categories: Sequence[str],
                            year: Optional[int] = None) -> pd.DataFrame:
    """DICE: sub-cube = chosen states x chosen categories (optionally a chosen year)."""
    state_ph = ",".join("?" * len(states))
    cat_ph = ",".join("?" * len(categories))
    year_clause = "AND d.year = ?" if year is not None else ""
    sql = f"""
        SELECT c.customer_state, p.category_en, ROUND(SUM(f.price), 2) AS revenue
        FROM fact_sales f
        JOIN dim_date d         ON f.purchase_date_key = d.date_key
        JOIN dim_customer c     ON f.customer_key = c.customer_key
        JOIN dim_product p      ON f.product_key = p.product_key
        JOIN dim_order_status s ON f.status_key = s.status_key
        WHERE c.customer_state IN ({state_ph})
          AND p.category_en IN ({cat_ph})
          {year_clause}
          AND {_not_canceled_clause()}
        GROUP BY c.customer_state, p.category_en
        ORDER BY c.customer_state, revenue DESC
    """
    params = [*states, *categories] + ([year] if year is not None else []) + list(CANCELED_STATUSES)
    return _read(sql, params)


def pivot_category_by_year(top_n: int = 10) -> pd.DataFrame:
    """PIVOT: categories as rows, years as columns."""
    sql = f"""
        SELECT p.category_en,
               ROUND(SUM(CASE WHEN d.year = 2016 THEN f.price END), 2) AS y2016,
               ROUND(SUM(CASE WHEN d.year = 2017 THEN f.price END), 2) AS y2017,
               ROUND(SUM(CASE WHEN d.year = 2018 THEN f.price END), 2) AS y2018,
               ROUND(SUM(f.price), 2) AS total
        FROM fact_sales f
        JOIN dim_date d         ON f.purchase_date_key = d.date_key
        JOIN dim_product p      ON f.product_key = p.product_key
        JOIN dim_order_status s ON f.status_key = s.status_key
        WHERE {_not_canceled_clause()}
        GROUP BY p.category_en
        ORDER BY total DESC LIMIT ?
    """
    return _read(sql, (*CANCELED_STATUSES, top_n))


# --------------------------------------------------------------------------- page 3: Địa lý & khách hàng
def revenue_review_by_state(top_n: int = 27) -> pd.DataFrame:
    sql = f"""
        SELECT c.customer_state,
               ROUND(SUM(f.price), 2)         AS revenue,
               COUNT(DISTINCT f.order_id)     AS orders,
               ROUND(AVG(f.review_score), 2)  AS avg_review
        FROM fact_sales f
        JOIN dim_customer c     ON f.customer_key = c.customer_key
        JOIN dim_order_status s ON f.status_key = s.status_key
        WHERE {_not_canceled_clause()}
        GROUP BY c.customer_state
        ORDER BY revenue DESC LIMIT ?
    """
    return _read(sql, (*CANCELED_STATUSES, top_n))


def payment_mix() -> pd.DataFrame:
    sql = """
        SELECT pt.payment_type,
               ROUND(SUM(f.price), 2) AS revenue,
               ROUND(100.0 * SUM(f.price) / (SELECT SUM(price) FROM fact_sales WHERE payment_type_key IS NOT NULL), 2) AS pct
        FROM fact_sales f
        JOIN dim_payment_type pt ON f.payment_type_key = pt.payment_type_key
        GROUP BY pt.payment_type
        ORDER BY revenue DESC
    """
    return _read(sql)


# --------------------------------------------------------------------------- page 4: Giao hàng & hài lòng
def delivery_vs_review() -> pd.DataFrame:
    sql = """
        SELECT CASE WHEN f.delay_days > 0 THEN 'late' ELSE 'on_time_or_early' END AS delivery,
               COUNT(*) AS items,
               ROUND(AVG(f.delivery_days), 1) AS avg_delivery_days,
               ROUND(AVG(f.review_score), 2)  AS avg_review
        FROM fact_sales f
        JOIN dim_order_status s ON f.status_key = s.status_key
        WHERE s.order_status = 'delivered' AND f.delay_days IS NOT NULL
        GROUP BY delivery
    """
    return _read(sql)


def delivery_vs_review_by_state() -> pd.DataFrame:
    sql = """
        SELECT c.customer_state,
               CASE WHEN f.delay_days > 0 THEN 'late' ELSE 'on_time_or_early' END AS delivery,
               COUNT(*) AS items,
               ROUND(AVG(f.review_score), 2) AS avg_review
        FROM fact_sales f
        JOIN dim_customer c     ON f.customer_key = c.customer_key
        JOIN dim_order_status s ON f.status_key = s.status_key
        WHERE s.order_status = 'delivered' AND f.delay_days IS NOT NULL
        GROUP BY c.customer_state, delivery
        ORDER BY c.customer_state
    """
    return _read(sql)


def delivery_vs_review_by_category(top_n: int = 10) -> pd.DataFrame:
    sql = """
        SELECT p.category_en,
               CASE WHEN f.delay_days > 0 THEN 'late' ELSE 'on_time_or_early' END AS delivery,
               COUNT(*) AS items,
               ROUND(AVG(f.review_score), 2) AS avg_review
        FROM fact_sales f
        JOIN dim_product p      ON f.product_key = p.product_key
        JOIN dim_order_status s ON f.status_key = s.status_key
        WHERE s.order_status = 'delivered' AND f.delay_days IS NOT NULL
        GROUP BY p.category_en, delivery
        ORDER BY p.category_en
    """
    # Keep only the top_n categories by item volume for a readable chart.
    df = _read(sql)
    top_cats = (df.groupby("category_en")["items"].sum()
                  .sort_values(ascending=False).head(top_n).index)
    return df[df.category_en.isin(top_cats)]


def category_revenue_summary() -> pd.DataFrame:
    """Full-period revenue & items sold per category (no year filter) — used by
    src/dss/whatif.py as the baseline for the promotion-elasticity what-if."""
    sql = f"""
        SELECT p.category_en, ROUND(SUM(f.price), 2) AS revenue, COUNT(*) AS items_sold
        FROM fact_sales f
        JOIN dim_product p      ON f.product_key = p.product_key
        JOIN dim_order_status s ON f.status_key = s.status_key
        WHERE {_not_canceled_clause()}
        GROUP BY p.category_en
        ORDER BY revenue DESC
    """
    return _read(sql, CANCELED_STATUSES)


def delivery_late_rate() -> float:
    """% đơn giao trễ trong các đơn đã giao — baseline cho what-if giao trễ."""
    sql = """
        SELECT ROUND(100.0 * SUM(CASE WHEN f.delay_days > 0 THEN 1 ELSE 0 END) / COUNT(*), 4) AS pct_late
        FROM fact_sales f
        JOIN dim_order_status s ON f.status_key = s.status_key
        WHERE s.order_status = 'delivered' AND f.delay_days IS NOT NULL
    """
    return float(_read(sql).iloc[0]["pct_late"])


# --------------------------------------------------------------------------- DSS helpers (read-only raw extracts)
def monthly_revenue_series_for_forecast() -> pd.DataFrame:
    """Chuỗi doanh thu tháng 2017-01..2018-08, dùng làm input cho src/dss/forecast.py."""
    return monthly_revenue("2017-01", "2018-08")


def customer_order_history() -> pd.DataFrame:
    """1 dòng / đơn hàng: customer_key, purchase date, order revenue, avg review.
    Dùng làm input cho src/dss/rfm.py (R, F, M)."""
    sql = f"""
        SELECT f.customer_key,
               d.full_date AS purchase_date,
               f.order_id,
               SUM(f.price) AS order_value,
               AVG(f.review_score) AS avg_review
        FROM fact_sales f
        JOIN dim_date d         ON f.purchase_date_key = d.date_key
        JOIN dim_order_status s ON f.status_key = s.status_key
        WHERE {_not_canceled_clause()}
        GROUP BY f.customer_key, f.order_id, d.full_date
    """
    return _read(sql, CANCELED_STATUSES)
