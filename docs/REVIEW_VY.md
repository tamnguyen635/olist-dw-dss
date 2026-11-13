# Góp ý cho phần B (Vỹ) – danh sách cần sửa

Nhánh được kiểm tra: `feature/dashboard-dss` (commit `0d28c94`).
Hạn nộp cả nhóm: **23:59 Chủ nhật 15/11**. A cần Vỹ sửa xong trước **tối nay (12/11)** để ngày 13/11 hai người tích hợp và chạy thử.

## Đã kiểm tra và ổn (không cần đụng vào)

- 16/16 test qua (`pytest tests/ -q`).
- 3 module DSS chạy ra đúng số trong báo cáo B (MAE/MAPE, K=3 silhouette 0,411, bảng what-if).
- Streamlit chạy với bản 1.67, cả 5 trang mở không lỗi. KPI khớp DW (doanh thu 13.494.401; 98.199 đơn).
- Chỉ đọc DW qua `queries.py`, SQL dùng tham số `?`, quy ước doanh thu giống phần A.
- Không sửa file nào của A. Nhánh không lệch so với `main`, ghép sẽ không xung đột.
- Báo cáo và giao diện nói thẳng việc Holt kém baseline, F của RFM bị thay thế, độ co giãn là giả định. Giữ nguyên cách viết trung thực này.

## Việc cần sửa

Ký hiệu: **[Bắt buộc]** phải xong trước khi nộp, **[Nên làm]** nên làm nếu kịp, **[Tùy chọn]** làm khi rảnh.

### 1. [Bắt buộc] Báo cáo B còn 5 khung ảnh trống (~30 phút)

`report/part_B_dss.tex` có 5 khung `\fbox{...TODO: chèn ảnh chụp màn hình...}` ở các dòng 111–115, 138–142, 148–152, 159–163, 170–174 (một khung cho mỗi trang dashboard). Bản PDF hiện chỉ 10 trang vì thế.

Cách làm:
1. Chạy `streamlit run src/app/app.py`, chụp từng trang. Trang dài thì dùng Chrome DevTools: `Ctrl+Shift+P` → "Capture full size screenshot", hoặc thu nhỏ trình duyệt xuống 50–67%.
2. Lưu vào `report/figures/` (ví dụ `ss_overview.png`, `ss_olap.png`, `ss_geo.png`, `ss_delivery.png`, `ss_dss.png`).
3. Thay mỗi `\fbox{...}` bằng `\includegraphics[width=\textwidth]{figures/ss_overview.png}` (đổi tên file cho từng hình).
4. Xóa ý "Chưa có ảnh chụp màn hình dashboard" trong mục Hạn chế (dòng 403–404).
5. Biên dịch lại bằng `xelatex part_B_dss.tex` **hai lần**, rồi commit cả `.tex` và `.pdf`.

### 2. [Bắt buộc] Đổi tên phân khúc RFM (~20 phút)

Tên hiện tại gây hiểu nhầm, thầy rất dễ hỏi vặn. Số liệu thật:

| Phân khúc hiện tại | Recency TB (ngày) | Review TB | Repeat | Số khách |
|---|---|---|---|---|
| Khách ngủ đông | 248,5 | 1,89 | 0 | 20.300 |
| Khách mới | 242,5 | 4,75 | 0 | 71.792 |
| Khách giá trị cao | 226,6 | 4,17 | 1 | 2.891 |

Recency của hai nhóm đầu gần như bằng nhau (~8 tháng). Vậy họ **không "mới"** và cũng **không "ngủ đông" hơn nhau**. Hai nhóm này chỉ khác nhau ở **điểm đánh giá**. Nên đổi:

- "Khách mới" → **"Mua 1 lần – hài lòng"**
- "Khách ngủ đông" → **"Mua 1 lần – không hài lòng"**
- "Khách giá trị cao" giữ nguyên (đúng là nhóm mua lại, chi tiêu 271 so với 135–150).
- "Khách thường xuyên" (nhóm dự phòng khi K>3) → **"Khách khác"**.

Chỉ cần sửa giá trị trong dict `SEGMENT_NAMES` ở `src/dss/rfm.py` (dòng 35–42). `SEGMENT_ACTIONS` (dòng 131–138) lấy khóa từ dict này nên tự theo. Sau đó sửa tên trong báo cáo B (bảng ở dòng 283–285, đoạn văn ở dòng 270–273, 290–297) và slide 6. Cập nhật câu mô tả `_name_segments` cho khớp, rồi chạy lại `pytest`.

### 3. [Bắt buộc] Slide 6 và Q&A về việc chọn K (~10 phút)

`slides/part_B_outline.md` dòng 79 ghi "chọn K bằng elbow + silhouette → K=3". Thực tế silhouette **cao nhất ở K=2 (0,681)**, K=3 (0,411) do code giới hạn trong khoảng 3–4. Báo cáo B (dòng 244–248) viết đúng, còn slide thì chưa.

- Sửa dòng 79 thành: "K=3 (giới hạn trong khoảng 3–4; K=2 có silhouette cao hơn 0,681 nhưng chỉ có 2 nhóm, không đủ để đề xuất hành động khác nhau)".
- Thêm vào mục Q&A (slide 10): **"Vì sao K=3 trong khi K=2 có silhouette cao hơn?"** Trả lời: K=2 chỉ cho hai nhóm, quá ít để đề xuất hành động riêng cho từng nhóm; trong khoảng 3–4 thì K=3 tốt nhất; silhouette 0,411 là mức trung bình và đã nêu ở phần hạn chế.

### 4. [Bắt buộc] Biểu đồ dice mặc định gần như trống (~10 phút)

`src/app/app.py` dòng 177–182 lấy mặc định `states[:3]` và `categories[:3]`, tức 3 bang và 3 danh mục đầu **theo thứ tự ABC** (`AC, AL, AM` và `agro_industry_and_commerce, air_conditioning, art`). Kết quả chỉ 4 dòng, tổng doanh thu 2.164. Khi demo, biểu đồ đầu tiên thầy thấy gần như rỗng.

Sửa thành bang lớn và danh mục doanh thu cao:

```python
states = _available_states()
categories = _available_categories()
default_states = [s for s in ("SP", "RJ", "MG") if s in states]
default_cats = _category_revenue_summary()["category_en"].head(3).tolist()
sel_states = st.multiselect("Chọn bang (state)", states, default=default_states)
sel_categories = st.multiselect("Chọn danh mục", categories, default=default_cats)
```

(`_category_revenue_summary()` đã có sẵn trong `app.py` và trả về danh mục sắp theo doanh thu giảm dần.)

### 5. [Bắt buộc] Ghim đúng phiên bản Streamlit trong `requirements.txt` (~5 phút)

`requirements.txt` ghi `streamlit>=1.30` nhưng `app.py` dùng `width='stretch'` cho `st.plotly_chart` và `st.dataframe`. A tải thử bản 1.40 và 1.50: ở `st.plotly_chart` hai bản này vẫn dùng `use_container_width`, **chưa có tham số `width`**. Dashboard chạy tốt với 1.67.

Việc cần làm: chạy `pip show streamlit` trên máy Vỹ, rồi sửa dòng này thành đúng bản đã chạy được (ví dụ `streamlit>=1.67`). Nếu máy Vỹ dùng bản khác 1.67 mà vẫn chạy tốt, ghi bản của Vỹ.

### 6. [Nên làm] Dự báo "tháng kế tiếp" vẫn lấy từ mô hình kém hơn (~15 phút)

`forecast.py` dòng 91–96 và `app.py` dòng 286–289 trình bày dự báo tháng kế tiếp từ **Holt**, dù Holt kém baseline gần 4 lần trên tập test (MAPE 32,24% so với 7,85%). Cảnh báo đã có, nhưng người xem vẫn thấy con số của mô hình đã thất bại. Hai hướng, chọn một:
- Hiển thị thêm dự báo tháng kế tiếp của **baseline** cạnh Holt, hoặc dùng mô hình có sai số test thấp hơn.
- Thử Holt có xu hướng giảm dần (`damped_trend=True`) và báo cáo kết quả (dù tốt hơn hay không, cũng là một điểm để nói khi trình bày).

### 7. [Nên làm] Hai lỗi nhỏ trong báo cáo B

- Dòng 223: "thời điểm doanh thu vẫn đang hồi phục **sau Tết**" sai bối cảnh vì dữ liệu là của Brazil. Bỏ cụm "sau Tết" (hoặc bỏ cả vế đó).
- Dòng 305: "(phần A, Bảng~giao trễ)" là chữ cứng, không phải tham chiếu thật. Đổi thành "(xem báo cáo phần A, mục OLAP: giao hàng và mức hài lòng)".

### 8. [Nên làm] Rút gọn thời lượng slide (~10 phút)

Outline cộng lại **510 giây (8,5 phút)**, vượt mức 7–8 phút (cả nhóm có 15 phút, mỗi người khoảng 7–8). Gợi ý cắt: slide 3 từ 70s xuống 55s, slide 4 từ 50s xuống 40s, slide 8 từ 60s xuống 45s. Tổng còn 470s. Sửa lại bảng tính ở dòng 151–152.

### 9. [Tùy chọn] Đọc hằng số 2,55 và 4,21 từ DW

`src/dss/whatif.py` dòng 25–27 viết cứng `REVIEW_SCORE_LATE = 2.55`, `REVIEW_SCORE_ON_TIME = 4.21`. Hiện đúng, nhưng sẽ lệch nếu ETL đổi. Có thể lấy từ hàm `delivery_vs_review()` đã có trong `queries.py`.

### 10. [Tùy chọn] Hiển thị bảng MAE gọn hơn

Trang "Dự báo & DSS" đang hiện `69432.0408`. Có thể định dạng: `st.dataframe(mae_table.style.format({"MAE": "{:,.0f}", "MAPE (%)": "{:.2f}"}))`.

## Cách nộp lại

1. Làm tiếp **trên nhánh `feature/dashboard-dss`**. Mỗi việc ở trên nên là **một commit riêng** với tên rõ nghĩa (ví dụ `Rename RFM segments`, `Set sensible dice defaults`). Lịch sử commit là bằng chứng đóng góp cho peer review.
2. Trước khi push, chạy kiểm tra:
   ```
   pytest tests/ -q
   streamlit run src/app/app.py     # mở thử cả 5 trang
   xelatex part_B_dss.tex           # chạy 2 lần
   ```
3. Push lên nhánh rồi nhắn A. A kiểm tra lại và merge vào `main`.
4. Nếu cần đổi `01_schema.sql` hoặc `run_etl.py`, nhắn A, đừng tự sửa.

## Thứ tự đề xuất (khoảng 1,5–2 giờ)

Việc **2 → 3 → 4 → 5** (đều ngắn và cần cho demo), rồi **1** (chụp ảnh sau khi đã sửa giao diện để ảnh là bản cuối), rồi **7 và 8**. Việc 6, 9, 10 làm nếu còn thời gian.
