-- ============================================================
-- OLAP operations on the Olist star schema (SQLite)
-- Convention: revenue = SUM(price); exclude canceled/unavailable orders
-- Each query is separated by a "-- name:" line so olap_demo.py can run them.
-- ============================================================

-- name: rollup_year
-- ROLL-UP: monthly -> yearly revenue
SELECT d.year, ROUND(SUM(f.price), 2) AS revenue, COUNT(DISTINCT f.order_id) AS orders
FROM fact_sales f
JOIN dim_date d         ON f.purchase_date_key = d.date_key
JOIN dim_order_status s ON f.status_key = s.status_key
WHERE s.order_status NOT IN ('canceled', 'unavailable')
GROUP BY d.year
ORDER BY d.year;

-- name: drilldown_month_2017
-- DRILL-DOWN: year 2017 -> quarter -> month
SELECT d.quarter, d.year_month, ROUND(SUM(f.price), 2) AS revenue
FROM fact_sales f
JOIN dim_date d         ON f.purchase_date_key = d.date_key
JOIN dim_order_status s ON f.status_key = s.status_key
WHERE d.year = 2017 AND s.order_status NOT IN ('canceled', 'unavailable')
GROUP BY d.quarter, d.year_month
ORDER BY d.year_month;

-- name: slice_year_2017_by_category
-- SLICE: fix time dimension (year = 2017), view revenue by product category (top 10)
SELECT p.category_en, ROUND(SUM(f.price), 2) AS revenue, COUNT(*) AS items_sold
FROM fact_sales f
JOIN dim_date d         ON f.purchase_date_key = d.date_key
JOIN dim_product p      ON f.product_key = p.product_key
JOIN dim_order_status s ON f.status_key = s.status_key
WHERE d.year = 2017 AND s.order_status NOT IN ('canceled', 'unavailable')
GROUP BY p.category_en
ORDER BY revenue DESC
LIMIT 10;

-- name: dice_sp_rj_top_categories
-- DICE: sub-cube = customer_state IN (SP, RJ) AND year 2018 AND 3 chosen categories
SELECT c.customer_state, p.category_en, ROUND(SUM(f.price), 2) AS revenue
FROM fact_sales f
JOIN dim_date d         ON f.purchase_date_key = d.date_key
JOIN dim_customer c     ON f.customer_key = c.customer_key
JOIN dim_product p      ON f.product_key = p.product_key
JOIN dim_order_status s ON f.status_key = s.status_key
WHERE c.customer_state IN ('SP', 'RJ')
  AND d.year = 2018
  AND p.category_en IN ('health_beauty', 'bed_bath_table', 'computers_accessories')
  AND s.order_status NOT IN ('canceled', 'unavailable')
GROUP BY c.customer_state, p.category_en
ORDER BY c.customer_state, revenue DESC;

-- name: pivot_category_by_year
-- PIVOT: categories as rows, years as columns (top categories)
SELECT p.category_en,
       ROUND(SUM(CASE WHEN d.year = 2016 THEN f.price END), 2) AS y2016,
       ROUND(SUM(CASE WHEN d.year = 2017 THEN f.price END), 2) AS y2017,
       ROUND(SUM(CASE WHEN d.year = 2018 THEN f.price END), 2) AS y2018,
       ROUND(SUM(f.price), 2) AS total
FROM fact_sales f
JOIN dim_date d         ON f.purchase_date_key = d.date_key
JOIN dim_product p      ON f.product_key = p.product_key
JOIN dim_order_status s ON f.status_key = s.status_key
WHERE s.order_status NOT IN ('canceled', 'unavailable')
GROUP BY p.category_en
ORDER BY total DESC
LIMIT 10;

-- name: revenue_by_state
-- Geographic analysis: revenue and average review score by customer state
SELECT c.customer_state,
       ROUND(SUM(f.price), 2)         AS revenue,
       COUNT(DISTINCT f.order_id)     AS orders,
       ROUND(AVG(f.review_score), 2)  AS avg_review
FROM fact_sales f
JOIN dim_customer c     ON f.customer_key = c.customer_key
JOIN dim_order_status s ON f.status_key = s.status_key
WHERE s.order_status NOT IN ('canceled', 'unavailable')
GROUP BY c.customer_state
ORDER BY revenue DESC
LIMIT 10;

-- name: payment_mix
-- Payment behaviour: share of revenue by main payment type
SELECT pt.payment_type,
       ROUND(SUM(f.price), 2) AS revenue,
       ROUND(100.0 * SUM(f.price) / (SELECT SUM(price) FROM fact_sales WHERE payment_type_key IS NOT NULL), 2) AS pct
FROM fact_sales f
JOIN dim_payment_type pt ON f.payment_type_key = pt.payment_type_key
GROUP BY pt.payment_type
ORDER BY revenue DESC;

-- name: delivery_vs_review
-- Delivery performance: late deliveries vs customer satisfaction (delivered orders only)
SELECT CASE WHEN f.delay_days > 0 THEN 'late' ELSE 'on_time_or_early' END AS delivery,
       COUNT(*) AS items,
       ROUND(AVG(f.delivery_days), 1) AS avg_delivery_days,
       ROUND(AVG(f.review_score), 2)  AS avg_review
FROM fact_sales f
JOIN dim_order_status s ON f.status_key = s.status_key
WHERE s.order_status = 'delivered' AND f.delay_days IS NOT NULL
GROUP BY delivery;
