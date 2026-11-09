# Data Contract (A -> B)

Người A (Data & DW) cam kết: file `data/olist_dw.db` (SQLite) luôn đúng schema trong `src/sql/01_schema.sql`.
Người B (Dashboard & DSS) chỉ đọc từ file này, không đọc CSV gốc.

## Star schema
fact_sales (grain: 1 dòng = 1 order item)
 ├─ dim_date (purchase_date_key, delivered_date_key)
 ├─ dim_customer
 ├─ dim_product
 ├─ dim_seller
 ├─ dim_payment_type
 └─ dim_order_status

## Measures
price, freight_value, item_total, payment_installments, review_score, delivery_days, delay_days

## Quy ước
- Doanh thu = SUM(item_total) hoặc SUM(price) (thống nhất dùng `price`; freight tách riêng).
- Chỉ tính đơn đã giao khi phân tích giao hàng: status = 'delivered'.
- Khoá ngày: INTEGER yyyymmdd. Join: fact_sales.purchase_date_key = dim_date.date_key.
- category_en = 'unknown' nếu thiếu danh mục.
- NULL có ý nghĩa: delivered_date_key, delivery_days, delay_days, review_score.

## Truy vấn mẫu
```sql
SELECT d.year_month, SUM(f.price) AS revenue
FROM fact_sales f JOIN dim_date d ON f.purchase_date_key = d.date_key
GROUP BY d.year_month ORDER BY d.year_month;
```
