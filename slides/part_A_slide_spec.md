# Đặc tả sinh slide – Phần A (Data & DW)

Dùng cho công cụ AI sinh slide. Tài liệu này mô tả **từng slide**: bố cục, toạ độ, cỡ chữ, màu, nội dung chữ chính xác, dữ liệu biểu đồ và ghi chú diễn giả. Công cụ chỉ cần làm đúng theo, không cần tự quyết định bố cục.

- Người trình bày: A (phần kho dữ liệu, ETL, OLAP). Thời lượng mục tiêu **7 phút 10 giây** (430 giây), giới hạn của đề bài là 7 đến 8 phút.
- Số slide: **10 slide chính + 2 slide phụ lục** (phụ lục chỉ dùng khi trả lời Q&A, không trình bày).
- Phần B (Vỹ) làm bộ slide riêng. Hai bộ dùng **cùng Mục 2 (hệ thiết kế)** để khi ghép trông như một bộ.

---

## 0. Cách dùng

Dán toàn bộ file này vào công cụ AI cùng câu lệnh sau:

> Hãy tạo bản trình chiếu đúng theo đặc tả dưới đây. Giữ nguyên toạ độ, cỡ chữ, màu và nội dung chữ. Không thêm, bớt hay đổi bất kỳ số liệu nào. Không thêm ảnh, icon hay hình trang trí ngoài những gì được mô tả. Nếu chữ bị tràn khung, hãy rút gọn câu chứ không giảm cỡ chữ dưới mức tối thiểu. Xuất ra PPTX có thể chỉnh sửa (mọi chữ và bảng là đối tượng thật, không phải ảnh) và PDF. Kiểm tra theo danh sách ở Mục 6 trước khi xuất.

Nếu công cụ không đặt được toạ độ chính xác: giữ **thứ tự, phân cấp và tỷ lệ** giữa các khối như trong đặc tả, không tự sáng tạo bố cục khác.

---

## 1. Quy ước chung

| Mục | Giá trị |
|---|---|
| Tỷ lệ | 16:9, **13,333 × 7,5 inch** (1920 × 1080 px) |
| Đơn vị toạ độ | inch, gốc (0,0) ở góc trên trái; mỗi khối ghi `x, y, w, h` |
| Ngôn ngữ | Tiếng Việt, **bắt buộc hiển thị đúng dấu** (kiểm tra không có ô vuông thay chữ) |
| Số | Dấu chấm ngăn nghìn, dấu phẩy thập phân (ví dụ `112.650`, `4,21`). Giữ nguyên như trong đặc tả |
| Hiệu ứng | Không animation, không chuyển cảnh |
| Ảnh / icon | Không dùng ảnh stock, không emoji. Chỉ dùng hình khối và biểu đồ được mô tả |

## 2. Hệ thiết kế (dùng chung với phần B)

### 2.1 Màu

| Tên | Hex | Dùng cho |
|---|---|---|
| `ink` | `#1F2937` | Chữ chính |
| `muted` | `#6B7280` | Chữ phụ, chú thích, footer |
| `bg` | `#FFFFFF` | Nền slide |
| `panel` | `#F3F4F6` | Nền thẻ (card) |
| `line` | `#E5E7EB` | Đường kẻ, lưới biểu đồ |
| `blue` | `#3465A4` | **Chiều (dimension)**, tiêu đề phụ, nhấn chính |
| `blue-light` | `#DBEAFE` | Nền chiều, nền banner |
| `orange` | `#D66028` | **Bảng fact**, điểm nhấn số liệu |
| `orange-light` | `#FDEBE3` | Nền thân bảng fact |
| `green` | `#2E7D32` | Đạt, tốt |
| `red` | `#C62828` | Xấu, giao trễ |
| `amber-light` | `#FEF3C7` | Khung lưu ý |

Quy tắc ngữ nghĩa: **cam = fact, xanh dương = chiều** xuyên suốt cả bộ slide. Không dùng màu ngoài bảng này.

### 2.2 Phông chữ và cỡ chữ

- Chữ thường: **Inter** (dự phòng: Segoe UI, Arial). Phải hỗ trợ tiếng Việt.
- Chữ đơn cách (tên bảng, cột, code): **JetBrains Mono** (dự phòng: Consolas, Courier New).

| Vai trò | Cỡ | Kiểu |
|---|---|---|
| Tiêu đề slide | 30 pt | Đậm, `ink`, căn trái, **một dòng**, tối đa 46 ký tự |
| Tiêu đề thẻ / tiêu đề phụ | 20 pt | Đậm |
| Nội dung chính | 18 đến 20 pt | Thường |
| Chữ trong bảng, mô tả thẻ | 16 pt | Thường |
| Chú thích, nhãn nhỏ | **14 pt (tối thiểu)** | `muted` |
| Footer | 12 pt | `muted` |
| Số lớn (KPI) | 36 đến 44 pt | Đậm |

Giãn dòng 1,2 (đoạn văn) và 1,3 (danh sách). Căn trái mọi đoạn chữ; số trong bảng căn phải hoặc giữa như ghi trong từng slide.

### 2.3 Lưới và khung chung (mọi slide trừ slide 1)

Nội dung chỉ nằm trong **vùng an toàn**: `x 0,6 đến 12,733` và `y 0,4 đến 7,3`.

| ID | Thành phần | x | y | w | h | Style |
|---|---|---|---|---|---|---|
| T | Tiêu đề slide | 0,6 | 0,4 | 12,133 | 0,8 | 30 pt đậm `ink`, canh giữa theo chiều dọc |
| TA | Gạch nhấn dưới tiêu đề | 0,6 | 1,25 | 1,2 | 0,06 | Tô `blue`, không viền |
| F1 | Footer trái | 0,6 | 7,05 | 9,0 | 0,3 | 12 pt `muted`: `CO4031 · Bài tập lớn · Phần A: Kho dữ liệu` |
| F2 | Số slide | 11,733 | 7,05 | 1,0 | 0,3 | 12 pt `muted`, căn phải, tự đánh số |

**Vùng nội dung:** `x 0,6 đến 12,733`, `y 1,6 đến 6,8` (rộng 12,133, cao 5,2).

Các cách chia cột chuẩn:
- 2 cột: `x = 0,6` và `x = 6,833`, mỗi cột rộng `5,9` (khe 0,333).
- 3 cột: `x = 0,6; 4,765; 8,93`, mỗi cột rộng `3,8` (khe 0,365).
- Khoảng cách tối thiểu giữa hai khối: 0,3 inch. **Không được chồng lấn.**

### 2.4 Thành phần dùng lại

- **Thẻ (card):** hình chữ nhật bo góc bán kính 0,12 inch, nền `panel`, không viền, đệm trong 0,2 inch.
- **Bảng:** hàng tiêu đề nền `blue`, chữ trắng đậm 16 pt; hàng nội dung xen kẽ `bg` và `panel`; không kẻ viền dọc; đệm ô 0,12 inch; chữ canh giữa theo chiều dọc.
- **Banner:** hình chữ nhật chiều rộng 12,133 inch, nền theo từng slide, chữ canh giữa theo chiều dọc.
- **Dấu đạt:** ký tự `✓` màu `green`, đậm.

---

## 3. Tổng quan thời lượng

| # | Slide | Giây |
|---|---|---|
| 1 | Tiêu đề phần A | 15 |
| 2 | Bài toán và dữ liệu nguồn | 45 |
| 3 | Kiến trúc: từ CSV đến phân tích | 40 |
| 4 | Star schema | 60 |
| 5 | Bốn quyết định thiết kế chính | 45 |
| 6 | Quy trình ETL | 55 |
| 7 | Kết quả nạp và kiểm tra chất lượng | 30 |
| 8 | Năm phép OLAP | 50 |
| 9 | Kho dữ liệu cho thấy điều gì? | 55 |
| 10 | Hạn chế và hướng phát triển | 35 |
| | **Tổng** | **430 (7 phút 10 giây)** |
| A1, A2 | Phụ lục (ẩn, chỉ dùng cho Q&A) | – |

---

## 4. Đặc tả từng slide

### Slide 1 – Tiêu đề phần A (15 giây)

**Layout:** nền trắng, không footer, không số slide.

| ID | Thành phần | x | y | w | h | Nội dung / style |
|---|---|---|---|---|---|---|
| 1a | Dải màu bên trái | 0 | 0 | 0,35 | 7,5 | Tô `blue` |
| 1b | Nhãn nhỏ | 1,0 | 1,4 | 11,3 | 0,4 | `CO4031 · KHO DỮ LIỆU VÀ HỆ HỖ TRỢ QUYẾT ĐỊNH · HK261`, 16 pt `muted`, chữ hoa |
| 1c | Tiêu đề | 1,0 | 2,2 | 11,3 | 1,9 | `Kho dữ liệu thương mại điện tử Olist`, 44 pt đậm `ink`, tối đa 2 dòng |
| 1d | Phụ đề | 1,0 | 4,2 | 11,3 | 0,6 | `Phần A: Phân tích yêu cầu, thiết kế kho dữ liệu, ETL và OLAP`, 24 pt `blue` |
| 1e | Gạch nhấn | 1,0 | 5,2 | 2,0 | 0,04 | Tô `orange` |
| 1f | Người trình bày | 1,0 | 5,4 | 11,3 | 0,5 | `Người trình bày: [Họ tên – MSSV]`, 20 pt `ink` |
| 1g | Nhóm | 1,0 | 5,95 | 11,3 | 0,5 | `Nhóm: [Họ tên A – MSSV] · [Họ tên Vỹ – MSSV]`, 16 pt `muted` |

Giữ nguyên các dấu ngoặc vuông, **không tự bịa tên hay mã số**; người dùng sẽ tự điền.

**Ghi chú diễn giả:** Em xin trình bày phần kho dữ liệu của nhóm: từ phân tích yêu cầu, thiết kế, quy trình ETL đến các phép phân tích OLAP. Phần dashboard và mô hình hỗ trợ quyết định sẽ do bạn Vỹ trình bày tiếp.

---

### Slide 2 – Bài toán và dữ liệu nguồn (45 giây)

**Layout:** hai cột. Cột trái là danh sách câu hỏi, cột phải là 4 thẻ số liệu và ghi chú nguồn.
**Tiêu đề (T):** `Bài toán và dữ liệu nguồn`

| ID | Thành phần | x | y | w | h | Nội dung / style |
|---|---|---|---|---|---|---|
| 2a | Tiêu đề phụ | 0,6 | 1,6 | 6,6 | 0,5 | `Ban quản lý sàn thương mại điện tử cần trả lời:`, 20 pt đậm `blue` |
| 2b | Danh sách đánh số | 0,6 | 2,2 | 6,6 | 4,4 | 5 đoạn, 20 pt `ink`, cách đoạn 0,15 inch; số thứ tự đậm `blue` (nội dung bên dưới) |
| 2c | Thẻ 1 | 7,6 | 1,6 | 2,45 | 1,5 | Số `99.441` (36 pt đậm `blue`) + nhãn `đơn hàng nguồn` (16 pt `muted`) |
| 2d | Thẻ 2 | 10,283 | 1,6 | 2,45 | 1,5 | Số `112.650` + nhãn `dòng hàng bán ra` |
| 2e | Thẻ 3 | 7,6 | 3,333 | 2,45 | 1,5 | Số `8` + nhãn `tệp CSV nguồn` |
| 2f | Thẻ 4 | 10,283 | 3,333 | 2,45 | 1,5 | Số `2016–2018` + nhãn `giai đoạn dữ liệu` |
| 2g | Ghi chú nguồn | 7,6 | 5,15 | 5,133 | 1,6 | 16 pt `muted`, hai đoạn (bên dưới) |

**Nội dung 2b (5 đoạn):**
1. Doanh thu thay đổi thế nào theo thời gian?
2. Danh mục nào mang lại nhiều doanh thu nhất?
3. Doanh thu và mức hài lòng khác nhau ra sao giữa các bang?
4. Khách thanh toán bằng hình thức nào?
5. Giao hàng trễ ảnh hưởng thế nào đến điểm đánh giá?

**Nội dung 2g:**
- Đoạn 1: `8 tệp CSV: đơn hàng, chi tiết đơn, khách hàng, sản phẩm, người bán, thanh toán, đánh giá, bản dịch danh mục.`
- Đoạn 2: `Nguồn: Brazilian E-Commerce Public Dataset by Olist (Kaggle), đã ẩn danh.`

**Ghi chú diễn giả:** Nhóm chọn bài toán thương mại điện tử với bộ dữ liệu Olist của Brazil, khoảng một trăm nghìn đơn hàng thật từ năm 2016 đến 2018. Ban quản lý muốn trả lời nhanh năm câu hỏi này. Dữ liệu gốc là tám bảng CSV giống một cơ sở dữ liệu giao dịch, rất khó tổng hợp theo nhiều chiều, nên cần một kho dữ liệu.

---

### Slide 3 – Kiến trúc: từ CSV đến phân tích (40 giây)

**Layout:** một hàng 4 hộp có mũi tên, nhãn tầng bên dưới, 3 thẻ giải thích ở dưới cùng.
**Tiêu đề (T):** `Kiến trúc: từ CSV đến phân tích`

**Hàng sơ đồ** (mỗi hộp bo góc 0,15 inch, rộng 2,55, cao 1,5, `y = 1,9`; tiêu đề hộp 20 pt đậm, dòng phụ 16 pt, canh giữa cả hai chiều):

| ID | x | Fill | Màu chữ | Tiêu đề hộp | Dòng phụ |
|---|---|---|---|---|---|
| 3a | 0,6 | `panel` | `ink` | `Nguồn dữ liệu` | `8 tệp CSV Olist` |
| 3b | 3,794 | `blue-light` | `ink` | `ETL` | `Python và pandas` |
| 3c | 6,988 | `blue` | trắng | `Kho dữ liệu` | `SQLite, star schema` |
| 3d | 10,182 | `panel` | `ink` | `Phân tích` | `OLAP, dashboard, DSS` |

**Mũi tên** (hình mũi tên phải, tô `muted`, w 0,444, h 0,4, `y = 2,45`): tại `x = 3,25`, `6,444`, `9,638`.

**Nhãn tầng** (14 pt `muted`, canh giữa, `y = 3,5`, `h = 0,35`, `w = 2,55`, cùng `x` với 4 hộp): `Tầng nguồn`, `Tầng ETL`, `Tầng kho dữ liệu`, `Tầng trình bày`.

**3 thẻ giải thích** (thẻ chuẩn, `y = 4,2`, `w = 3,8`, `h = 2,4`, `x = 0,6; 4,765; 8,93`; tiêu đề thẻ 20 pt đậm `blue`, nội dung 18 pt `ink`):

| ID | Tiêu đề | Nội dung |
|---|---|---|
| 3e | `Hướng Kimball` | `Xây một data mart cho chủ đề bán hàng: phạm vi rõ, có kết quả sớm.` |
| 3f | `ROLAP trên SQLite` | `Phép OLAP chạy bằng SQL trên lược đồ quan hệ, không dựng khối dữ liệu tính trước.` |
| 3g | `ETL một lệnh` | `python src/etl/run_etl.py tạo lại toàn bộ kho trong vài giây.` (phần lệnh dùng phông đơn cách) |

**Ghi chú diễn giả:** Hệ thống có bốn tầng: nguồn CSV, ETL bằng Python, kho dữ liệu SQLite, và tầng phân tích. Nhóm đi theo hướng Kimball, tức là xây trước một data mart cho chủ đề bán hàng, vì phạm vi nhỏ và cần có kết quả sớm. Các phép OLAP chạy bằng SQL nên đây là ROLAP. Toàn bộ kho dựng lại được bằng một lệnh.

---

### Slide 4 – Star schema (60 giây)

**Layout:** sơ đồ star schema bên trái (bảng fact cao ở giữa, 3 chiều mỗi bên), bảng chú giải bên phải.
**Tiêu đề (T):** `Star schema của kho dữ liệu`

**Sơ đồ (vùng `x 0,6 đến 8,4`, `y 1,6 đến 6,8`)**

*Bảng fact:* `x 3,3; y 1,6; w 2,4; h 5,2`.
- Đầu bảng (`h 0,6`): nền `orange`, chữ `fact_sales` 20 pt đậm trắng, canh giữa.
- Thân bảng: nền `orange-light`, đệm 0,2, chữ 14 pt. Nội dung từ trên xuống:
  - `SỐ ĐO` (đậm, `orange`), rồi 6 dòng đơn cách: `price`, `freight_value`, `item_total`, `review_score`, `delivery_days`, `delay_days`
  - `CHIỀU SUY BIẾN` (đậm, `orange`), rồi `order_id`
  - `KHÓA NGOẠI` (đậm, `orange`), rồi `6 khóa tới 6 chiều`
  - Cách giữa các nhóm 0,15 inch.

*Sáu bảng chiều:* mỗi bảng `w 2,3; h 1,4`. Đầu bảng `h 0,45` nền `blue`, chữ trắng đậm 16 pt (tên bảng và số dòng). Thân bảng nền `blue-light`, chữ 14 pt `ink`, tối đa 3 dòng.

| Vị trí | x | y | Đầu bảng | Thân bảng |
|---|---|---|---|---|
| Trái, hàng 1 | 0,6 | 1,6 | `dim_date · 774` | `ngày, tháng, quý, năm`; `dùng 2 lần: mua và giao` |
| Trái, hàng 2 | 0,6 | 3,5 | `dim_customer · 96.096` | `customer_unique_id`; `thành phố, bang` |
| Trái, hàng 3 | 0,6 | 5,4 | `dim_payment_type · 5` | `credit_card, boleto,`; `voucher, debit_card` |
| Phải, hàng 1 | 6,1 | 1,6 | `dim_product · 32.951` | `danh mục, cân nặng,`; `kích thước` |
| Phải, hàng 2 | 6,1 | 3,5 | `dim_seller · 3.095` | `thành phố, bang`; `mã bưu chính` |
| Phải, hàng 3 | 6,1 | 5,4 | `dim_order_status · 8` | `delivered, shipped,`; `canceled...` |

*Đường nối:* 6 đoạn thẳng ngang, nét 2 pt, màu `muted`, chạy từ mép bảng chiều tới mép bảng fact tại tâm mỗi hàng. Đường trái: `x 2,9 đến 3,3`. Đường phải: `x 5,7 đến 6,1`. Tung độ `y = 2,3; 4,2; 6,1`.

**Bảng chú giải bên phải** (`x 8,8 đến 12,733`, `w 3,933`):

| ID | y | h | Nội dung / style |
|---|---|---|---|
| 4a | 1,6 | 0,35 | `MỨC HẠT`, 14 pt đậm `orange`, chữ hoa |
| 4b | 1,95 | 1,1 | `1 dòng = 1 sản phẩm trong 1 đơn hàng`, 24 pt đậm `ink` |
| 4c | 3,1 | 0,7 | `112.650`, 40 pt đậm `orange` |
| 4d | 3,8 | 0,35 | `dòng fact`, 16 pt `muted` |
| 4e | 4,3 | 2,0 | 3 gạch đầu dòng 18 pt `ink`: `Gộp lên được theo đơn, ngày, bang, danh mục`; `Chiều ngày dùng 2 lần: ngày mua, ngày giao`; `Mỗi chiều có khóa thay thế` |
| 4f | 6,45 | 0,35 | Chú giải màu: ô vuông 0,2 `orange` tại `x 8,8` + chữ `Bảng fact` (14 pt) tại `x 9,1`; ô vuông 0,2 `blue` tại `x 10,5` + chữ `Bảng chiều` tại `x 10,8` |

**Ghi chú diễn giả:** Đây là star schema. Ở giữa là bảng fact, mỗi dòng là một sản phẩm trong một đơn hàng, đó là mức hạt, tức mức chi tiết nhất có sẵn. Từ đó gộp lên theo đơn, theo ngày, theo bang hay danh mục đều được. Xung quanh là sáu bảng chiều, mô tả đơn hàng theo các góc nhìn: thời gian, khách hàng, sản phẩm, người bán, hình thức thanh toán, trạng thái. Chiều ngày được dùng hai lần, cho ngày mua và ngày giao.

---

### Slide 5 – Bốn quyết định thiết kế chính (45 giây)

**Layout:** lưới thẻ 2×2.
**Tiêu đề (T):** `Bốn quyết định thiết kế chính`

Mỗi thẻ chuẩn `w 5,9; h 2,4`. Vị trí thẻ: `(0,6; 1,6)`, `(6,833; 1,6)`, `(0,6; 4,4)`, `(6,833; 4,4)`.
Trong mỗi thẻ (toạ độ tương đối so với góc trên trái của thẻ):
- Huy hiệu tròn: `+0,25; +0,25`, đường kính 0,5, nền `blue`, số trắng đậm 18 pt, canh giữa.
- Tiêu đề: `+0,95; +0,25`, `w 4,7`, `h 0,5`, 20 pt đậm `ink`, canh giữa theo chiều dọc.
- Nội dung: `+0,25; +0,95`, `w 5,4`, `h 1,3`, 18 pt `ink`.

| Thẻ | Số | Tiêu đề | Nội dung |
|---|---|---|---|
| 5a | 1 | `Mức hạt thấp nhất` | `Chi tiết nhất có sẵn, nên gộp lên theo đơn, ngày, bang hay danh mục đều được.` |
| 5b | 2 | `Khách theo người thật` | `customer_id đổi theo từng đơn; dùng customer_unique_id: 96.096 người thay vì 99.441 mã.` |
| 5c | 3 | `Thanh toán chính của đơn` | `Đơn trả nhiều cách (2.246 đơn): lấy hình thức có số tiền lớn nhất để giữ mức hạt.` |
| 5d | 4 | `Giữ cả đơn hủy trong kho` | `Không xóa khỏi kho; lọc theo trạng thái khi truy vấn để bảo toàn lịch sử.` |

**Ghi chú diễn giả:** Có bốn quyết định đáng nói. Một, chọn mức hạt thấp nhất để không mất thông tin. Hai, trong Olist mã khách thay đổi theo từng đơn, nên em dùng mã người thật, nhờ đó đếm khách chính xác. Ba, một đơn có thể trả bằng nhiều cách, em lấy cách có số tiền lớn nhất làm hình thức chính. Bốn, đơn bị hủy vẫn giữ trong kho và chỉ lọc khi truy vấn, vì kho dữ liệu lưu lịch sử chứ không xóa.

---

### Slide 6 – Quy trình ETL (55 giây)

**Layout:** hàng 3 bước ở trên, bảng "vấn đề và cách xử lý" ở dưới.
**Tiêu đề (T):** `Quy trình ETL`

**Hàng 3 bước** (hình ngũ giác mũi tên phải, nền `blue-light`, `y 1,6`, `w 3,8`, `h 1,25`, `x = 0,6; 4,765; 8,93`). Tiêu đề bước 20 pt đậm `blue`, mô tả 16 pt `ink`, đệm trái 0,25 và chừa 0,5 cho mũi tên bên phải:

| ID | Tiêu đề | Mô tả |
|---|---|---|
| 6a | `1 · Extract` | `Đọc 8 CSV, giữ nguyên mã bưu chính` |
| 6b | `2 · Transform` | `Làm sạch, gộp bảng, tính độ đo` |
| 6c | `3 · Load` | `Nạp chiều trước, fact sau` |

**Bảng 6d** (`x 0,6; y 3,2; w 12,133`; cột: `x 0,6 w 4,4`; `x 5,0 w 5,0`; `x 10,0 w 2,733`; hàng tiêu đề cao 0,5; 5 hàng nội dung mỗi hàng cao 0,55; cột 3 canh giữa):

| Vấn đề | Xử lý | Quy mô |
|---|---|---|
| `Một người có nhiều customer_id` | `Gộp theo customer_unique_id` | `99.441 → 96.096` |
| `Đơn không có sản phẩm` | `Loại khỏi bảng fact` | `775 đơn` |
| `Đơn thanh toán nhiều cách` | `Giữ hình thức có số tiền lớn nhất` | `2.246 đơn` |
| `Đơn có nhiều đánh giá` | `Lấy điểm trung bình` | `547 đơn` |
| `Sản phẩm thiếu danh mục` | `Gán nhãn unknown` | `610 sản phẩm` |

**Chú thích 6e:** `x 0,6; y 6,5; w 12,133; h 0,3`, 14 pt `muted`: `Tập lệnh: src/etl/run_etl.py · pandas và sqlite3`.

**Ghi chú diễn giả:** ETL gồm ba bước. Extract đọc tám tệp CSV dưới dạng chuỗi để không mất số không đứng đầu của mã bưu chính. Transform làm sạch và biến đổi, bảng này liệt kê các vấn đề dữ liệu thật và cách xử lý, ví dụ gộp khách theo người thật, hay loại bảy trăm bảy mươi lăm đơn không có sản phẩm. Load nạp các bảng chiều trước rồi mới đến bảng fact để thỏa ràng buộc khóa ngoại.

---

### Slide 7 – Kết quả nạp và kiểm tra chất lượng (30 giây)

**Layout:** hai cột. Trái là bảng số dòng, phải là danh sách kiểm tra và khung lưu ý.
**Tiêu đề (T):** `Kết quả nạp và kiểm tra chất lượng`

**Bảng 7a** (`x 0,6; y 1,6; w 5,9`; cột: `w 3,6` tên bảng (phông đơn cách 16 pt), `w 2,3` số dòng (canh phải); tiêu đề `Bảng` và `Số dòng`; hàng tiêu đề cao 0,5; 7 hàng mỗi hàng cao 0,52; dòng `fact_sales` chữ đậm màu `orange`):

| Bảng | Số dòng |
|---|---|
| `fact_sales` | `112.650` |
| `dim_customer` | `96.096` |
| `dim_product` | `32.951` |
| `dim_seller` | `3.095` |
| `dim_date` | `774` |
| `dim_order_status` | `8` |
| `dim_payment_type` | `5` |

**Chú thích 7b:** `x 0,6; y 5,95; w 5,9; h 0,35`, 14 pt đơn cách `muted`: `python src/etl/run_etl.py`.

**Tiêu đề phải 7c:** `x 6,833; y 1,6; w 5,9; h 0,5`: `8 kiểm tra tự động, đều đạt`, 20 pt đậm `green`.

**Danh sách 7d:** `x 6,833; y 2,2; w 5,9; h 2,2`, 4 dòng 18 pt `ink` có dấu `✓` xanh đứng đầu, cách dòng 0,12 inch:
- `✓ Số dòng fact bằng số dòng nguồn (112.650)`
- `✓ Không có khóa ngoại mồ côi (5 kiểm tra)`
- `✓ Không có giá âm`
- `✓ item_total = price + freight_value`

**Khung lưu ý 7e:** `x 6,833; y 4,6; w 5,9; h 1,4`, nền `amber-light`, đệm 0,25.
- Dòng 1 (16 pt đậm `ink`): `Giá trị NULL được giữ vì có ý nghĩa`
- Dòng 2 (16 pt `ink`): `942 dòng chưa có điểm đánh giá; 3 dòng chưa có thông tin thanh toán.`

**Ghi chú diễn giả:** Sau khi nạp, ETL tự chạy tám kiểm tra chất lượng và dừng lại nếu có kiểm tra nào thất bại. Số dòng fact bằng đúng số dòng nguồn nên không mất và không nhân đôi dòng nào, không có khóa ngoại mồ côi. Một số giá trị thiếu em giữ nguyên vì có ý nghĩa nghiệp vụ, ví dụ đơn chưa có đánh giá.

---

### Slide 8 – Năm phép OLAP (50 giây)

**Layout:** một bảng lớn toàn chiều rộng và một dòng chú thích.
**Tiêu đề (T):** `Năm phép OLAP trên kho dữ liệu`

**Bảng 8a** (`x 0,6; y 1,6; w 12,133`; cột: `x 0,6 w 2,2`; `x 2,8 w 3,6`; `x 6,4 w 6,333`; hàng tiêu đề cao 0,5; 5 hàng mỗi hàng cao 0,8; cột 1 chữ 20 pt đậm `blue`, cột 2 và 3 chữ 16 pt `ink`):

| Phép OLAP | Ý nghĩa | Ví dụ trên dữ liệu Olist |
|---|---|---|
| `Roll-up` | `Gộp lên mức cao hơn (tháng → năm)` | `Doanh thu 2017: 6,11 triệu; 2018 (đến tháng 8): 7,34 triệu` |
| `Drill-down` | `Đi sâu vào chi tiết (năm → quý → tháng)` | `Năm 2017 → tháng 11/2017: đỉnh khoảng 1,0 triệu, trùng dịp Black Friday` |
| `Slice` | `Cố định một chiều (ví dụ: một năm)` | `Năm 2017 theo danh mục: bed_bath_table dẫn đầu (khoảng 498 nghìn)` |
| `Dice` | `Chọn khối con theo nhiều chiều` | `SP và RJ × năm 2018 × 3 danh mục: SP, health_beauty đạt 302 nghìn` |
| `Pivot` | `Xoay chiều thành cột để so sánh` | `health_beauty: 481 nghìn (2017) → 770 nghìn (2018)` |

**Chú thích 8b:** `x 0,6; y 6,3; w 12,133; h 0,4`, 14 pt `muted`: `Hiện thực bằng SQL trên lược đồ quan hệ (ROLAP): src/sql/02_olap_queries.sql`.

**Ghi chú diễn giả:** Năm phép OLAP đều chạy bằng SQL trên kho dữ liệu. Roll-up gộp tháng lên năm. Drill-down đi sâu từ năm 2017 xuống từng tháng, và thấy đỉnh doanh thu vào tháng mười một, trùng dịp Black Friday. Slice cố định một năm để xem theo danh mục. Dice chọn khối con gồm hai bang, một năm và ba danh mục. Pivot xoay năm thành cột để so sánh trực tiếp.

---

### Slide 9 – Kho dữ liệu cho thấy điều gì? (55 giây)

**Layout:** biểu đồ đường lớn bên trái, hai thẻ số liệu bên phải, banner nối sang phần B ở dưới.
**Tiêu đề (T):** `Kho dữ liệu cho thấy điều gì?`

**Biểu đồ 9a** (`x 0,6; y 1,6; w 7,0; h 3,9`):
- Tiêu đề biểu đồ (18 pt đậm `ink`, ngay trong khung, phía trên): `Doanh thu theo tháng (nghìn)`.
- Loại: đường, **một chuỗi**, không chú giải. Đường nét 2,5 pt `blue`, điểm đánh dấu tròn 6 pt `blue`.
- Trục X: nhãn dạng `MM/YYYY`, hiển thị cách 3 nhãn (`01/2017, 04/2017, 07/2017, 10/2017, 01/2018, 04/2018, 07/2018`), 14 pt `muted`.
- Trục Y: từ 0 đến 1.100, bước 250, 14 pt `muted`; lưới ngang nét 0,75 pt `line`; không lưới dọc.
- Điểm nhấn: điểm `11/2017` dùng chấm tròn 10 pt `orange`, kèm nhãn `11/2017: khoảng 1,0 triệu` (14 pt đậm `orange`) đặt phía trên bên trái điểm. Không hiện nhãn dữ liệu ở các điểm khác.
- Dữ liệu (nghìn), theo thứ tự 2017-01 đến 2018-08:
  `120, 245, 368, 354, 503, 430, 492, 568, 621, 660, 1004, 742, 945, 838, 981, 994, 993, 863, 878, 849`

**Chú thích 9b:** `x 0,6; y 5,6; w 7,0; h 0,4`, 14 pt `muted`: `Không vẽ 2016 và tháng 9/2018 vì dữ liệu thưa.`

**Thẻ phải trên 9c** (thẻ chuẩn `x 8,0; y 1,6; w 4,733; h 2,2`):
- Tiêu đề: `x 8,25; y 1,8; w 4,23` `Giao trễ làm tụt điểm đánh giá`, 18 pt đậm `ink`.
- Số trái: `x 8,25; y 2,3; w 2,05; h 0,8`, `2,55`, 44 pt đậm `red`.
- Nhãn trái: `x 8,25; y 3,1; w 2,05; h 0,6`, 14 pt `muted`, hai dòng: `giao trễ` / `(8.714 dòng hàng)`.
- Số phải: `x 10,45; y 2,3; w 2,03; h 0,8`, `4,21`, 44 pt đậm `green`.
- Nhãn phải: `x 10,45; y 3,1; w 2,03; h 0,6`, 14 pt `muted`, hai dòng: `đúng hạn hoặc sớm` / `(101.475 dòng hàng)`.

**Thẻ phải dưới 9d** (thẻ chuẩn `x 8,0; y 4,0; w 4,733; h 2,1`):
- Tiêu đề: `x 8,25; y 4,2; w 4,23`, `Doanh thu tập trung`, 18 pt đậm `ink`.
- 3 gạch đầu dòng 16 pt `ink`, `x 8,25; y 4,7; w 4,23; h 1,3`:
  - `SP: 5,17 / 13,49 triệu (khoảng 38%)`
  - `Thẻ tín dụng: 78,9% doanh thu`
  - `Điểm đánh giá TB: RJ 3,82; SP 4,14`

**Banner 9e:** `x 0,6; y 6,3; w 12,133; h 0,5`, nền `blue-light`, chữ 18 pt đậm `ink`, canh giữa: `Đầu vào cho DSS của Vỹ: dự báo doanh thu, phân khúc khách hàng, what-if giao trễ`.

**Ghi chú diễn giả:** Từ kho dữ liệu, bốn phát hiện chính. Doanh thu tăng đều trong 2017 và đạt đỉnh khoảng một triệu vào tháng mười một. Bang SP chiếm khoảng 38% doanh thu và thẻ tín dụng chiếm gần 79%. Quan trọng nhất, các dòng hàng giao trễ có điểm đánh giá trung bình chỉ 2,55, trong khi giao đúng hạn là 4,21. Những phát hiện này là đầu vào cho các mô hình hỗ trợ ra quyết định của bạn Vỹ.

---

### Slide 10 – Hạn chế và hướng phát triển (35 giây)

**Layout:** hai thẻ cột, banner chuyển giao ở dưới.
**Tiêu đề (T):** `Hạn chế và hướng phát triển`

| ID | Thành phần | x | y | w | h | Style |
|---|---|---|---|---|---|---|
| 10a | Thẻ trái | 0,6 | 1,6 | 5,9 | 4,1 | Thẻ chuẩn; dải màu mỏng ở mép trên (`h 0,08`, tô `#F59E0B`) |
| 10b | Thẻ phải | 6,833 | 1,6 | 5,9 | 4,1 | Thẻ chuẩn; dải màu mỏng ở mép trên (`h 0,08`, tô `green`) |
| 10c | Banner chuyển giao | 0,6 | 6,0 | 12,133 | 0,8 | Nền `blue`, chữ trắng 24 pt đậm, canh giữa cả hai chiều |

Trong mỗi thẻ: tiêu đề `+0,25; +0,25` (20 pt đậm `ink`), gạch đầu dòng ở `+0,25; +0,9`, `w 5,4`, 18 pt `ink`, cách dòng 0,12 inch.

**Thẻ trái:** tiêu đề `Hạn chế`
- `Mới có một data mart (chủ đề bán hàng)`
- `ETL tạo lại toàn bộ kho mỗi lần chạy, chưa nạp gia tăng`
- `Mỗi đơn chỉ giữ một hình thức thanh toán chính`
- `Dữ liệu 2016 thưa và 2018 dừng ở tháng 8`

**Thẻ phải:** tiêu đề `Hướng phát triển`
- `Thêm fact thanh toán và fact đánh giá (fact constellation)`
- `Nạp gia tăng, ghi lại lịch sử nạp`
- `Dùng hệ quản trị có phân vùng hoặc khối MOLAP khi dữ liệu lớn`
- `Thêm tọa độ theo mã bưu chính để vẽ bản đồ`

**Banner 10c:** `Tiếp theo: Vỹ trình bày Dashboard và các mô hình DSS`

**Ghi chú diễn giả:** Phần kho dữ liệu còn một số hạn chế: mới có một data mart, mỗi lần chạy ETL tạo lại toàn bộ kho, và mỗi đơn chỉ giữ một hình thức thanh toán chính. Hướng phát triển là mở rộng thành nhiều bảng fact dùng chung chiều, nạp gia tăng và dùng hệ quản trị phù hợp hơn khi dữ liệu lớn. Em xin chuyển sang bạn Vỹ để trình bày dashboard và các mô hình hỗ trợ ra quyết định.

---

## 5. Phụ lục (ẩn khi trình bày, đặt sau slide 10)

Đánh dấu cả hai slide là **ẩn** (hidden) nếu công cụ hỗ trợ; nếu không thì đặt ở cuối bộ và ghi tiêu đề có tiền tố `Phụ lục`. Dùng khung chung (T, TA, F1, F2).

### Slide A1 – Phụ lục A1: Từ điển bảng fact
**Tiêu đề (T):** `Phụ lục A1: Từ điển bảng fact`

**Bảng** (`x 0,6; y 1,6; w 12,133`; cột: `x 0,6 w 4,6` (phông đơn cách 14 pt), `x 5,2 w 2,6`, `x 7,8 w 4,933`; chữ 14 pt; hàng tiêu đề cao 0,45; 8 hàng mỗi hàng cao 0,5):

| Cột | Loại | Ý nghĩa |
|---|---|---|
| `order_id, order_item_id` | `Chiều suy biến` | `Định danh đơn và dòng hàng` |
| `purchase_date_key, delivered_date_key` | `Khóa ngoại` | `Ngày mua; ngày giao (NULL nếu chưa giao)` |
| `customer_key, product_key, seller_key` | `Khóa ngoại` | `Khách hàng, sản phẩm, người bán` |
| `payment_type_key, status_key` | `Khóa ngoại` | `Hình thức thanh toán chính; trạng thái đơn` |
| `price, freight_value, item_total` | `Số đo cộng được` | `Giá bán, phí vận chuyển, tổng hai khoản` |
| `payment_installments` | `Số đo không cộng` | `Số kỳ trả góp của hình thức chính` |
| `review_score` | `Số đo bán cộng` | `Điểm đánh giá trung bình của đơn (1 đến 5)` |
| `delivery_days, delay_days` | `Số đo bán cộng` | `Số ngày giao; số ngày trễ (lớn hơn 0 là trễ)` |

### Slide A2 – Phụ lục A2: Ví dụ truy vấn roll-up
**Tiêu đề (T):** `Phụ lục A2: Ví dụ truy vấn roll-up`

- **Khối code A2a:** `x 0,6; y 1,6; w 7,6; h 3,9`, nền `ink`, chữ `#E5E7EB`, phông đơn cách **14 pt**, đệm 0,25, không tự ngắt dòng, giữ nguyên thụt lề:

```
SELECT d.year, ROUND(SUM(f.price), 2) AS revenue,
       COUNT(DISTINCT f.order_id) AS orders
FROM fact_sales f
JOIN dim_date d         ON f.purchase_date_key = d.date_key
JOIN dim_order_status s ON f.status_key = s.status_key
WHERE s.order_status NOT IN ('canceled', 'unavailable')
GROUP BY d.year ORDER BY d.year;
```

- **Tiêu đề kết quả A2b:** `x 8,5; y 1,6; w 4,233; h 0,4`, `Kết quả`, 18 pt đậm `ink`.
- **Bảng kết quả A2c:** `x 8,5; y 2,05; w 4,233`; cột `w 1,2` (`Năm`), `w 1,9` (`Doanh thu`, canh phải), `w 1,133` (`Số đơn`, canh phải); chữ 16 pt; hàng tiêu đề cao 0,5; 3 hàng cao 0,5:

| Năm | Doanh thu | Số đơn |
|---|---|---|
| `2016` | `44.726` | `293` |
| `2017` | `6.108.492` | `44.375` |
| `2018` | `7.341.182` | `53.531` |

- **Chú thích A2d:** `x 0,6; y 5,7; w 12,133; h 0,4`, 16 pt `muted`: `Roll-up: GROUP BY d.year gộp doanh thu từ mức ngày lên mức năm. Đã loại đơn canceled và unavailable.`

---

## 6. Danh sách kiểm tra trước khi xuất (công cụ AI và người dùng cùng kiểm)

1. Đủ **10 slide chính + 2 phụ lục**, đúng thứ tự trong Mục 3.
2. Không có chữ tràn khung, không có hai khối chồng lấn, mọi khối nằm trong vùng an toàn.
3. Không có chữ nào nhỏ hơn mức tối thiểu: nội dung 16 pt, chú thích 14 pt, footer 12 pt. Nếu thiếu chỗ thì rút câu, không giảm cỡ chữ.
4. Tiêu đề mọi slide đứng **cùng vị trí**, một dòng.
5. Tiếng Việt hiển thị đúng dấu (không có ô vuông thay chữ).
6. Chỉ dùng màu trong Mục 2.1; **cam chỉ dùng cho fact và điểm nhấn số liệu, xanh dương cho chiều**.
7. Mọi số liệu khớp **Mục 7**. Đặc biệt không làm tròn lại các số: `112.650`, `96.096`, `2,55`, `4,21`, `7,91`.
8. Chữ, bảng, biểu đồ đều là đối tượng chỉnh sửa được (không dán thành ảnh).
9. Không có animation, chuyển cảnh, ảnh stock hay emoji.
10. Tổng thời lượng theo ghi chú diễn giả khoảng 430 giây.

---

## 7. Bảng số liệu gốc (nguồn: `data/processed/olist_dw.db`, đã chạy lại ngày 13/11/2026)

| Số liệu | Giá trị | Dùng ở slide |
|---|---|---|
| Đơn hàng trong dữ liệu nguồn | 99.441 | 2 |
| Dòng fact (dòng hàng bán ra) | 112.650 | 2, 4, 7 |
| Số bảng CSV nguồn | 8 | 2 |
| Khách hàng (người thật) / mã khách theo đơn | 96.096 / 99.441 | 5, 6, 7 |
| Số dòng `dim_product` / `dim_seller` / `dim_date` / `dim_order_status` / `dim_payment_type` | 32.951 / 3.095 / 774 / 8 / 5 | 4, 7 |
| Đơn không có sản phẩm bị loại | 775 | 6 |
| Đơn thanh toán nhiều cách | 2.246 | 5, 6 |
| Đơn có nhiều đánh giá | 547 | 6 |
| Sản phẩm không có danh mục | 610 | 6 |
| Dòng fact chưa có điểm đánh giá / chưa có thanh toán | 942 / 3 | 7 |
| Doanh thu 2017 (loại đơn hủy) | 6.108.492 | 8, A2 |
| Doanh thu 2018 đến tháng 8 (loại đơn hủy) | 7.341.182 | 8, A2 |
| Doanh thu 2016 / số đơn 2016 | 44.726 / 293 | A2 |
| Số đơn 2017 / 2018 | 44.375 / 53.531 | A2 |
| Tổng doanh thu (loại đơn hủy) | 13.494.401 | 9 |
| Doanh thu bang SP / điểm đánh giá TB SP | 5,17 triệu / 4,14 | 9 |
| Điểm đánh giá TB RJ (doanh thu 1,81 triệu) | 3,82 | 9 |
| Cơ cấu thanh toán: thẻ tín dụng / boleto / voucher / thẻ ghi nợ | 78,9% / 17,6% / 2,1% / 1,4% | 9 |
| Giao trễ: số dòng, ngày giao TB, điểm TB | 8.714; 31,3; 2,55 | 9 |
| Đúng hạn hoặc sớm: số dòng, ngày giao TB, điểm TB | 101.475; 10,9; 4,21 | 9 |
| Tỷ lệ giao trễ | 7,91% | (phần B) |
| Top danh mục 2017 (nghìn) | bed_bath_table 498; watches_gifts 487; health_beauty 481; sports_leisure 448; computers_accessories 400 | 8 |
| Dice 2018, SP (đồng) | health_beauty 302.498; bed_bath_table 270.372; computers_accessories 210.550 | 8 |
| Dice 2018, RJ (đồng) | health_beauty 79.176; bed_bath_table 67.562; computers_accessories 59.659 | 8 |
| Pivot health_beauty (nghìn): 2017 / 2018 / tổng | 481 / 770 / 1.256 | 8 |

**Chuỗi doanh thu theo tháng (nghìn), dùng cho biểu đồ slide 9:**

| Tháng | 2017-01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | 09 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2017 | 120 | 245 | 368 | 354 | 503 | 430 | 492 | 568 | 621 | 660 | 1004 | 742 |

| Tháng | 2018-01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 |
|---|---|---|---|---|---|---|---|---|
| 2018 | 945 | 838 | 981 | 994 | 993 | 863 | 878 | 849 |

---

## 8. Việc người dùng cần tự làm sau khi sinh slide

1. Điền `[Họ tên – MSSV]` ở slide 1.
2. Đọc từng ghi chú diễn giả và nói thử có bấm giờ (mục tiêu 7 phút 10 giây, tối đa 8 phút).
3. Ghép với bộ slide của Vỹ: bỏ hoặc giữ slide 1 làm trang chia phần, kiểm tra số slide tự cập nhật.
4. Xuất **PDF** (đề bài yêu cầu slide dạng PDF) và đặt vào thư mục `slides/`.
