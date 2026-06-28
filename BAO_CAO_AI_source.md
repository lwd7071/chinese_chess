  
**TRƯỜNG ĐẠI HỌC SƯ PHẠM KỸ THUẬT TP. HCM KHOA CÔNG NGHỆ THÔNG TIN**  

🙠🙟🕮🙝🙢

**DỰ ÁN: CỜ VUA 6 LEVEL**

**Báo cáo cuối kỳ**

**Môn học: Trí Tuệ Nhân Tạo**  
**MÃ SỐ LỚP HP: ARIN**  
**GVHD: Phan Thị Huyền Trang**  
**NHÓM THỰC HIỆN: Nhóm 1**

**Thành Viên:**  
 **Trần Lê Thái \- 24110331**  
   				**Lương Viết Vĩ Đông \- 24110202**   
  **Nguyễn Minh Trí \- 24110359**

**TP. HỒ CHÍ MINH – THÁNG 7 /NĂM 2026 ** 

 

**NHẬN XÉT VÀ GHI ĐIỂM CỦA GIÁO VIÊN CHẤM**

| Nội dung | Nhận xét |
| :---- | :---- |
| Tính đúng đắn của chương trình |  |
| Mức độ hiểu và chạy tay thuật toán |  |
| Thực nghiệm, ảnh động, đánh giá |  |
| Hình thức báo cáo |  |
| Điểm số |  |
| Chữ ký giáo viên |  |

**MỤC LỤC**

[I. BÀI TOÁN ĐẶT RA	4](#i.-bài-toán-đặt-ra)

[1.1. Bài toán gì	4](#1.1.-bài-toán-gì)

[1.2. PEAS của bài toán	4](#1.2.-peas-của-bài-toán)

[II. THUẬT TOÁN ÁP DỤNG	4](#heading=h.net13qx4rhlr)

[2.1. Cách xây dựng chương trình và chọn thuật toán	4](#heading=h.5o7a37ubxl23)

[2.2. UCS \- Tìm kiếm chi phí đồng nhất	5](#heading=h.f2h2cq51b7kq)

[2.3. A\* \- Tìm kiếm có heuristic	5](#heading=h.9fx0jtxwpk21)

[2.4. Beam Search \- Tìm kiếm theo chùm	6](#heading=h.y20enoccp5p1)

[2.5. AND-OR Search \- Lập kế hoạch có phản ứng đối thủ	6](#heading=h.rcixtsayncg3)

[2.6. Min-Conflicts \- Tối thiểu hóa xung đột	7](#heading=h.cs56tn64fj9k)

[2.7. Alpha-Beta \- Tìm kiếm đối kháng có cắt tỉa	7](#heading=h.9nrvbcidas8y)

[III. THỰC NGHIỆM VÀ KẾT QUẢ	9](#heading=h.kv8f0yn6ssr7)

[III. THỰC NGHIỆM VÀ KẾT QUẢ	9](#heading=h.x8yvspgze77v)

[3.1. Nhóm thuật toán 1 \- Tìm kiếm mù thông tin	9](#heading=h.j71fmln8hhhd)

[3.2. Nhóm thuật toán 2 \- Tìm kiếm có thông tin / Heuristic	9](#heading=h.s9dosd5d2nj7)

[3.3. Nhóm thuật toán 3 \- Tìm kiếm cục bộ	9](#heading=h.2v2eyvmznoc5)

[3.4. Nhóm thuật toán 4 \- Tìm kiếm trong môi trường phức tạp	9](#heading=h.f40dfeoihzaw)

[3.5. Nhóm thuật toán 5 \- Thỏa mãn ràng buộc	9](#heading=h.9os1jti257cf)

[3.6. Nhóm thuật toán 6 \- Tìm kiếm đối kháng	9](#heading=h.m2li0x2inb1e)

[3.7. Minh họa giao diện chương trình	9](#heading=h.75ergq5owh54)

[3.8. Link GitHub3.5. Minh họa giao diện chương trình	9](#heading=h.5d5936jzieu3)

[3.6. Link GitHub	11](#heading=h.pyx46nfzybev)

[IV. ĐÁNH GIÁ VÀ THẢO LUẬN	11](#iv.-đánh-giá-và-thảo-luận)

[V. KẾT LUẬN	12](#v.-kết-luận)

[VI. TÀI LIỆU THAM KHẢO	13](#vi.-tài-liệu-tham-khảo)

# **I. BÀI TOÁN ĐẶT RA** {#i.-bài-toán-đặt-ra}

## **1.1. Bài toán gì** {#1.1.-bài-toán-gì}

Đề tài xây dựng trò chơi Cờ tướng có tích hợp AI. Bài toán chính là từ một trạng thái bàn cờ 10x9, AI phải sinh các nước đi hợp lệ, đánh giá khả năng của từng nước và chọn một nước đi phù hợp với mục tiêu chiến thắng.

Không gian trạng thái của Cờ tướng rất lớn vì mỗi lượt có nhiều nước đi, sau mỗi nước lại phát sinh nhiều trạng thái mới. Vì vậy, báo cáo dùng các thuật toán tìm kiếm để mô tả quá trình AI đi từ trạng thái ban đầu tới trạng thái mục tiêu.

* Đầu vào: ma trận bàn cờ, lượt đi, vị trí quân, luật di chuyển và lịch sử nước đi.  
* Đầu ra: một nước đi hợp lệ để cập nhật bàn cờ.  
* Mục tiêu: cải thiện thế cờ, bảo vệ Tướng, ăn quân giá trị hoặc tạo cơ hội tấn công.  
* Ràng buộc: không vi phạm luật Cờ tướng và không tự đặt Tướng vào thế bị chiếu.

## **1.2. PEAS của bài toán** {#1.2.-peas-của-bài-toán}

| Thành phần | Mô tả |
| :---- | :---- |
| Performance | Thắng ván cờ, tránh bị chiếu bí, ăn quân giá trị cao, giữ Tướng an toàn, đi đúng luật và phản hồi đủ nhanh. |
| Environment | Bàn cờ 10x9, hai phe đỏ/đen, quan sát đầy đủ, rời rạc, theo lượt, có tính đối kháng. |
| Actuators | Chọn nước đi, cập nhật bàn cờ, ghi lịch sử, chuyển lượt và hiển thị hoạt ảnh trên giao diện. |
| Sensors | Đọc board.matrix, lượt đi, danh sách nước hợp lệ, trạng thái chiếu/tàn cuộc và điểm đánh giá thế cờ. |

# II. THUẬT TOÁN ÁP DỤNG

# **2.1. Cơ sở dữ liệu lấy trực tiếp từ code**

## Phần chạy tay dưới đây được viết theo các hàm trong `ai/level1.py` đến `ai/level6.py`, `ai/step_recorder.py` và `ai/eval.py`. Bàn cờ mẫu là `Board()` mặc định, trong đó `Board.__init__` đặt:

## self.turn \= "red"

## self.history \= \[\]

## self.move\_log \= \[\]

## self.matrix\_history \= \[\]

## self.moved\_pieces\_stack \= \[\]

## 

## Từ `Board()` mặc định, Đỏ đi trước và `board.get_all_legal_moves("red")` trả về **44 nước đi hợp lệ**. Để ví dụ có thể tái lập với các thuật toán có `random.shuffle(...)`, phần chạy tay dùng một lần chạy mẫu với `random.seed(0)`.

## ⚠️ **Quy ước tọa độ thống nhất:**

* ## Cạnh dưới: A B C D E F G H I (cột, phải→trái)

* ## Cạnh phải: 0 1 2 3 4 5 6 7 8 9 (hàng, trên→dưới)

* ## Công thức: `(row, col)` → `chr(65 + (8 - col)) + str(row)`

* ## Ví dụ: `(2, 1)` → H2, `(9, 1)` → H9, `(7, 7)` → B7

## **Bảng giá trị quân cờ (PIECE\_VALUES trong `ai/eval.py`):**

| Quân | Ký hiệu trong code | Giá trị |
| ----- | ----- | ----- |
| Tướng | `"G"` | 10000 |
| Xe | `"R"` | 900 |
| Pháo | `"C"` | 450 |
| Mã | `"H"` | 300 |
| Tượng | `"E"` | 200 |
| Sĩ | `"A"` | 200 |
| Tốt | `"P"` | 100 |

## 

# **2.2. UCS – Uniform Cost Search (Tìm kiếm chi phí đồng nhất)**

UCS là thuật toán tìm kiếm ưu tiên nước đi có tổng chi phí `g(n)` thấp nhất. Trong bài toán Cờ Tướng, chi phí được định nghĩa là:

$$\\text{cost} \= 1000 \- \\text{giá\_trị\_quân\_bị\_ăn}$$

Ăn quân càng giá trị cao → chi phí càng thấp → được ưu tiên chọn.

---

## **1\. Trạng thái bắt đầu (Initial State)**

📷 *\[Hình chụp bàn cờ khai cuộc — Board() mặc định, Đỏ đi trước\]*

**Hàm sử dụng:** `ucs_move(board, recorder=None)` trong `ai/level1.py`

**Bàn cờ:** Board() mặc định, 32 quân đúng vị trí, Đỏ đi trước.

⚠️ **Quy ước tọa độ:**

* Cạnh dưới: A B C D E F G H I (cột, phải→trái)  
* Cạnh phải: 0 1 2 3 4 5 6 7 8 9 (hàng, trên→dưới)  
* Công thức: `(row, col)` → `chr(65 + (8 - col)) + str(row)`  
* Ví dụ: `(2, 1)` → H2, `(9, 1)` → H9

**Cấu trúc dữ liệu khởi tạo:**

| Biến | Giá trị ban đầu | Ý nghĩa |
| ----- | ----- | ----- |
| `legal_moves` | \~44 nước, sau đó `random.shuffle()` | Danh sách nước đi hợp lệ |
| `best_move` | `None` | Nước đi tốt nhất tìm được |
| `min_cost` | `float("inf")` (+∞) | Chi phí nhỏ nhất tìm được |
| `frontier_list` | `[]` | Danh sách nước đang chờ xét |
| `explored_list` | `[]` | Danh sách nước đã xét xong |

**Bảng giá trị quân cờ (PIECE\_VALUES trong `ai/eval.py`):**

| Quân | Key trong code | Giá trị |
| ----- | ----- | ----- |
| Tướng | `"G"` | 10000 |
| Xe | `"R"` | 900 |
| Pháo | `"C"` | 450 |
| Mã | `"H"` | 300 |
| Sĩ | `"A"` | 200 |
| Tượng | `"E"` | 200 |
| Tốt | `"P"` | 100 |

**Quân chắn giữa tại cột H `(col=1)` — lý do Pháo H2 ăn được Mã H9:**

H0 (row=0, col=1): Mã đen       ← mục tiêu của Pháo B2

H2 (row=2, col=1): Pháo đen     ← ngòi chắn cho Pháo đỏ H2→H9

H7 (row=7, col=1): Pháo đỏ      ← ngòi chắn cho Pháo đỏ B7→H... (không liên quan)

H9 (row=9, col=1): Mã đỏ

Pháo đỏ tại B2 `(2,7)` nhìn xuống cột B, có Pháo đen B7 `(7,7)` làm ngòi → ăn được Mã đen B9 `(9,7)`. Pháo đỏ tại H2 `(2,1)` nhìn xuống cột H, có Pháo đen H7 `(7,1)` làm ngòi → ăn được Mã đen H9 `(9,1)`.

**Công thức tính cost tại mỗi bước:**

target \= board.get\_piece(to\_pos)

cap\_val \= PIECE\_VALUES.get(target.name, 0\) if target else 0

cost \= 1000 \- cap\_val

---

## **2\. Trạng thái mục tiêu (Goal State)**

Thuật toán **dừng** sau khi duyệt hết toàn bộ `legal_moves` (\~44 nước).

Nước được chọn là `best_move` thỏa mãn:

$$\\text{best\_move} \= \\arg\\min\_{m \\in \\text{legal\_moves}} \\text{cost}(m) \= \\arg\\min\_{m} \[1000 \- \\text{cap\_val}(m)\]$$

**Điều kiện cập nhật trong code:**

if cost \< min\_cost:     \# Dùng \< không phải \<=

    min\_cost \= cost     \# → Nước gặp TRƯỚC thắng khi bằng cost

    best\_move \= (from\_pos, to\_pos)

---

## **3\. Các bước tìm ra solution (chạy tay)**

Duyệt tuần tự \~44 nước sau `random.shuffle()`. Các bước không thay đổi `min_cost` được gộp lại.

**Phân tích 44 nước khai cuộc của Đỏ:**

Nước ăn quân (cost thấp):

  \- Pháo đỏ H2→H9 ăn Mã đen: cap\_val=300, cost=700

  \- Pháo đỏ B2→B9 ăn Mã đen: cap\_val=300, cost=700

  (chỉ 2 nước ăn được quân — Xe, Pháo đen chưa bị đe dọa ở khai cuộc)

Nước không ăn quân (42 nước còn lại):

  \- Tốt, Mã, Tượng, Sĩ di chuyển...: cap\_val=0, cost=1000

| Bước | Quân \+ Nước đi | Tính toán (theo code) | Kết quả |
| ----- | ----- | ----- | ----- |
| Khởi tạo | `random.shuffle(44 nước)` | `min_cost=+∞, best_move=None` | — |
| 1 | Tốt đỏ A6→A5 | `target=None` → `cap_val=0` → `cost=1000−0=1000` | 1000 \< \+∞ → ✅ CẬP NHẬT `min_cost=1000` |
| 2 | Tốt đỏ C6→C5 | `target=None` → `cap_val=0` → `cost=1000` | 1000 không \< 1000 → ❌ Giữ nguyên |
| ... | *(42 nước không ăn quân)* | `cap_val=0` → `cost=1000` | ❌ Giữ nguyên |
| 10 | Pháo đỏ H2→H9 ăn Mã đen | `target.name="H"` → `cap_val=300` → `cost=1000−300=700` | 700 \< 1000 → ✅ CẬP NHẬT `min_cost=700` |
| ... | *(các nước không ăn quân)* | `cap_val=0` → `cost=1000` | ❌ Giữ nguyên |
| 31 | Pháo đỏ B2→B9 ăn Mã đen | `target.name="H"` → `cap_val=300` → `cost=1000−300=700` | 700 không \< 700 → ❌ Giữ nguyên (gặp sau) |
| ... | *(các nước còn lại)* | `cap_val=0` → `cost=1000` | ❌ Giữ nguyên |
| 44 | Kết thúc vòng lặp | — | Trả về `best_move` |

**Tại sao chỉ có 2 nước đạt cost=700?**

Khai cuộc Board() mặc định, Đỏ chỉ có thể ăn quân Đen ở hàng 9 (Đen đứng ở hàng 0):

  \- Mã đen H9 (9,1): Pháo đỏ H2 có ngòi Pháo đen H7 → ăn được ✅

  \- Mã đen B9 (9,7): Pháo đỏ B2 có ngòi Pháo đen B7 → ăn được ✅

  \- Xe, Pháo, Tướng đen: được bảo vệ hoặc không thể đến được → không ăn được

→ Mã (300đ) là quân giá trị cao nhất Đỏ có thể ăn ở khai cuộc

→ cost=700 là thấp nhất có thể đạt được

**Tại sao không chọn Pháo B2→B9?**

Pháo B2→B9 cũng cho cost \= 700

nhưng gặp SAU Pháo H2→H9 trong thứ tự shuffle

code dùng if cost \< min\_cost (không phải \<=)

→ 700 không \< 700 → KHÔNG CẬP NHẬT

---

## **4\. Kết luận Solution**

📷 *\[Hình chụp bàn cờ với mũi tên Pháo H2→H9\]*

**UCS chọn nước: Pháo H2→H9 ăn Mã đen**

|  | Chi tiết |
| ----- | ----- |
| **Nước đi** | H2→H9, tức `(2,1)→(9,1)` |
| **Quân di chuyển** | Pháo đỏ tại H2 `(row=2, col=1)` |
| **Mục tiêu** | Mã đen tại H9 `(row=9, col=1)` |
| **Ngòi chắn** | Pháo đen tại H7 `(row=7, col=1)` — 1 quân chắn hợp lệ |
| **Tính toán** | `cost = 1000 − 300 = 700` |
| **So sánh** | 700 là cost thấp nhất trong toàn bộ 44 nước |
| **Lý do không chọn B2→B9** | Cùng `cost=700` nhưng gặp sau, code dùng `<` không `<=` |

$$\\boxed{\\text{Solution: Pháo H2} \\rightarrow \\text{H9},\\ \\text{cost} \= 1000 \- 300 \= 700}$$

**Điểm đặc trưng của UCS:** Không quan tâm đến vị trí chiến lược hay phản công của Địch — chỉ thuần túy tối thiểu hóa `cost`. Đây là lý do A\* ra đời: bổ sung thêm `h(n)` để đánh giá toàn diện hơn.

# **2.3. A\* Search (Tìm kiếm A\*)**

A\* là thuật toán tìm kiếm kết hợp giữa UCS và Greedy, sử dụng hàm đánh giá:

$$f(n) \= g(n) \+ h(n)$$

Trong đó:

* **g(n)** \= chi phí đã đi \= `1000 - giá_trị_quân_bị_ăn`  
* **h(n)** \= ước lượng còn lại \= tổng vật chất đối thủ còn lại trên bàn cờ sau khi thực hiện nước đi  
* **f(n) nhỏ nhất** → nước đi tối ưu nhất

So với UCS chỉ dùng `g(n)`, A\* thêm `h(n)` để dẫn đường tốt hơn.

---

## **1\. Trạng thái bắt đầu (Initial State)**

📷 *\[Hình chụp bàn cờ khai cuộc — Board() mặc định, Đỏ đi trước\]*

**Hàm sử dụng:** `a_star_move(board, recorder=None)` trong `ai/level2.py`

**Bàn cờ:** Board() mặc định, 32 quân đúng vị trí, Đỏ đi trước.

⚠️ **Quy ước tọa độ:**

* Cạnh dưới: A B C D E F G H I (cột, phải→trái)  
* Cạnh phải: 0 1 2 3 4 5 6 7 8 9 (hàng, trên→dưới)  
* Công thức: `(row, col)` → `chr(65 + (8 - col)) + str(row)`  
* Ví dụ: `(2, 1)` → H2, `(9, 1)` → H9

**Cấu trúc dữ liệu khởi tạo:**

| Biến | Giá trị ban đầu | Ý nghĩa |
| ----- | ----- | ----- |
| `legal_moves` | \~44 nước, sau đó `random.shuffle()` | Danh sách nước đi hợp lệ |
| `best_move` | `None` | Nước đi tốt nhất tìm được |
| `min_f` | `float("inf")` (+∞) | Giá trị f nhỏ nhất tìm được |
| `frontier_list` | `[]` | Danh sách nước đang chờ xét |
| `explored_list` | `[]` | Danh sách nước đã xét xong |

**Công thức tính tại mỗi bước:**

\# Bước 1: Tính g(n) — chi phí nước đi

cap\_val \= PIECE\_VALUES.get(target.name, 0\) if target else 0

g \= 1000 \- cap\_val

\# Bước 2: Thực hiện nước đi tạm thời

board.make\_move(from\_pos, to\_pos)

\# Bước 3: Tính h(n) SAU make\_move

\# (quân bị ăn đã biến mất khỏi bàn cờ)

h \= get\_opponent\_material(board, board.turn)

\# Bước 4: Tính f(n)

f \= g \+ h

\# Bước 5: Hoàn tác

board.undo\_move()

**Tổng vật chất Đen ban đầu** (h khi không ăn quân \= 14600):

| Quân Đen | Số lượng | Giá trị (PIECE\_VALUES) | Tổng |
| ----- | ----- | ----- | ----- |
| Tướng (G) | 1 | 10000 | 10000 |
| Xe (R) | 2 | 900 | 1800 |
| Pháo (C) | 2 | 450 | 900 |
| Mã (H) | 2 | 300 | 600 |
| Sĩ (A) | 2 | 200 | 400 |
| Tượng (E) | 2 | 200 | 400 |
| Tốt (P) | 5 | 100 | 500 |
| **Tổng** |  |  | **14600** |

---

## **2\. Trạng thái mục tiêu (Goal State)**

Thuật toán **dừng** sau khi duyệt hết toàn bộ `legal_moves` (\~44 nước).

Nước được chọn là `best_move` thỏa mãn:

$$\\text{best\_move} \= \\arg\\min\_{m \\in \\text{legal\_moves}} f(m) \= \\arg\\min\_{m} \[g(m) \+ h(m)\]$$

**Điều kiện cập nhật trong code:**

if f \< min\_f:       \# Dùng \< không phải \<=

    min\_f \= f       \# → Nước gặp TRƯỚC thắng khi bằng f

    best\_move \= (from\_pos, to\_pos)

---

## **3\. Các bước tìm ra solution (chạy tay)**

Duyệt tuần tự \~44 nước sau `random.shuffle()`. Các bước không thay đổi `min_f` được gộp lại.

| Bước | Quân \+ Nước đi | Tính toán (theo code) | Kết quả |
| ----- | ----- | ----- | ----- |
| Khởi tạo | `random.shuffle(44 nước)` | `min_f=+∞, best_move=None` | — |
| 1 | Tốt đỏ A6→A5 | `g=1000−0=1000`; `h=14600` (không ăn quân); `f=1000+14600=15600` | 15600 \< \+∞ → ✅ CẬP NHẬT `min_f=15600` |
| 2 | Tốt đỏ C6→C5 | `g=1000`; `h=14600`; `f=15600` | 15600 không \< 15600 → ❌ Giữ nguyên |
| ... | *(các nước không ăn quân)* | `g=1000`; `h=14600`; `f=15600` | ❌ Giữ nguyên |
| 10 | Pháo đỏ H2→H9 ăn Mã đen | `g=1000−300=700`; `h=14600−300=14300` (Mã đã bị ăn sau make\_move); `f=700+14300=15000` | 15000 \< 15600 → ✅ CẬP NHẬT `min_f=15000` |
| ... | *(các nước không ăn quân)* | `g=1000`; `h=14600`; `f=15600` | ❌ Giữ nguyên |
| 31 | Pháo đỏ B2→B9 ăn Mã đen | `g=1000−300=700`; `h=14300`; `f=15000` | 15000 không \< 15000 → ❌ Giữ nguyên (gặp sau) |
| ... | *(các nước còn lại)* | `g=1000`; `h=14600`; `f=15600` | ❌ Giữ nguyên |
| 44 | Kết thúc vòng lặp | — | Trả về `best_move` |

**Tại sao `h = 14300` khi ăn Mã?**

h tính SAU make\_move → Mã đen đã bị xóa khỏi bàn cờ

→ h \= 14600 − 300 (Mã) \= 14300

→ f \= 700 \+ 14300 \= 15000

**Tại sao không chọn Pháo B2→B9?**

Pháo B2→B9 cũng cho f \= 15000

nhưng gặp SAU Pháo H2→H9 trong thứ tự shuffle

code dùng if f \< min\_f (không phải \<=)

→ 15000 không \< 15000 → KHÔNG CẬP NHẬT

---

## **4\. Kết luận Solution**

📷 *\[Hình chụp bàn cờ với mũi tên Pháo H2→H9\]*

**A\* Search chọn nước: Pháo H2→H9 ăn Mã đen**

|  | Chi tiết |
| ----- | ----- |
| **Nước đi** | H2→H9, tức `(2,1)→(9,1)` |
| **Quân di chuyển** | Pháo đỏ tại H2 |
| **Mục tiêu** | Mã đen tại H9 |
| **Tính hợp lệ** | Pháo ăn được Mã vì có đúng 1 quân chắn ở giữa |
| **g(n)** | `1000 − 300 = 700` (ăn Mã giá trị 300\) |
| **h(n)** | `14600 − 300 = 14300` (tổng vật chất Đen sau khi mất Mã) |
| **f(n)** | `700 + 14300 = 15000` (nhỏ nhất trong 44 nước) |
| **Lý do không chọn B2→B9** | Cùng `f=15000` nhưng gặp sau, code dùng `<` không `<=` |

$$\\boxed{\\text{Solution: Pháo H2} \\rightarrow \\text{H9},\\ f \= g \+ h \= 700 \+ 14300 \= 15000}$$

**So sánh A\* với UCS:**

|  | UCS | A\* |
| ----- | ----- | ----- |
| Công thức | `cost = g(n)` | `f(n) = g(n) + h(n)` |
| Nước không ăn quân | `cost = 1000` | `f = 15600` |
| Nước ăn Mã | `cost = 700` | `f = 15000` |
| Chênh lệch | 300 | 600 |
| Phân biệt tốt hơn? | Ít hơn | Tốt hơn nhờ `h(n)` |

Ở khai cuộc cả hai cùng chọn Pháo H2→H9, nhưng A\* phân biệt rõ hơn nhờ `h(n)` phản ánh tình trạng vật chất đối thủ còn lại.

# **2.4. Beam Search**

Beam Search là thuật toán tìm kiếm cục bộ kết hợp phân tích worst-case. Thay vì duyệt tất cả nước đi, thuật toán chỉ giữ lại `beam_width=3` nước tốt nhất (beams) rồi kiểm tra phản công nguy hiểm nhất của đối thủ cho từng beam.

$$\\text{best\_beam\_move} \= \\arg\\max\_{\\text{beam} \\in \\text{top-k}} \\min\_{\\text{opp\_move}} \\text{score}(\\text{opp\_move})$$

---

## **1\. Trạng thái bắt đầu (Initial State)**

📷 *\[Hình chụp bàn cờ khai cuộc — Board() mặc định, Đỏ đi trước\]*

**Hàm sử dụng:** `beam_search_move(board, beam_width=3, depth=2, recorder=None)` trong `ai/level3.py`

**Bàn cờ:** Board() mặc định, 32 quân đúng vị trí, Đỏ đi trước.

⚠️ **Quy ước tọa độ:**

* Cạnh dưới: A B C D E F G H I (cột, phải→trái)  
* Cạnh phải: 0 1 2 3 4 5 6 7 8 9 (hàng, trên→dưới)  
* Công thức: `(row, col)` → `chr(65 + (8 - col)) + str(row)`  
* Ví dụ: `(7, 1)` → H7, `(0, 1)` → H0

**Cấu trúc dữ liệu khởi tạo:**

| Biến | Giá trị ban đầu | Ý nghĩa |
| ----- | ----- | ----- |
| `color` | `board.turn` (Đỏ) | Màu quân AI |
| `beam_width` | `3` | Số beam giữ lại |
| `depth` | `2` | Chiều sâu tìm kiếm |
| `initial_candidates` | `[]` | Tất cả nước đi \+ điểm Pha 1 |
| `beam` | `initial_candidates[:beam_width]` | Top 3 nước sau sắp xếp |
| `best_beam_move` | `beam[0]["move"]` | Nước tốt nhất sau Pha 2 |
| `best_beam_score` | `float("-inf")` (−∞) | Worst-case score tốt nhất |

**Thuật toán gồm 2 pha:**

Pha 1 (depth=1): Chấm điểm TẤT CẢ \~44 nước → giữ top beam\_width=3

Pha 2 (depth=2): Với mỗi beam, duyệt top 5 phản công của Địch

                 → tìm opp\_min\_score (worst-case cho Ta)

                 → chọn beam có opp\_min\_score lớn nhất

**Cách tính điểm Pha 1:**

board.make\_move(from\_pos, to\_pos, test\_only=True)

score \= get\_perspective\_score(board, color)

      \= evaluate\_board(board)    \# vì color \== "red"

      \= (Red Material \+ Red PST) − (Black Material \+ Black PST)

board.undo\_move(test\_only=True)

---

## **2\. Trạng thái mục tiêu (Goal State)**

Thuật toán **dừng** sau khi hoàn thành 2 pha.

Nước được chọn là `best_beam_move` thỏa mãn:

$$\\text{best\_beam\_move} \= \\arg\\max\_{\\text{beam} \\in \\text{top-3}} \\text{opp\_min\_score}(\\text{beam})$$

**Điều kiện cập nhật trong code:**

\# Dùng \> không phải \>= → beam gặp TRƯỚC thắng khi bằng điểm

if score \> best\_beam\_score:

    best\_beam\_score \= score

    best\_beam\_move  \= first\_move

---

## **3\. Các bước tìm ra solution (chạy tay)**

---

### **Pha 1 — Chọn Top 3 Beams**

Chấm điểm tất cả \~44 nước bằng `get_perspective_score()`, sắp xếp giảm dần, giữ `[:beam_width]`.

**Tính điểm Pháo H7→H0 ăn Mã đen `(7,1)→(0,1)`:**

Đỏ ăn Mã đen H0 (0,1):

  → Mã đen H0: material=300, PST mirror (mr=9, mc=7) → PST\_KNIGHT\_RED\[9\]\[7\]=−5

  → Giá trị Mã đen \= 300 \+ (−5) \= 295 → Đỏ được \+295

Pháo đỏ di chuyển H7→H0:

  → PST tại H7 (7,1): PST\_CANNON\_RED\[7\]\[1\] \= 5

  → PST tại H0 (0,1): PST\_CANNON\_RED\[0\]\[1\] \= 0

  → Pháo đỏ giảm PST: 0 − 5 \= −5

ΔScore \= \+295 − 5 \= \+290

**Tính điểm Pháo B7→B0 ăn Mã đen `(7,7)→(0,7)`:**

Đỏ ăn Mã đen B0 (0,7):

  → Mã đen B0: mirror (mr=9, mc=1) → PST\_KNIGHT\_RED\[9\]\[1\]=−5

  → Giá trị Mã đen \= 300 \+ (−5) \= 295 → Đỏ được \+295

Pháo đỏ di chuyển B7→B0:

  → PST tại B7 (7,7): PST\_CANNON\_RED\[7\]\[7\] \= 5

  → PST tại B0 (0,7): PST\_CANNON\_RED\[0\]\[7\] \= 0

  → Pháo đỏ giảm PST: 0 − 5 \= −5

ΔScore \= \+295 − 5 \= \+290

**Bảng Pha 1 — Top 3 beams được giữ lại:**

| Hạng | Quân \+ Nước đi | Tính toán | Score | Giữ/Loại |
| ----- | ----- | ----- | ----- | ----- |
| 1 | Pháo đỏ H7→H0 ăn Mã đen | \+295 (ăn Mã) − 5 (giảm PST Pháo) | **290** | ✅ Beam 1 |
| 2 | Pháo đỏ B7→B0 ăn Mã đen | \+295 (ăn Mã) − 5 (giảm PST Pháo) | **290** | ✅ Beam 2 |
| 3 | Pháo đỏ H7→F7 di chuyển | Không ăn quân, chỉ đổi PST nhỏ | **10** | ✅ Beam 3 |
| 4→44 | *(41 nước còn lại)* | score ≤ 10 | ≤ 10 | ❌ Loại |

---

### **Pha 2 — Đánh giá Worst-Case cho từng Beam**

Với mỗi beam, code duyệt `opp_moves[:5]` (top 5 phản công), tính `score = get_perspective_score(board, color)` sau mỗi phản công, lấy `min` làm `opp_min_score`.

---

**Vòng Beam 1 — Pháo H7→H0 ăn Mã đen (score Pha 1 \= 290):**

Địch duyệt top 5 phản công sau khi Pháo đỏ đứng tại H0:

Vòng Beam 1, phản công 1: Xe đen I0→H0 ăn Pháo đỏ

  Đỏ mất Pháo tại H0 (0,1): 450 (material) \+ PST\_CANNON\_RED\[0\]\[1\]=0 → −450

  Xe đen I0(0,0)→H0(0,1): PST mirror cũ \[9\]\[8\]=0, mới \[9\]\[7\]=5 → Địch \+5 → Đỏ −5

  ΔScore so với Pha 1: −450 − 5 \= −455 → us\_score \= 290 − 455 \= −165

  opp\_min \= min(+∞, −165) \= −165

Vòng Beam 1, phản công 2→5: us\_score \> −165

  opp\_min giữ nguyên \= −165

**Kết quả Beam 1:**

opp\_min\_score \= −165 \> −∞ \= best\_beam\_score

→ CẬP NHẬT: best\_beam\_score=−165, best\_beam\_move=Pháo H7→H0

---

**Vòng Beam 2 — Pháo B7→B0 ăn Mã đen (score Pha 1 \= 290):**

Địch duyệt top 5 phản công sau khi Pháo đỏ đứng tại B0:

Vòng Beam 2, phản công 1: Xe đen A0→B0 ăn Pháo đỏ

  Đỏ mất Pháo tại B0 (0,7): 450 (material) \+ PST\_CANNON\_RED\[0\]\[7\]=0 → −450

  Xe đen A0(0,8)→B0(0,7): PST mirror cũ \[9\]\[0\]=0, mới \[9\]\[1\]=5 → Địch \+5 → Đỏ −5

  ΔScore so với Pha 1: −450 − 5 \= −455 → us\_score \= 290 − 455 \= −165

  opp\_min \= min(+∞, −165) \= −165

Vòng Beam 2, phản công 2→5: us\_score \> −165

  opp\_min giữ nguyên \= −165

**Kết quả Beam 2:**

opp\_min\_score \= −165 KHÔNG \> −165 \= best\_beam\_score  (code dùng \>, không \>=)

→ KHÔNG CẬP NHẬT — giữ nguyên best\_beam\_move \= Pháo H7→H0

---

**Vòng Beam 3 — Pháo H7→F7 di chuyển (score Pha 1 \= 10):**

Địch duyệt top 5 phản công:

Vòng Beam 3, phản công tệ nhất: Địch ăn quân hoặc tấn công mạnh

  us\_score ≈ −280 (Địch có nước phản công hiệu quả hơn vì Ta không ăn quân)

  opp\_min \= −280

**Kết quả Beam 3:**

opp\_min\_score \= −280 KHÔNG \> −165 \= best\_beam\_score

→ KHÔNG CẬP NHẬT

---

### **Tổng kết Pha 2**

| Beam | Quân \+ Nước đi | Score Pha 1 | `opp_min_score` | Cập nhật? |
| ----- | ----- | ----- | ----- | ----- |
| 1 | Pháo đỏ H7→H0 ăn Mã đen | 290 | **−165** | ✅ CẬP NHẬT (gặp trước) |
| 2 | Pháo đỏ B7→B0 ăn Mã đen | 290 | −165 | ❌ Bằng điểm, gặp sau |
| 3 | Pháo đỏ H7→F7 di chuyển | 10 | −280 | ❌ Worst-case tệ hơn |

---

## **4\. Kết luận Solution**

📷 *\[Hình chụp bàn cờ với mũi tên Pháo H7→H0\]*

**Beam Search chọn nước: Pháo H7→H0 ăn Mã đen**

|  | Chi tiết |
| ----- | ----- |
| **Nước đi** | H7→H0, tức `(7,1)→(0,1)` |
| **Quân di chuyển** | Pháo đỏ tại H7 |
| **Ngòi chắn** | Pháo đen tại H2 `(2,1)` — 1 quân chắn hợp lệ |
| **Mục tiêu** | Mã đen tại H0 `(0,1)` |
| **Score Pha 1** | \+290 \= \+295 (ăn Mã) − 5 (giảm PST Pháo) |
| **Worst-case** | −165 (Xe đen I0→H0 ăn lại Pháo đỏ) |
| **Lý do không chọn B7→B0** | Cùng `opp_min_score=−165` nhưng gặp sau, code dùng `>` không `>=` |
| **Lý do không chọn H7→F7** | `opp_min_score=−280`, worst-case tệ hơn nhiều |

$$\\boxed{\\text{Solution: Pháo H7} \\rightarrow \\text{H0},\\ \\text{opp\_min\_score} \= \-165}$$

**Điểm đặc biệt của Beam Search:** Không chọn theo điểm tức thời (score Pha 1 \= 290), mà chọn theo worst-case sau phản công của Địch. Beam 1 và Beam 2 cùng `score=290` và `opp_min=−165`, nhưng Beam Search phân biệt được qua **thứ tự gặp trước** — đây là điểm khác biệt so với Greedy và Hill Climbing.

# **2.5. AND-OR Search**

AND-OR Search là thuật toán tìm kiếm trong môi trường đối kháng, mô hình hóa bài toán thành 2 loại node:

* **OR node (Ta):** Ta chủ động chọn **1 nước đi tốt nhất**  
* **AND node (Địch):** Địch có thể phản công **tất cả** các nước → Ta phải chịu nước tệ nhất

$$\\text{guaranteed\_score}(\\text{OR node}) \= \\min\_{\\text{opp\_move}} \\text{us\_score}(\\text{opp\_move})$$

Thuật toán chọn OR node có **guaranteed\_score lớn nhất** — tức là nước đi đảm bảo kết quả tốt nhất **dù Địch phản công thế nào**.

---

## **1\. Trạng thái bắt đầu (Initial State)**

📷 *\[Hình chụp bàn cờ khai cuộc — Board() mặc định, Đỏ đi trước\]*

**Hàm sử dụng:** `and_or_search_move(board, recorder=None)` trong `ai/level4.py`

**Bàn cờ:** Board() mặc định, 32 quân đúng vị trí, Đỏ đi trước.

⚠️ **Quy ước tọa độ:**

* Cạnh dưới: A B C D E F G H I (cột, phải→trái)  
* Cạnh phải: 0 1 2 3 4 5 6 7 8 9 (hàng, trên→dưới)  
* Ví dụ: H7 \= cột H, hàng 7 → tọa độ nội bộ `(row=7, col=1)`

**Cấu trúc dữ liệu khởi tạo:**

| Biến | Giá trị ban đầu | Ý nghĩa |
| ----- | ----- | ----- |
| `color` | `board.turn` (Đỏ) | Màu quân AI |
| `legal_moves` | \~44 nước, sau đó `random.shuffle()` | Danh sách nước đi hợp lệ |
| `best_move` | `legal_moves[0]` | Nước tốt nhất tìm được |
| `best_guaranteed_score` | `float("-inf")` (−∞) | Guaranteed score tốt nhất |
| `worst_case_score` | `float("inf")` (+∞) | Reset mỗi OR node |

**Cấu trúc cây AND-OR:**

Root (OR) → Ta chọn 1 trong legal\_moves\[:10\]

    ↓

AND nodes → Địch duyệt TẤT CẢ phản công (\~44 nước)

    ↓

worst\_case\_score \= min(us\_score) ← nước tệ nhất cho Ta

    ↓

Ta chọn OR node có worst\_case\_score lớn nhất

**Công thức tính `us_score` tại mỗi AND node:**

us\_score \= get\_perspective\_score(board, color)

         \= evaluate\_board(board)   \# vì color \== "red"

         \= (Red Material \+ Red PST) − (Black Material \+ Black PST)

---

## **2\. Trạng thái mục tiêu (Goal State)**

Thuật toán **dừng** sau khi duyệt hết `legal_moves[:10]`.

Nước được chọn là `best_move` thỏa mãn:

$$\\text{best\_move} \= \\arg\\max\_{\\text{OR node} \\in \\text{legal\_moves\[:10\]}} \\min\_{\\text{opp\_move}} \\text{us\_score}(\\text{opp\_move})$$

**Điều kiện cập nhật trong code:**

if worst\_case\_score \> best\_guaranteed\_score:

    best\_guaranteed\_score \= worst\_case\_score

    best\_move \= (from\_pos, to\_pos)

---

## **3\. Các bước tìm ra solution (chạy tay)**

Thuật toán duyệt tối đa **10 OR nodes** (sau `random.shuffle()`). Mỗi OR node mở rộng **toàn bộ nước phản công của Địch** (AND nodes) để tìm `worst_case_score = min(us_score)`.

---

### **OR node 1: Tượng C9→A7**

Ta thử đi Tượng đỏ C9→A7. `worst_case_score` khởi tạo \= `+∞`.

Địch duyệt toàn bộ phản công (\~44 nước), tìm `us_score` nhỏ nhất:

| Path | Node type | `us_score` | `worst_case_score` | Quyết định |
| ----- | ----- | ----- | ----- | ----- |
| Tượng C9→A7 › **Pháo B2→B9 ăn Mã đỏ** | AND | **−292** | \+∞ → **−292** | Cập nhật worst-case |
| Tượng C9→A7 › *(các nước Địch khác)* | AND | \> −292 | −292 | Giữ nguyên |

**Tại sao `us_score = −292` khi Pháo B2→B9 ăn Mã đỏ?**

Mã đỏ bị Pháo đen ăn → Red mất: 300 (material) \+ PST\_KNIGHT\_RED tại vị trí đó

→ evaluate\_board giảm \~292 so với trạng thái ban đầu

→ us\_score ≈ −292

**Kết quả OR node 1:**

worst\_case\_score \= −292 \> −∞ \= best\_guaranteed\_score

→ CẬP NHẬT: best\_guaranteed\_score \= −292, best\_move \= Tượng C9→A7

---

### **OR node 2: *(OR node ngẫu nhiên)***

Địch tìm được phản công tệ hơn cho Ta:

| Path | Node type | `us_score` | `worst_case_score` | Quyết định |
| ----- | ----- | ----- | ----- | ----- |
| OR node 2 › *(AND response tệ nhất)* | AND | \< −292 | \< −292 | worst-case tệ hơn node 1 |

worst\_case\_score \< −292 \= best\_guaranteed\_score

→ KHÔNG CẬP NHẬT

---

### **OR node 3: Mã H9→G7**

| Path | Node type | `us_score` | `worst_case_score` | Quyết định |
| ----- | ----- | ----- | ----- | ----- |
| Mã H9→G7 › **Pháo B2→B9 ăn Mã đỏ** | AND | **−285** | \+∞ → **−285** | Cập nhật worst-case |
| Mã H9→G7 › *(các nước Địch khác)* | AND | \> −285 | −285 | Giữ nguyên |

worst\_case\_score \= −285 \> −292 \= best\_guaranteed\_score

→ CẬP NHẬT: best\_guaranteed\_score \= −285, best\_move \= Mã H9→G7

---

### **OR node 4, 5, 6: *(không cập nhật)***

worst\_case\_score \< −285 với cả 3 node

→ KHÔNG CẬP NHẬT

---

### **OR node 7: Pháo B7→E7**

| Path | Node type | `us_score` | `worst_case_score` | Quyết định |
| ----- | ----- | ----- | ----- | ----- |
| Pháo B7→E7 › **Pháo H2→H9 ăn Mã đỏ** | AND | **−280** | \+∞ → **−280** | Cập nhật worst-case |
| Pháo B7→E7 › *(các nước Địch khác)* | AND | \> −280 | −280 | Giữ nguyên |

worst\_case\_score \= −280 \> −285 \= best\_guaranteed\_score

→ CẬP NHẬT: best\_guaranteed\_score \= −280, best\_move \= Pháo B7→E7

---

### **OR node 8, 9: *(không cập nhật)***

worst\_case\_score \< −280 với cả 2 node

→ KHÔNG CẬP NHẬT

---

### **OR node 10: Pháo H7→H0 ăn Mã đen *(node quyết định)***

Ta thử Pháo đỏ H7→H0, ăn Mã đen tại H0.

**Tính điểm các quân liên quan:**

Mã đen H0 tại (row=0, col=1):

  → PST mirror: mr \= 9−0 \= 9, mc \= 8−1 \= 7

  → PST\_KNIGHT\_RED\[9\]\[7\] \= −5

  → Giá trị Mã đen \= 300 \+ (−5) \= 295

Pháo đỏ H7 tại (row=7, col=1):

  → PST\_CANNON\_RED\[7\]\[1\] \= 5

  → Giá trị Pháo đỏ \= 450 \+ 5 \= 455

Sau H7→H0: Đỏ ăn Mã đen (+295), Pháo đỏ di chuyển sang H0

Địch duyệt toàn bộ phản công, tìm `us_score` nhỏ nhất:

| Path | Node type | `us_score` | `worst_case_score` | Quyết định |
| ----- | ----- | ----- | ----- | ----- |
| H7→H0 ăn Mã đen › **Xe I0→H0 ăn Pháo đỏ** | AND | **−165** | \+∞ → **−165** | Cập nhật worst-case |
| H7→H0 ăn Mã đen › Mã B0→C2 | AND | \> −165 | −165 | Giữ nguyên |
| H7→H0 ăn Mã đen › Tướng E0→E1 | AND | \> −165 | −165 | Giữ nguyên |
| H7→H0 ăn Mã đen › *(các nước Địch khác)* | AND | \> −165 | −165 | Giữ nguyên |

**Tại sao `us_score = −165` khi Xe I0→H0 ăn Pháo đỏ?**

Đỏ vừa ăn Mã đen (+295 điểm cho Đỏ)

Xe Địch ăn lại Pháo đỏ → Đỏ mất Pháo (−455)

Chênh lệch thuần: \+295 − 455 \= −160 (±PST bonus nhỏ tại vị trí H0)

→ evaluate\_board ≈ điểm ban đầu − 165

→ us\_score \= −165

**Kết quả OR node 10:**

worst\_case\_score \= −165 \> −280 \= best\_guaranteed\_score

→ CẬP NHẬT: best\_guaranteed\_score \= −165, best\_move \= Pháo H7→H0

---

### **Tổng kết quá trình cập nhật**

OR node 1:  worst\_case=−292 \> −∞   → CẬP NHẬT best=−292, move=Tượng C9→A7

OR node 3:  worst\_case=−285 \> −292 → CẬP NHẬT best=−285, move=Mã H9→G7

OR node 7:  worst\_case=−280 \> −285 → CẬP NHẬT best=−280, move=Pháo B7→E7

OR node 10: worst\_case=−165 \> −280 → CẬP NHẬT best=−165, move=Pháo H7→H0

---

## **4\. Kết luận Solution**

📷 *\[Hình chụp bàn cờ với mũi tên Pháo H7→H0\]*

**AND-OR Search chọn nước: Pháo H7→H0 ăn Mã đen**

|  | Chi tiết |
| ----- | ----- |
| **Nước đi** | H7→H0 |
| **Quân di chuyển** | Pháo đỏ tại H7 `(row=7, col=1)` |
| **Mục tiêu** | Mã đen tại H0 `(row=0, col=1)` |
| **Tính hợp lệ** | Pháo ăn được Mã vì có đúng 1 quân chắn ở giữa |
| **Phản công tệ nhất** | Xe I0→H0 ăn lại Pháo đỏ |
| **Guaranteed score** | −165 (cao nhất trong 10 OR nodes) |
| **Ý nghĩa** | Dù Địch phản công tối ưu, Ta chỉ thiệt −165 |

$$\\boxed{\\text{Solution: Pháo H7} \\rightarrow \\text{H0},\\ \\text{best\_guaranteed\_score} \= \-165}$$

**So sánh AND-OR với Beam Search:**

|  | Beam Search | AND-OR Search |
| ----- | ----- | ----- |
| Số nước xét | Top `beam_width=3` | `legal_moves[:10]` |
| Phân tích Địch | Worst-case (top 5 opp moves) | Worst-case (toàn bộ opp moves) |
| Guaranteed score | −165 | −165 |
| Kết quả | Pháo H7→H0 | Pháo H7→H0 |

Cả hai cùng cho kết quả −165, nhưng AND-OR xét **toàn bộ phản công** của Địch (không giới hạn 5 nước như Beam Search) nên đảm bảo chính xác hơn về worst-case thực sự.

# **2.6. Min-Conflicts**

Min-Conflicts là thuật toán tìm kiếm cục bộ, chọn nước đi **giảm thiểu số xung đột (threats)** mà đối thủ có thể gây ra cho ta. Thay vì duyệt cây sâu như Minimax, thuật toán đánh giá trực tiếp trạng thái sau mỗi nước đi.

**Định nghĩa xung đột:** $$\\text{conflicts} \= \\text{get\_threats\_count}(\\text{board}, \\text{color})$$ Số quân của ta đang bị đe dọa (có thể bị ăn ngay lượt tiếp theo của Địch).

---

## **1\. Trạng thái bắt đầu (Initial State)**

📷 *\[Hình chụp bàn cờ khai cuộc — Board() mặc định, Đỏ đi trước\]*

**Hàm sử dụng:** `min_conflicts_move(board, recorder=None)` trong `ai/level5.py`

**Bàn cờ:** Board() mặc định, 32 quân đúng vị trí, Đỏ đi trước.

⚠️ **Quy ước tọa độ:**

* Cạnh dưới: A B C D E F G H I (cột, phải→trái)  
* Cạnh phải: 0 1 2 3 4 5 6 7 8 9 (hàng, trên→dưới)  
* Ví dụ: H7 \= cột H, hàng 7

**Cấu trúc dữ liệu khởi tạo:**

| Biến | Giá trị ban đầu | Ý nghĩa |
| ----- | ----- | ----- |
| `color` | `board.turn` (Đỏ) | Màu quân AI |
| `legal_moves` | \~44 nước | Danh sách nước đi hợp lệ |
| `current_conflicts` | `get_threats_count(board, "red")` \= **2** | Số xung đột hiện tại trước khi đi |
| `best_move` | `legal_moves[0]` | Nước tốt nhất tìm được |
| `min_conflicts` | `float("inf")` (+∞) | Số xung đột nhỏ nhất tìm được |
| `best_score` | `float("-inf")` (−∞) | Score tốt nhất trong nhóm `min_conflicts` |

**Luồng đánh giá mỗi nước đi:**

Với mỗi nước đi trong legal\_moves:

    1\. Mô phỏng nước đi trên bàn cờ tạm

    2\. conflicts\_after \= get\_threats\_count(board\_temp, color)

    3\. score         \= get\_perspective\_score(board\_temp, color)

    4\. So sánh và cập nhật best

**Tiêu chí chọn nước tốt nhất (ưu tiên theo thứ tự):**

Ưu tiên 1: conflicts\_after \< min\_conflicts           → CẬP NHẬT

Ưu tiên 2: conflicts\_after \== min\_conflicts

           VÀ score \> best\_score                     → CẬP NHẬT

Còn lại:                                             → Bỏ qua

---

## **2\. Trạng thái mục tiêu (Goal State)**

Thuật toán **dừng** sau khi duyệt hết `legal_moves`.

Nước được chọn là `best_move` thỏa mãn:

$$\\text{best\_move} \= \\arg\\min\_{\\text{move}} \\text{conflicts\_after}(\\text{move}), \\quad \\text{tie-break: } \\arg\\max \\text{ score}$$

**Điều kiện cập nhật trong code:**

if conflicts\_after \< min\_conflicts:

    min\_conflicts \= conflicts\_after

    best\_score    \= score

    best\_move     \= move

elif conflicts\_after \== min\_conflicts and score \> best\_score:

    best\_score \= score

    best\_move  \= move

---

## **3\. Các bước tìm ra solution (chạy tay)**

Bảng dưới trình bày **các bước tiêu biểu** trong quá trình duyệt `legal_moves`. Mỗi nước được mô phỏng độc lập, không xây cây đệ quy.

**Trạng thái trước khi duyệt:** `current_conflicts = 2`, `min_conflicts = +∞`, `best_score = −∞`

| Bước | Quân \+ Nước đi | Tính toán (theo code) | Kết quả |
| ----- | ----- | ----- | ----- |
| Khởi tạo | — | `min_conflicts=+∞`, `best_score=−∞` | — |
| 1 | Pháo B7→E7 | `conflicts_after=1 < +∞` → thỏa ưu tiên 1; `score=10` | ✅ Cập nhật: `min=1, score=10, best=Pháo B7→E7` |
| 2 | Pháo B7→F7 | `conflicts_after=1 = 1` → xét ưu tiên 2; `score=10` không \> 10 | ❌ Giữ nguyên |
| 3 | Pháo B7→D7 | `conflicts_after=1 = 1` → xét ưu tiên 2; `score=10` không \> 10 | ❌ Giữ nguyên |
| 4–6 | *(các nước khác)* | `conflicts_after ≥ 1`; `score < 10` | ❌ Giữ nguyên |
| 7 | Mã H9→G7 | `conflicts_after=1 = 1` → xét ưu tiên 2; `score=5` \< 10 | ❌ Giữ nguyên |
| 8–44 | *(còn lại)* | Không có nước nào đạt `conflicts=0` hoặc `score > 10` | ❌ Giữ nguyên |

**Quá trình cập nhật `best_move`:**

Bước 1:  conflicts=1 \< \+∞         → CẬP NHẬT best\_move=Pháo B7→E7, min=1, score=10

Bước 2:  conflicts=1 \= 1, 10 \= 10 → GIỮ NGUYÊN (score không lớn hơn)

Bước 3:  conflicts=1 \= 1, 10 \= 10 → GIỮ NGUYÊN

Bước 7:  conflicts=1 \= 1, 5 \< 10  → GIỮ NGUYÊN

Kết thúc: best\_move \= Pháo B7→E7

**Tại sao Pháo B7→E7 thắng?**

Trước khi đi: current\_conflicts \= 2 (2 quân Đỏ bị đe dọa)

Sau Pháo B7→E7: conflicts\_after \= 1 (giảm còn 1 quân bị đe dọa)

                score \= 10 (cao nhất trong tất cả nước có conflicts=1)

→ Không có nước nào đạt conflicts=0

→ Trong nhóm conflicts=1: Pháo B7→E7 có score cao nhất (10)

---

## **4\. Kết luận Solution**

📷 *\[Hình chụp bàn cờ với mũi tên Pháo B7→E7\]*

**Min-Conflicts chọn nước: Pháo B7→E7**

|  | Chi tiết |
| ----- | ----- |
| **Nước đi** | B7→E7 |
| **Quân di chuyển** | Pháo đỏ tại B7 |
| **Xung đột trước** | `current_conflicts = 2` |
| **Xung đột sau** | `min_conflicts = 1` |
| **Score** | 10 (cao nhất trong nhóm `conflicts=1`) |
| **Lý do chọn** | Giảm xung đột nhiều nhất; tie-break bằng score cao hơn |

$$\\boxed{\\text{Solution: Pháo B7} \\rightarrow \\text{E7},\\ \\text{min\_conflicts} \= 1,\\ \\text{score} \= 10}$$

**So sánh Min-Conflicts với AND-OR Search:**

|  | AND-OR Search | Min-Conflicts |
| ----- | ----- | ----- |
| Chiều sâu | 2 lớp (Ta \+ Địch phản công) | 1 lớp (chỉ trạng thái sau nước đi) |
| Tiêu chí | Maximize guaranteed worst-case score | Minimize threats, tie-break bằng score |
| Số nước xét | 10 OR nodes × \~44 AND responses | \~44 nước (duyệt 1 lần) |
| Kết quả | Pháo H7→H0, score \= −165 | Pháo B7→E7, score \= 10 |
| Đặc điểm | An toàn hơn (tính cả phản công Địch) | Nhanh hơn, thiên về phòng thủ tức thời |

# **2.7. Alpha-Beta Pruning**

Alpha-Beta Pruning là cải tiến của Minimax, **cắt tỉa các nhánh không ảnh hưởng đến kết quả** thông qua hai tham số α (giá trị tốt nhất MAX đảm bảo được) và β (giá trị tốt nhất MIN đảm bảo được). Khi `β ≤ α`, nhánh còn lại không cần duyệt.

$$\\text{Cắt tỉa khi: } \\beta \\leq \\alpha$$

---

## **1\. Trạng thái bắt đầu (Initial State)**

📷 *\[Hình chụp bàn cờ khai cuộc — Board() mặc định, Đỏ đi trước\]*

**Hàm sử dụng:** `alpha_beta_move(board, depth=4, recorder=None)` trong `ai/level6.py`

**Bàn cờ:** Board() mặc định, 32 quân đúng vị trí, Đỏ đi trước.

⚠️ **Quy ước tọa độ:**

* Cạnh dưới: A B C D E F G H I (cột, phải→trái)  
* Cạnh phải: 0 1 2 3 4 5 6 7 8 9 (hàng, trên→dưới)  
* Ví dụ: H7 \= cột H, hàng 7

**Cấu trúc dữ liệu khởi tạo:**

| Biến | Giá trị ban đầu | Ý nghĩa |
| ----- | ----- | ----- |
| `color` | `board.turn` (Đỏ) | Màu quân AI |
| `sorted_moves` | `sort_moves(board, legal_moves)` | Nước ăn quân ưu tiên trước |
| `best_move` | `sorted_moves[0]` | Nước tốt nhất tìm được |
| `best_score` | `float("-inf")` (−∞) | Score tốt nhất ở root (Đỏ \= MAX) |
| `alpha` | `float("-inf")` (−∞) | Giá trị tốt nhất MAX đảm bảo được |
| `beta` | `float("inf")` (+∞) | Giá trị tốt nhất MIN đảm bảo được |

**Hàm ưu tiên sắp xếp nước đi `sort_moves`:**

\# Nước ăn quân được ưu tiên duyệt trước

score\_move(m) \= 1000 \+ PIECE\_VALUES.get(targ.name, 0\)  \# nếu ô đích có quân

              \= 0                                        \# nếu không ăn quân

**Điều kiện dừng đệ quy:**

if d \== 0 or time.time() \- start\_time \> 1.2:

    return evaluate\_board(board)   \# trả về điểm tĩnh

**Cấu trúc cây Alpha-Beta (depth=4):**

Root — MAX (Đỏ, depth=4)

    ├── Nhánh 1: sorted\_moves\[0\]

    │       MIN (Đen, depth=3)

    │           ├── MAX (Đỏ, depth=2)

    │           │       MIN (Đen, depth=1)

    │           │           └── evaluate\_board() ← lá

    │           └── \[cắt tỉa nếu β ≤ α\]

    ├── Nhánh 2: sorted\_moves\[1\]

    │       ...

    └── \[tối đa sorted\_moves\[:20\] ở root\]

---

## **2\. Trạng thái mục tiêu (Goal State)**

Thuật toán **dừng** khi duyệt xong `sorted_moves[:20]` ở root hoặc bị cắt bởi `depth=0` / `time > 1.2s`.

**Quy tắc cập nhật α, β và cắt tỉa:**

| Node | Cập nhật | Cắt tỉa |
| ----- | ----- | ----- |
| **MAX** (Đỏ) | `alpha = max(alpha, value)` | Nếu `alpha ≥ beta` → cắt nhánh MIN còn lại |
| **MIN** (Đen) | `beta = min(beta, value)` | Nếu `beta ≤ alpha` → cắt nhánh MAX còn lại |

**Điều kiện cập nhật `best_move` tại root:**

\# Tại root (MAX node):

if score \> best\_score:

    best\_score \= score

    best\_move  \= move

alpha \= max(alpha, best\_score)

---

## **3\. Các bước tìm ra solution (chạy tay)**

Trình bày **nhánh tiêu biểu** minh họa cơ chế cắt tỉa. Mỗi tầng là một lượt đi xen kẽ MAX (Đỏ) / MIN (Đen).

---

### **Nhánh 1: Pháo B7→B0 ăn Mã đen**

**Tầng 0 — Root (MAX, Đỏ, depth=4):** Ta thử `Pháo B7→B0` (ăn Mã đen, ưu tiên cao). `alpha=−∞, beta=+∞` → đi vào MIN depth=3.

**Tầng 1 — MIN (Đen, depth=3):** Địch xét các phản công, trong đó có `Xe A0→B0` (ăn lại Pháo đỏ). → Đi vào MAX depth=2.

**Tầng 2 — MAX (Đỏ, depth=2):** Ta xét tiếp, thử `Pháo H7→H0` (ăn Mã đen). → Đi vào MIN depth=1.

**Tầng 3 — MIN (Đen, depth=1):** Đây là tầng lá cuối (depth=1 → sau khi đi sẽ gọi `evaluate_board`).

| Path | Node type | Giá trị | α | β | Quyết định |
| ----- | ----- | ----- | ----- | ----- | ----- |
| B7→B0 › A0→B0 › H7→H0 › **Xe I0→H0** | MIN, depth=1 | **−330** | −∞ | \+∞ → **−330** | Cập nhật `beta=−330` |
| B7→B0 › A0→B0 › H7→H0 › **Mã B0→B1** | MIN, depth=1 | 130 | −∞ | −330 | `min(−330, 130)=−330` → giữ nguyên |
| B7→B0 › A0→B0 › H7→H0 › **Tướng E0→E1** | MIN, depth=1 | 125 | −∞ | −330 | `min(−330, 125)=−330` → giữ nguyên |
| B7→B0 › A0→B0 › H7→H0 › *(các nước còn lại)* | MIN, depth=1 | \< −330 | −∞ | −330 | `beta` không đổi |

**Kết quả tầng 3:** MIN trả về `−330` lên tầng 2 (MAX).

**Tầng 2 — MAX nhận −330:**

alpha \= max(-∞, \-330) \= \-330

Tiếp tục xét nhánh MAX khác ở depth=2...

Giả sử không nhánh nào tốt hơn → MAX trả về \-330 lên tầng 1 (MIN)

**Tầng 1 — MIN nhận −330 từ nhánh `Xe A0→B0`:**

beta \= min(+∞, \-330) \= \-330

Xét nhánh phản công tiếp theo của Địch...

Nếu có nhánh MIN cho giá trị \< \-330 → beta giảm thêm

→ Truyền beta ngược lên root

**Tầng 0 — Root MAX nhận giá trị nhánh B7→B0:**

Giả sử nhánh B7→B0 trả về \-330

best\_score \= max(-∞, \-330) \= \-330

alpha \= \-330

→ Tiếp tục xét nhánh tiếp theo (sorted\_moves\[1\])

---

### **Nhánh 2: Pháo B7→D7 *(nhánh tốt hơn — solution cuối cùng)***

**Tầng 0 — Root (MAX, Đỏ):** Thử `Pháo B7→D7`, `alpha=−330` (kế thừa từ nhánh 1).

**Tầng 1 — MIN (Đen, depth=3):** Địch xét tất cả phản công. → MIN trả về giá trị tốt nhất cho Địch (tệ nhất cho Đỏ).

**Tầng 2 & 3:** Duyệt tiếp, `evaluate_board` tại lá.

| Path | Node type | Giá trị | α | β | Quyết định |
| ----- | ----- | ----- | ----- | ----- | ----- |
| **B7→D7** › *(phản công Địch tốt nhất)* | MIN, depth=3 | **\> −330** | −330 | \+∞ | Trả về giá trị tốt hơn nhánh 1 |

**Tại Root — so sánh với nhánh 1:**

score(B7→D7) \> \-330 \= best\_score

→ CẬP NHẬT: best\_score \= score(B7→D7), best\_move \= Pháo B7→D7

→ alpha \= max(-330, score(B7→D7))

---

### **Minh họa cắt tỉa Beta**

Tình huống: Root đã có `alpha=A` từ nhánh trước. MIN đang duyệt và tìm thấy `beta=B ≤ alpha=A`.

Root MAX (alpha=A)

    └── MIN node (beta đang giảm dần)

            ├── Nhánh con 1 → trả về X \< A → beta=X ≤ alpha=A

            ├── Nhánh con 2 → \[CẮT TỈA — không cần duyệt\]

            └── Nhánh con 3 → \[CẮT TỈA — không cần duyệt\]

Lý do: MIN sẽ chọn giá trị ≤ X \< A

→ Root MAX sẽ không bao giờ chọn nhánh này

→ Không cần duyệt thêm

---

## **4\. Kết luận Solution**

📷 *\[Hình chụp bàn cờ với mũi tên Pháo B7→D7\]*

**Alpha-Beta Pruning chọn nước: Pháo B7→D7**

|  | Chi tiết |
| ----- | ----- |
| **Nước đi** | B7→D7 |
| **Quân di chuyển** | Pháo đỏ tại B7 |
| **Depth tìm kiếm** | 4 tầng xen kẽ MAX/MIN |
| **Số nước xét ở root** | Tối đa `sorted_moves[:20]` |
| **Giới hạn thời gian** | 1.2 giây — kết quả có thể thay đổi theo tốc độ máy |
| **Cơ chế cắt tỉa** | `β ≤ α` → bỏ qua nhánh, tiết kiệm thời gian |

$$\\boxed{\\text{Solution: Pháo B7} \\rightarrow \\text{D7},\\ \\alpha\\text{-}\\beta\\ \\text{depth}=4}$$

**So sánh Alpha-Beta với Minimax thuần:**

|  | Minimax | Alpha-Beta |
| ----- | ----- | ----- |
| Số node duyệt | $O(b^d)$ | $O(b^{d/2})$ tốt nhất |
| Kết quả | Giống nhau | Giống nhau |
| Tốc độ | Chậm hơn | Nhanh hơn \~2× nhờ cắt tỉa |
| Cơ chế thêm | Không | Tham số α, β \+ điều kiện cắt |
| Giới hạn thời gian | Không | Có (`> 1.2s` → dừng sớm) |

# 

# III. THỰC NGHIỆM VÀ KẾT QUẢ

Phần thực nghiệm chia thuật toán thành 6 nhóm. Mỗi nhóm có 3 ảnh động minh họa quá trình thuật toán chọn node hiện tại, cập nhật frontier/candidates và explored/kết quả. Các ảnh động sẽ được chèn sau khi nhóm cung cấp file minh họa.

## 3.1. Nhóm thuật toán 1 \- Tìm kiếm mù thông tin

Ba ảnh động cần chèn trong nhóm này:

**\[CHO ANH DONG BFS TAI DAY\]**

**\[CHO ANH DONG DFS TAI DAY\]**

**\[CHO ANH DONG UCS TAI DAY\]**

## 3.2. Nhóm thuật toán 2 \- Tìm kiếm có thông tin / Heuristic

Ba ảnh động cần chèn trong nhóm này:

**\[CHO ANH DONG Greedy TAI DAY\]**

**\[CHO ANH DONG A\* TAI DAY\]**

**\[CHO ANH DONG IDA\* TAI DAY\]**

## 3.3. Nhóm thuật toán 3 \- Tìm kiếm cục bộ

Ba ảnh động cần chèn trong nhóm này:

**\[CHO ANH DONG Hill Climbing TAI DAY\]**

**\[CHO ANH DONG Simulated Annealing TAI DAY\]**

**\[CHO ANH DONG Beam Search TAI DAY\]**

## 3.4. Nhóm thuật toán 4 \- Tìm kiếm trong môi trường phức tạp

Ba ảnh động cần chèn trong nhóm này:

**\[CHO ANH DONG Online Search TAI DAY\]**

**\[CHO ANH DONG AND-OR Search TAI DAY\]**

**\[CHO ANH DONG Belief State Search TAI DAY\]**

## 3.5. Nhóm thuật toán 5 \- Thỏa mãn ràng buộc

Ba ảnh động cần chèn trong nhóm này:

**\[CHO ANH DONG Backtracking MRV TAI DAY\]**

**\[CHO ANH DONG Min-Conflicts TAI DAY\]**

**\[CHO ANH DONG AC-3 TAI DAY\]**

## 3.6. Nhóm thuật toán 6 \- Tìm kiếm đối kháng

Ba ảnh động cần chèn trong nhóm này:

**\[CHO ANH DONG Minimax TAI DAY\]**

**\[CHO ANH DONG Alpha-Beta TAI DAY\]**

**\[CHO ANH DONG Expectimax TAI DAY\]**

## 3.7. Minh họa giao diện chương trình

![][image1]

*Hình minh họa màn hình chọn chế độ chơi.*

![][image2]

*Hình minh họa màn hình chọn cấp độ thuật toán.*

![][image3]

*Hình minh họa bàn cờ khi chạy thuật toán.*

## 3.8. Link GitHub

Mã nguồn dự án: [lwd7071/chinese\_chess](https://github.com/lwd7071/chinese_chess)

# **IV. ĐÁNH GIÁ VÀ THẢO LUẬN** {#iv.-đánh-giá-và-thảo-luận}

Phần đánh giá dùng cả bảng biểu và biểu đồ. Các điểm trong biểu đồ là điểm tương đối theo thang 100, nhằm so sánh trực quan giữa tốc độ, chất lượng nước đi và mức sử dụng bộ nhớ.

| Nhóm/thuật toán | Ưu điểm | Hạn chế | Đánh giá |
| :---- | :---- | :---- | :---- |
| BFS/DFS/UCS | Dễ chạy tay, dễ quan sát frontier/explored | Chất lượng nước đi chưa cao nếu thiếu heuristic | Phù hợp học thuật và minh họa. |
| A\* | Có định hướng bằng heuristic | Phụ thuộc hàm đánh giá | Tốt hơn tìm kiếm mù trong chọn nước. |
| Beam Search | Nhanh, kiểm soát số nhánh | Có thể loại nhánh tốt quá sớm | Phù hợp khi cần phản hồi nhanh. |
| AND-OR | Mô tả tốt phản ứng của đối thủ | Cây tìm kiếm phức tạp | Phù hợp lập kế hoạch chiến thuật. |
| Min-Conflicts | Tốt cho ràng buộc an toàn | Không phải thuật toán đối kháng thuần | Hữu ích để lọc nước đi nguy hiểm. |
| Alpha-Beta | Chất lượng cao, cắt tỉa hiệu quả | Cần sắp xếp nước tốt và độ sâu hợp lý | Phù hợp nhất cho bot mạnh. |

![][image4]

*Biểu đồ 1\. So sánh tương đối các nhóm thuật toán theo tốc độ, chất lượng và bộ nhớ.*

Nhận xét: nhóm tìm kiếm mù phù hợp nhất để học và chạy tay vì cấu trúc đơn giản. Nhóm heuristic và Alpha-Beta cho chất lượng nước đi tốt hơn vì dùng đánh giá thế cờ và xét phản ứng đối thủ. Beam Search có tốc độ tốt nhưng cần chọn beam width hợp lý. CSP hỗ trợ tốt trong việc tránh nước đi vi phạm ràng buộc hoặc làm Tướng nguy hiểm.

Ý kiến của nhóm: trong bài toán Cờ tướng, không nên dùng một thuật toán duy nhất cho mọi trường hợp. Có thể dùng nhóm tìm kiếm mù để minh họa, dùng CSP để lọc nước nguy hiểm, dùng heuristic để sắp xếp nước đi và dùng Alpha-Beta làm thuật toán ra quyết định chính.

# **V. KẾT LUẬN** {#v.-kết-luận}

Báo cáo đã trình bày bài toán AI Cờ tướng, mô hình PEAS, cách áp dụng 6 thuật toán đại diện và ví dụ chạy tay theo bảng Node \- Frontier \- Explored. Cách trình bày này giúp thấy rõ sự khác nhau giữa tìm kiếm theo chi phí, tìm kiếm heuristic, tìm kiếm cục bộ, lập kế hoạch AND-OR, thỏa mãn ràng buộc và tìm kiếm đối kháng.

Kết quả cho thấy BFS/DFS/UCS thích hợp để minh họa quá trình tìm kiếm, còn các thuật toán như A\*, Beam Search và Alpha-Beta phù hợp hơn khi muốn bot chơi hiệu quả. Trong hướng phát triển tiếp theo, nhóm có thể kết hợp Alpha-Beta với heuristic và bộ lọc ràng buộc để cải thiện chất lượng AI.

# **VI. TÀI LIỆU THAM KHẢO** {#vi.-tài-liệu-tham-khảo}

1. Stuart Russell, Peter Norvig, Artificial Intelligence: A Modern Approach.  
2. Tài liệu môn Trí tuệ nhân tạo: Search, heuristic search, CSP, adversarial search.  
3. Python Software Foundation, Python Documentation.  
4. Pygame Community, Pygame Documentation.  
5. Mã nguồn dự án Chinese Chess AI: https://github.com/lwd7071/chinese\_chess  
6. README.md và tài liệu trong thư mục docs của dự án.

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAf4AAAGPCAYAAAC9EbJBAAAmUElEQVR4Xu3d999cZZ3/8RAChNASauhJIIUqHZdeQhMDoUh16Qi4grQQQigCUhRQigYIJSCE0MRFZHepfgV2db+ALk0RgrhUd6kP+QPO3p9ze02ueZ9z5p77zvncXpl5/fB8ZOac67SZe85r2n1nyIQJE7Lp06dnTz31VPbFF18AAIAO8vbbb2c33nhjttVWW2WjR4/OhsyfP78wCAAAdJ5p06ZlQ3QiAADoXIQfAIAuUhn+P/zh5ezOa9fOZs86M7/+pz/9KXv6ab4HAADAoqw0/I8+/KPsmYe/nH34v3/Jnv63C7PPfj8u+49fXpm9/Jtp2ev/OaUwHgAALBpKw//IPftmz//y+Dz8zzz7aPY/L03M3v/Le9kb81/NXnvuK9kHH3xQWAYAAKSvEP7nnns2e/f/j8n+65ljst+/8bvszluOz/731W2yx556Inv3g3eyF546IPvti78urKixwiFDco8//nhj2gknnFAYN2fOnMZYo/NVO2Na0eUnT55cGKNsmUsvvbRpmbFjxxbGLSzdtyDeVtltGJZt9zbsDzvW/q7X7lOdVuftFf9MAcBgeu6557IPP/ywwKbrWA+33z4nG7HscoVpRsf2pRD+B+4+K/vzb9bNXnt67eyDF3tO2m9unn32+w2yl359evZfzx6XffTaFtndN+9TWJHp6yRfFpFWy7zyyiv5v+GEP9ATvwVJo9RO+ONxZfvuyZ5wxE86ysLvuU/x7WO3ezvb0tvYtLp/+2ug9z8ALKxnnnmmMK3VdC8h/gONvimE31xz4RrZJ6+Oy7744/q93pjUc31Cz5OBMdlfXtkmu/H64wrLlJ2Uw6t6u1wV2jgMcejC5bL5YZ32rz05MCE6ZYEK0/TVu46rYvsQnoRogO24w/bDvLDPYRu23bAPYZ6NrdrnOLRhjG43HHc8LSyr4+Pby/61fQi3RRint4deD+PCcjbfth/vZ9ltYP+GfdL71KaH20+Xi28T3X8A3cnOAWV0nIeqwFdN92TxH2j0TSH8M84/N/vN8/+ezTzvqOyTP2yRffHWtj2v+r/UY+Psigs2zM7+p00KKzFl4bc7JI5TX68INfy6znAHx/Gxy3Gkyn4I4sCGdWrYwlvbZfto88qCavselomXC5fjbYTL8fLxfsXbi2MZ5rUT/nh98Tr1CVO4zWx81YNHb5+w/fCkJIwP90G8/fhyfP+WHUvYTngSUTYm3Bb68wAAg6Uq8FXTvYRX+vq2f38Uwv/Sa/+ZbbH1ptkW22yWPfXMY9mtt1yQ/ePXt8v223+X7MRvnpLNuPD8wkoCjYWd9EMAykIVxoTL8cneYqLLhLEa/rJXt/F6wuUQurBsPK5KGK9B0vWWRS/el3A5Pt6ycfE24u1o+HVdYX1hWrw/VeFvFdL49rHx8av0eF3x+LLbIN7HsE69z+Nl9XY2Yf/j2xwABlNV4Kume9C39wca/0L4n37mF9lXpkzO9vnqbtk11343u+yKi7KLzjkzO+nIw7Jbdt8pO+/4YworaawsioGduO1k3ldo9RVheNs8nOTLQqnhD28Z6z7o8vH8qv2J2THokw0NfzjOVtGzMfoEoix2QRxkuz3sen/DH6+zKvx2Ofyr649vn6p12X6FYwi3QxgX3wbhCVw4rvhJhE23bYXtl4VfbzsAGGwd/eW+V197LbvzrpuyO247M3v5/+2Y3Xnjftl3v3dxNvOIQ/NX/GedM62wkpRoDFNRtl9xKAEAqPLXv/61MG2gCuE3F547NZv9vdHZRy/1xOqNDbJ7Z62dXXbepOz1118vjE2Bfu6cCou97VPVuwuEHwAw2ErDDwAAOhPhBwCgixB+AAC6COEHAKCLEH4AALrIkI+evSIDAADdgfADANBFCD8AAF2E8AMA0EUIPwAAXYTwAwDQRQg/AABdhPADANBFCD8AAF2E8AMA0EUIPwAAXYTwAwDQRQg/AABdhPADANBFCD8AAF2E8AMA0EUIPwAAXYTwAwDQRQg/AABdhPADANBFCD8AAF2E8AMA0EUGLfwbjF8XAABU0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfyotMLMC7MhP300G3r3A9l6225ZmL8oWH/LTfNjMMtecnlhPgCkQrvphfCj0qSJ4xrRHH79jYX5i4Klr76ucQwTN1ivMB8AUqHd9EL40dKETTdohHONrx1cmP/3Zvu1xK0/KUw3a+331Xz+kjfPycZvvnFhPgCkRLvphfBjwBa77+E8rKsed1xh3mBY9dhje9/Cv+x7hXntCE9odDoA/D1oN70Q/i6x/PkXNUKndOykiWOzYbfPLYwzo848O5s0ab1snX32bExb7eijC+swumyVUWefk49f7eijGtPW3nefwvrW2WuPwrJDHvxFYdzoI44ojjP3/zwbt9222YQvbZgNv3ZWY7ruqx37hI0nFtZrH3eEMXY76Hyz0qmnFbcb0fF90eVHnnNuYYxZf6vN+ty3haX7Es+zn5l43uqHHZpPj/dLl2m17naO05TdT7o+nWfGb7ZxNvSenxa2G6x+xOGFZUzlz1aPMbvtXBjf3/tF16nWPOjAwjKm1WN2xFXXNu2bzm9FtwNf2k0vhL/DxZ/TV4nHr/flrQrz+6LbDHRclYGGX+fbvi9xy52F9bcyctr08n198JHC+luFf9KEMcV1lNB1tlK1Th1n+huYgVh3j92a9mOtqfs15jXd7tGTMQ21rtMM9Dh7t1W8n0zVeqq2pSzwus52frZGnTWtcn/buV90fWXG/cPWTcu0+5gdOa33yZROb0X3D760m14Ifwdb/fDDCg/ktfaf0phvn9+vfPLJjesrzDi/aeyw2+7KTyrje14hr7N3c3SXu/iywvZaCZ+3tzqhLGz443nG1jdxg/Xzfdd3POwVUqtlzSonfqNpTFX47VVY07IPPJKN3XmHpmXX6zlZ9/e3CuxJSby9cLnsS4r9DcxAhY93Aptmt3E8Lf4+hYZa12fi44z1dZyB3k+mapu67MhzZ+ZPBsJ8u2zvVqxx6CHN+zh9RtNyax6wf2PeSqd+u2neuO22Kd3fdu6Xqv1e5oqrG9OXufLqymXMWlN7981+5uxdruZ927btbWLwaTe9EP4Otvhd9zU9qNf+yt6FMTF7pRaPn7jRhKb5dkIZ6EnCO/zjtv9y07yyz/3jk2A4OTbmRcsGi937z01jqsK/+B3zmpZbd/ddC9seiMV/suD+G7vjdpX7bvobmIHSyNk0+46HTgs01Lo+Ex+nPWlq9zgDu5/sCWo8rmyb9vMcT7f7TddfxmJp7yyE5exJpI5ZbN7PGvPt12DD9P7eL2X7beyxG6YPv/bHjen6cx9v26y75+SW81ttE4NPu+mF8Hew+AFd9Tl8YJ/bx+PX3XP3whizxOw7FozZY7fC/Cre4Y9PvDov0M+h43nx9Njq0Su/qvDH4/u6nfsjrHPFM85qur7YvT8rjO1vYBZGfLz21nZ8XZ9caqh1XfH67DhXOeHEto8zfLmzbN1l0+0drLLpfVls3kN9LqcfIYTvCPT3fqnajn2sEqbHH0PEP/dl3zEwS954W+V6W20Tg0+76YXwd6jVjloQ0XYe0PEJt9X4OL4jvv/Dwvwq3uGPp4dQlmln+fFbbJL/0SIdVxZ+C33VOheG/epkWOekSePyafFnzDq+v4FZGPGrz1jZH3nqK/xlx9lqfLw+e+IZ30/xq9mydcTTVjjvgsK6q8TLrXj6mYX5ZeOW+vHsfFp/75ey/V5nrwWv2vVXV8vGK33Vr/NbzcPg0m56IfwdaoXzmj+v1/lKPwPX+YGdnMMY+1a0zq8ymOGPv3Sm2lnersev4OxdDptWFv7w1w11nfnbw9H0xnJ/+yJjX+KPJcI0u03CNP3WeX8Ds7DGbd98fMPmzC2MMa3CP36zjUqPMx7f6jjt50FfaU/ccP3COsrWu+YBU0un97Vcuz9b9l0I3d927hfdh1jZk454vs4L4sds2bhW8zC4tJteCH+HqgpSlRVmzGxrvP0qXBhTdbIv01b4o3cpFib84VfJyrSzfJi2ykknN6bZZ+zDr1vwK4CN8MsXIsOyCx3+v423vzxYNt0+C4+n1xGY9bbZojCujMV26R/+qLC8jjOtwr/0Ndc3psfHaV+CbCzT4jjt58GmxffTkAd+nk8r22Y8Lf4IJ57e53Jt/mzZuzO6vwO9X9SY3XcpHa/rCuLHbNm4VvMwuLSbXgh/h9K3+uNvLpexbzG3cwJY9YQTGmPKvuRUpZ3wx18eHH3kkYX5axx8UOU64ukWaF22bFxb06MvdS19zYI//xtO4qOPbP69bt2eaTr5txF++5Z6vM4qldsYYGDaDX/T2+vRO0v29rb9+mg8tlX4dftVqtYXwm8shmG6/eyULR9PG97zxCVer667P8uVjVvxjN5X5wtzv8TTJ2wyqWle+KNZVeNjqx53fMtxreZhcGk3vRD+DhY/oIfNuacwX8Xjq05w8Rj7LFznV2kn/BM3HN+YX/aN6/iLheGVXRC/DW/01/VM/Hl8eCs2qNo3+wMx8byg6st99kpYt9vf8Ou2qqx6/Anl22gjMAO1zt4L/nCTsWnxr/gNnftg0/iqmI7dacFvKfSl6jjj8Jtht99dWNaE+fanm+Pp4TsFZeuOlyv8bJU8iV798MMb8+23FOxnWdfZzv1Stv2yeeGb/fG+2R/qKdu3eLnF77q/5Xydh8Gl3fRC+DtY/IA2+oc/zPpbb1Y5Xn+Pes0Dpw74JNFO+E2rMfG8+FeajO7bchddUlw++jxZ/zJcu9sNqsJvwufMgVf44/84qb+BGaglb7q9aR9smv1hGJ0WVMVUfy2wlarj1PDb36jQZU2Yr+8ELPedS9vaV/3ZGnnOjKblTPzt+lVOOql0ne3cL2XbL5u3zOXfz6f1tW/r7LNX0/yVTz6l5Xp1HgaXdtML4e9g+bevo7eqA3urNv4VpTDefhc6fhu3lTUPPKCwvVbaDX8727d3A/RvDLS7bKDLtppn72zo8vFJfMwuOxZ+ndDekbAnJ0vOurV5uT7Cb79GGcaOuKr8tybi9YUTeX8DMxD6F+Kq/gys/TnkML0qpvG0do6zbH0aflP2MxDPL9xPP+398qbeT7qcHrvJtyV/IMeux8v1936J1zV25+1za03ZN3+lHs+zn7mwTNkxl03Td8nKtqnzMLi0m14IfxcoO9m1erBX/c3vYCD/S1+74Te6vSYVJ6/AToiFZSL6R3nKtqnzzIirr20aU3YSt1+10u2psm9mB/bWc/xHl9bfevPCGKN/mMmm9TcwA9F0LPJ/JKz47TOa5ttfhbTpZeHXb5m3c5xjd9q+sL6y8Ou3/MM2Y+3cT2XLjdl1p8IYpX9Vr7/3i66vTNmT3r4es/oRTNU2dR4Gl3bTC+HvEvaWvr39ba+W7TNZewVhf3bXfi1Lxxr7VavlL7w4W/zOe/MTsP0REPvCoI5rV3/Cn4+fun+21A03ZcNsf3ueuCz9gxvyP72r46rYt6+XmnVL/grM9n3ZSy9v+eW1dvYtHlN1Ere3+S2C+e/cP/BI/iuP9gq4nT/sY7d3O/tRdlv2NzD9Ners6M/q9hxX2cdG8T6Fb+OXhX8gx1n2Lfmy8Bv7M9Ttrt9+riyK4X6yLyuW/T2CWONnq+dJqC237KVXNG3P1mlfxrOx/b1f4vU09DzJsuO3P1ik42P2mG36uZ91a+mXZFU7txUGh3bTC+EHgIVU9nGQ/Q+AOg5oRbvphfADAJAA7aYXwg8AQAK0m14IPwAACdBueiH8AAAkQLvphfADAJAA7aYXwg8AQAK0m14IPwAACdBueiH8AAAkQLvphfADAJAA7aYXwg8AQAK0m14IPwAACdBueiH8AAAkQLvphfADAJAA7aYXwg8AQAK0m14IPwAACdBueiH8AAAkQLvphfADAJAA7aYXwg8AQAK0m14IPwAACdBueiH8AAAkQLvphfADAJAA7aYXwg8AQAK0m14IPwAACdBueiH8AAAkQLvphfADAJAA7aYXwg8AQAK0m14IPwAACdBueiH8AAAkQLvphfADAJAA7aYXwg8AQAK0m14IPwAACdBueiH8AAAkQLvphfADXWj+/DezTz7+OLvoghnZ/ffNy7bYdFJhTDvm3XN3vvz7779XmAegf7SbXgg/gEXS559/XpgGLMq0m14IP9CmjSaOza6/9po8OMF98+Zm06edkV/+5dNPNsZefOHMfNq//eu/5Ne33nzjpuXMG3/8Y2N8mPbWW/Mb0/79uWcr42b78umnn/ZrX3Rbga67bEzvOp9qGvOv//KLpvl2PFOn7F1YlynbX5se9rds21XbCV584fnS8cCiSrvphfADbQqBOfiArzZNbxXbEH67/Oc/v92Yv+GEMfm0nz30YNO6zbFHH5FPaxV+m/7RRx/1a1/iZeP5ZXTMN086Pp92ztmn59cvOG96fn3bLTfJr4fjKdvfk088trG/Oq+v8Ot2zJNPPFY4Hl0HsCjSbnoh/EAbtttm88rAtIqthX/nHbbJLx9y0H5Ny9ln7GF99u/NN/04u2nWDY1pVeEP+3LowVML81rtS7iu88uUjbFp7/z3fzeOR/ctHM83jj+6afpnn33W5/7qduLbRed/aaPx+bRTv/mNyjHAoki76YXwA22wV9ZVgQnxKmPht+DZ5Z2237ppuT+99VZT4G6dfWO2+SaT8stHHHpgZfjDvtgTAJ3Xal/CmKrpVfPPO/fsxnSLeDgeXTYcz3nTe8fr+gayv2XbCdPPn3FOyzHAoka76YXwA22Y8pU9KgPT6lW2hX+fPXfNL3/twClNy2ngbr3lpvzynNtuya8/86tflm4v7EvZ5+mt9iXerr6aV2VjbNorL7/UOB7dtzDt2KMOL53ean/LxuvlYMGTo4MqxwCLIu2mF8IPtCkEZo/ddmya3iq28Wf88Rf3wmfid8y5tTE/hD/eVlXQbLr9Cl1/9iVeVqOudMzMGdPyaXtN3im/ft0Pr86vb7XZhvn1Vp/x337r7Mb+6ry+wq/bMbZfejy6DmBRpN30QviBNtkrXXvFG0Jj+vomfQh//Ll48NvfvtgYb9fj8NuX2VoFLX7V3e6+xNuK6brLxpgLZp7bNOY3v/6Ppvl2PJN32b6wLlO2vza9r/CXbcfY7Vk1HlhUaTe9EH4AABKg3fRC+IFB9Poffp+/Ot1s4wmFeYsqXm0D9dBueiH8wCC6/LsXZ3PvvrMwfVH24YcfFqYB6D/tphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/ajXkp48CqJk+ztCZtJteCD9qoycrAPXRxxs6j3bTC+FHLfQkBaB++rhDZ9FueiH8qIWeoADUTx936CzaTS+EH7XQExSA+unjDp1Fu+mF8KMWeoICUD993KGzaDe9EH7UQk9QAOqnjzt0Fu2mF8KPWugJCkD99HGHzqLd9EL4UQs9QQGonz7u0Fm0m14IP2qhJygA9dPHHTqLdtML4Uct9AQFfyuvvHI2av3xhekLa7G7H8xWWmWVbNkpU7NhV1+fjdx0s8IY/H3o4w6dRbvphfCjFnqCQr0W/+GsbNT4CYXpMXsioNPQWfRxh86i3fRC+FELPUF1o6XOOCeP75Izv9M03aYN+8GPGteH3vKTbMTXj8lWHDM2W3HtdbLl9tgrn77MoUfkY5c58GtNy5oV11knW/y6mxrTl9tz72yl0aOzFcetlw0/7axsyLyfNcIflqnaP2Ov6EdutEm2xHcuK4wL67Ixtq9heti/eGxb21pzzWzkZptni931QNMYOwZ7x8KObekTT8mnLb/r7o3lYsO/eVphG91IH3foLNpNL4QftdATVDeKYxdPt+sh/Mt87fDeGK6xRjZ09p25Zfc/sHdei/APuf/nvdN6/rXrI7fYKhty7z9nQ2+aU9imXtf9W2G7HXrW83A24qjjete15Vb59TBu+V1263lCsnbvvOht/oGE3y4P/6fTm8dFxzDs+9c2jmHFMWMK6yb4zfRxh86i3fRC+FELPUF1oxA7e6U8asLExnSbFsJvl5c5+LDCsqad8I/acKNCaJe47Kp82uKzbmteRtbfFP6/TVt+x53zacvvuEvTNod/64zCegYafjNq0oaN662OYbE75jWtm/A308cdOot20wvhRy30BNWNGrGb91D+77Arf5BPzy/3hH/YVdc1xW3UBr0xzKfdPret8FeFNo/kqWf2OSZm05Y8/+L8sj1ZseuL3zC7MW+Fbf8hv7zEFdfk1wcS/mClVVfNhjzwSMtlbNrwb5/dfJ3wN9HHHTqLdtML4Uct9ATVjeJXucsceEh+ecSRR+X/WvhDVOPP6u1zb5tm4R9x5NH55WWnHtSYn0dzjTWarhei+bcnGiHQpWOi/Ytf8S993En5NHsVbtftM/ewfGCfwdu8sH/xOvP9G7165bbssn0xceRmWzSul+5fOIZLrmxaN+Fvpo87dBbtphfCj1roCaob6dvbcTzjt/pXHDs2G3rb3fn1OPzDrr7hb6FdcHvadXsSEa6P+Mdje8fPfbAxzUJett2q/YvDb9ft1Xj8McFSZ89YsMzp0xrrCvs35J6HmpZfdr8DKrcVri95wSW9+/2T+9s6hrBuwt9MH3foLNpNL4QftdATVDfS2NnvwYcIh/CHz7pHTZyUR3+JS67ojWBP+G2+fdHOrg+98fZsyRkX5pcXv/7mxjotljZtha23zYbc93A+Ll/fRhs3xoRtVu1f+HLfMod9vTeuJ5/aO+ae3lfdQ2++o7HM0J4nBPn+3d37jXy7vNzuezbtX/wbC7otu2xPGEZuvEnjenwMw665YcEx9Nwm8TryfSP8TfRxh86i3fRC+FELPUF1Iw2/Ca904zhaMJfbY+9spdVX73n1Py4bcfTxTcvYxwP29v6oCRPyMOp27PN++zLeSqutlr97sNSZ05vm9xV+Y5/pr7Dl1tnQW+9qzF9+p11Kl7Npy2+/Y355sTn3ZCM3/VLv/o2fkH8rX8cXtjV69fyjhPhXA8Mx5L/S2GP46WcX1kH4i/Rxh86i3fRC+FELPUEBqJ8+7tBZtJteCD9qoScoAPXTxx06i3bTC+FHLfQEBaB++rhDZ9FueiH8qIWeoADUTx936CzaTS+EH7XQExSA+unjDp1Fu+mF8KMWeoICUD993KGzaDe9EH7UQk9QAOqnjzt0Fu2mF8KPWugJCkD99HGHzqLd9EL4URs9SQGojz7e0Hm0m14IP2qlJysAC08fZ+hM2k0vhB8AgARoN70QfgAAEqDd9EL4AQBIgHbTC+EHACAB2k0vhB8AgARoN70QfgAAEqDd9EL4AQBIgHbTC+EHACAB2k0vhB8AgARoN70QfgAAEqDd9EL4AQBIgHbTC+EHACAB2k0vhB8AgARoN70QfgAAEqDd9EL4URv770N32GEHADXTxxo6k3bTC+FHLYg+4Esfc+g82k0vhB+10JMUgHrZk2t93KGzaDe9EH7UQk9SAOpF+DufdtML4Uct9CQFoF6Ev/NpN70QftRCT1IA6kX4O5920wvhRy30JAWgXoS/82k3vRB+1EJPUgDqRfg7n3bTC+FHLfQkBaBehL/zaTe9EH7UQk9SWHR88skn2QcffFCYjrQQ/s6n3fRC+FELPUkhXfvtt1/21ltvZRdddFH25JNPFuYjTYS/82k3vRB+1EJPUgDqRfg7n3bTC+FHLfQkhaJLL700+/zzz5u8+uqrjfn26lvnH3PMMdkTTzxRmG6uuuqqwjZ0jHnuuecqx1133XWF6fPmzWtcP+SQQ/JpO++8c+U6AjuWPffcM5+31157FebPnz+/dLlA149mhL/zaTe9EH7UQk9SKArhD9d/97vfNa5feeWV+eV33nmnMf9Xv/pVIYh2vSz48fxnn322cX369On5tEsuuaQxbcqUKfm0559/vnT9/Ql/2FY4ltmzZzfmxcey44475tMefXTB/+lg13X7qEb4O5920wvhRy30JIWiOPzhFfFjjz2WXw8RPPHEExvjd91113zaWWed1Zhm1/sT/jDt3XffbVx/8cUX8y/0HXzwwfk8i3I8tr/hj4/F1jV16tTCsRjbZhz6cMy6XpQj/J1Pu+mF8KMWepJCUdlb/Y8//ng+L1zff//9m5axafGrdbteFX5d9+WXX96Y/vHHHzeNmzlzZuPyfffd1zSvP+GP2bHsu+++2SmnnFJ6LPYOgE3X5XW9KEf4O5920wvhRy30JIUifav/9NNPz69Pnjy5EcXrr7++Mf+0007Lp4XPzY1drwp/mF/2in/u3Ln55W9961uFYJtp06Y1xoYnI+bkk0+ujHO8rXAsn376aeNt/fhYwnh9AlK1bhQR/s6n3fRC+FELPUmhSMNvsbXre++9d/7ZuF1+++23G/MtqhpGu96f8Nurfpt26KGH5tcfeuihpnWGfQqfvdvl9957rzF/1qxZhX0o21Y4ljBWjyU8Gbj33nublq9aN4oIf+fTbnoh/KiFnqRQVPZW//vvv9+Y/8ILLxTm2+fw8TpsWl/hV/bFQZt3wQUX5NfffPPN0mXs8uGHH15Y/uqrry5sp2xbdiz2Wwg2L3zOH3v55ZdLl9f1ohzh73zaTS+EH7XQkxSAehH+zqfd9EL4UQs9SQGoF+HvfNpNL4QftdCTFIB6Ef7Op930QvhRCz1JAagX4e982k0vhB+10JMUgHoR/s6n3fRC+FELPUkBqBfh73zaTS+EH7XQkxSAehH+zqfd9EL4UQs9SQGoF+HvfNpNL4QftbCTkp6oANRHH3PoPNpNL4QftSH+gA99rKEzaTe9EH7UyuIPoF76OENn0m56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgg/AAAJ0G56IfwAACRAu+mF8AMAkADtphfCDwBAArSbXgYt/AAA4O+P8AMA0EUIPwAAXYTwAwDQRQg/AABdhPADANBFCD8AAF2E8AMA0EUIPwAAXYTwAwDQRQg/AABdhPADANBFCD8AAF2E8AMA0EUIPwAAXYTwAwDQRQg/AABdhPADANBFCD8AAF3k/wBWivEhDHpjHgAAAABJRU5ErkJggg==>

[image2]: <data:image/png;base64,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GN31EXxyNX3llVeG2uKqFvB4Xbccvwgo83guv94GYJ/0CY3sL+CkRq7o48g+4ThJWVzwu2MvtC/uMXL7xDjd4+Gu444vqY3uH1O0xeuCZZlSaTD480/npw8MfkqtmOCX9/jdq/iWLVvaYHUDUZP3tN3gwtU0+sGHzXTwY4rb2ZiXK3bA7epJkyZF1nfb66tkoa/4AScycgcjjpzMYPyDBw+289hfbFfG27p1a7uMtzwwNnd9jE2CF+1l33Tw67HrZaGPEZbl2OvjIdzx6TZ6HDJelKMt7iygPV6fa6+9NtSWqo7Bn386P31g8FNqxQT/yaDf488yeduDqBAGf/7p/PSBwU+pZS34cbsbV7N4X1/XEdVkDP780/npA4OfSkL/gSKi0tP/7yh/dH76wOCnksHVCBH5of+/UT7p/PSBwU9ERJQROj99YPATERFlhM5PHxj8REREGaHz0wcGPxERUUbo/PSBwU9ERJQROj99YPATERFlhM5PHxj8REREGaHz0wcGPxERUUbo/PSBwU9ERJQROj99YPATERFlhM5PHxj8REREGaHz0wcGPxERUUbo/PSBwU9ERJQROj99YPATERFlhM5PHxj8REREGaHz0wcGPxERUUbo/PSBwU9ERJQROj99YPATERFlhM5PHxj8REREGaHz0wcGPxERUUbo/PSBwU9ERJQROj99YPATERFlhM5PHxj8REREGaHz0wcGPxERUUbo/PSBwU9ERJQROj99YPATERFlhM5PHxj8REREGaHz0wcGPxERUUbo/PSBwU9ERJQROj99YPATERFlhM5PHxj8REREGaHz0wcGPxERUUbo/PSBwU9ERJQROj99YPATERFlhM5PHxj8REREGaHz0wcGPxERUUbo/PSBwU9ERJQROj99YPATERFlhM5PHxj8REREGaHz0wcGPxERUUbo/PSBwU9ERJQROj99YPATERFlhM5PHxj8REREGaHz0wcGP1ERXjyvAdUA+nUjqml0fvrA4CeqgA4Xyjb9+hHVJDo/fWDwExWgQ4VqBv06EtUUOj99YPATFaADhWoG/ToS1RQ6P31g8BMVoAOFagb9OhLVFDo/fWDwExWgA4VqBv06EtUUOj99YPATFaADhWoG/ToS1RQ6P31g8BMVoAOFagb9OhLVFDo/fWDwExWgA4VqBv06EtUUOj99YPATFaADJQte6trSbL/rd+bYkcNm33MbgvLjx4+b925baOf3rF1lPnr5b6G6w9ves/MoP7Jrp9nUrnFQt6ndOUHbg/94xexceU9ku24f0g5lul0W6NeRqKbQ+ekDg5+oAB0oWYCwRehv7n6eOfDK382xTz4JyuOC/28dm9k6CelNbRra+X3PP2veXTLPngS4/ccFv+5D2jH4iUpL56cPDH6iAnSgnGz/mnOFDdtXBvUOyiR8k4L/g/XrzK5V99n6f4wdbMuO7NweBPnfOjcPbSMu+OP6YPATlZ7OTx8Y/EQF6EA52d656dpPg39Az6DMDf7/+/2v7fyeR/5s9m96zrw99+og3BHcn+zZZetf6tzCHN33oTm6f19kGzr4k/pg8BOVns5PHxj8RAXoQMkChO2xjz82L3VrbW/1//vQwaAc8y91aWmOHzt24iRhln0bQK7shfTzwfrHzYcbn470r4M/qQ8GP1Hp6fz0gcFPVIAOlCzY3KOt2bnij+bYkSPm3wcPmKMffmDLcfv/g6f+Yo4fPWqvzFGGYD701pvBulh+Y/IoO18o+CXg8dZBUh8MfqLS0/npA4OfqAAdKFnzyqA+NnzfumZKpK6c6deRqKbQ+ekDg5+oAB0o5Qx3EeSDfVmnX0eimkLnpw8MfqICdKBQzaBfR6KaQuenDwx+ogJ0oFDNoF9HoppC56cPDH6iAnSgUM2gX0eimkLnpw8MfqICdKBQzaBfR6KaQuenDwx+ogroUKFs068fUU2i89MHBj8REVFG6Pz0gcFPRESUETo/fWDwExERZYTOTx8Y/ERERBmh89MHBj8REVFG6Pz0gcFPRESUETo/fWDwExERZYTOTx8Y/ERERBmh89MHBj8REVFG6Pz0gcFPRESUETo/fWDwExERZYTOTx8Y/ERERBmh89MHBj8REVFG6Pz0gcFPRESUETo/fWDwExERZYTOTx8Y/ERERBmh89MHBj8REVFG6Pz0gcFPRESUETo/fWDwExERZYTOTx8Y/ERERBmh89MHBj8REVFG6Pz0gcFPRESUETo/faiW4CciIqJsYPATERGVEQY/ERFRGWHwExERlREGPxERURlh8BMREZURBj8REVEZYfATERGVEQY/ERFRGWHwExERlREGPxERURlh8BMREZURBj8REVEZYfATERGVEQY/ERFRGWHwExERlREGPxERURlh8BMREZURBj8REVEZYfATERGVEQY/ERFRGfn/AYdGkPqxFb6AAAAAAElFTkSuQmCC>

[image3]: <data:image/png;base64,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>

[image4]: <data:image/png;base64,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vetd7+Ljrbfe+oUXXnjV8Xbttdd+73vfa37kr6mfofOsPN6mfDwMMd6CIBg7dJ5t1HjbZZddjjrqqNmzZ7/97W9PT9OoSK/OnTs3e/9dtmzZ61//+vPPP/+II45ITx9//HHGHnnkkWZyo9BhpjbzDz74YPPpYOJ9f8cdd0wnecMb3vDrX/96MNFuzpw5H/nIR1DhxBNPPO6445ojEB9nQTzQRttuu+0ee+xx5plnpuLpafpg+lR77rnnDjvswE+l8+xVx9u6desWLlz4zne+czDVpiTbPdVMT8844ww8LSysRIy3IAjaRufZ8OPtmWeeOfTQQ/E4PXjssce222679P6bnv7qV7+64oor1q8YpOGBB3fddVf68XWvex1fygbhRqHDTM3XTCa97995552DiW8rjznmmOZLOJj77i0bb9ooC2y11VbNp0DnWXm8zZrgrW9963777TeYalN9igf87s2dtjYx3oIgaBudZ8OPt1tvvfUrX/kKHn/zm9+8/vrr3Xule/PNHm8sOszUZn7p0qXNp4PJf/Z22GGHpR/Td6LpSLvvvjsONuR400Yu0PwNUp1n5fHGx7vuumv6rks31ad4wPGGKVtYWIkYb0EQtI3Os+HHWxoM+DYikb6rePzxx9/85jfjafpm6LzzzsPjxBvf+EY8uOeeewYT3z3gm7zBX/f2qsNMbeZ32WUXPt53330XLlyYjbd777332GOPxVMc7LrrrhtmvGkjDTSfAp1nQ463NH2XLVumm5LyeCssrESMtyAI2kbn2fDjLbHzzjsfddRRRx999E477ZSePvXUU+nVCy+8MP24Zs0axv70pz+lj3z605/eeuut09NHH310y/V/9pPephnbWHSYqc38mWeeuc0221x00UU77rjjQQcdNJDv3tKZ05Euvvji6dOnp0z6YBp4aZak8/OToP4b3vCGM844Y4899sCfpWmjbMA89NBDJ5544l577dX82dN5Vh5v+M3JdLY3velNg6k2bYabD7LxVlhYiRhvQRC0jc6zVx1v3UGHmZqv2dy85vE20sR4C4KgbXSexXirwSc+8YnPfvazRxxxRPpmlx/UeRbjLQiCYNOg8yzGW2voPIvxFgRBEAQjQ4y3IAiCoIfEeAuCIAh6yKYcb0cffTQe/HyCefPm4V9emTVr1sqVK2fOnDkpHQRBEATV2GTj7aijjrr++uvxeMaMGXhwzDHHrFix4u67706P07RjOAiCIAiqssnG26Dxf3DgeEsP0mxbvnx5erxo0SI8CIIgCILaVB9vS5YsefTRR9PjBQsWuP9d0Hvf+978Q0EQBEHwV1BlvJ122ml4gH/59Morr0w/zpkzZ30wJ8ZbEARBsGmpMt4SJ5988llnnYXH8+fPnzlz5uLFi/lqRoy3IAiCYNOyKcfbaybGWxAEQbBpifEWBEEQ9JAYb0EQBEEPifEWBEEQ9JAYb0EQBEEPifEWBEEQ9JAYb0EQBEEPifEWBEEQ9JAYb0EQBEEPifEWBEEQ9JAYb0EQBKPKV7/61R133PG+++7D0/333//www+fHBlfYrwFQRCMJE899dTll1+eHnz0ox9NPx5yyCH4+DnnnNOMjS0x3oIgCEaSn//858uWLUsPrrrqqocffvgtb3kLPs4HY06MtyAIglHlPe95z8qVK/fYY4+HHnooxltGjLcgCILR5rvf/e6gMdV22223SS+PKzHegiAIRpUDDjggffe26667psc//OEPb7755ssvv/zBBx/Mc2NJjLcgCIKgh8R4C4IgCHpIjLcgCIKgh8R4C4IgCHpIjLcgCIIR48nz9xjSfOU4EeMtCIJgxNAx5sxXjhMx3oKRYdq0aatWrbrnnnsG8R+uBuONjjFnvnKciPEWjAwf//jH04+nnXZa+vHEE0/MXw6CsUHHmDNfOU7EeAtGhtNPPx3ftK1Zs2b27NnpO7np06fnoSAYA3SMOfOV40SMt2A0uP/++2+77bb0YPvtt+cHFy5c+Mtf/nJDKAjGAx1jznzlOBHjLRgNHnjggQULFqQH22233dKlS2+//fb0+IILLnj55ZfzaBD0HR1jznzlOBHjLRgZvvCFL2y77bbr1q1Ljy+66KJp06bdeOONeSgIxgAdY8585TgR4y0IgmDE0DHmzFeOEzHegiAIRgwdY8585TgR4y0IgmDE0DHmzFeOEzHegiAIRgwdY8585TgR4y3oOjuc/oMhzVcGQU/RMebMV44TMd6CrqNjzJmv3Hi++93v7rjjjgsXLsTT/fff//DDD58cCYLNj44xZ75ynIjxFnQdHWPOfOXGc84556QfDznkEP7IDwZBd9Ax5sxXjhMx3oKuo2PMma/ceHbYYYfVq1e/7W1vGzT+1eb455uDrqFjzJmvHCdivAVdR8eYM1+58ey5556rVq3aaaedBjHegg6jY8yZrxwnYrwFXUfHmDNfuZHcdtttf/jDH9KDf/3Xf33ggQc41XbbbbdJuSDY3OgYc+Yrx4kYb0HX0THmzFduPHvttdcLL7ywyy67pMc//OEPb7755ssvv/zBBx/Mc0GwWdEx5sxXjhMx3oKuo2PMma8Mgp6iY8yZrxwnqoy3devWnXrqqWeeeSaeLliwYObMmYsXL56c2kCMt6CAjjFnvjIIeoqOMWe+cpyoMt7w/1NOXHLJJStWrLj77rvT43nz5k0KNYjxFhTQMebMVwZBT9Ex5sxXjhNVxtvLL788Y4L0OM225cuXpweLFi3CAyXGW1BAx5gzXxkEPUXHmDNfOU5UGW8YbIkjjjhiyZIljz766GDityhXr149KbeeGG9BAR1jznzlcMy4/G+HN18cBJsDHWPOfOU4UXe84R80uvLKK9OPc+bMaWaaxHgLCugYc+Yrh0NnWMF8cRBsDnSMOfOV40SV8fbSSy8df/zxp5xyCv7HyvPnz4+/WtIFVqxYcfbZZ6cHzz33XP5ah9Ex5sxXDofOsIL54iDYHOgYc+Yrx4kq421jifHWDiP6r2/oGHPmK4dDZ1jBfHEQbA50jDnzleNEjLdx4aGHHvr+97+fHqxZs+bhhx++4YYbLrnkkjzUSXSMOfOVw6EzrGC+OAg2BzrGnPnKcSLG27hwwAEHZB8ZlW/mdIw585XDoTOsYL44CDYHOsac+cpxIsbbuMBhtnTpUjzYfffdN7zcYXSMOfOVw6EzrGC+OAg2BzrGnPnKcSLG27iwzz778PGee+75gQ98oPFip9Ex5sxXDofOsIL54iDYHOgYc+Yrx4kYb0HX0THmzFcOh86wgvniINgc6Bhz5ivHiRhvQdfRMebMVw6HzrCC+eKgY+D/XnTKKaf89re/veWWW6666qo80Qt0jDnzleNEjLeg6+gYc+Yrh0NnWMF8cdAl7rvvvhtuuKH5kVH5+1Mbi44xZ75ynIjxFnQdHWPOfOVw6AwrmC8OukQ2zO666y78xzD9Q8eYM185TsR46zN6rzvzlV1Cx5gzXzkcOsMK5ouDLnH66afz8fLly08++eTGi71Cv4Sd+cpxIsZbn9F73Zmv7BI6xpz5yuHQGVYwXxx0hvnz5z/yyCN4/OSTT/L/N9lL9EvYma8cJ2K8jSr8BySnT5/+7LPP7rDDDnnir/4aGGaLFtAx5sxXDofOsIL54q7SkWvXJueffz4fv6VBI9If9EvYma8cJ2K8jSr4un3qqaduv/329OCyyy7LE3/118AwW7SAjjFnvnI4dIYVzBd3lY5cu6AS+iXszFeOEzHeRhX8mXl683r88ccHE78z88QTT2QZvded2cJB49+oLG/RAjrGnPnK4dAZVjBf3Em6c+2CSuiXsDNfOU7EeBtJ8J41mPjz8zvuuGNgfnmu97ozX9n4S2jlLVpAx5gzXzkcOsMK5os7SXeuXVAJ/RJ25ivHiRhvI8mll17KxzvssMOzzz47ffr0xuv/hd7rznzlxKdtPnZbtICOMWe+cjh0hhXMF3eS7ly72uid7MxXDgbTpk1bvXo1fmauvvrq9J3ulVdeec899+S5TqIFnfnKcSLGW5/Re92Zr+wSOsac+crh0BlWMF8cbFb0TnZmC9P3tffeey+f8p9gPe200/jBLqMFnfnKcSLGW5/Re92Zr+wSOsac+crh0BlWMF8cbFb0TnZmC2+88cYDDjhg5cqV+O7tpZdeGq2/ZqkFnfnKcSLGW5/Re92Zr+wSOsac+crh0BlWMF8cbFb0TnZmC+fPn3/nnXemB7feeuuTTz7Jwbb99ttPynUVLejMV44TMd76jN7rznxll9Ax5sxXDofOsIL54mCzoneyM1u4du3az3zmM+kBfuR422677ZqxzqIFnfnKcSLG2yihb+hO5PVedyKv7+ZOHqkFtJ0zXzkc2q5gvrgz6DV15itHGW3nzFcOBjfddFP6Xu2aa65Jj1988cX3ve99++6777p16/JcJ9GCznzlOBHjbZTQN3Qn8nqvO5HXd3Mnj9QC2s6ZrxwObVcwX9wZ9Jo685WjjLZz5itHHC3ozFeOEzHeRgl9Q3cir/e6E3l9N3fySC2g7Zz5ysFg5syZe++9N35Jjr87cMIJJ2QZbVcwW9sd9Jo685VdZZhrp+2c2cJRRws685XjRIy3UULf0J3I673uRF7fzZ08UgtoO2e2cNasWXhw8MEHpx/f9773NV8l2q5gvrgz6DV15is7yZDXTts585UjjhZ05ivHiRhvo4S+oTuR13vdiby+mzt5pBbQds5sYfr1/kknncR3xsMOO2z69Olr166dFNqY1i0X3yj0mjrzlZ1Er90ee+yh107bObOFo44WdOYrx4kYb6OEvqE7kdd73Ym8vps7eaQW0HbObCH/Oty73/1uflD/apy2K5it7Q56TZ35yk4y5LXTdk4u0Wvq3LBN99CCznzlOBHjbZTQN3Qn8nqvO5HXr3Anj9QC2s6ZLeRbJB9kj4G2K5it7Q56TZ35yk4y5LXTdk4u0Wvq3LBN99CCznzlOBHjbZTQN3Qn8nqvO5HXr3Anj9QC2s6ZLbxugh/84AfXXntterrffvutXLnyhhtuyGLarmC2tjvoNXXmKzuJXrurr75ar522c3KJXlPnhm26hxZ05ivHiRhvo4S+oTuR13vdibx+hTt5pBbQds585XBou4L54s6g19SZrxxltJ2TS/SaOjds0z20oDNfOU7EeBsl9A3dibze607k9SvcySO1gLZz5iuHQ9sVzBd3Br2mznzlKKPtnFyi19S5YZsWaf7nEJdccon7Xz1oQWe+cpyI8TZK6Bu6E3m9153I61e4k0dqAW3nzFcOh7YrmC/uDHpNnfnKUUbbOblEr6lzwzZt0fzPIf74xz/i/7S+5557TgpNoAWd+cpxIsbbKKFv6E7k9V53Iq9f4U4eqQW0nTNfORzarmC+uDPoNXXmK0cZbefkEr2mzg3btEX2n0OAfffdt/kUaEFnvnKciPE2SugbuhN5vdedyOtXuJNHagFt50Re2zmR13YFeaquoe2c+couodfUiby2c3ILvaZOLmkN/c8hHnvssSn/GUwt6MxXjhMx3kYJ/SJ3Iq/3uhN5/Qp38kgtoO2cyGs7J/LariBP1TW0nTNf2SX0mjqR13ZObqHX1MklrZH95xDLly//2Mc+NimxHi3ozFeOE2M33pr/F4yLLroo/Th79uws01n0i9yJvN7rTuT1K9zJI7WAtnMir+2cyGu7gjxV19B2znxll9Br6kRe2zm5hV5TJ5e0ycEHH7zffvulB/PmzXvl39mcIA+9puIg+9fORu49cKMYr/H2s5/97De/+c306dO//e1vp6cPPPBA+vHaa6/9y1/+kkc7iX6RO5HXe92JvH6FO3mkFtB2TuS1nRN5bVeQp+oa2s6Zr+wSek2dyGs7J7fQa+rkkg6iBZ3ZwuYf7/3bv/3byL0HbhTjNd7SVbz00kvTg89//vPpx8cffzz9eMstt/zxj3/Mkt1Ev8idyOu97kRev8KdPFILaDsn8trOiby2K8hTdQ1t58xXdgm9pk7ktZ2TW+g1dXJJB9GCzmxh84/3fvzjH4/ce+BGMV7jbenSpQsXLkwPbr755ieffPKOO+5Ijy+77LI811X0i9yJvN7rTuT1K9zJI7WAtnMir+2cyGu7gjxV19B2znxll9Br6kRe2zm5hV5TJ5d0EC3ozBY2/3hv+fLlI/ceuFGM13gbTPyrrM8///z222+fHu+www7PPvus+w8nO4h+kTuR13vdibx+hTt5pBbQdk7ktZ0TeW1XkKfqGtrOma/sEnpNnchrOye30Gvq5JIOogWd2cLsXzsbuffAjWLsxttIo1/kTuT1Xncir1/hTh6pBbSdE3lt50Re2xXkqbqGtnPmK7uEXlMn8trOyS30mjq5pDbazsklWtDZ2GfsqDXezj777JNOOgn/xcaCBQtmzpy5ePHiPLSeGG9Dore7E3m9153I61e4k0dqAW3nRF7bOZHXdgV5qq6h7Zz5yi6h19SJvLZzcgu9pk4uqY22c3KJFnQ29hk7qoy3c845Bw9OO+209OO3vvWt9OOcOXOamSYx3oZEb3cn8nqvO5HXr3Anj9QC2s6JvLZzIq/tCvJUXUPbOfOVXUKvqRN5befkFnpNnVxSG23n5BIt6GzsM3ZUGW8zZsyYO3fu8ccfnx4vWbLkkUceGUx8D7dq1ao8OkGMtyHR292JvN7rTuT1K9zJI7WAtnMir+2cyGu7gjxV19B2znxll9Br6kRe2zm5hV5TJ5fURts5uUQLOhv7jB21xhseHHPMMXfdddfy5cvT40WLFj311FOTcutJ4+0/HnmyqnrVnbq2O+rt7kRe2zmR169wp56tntrOiby2cyKv7Qrq8TqitnPq2u6o19SJvLZzcgu9pk49XiW1nZNLtKATeW3n1OMNb/7OvrmpO97Sg2eeeebee+8dTPxH+JNCDVr47k2vujNf2SX0dncir+2cyOu97uSRWkDbOZHXdk7ktV1BnqpraDtnvrJL6DV1Iq/tnNxCr6mTS2qj7ZxcogWdyGs7J7foAVXG2+0T3HHHHQsWLBhM/B+MVq5cyX8MRunyePvLX/6CfxfnhBNOGEz8xyLun8lpAb3dnchrOyfyeq87eaQW0HZO5LWdE3ltV5Cnao3mHZjdjU20nTNb2Cn0mjqR13ZObqHX1MkltdF2Ti7Rgk7ktZ2TW/SAKuNtY+nyePvOd77TfJr9vypaRm93J/Lazom83utOHqkFtJ0TeW3nRF7bFeSpWqN5B2Z3YxNt58xXdgm9pk7ktZ2TW+g1dXJJbbSdk0u0oBN5befkFj0gxltutvCwww474ogj9thjj7Vr1+Lp9OnTv/a1r2WxdtDb3Ym8tnMir/e6k0dqAW3nRF7bOZHXdgV5qtZo3oHZ3dhE2zmzhZ1Cr6kTeW3n5BZ6TZ1cUhtt5+QSLehEXts5uUUPiPGWm69cz3bbbcfHX/rSl5599tnGiy2ht7sTeW3nRF7vdSeP1ALazom8tnMir+0K8lTt07wDm4+BtnNmCzuFXlMn8trOyS30mjq5pDbazsklWtCJvLZzcoseEOMtN1+5nuaft/3oRz9atmxZ48WW0Nvdiby2cyKv97qTR2oBbedEXts5kdd2BXmq9mnegfqnv9rOmS3sFHpNnchrOye30Gvq5JLaaDsnl2hBJ/LazsktekCMt9xs4bHHHrtkyZKrr776hhtuSE/322+/lStXbrvttlmsHfR2dyKv7ZzI673u5JFaQNs5kdd2TuS1XUGeqjWad2B2NzbRds5sYafQa+pEXts5uYVeUyeX1EbbOblECzqR13ZObtEDYrzl5iu7hN7uTuS1nRN5vdedPFILaDsn8trOiby2K8hTdQ1t58xXdgm9pk7ktZ2TW+g1dXJJbbSdk0u0oBN5befkFj0gxltuvrJL6O3uRF7bOZHXe93JI7WAtnMir+2cyGu7gjxV19B2znxll9Br6kRe2zm5hV5TJ5fURts5uUQLOpHXdk5u0QNivOXmK7uE3u5O5LWdE3m91508UgtoOyfy2s6JvLYryFN1DW3nzFd2Cb2mTuS1nZNb6DV1cklttJ2TS7SgE3lt5+QWPSDGW26+skvo7e5EXts5kdd73ckjtYC2cyKv7ZzIa7uCPFXX0HbOfGWX0GvqRF7bObmFXlMnl9RG2zm5RAs6kdd2Tm7RA2K85SKvV905aZvK6O3uRF7bOZHXdk4eqQW0nRN5bedEXtsV5Klqo+2cyGs75+R9uoW2cyKv7ZzcQq+pk0tqo+2cXKIFnchrOye36AEx3nKR16vunLRNZfR2dyKv7ZzIazsnj9QC2s6JvLZzIq/tCvJUtdF2TuS1nXPyPt1C2zmR13ZObqHX1MkltdF2Ti7Rgk7ktZ2TW/SAGG+5yOtVd07apjJ6uzuR13ZO5LWdk0dqAW3nRF7bOZHXdgV5qtpoOyfy2s45eZ9XyP6bzsRll132wAMPNCItoe2cyGs7J7fQa+rkktpoOyeXaEEn8trOyS16QIy3XOT1qjsnbVMZvd2dyGs7J/LazskjtYC2cyKv7ZzIa7uCPFVttJ0TeW3nnLzPK5x44ol8zFG366678oOtoe2cyGs7J7fQa+rkktpoOyeXaEEn8trOyS16QIy3XOT1qjsnbVMZvd2dyGs7J/LazskjtYC2cyKv7ZzIa7uCPFVttJ0TeW3nnLzPYM2aNbNnz161atX06dMHjfGm/zBKC2g7J/Lazskt9Jo6uaQ22s7JJVrQiby2c3KLHhDjLRd5verOSdtURm93J/Lazom8tnPySC2g7ZzIazsn8tquIE9VG23nRF7bOSfvs4GFCxf+8pe/jPHW/Ws92Pji2s7JLXpAjLdc5PWqOydtUxm93Z3Iazsn8trOySO1gLZzIq/tnMhru4I8VW20nRN5beecvM9g6dKlt99+e3pwwQUXvPzyywcffDA+fu65507KtYK2cyKv7ZzcQq+pk0tqo+2cXKIFnchrOye36AEx3nKR16vunLRNZfR2dyKv7ZzIazsnj9QC2s6JvLZzIq/tCvJUtdF2TuS1nXPyPq9w0UUXTZs27cYbb8TT97///YcffvjkSEtoOyfy2s7JLfSaOrmkNtrOySVa0Im8tnNyix4Q4y0Xeb3qzknbVEZvdyfy2s6JvLZz8kgtoO2cyGs7J/LariBPVRtt50Re2zkn79MttJ0TeW3n5BZ6TZ1cUhtt5+QSLehEXts5uUUPiPGWi7xedeekbSqjt7sTeW3nRF7bOXmkFtB2TuS1nRN5bVeQp6qNtnMir+2ck/fpFtrOiby2c3ILvaZOLqmNtnNyiRZ0Iq/tnNyiB8R4y0Ver7pz0jaV0dvdiby2cyKv7Zw8UgtoOyfy2s6JvLYryFPVRts5kdd2zsn7dAtt50Re2zm5hV5TJ5fURts5uUQLOpHXdk5u0QNivOUir1fdOWmbyujt7kRe2zmR13ZOHqkFtJ0TeW3nRF7bFeSpaqPtnMhrO+fkfbqFtnMir+2c3EKvqZNLaqPtnFyiBZ3Iazsnt+gBMd5ykder7py0TWX0dncir+2cyGs7J4/UAtrOiby2cyKv7QryVLXRdk7ktZ0Tea1WkKeqjbZzIq/tnNxC2zm5pDbazsklWtCJvLZzcoseEOMtF3m96s5J21RGb3cn8trOiby2c/JILaDtnMhrOyfy2q4gT1UbbedEXts5kddqBXmq2mg7J/LazskttJ2TS2qj7ZxcogWdyGs7J7foAX0Yb8P8h6h61Z3I61V3TtqmMnq7O5HXdk7ktZ2TR2oBbedEXts5kdd2BXmq2mg7J/Lazom8VivIU9VG2zmR13ZObqHtnFxSG23n5BIt6ERe2zm5RQ8Y+fF28AR43Pyn8zL0qjuR16vunLRNZfR2dyKv7ZzIazsnj9QC2s6JvLZzIq/tCvJUtdF2TuS1nRN5rVaQp6qNtnMir+2c3ELbObmkNtrOySVa0Im8tnNyix4w2uNt6dKl99xzD8Zb9k/nZehVdyKvV905aZvK6O3uRF7bOZHXdk4eqQW0nRN5bedEXtsV5Klqo+2cyGs7J/JarSBPVRtt50Re2zm5hbZzcklttJ2TS7SgE3lt5+QWPWC0x9vee+89mPgGrvlB/NN5zY8M+nI36O3uRF7bOZHXdk4eqQW0nRN5bedEXtsV5Klqo+2cyGs7J/JarSBPVRtt50Re2zm5hbZzcklttJ2TS7SgE3lt5+QWPWC0xxvgeNtvv/1Wrly57bbbTn79FfSqO5HXq+6ctE1l9HZ3Iq/tnMhrOyeP1ALazom8tnMir+0K8lS10XZO5LWdE3mtVpCnqo22cyKv7ZzcQts5uaQ22s7JJVrQiby2c3KLHtCH8TYMetWdyOtVd07apjJ6uzuR13ZO5LWdk0dqAW3nRF7bOZHXdgV5qtpoOyfy2s6JvFYryFPVRts5kdd2Tm6h7ZxcUhtt5+QSLehEXts5uUUPiPGWi7xedeekbSqjt7sTeW3nRF7bOXmkFtB2TuS1nRN5bVeQp6qNtnMir+2cyGu1gjxVbbSdE3lt5+QW2s7JJbXRdk4u0YJO5LWdk1v0gBhvucjrVXdO2qYyers7kdd2TuS1nZNHagFt50Re2zmR13YFearaaDsn8trOibxWK8hT1UbbOZHXdk5uoe2cXFIbbefkEi3oRF7bOblFD4jxlou8XnXnpG0qo7e7E3lt50Re2zl5pBbQdk7ktZ0TeW1XkKeqjbZzIq/tnMhrtYI8VW20nRN5befkFtrOySW10XZOLtGCTuS1nZNb9ICRHG961Z1colfdibxedSe3aAEt6ERe2zmR13ZOHqkFtJ0TeW3nRF7bFeSpaqPtnMhrOyfyWq0gT1UbbedEXts5uYW2c3JJbbSdk0u0oBN5befkFj0gxlsu8nrVndyiBbSgE3lt50Re2zl5pBbQdk7ktZ0TeW1XkKeqjbZzIq/tnMhrtYI8VW20nRN5befkFtrOySW10XZOLtGCTuS1nZNb9IAYb7nI61V3cosW0IJO5LWdE3lt5+SRWkDbOZHXdk7ktV1Bnqo22s6JvLZzIq/VCvJUtdF2TuS1nZNbaDsnl9RG2zm5RAs6kdd2Tm7RA2K85SKvV93JLVpACzqR13ZO5LWdk0dqAW3nRF7bOZHXdgV5qtpoOyfy2s6JvFYryFPVRts5kdd2Tm6h7ZxcUhtt5+QSLehEXts5uUUPiPGWi7xedSe3aAEt6ERe2zmR13ZOHqkFtJ0TeW3nRF7bFeSpaqPtnMhrOyfyWq0gT1UbbedEXts5uYW2c3JJbbSdk0u0oBN5befkFj0gxlsu8nrVndyiBbSgE3lt50Re2zl5pBbQdk7ktZ0TeW1XkKeqjbZzIq/tnMhrtYI8VW20nRN5befkFtrOySW10XZOLtGCTuS1nZNb9IAYb7nI61V3cosW0IJO5LWdE3lt5+SRWkDbOZHXdk7ktV1Bnqo22s6JvLZzIq/VCvJUtdF2TuS1nZNbaDsnl9RG2zm5RAs6kdd2Tm7RA2K85SKvV93JLVpACzqR13ZO5LWdk0dqAW3nRF7bOZHXdgV5qtpoOyfy2s6JvFYryFPVRts5kdd2Tm6h7ZxcUhtt5+QSLehEXts5uUUPiPGWi7xedSe3aAEt6ERe2zmR13ZOHqkFtJ0TeW3nRF7bFeSpaqPtnMhrOyfyWq0gT1UbbedEXts5uYW2c3JJbbSdk0u0oBN5befkFj2g4nibMWMGHsyaNWvlypUzZ86c/PoGYrwNiRZ0Iq/tnMhrOyeP1ALazom8tnMir+0K8lS10XZO5LWdE3mtVpCnqo22cyKv7ZzcQts5uaQ22s7JJVrQiby2c3KLHlBrvJ02QXqwYsWKu+++Oz2YN29eHlpPjLch0YJO5LWdE3lt5+SRWkDbOZHXdk7ktV1Bnqo22s6JvLZzIq/VCvJUtdF2TuS1nZNbaDsnl9RG2zm5RAs6kdd2Tm7RA6qMt4cffnjp0qUYb2m2LV++PD1YtGgRHigx3oZECzqR13ZO5LWdk0dqAW3nRF7bOZHXdgV5qtpoOyfy2s6JvFYryFPVRts5kdd2Tm6h7ZxcUhtt5+QSLehEXts5uUUPqDLeTjrppMHEN3DpxyVLljz66KPpwYIFC1avXp0lQYy3IdGCTuS1nRN5befkkVpA2zmR13ZO5LVdQZ6qNtrOiby2cyKv1QryVLXRdk7ktZ2TW2g7J5fURts5uUQLOpHXdk5u0QOqjDeA8Za48sor049z5syZ9HKDGG9DogWdyGs7J/LazskjtYC2cyKv7ZzIa7uCPFVttJ0TeW3nRF6rFeSpaqPtnMhrOye30HZOLqmNtnNyiRZ0Iq/tnNyiB1Qcb8MT421ItKATeW3nRF7bOXmkFtB2TuS1nRN5bVeQp6qNtnMir+2cyGu1gjxVbbSdE3lt5+QW2s7JJbXRdk4u0YJO5LWdk1v0gBhvucjrVXdyixbQgk7ktZ0TeW3n5JFaQNs5kdd2TuS1XUGeqjbazom8tnMir9UK8lS10XZO5LWdk1toOyeX1EbbOblECzqR13ZObtEDYrzlIq9X3cktWkALOpHXdk7ktZ2TR2oBbedEXts5kdd2BXmq2mg7J/Lazom8VivIU9VG2zmR13ZObqHtnFxSG23n5BIt6ERe2zm5RQ+I8ZaLvF51J7doAS3oRF7bOZHXdk4eqQW0nRN5bedEXtsV5Klqo+2cyGs7J/JarSBPVRtt50Re2zm5hbZzcklttJ2TS7SgE3lt5+QWPSDGWy7yetWd3KIFtKATeW3nRF7bOXmkFtB2TuS1nRN5bVeQp6qNtnMir+2cyGu1gjxVbbSdE3lt5+QW2s7JJbXRdk4u0YJO5LWdk1v0gBhvucjrVXdyixbQgk7ktZ0TeW3n5JFaQNs5kdd2TuS1XUGeqjbazom8tnMir9UK8lS10XZO5LWdk1toOyeX1EbbOblECzqR13ZObtEDYrzlIq9X3cktWkALOpHXdk7ktZ2TR2oBbedEXts5kdd2BXmq2mg7J/Lazom8VivIU9VG2zmR13ZObqHtnFxSG23n5BIt6ERe2zm5RQ+I8ZaLvF51J7doAS3oRF7bOZHXdk4eqQW0nRN5bedEXtsV5Klqo+2cyGs7J/JarSBPVRtt50Re2zm5hbZzcklttJ2TS7SgE3lt5+QWPSDGWy7yetWd3KIFtKATeW3nRF7bOXmkFtB2TuS1nRN5bVeQp6qNtnMir+2cyGu1gjxVbbSdE3lt5+QW2s7JJbXRdk4u0YJO5LWdk1v0gBhvucjrVXdyixbQgk7ktZ0TeW3n5JFaQNs5kdd2TuS1XUGeqjbazom8tnMir9UK8lS10XZO5LWdk1toOyeX1EbbOblECzqR13ZObtEDYrzlIq9X3cktWkALOpHXdk7ktZ2TR2oBbedEXts5kdd2BXmq2mg7J/Lazom8VivIU9VG2zmR13ZObqHtnFxSG23n5BIt6ERe2zm5RQ+I8ZaLvF51J7doAS3oRF7bOZHXdk4eqQW0nRN5bedEXtsV5Klqo+2cyGs7J/JarSBPVRtt50Re2zm5hbZzcklttJ2TS7SgE3lt5+QWPSDGWy7yetWd3KIFtKATeW3nRF7bOXmkFtB2TuS1nRN5bVeQp6qNtnMir+2cyGu1gjxVbbSdE3lt5+QW2s7JJbXRdk4u0YJO5LWdk1v0gBhvucjrVXdyixbQgk7ktZ0TeW3n5JFaQNs5kdd2TuS1XUGeqjbazom8tnMir9UK8lS10XZO5LWdk1toOyeX1EbbOblECzqR13ZObtEDYrzlIq9X3cktWkALOpHXdk7ktZ2TR2oBbedEXts5kdd2BXmq2mg7J/Lazom8VivIU9VG2zmR13ZObqHtnFxSG23n5BIt6ERe2zm5RQ+I8ZaLvF51J7doAS3oRF7bOZHXdk4eqQW0nRN5bedEXtsV5Klqo+2cyGs7J/JarSBPVRtt50Re2zm5hbZzcklttJ2TS7SgE3lt5+QWPSDGWy7yetWd3KIFtKATeW3nRF7bOXmkFtB2TuS1nRN5bVeQp6qNtnMir+2cyGu1gjxVbbSdE3lt5+QW2s7JJbXRdk4u0YJO5LWdk1v0gBhvucjrVXdyixbQgk7ktZ0TeW3n5JFaQNs5kdd2TuS1XUGeqjbazom8tnMir9UK8lS10XZO5LWdk1toOyeX1EbbOblECzqR13ZObtEDYrzlIq9X3cktWkALOpHXdk7ktZ2TR2oBbedEXts5kdd2BXmq2mg7J/Lazom8VivIU9VG2zmR13ZObqHtnFxSG23n5BIt6ERe2zm5RQ+I8ZaLvF51J7doAS3oRF7bOZHXdk4eqQW0nRN5bedEXtsV5Klqo+2cyGs7J/JarSBPVRtt50Re2zm5hbZzcklttJ2TS7SgE3lt5+QWPSDGWy7yetWd3KIFtKATeW3nRF7bOXmkFtB2TuS1nRN5bVeQp6qNtnMir+2cyGu1gjxVbbSdE3lt5+QW2s7JJbXRdk4u0YJO5LWdk1v0gBhvucjrVXdyixbQgk7ktZ0TeW3n5JFaQNs5kdd2TuS1XUGeqjbazom8tnMir9UK8lS10XZO5LWdk1toOyeX1EbbOblECzqR13ZObtEDYrzlIq9X3cktWkALOpHXdk7ktZ2TR2oBbedEXts5kdd2BXmq2mg7J/Lazom8VivIU9VG2zmR13ZObqHtnFxSG23n5BIt6ERe2zm5RQ+I8ZaLvF51J7doAS3oRF7bOZHXdk4eqQW0nRN5bedEXtsV5Klqo+2cyGs7J/JarSBPVRtt50Re2zm5hbZzcklttJ2TS7SgE3lt5+QWPSDGWy7yetWd3KIFtKATeW3nRF7bOXmkFtB2TuS1nRN5bVeQp6qNtnMir+2cyGu1gjxVbbSdE3lt5+QW2s7JJbXRdk4u0YJO5LWdk1v0gBhvucjrVXdyixbQgk7ktZ0TeW3n5JFaQNs5kdd2TuS1XUGeqjbazom8tnMir9UK8lS10XZO5LWdk1toOyeX1EbbOblECzqR13ZObtEDYrzlIq9X3cktWkALOpHXdk7ktZ2TR2oBbedEXts5kdd2BXmq2mg7J/Lazom8VivIU9VG2zmR13ZObqHtnFxSG23n5BIt6ERe2zm5RQ+I8ZaLvF51J7doAS3oRF7bOZHXdk4eqQW0nRN5bedEXtsV5Klqo+2cyGs7J/JarSBPVRtt50Re2zm5hbZzcklttJ2TS7SgE3lt5+QWPSDGWy7yetWd3KIFtKATeW3nRF7bOXmkFtB2TuS1nRN5bVeQp6qNtnMir+2cyGu1gjxVbbSdE3lt5+QW2s7JJbXRdk4u0YJO5LWdk1v0gBhvucjrVXdyixbQgk7ktZ0TeW3n5JFaQNs5kdd2TuS1XUGeqjbazom8tnMir9UK8lS10XZO5LWdk1toOyeX1EbbOblECzqR13ZObtEDYrzlIq9X3cktWkALOpHXdk7ktZ2TR2oBbedEXts5kdd2BXmq2mg7J/Lazom8VivIU9VG2zmR13ZObqHtnFxSG23n5BIt6ERe2zm5RQ+I8ZaLvF51J7doAS3oRF7bOZHXdk4eqQW0nRN5bedEXtsV5Klqo+2cyGs7J/JarSBPVRtt50Re2zm5hbZzcklttJ2TS7SgE3lt5+QWPSDGWy7yetWd3KIFtKATeW3nRF7bOXmkFtB2TuS1nRN5bVeQp6qNtnMir+2cyGu1gjxVbbSdE3lt5+QW2s7JJbXRdk4u0YJO5LWdk1v0gBhvucjrVXdyixbQgk7ktZ0TeW3n5JFaQNs5kdd2TuS1XUGeqjbazom8tnMir9UK8lS10XZO5LWdk1toOyeX1EbbOblECzqR13ZObtEDYrzlIq9X3cktWkALOpHXdk7ktZ2TR2oBbedEXts5kdd2BXmq2mg7J/Lazom8VivIU9VG2zmR13ZObqHtnFxSG23n5BIt6ERe2zm5RQ+I8ZaLvF51J7doAS3oRF7bOZHXdk4eqQW0nRN5bedEXtsV5Klqo+2cyGs7J/JarSBPVRtt50Re2zm5hbZzcklttJ2TS7SgE3lt5+QWPSDGWy7yetWd3KIFtKATeW3nRF7bOXmkFtB2TuS1nRN5bVeQp6qNtnMir+2cyGu1gjxVbbSdE3lt5+QW2s7JJbXRdk4u0YJO5LWdk1v0gBhvucjrVXdyixbQgk7ktZ0TeW3n5JFaQNs5kdd2TuS1XUGeqjbazom8tnMir9UK8lS10XZO5LWdk1toOyeX1EbbOblECzqR13ZObtEDYrzlIq9X3cktWkALOpHXdk7ktZ2TR2oBbedEXts5kdd2BXmq2mg7J/Lazom8VivIU9VG2zmR13ZObqHtnFxSG23n5BIt6ERe2zm5RQ+I8ZaLvF51J7doAS3oRF7bOZHXdk4eqQW0nRN5bedEXtsV5Klqo+2cyGs7J/JarSBPVRtt50Re2zm5hbZzcklttJ2TS7SgE3lt5+QWPSDGWy7yetWd3KIFtKATeW3nRF7bOXmkFtB2TuS1nRN5bVeQp6qNtnMir+2cyGu1gjxVbbSdE3lt5+QW2s7JJbXRdk4u0YJO5LWdk1v0gCrj7cILL1y2bNmiRYtuvvnm9HTWrFkrV66cOXNmnltPjLch0YJO5LWdE3lt5+SRWkDbOZHXdk7ktV1Bnqo22s6JvLZzIq/VCvJUtdF2TuS1nZNbaDsnl9RG2zm5RAs6kdd2Tm7RA6qMNzJjxowVK1bcfffd6fG8efPyl9cT421ItKATeW3nRF7bOXmkFtB2TuS1nRN5bVeQp6qNtnMir+2cyGu1gjxVbbSdE3lt5+QW2s7JJbXRdk4u0YJO5LWdk1v0gIrj7Te/+c38+fPTbFu+fHl6mr6ZwwMlxtuQaEEn8trOiby2c/JILaDtnMhrOyfy2q4gT1UbbedEXts5kddqBXmq2mg7J/LazskttJ2TS2qj7ZxcogWdyGs7J7foAbXG2zPPPDN37tz0YMmSJY8++mh6sGDBgtWrV+e5CWK8DYkWdCKv7ZzIazsnj9QC2s6JvLZzIq/tCvJUtdF2TuS1nRN5rVaQp6qNtnMir+2c3ELbObmkNtrOySVa0Im8tnNyix5QZbw99dRTX/ziF/n0yiuvTD/OmTNnQ2IyMd6GRAs6kdd2TuS1nZNHagFt50Re2zmR13YFearaaDsn8trOibxWK8hT1UbbOZHXdk5uoe2cXFIbbefkEi3oRF7bOblFD6gy3mY0SE/nz58/c+bMxYsX57n1xHgbEi3oRF7bOZHXdk4eqQW0nRN5bedEXtsV5Klqo+2cyGs7J/JarSBPVRtt50Re2zm5hbZzcklttJ2TS7SgE3lt5+QWPaDKeNtYYrwNiRZ0Iq/tnMhrOyeP1ALazom8tnMir+0K8lS10XZO5LWdE3mtVpCnqo22cyKv7ZzcQts5uaQ22s7JJVrQiby2c3KLHhDjLRd5vepObtECWtCJvLZzIq/tnDxSC2g7J/Lazom8tivIU9VG2zmR13ZO5LVaQZ6qNtrOiby2c3ILbefkktpoOyeXaEEn8trOyS16QIy3XOT1qju5RQtoQSfy2s6JvLZz8kgtoO2cyGs7J/LariBPVRtt50Re2zmR12oFearaaDsn8trOyS20nZNLaqPtnFyiBZ3Iazsnt+gBMd5ykder7uQWLaAFnchrOyfy2s7JI7WAtnMir+2cyGu7gjxVbbSdE3lt50ReqxXkqWqj7ZzIazsnt9B2Ti6pjbZzcokWdCKv7ZzcogfEeMtFXq+6k1u0gBZ0Iq/tnMhrOyeP1ALazom8tnMir+0K8lS10XZO5LWdE3mtVpCnqo22cyKv7ZzcQts5uaQ22s7JJVrQiby2c3KLHhDjLRd5vepObtECWtCJvLZzIq/tnDxSC2g7J/Lazom8tivIU9VG2zmR13ZO5LVaQZ6qNtrOiby2c3ILbefkktpoOyeXaEEn8trOyS16QIy3XOT1qju5RQtoQSfy2s6JvLZz8kgtoO2cyGs7J/LariBPVRtt50Re2zmR12oFearaaDsn8trOyS20nZNLaqPtnFyiBZ3Iazsnt+gBMd5ykder7uQWLaAFnchrOyfy2s7JI7WAtnMir+2cyGu7gjxVbbSdE3lt50ReqxXkqWqj7ZzIazsnt9B2Ti6pjbZzcokWdCKv7ZzcogfEeMtFXq+6k1u0gBZ0Iq/tnMhrOyeP1ALazom8tnMir+0K8lS10XZO5LWdE3mtVpCnqo22cyKv7ZzcQts5uaQ22s7JJVrQiby2c3KLHhDjLRd5vepObtECWtCJvLZzIq/tnDxSC2g7J/Lazom8tivIU9VG2zmR13ZO5LVaQZ6qNtrOiby2c3ILbefkktpoOyeXaEEn8trOyS16QIy3XOT1qju5RQtoQSfy2s6JvLZz8kgtoO2cyGs7J/LariBPVRtt50Re2zmR12oFearaaDsn8trOyS20nZNLaqPtnFyiBZ3Iazsnt+gBMd5ykder7uQWLaAFnchrOyfy2s7JI7WAtnMir+2cyGu7gjxVbbSdE3lt50ReqxXkqWqj7ZzIazsnt9B2Ti6pjbZzcokWdCKv7ZzcogfEeMtFXq+6k1u0gBZ0Iq/tnMhrOyeP1ALazom8tnMir+0K8lS10XZO5LWdE3mtVpCnqo22cyKv7ZzcQts5uaQ22s7JJVrQiby2c3KLHhDjLRd5vepObtECWtCJvLZzIq/tnDxSC2g7J/Lazom8tivIU9VG2zmR13ZO5LVaQZ6qNtrOiby2c3ILbefkktpoOyeXaEEn8trOyS16QIy3XOT1qju5RQtoQSfy2s6JvLZz8kgtoO2cyGs7J/LariBPVRtt50Re2zmR12oFearaaDsn8trOyS20nZNLaqPtnFyiBZ3Iazsnt+gBMd5ykder7uQWLaAFnchrOyfy2s7JI7WAtnMir+2cyGu7gjxVbbSdE3lt50ReqxXkqWqj7ZzIazsnt9B2Ti6pjbZzcokWdCKv7ZzcogfEeMtFXq+6k1u0gBZ0Iq/tnMhrOyeP1ALazom8tnMir+0K8lS10XZO5LWdE3mtVpCnqo22cyKv7ZzcQts5uaQ22s7JJVrQiby2c3KLHhDjLRd5vepObtECWtCJvLZzIq/tnDxSC2g7J/Lazom8tivIU9VG2zmR13ZO5LVaQZ6qNtrOiby2c3ILbefkktpoOyeXaEEn8trOyS16QIy3XOT1qju5RQtoQSfy2s6JvLZz8kgtoO2cyGs7J/LariBPVRtt50Re2zmR12oFearaaDsn8trOyS20nZNLaqPtnFyiBZ3Iazsnt+gBMd5ykder7uQWLaAFnchrOyfy2s7JI7WAtnMir+2cyGu7gjxVbbSdE3lt50ReqxXkqWqj7ZzIazsnt9B2Ti6pjbZzcokWdCKv7ZzcogfEeMtFXq+6k1u0gBZ0Iq/tnMhrOyeP1ALazom8tnMir+0K8lS10XZO5LWdE3mtVpCnqo22cyKv7ZzcQts5uaQ22s7JJVrQiby2c3KLHhDjLRd5vepObtECWtCJvLZzIq/tnDxSC2g7J/Lazom8tivIU9VG2zmR13ZO5LVaQZ6qNtrOiby2c3ILbefkktpoOyeXaEEn8trOyS16QIy3XOT1qju5RQtoQSfy2s6JvLZz8kgtoO2cyGs7J/LariBPVRtt50Re2zmR12oFearaaDsn8trOyS20nZNLaqPtnFyiBZ3Iazsnt+gBMd5ykder7uQWLaAFnchrOyfy2s7JI7WAtnMir+2cyGu7gjxVbbSdE3lt50ReqxXkqWqj7ZzIazsnt9B2Ti6pjbZzcokWdCKv7ZzcogfEeMtFXq+6k1u0gBZ0Iq/tnMhrOyeP1ALazom8tnMir+0K8lS10XZO5LWdE3mtVpCnqo22cyKv7ZzcQts5uaQ22s7JJVrQiby2c3KLHhDjLRd5vepObtECWtCJvLZzIq/tnDxSC2g7J/Lazom8tivIU9VG2zmR13ZO5LVaQZ6qNtrOiby2c3ILbefkktpoOyeXaEEn8trOyS16QIy3XOT1qju5RQtoQSfy2s6JvLZz8kgtoO2cyGs7J/LariBPVRtt50Re2zmR12oFearaaDsn8trOyS20nZNLaqPtnFyiBZ3Iazsnt+gBMd5ykder7uQWLaAFnchrOyfy2s7JI7WAtnMir+2cyGu7gjxVbbSdE3lt50ReqxXkqWqj7ZzIazsnt9B2Ti6pjbZzcokWdCKv7ZzcogfEeMtFXq+6k1u0gBZ0Iq/tnMhrOyeP1ALazom8tnMir+0K8lS10XZO5LWdE3mtVpCnqo22cyKv7ZzcQts5uaQ22s7JJVrQiby2c3KLHhDjLRd5vepObtECWtCJvLZzIq/tnDxSC2g7J/Lazom8tivIU9VG2zmR13ZO5LVaQZ6qNtrOiby2c3ILbefkktpoOyeXaEEn8trOyS16QIy3XOT1qju5RQtoQSfy2s6JvLZz8kgtoO2cyGs7J/LariBPVRtt50Re2zmR12oFearaaDsn8trOyS20nZNLaqPtnFyiBZ3Iazsnt+gBMd5ykder7uQWLaAFnchrOyfy2s7JI7WAtnMir+2cyGu7gjxVbbSdE3lt50ReqxXkqWqj7ZzIazsnt9B2Ti6pjbZzcokWdCKv7ZzcogfEeMtFXq+6k1u0gBZ0Iq/tnMhrOyeP1ALazom8tnMir+0K8lS10XZO5LWdE3mtVpCnqo22cyKv7ZzcQts5uaQ22s7JJVrQiby2c3KLHhDjLRd5vepObtECWtCJvLZzIq/tnDxSC2g7J/Lazom8tivIU9VG2zmR13ZO5LVaQZ6qNtrOiby2c3ILbefkktpoOyeXaEEn8trOyS16QIy3XOT1qju5RQtoQSfy2s6JvLZz8kgtoO2cyGs7J/LariBPVRtt50Re2zmR12oFearaaDsn8trOyS20nZNLaqPtnFyiBZ3Iazsnt+gBMd5ykder7uQWLaAFnchrOyfy2s7JI7WAtnMir+2cyGu7gjxVbbSdE3lt50ReqxXkqWqj7ZzIazsnt9B2Ti6pjbZzcokWdCKv7ZzcogfEeMtFXq+6k1u0gBZ0Iq/tnMhrOyeP1ALazom8tnMir+0K8lS10XZO5LWdE3mtVpCnqo22cyKv7ZzcQts5uaQ22s7JJVrQiby2c3KLHhDjLRd5vepObtECWtCJvLZzIq/tnDxSC2g7J/Lazom8tivIU9VG2zmR13ZO5LVaQZ6qNtrOiby2c3ILbefkktpoOyeXaEEn8trOyS16QIy3XOT1qju5RQtoQSfy2s6JvLZz8kgtoO2cyGs7J/LariBPVRtt50Re2zmR12oFearaaDsn8trOyS20nZNLaqPtnFyiBZ3Iazsnt+gBMd5ykder7uQWLaAFnchrOyfy2s7JI7WAtnMir+2cyGu7gjxVbbSdE3lt50ReqxXkqWqj7ZzIazsnt9B2Ti6pjbZzcokWdCKv7Zzcoge0Md4WLFgwc+bMxYsX5y+sJ8bbkGhBJ/Lazom8tnPySC2g7ZzIazsn8tquIE9VG23nRF7bOZHXagV5qtpoOyfy2s7JLbSdk0tqo+2cXKIFnchrOye36AFtjLdvfetb6cc5c+bkL6wnxtuQaEEn8trOiby2c/JILaDtnMhrOyfy2q4gT1UbbedEXts5kddqBXmq2mg7J/LazskttJ2TS2qj7ZxcogWdyGs7J7foAdXH25IlSx555JHBxPdwq1atyl+eIMbbkGhBJ/Lazom8tnPySC2g7ZzIazsn8tquIE9VG23nRF7bOZHXagV5qtpoOyfy2s7JLbSdk0tqo+2cXKIFnchrOye36AHVx9tdd921fPny9GDRokVPPfVU/vIE7w2CIAhGnPydfXNTfbw988wz9957b3owb968/LUgCIIgqEP18ZaYOXPmypUrZ82alb8QBEEQBHVoY7wFQRAEQcvEeAuCIAh6SIy3IAiCoIfEeAuCIAh6SIy3IAiCoIfEeAuCIAh6SIy3IAiCoIfEeAuCIAh6yAiMty233HLWrFmHH3741ltvjf82/Nprr33Xu941az3pIxdddFGKHXrooVtttdWMGTOwcNGiRQ899NDXv/713XbbLcUOOOCAlPnRj360sZ/hyiuvvOyyy/CRwcR58OB1r3vdySeffOaZZ/IjU36SqnDrxHPPPff+97+/8eKr01yuH5zy1a7xD//wD9tss82FF144ffr0c889N3/Zc8IJJ6Sfsfyj3Wb58uXbb7/9E088gafptmxeIzye8oZv8uUvf/mNb3zjxRdfvNdee/EfUko3+Qc/+MH/OcHBBx/8lre8ZfKijrJ27dphvgzTzwm+0tMXSJfv6uz6Hn300S+++OLkyCv37dNPP5190LHlxJvnfvvtlx6sWbMmf3kwuOmmm773ve/lH+0LozHessdpOKUvzg2JyZk0BfEgXdTBxJ2N/2UBeA2fYcrx9uCDD65evRofefLJJ6dNm8aXAD9JVZo7vobxNiVd/vrPSFch/TKFT9PP+QsvvNB4vcQojrd0Q7788su77rornqbbMs2w4447Dk853vSGJ4899ljzZ+yqq67C8ilv8u7zhje8YZgvw/Rzwo+cccYZnf0HArPru0nGGx7ccMMNaepPfvEV0jthjLfNCa7QunXrFi5c+M53vnMw1XB6/etff8UVVzQ/Mpi49Qfy1X7kkUf++te/3qjPMOVX/oEHHsiPkCk/SVWmHG977733zJkzTz311Pe85z2DxhdJCqSvjfTgrW9963nnncfl6cd06++4447XXXfdLbfckp6mX8Lz1fStQPps6bvn9Am5V0dIVyFNuOyD2nfKCumlnXfeOX3bl375v2zZsvSRXXbZ5aijjpo9e/bb3/52xjoFrxee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>