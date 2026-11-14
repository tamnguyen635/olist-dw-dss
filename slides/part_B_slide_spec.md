# Đặc tả sinh slide – Phần B (Dashboard & DSS)

Dùng cho công cụ AI sinh slide. Tài liệu mô tả **từng slide**: bố cục, toạ độ, cỡ chữ, màu, nội dung chữ chính xác, dữ liệu biểu đồ và ghi chú diễn giả. Công cụ chỉ cần làm đúng theo, không tự quyết định bố cục.

**Bộ slide này dùng đúng hệ thiết kế, lưới và thành phần của `slides/part_A_slide_spec.md`** (khổ giấy, màu, phông, tiêu đề, footer, thẻ, bảng, banner). Mục 1 và 2 dưới đây chép lại nguyên văn để file đọc độc lập; nếu hai file khác nhau ở các mục này thì **file phần A là chuẩn**.

- Người trình bày: Vỹ (Người B: dashboard, DSS, demo). Thời lượng mục tiêu **7 phút 10 giây** (430 giây), bằng phần A. Hai phần cộng lại 860 giây (14 phút 20 giây), nằm trong mức 15 phút của đề bài, còn khoảng 40 giây để chuyển phần.
- Số slide: **10 slide chính + 2 slide phụ lục** (phụ lục chỉ dùng khi trả lời Q&A, không trình bày).

---

## 0. Cách dùng

Dán toàn bộ file này vào công cụ AI cùng câu lệnh sau:

> Hãy tạo bản trình chiếu đúng theo đặc tả dưới đây. Giữ nguyên toạ độ, cỡ chữ, màu và nội dung chữ. Không thêm, bớt hay đổi bất kỳ số liệu nào. Không thêm ảnh, icon hay hình trang trí ngoài những gì được mô tả. Nếu chữ bị tràn khung, hãy rút gọn câu chứ không giảm cỡ chữ dưới mức tối thiểu. Biểu đồ phải là đối tượng biểu đồ có thể chỉnh sửa, **nét đường đúng độ dày ghi trong đặc tả, chấm đánh dấu đúng kích thước ghi trong đặc tả (đơn vị point, không phóng to)**. Xuất ra PPTX có thể chỉnh sửa (mọi chữ và bảng là đối tượng thật, không phải ảnh) và PDF. Kiểm tra theo danh sách ở Mục 6 trước khi xuất.

Nếu công cụ không đặt được toạ độ chính xác: giữ **thứ tự, phân cấp và tỷ lệ** giữa các khối như trong đặc tả.

**Quy tắc cho bảng và chữ (bắt buộc):**
- Tô màu hoặc in đậm một con số trong bảng bằng **định dạng của chính ô đó**. Tuyệt đối không đặt hộp chữ riêng chồng lên bảng.
- Mọi hộp chữ phải **bật tự xuống dòng**, có chiều rộng đúng bằng chiều rộng trong đặc tả trừ đệm; chữ không được vượt ra ngoài thẻ chứa nó. Tắt tự động co giãn khung.
- Hàng bảng chỉ cao đúng giá trị trong đặc tả; không để bảng đè lên khối khác.
- Biểu đồ dùng trục, chú giải, tiêu đề của chính đối tượng biểu đồ.

**Khung ảnh chụp màn hình:** các slide 3 và 4 có khung dành cho ảnh chụp dashboard. Ảnh sẽ được chèn sau, nên công cụ chỉ vẽ **khung nét đứt kèm dòng chữ giữ chỗ** như mô tả, không tự tạo ảnh giả.

---

## 1. Quy ước chung

| Mục | Giá trị |
|---|---|
| Tỷ lệ | 16:9, **13,333 × 7,5 inch** (1920 × 1080 px) |
| Đơn vị toạ độ | inch, gốc (0,0) ở góc trên trái; mỗi khối ghi `x, y, w, h` |
| Ngôn ngữ | Tiếng Việt, **bắt buộc hiển thị đúng dấu** (kiểm tra không có ô vuông thay chữ) |
| Số | Dấu chấm ngăn nghìn, dấu phẩy thập phân (ví dụ `112.650`, `4,21`). Giữ nguyên như trong đặc tả |
| Hiệu ứng | Không animation, không chuyển cảnh |
| Ảnh / icon | Không dùng ảnh stock, không emoji. Chỉ dùng hình khối, biểu đồ và khung giữ chỗ được mô tả |

## 2. Hệ thiết kế (giống hệt phần A)

### 2.1 Màu

| Tên | Hex | Dùng cho |
|---|---|---|
| `ink` | `#1F2937` | Chữ chính |
| `muted` | `#6B7280` | Chữ phụ, chú thích, footer |
| `bg` | `#FFFFFF` | Nền slide |
| `panel` | `#F3F4F6` | Nền thẻ (card) |
| `line` | `#E5E7EB` | Đường kẻ, lưới biểu đồ |
| `blue` | `#3465A4` | Nhấn chính, tiêu đề phụ, đường dữ liệu thực tế |
| `blue-light` | `#DBEAFE` | Nền banner |
| `orange` | `#D66028` | Điểm nhấn số liệu |
| `orange-light` | `#FDEBE3` | Nền nhấn nhẹ |
| `green` | `#2E7D32` | Đạt, tốt, số đo thực tế |
| `red` | `#C62828` | Xấu, giao trễ, mô hình kém |
| `amber` | `#F59E0B` | Nhãn "giả định" |
| `amber-light` | `#FEF3C7` | Khung lưu ý |

Quy ước ngữ nghĩa dùng riêng cho phần B: **xanh lá = số đo thực tế hoặc mô hình tốt; đỏ = giao trễ hoặc mô hình kém; vàng (amber) = giả định của người dùng**. Không dùng màu ngoài bảng này.

### 2.2 Phông chữ và cỡ chữ

- Chữ thường: **Inter** (dự phòng: Segoe UI, Arial). Phải hỗ trợ tiếng Việt.
- Chữ đơn cách (tên hàm, lệnh, công thức): **JetBrains Mono** (dự phòng: Consolas, Courier New).

| Vai trò | Cỡ | Kiểu |
|---|---|---|
| Tiêu đề slide | 30 pt | Đậm, `ink`, căn trái, **một dòng**, tối đa 46 ký tự |
| Tiêu đề thẻ / tiêu đề phụ | 20 pt | Đậm |
| Nội dung chính | 18 đến 20 pt | Thường |
| Chữ trong bảng, mô tả thẻ | 16 pt | Thường |
| Chú thích, nhãn nhỏ | **14 pt (tối thiểu)** | `muted` |
| Footer | 12 pt | `muted` |
| Số lớn (KPI) | 28 đến 44 pt | Đậm |

Giãn dòng 1,2 (đoạn văn) và 1,3 (danh sách). Căn trái mọi đoạn chữ; số trong bảng căn phải hoặc giữa như ghi trong từng slide.

### 2.3 Lưới và khung chung (mọi slide trừ slide 1)

Nội dung chỉ nằm trong **vùng an toàn**: `x 0,6 đến 12,733` và `y 0,4 đến 7,3`.

| ID | Thành phần | x | y | w | h | Style |
|---|---|---|---|---|---|---|
| T | Tiêu đề slide | 0,6 | 0,4 | 12,133 | 0,8 | 30 pt đậm `ink`, canh giữa theo chiều dọc |
| TA | Gạch nhấn dưới tiêu đề | 0,6 | 1,25 | 1,2 | 0,06 | Tô `blue`, không viền |
| F1 | Footer trái | 0,6 | 7,05 | 9,0 | 0,3 | 12 pt `muted`: `CO4031 · Bài tập lớn · Phần B: Dashboard và DSS` |
| F2 | Số slide | 11,733 | 7,05 | 1,0 | 0,3 | 12 pt `muted`, căn phải, tự đánh số |

**Vùng nội dung:** `x 0,6 đến 12,733`, `y 1,6 đến 6,8` (rộng 12,133, cao 5,2).

Các cách chia cột chuẩn:
- 2 cột: `x = 0,6` và `x = 6,833`, mỗi cột rộng `5,9` (khe 0,333).
- 3 cột: `x = 0,6; 4,765; 8,93`, mỗi cột rộng `3,8` (khe 0,365).
- 5 thẻ ngang: `x = 0,6; 3,07; 5,54; 8,01; 10,48`, mỗi thẻ rộng `2,25` (khe 0,22).
- Khoảng cách tối thiểu giữa hai khối: 0,3 inch (trừ hàng 5 thẻ ngang). **Không được chồng lấn.**

### 2.4 Thành phần dùng lại

- **Thẻ (card):** hình chữ nhật bo góc bán kính 0,12 inch, nền `panel`, không viền, đệm trong 0,2 inch.
- **Bảng:** hàng tiêu đề nền `blue`, chữ trắng đậm 16 pt; hàng nội dung xen kẽ `bg` và `panel`; không kẻ viền dọc; đệm ô 0,12 inch; chữ canh giữa theo chiều dọc.
- **Banner:** hình chữ nhật chiều rộng 12,133 inch, nền theo từng slide, chữ canh giữa cả hai chiều.
- **Khung giữ chỗ ảnh:** hình chữ nhật nền `bg`, viền nét đứt 1,5 pt màu `muted`, chữ giữ chỗ 16 pt `muted` canh giữa cả hai chiều.
- **Dấu đạt:** ký tự `✓` màu `green`, đậm.
- **Nhãn (badge):** hình chữ nhật bo góc 0,2 inch, cao 0,4, chữ 14 pt đậm, canh giữa; màu theo từng slide.

---

## 3. Tổng quan thời lượng

| # | Slide | Giây |
|---|---|---|
| 1 | Tiêu đề phần B | 15 |
| 2 | Kiến trúc và hợp đồng dữ liệu | 35 |
| 3 | Dashboard: Tổng quan và OLAP | 55 |
| 4 | Dashboard: Địa lý, thanh toán, giao hàng | 45 |
| 5 | DSS 1: Dự báo doanh thu | 55 |
| 6 | DSS 2: Phân khúc khách hàng RFM | 55 |
| 7 | DSS 3: Mô hình what-if | 50 |
| 8 | Demo trực tiếp | 60 |
| 9 | Hạn chế và hướng phát triển | 30 |
| 10 | Kết luận và Q&A | 30 |
| | **Tổng** | **430 (7 phút 10 giây)** |
| B1, B2 | Phụ lục (ẩn, chỉ dùng cho Q&A) | – |

Outline cũ (`part_B_outline.md`) cộng lại 510 giây, vượt mức cho phép. Bản này đã rút xuống 430 giây.

---

## 4. Đặc tả từng slide

### Slide 1 – Tiêu đề phần B (15 giây)

**Layout:** giống hệt slide 1 của phần A. Nền trắng, không footer, không số slide.

| ID | Thành phần | x | y | w | h | Nội dung / style |
|---|---|---|---|---|---|---|
| 1a | Dải màu bên trái | 0 | 0 | 0,35 | 7,5 | Tô `blue` |
| 1b | Nhãn nhỏ | 1,0 | 1,4 | 11,3 | 0,4 | `CO4031 · KHO DỮ LIỆU VÀ HỆ HỖ TRỢ QUYẾT ĐỊNH · HK261`, 16 pt `muted`, chữ hoa |
| 1c | Tiêu đề | 1,0 | 2,2 | 11,3 | 1,9 | `Dashboard và hệ hỗ trợ quyết định trên kho dữ liệu Olist`, 44 pt đậm `ink`, tối đa 2 dòng |
| 1d | Phụ đề | 1,0 | 4,2 | 11,3 | 0,6 | `Phần B: Dashboard Streamlit, mô hình DSS và demo`, 24 pt `blue` |
| 1e | Gạch nhấn | 1,0 | 5,2 | 2,0 | 0,04 | Tô `orange` |
| 1f | Người trình bày | 1,0 | 5,4 | 11,3 | 0,5 | `Người trình bày: [Họ tên – MSSV]`, 20 pt `ink` |
| 1g | Nhóm | 1,0 | 5,95 | 11,3 | 0,5 | `Nhóm: [Họ tên A – MSSV] · [Họ tên Vỹ – MSSV]`, 16 pt `muted` |

Giữ nguyên các dấu ngoặc vuông, **không tự bịa tên hay mã số**; người dùng sẽ tự điền. Nếu ghép chung một bộ slide với phần A, có thể bỏ slide này.

**Ghi chú diễn giả:** Em là Vỹ, phụ trách phần dashboard, các mô hình hỗ trợ ra quyết định và phần demo. Em dùng kho dữ liệu mà bạn A vừa trình bày.

---

### Slide 2 – Kiến trúc và hợp đồng dữ liệu (35 giây)

**Layout:** một hàng 3 hộp có mũi tên ở trên, 3 thẻ giải thích ở dưới.
**Tiêu đề (T):** `Kiến trúc và hợp đồng dữ liệu`

**Hàng sơ đồ** (hộp bo góc 0,15 inch, `w 3,2`, `h 1,5`, `y 1,8`; tiêu đề hộp 20 pt đậm, dòng phụ 16 pt, canh giữa cả hai chiều):

| ID | x | Fill | Màu chữ | Tiêu đề hộp | Dòng phụ |
|---|---|---|---|---|---|
| 2a | 0,6 | `blue` | trắng | `Kho dữ liệu` | `olist_dw.db (phần A)` |
| 2b | 5,067 | `blue-light` | `ink` | `Tầng truy vấn` | `src/app/queries.py` |
| 2c | 9,533 | `panel` | `ink` | `Giao diện và mô hình` | `app.py · src/dss/` |

**Mũi tên** (hình mũi tên phải, tô `muted`, `w 0,6`, `h 0,4`, `y 2,35`): tại `x 4,1` và `x 8,567`.

**3 thẻ giải thích** (thẻ chuẩn, `y 3,7`, `w 3,8`, `h 2,9`, `x = 0,6; 4,765; 8,93`; tiêu đề thẻ 20 pt đậm `blue`, nội dung 18 pt `ink`):

| ID | Tiêu đề | Nội dung |
|---|---|---|
| 2d | `Chỉ đọc từ DW` | `Không đọc CSV gốc, không sửa schema. Mọi thay đổi schema do phần A thực hiện.` |
| 2e | `Một cửa truy vấn` | `Mọi câu SQL nằm trong queries.py. Dashboard và mô hình DSS đều gọi qua đây.` (tên tệp dùng phông đơn cách) |
| 2f | `An toàn và nhanh` | `Tham số hóa bằng dấu ?, không nối chuỗi SQL. Kết quả được cache bằng st.cache_data.` (tên hàm dùng phông đơn cách) |

**Ghi chú diễn giả:** Em kế thừa nguyên star schema của bạn A, không đổi schema và không đọc lại CSV. Toàn bộ câu SQL nằm trong một tệp queries.py, nên dashboard và các mô hình dùng chung một quy ước tính doanh thu. Điều kiện lọc đều là tham số, không nối chuỗi, để tránh SQL injection.

---

### Slide 3 – Dashboard: Tổng quan và OLAP (55 giây)

**Layout:** hàng 5 thẻ KPI ở trên; dưới là khung ảnh bên trái và danh sách phép OLAP bên phải.
**Tiêu đề (T):** `Dashboard: Tổng quan và OLAP`

**5 thẻ KPI** (thẻ chuẩn, `y 1,6`, `w 2,25`, `h 1,3`, `x = 0,6; 3,07; 5,54; 8,01; 10,48`). Mỗi thẻ có số (28 pt đậm, `x` thẻ `+0,2`, `y 1,7`, `w 1,85`, `h 0,6`) và nhãn (14 pt `muted`, `y 2,35`, `h 0,45`):

| Thẻ | Số | Màu số | Nhãn |
|---|---|---|---|
| 3a | `13,49 triệu` | `blue` | `doanh thu` |
| 3b | `98.199` | `blue` | `đơn hàng` |
| 3c | `137,42` | `blue` | `giá trị đơn trung bình` |
| 3d | `4,04` | `blue` | `điểm đánh giá trung bình` |
| 3e | `7,91%` | `red` | `tỷ lệ giao trễ` |

**Khung ảnh 3f:** `x 0,6; y 3,15; w 6,9; h 3,65`. Khung giữ chỗ ảnh. Chữ giữ chỗ: `Ảnh chụp trang Phân tích đa chiều (OLAP): chèn sau`.

**Phần phải (x 7,8 đến 12,733, w 4,933):**
- 3g: tiêu đề `Trang OLAP có đủ 5 phép toán`, `x 7,8; y 3,15; w 4,933; h 0,45`, 18 pt đậm `blue`.
- 3h: 5 hàng, `x 7,8`, `w 4,933`, `h 0,6`, bắt đầu `y 3,65` (các hàng cách nhau 0,6, hàng cuối kết thúc `y 6,65`). Trong mỗi hàng: tên phép toán (`w 1,5`, 18 pt đậm `blue`) và mô tả (`x 9,3`, `w 3,433`, 16 pt `ink`):

| Phép toán | Mô tả |
|---|---|
| `Roll-up` | `Tháng → năm` |
| `Drill-down` | `Năm → quý → tháng` |
| `Slice` | `Cố định năm, xem theo danh mục` |
| `Dice` | `Nhiều bang × nhiều danh mục` |
| `Pivot` | `Danh mục × năm` |

**Ghi chú diễn giả:** Trang Tổng quan có năm chỉ số tính trực tiếp từ bảng fact: doanh thu 13,49 triệu, 98.199 đơn, giá trị đơn trung bình 137,42, điểm đánh giá 4,04 và tỷ lệ giao trễ 7,91%. Trang OLAP có đủ năm phép toán của phần A, mỗi phép toán có một hàm SQL riêng và có thể chọn năm, bang, danh mục ngay trên giao diện.

---

### Slide 4 – Dashboard: Địa lý, thanh toán, giao hàng (45 giây)

**Layout:** hai cột (bảng bang và thẻ nhận xét bên trái, biểu đồ thanh bên phải), banner nối sang trang Giao hàng ở dưới.
**Tiêu đề (T):** `Địa lý, thanh toán và giao hàng`

**Cột trái (x 0,6, w 5,9):**
- 4a: tiêu đề `Doanh thu và điểm đánh giá theo bang`, `x 0,6; y 1,6; w 5,9; h 0,45`, 18 pt đậm `ink`.
- 4b: bảng `x 0,6; y 2,15; w 5,9`; cột: `w 1,3` (`Bang`, canh trái), `w 2,6` (`Doanh thu (triệu)`, canh phải), `w 2,0` (`Điểm đánh giá TB`, canh phải); hàng tiêu đề cao 0,5; 3 hàng cao 0,5 (kết thúc `y 4,15`):

| Bang | Doanh thu (triệu) | Điểm đánh giá TB |
|---|---|---|
| `SP` | `5,17` | `4,14` |
| `RJ` | `1,81` | `3,82` |
| `MG` | `1,57` | `4,09` |

  Ô `3,82` của RJ in đậm màu `red`.
- 4c: thẻ chuẩn `x 0,6; y 4,35; w 5,9; h 1,4`, chữ 18 pt `ink`, đệm 0,2: `RJ đứng thứ hai về doanh thu nhưng điểm đánh giá thấp hơn SP 0,32 điểm.`

**Cột phải (x 6,833, w 5,9):**
- 4d: tiêu đề `Cơ cấu doanh thu theo hình thức thanh toán`, `x 6,833; y 1,6; w 5,9; h 0,45`, 18 pt đậm `ink`.
- 4e: biểu đồ thanh ngang `x 6,833; y 2,1; w 5,9; h 3,65`. **Một chuỗi**, không chú giải, thanh tô `blue`, độ dày thanh vừa phải (khe giữa các thanh bằng nửa độ dày thanh). Trục giá trị 0 đến 100 (đơn vị %), bước 25, nhãn 14 pt `muted`; lưới dọc nét 0,75 pt `line`, không lưới ngang. Nhãn hạng mục 14 pt `ink` ở bên trái. Nhãn giá trị 14 pt đậm `ink` ở đầu mỗi thanh. Thứ tự từ trên xuống:

| Hạng mục | Giá trị (%) |
|---|---|
| `Thẻ tín dụng` | 78,9 |
| `Boleto` | 17,6 |
| `Voucher` | 2,1 |
| `Thẻ ghi nợ` | 1,4 |

**Banner 4f:** `x 0,6; y 6,0; w 12,133; h 0,8`, nền `blue-light`, chữ 18 pt đậm `ink`: `Trang Giao hàng: đơn giao trễ có điểm đánh giá 2,55, đơn đúng hạn hoặc sớm có 4,21`.

**Ghi chú diễn giả:** Trang địa lý cho thấy SP là bang có doanh thu lớn nhất, 5,17 triệu, và điểm đánh giá 4,14. RJ đứng thứ hai về doanh thu nhưng điểm chỉ 3,82, đây là gợi ý để xem lại vận hành ở RJ. Thẻ tín dụng chiếm gần 79% doanh thu. Trang Giao hàng so sánh trực tiếp hai nhóm đơn: giao trễ được 2,55 điểm, đúng hạn hoặc sớm được 4,21.

---

### Slide 5 – DSS 1: Dự báo doanh thu (55 giây)

**Layout:** biểu đồ đường lớn bên trái, bảng sai số và kết luận bên phải, banner dự báo tháng kế tiếp ở dưới.
**Tiêu đề (T):** `DSS 1: Dự báo doanh thu`

**Nền biểu đồ 5a:** thẻ chuẩn `x 0,6; y 1,6; w 7,4; h 4,1` (kết thúc `y 5,7`). Mọi thành phần của biểu đồ nằm trong khung này.

**Biểu đồ 5b** (nằm trong thẻ 5a):
- Tiêu đề: `Doanh thu theo tháng (nghìn)`, 18 pt đậm `ink`, `x 0,85; y 1,7; w 6,9; h 0,4`.
- Chú giải: chú giải gốc của biểu đồ, phía trên vùng vẽ, 14 pt: `Thực tế` (`blue`, nét liền), `Baseline` (`green`, nét đứt), `Holt` (`red`, nét đứt).
- Vùng vẽ: `x 1,5 đến 7,7`, `y 2,6 đến 4,85`.
- Trục Y: 0 đến 1.400, vạch 0, 350, 700, 1.050, 1.400; nhãn 14 pt `muted` bên trái vùng vẽ; lưới ngang nét 0,75 pt `line`; không lưới dọc.
- Trục X: 20 điểm từ `01/2017` đến `08/2018`; chỉ ghi nhãn tại `01/2017`, `07/2017`, `01/2018`, `07/2018` (14 pt `muted`), đặt dưới vùng vẽ `y 4,9; h 0,3`.
- **Không vẽ dải nền vùng kiểm tra** (dải đặt tay luôn lệch khỏi biểu đồ). Vùng kiểm tra chỉ được nêu ở chú thích 5c.
- **Chỉ dùng trục, nhãn trục, chú giải và tiêu đề của chính đối tượng biểu đồ.** Không đặt thêm hộp chữ nào làm nhãn trục, chú giải hay tiêu đề (tránh bị nhân đôi và chồng chữ). Tắt nhãn "Plot Area". Biểu đồ có **đúng 3 chuỗi**, không đường xu hướng, không chuỗi thừa. Với Baseline và Holt, 16 ô đầu để **trống** (hiển thị khoảng trống, không phải số 0).
- Chuỗi **Thực tế** (nghìn), 20 điểm, nét 2,5 pt `blue`, nét liền, chấm tròn đường kính 6 pt `blue`:
  `120, 245, 368, 354, 503, 430, 492, 568, 621, 660, 1004, 742, 945, 838, 981, 994, 993, 863, 878, 849`
- Chuỗi **Baseline**, chỉ 4 điểm cuối (từ `05/2018` đến `08/2018`), nét 2,5 pt `green`, nét đứt, chấm tròn 6 pt `green`: `938, 938, 938, 938`
- Chuỗi **Holt**, chỉ 4 điểm cuối, nét 2,5 pt `red`, nét đứt, chấm tròn 6 pt `red`: `1093, 1149, 1205, 1261`
- Không hiện nhãn giá trị trên các điểm.

**Chú thích 5c:** `x 0,85; y 5,25; w 6,9; h 0,35`, 14 pt `muted`: `Huấn luyện 16 tháng đầu; kiểm tra 4 tháng cuối (05/2018 đến 08/2018), nơi Baseline và Holt xuất hiện.`

**Bảng sai số 5d** (`x 8,3; y 1,6; w 4,433`; cột: `w 1,9` (`Mô hình`), `w 1,3` (`MAE`, canh phải), `w 1,233` (`MAPE`, canh phải); hàng tiêu đề cao 0,5; 2 hàng cao 0,55, kết thúc `y 3,2`; chữ 16 pt):

| Mô hình | MAE | MAPE |
|---|---|---|
| `Baseline` | `69.432` | `7,85%` |
| `Holt` | `281.179` | `32,24%` |

  Hàng Baseline: số in đậm `green`. Hàng Holt: số in đậm `red`.

**Thẻ kết luận 5e:** thẻ chuẩn `x 8,3; y 3,4; w 4,433; h 2,3` (kết thúc `y 5,7`). Tiêu đề thẻ `Baseline chính xác hơn Holt` (18 pt đậm `ink`, `x 8,5; y 3,55; w 4,03; h 0,4`). Hai gạch đầu dòng 16 pt `ink`, bật tự xuống dòng (`x 8,5; y 4,05; w 4,03; h 1,55`):
- `Holt có MAPE cao gấp khoảng 4 lần baseline`
- `Holt ngoại suy đà tăng, nhưng doanh thu đi ngang sau 11/2017`

**Banner 5f:** `x 0,6; y 6,0; w 12,133; h 0,8`, nền `blue-light`, chữ 16 pt `ink`, canh giữa. Dòng 1 (đậm): `Dự báo tháng 09/2018: Holt 854.930 (khoảng tin cậy 95%: 643.624 đến 1.066.236), baseline 863.390`.

  Ghi chú cho người làm slide: `863.390` là trung bình của 3 tháng cuối (863.266, 878.044, 848.860), không hiển thị trên dashboard.

**Ghi chú diễn giả:** Em dự báo doanh thu tháng từ chuỗi 20 tháng, huấn luyện trên 16 tháng đầu và kiểm tra trên 4 tháng cuối. Em so sánh baseline, tức trung bình trượt ba tháng, với Holt có xu hướng. Kết quả thật là Holt kém hơn: MAPE 32,24% so với 7,85%. Lý do là doanh thu đi ngang sau đỉnh tháng 11/2017 nhưng Holt vẫn ngoại suy xu hướng tăng. Chuỗi quá ngắn để dùng mô hình mùa vụ. Dashboard có cảnh báo rõ điều này. Dự báo tháng kế tiếp của hai mô hình khá gần nhau, quanh 860 nghìn.

---

### Slide 6 – DSS 2: Phân khúc khách hàng RFM (55 giây)

**Layout:** hàng trên là hai thẻ nối bằng mũi tên (vấn đề rồi cách xử lý), giữa là bảng ba phân khúc, dưới cùng là dòng ghi chú về K.
**Tiêu đề (T):** `DSS 2: Phân khúc khách hàng RFM`

**Hàng trên** (thẻ chuẩn `y 1,6; h 1,5`):

| ID | x | w | Tiêu đề (18 pt đậm `blue`) | Nội dung (16 pt `ink`) |
|---|---|---|---|---|
| 6a | 0,6 | 5,55 | `Vấn đề` | `Chỉ 2.887 trong 94.983 khách (khoảng 3%) mua từ 2 lần. Frequency gần như luôn bằng 1, không chia phân vị được.` |
| 6b | 7,18 | 5,55 | `Cách xử lý` | `Thay F bằng cờ mua lại và điểm đánh giá trung bình. Giữ Recency và Monetary, chuẩn hóa rồi chạy K-Means.` |

Tiêu đề thẻ tại `y 1,7` (cách mép trên thẻ 0,1), nội dung tại `y 2,15`, `h 0,9`, đệm 0,2. **Mũi tên 6c:** hình mũi tên phải, tô `muted`, `x 6,25; y 2,15; w 0,83; h 0,4`.

**Bảng 6d** (`x 0,6; y 3,3; w 12,133`; cột: `w 3,4` (`Phân khúc`), `w 1,5` (`Số khách`, canh phải), `w 1,1` (`Tỷ lệ`, canh phải), `w 1,7` (`Recency TB (ngày)`, canh phải), `w 1,6` (`Chi tiêu TB`, canh phải), `w 1,5` (`Review TB`, canh phải), `w 1,333` (`Mua lại`, canh phải); hàng tiêu đề cao 0,7; 3 hàng cao 0,65, kết thúc `y 5,95`). Cột 1 gồm hai dòng: tên phân khúc (16 pt đậm `ink`) và mô tả (14 pt `muted`):

| Phân khúc | Mô tả | Số khách | Tỷ lệ | Recency TB (ngày) | Chi tiêu TB | Review TB | Mua lại |
|---|---|---|---|---|---|---|---|
| `Khách mới` | `mua 1 lần, hài lòng` | `71.792` | `75,6%` | `242,5` | `134,8` | `4,75` | `0%` |
| `Khách ngủ đông` | `mua 1 lần, không hài lòng` | `20.300` | `21,4%` | `248,5` | `149,5` | `1,89` | `0%` |
| `Khách giá trị cao` | `mua lại, chi tiêu cao` | `2.891` | `3,0%` | `226,6` | `271,1` | `4,17` | `99,9%` |

Ô `1,89` in đậm `red`; ô `4,75` in đậm `green`; ô `271,1` in đậm `blue`.

**Ghi chú về tên phân khúc:** tên dùng đúng như dashboard hiện tại. Nếu tên được đổi trong code (theo `docs/REVIEW_VY.md` mục 2), đổi cả ba nhãn ở slide này và slide B2 cho khớp. Dòng mô tả trong cột 1 đã mô tả đúng bản chất của từng nhóm.

**Dòng ghi chú 6e:** `x 0,6; y 6,1; w 12,133; h 0,7`, 16 pt `ink`: `K = 3, silhouette 0,411 (mức trung bình). K = 2 có silhouette cao hơn (0,681) nhưng chỉ cho 2 nhóm, không đủ để đề xuất hành động riêng.`

**Ghi chú diễn giả:** Điểm cần nói rõ là với dữ liệu Olist, Frequency kiểu RFM cổ điển không dùng được vì khoảng 97% khách chỉ mua một lần. Em thay bằng cờ mua lại và điểm đánh giá trung bình. K-Means với K bằng 3 cho ba nhóm: nhóm mua một lần và hài lòng chiếm 75,6%, nhóm mua một lần nhưng không hài lòng chiếm 21,4%, và nhóm mua lại chỉ 3%. Hai nhóm đầu có recency gần như nhau, chỉ khác nhau ở điểm đánh giá. Silhouette 0,411 là mức trung bình, và K bằng 2 có silhouette cao hơn nhưng chỉ cho hai nhóm nên em chọn K bằng 3.

---

### Slide 7 – DSS 3: Mô hình what-if (50 giây)

**Layout:** hai thẻ cạnh nhau (mỗi thẻ có nhãn loại căn cứ, công thức và bảng ví dụ), banner lưu ý ở dưới.
**Tiêu đề (T):** `DSS 3: Mô hình what-if`

**Hai thẻ** (thẻ chuẩn `y 1,6; w 5,9; h 4,2`, kết thúc `y 5,8`; `x 0,6` và `x 6,833`). Toạ độ bên trong thẻ là tương đối so với góc trên trái của thẻ:
- Nhãn loại căn cứ: `+0,25; +0,2`, `w 2,8`, `h 0,4`.
- Tiêu đề: `+0,25; +0,7`, `w 5,4`, `h 0,45`, 20 pt đậm `ink`.
- Công thức: `+0,25; +1,2`, `w 5,4`, `h 0,4`, 14 pt phông đơn cách `muted`.
- Bảng ví dụ: `+0,25; +1,75`, `w 5,4`; hàng tiêu đề cao 0,5; 3 hàng cao 0,5; chữ 16 pt; cột canh phải trừ cột 1.

| | Thẻ trái | Thẻ phải |
|---|---|---|
| Nhãn | `SỐ ĐO THỰC TẾ` (nền `green`, chữ trắng) | `GIẢ ĐỊNH CỦA NGƯỜI DÙNG` (nền `amber`, chữ `ink`) |
| Tiêu đề | `What-if 1: giảm giao trễ` | `What-if 2: khuyến mãi` |
| Công thức | `điểm = p × 2,55 + (1 − p) × 4,21` | `DT mới = DT nền × (1 − d) × (1 + e × d)` |
| Cột bảng | `Tỷ lệ trễ` (`w 2,0`), `Điểm TB dự kiến` (`w 1,9`), `Thay đổi` (`w 1,5`) | `Giảm giá` (`w 1,4`), `Co giãn` (`w 1,4`), `Doanh thu` (`w 2,6`) |
| Hàng 1 | `7,91% (hiện tại)` · `4,079` · `+0,000` | `10%` · `1,0` · `−1,00%` |
| Hàng 2 | `1,91%` · `4,178` · `+0,100` | `10%` · `2,0` · `+8,00%` |
| Hàng 3 | `0%` · `4,210` · `+0,131` | `20%` · `1,5` · `+4,00%` |

Trong thẻ phải, thêm dòng mô tả dưới bảng, trong thẻ phải: `+0,25; +3,8; w 5,4; h 0,35`, 14 pt `muted`: `e là độ co giãn. Danh mục health_beauty, doanh thu nền 1.255.695`. Ô `−1,00%` in `red`; ô `+8,00%` và `+4,00%` in `green`. Trong thẻ trái, các ô `Thay đổi` in `green`.

**Banner 7a:** `x 0,6; y 5,95; w 12,133; h 0,85`, nền `amber-light`, chữ 16 pt `ink`, canh giữa cả hai chiều. Dòng 1 (đậm): `Mô hình 1 dựa trên chênh lệch đo được trong DW. Mô hình 2 dựa trên giả định.` Dòng 2: `Độ co giãn do người dùng nhập, kết quả chỉ minh họa kịch bản, không phải dự báo.`

**Ghi chú diễn giả:** Mô hình what-if thứ nhất dựa trên chênh lệch đo được trong kho dữ liệu: đơn trễ 2,55 điểm, đơn đúng hạn 4,21 điểm. Nếu giảm tỷ lệ giao trễ từ 7,91% xuống 1,91% thì điểm trung bình tăng khoảng 0,1. Đây là phép nội suy, không phải mô hình nhân quả. Mô hình thứ hai tính doanh thu khi giảm giá, nhưng độ co giãn do người dùng nhập, nên em ghi cảnh báo trên giao diện mỗi lần hiển thị kết quả. Ví dụ giảm 10% với co giãn 1,0 thì doanh thu giảm 1%, với co giãn 2,0 thì tăng 8%.

---

### Slide 8 – Demo trực tiếp (60 giây)

**Layout:** hàng 5 bước, khối lệnh chạy, hai thẻ chuẩn bị và dự phòng.
**Tiêu đề (T):** `Demo trực tiếp`

**5 thẻ bước** (thẻ chuẩn, `y 1,6`, `w 2,25`, `h 1,9`, `x = 0,6; 3,07; 5,54; 8,01; 10,48`). Mỗi thẻ có huy hiệu tròn (đường kính 0,5, nền `blue`, số trắng đậm 18 pt) tại `x thẻ +0,2; y 1,75`; tiêu đề 18 pt đậm `ink` (`x thẻ +0,2; y 2,35; w 1,85; h 0,45`); mô tả 14 pt `muted` (`x thẻ +0,2; y 2,8; w 1,85; h 0,6`):

| Thẻ | Số | Tiêu đề | Mô tả |
|---|---|---|---|
| 8a | 1 | `Tổng quan` | `5 chỉ số KPI` |
| 8b | 2 | `OLAP` | `Drill-down và dice` |
| 8c | 3 | `Giao hàng` | `Trễ và đúng hạn` |
| 8d | 4 | `Dự báo, RFM` | `So sánh hai mô hình` |
| 8e | 5 | `What-if` | `Giảm tỷ lệ giao trễ` |

**Khối lệnh 8f:** `x 0,6; y 3,8; w 12,133; h 0,9`, hình chữ nhật bo góc 0,12, nền `ink`, chữ `#E5E7EB` 20 pt phông đơn cách, đệm trái 0,3, canh giữa theo chiều dọc: `streamlit run src/app/app.py`.

**Hai thẻ** (thẻ chuẩn, `y 5,0`, `w 5,9`, `h 1,8`, `x 0,6` và `x 6,833`; tiêu đề thẻ 18 pt đậm `blue` tại `+0,25; +0,15`; nội dung 16 pt `ink` tại `+0,25; +0,65`, `w 5,4`, `h 1,0`):

| ID | Tiêu đề | Nội dung |
|---|---|---|
| 8g | `Trước khi demo` | `Chạy thử trên máy sẽ dùng. Kiểm tra olist_dw.db đã build. Chuẩn bị sẵn vài lựa chọn bang và danh mục cho dice.` |
| 8h | `Phương án dự phòng` | `Video demo quay sẵn (1 đến 2 phút), mở ngay nếu máy hoặc mạng lỗi.` |

**Ghi chú diễn giả:** Bây giờ em demo trực tiếp, đi nhanh qua bốn trang rồi dừng ở trang DSS. Em bắt đầu từ Tổng quan, sang OLAP để drill-down một năm và chọn một khối dice, sang trang Giao hàng, sau đó xem dự báo và phân khúc, cuối cùng kéo thanh trượt what-if giao trễ. Nếu có sự cố kỹ thuật, em có video quay sẵn.

---

### Slide 9 – Hạn chế và hướng phát triển (30 giây)

**Layout:** giống slide 10 của phần A. Hai thẻ cột, banner ở dưới.
**Tiêu đề (T):** `Hạn chế và hướng phát triển`

| ID | Thành phần | x | y | w | h | Style |
|---|---|---|---|---|---|---|
| 9a | Thẻ trái | 0,6 | 1,6 | 5,9 | 4,1 | Thẻ chuẩn; dải màu mỏng ở mép trên (`h 0,08`, tô `amber`) |
| 9b | Thẻ phải | 6,833 | 1,6 | 5,9 | 4,1 | Thẻ chuẩn; dải màu mỏng ở mép trên (`h 0,08`, tô `green`) |
| 9c | Banner | 0,6 | 6,0 | 12,133 | 0,8 | Nền `blue-light`, chữ 18 pt đậm `ink`, canh giữa cả hai chiều |

Trong mỗi thẻ: tiêu đề `+0,25; +0,25` (20 pt đậm `ink`), gạch đầu dòng ở `+0,25; +0,9`, `w 5,4`, 18 pt `ink`, cách dòng 0,12 inch.

**Thẻ trái:** tiêu đề `Hạn chế`
- `Chuỗi chỉ 20 tháng, chưa bắt được mùa vụ`
- `Holt hiện kém baseline`
- `F trong RFM bị thay thế, không phải RFM kinh điển`
- `Độ co giãn của what-if khuyến mãi là giả định`

**Thẻ phải:** tiêu đề `Hướng phát triển`
- `Thêm dữ liệu nhiều năm để dùng Holt-Winters`
- `Ghi nhận giá khuyến mãi để ước lượng độ co giãn`
- `Thử mô hình dự đoán nguy cơ giao trễ`

**Banner 9c:** `Các hạn chế đều đến từ đặc điểm dữ liệu và đã ghi rõ trên giao diện và trong báo cáo`

**Ghi chú diễn giả:** Các hạn chế chính là chuỗi thời gian ngắn nên chưa bắt được mùa vụ, F trong RFM bị thay thế, và độ co giãn trong what-if khuyến mãi là giả định. Em đã ghi cả ba trên giao diện và trong báo cáo. Hướng phát triển là thêm dữ liệu nhiều năm, ghi nhận giá khuyến mãi thật để ước lượng độ co giãn, và thử mô hình dự đoán nguy cơ giao trễ.

---

### Slide 10 – Kết luận và Q&A (30 giây)

**Layout:** 3 thẻ tóm tắt, banner cảm ơn ở dưới.
**Tiêu đề (T):** `Kết luận`

**3 thẻ** (thẻ chuẩn, `y 1,6`, `w 3,8`, `h 3,9`, `x = 0,6; 4,765; 8,93`; tiêu đề 20 pt đậm `blue`, nội dung 18 pt `ink`, đệm 0,2):

| ID | Tiêu đề | Nội dung |
|---|---|---|
| 10a | `Dashboard` | `5 trang, đủ 5 phép toán OLAP, đọc từ một nguồn duy nhất là kho dữ liệu.` |
| 10b | `Ba mô hình DSS` | `Dự báo, phân khúc khách hàng và what-if. Mỗi mô hình có số liệu đánh giá và hạn chế nêu rõ.` |
| 10c | `Trung thực về kết quả` | `Holt kém baseline, F bị thay thế, độ co giãn là giả định. Cả ba đều được ghi trên giao diện.` |

**Banner 10d:** `x 0,6; y 5,85; w 12,133; h 0,9`, nền `blue`, chữ trắng 24 pt đậm, canh giữa cả hai chiều: `Cảm ơn thầy và các bạn. Xin mời đặt câu hỏi.`

**Ghi chú diễn giả:** Em xin tóm tắt: dashboard có đủ năm phép toán OLAP, ba thành phần DSS đều chạy được với số liệu đánh giá thật, và các hạn chế được nêu rõ. Em xin cảm ơn thầy và các bạn, em sẵn sàng trả lời câu hỏi.

---

## 5. Phụ lục (ẩn khi trình bày, đặt sau slide 10)

Đánh dấu cả hai slide là **ẩn** (hidden) nếu công cụ hỗ trợ; nếu không thì đặt ở cuối bộ và ghi tiêu đề có tiền tố `Phụ lục`. Dùng khung chung (T, TA, F1, F2).

### Slide B1 – Phụ lục B1: Câu hỏi dự kiến
**Tiêu đề (T):** `Phụ lục B1: Câu hỏi dự kiến`

**Bảng** (`x 0,6; y 1,6; w 12,133`; cột: `x 0,6 w 4,6` (`Câu hỏi`, 14 pt đậm), `x 5,2 w 7,533` (`Trả lời ngắn`, 14 pt); hàng tiêu đề cao 0,45; 6 hàng cao 0,78, kết thúc `y 6,73`):

| Câu hỏi | Trả lời ngắn |
|---|---|
| `Vì sao F trong RFM gần như luôn bằng 1?` | `Chỉ 2.887 trong 94.983 khách (khoảng 3%) mua từ 2 lần. Thay F bằng cờ mua lại và điểm đánh giá trung bình, vẫn tách được 3 nhóm.` |
| `Vì sao K = 3 trong khi K = 2 có silhouette cao hơn?` | `K = 2 chỉ cho 2 nhóm, quá ít để đề xuất hành động riêng. Trong khoảng 3 đến 4, K = 3 tốt nhất (0,411, mức trung bình).` |
| `Vì sao không dùng Holt-Winters có mùa vụ?` | `Chuỗi 20 tháng, chưa đủ hai chu kỳ năm để ước lượng mùa vụ. Holt hiện còn kém baseline (MAPE 32,24% so với 7,85%).` |
| `What-if khuyến mãi có đáng tin không?` | `Không phải dự báo. Độ co giãn do người dùng nhập, chỉ minh họa kịch bản. Giao diện luôn hiển thị cảnh báo.` |
| `Dashboard có đọc trực tiếp CSV không?` | `Không. Chỉ đọc olist_dw.db qua queries.py, dùng tham số ? và cache bằng st.cache_data.` |
| `Vì sao star schema, và vì sao loại đơn hủy khi tính doanh thu?` | `Star schema cho truy vấn OLAP nhanh và dễ hiểu. Đơn canceled và unavailable không tạo doanh thu thật; quy ước này dùng thống nhất ở dashboard và DSS.` |

### Slide B2 – Phụ lục B2: Chọn K và hành động đề xuất
**Tiêu đề (T):** `Phụ lục B2: Chọn K và hành động đề xuất`

- **Bảng K (B2a):** `x 0,6; y 1,6; w 4,8`; cột: `w 1,2` (`K`, giữa), `w 1,9` (`Inertia`, canh phải), `w 1,7` (`Silhouette`, canh phải); hàng tiêu đề cao 0,5; 5 hàng cao 0,5 (kết thúc `y 4,6`); chữ 16 pt. Hàng `K = 3` tô nền `orange-light`, chữ đậm.

| K | Inertia | Silhouette |
|---|---|---|
| `2` | `283.974,6` | `0,681` |
| `3` | `208.709,2` | `0,411` |
| `4` | `153.541,4` | `0,399` |
| `5` | `108.683,3` | `0,422` |
| `6` | `95.277,0` | `0,430` |

- **Chú thích B2b:** `x 0,6; y 4,8; w 4,8; h 0,9`, 14 pt `muted`: `Silhouette tính trên mẫu 5.000 khách. Mô-đun giới hạn K trong khoảng 3 đến 4.`
- **Bảng hành động (B2c):** `x 5,8; y 1,6; w 6,933`; cột: `w 2,4` (`Phân khúc`), `w 4,533` (`Hành động đề xuất`); hàng tiêu đề cao 0,5; 3 hàng cao 1,0 (kết thúc `y 5,1`); chữ 16 pt:

| Phân khúc | Hành động đề xuất |
|---|---|
| `Khách giá trị cao` | `Chăm sóc VIP, ưu đãi độc quyền, giao hàng ưu tiên` |
| `Khách mới` | `Gửi voucher cho đơn thứ hai, gợi ý sản phẩm liên quan` |
| `Khách ngủ đông` | `Khảo sát lý do không hài lòng, chiến dịch giành lại khách` |

---

## 6. Danh sách kiểm tra trước khi xuất (công cụ AI và người dùng cùng kiểm)

1. Đủ **10 slide chính + 2 phụ lục**, đúng thứ tự trong Mục 3.
2. Không có chữ tràn khung, không có hai khối chồng lấn, mọi khối nằm trong vùng an toàn.
3. Không có chữ nào nhỏ hơn mức tối thiểu: nội dung 16 pt, chú thích 14 pt, footer 12 pt. Nếu thiếu chỗ thì rút câu, không giảm cỡ chữ.
4. Tiêu đề mọi slide đứng **cùng vị trí**, một dòng, cùng vị trí với bộ slide phần A.
5. Tiếng Việt hiển thị đúng dấu (không có ô vuông thay chữ).
6. Chỉ dùng màu trong Mục 2.1; xanh lá, đỏ, vàng dùng đúng ngữ nghĩa ở Mục 2.1.
7. Mọi số liệu khớp **Mục 7**. Đặc biệt không làm tròn lại các số: `13,49 triệu`, `98.199`, `7,91%`, `69.432`, `281.179`, `0,411`, `94.983`.
8. **Biểu đồ slide 4 và 5:** nét đường mảnh (2,5 pt), chấm nhỏ (6 pt), không có khối màu lớn che biểu đồ; đường Thực tế có 20 điểm, đường Baseline và Holt chỉ có 4 điểm cuối.
9. Mỗi con số tô màu nằm **trong ô bảng của nó**; không có hộp chữ nổi chồng lên bảng; không có chữ nào tràn ra ngoài thẻ hoặc ô chứa nó.
10. Chữ, bảng, biểu đồ đều là đối tượng chỉnh sửa được (không dán thành ảnh). Riêng khung ảnh chụp màn hình ở slide 3 chỉ là khung giữ chỗ.
11. Không có animation, chuyển cảnh, ảnh stock hay emoji.
12. Tổng thời lượng theo ghi chú diễn giả khoảng 430 giây.

---

## 7. Bảng số liệu gốc (nguồn: `data/processed/olist_dw.db` và các mô-đun `src/dss/`, đã chạy lại ngày 14/11/2026)

| Số liệu | Giá trị | Dùng ở slide |
|---|---|---|
| Doanh thu (loại đơn canceled và unavailable) | 13.494.400,74 (13,49 triệu) | 3 |
| Số đơn hàng | 98.199 | 3 |
| Giá trị đơn trung bình | 137,42 | 3 |
| Điểm đánh giá trung bình | 4,04 | 3 |
| Tỷ lệ giao trễ | 7,91% | 3, 7 |
| Doanh thu / điểm đánh giá bang SP | 5,17 triệu / 4,14 | 4 |
| Doanh thu / điểm đánh giá bang RJ | 1,81 triệu / 3,82 | 4 |
| Doanh thu / điểm đánh giá bang MG | 1,57 triệu / 4,09 | 4 |
| Cơ cấu thanh toán: thẻ tín dụng / boleto / voucher / thẻ ghi nợ | 78,9% / 17,6% / 2,1% / 1,4% | 4 |
| Điểm đánh giá TB giao trễ / đúng hạn hoặc sớm | 2,55 / 4,21 | 4, 7 |
| Baseline: MAE / MAPE | 69.432,04 / 7,85% | 5, B1 |
| Holt: MAE / MAPE | 281.179,04 / 32,24% | 5, B1 |
| Dự báo tháng kế tiếp (Holt) và khoảng tin cậy 95% | 854.929,55 (643.623,52 đến 1.066.235,57) | 5 |
| Dự báo tháng kế tiếp (baseline, trung bình 3 tháng cuối) | 863.389,97 | 5 |
| Dự báo baseline trên tập kiểm tra (mỗi tháng) | 937.513 | 5 |
| Dự báo Holt trên tập kiểm tra (nghìn) | 1.093; 1.149; 1.205; 1.261 | 5 |
| Số khách phân khúc / khách mua lại | 94.983 / 2.887 (khoảng 3%) | 6, B1 |
| Silhouette theo K = 2, 3, 4, 5, 6 | 0,681; 0,411; 0,399; 0,422; 0,430 | 6, B2 |
| Phân khúc Khách mới | 71.792 (75,6%), recency 242,5, chi tiêu 134,8, review 4,75, mua lại 0% | 6 |
| Phân khúc Khách ngủ đông | 20.300 (21,4%), recency 248,5, chi tiêu 149,5, review 1,89, mua lại 0% | 6 |
| Phân khúc Khách giá trị cao | 2.891 (3,0%), recency 226,6, chi tiêu 271,1, review 4,17, mua lại 99,9% | 6 |
| What-if giao trễ: điểm dự kiến khi trễ 7,91% / 1,91% / 0% | 4,079 / 4,178 / 4,210 (thay đổi 0 / +0,100 / +0,131) | 7 |
| What-if khuyến mãi, doanh thu nền health_beauty | 1.255.695 | 7 |
| What-if khuyến mãi: (10%, co giãn 1,0) / (10%, 2,0) / (20%, 1,5) | −1,00% / +8,00% / +4,00% | 7 |

**Chuỗi doanh thu theo tháng (nghìn), dùng cho biểu đồ slide 5:**

| Tháng | 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | 09 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2017 | 120 | 245 | 368 | 354 | 503 | 430 | 492 | 568 | 621 | 660 | 1004 | 742 |
| 2018 | 945 | 838 | 981 | 994 | 993 | 863 | 878 | 849 | | | | |

---

## 8. Việc người dùng cần tự làm sau khi sinh slide

1. Điền `[Họ tên – MSSV]` ở slide 1.
2. Chèn ảnh chụp màn hình trang OLAP vào khung ở slide 3 (khung 6,9 × 3,65 inch). Tùy chọn: chụp thêm các trang khác để dùng cho phụ lục hoặc báo cáo.
3. Nếu tên phân khúc RFM được đổi trong code, đổi ba nhãn ở slide 6 và slide B2.
4. Đọc từng ghi chú diễn giả và nói thử có bấm giờ (mục tiêu 7 phút 10 giây, tối đa 8 phút).
5. Quay video demo dự phòng và đặt đường dẫn vào báo cáo.
6. Ghép với bộ slide phần A: bỏ hoặc giữ slide 1 làm trang chia phần, kiểm tra số slide tự cập nhật và footer.
7. Xuất **PDF** (đề bài yêu cầu slide dạng PDF) và đặt vào thư mục `slides/`.
