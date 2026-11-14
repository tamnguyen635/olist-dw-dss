# Báo cáo kiểm thử (14/11/2026)

Chạy: `pytest tests/ -q`. Cần `data/processed/olist_dw.db` (chạy `python src/etl/run_etl.py` trước).
Tổng cộng **160 test case**. Bộ test được thiết kế theo bốn lớp: kiểm thử đơn vị (dữ liệu nhỏ tự tạo, kết quả tính tay), đối chiếu với CSV gốc, kiểm thử chức năng và biên, và đối chiếu yêu cầu đề bài.

| File | Số test | Phạm vi |
|---|---|---|
| `test_etl_unit.py` | 24 | Quy tắc ETL trên 4 đơn hàng tự tạo: mức hạt, loại đơn không có sản phẩm, gộp khách theo `customer_unique_id`, thanh toán chính, điểm đánh giá trung bình, `delivery_days`/`delay_days`, dịch danh mục (kể cả 2 danh mục dịch tay, `unknown`), `dim_date`, nạp lại nhiều lần, quality check phải báo lỗi khi sai |
| `test_dw_integrity.py` | 33 | Schema, 7 khóa ngoại (ngày dùng 2 lần), chỉ mục; đối chiếu với CSV gốc (số dòng, SUM price/freight, số đơn, số khách, số sản phẩm, số người bán, cơ cấu trạng thái); khóa duy nhất; `dim_date` liên tục; quy tắc nghiệp vụ; các số liệu đã in trong báo cáo/slide |
| `test_olap.py` | 23 | 5 phép OLAP + payment mix + delivery vs review: tổng khớp nhau, drill-down 12 tháng đúng quý, slice top 10 giảm dần, dice chỉ chứa SP/RJ, pivot tổng = tổng các năm; tầng truy vấn của dashboard; biên (chọn rỗng, năm không có, SQL injection) |
| `test_app_smoke.py` | 11 | Chạy ngầm Streamlit (AppTest): 5 trang không lỗi, KPI, các điều khiển, chọn lần lượt mọi năm, mặc định dice |
| `test_dss_edge.py` | 28 | Dự báo (baseline, Holt, tính tái lập, công thức MAE/MAPE); RFM (mỗi khách đúng 1 nhóm, K trong 3 đến 4, mỗi nhóm có hành động đề xuất, tên nhóm không gây hiểu nhầm); what-if giao trễ và khuyến mãi (công thức tính tay, biên, đầu vào sai, hằng số khớp DW) |
| `test_submission_checklist.py` | 25 | Đối chiếu mục 1.1 và 5.1 của đề bài (schema, ETL, OLAP, dashboard, DSS, báo cáo PDF, src, data, README, slide PDF) + các việc còn lại trong `REVIEW_VY.md`; chạy lại ETL từ CSV vào DB tạm và so số dòng; chạy CLI OLAP |
| `test_queries.py`, `test_dss.py` | 16 | Test cũ của Vỹ, giữ nguyên |

## Kết quả

Kết quả: **150 đạt, 10 chưa đạt**.

Phần A (kho dữ liệu, ETL, OLAP): **toàn bộ đạt**. ETL chạy lại từ đầu cho đúng 112.650 dòng fact và 96.096 khách.

**Chưa hoàn thiện (test đang đỏ), đều ở phần B hoặc phần nộp bài:**

| Test | Nguyên nhân | Người sửa | Mức độ |
|---|---|---|---|
| `test_olap_dice_default_selection_is_not_nearly_empty` | Dice mặc định vẫn là AC, AL, AM nên biểu đồ gần như trống (REVIEW_VY mục 4) | Vỹ | Cao, lộ ngay khi demo |
| `test_report_B_has_no_empty_screenshot_placeholders` | Báo cáo B còn 5 khung ảnh trống (mục 1) | Vỹ | Cao |
| `test_rfm_segment_names_are_not_misleading` | "Khách mới" và "Khách ngủ đông" có recency gần như bằng nhau (mục 2) | Vỹ | Cao, dễ bị hỏi vặn |
| `test_requirements_pin_a_streamlit...` | `requirements.txt` vẫn ghi `streamlit>=1.30` (mục 5) | Vỹ | Trung bình |
| `test_review_item3_slide_outline_explains_k_choice` | Slide 6 chưa nói K=2 có silhouette cao hơn (mục 3) | Vỹ | Trung bình |
| `test_review_item7_*` (2 test) | Còn cụm "sau Tết" và tham chiếu cứng "Bảng~giao trễ" (mục 7) | Vỹ | Thấp |
| `test_review_item8_presentation_time_fits_the_limit` | Slide B cộng lại 510 giây, vượt 8 phút (mục 8) | Vỹ | Trung bình |
| `test_slides_pdf_exported_for_submission` | Chưa có file PDF slide trong `slides/` | Cả nhóm | Bắt buộc khi nộp |
| `test_report_A_cover_has_real_student_name_and_id` | Bìa báo cáo A chưa có MSSV | A | Bắt buộc khi nộp |

## Phát hiện từ dữ liệu

Dữ liệu gốc Olist có 6 đơn `canceled` (7 dòng) vẫn có ngày giao. Không ảnh hưởng kết quả vì mọi truy vấn giao hàng đều lọc `status = 'delivered'`. Một test ghi nhận điều này để nếu số lượng tăng lên sẽ báo.

## Chưa kiểm thử được

Giao diện thật trên trình duyệt (bố cục, màu, đọc được hay không), chất lượng dự báo ngoài các sai số đã báo cáo, và độ chính xác của nội dung báo cáo. Những phần này cần người đọc.
