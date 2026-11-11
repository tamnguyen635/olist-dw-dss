# Phần B – Dashboard & DSS (Vỹ) — Outline thuyết trình (~7–8 phút / ~450 giây)

> Dùng cho phần nói, không phải slide hoàn chỉnh. Mỗi slide: tiêu đề, nội dung trên slide (ngắn gọn), và "nói gì" (speaker notes).
> Số liệu lấy từ chạy thực tế ngày hôm nay (sau `python src/etl/run_etl.py`):
> - `python src/dss/forecast.py`, `python src/dss/rfm.py`, `python src/dss/whatif.py`
> - `queries.kpi_summary()`, `queries.payment_mix()`, `queries.revenue_review_by_state()`

Tổng thời lượng mục tiêu: **450 giây (7.5 phút)**, còn lại 30–90s làm đệm/chuyển giao giữa các phần A→B.

---

## Slide 1 — Tiêu đề (25s)

**Nội dung slide:**
- Olist E-Commerce: Dashboard & DSS trên Data Warehouse
- CO4031 – BTL Kho dữ liệu & Hệ hỗ trợ ra quyết định
- Người trình bày: Vỹ (Phần B) — Dashboard, DSS, Demo

**Speaker notes:** Chào thầy và các bạn, em là Vỹ, phụ trách phần Dashboard, các mô hình hỗ trợ ra quyết định (DSS), và sẽ demo trực tiếp hệ thống.

---

## Slide 2 — Kiến trúc tổng quan (40s)

**Nội dung slide:**
- Phần A: ETL → Star schema (`olist_dw.db`) — đã có đủ fact_sales + các dim
- Phần B: Dashboard Streamlit + 3 mô hình DSS, **chỉ đọc từ DB đã xử lý**, không đụng CSV gốc
- Tách lớp rõ ràng: `src/app/queries.py` (SQL) ↔ `src/app/app.py` (giao diện) ↔ `src/dss/*.py` (mô hình)
- Toàn bộ query dùng tham số `?`, không nối chuỗi SQL

**Speaker notes:** Em kế thừa nguyên star schema anh A đã xây — không đổi schema, không đọc lại CSV thô. Dashboard và DSS đều lấy dữ liệu qua một lớp `queries.py` duy nhất để đảm bảo nhất quán và tránh SQL injection.

---

## Slide 3 — Dashboard: Tổng quan & OLAP (70s)

**Nội dung slide:**
- Trang Tổng quan: 5 KPI — Doanh thu **13.49 triệu**, 98.199 đơn, giá trị đơn TB **137.42**, điểm đánh giá TB **4.04**, % giao trễ **7.91%**
- Trang OLAP có đủ 5 thao tác:
  - **Roll-up**: tháng → năm
  - **Drill-down**: năm → quý → tháng
  - **Slice**: cố định năm, xem theo danh mục
  - **Dice**: chọn nhiều bang × nhiều danh mục
  - **Pivot**: danh mục × năm

**Speaker notes:** Trang Tổng quan cho cái nhìn nhanh bằng 5 chỉ số KPI tính trực tiếp từ fact_sales. Trang OLAP là phần chứng minh yêu cầu đa chiều của đề bài — em làm đủ cả roll-up, drill-down, slice, dice và pivot, mỗi thao tác có một SQL riêng trong `queries.py`, có chú thích rõ loại thao tác OLAP tương ứng.

---

## Slide 4 — Dashboard: Địa lý/khách hàng & Giao hàng (50s)

**Nội dung slide:**
- Doanh thu & điểm đánh giá theo bang: SP dẫn đầu (**~5.17 triệu**, review TB 4.14), RJ review TB thấp hơn (**3.82**)
- Cơ cấu thanh toán: thẻ tín dụng **78.9%**, boleto **17.6%**
- Trang Giao hàng: so sánh điểm đánh giá giữa đơn **giao trễ** và **đúng hạn/sớm**

**Speaker notes:** Trang địa lý cho thấy SP vừa là bang doanh thu lớn nhất vừa có đánh giá tốt, trong khi RJ doanh thu cao thứ hai nhưng đánh giá thấp hơn hẳn — đây là gợi ý cho đội vận hành logistics. Thanh toán thì thẻ tín dụng chiếm gần 4/5 doanh thu.

---

## Slide 5 — DSS 1: Dự báo doanh thu (55s)

**Nội dung slide:**
- Dữ liệu: chuỗi doanh thu tháng **2017-01 → 2018-08** (20 điểm), train 16 tháng / test 4 tháng cuối
- So sánh 2 mô hình: **Baseline (trung bình trượt 3 tháng)** vs **Holt (xu hướng tuyến tính, không mùa vụ)**
- Kết quả trên tập test: Baseline MAE **69.432**, MAPE **7.85%** — Holt MAE **281.179**, MAPE **32.24%**
- **→ Baseline tốt hơn Holt** vì doanh thu chững lại sau đỉnh Black Friday 11/2017, Holt ngoại suy xu hướng tăng nên dự báo vượt thực tế
- Hạn chế: chuỗi quá ngắn, chưa đủ 2 chu kỳ mùa vụ → không dùng Holt-Winters mùa vụ

**Speaker notes:** Em thử nghiệm nghiêm túc chứ không chỉ chạy cho có — và kết quả thật là mô hình Holt có xu hướng lại sai nhiều hơn baseline đơn giản, vì nó ngoại suy đà tăng trước Black Friday trong khi thực tế doanh thu chững lại. Em báo cáo trung thực điều này trong dashboard bằng một cảnh báo rõ ràng, thay vì tô hồng kết quả.

---

## Slide 6 — DSS 2: Phân khúc RFM + K-Means (60s)

**Nội dung slide:**
- **Bẫy dữ liệu:** chỉ ~3% khách (2.913/95.420) mua lại → Frequency cổ điển gần như luôn = 1, không chia phân vị được
- **Xử lý:** thay F bằng (1) cờ nhị phân mua lại (repeat_flag) + (2) điểm đánh giá TB; giữ Recency, Monetary
- Chuẩn hóa `StandardScaler`, chọn K bằng elbow + silhouette → **K = 3** (silhouette = **0.411**)
- 3 phân khúc thật: **Khách giá trị cao** (2.891 khách, 3.0%, review TB 4.17, gần như 100% mua lại) · **Khách mới** (71.792 khách, 75.6%, review TB 4.75) · **Khách ngủ đông** (20.300 khách, 21.4%, review TB 1.89)

**Speaker notes:** Đây là phần thầy rất hay hỏi nên em nhấn mạnh: với dữ liệu Olist, Frequency kiểu RFM cổ điển vô nghĩa vì gần hết khách chỉ mua một lần. Em thay bằng cờ mua lại nhị phân và điểm đánh giá trung bình — hai biến này vẫn tách được rõ ba nhóm khách có hành vi khác nhau, với silhouette 0.411 ở K=3, mỗi nhóm có hành động đề xuất riêng.

---

## Slide 7 — DSS 3: Mô hình What-if (55s)

**Nội dung slide:**
- **What-if 1 (dựa số liệu thật):** Giao trễ hiện tại **7.91%**, review TB trễ **2.55** vs đúng hạn **4.21**
  - Ví dụ: giảm trễ 7.91% → 1.91% ⇒ review TB dự kiến tăng từ ~4.08 lên **4.18 (+0.10)**
  - Nếu về 0% trễ: review TB dự kiến **4.21 (+0.13)**
- **What-if 2 (GIẢ ĐỊNH người dùng nhập):** khuyến mãi theo danh mục, độ co giãn cầu tự nhập
  - Ví dụ danh mục *health_beauty* (DT nền 1.255.695): giảm giá 10% + co giãn 2.0 → doanh thu dự kiến **+8.00%**; giảm giá 10% + co giãn 1.0 → **-1.00%**
  - Giao diện ghi rõ: đây là giả định, KHÔNG phải dự báo chắc chắn

**Speaker notes:** What-if đầu dựa trên mối quan hệ đo được thật trong DW nên đáng tin hơn — là phép nội suy trọng số giữa hai mức review đã quan sát. What-if thứ hai thì độ co giãn do người dùng tự đặt, nên em ghi cảnh báo ngay trên UI để không ai hiểu nhầm đó là số liệu đo được.

---

## Slide 8 — Demo trực tiếp / video dự phòng (60s)

**Nội dung slide:**
- Lệnh chạy: `streamlit run src/app/app.py`
- Luồng demo: Tổng quan → OLAP (drill-down + dice) → DSS (forecast → RFM → what-if giao trễ)
- Có video quay sẵn dự phòng nếu máy/mạng lỗi

**Ghi chú chuẩn bị (không đọc hết trên slide, nhắc miệng):**
- Test `streamlit run` trên máy sẽ demo **trước** buổi thuyết trình, không thử lần đầu trên lớp
- Đóng các app nặng khác, tắt notification, kiểm tra DB đã build (`data/processed/olist_dw.db` tồn tại)
- Chuẩn bị sẵn 2-3 lựa chọn bang/danh mục cho phần dice để demo mượt
- Quay video demo đầy đủ luồng (khoảng 1-2 phút) trước, để mở ngay nếu live demo lỗi

**Speaker notes:** Bây giờ em demo trực tiếp Dashboard — em sẽ đi nhanh qua 4 trang rồi dừng ở DSS. Nếu có sự cố kỹ thuật, em có video dự phòng đã quay sẵn.

---

## Slide 9 — Hạn chế & hướng phát triển (40s)

**Nội dung slide:**
- Chuỗi thời gian ngắn (20 tháng) → forecast chưa bắt được mùa vụ, Holt hiện kém hơn baseline
- RFM: F thay thế không phải F chuẩn, cần thêm dữ liệu hành vi (số lần xem, giỏ hàng...) nếu có
- What-if khuyến mãi dựa trên giả định co giãn do người dùng nhập, chưa phải mô hình học từ dữ liệu
- Hướng phát triển: thêm dữ liệu các năm sau để làm forecast mùa vụ đầy đủ; thử mô hình phân loại dự đoán nguy cơ giao trễ; kết nối dashboard với dữ liệu realtime

**Speaker notes:** Em không muốn phóng đại kết quả. Những hạn chế này đều xuất phát từ đặc điểm dữ liệu Olist chứ không phải lỗi thực hiện, và em đã nêu rõ trong cả báo cáo lẫn giao diện.

---

## Slide 10 — Kết / Chuẩn bị Q&A (55s)

**Nội dung slide:**
- Tóm tắt: Dashboard đủ 5 OLAP + 3 thành phần DSS, đều có đánh giá bằng số liệu thật và hạn chế rõ ràng
- Cảm ơn thầy/các bạn — sẵn sàng trả lời câu hỏi

**Câu hỏi Q&A dự kiến + trả lời ngắn:**
1. **Tại sao F trong RFM gần như luôn = 1, xử lý thế nào?**
   → Chỉ ~3% khách (2.913/95.420) mua lại; nếu `qcut` F sẽ lỗi/vô nghĩa. Em thay F bằng cờ nhị phân mua lại + điểm đánh giá TB, vẫn tách được 3 nhóm rõ với silhouette 0.411.
2. **Tại sao không dùng Holt-Winters mùa vụ để dự báo?**
   → Chuỗi chỉ 20 tháng (2017-01..2018-08), chưa đủ 2 chu kỳ năm để ước lượng tham số mùa vụ đáng tin cậy. Em dùng Holt tuyến tính (không mùa vụ) và baseline trung bình trượt để so sánh trung thực — thực tế Holt hiện có MAPE (32.24%) cao hơn baseline (7.85%) vì nó ngoại suy đà tăng trước Black Friday.
3. **Mô hình what-if khuyến mãi có đáng tin không?**
   → Không phải dự báo đo được — độ co giãn cầu do người dùng tự nhập, chỉ mang tính minh họa kịch bản. Giao diện ghi cảnh báo rõ ràng mỗi lần hiển thị kết quả.
4. **Dashboard có đang đọc trực tiếp CSV không, có tốn hiệu năng không?**
   → Không, dashboard chỉ đọc từ `data/processed/olist_dw.db` (SQLite đã qua ETL) qua `queries.py`, dùng `st.cache_data` để cache kết quả query.
5. **(Câu hỏi chéo về phần A)** Vì sao chọn star schema / quy ước doanh thu `SUM(price)` loại trừ `canceled`/`unavailable`?
   → (Vỹ trả lời ở mức hiểu được): Star schema giúp truy vấn OLAP nhanh và trực quan hơn snowflake cho khối lượng dữ liệu này; quy ước doanh thu loại đơn hủy/không có hàng để tránh đếm doanh thu ảo — quy ước này được dùng thống nhất xuyên suốt dashboard và DSS.

**Speaker notes:** Em xin tóm tắt lại: dashboard đáp ứng đủ yêu cầu OLAP, ba thành phần DSS đều chạy được với số liệu đánh giá thật và hạn chế được nêu rõ, không phóng đại. Em sẵn sàng trả lời câu hỏi của thầy và các bạn.

---

### Kiểm tra tổng thời lượng
25 + 40 + 70 + 50 + 55 + 60 + 55 + 60 + 40 + 55 = **510s** trên outline chi tiết, nhưng phần demo (slide 8) sẽ được rút gọn linh hoạt khi tập luyện — mục tiêu thực tế khi nói nhanh/tự nhiên là ~**450s (7.5 phút)**, dưới mức trần 8 phút của đề bài. Luyện tập để cắt bớt phần đọc bullet, ưu tiên nói từ speaker notes.

---

## Checklist chuẩn bị trước khi thuyết trình

(Theo mục 9 và 11 của `docs/TASKS_VY.md`)

- [ ] `streamlit run src/app/app.py` chạy được trên máy sạch, test lại **trước** ngày thuyết trình, không thử lần đầu trên lớp
- [ ] Chạy thử toàn bộ luồng demo (Tổng quan → OLAP → Địa lý → Giao hàng → DSS) ít nhất 1 lần đúng kịch bản sẽ trình bày
- [ ] **Quay sẵn video demo dự phòng** (phòng khi máy/mạng lỗi lúc thuyết trình thật) — theo đúng mục 9 TASKS_VY.md
- [ ] Hiểu cả phần của A (star schema, ETL, các quyết định thiết kế: quy ước doanh thu, loại trạng thái đơn, dim_customer vs customer_id...) để trả lời Q&A chéo
- [ ] Canh giờ nói thử bằng đồng hồ, đảm bảo nằm trong 7-8 phút, chừa thời gian cho 5 phút Q&A chung của nhóm
- [ ] Kiểm tra lại các giả định (độ co giãn what-if, giới hạn chuỗi thời gian...) đã được ghi chú rõ trên cả giao diện và báo cáo phần B
- [ ] Đảm bảo `data/processed/olist_dw.db` đã được build từ ETL mới nhất trước khi demo (không commit file `.db` lên Git)
