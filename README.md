# Olist E-Commerce Data Warehouse & Decision Support System

Bài tập lớn môn **CO4031 – Kho dữ liệu và Hệ hỗ trợ Quyết định** (HK261, ĐH Bách Khoa TP.HCM).

Hệ thống gồm một kho dữ liệu đa chiều (star schema) xây từ bộ dữ liệu thương mại điện tử
[Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce),
quy trình ETL, các truy vấn OLAP, dashboard phân tích và thành phần hỗ trợ ra quyết định (DSS).

## Thành viên

| Thành viên | Vai trò |
|---|---|
| tamnguyen635 | **A – Data & DW**: thiết kế DW, ETL, OLAP |
| Vỹ | **B – Ứng dụng & DSS**: dashboard Streamlit, dự báo, phân khúc RFM, what-if |

## Kiến trúc

```
CSV (Olist) ──► ETL (Python/pandas) ──► SQLite DW (star schema) ──► OLAP queries
                                                   │
                                                   └──► Streamlit dashboard + DSS
```

## Cấu trúc thư mục

```
olist-dw-dss/
├── src/
│   ├── sql/        # DDL schema, truy vấn OLAP (SQL)
│   ├── etl/        # Script ETL: extract, transform, load
│   ├── olap/       # Truy vấn / hàm OLAP: slice, dice, drill-down, roll-up, pivot
│   ├── app/        # Dashboard Streamlit (frontend)
│   └── dss/        # Thành phần DSS: dự báo, RFM + K-Means, what-if
├── data/
│   ├── raw/        # CSV gốc Olist (KHÔNG commit, tải từ Kaggle)
│   └── processed/  # olist_dw.db sinh ra sau ETL (KHÔNG commit)
├── docs/           # Data contract, tài liệu thiết kế
├── notebooks/      # Notebook khám phá dữ liệu
├── report/         # Báo cáo PDF
└── slides/         # Slide thuyết trình PDF
```

## Cách chạy

```bash
# 1. Lấy code
git clone https://github.com/tamnguyen635/olist-dw-dss.git
cd olist-dw-dss

# 2. Môi trường (Python 3.10+)
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Đặt 8 file CSV vào data/raw/ (xem mục "Dữ liệu" bên dưới)

# 4. Chạy ETL -> tạo data/processed/olist_dw.db (~5 giây)
python src/etl/run_etl.py

# 5. (Tuỳ chọn) Xem kết quả các phép OLAP
python src/olap/olap_demo.py

# 6. Chạy dashboard (sẽ có khi phần Streamlit hoàn thiện)
streamlit run src/app/app.py
```

ETL tự chạy các kiểm tra chất lượng dữ liệu ở cuối. Nếu thấy dòng `FAIL` thì dừng lại và báo cho người phụ trách ETL.

## Dữ liệu

Tải **Brazilian E-Commerce Public Dataset by Olist** từ Kaggle (tìm theo tên trên kaggle.com) và đặt
các file CSV sau vào `data/raw/`:

```
olist_customers_dataset.csv
olist_orders_dataset.csv
olist_order_items_dataset.csv
olist_order_payments_dataset.csv
olist_order_reviews_dataset.csv
olist_products_dataset.csv
olist_sellers_dataset.csv
product_category_name_translation.csv
```

`olist_geolocation_dataset.csv` **không cần** cho dự án này. Dữ liệu thô và file `.db` không được commit
vì dung lượng lớn (xem `.gitignore`).

## Tài liệu

- [Data contract giữa A và B](docs/data_contract.md)
- [Schema kho dữ liệu](src/sql/01_schema.sql)
