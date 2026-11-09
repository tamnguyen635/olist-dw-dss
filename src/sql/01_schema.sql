-- ============================================================
-- Olist E-Commerce Data Warehouse - Star Schema (SQLite)
-- Grain of fact_sales: ONE ROW PER ORDER ITEM (order_id + order_item_id)
-- ============================================================
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_seller;
DROP TABLE IF EXISTS dim_payment_type;
DROP TABLE IF EXISTS dim_order_status;

-- ---------- Dimensions ----------
CREATE TABLE dim_date (
    date_key      INTEGER PRIMARY KEY,      -- yyyymmdd, e.g. 20180315
    full_date     TEXT NOT NULL,            -- YYYY-MM-DD
    day           INTEGER NOT NULL,
    month         INTEGER NOT NULL,
    month_name    TEXT NOT NULL,
    quarter       INTEGER NOT NULL,
    year          INTEGER NOT NULL,
    year_month    TEXT NOT NULL,            -- YYYY-MM
    day_of_week   INTEGER NOT NULL,         -- 0=Mon .. 6=Sun
    day_name      TEXT NOT NULL,
    is_weekend    INTEGER NOT NULL          -- 0/1
);

CREATE TABLE dim_customer (
    customer_key        INTEGER PRIMARY KEY,
    customer_unique_id  TEXT NOT NULL UNIQUE,   -- real person (customer_id in Olist is per order)
    customer_city       TEXT,
    customer_state      TEXT,
    zip_code_prefix     TEXT
);

CREATE TABLE dim_product (
    product_key         INTEGER PRIMARY KEY,
    product_id          TEXT NOT NULL UNIQUE,
    category_pt         TEXT,
    category_en         TEXT,                   -- 'unknown' if missing
    name_length         INTEGER,
    description_length  INTEGER,
    photos_qty          INTEGER,
    weight_g            REAL,
    length_cm           REAL,
    height_cm           REAL,
    width_cm            REAL
);

CREATE TABLE dim_seller (
    seller_key       INTEGER PRIMARY KEY,
    seller_id        TEXT NOT NULL UNIQUE,
    seller_city      TEXT,
    seller_state     TEXT,
    zip_code_prefix  TEXT
);

CREATE TABLE dim_payment_type (
    payment_type_key  INTEGER PRIMARY KEY,
    payment_type      TEXT NOT NULL UNIQUE      -- credit_card, boleto, voucher, debit_card, not_defined
);

CREATE TABLE dim_order_status (
    status_key    INTEGER PRIMARY KEY,
    order_status  TEXT NOT NULL UNIQUE          -- delivered, shipped, canceled, ...
);

-- ---------- Fact ----------
CREATE TABLE fact_sales (
    sales_key            INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id             TEXT NOT NULL,          -- degenerate dimension
    order_item_id        INTEGER NOT NULL,
    purchase_date_key    INTEGER NOT NULL REFERENCES dim_date(date_key),
    delivered_date_key   INTEGER REFERENCES dim_date(date_key),   -- NULL if not delivered
    customer_key         INTEGER NOT NULL REFERENCES dim_customer(customer_key),
    product_key          INTEGER NOT NULL REFERENCES dim_product(product_key),
    seller_key           INTEGER NOT NULL REFERENCES dim_seller(seller_key),
    payment_type_key     INTEGER REFERENCES dim_payment_type(payment_type_key),  -- main payment type of the order
    status_key           INTEGER NOT NULL REFERENCES dim_order_status(status_key),
    -- measures
    price                REAL NOT NULL,
    freight_value        REAL NOT NULL,
    item_total           REAL NOT NULL,          -- price + freight_value
    payment_installments INTEGER,
    review_score         REAL,                   -- avg review score of the order, NULL if none
    delivery_days        REAL,                   -- delivered - purchase, NULL if not delivered
    delay_days           REAL,                   -- delivered - estimated (>0 = late), NULL if n/a
    UNIQUE (order_id, order_item_id)
);

-- ---------- Indexes for OLAP queries ----------
CREATE INDEX ix_fact_purchase_date ON fact_sales(purchase_date_key);
CREATE INDEX ix_fact_customer      ON fact_sales(customer_key);
CREATE INDEX ix_fact_product       ON fact_sales(product_key);
CREATE INDEX ix_fact_seller        ON fact_sales(seller_key);
CREATE INDEX ix_fact_status        ON fact_sales(status_key);
