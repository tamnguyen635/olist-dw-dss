"""
ETL: Olist CSV  ->  SQLite star schema (see src/sql/01_schema.sql)

Usage (from repo root):
    python src/etl/run_etl.py
    python src/etl/run_etl.py --raw data/raw --db data/processed/olist_dw.db

Pipeline:
    1. EXTRACT   : read the 8 CSV files (all as string to keep zip-code leading zeros)
    2. TRANSFORM : clean, de-duplicate, build dimensions + fact, compute measures
    3. LOAD      : create schema, bulk insert, run data-quality checks
"""
import argparse
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]

# Two categories exist in products but not in the translation file.
EXTRA_TRANSLATION = {
    "pc_gamer": "pc_gamer",
    "portateis_cozinha_e_preparadores_de_alimentos": "portable_kitchen_food_preparers",
}


# ----------------------------------------------------------------- EXTRACT
def extract(raw: Path) -> dict:
    names = {
        "customers": "olist_customers_dataset",
        "orders": "olist_orders_dataset",
        "items": "olist_order_items_dataset",
        "payments": "olist_order_payments_dataset",
        "reviews": "olist_order_reviews_dataset",
        "products": "olist_products_dataset",
        "sellers": "olist_sellers_dataset",
        "translation": "product_category_name_translation",
    }
    missing = [f"{v}.csv" for v in names.values() if not (raw / f"{v}.csv").exists()]
    if missing:
        raise SystemExit(
            f"Missing CSV file(s) in {raw}:\n  " + "\n  ".join(missing) +
            "\nDownload the Olist dataset from Kaggle and put the CSVs in data/raw/ "
            "(olist_geolocation_dataset.csv is NOT needed).")
    data = {k: pd.read_csv(raw / f"{v}.csv", dtype=str) for k, v in names.items()}
    for k, df in data.items():
        print(f"[extract] {k:<12} {len(df):>9,} rows")
    return data


# --------------------------------------------------------------- TRANSFORM
def build_dim_date(dates: pd.Series) -> pd.DataFrame:
    rng = pd.date_range(dates.min().normalize(), dates.max().normalize(), freq="D")
    d = pd.DataFrame({"full_date": rng})
    d["date_key"] = d.full_date.dt.strftime("%Y%m%d").astype(int)
    d["day"] = d.full_date.dt.day
    d["month"] = d.full_date.dt.month
    d["month_name"] = d.full_date.dt.month_name()
    d["quarter"] = d.full_date.dt.quarter
    d["year"] = d.full_date.dt.year
    d["year_month"] = d.full_date.dt.strftime("%Y-%m")
    d["day_of_week"] = d.full_date.dt.dayofweek
    d["day_name"] = d.full_date.dt.day_name()
    d["is_weekend"] = (d.day_of_week >= 5).astype(int)
    d["full_date"] = d.full_date.dt.strftime("%Y-%m-%d")
    return d[["date_key", "full_date", "day", "month", "month_name", "quarter",
              "year", "year_month", "day_of_week", "day_name", "is_weekend"]]


def transform(data: dict) -> dict:
    orders = data["orders"].copy()
    for col in ["order_purchase_timestamp", "order_delivered_customer_date",
                "order_estimated_delivery_date"]:
        orders[col] = pd.to_datetime(orders[col], errors="coerce")

    # ---- dim_customer: one row per real person (customer_unique_id) ----
    cust = data["customers"].merge(
        orders[["customer_id", "order_purchase_timestamp"]], on="customer_id", how="left")
    # a person may appear with several customer_id / locations -> keep the most recent one
    cust = cust.sort_values("order_purchase_timestamp").drop_duplicates("customer_unique_id", keep="last")
    dim_customer = cust[["customer_unique_id", "customer_city", "customer_state",
                         "customer_zip_code_prefix"]].rename(
        columns={"customer_zip_code_prefix": "zip_code_prefix"}).sort_values("customer_unique_id")
    dim_customer.insert(0, "customer_key", range(1, len(dim_customer) + 1))
    # customer_id (per order) -> customer_key (per person)
    cust_map = data["customers"][["customer_id", "customer_unique_id"]].merge(
        dim_customer[["customer_key", "customer_unique_id"]], on="customer_unique_id")[["customer_id", "customer_key"]]

    # ---- dim_product ----
    tr = dict(zip(data["translation"].product_category_name,
                  data["translation"].product_category_name_english))
    tr.update(EXTRA_TRANSLATION)
    prod = data["products"].rename(columns={
        "product_category_name": "category_pt",
        "product_name_lenght": "name_length",
        "product_description_lenght": "description_length",
        "product_photos_qty": "photos_qty",
        "product_weight_g": "weight_g",
        "product_length_cm": "length_cm",
        "product_height_cm": "height_cm",
        "product_width_cm": "width_cm"}).copy()
    prod["category_en"] = prod.category_pt.map(tr).fillna("unknown")
    for c in ["name_length", "description_length", "photos_qty"]:
        prod[c] = pd.to_numeric(prod[c], errors="coerce").astype("Int64")
    for c in ["weight_g", "length_cm", "height_cm", "width_cm"]:
        prod[c] = pd.to_numeric(prod[c], errors="coerce")
    dim_product = prod[["product_id", "category_pt", "category_en", "name_length", "description_length",
                        "photos_qty", "weight_g", "length_cm", "height_cm", "width_cm"]].sort_values("product_id")
    dim_product.insert(0, "product_key", range(1, len(dim_product) + 1))

    # ---- dim_seller ----
    dim_seller = data["sellers"].rename(columns={
        "seller_zip_code_prefix": "zip_code_prefix"}).sort_values("seller_id")
    dim_seller.insert(0, "seller_key", range(1, len(dim_seller) + 1))

    # ---- dim_payment_type / dim_order_status ----
    pay = data["payments"].copy()
    pay["payment_value"] = pd.to_numeric(pay.payment_value)
    pay["payment_installments"] = pd.to_numeric(pay.payment_installments)
    dim_payment_type = pd.DataFrame({"payment_type": sorted(pay.payment_type.unique())})
    dim_payment_type.insert(0, "payment_type_key", range(1, len(dim_payment_type) + 1))
    dim_order_status = pd.DataFrame({"order_status": sorted(orders.order_status.unique())})
    dim_order_status.insert(0, "status_key", range(1, len(dim_order_status) + 1))

    # ---- order-level helpers ----
    # main payment = payment row with the largest value in the order
    main_pay = (pay.sort_values(["order_id", "payment_value"], ascending=[True, False])
                   .drop_duplicates("order_id")[["order_id", "payment_type", "payment_installments"]])
    main_pay = main_pay.merge(dim_payment_type, on="payment_type")[
        ["order_id", "payment_type_key", "payment_installments"]]
    # review score = mean of all reviews of the order
    rev = data["reviews"].copy()
    rev["review_score"] = pd.to_numeric(rev.review_score)
    rev_score = rev.groupby("order_id", as_index=False).review_score.mean()

    # ---- fact_sales: grain = order item ----
    f = data["items"].copy()
    f["order_item_id"] = f.order_item_id.astype(int)
    f["price"] = pd.to_numeric(f.price)
    f["freight_value"] = pd.to_numeric(f.freight_value)
    f["item_total"] = f.price + f.freight_value
    f = (f.merge(orders[["order_id", "customer_id", "order_status", "order_purchase_timestamp",
                         "order_delivered_customer_date", "order_estimated_delivery_date"]], on="order_id")
          .merge(cust_map, on="customer_id")
          .merge(dim_product[["product_key", "product_id"]], on="product_id")
          .merge(dim_seller[["seller_key", "seller_id"]], on="seller_id")
          .merge(dim_order_status, on="order_status")
          .merge(main_pay, on="order_id", how="left")
          .merge(rev_score, on="order_id", how="left"))

    f["purchase_date_key"] = f.order_purchase_timestamp.dt.strftime("%Y%m%d").astype(int)
    deliv = f.order_delivered_customer_date
    f["delivered_date_key"] = deliv.dt.strftime("%Y%m%d").astype("Float64").astype("Int64")
    f["delivery_days"] = (deliv - f.order_purchase_timestamp).dt.total_seconds() / 86400
    f["delay_days"] = (deliv - f.order_estimated_delivery_date).dt.total_seconds() / 86400
    f["payment_type_key"] = f.payment_type_key.astype("Int64")
    f["payment_installments"] = f.payment_installments.astype("Int64")

    # dim_date covers every date used by the fact (purchase + delivery)
    all_dates = pd.concat([f.order_purchase_timestamp, deliv.dropna()])
    dim_date = build_dim_date(all_dates)

    fact_sales = f[["order_id", "order_item_id", "purchase_date_key", "delivered_date_key",
                    "customer_key", "product_key", "seller_key", "payment_type_key", "status_key",
                    "price", "freight_value", "item_total", "payment_installments",
                    "review_score", "delivery_days", "delay_days"]].sort_values(["order_id", "order_item_id"])

    print(f"[transform] orders skipped (no items): {(~orders.order_id.isin(data['items'].order_id)).sum():,}")
    return dict(dim_date=dim_date, dim_customer=dim_customer, dim_product=dim_product,
                dim_seller=dim_seller, dim_payment_type=dim_payment_type,
                dim_order_status=dim_order_status, fact_sales=fact_sales)


# -------------------------------------------------------------------- LOAD
def load(tables: dict, db: Path, schema: Path) -> None:
    db.parent.mkdir(parents=True, exist_ok=True)
    if db.exists():
        db.unlink()
    con = sqlite3.connect(db)
    con.executescript(schema.read_text(encoding="utf-8"))
    # dimensions first, fact last (foreign keys)
    for name in ["dim_date", "dim_customer", "dim_product", "dim_seller",
                 "dim_payment_type", "dim_order_status", "fact_sales"]:
        df = tables[name].astype(object).where(tables[name].notna(), None)
        cols = list(df.columns)
        con.executemany(
            f"INSERT INTO {name} ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})",
            df.itertuples(index=False, name=None))
        print(f"[load] {name:<18} {len(df):>9,} rows")
    con.commit()
    quality_checks(con)
    con.close()


def quality_checks(con: sqlite3.Connection) -> None:
    print("\n[quality checks]")
    q = lambda sql: con.execute(sql).fetchone()[0]
    checks = {
        "fact rows == order_items rows (112,650)": q("SELECT COUNT(*) FROM fact_sales") == 112650,
        "no orphan customer_key": q("SELECT COUNT(*) FROM fact_sales f LEFT JOIN dim_customer d USING(customer_key) WHERE d.customer_key IS NULL") == 0,
        "no orphan product_key": q("SELECT COUNT(*) FROM fact_sales f LEFT JOIN dim_product d USING(product_key) WHERE d.product_key IS NULL") == 0,
        "no orphan seller_key": q("SELECT COUNT(*) FROM fact_sales f LEFT JOIN dim_seller d USING(seller_key) WHERE d.seller_key IS NULL") == 0,
        "no orphan purchase_date_key": q("SELECT COUNT(*) FROM fact_sales f LEFT JOIN dim_date d ON f.purchase_date_key=d.date_key WHERE d.date_key IS NULL") == 0,
        "no orphan delivered_date_key": q("SELECT COUNT(*) FROM fact_sales f LEFT JOIN dim_date d ON f.delivered_date_key=d.date_key WHERE f.delivered_date_key IS NOT NULL AND d.date_key IS NULL") == 0,
        "no negative price": q("SELECT COUNT(*) FROM fact_sales WHERE price < 0") == 0,
        "item_total = price + freight": q("SELECT COUNT(*) FROM fact_sales WHERE ABS(item_total-price-freight_value) > 0.001") == 0,
    }
    for name, ok in checks.items():
        print(f"  {'OK  ' if ok else 'FAIL'} {name}")
    print("\n  SUM(price) =", round(q("SELECT SUM(price) FROM fact_sales"), 2))
    print("  distinct orders =", q("SELECT COUNT(DISTINCT order_id) FROM fact_sales"))
    print("  NULL review_score =", q("SELECT COUNT(*) FROM fact_sales WHERE review_score IS NULL"))
    print("  NULL payment_type_key =", q("SELECT COUNT(*) FROM fact_sales WHERE payment_type_key IS NULL"))
    print("  category 'unknown' products =", q("SELECT COUNT(*) FROM dim_product WHERE category_en='unknown'"))
    if not all(checks.values()):
        raise SystemExit("Data quality checks FAILED")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", type=Path, default=REPO / "data" / "raw")
    ap.add_argument("--db", type=Path, default=REPO / "data" / "processed" / "olist_dw.db")
    ap.add_argument("--schema", type=Path, default=REPO / "src" / "sql" / "01_schema.sql")
    a = ap.parse_args()
    load(transform(extract(a.raw)), a.db, a.schema)
    print(f"\nDone -> {a.db}")


if __name__ == "__main__":
    main()
