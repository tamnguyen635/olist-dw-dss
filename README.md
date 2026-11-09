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

## Cách chạy (sẽ cập nhật khi code hoàn thiện)

```bash
# 1. Môi trường
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Đặt các file CSV Olist vào data/raw/

# 3. Chạy ETL -> tạo data/processed/olist_dw.db
python src/etl/run_etl.py

# 4. Chạy dashboard
streamlit run src/app/app.py
```

## Dữ liệu

Tải bộ **Brazilian E-Commerce Public Dataset by Olist** từ Kaggle và giải nén các file CSV vào `data/raw/`.
Dữ liệu và file `.db` không được commit vì dung lượng lớn.

## Tài liệu

- [Data contract giữa A và B](docs/data_contract.md)
- [Schema kho dữ liệu](src/sql/01_schema.sql)
