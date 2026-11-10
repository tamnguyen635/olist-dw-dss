# Nhiệm vụ của Vỹ (Người B – Dashboard & DSS)

Dự án: **Olist E-Commerce DW & DSS** – BTL CO4031.
Repo: https://github.com/tamnguyen635/olist-dw-dss
**Hạn nộp: 23:59 Chủ nhật 15/11/2026** (nên nộp từ chiều 15/11, đừng sát giờ).

Phần của A (tamnguyen635) đã xong: star schema, ETL, OLAP, báo cáo phần A. Phần của Vỹ dùng lại DW đó để làm **dashboard** và **DSS**.

---

## 1. Việc cần làm ngay hôm nay (khoảng 20 phút)

1. A mời Vỹ vào repo (Settings → Collaborators). Vỹ nhận lời mời qua email GitHub.
2. A gửi cho Vỹ **8 file CSV** Olist (qua Zalo/Drive). Không cần file `olist_geolocation_dataset`.
3. Vỹ chạy:

```bash
git clone https://github.com/tamnguyen635/olist-dw-dss.git
cd olist-dw-dss
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# đặt 8 file CSV vào data/raw/
python src/etl/run_etl.py            # ~5 giây, tạo data/processed/olist_dw.db
python src/olap/olap_demo.py         # xem thử các truy vấn OLAP
```

Cuối ETL phải thấy các dòng `OK` và không có `FAIL`. File `.db` **không** nằm trên GitHub, mỗi người tự tạo bằng ETL.

---

## 2. Đọc trước khi code (15 phút)

- `docs/data_contract.md`: tên bảng, tên cột, quy ước.
- `report/figures/star_schema.pdf`: sơ đồ star schema.
- `src/sql/02_olap_queries.sql`: các truy vấn mẫu có thể tái sử dụng.

**Chỉ đọc từ `data/processed/olist_dw.db`, không đọc CSV gốc trong dashboard/DSS.**

---

## 3. Những điều về dữ liệu Vỹ cần biết (đã kiểm tra trên dữ liệu thật)

| Chủ đề | Thực tế | Hệ quả khi làm |
|---|---|---|
| Doanh thu | Quy ước `SUM(price)`; loại đơn `canceled`, `unavailable` | Dùng thống nhất, đừng tự đổi |
| Phạm vi thời gian | Bán hàng thực sự từ **2017-01 đến 2018-08** (20 tháng đủ). 2016 chỉ có 3 tháng rời rạc, 2018-09 chỉ có 1 đơn | Cắt chuỗi thời gian về 2017-01..2018-08 khi dự báo, nếu không mô hình bị nhiễu |
| Mùa vụ | Đỉnh **11/2017 ≈ 1,0 triệu** (Black Friday). Chưa có đủ 2 chu kỳ năm | Mô hình mùa vụ dễ sai, nêu rõ hạn chế trong báo cáo |
| Khách mua lại | Chỉ **2.913 / 95.420 khách (~3%)** có từ 2 đơn trở lên | **Frequency của RFM gần như luôn bằng 1** (xem mục 5.2) |
| Khách | Dùng `dim_customer.customer_key` (đã gộp theo người thật), không dùng `customer_id` | Không đếm trùng khách |
| Đánh giá | `review_score` có thể NULL (942 dòng) | `AVG` tự bỏ NULL, đừng điền 0 |
| Giao hàng | `delivery_days`, `delay_days` chỉ có khi đã giao | Lọc `order_status = 'delivered'` |
| Giao trễ | Trễ: điểm đánh giá TB **2,55** (8.714 dòng). Đúng hạn: **4,21** (101.475 dòng) | Phát hiện mạnh nhất, nên dùng cho what-if |
| Địa lý | SP ≈ 5,17 triệu / 13,5 triệu doanh thu; RJ có điểm TB thấp (3,82) so với SP (4,14) | Gợi ý nội dung cho trang địa lý |
| Thanh toán | Thẻ tín dụng ≈ 78,9% doanh thu, boleto 17,6% | Biểu đồ cơ cấu thanh toán |

Truy vấn lấy chuỗi doanh thu tháng (để bắt đầu dự báo):

```sql
SELECT d.year_month, SUM(f.price) AS revenue
FROM fact_sales f
JOIN dim_date d         ON f.purchase_date_key = d.date_key
JOIN dim_order_status s ON f.status_key = s.status_key
WHERE s.order_status NOT IN ('canceled', 'unavailable')
  AND d.year_month BETWEEN '2017-01' AND '2018-08'
GROUP BY d.year_month ORDER BY d.year_month;
```

---

## 4. Dashboard Streamlit – `src/app/app.py`

Chạy bằng `streamlit run src/app/app.py`. Đề xuất 4 trang (dùng `st.sidebar` để chọn trang):

1. **Tổng quan**: KPI (doanh thu, số đơn, giá trị đơn trung bình, điểm đánh giá TB, % giao trễ) và đường doanh thu theo tháng.
2. **Phân tích đa chiều (OLAP)**: bộ lọc năm / bang / danh mục. Thể hiện được **roll-up, drill-down (năm → quý → tháng), slice, dice, pivot** để chứng minh yêu cầu OLAP của đề bài.
3. **Địa lý & khách hàng**: doanh thu và điểm đánh giá theo bang; cơ cấu thanh toán.
4. **Giao hàng & hài lòng**: giao trễ ảnh hưởng điểm đánh giá thế nào, theo bang/danh mục.

Gợi ý kỹ thuật:
- Một hàm kết nối dùng chung, đường dẫn tính từ vị trí file để chạy được trên mọi máy:

```python
from pathlib import Path
import sqlite3, pandas as pd, streamlit as st

DB = Path(__file__).resolve().parents[2] / "data" / "processed" / "olist_dw.db"

@st.cache_data
def query(sql: str, params=()):
    with sqlite3.connect(DB) as con:
        return pd.read_sql_query(sql, con, params=params)
```

- Dùng `plotly.express` cho biểu đồ. Dùng tham số `?` trong SQL khi lọc, không nối chuỗi.
- Tách code: `src/app/app.py` (giao diện), `src/app/queries.py` (các câu SQL). Có thể tái dùng câu SQL trong `src/sql/02_olap_queries.sql`.

---

## 5. Thành phần DSS – `src/dss/`

Đề bài yêu cầu **ít nhất một thành phần DSS** dựa trên kho dữ liệu. Làm cả 3 phần dưới đây nếu kịp, tối thiểu phải có (5.1) và (5.3).

### 5.1 Dự báo doanh thu – `src/dss/forecast.py`
- Dữ liệu: chuỗi tháng 2017-01..2018-08 (20 điểm).
- Chia train/test (ví dụ giữ 3–4 tháng cuối để kiểm tra).
- So sánh ít nhất 2 mô hình: baseline (naive hoặc trung bình trượt) và Holt-Winters / hồi quy xu hướng (`statsmodels`).
- Báo cáo sai số **MAE và MAPE** trên tập test. Vẽ thực tế vs dự báo và khoảng tin cậy.
- Đừng quảng cáo quá mức: chuỗi ngắn, chưa đủ 2 chu kỳ mùa vụ. Nói rõ điều này là một hạn chế.

### 5.2 Phân khúc khách hàng RFM + K-Means – `src/dss/rfm.py`
- R = số ngày từ lần mua gần nhất đến ngày tham chiếu (ví dụ 2018-09-03), M = tổng chi tiêu.
- **Bẫy:** chỉ ~3% khách mua lại, nên F gần như luôn bằng 1. Nếu chia phân vị F (`qcut`) sẽ lỗi hoặc vô nghĩa. Cách xử lý: dùng F nhị phân (1 đơn / ≥2 đơn), hoặc thay F bằng điểm đánh giá TB / số sản phẩm mua. Ghi rõ lựa chọn này trong báo cáo, vì thầy rất dễ hỏi.
- Chuẩn hóa dữ liệu (`StandardScaler`), chọn K = 3–4 bằng elbow + silhouette, đặt tên cho từng nhóm (ví dụ "Khách giá trị cao", "Khách mới", "Khách ngủ đông") và đề xuất hành động cho mỗi nhóm.

### 5.3 Mô hình what-if – `src/dss/whatif.py` (+ một trang trong dashboard)
Người dùng kéo thanh trượt, hệ thống tính lại kết quả. Hai gợi ý:
- **Giảm giao trễ → điểm hài lòng.** Dựa trên số liệu thật (trễ 2,55 vs đúng hạn 4,21): "nếu giảm tỷ lệ giao trễ từ x% xuống y% thì điểm đánh giá TB thay đổi bao nhiêu?"
- **Khuyến mãi theo danh mục → doanh thu.** Người dùng nhập mức giảm giá và độ co giãn của cầu. Đây là **giả định** do người dùng đặt, phải ghi chú rõ trên giao diện, không trình bày như dự đoán chắc chắn.

---

## 6. Cấu trúc file đề xuất (Vỹ chỉ sửa trong `src/app/` và `src/dss/`)

```
src/
├── app/
│   ├── app.py
│   └── queries.py
└── dss/
    ├── forecast.py
    ├── rfm.py
    └── whatif.py
```

Nếu cần thêm cột hay đổi schema (`01_schema.sql`, `run_etl.py`), **nhắn A sửa**, đừng tự sửa để tránh xung đột và làm hỏng data contract.

---

## 7. Quy tắc làm việc với Git

- Trước khi làm: `git pull`. Commit nhỏ, thông điệp rõ (ví dụ `Add monthly revenue forecast with Holt-Winters`).
- Commit bằng **tài khoản GitHub cá nhân của Vỹ**. Lịch sử commit là bằng chứng đóng góp khi chấm điểm cá nhân.
- **Không commit** `data/raw/*` và `*.db` (đã chặn trong `.gitignore`).
- A làm `src/etl`, `src/olap`, `src/sql`, `report/part_A_*`; Vỹ làm `src/app`, `src/dss`, `report/part_B_*`. Hai bên không sửa file của nhau thì sẽ không xung đột.

---

## 8. Báo cáo phần B

Báo cáo phần A viết bằng LaTeX (`report/part_A_dw.tex`, biên dịch bằng **xelatex** hai lần). Phần B nên theo cùng định dạng để ghép dễ: tạo `report/part_B_dss.tex` với các mục:

1. Kiến trúc dashboard và DSS.
2. Dashboard: ảnh chụp từng trang, các chức năng OLAP đã có.
3. Mô hình DSS: dữ liệu vào, phương pháp, tham số, kết quả (có số liệu thật).
4. Đánh giá (MAE/MAPE, silhouette, v.v.).
5. Hạn chế và hướng phát triển.

Hai bạn cùng viết chung: Giới thiệu, Kết luận, Tài liệu tham khảo.

---

## 9. Thuyết trình (15 phút + 5 phút Q&A)

Vỹ trình bày phần **Dashboard + DSS + demo** (khoảng 7–8 phút). **Mọi thành viên đều phải trình bày**, người không trình bày sẽ bị trừ điểm hoặc không được tính điểm.
- Chuẩn bị demo chạy trên máy cá nhân, **quay sẵn video demo dự phòng** phòng khi lỗi.
- Hiểu cả phần của A (star schema, ETL, quyết định thiết kế) để trả lời Q&A, và A cũng cần hiểu phần của Vỹ.

---

## 10. Lịch làm việc

| Ngày | Vỹ | A |
|---|---|---|
| **Thứ Ba 10/11** | Cài môi trường, chạy ETL, đọc data contract, dựng khung dashboard | Gửi CSV, mời vào repo, hỗ trợ khi Vỹ cần |
| **Thứ Tư 11/11** | Hoàn thành trang Tổng quan + OLAP + dự báo | Soạn slide phần A, chuẩn bị Q&A |
| **Thứ Năm 12/11** | RFM + K-Means, what-if, các trang còn lại | Hoàn thiện báo cáo chung (bìa, mở đầu, kết luận) |
| **Thứ Sáu 13/11** | **Tích hợp, chạy thử toàn hệ thống, sửa lỗi** (cả hai) | |
| **Thứ Bảy 14/11** | Viết báo cáo phần B, làm slide phần B | Ghép báo cáo, kiểm tra PDF |
| **Chủ nhật 15/11** | Quay/tập thuyết trình, đóng gói, **nộp trước chiều** | |

---

## 11. Tiêu chí hoàn thành (Vỹ tự kiểm tra)

- [ ] `streamlit run src/app/app.py` chạy được trên máy sạch sau khi làm theo README.
- [ ] Dashboard có đủ roll-up, drill-down, slice, dice, pivot.
- [ ] Ít nhất 1 thành phần DSS chạy được, có đánh giá bằng số liệu, và hạn chế được nêu rõ.
- [ ] Các giả định (độ co giãn, dữ liệu ngắn…) được ghi chú trên giao diện và trong báo cáo.
- [ ] Báo cáo phần B và slide phần B xong.
- [ ] Code đã push lên GitHub, commit dưới tên Vỹ.
- [ ] Có video demo dự phòng.

Nếu bị kẹt hoặc cần đổi schema: nhắn A ngay, đừng chờ đến ngày 13/11.
