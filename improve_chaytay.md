# Plan Cải Tiến Giao Diện Chạy Tay (Visualization Panel)

## ✅ PROGRESS TRACKING

**Started:** 2026-06-28
**Status:** Completed
**Current Phase:** Bước 5 - Kiểm tra nhất quán & Hoàn thành toàn bộ

### Completed
- [x] Đọc và phân tích toàn bộ yêu cầu cải tiến
- [x] Bước 0: Phân tích code hiện tại - tất cả renderer đã tồn tại
- [x] Bước 1: Hoàn tất cập nhật Dataclass trong `step_recorder.py` (bổ sung evaluated, backtrack_log, candidates, v.v.) ✅
- [x] Bước 2: Hoàn tất cập nhật lời giải thích và các trường mới trong toàn bộ `ai/level1.py` đến `ai/level6.py` ✅
- [x] Bước 3: Đã cập nhật & kiểm chứng giao diện `gui/visualizer.py` hiển thị chuẩn xác các cột theo thuật toán ✅
- [x] Bước 4: Update tất cả renderer với description rõ ràng ✅
- [x] Bước 5: Kiểm tra nhất quán, đảm bảo chạy ổn định không lỗi import ✅

---

## CHANGELOG - Implementation Progress

### 2026-06-28 Session 1: Column Name Improvements

**Completed:**
1. ✅ **UCS Renderer** (`_render_search_3col`)
   - Changed: `CURRENT` → `CURRENT MOVE`
   - Changed: `FRONTIER` → `FRONTIER (PQ)`
   - Changed: `EXPLORED` → `EVALUATED`
   - Improved: Highlight current column with COLOR_ACCENT
   - Improved: Show `cost:` label instead of `c=`

2. ✅ **A* Renderer** (`_render_search_3col`)
   - Changed: Same column names as UCS
   - Improved: Show breakdown `g+h=f` in display
   - Kept: Score breakdown box at bottom

3. ✅ **BFS Renderer** (`_render_bfs_dfs`)
   - Changed: `CURRENT` → `CURRENT NODE`
   - Changed: `QUEUE` → `QUEUE (FIFO)`
   - Changed: `EXPLORED` → `EVALUATED`
   - Kept: Backtracking badge for DFS

4. ✅ **DFS Renderer** (`_render_bfs_dfs`)
   - Changed: `CURRENT` → `CURRENT NODE`
   - Changed: `EXPLORED` → `BACKTRACK LOG`
   - Kept: STACK label unchanged

**Files Modified:**
- `gui/visualizer.py`: Lines 537-665 (BFS/DFS, UCS/A* renderers)

**Next Priority:**
- Greedy/Hill Climbing column names
- IDA* column names
- Alpha-Beta/Minimax renderers

**Lý do ưu tiên:**
- UCS, A*, Alpha-Beta là 4 Tier Full → demo chính với giáo viên
- Tên cột sai → học sinh hiểu sai khái niệm → mất điểm báo cáo
- Dòng mô tả bằng lời sẽ làm sau (cần nhiều thời gian hơn)

---

## Summary for User

Đã hoàn thành **4/18 thuật toán** cải tiến tên cột:
1. ✅ UCS: EXPLORED → EVALUATED, FRONTIER (PQ)
2. ✅ A*: Tương tự UCS
3. ✅ BFS: QUEUE (FIFO), EVALUATED
4. ✅ DFS: BACKTRACK LOG

**Tác động:** Giao diện demo với cô giáo sẽ rõ ràng hơn, đúng thuật ngữ giáo khoa.

**Tiếp theo:** Cần cải tiến 14 thuật toán còn lại + thêm dòng mô tả bằng lời.

### Implementation Strategy

**Quan sát quan trọng:**
- ✅ Tất cả 18 renderer đã được implement trong `gui/visualizer.py`
- ✅ Backend (step_recorder.py + level*.py) đã hoàn chỉnh với đủ dữ liệu
- ⚠️ Cần cải thiện: **Tên cột** + **Mô tả bằng lời** trong visualizer

**Approach (theo CLAUDE.md - Surgical Changes):**
1. **KHÔNG sửa AI logic** (level1-6.py) - đã đủ tốt
2. **KHÔNG sửa step_recorder.py** - dataclass đã đủ fields
3. **CHỈ sửa gui/visualizer.py** - cải thiện labels + descriptions

**Priority:**
- 🔴 **P0 (High Impact):** UCS, Greedy, A*, Alpha-Beta (4 Tier Full - demo chính)
- 🟡 **P1 (Medium):** BFS, DFS, SA, IDA*, Minimax
- 🟢 **P2 (Low):** Level 4, Level 5 (Text tier)

---

## Mục Tiêu

Chuẩn hóa giao diện step-by-step của 18 thuật toán để:
- Khớp với lý thuyết chuẩn (đúng tên cột, đúng nội dung)
- Mỗi bước hiển thị **mô tả bằng lời** rõ ràng, không chỉ con số
- Nhất quán giữa các thuật toán cùng nhóm
- Người học AI lần đầu đọc được ngay, không cần giải thích thêm

---

## Nguyên Tắc Chung

### 1. Dòng mô tả (Description Line)
Mỗi bước PHẢI có 1 dòng mô tả bằng lời ở trên cùng, theo format:

```
[Tên thuật toán] đang xét [nước đi]: [giải thích ngắn gọn kết quả]
```

Ví dụ tốt:
```
✅ "UCS xét nước A6→A5: không ăn quân nào → cost = 1000 - 0 = 1000"
✅ "Greedy xét H2→H9: ăn Mã (300đ) → h = 300, đây là nước tốt nhất hiện tại"
✅ "DFS backtrack từ D2→D5: điểm trả về = -15, cập nhật best = -15"
```

Ví dụ xấu (hiện tại):
```
❌ "DFS ở depth=1, duyệt 20 nước đi"  ← quá chung chung
❌ "Xét nước (6, 0)→(5, 0): cost = 1000 - 0(—) = 1000"  ← khó đọc tọa độ tuple
```

### 2. Tên Cột
- **EXPLORED → EVALUATED**: tránh hiểu nhầm "đã đi rồi"
- DFS không dùng EXPLORED (backtrack không cần) → thay bằng **BACKTRACK LOG**
- Tên cột phải là danh từ ngắn gọn, đúng thuật ngữ giáo khoa

### 3. Nội Dung Cột
Mỗi dòng trong cột phải có đủ:
```
[Nước đi] | [Chỉ số chính] | [Nhãn trạng thái]
```

Ví dụ:
```
H2→H9 | h=300 | ★ TỐT NHẤT
B2→B9 | h=300 | bằng điểm
A6→A5 | h=0   | bỏ qua
```

### 4. Tọa Độ
Luôn hiển thị dạng **ký hiệu cờ** (B2→H9), không hiển thị tuple `(7,1)→(0,7)`.

---

## Chi Tiết Từng Thuật Toán

---

### LEVEL 1 — Tìm Kiếm Mù

---

#### 1. BFS

**Vấn đề hiện tại:** Thiếu thông tin độ sâu trong Queue, EXPLORED dễ gây hiểu nhầm.

**Cột đề xuất:**

| Cột | Tên | Nội dung |
|---|---|---|
| 1 | **CURRENT NODE** | Nước đang xét + depth hiện tại |
| 2 | **QUEUE (FIFO)** | Các nước đang chờ, kèm depth từng nước |
| 3 | **EVALUATED** | Các nước đã tính điểm xong, kèm điểm |

**Dòng mô tả mẫu:**
```
BFS pop node A6→A5 (depth=1): sinh 44 node con ở depth=2, thêm vào cuối Queue
BFS chấm điểm lá B2→B9 (depth=2): score = 290, truyền ngược lên node cha
BFS kết thúc: root chọn nước có score MAX = 290 → B2→B9
```

**Thay đổi cần làm:**
- Thêm trường `depth` vào mỗi dòng trong QUEUE
- Đổi tên EXPLORED → EVALUATED
- Thêm giai đoạn "Truyền điểm ngược" với mô tả rõ MAX/MIN

---

#### 2. DFS

**Vấn đề hiện tại:** CURRENT chỉ hiện `d=1`, EXPLORED luôn trống, STACK chỉ có 1 nước.

**Cột đề xuất:**

| Cột | Tên | Nội dung |
|---|---|---|
| 1 | **CURRENT PATH** | Chuỗi nước đang đi sâu: Ta→Địch→Ta |
| 2 | **STACK** | Nước đang thử ở đầu nhánh + lượt đi (Ta/Địch) + điểm tạm |
| 3 | **BACKTRACK LOG** | Các nước đã undo + điểm truyền ngược |

**Dòng mô tả mẫu:**
```
DFS đi sâu: Ta đi A6→A5 (depth=1) → Địch phản công D9→D8 (depth=2) → chạm đáy
DFS chạm đáy: evaluate_board() = -15 → truyền ngược lên node cha
DFS backtrack: undo D9→D8, cập nhật min_val = -15, thử phản công tiếp theo của Địch
DFS backtrack: undo A6→A5, trả score = -15 về root, so sánh với best hiện tại
```

**Thay đổi cần làm:**
- Bỏ hoàn toàn cột EXPLORED
- CURRENT PATH hiện chuỗi nước dạng `A6→A5 / D9→D8`
- BACKTRACK LOG ghi lại từng lần undo + điểm trả về

---

#### 3. UCS

**Vấn đề hiện tại:** EXPLORED gây hiểu nhầm "đã đi rồi".

**Cột đề xuất:**

| Cột | Tên | Nội dung |
|---|---|---|
| 1 | **CURRENT MOVE** | Nước đang xét + quân bị ăn + cost |
| 2 | **FRONTIER (PQ)** | Hàng đợi ưu tiên, sort theo cost tăng dần |
| 3 | **EVALUATED** | Các nước đã tính cost xong, xếp từ rẻ đến đắt |

**Dòng mô tả mẫu:**
```
UCS xét A6→A5: không ăn quân → cost = 1000 - 0 = 1000, thêm vào FRONTIER
UCS xét H2→H9: ăn Mã (300đ) → cost = 1000 - 300 = 700 ← rẻ nhất, cập nhật BEST
UCS xét B2→B9: ăn Mã (300đ) → cost = 700, bằng BEST hiện tại → giữ nguyên
UCS kết thúc: chọn nước cost thấp nhất = 700 → H2→H9
```

**Thay đổi cần làm:**
- Đổi tên EXPLORED → EVALUATED
- Mỗi dòng trong EVALUATED ghi rõ: `H2→H9 | cost=700 | ★ BEST`

---

### LEVEL 2 — Tìm Kiếm Heuristic

---

#### 4. Greedy

**Vấn đề hiện tại:** Giao diện 2 cột, thiếu cột EVALUATED.

**Cột đề xuất:**

| Cột | Tên | Nội dung |
|---|---|---|
| 1 | **CURRENT MOVE** | Nước đang xét + h(n) |
| 2 | **CANDIDATES** | Các nước chưa xét |
| 3 | **EVALUATED** | Các nước đã tính h xong, sort h giảm dần |

**Dòng mô tả mẫu:**
```
Greedy xét A6→A5: không ăn quân → h = 0, chưa tốt hơn BEST
Greedy xét H2→H9: ăn Mã (300đ) → h = 300 > max_val (0) → cập nhật BEST = H2→H9
Greedy xét B2→B9: ăn Mã (300đ) → h = 300 = max_val → giữ BEST = H2→H9 (gặp trước)
Greedy kết thúc: chọn h cao nhất = 300 → H2→H9
```

---

#### 5. A*

**Vấn đề hiện tại:** EXPLORED gây hiểu nhầm, thiếu breakdown g+h=f.

**Cột đề xuất:**

| Cột | Tên | Nội dung |
|---|---|---|
| 1 | **CURRENT MOVE** | Nước đang xét + g(n) + h(n) + f(n) |
| 2 | **FRONTIER (PQ)** | Hàng đợi, sort theo f tăng dần |
| 3 | **EVALUATED** | Các nước đã tính f xong, xếp từ tốt đến tệ |

**Dòng mô tả mẫu:**
```
A* xét A6→A5: g=1000 (không ăn quân) + h=14600 (vật chất Địch còn nguyên) = f=15600
A* xét H2→H9: g=700 (ăn Mã) + h=14300 (Địch mất Mã) = f=15000 ← tốt hơn, cập nhật BEST
A* kết thúc: chọn f nhỏ nhất = 15000 → H2→H9
```

**Thay đổi cần làm:**
- Đổi EXPLORED → EVALUATED
- Hiển thị rõ breakdown `g + h = f` thay vì chỉ f
- Sửa giá trị h cho nước ăn quân (h tính SAU make_move)

---

#### 6. IDA*

**Vấn đề hiện tại:** Không rõ cơ chế threshold tăng qua các iteration.

**Cột đề xuất:**

| Cột | Tên | Nội dung |
|---|---|---|
| 1 | **ITERATION STATE** | Vòng lặp hiện tại + threshold hiện tại |
| 2 | **CURRENT NODE** | Nước đang xét + f(n) + so sánh với threshold |
| 3 | **CUTOFF / PASS** | Các nước bị cắt (f > threshold) hoặc được chấp nhận |

**Dòng mô tả mẫu:**
```
IDA* Iteration 1: threshold = 14600
IDA* xét H2→H9: f = 15000 > threshold (14600) → CẮT, ghi nhớ min_exceeded = 15000
IDA* Iteration 1 kết thúc: không có nước nào pass, tăng threshold = 15000
IDA* Iteration 2: threshold = 15000
IDA* xét H2→H9: f = 15000 ≤ threshold (15000) → PASS → chọn H2→H9
```

---

### LEVEL 3 — Tìm Kiếm Cục Bộ

---

#### 7. Hill Climbing

**Vấn đề hiện tại:** Giao diện 2 cột, thiếu EVALUATED.

**Cột đề xuất:**

| Cột | Tên | Nội dung |
|---|---|---|
| 1 | **CURRENT STATE** | Nước mốc hiện tại + điểm mốc |
| 2 | **NEIGHBORS** | Các nước lân cận chưa đánh giá |
| 3 | **EVALUATED** | Các nước đã đánh giá + điểm, sort giảm dần |

**Dòng mô tả mẫu:**
```
Hill Climbing mốc hiện tại: chưa có nước nào, điểm mốc = -∞
Hill Climbing xét H2→E2: score = 10 > mốc (-∞) → leo đồi, cập nhật mốc = H2→E2 (10đ)
Hill Climbing xét H2→H9: score = 290 > mốc (10) → leo đồi, cập nhật mốc = H2→H9 (290đ)
Hill Climbing kết thúc: đỉnh đồi tìm được = H2→H9 (290đ)
```

---

#### 8. Simulated Annealing

**Vấn đề hiện tại:** Giao diện thẻ dọc, khó thấy logic xác suất Boltzmann.

**Cột đề xuất:**

| Cột | Tên | Nội dung |
|---|---|---|
| 1 | **PARAMETERS** | T hiện tại + alpha + vòng lặp |
| 2 | **COMPARISON** | Current vs Candidate + ΔE |
| 3 | **DECISION** | P(accept) + random value + kết quả Chấp nhận/Từ chối |

**Dòng mô tả mẫu:**
```
SA vòng 1: T=100.0, current=A6→A5 (score=0), candidate=H2→H9 (score=290)
SA tính: ΔE = 290 - 0 = 290 > 0 → Chấp nhận ngay (nước tốt hơn)
SA vòng 5: T=65.6, current=H2→H9 (score=290), candidate=A6→A5 (score=0)
SA tính: ΔE = 0 - 290 = -290 < 0 → P(accept) = e^(-290/65.6) = 0.012, random=0.847 > P → Từ chối
SA kết thúc: best_move_ever = B2→B9 (score=290đ)
```

---

#### 9. Beam Search

**Vấn đề hiện tại:** Worst-case hiển thị ở đáy dạng chữ nhỏ.

**Cột đề xuất:**

| Cột | Tên | Nội dung |
|---|---|---|
| 1 | **BEAMS (KEPT)** | Top K nước được giữ lại + initial score |
| 2 | **ELIMINATED** | Các nước bị loại + lý do |
| 3 | **WORST-CASE** | Phản công tệ nhất của Địch cho từng Beam + guaranteed score |

**Dòng mô tả mẫu:**
```
Beam Search chấm 44 nước: giữ top 3, loại 41 nước còn lại
Beam Search giữ: B2→B9 (290đ), H2→H9 (290đ), B2→D2 (10đ)
Beam Search xét worst-case cho B2→B9: Địch phản công tốt nhất → guaranteed = -165đ
Beam Search xét worst-case cho H2→H9: Địch phản công tốt nhất → guaranteed = -165đ
Beam Search xét worst-case cho B2→D2: Địch phản công tốt nhất → guaranteed = -280đ
Beam Search kết thúc: chọn Beam có guaranteed cao nhất = -165đ → B2→B9
```

---

### LEVEL 4 — Môi Trường Phức Tạp

---

#### 10. Online Search

**Vấn đề hiện tại:** Layout lộn xộn, không rõ cơ chế thay đổi trọng số động.

**Cột đề xuất:**

| Cột | Tên | Nội dung |
|---|---|---|
| 1 | **ENVIRONMENT** | Trạng thái (An toàn / Bị chiếu) + chiến thuật áp dụng |
| 2 | **WEIGHT ADJUST** | Bảng trọng số TRƯỚC → SAU khi điều chỉnh |
| 3 | **EVALUATED** | Các nước được chấm điểm theo trọng số mới |

**Dòng mô tả mẫu:**
```
Online Search kiểm tra: Đỏ KHÔNG bị chiếu → chế độ TẤN CÔNG
Online Search điều chỉnh trọng số: Xe 900→1100, Pháo 450→550, Mã 300→400
Online Search chấm H2→H9: ăn Mã (trọng số mới=400đ) → score=290, BEST hiện tại
Online Search kết thúc: chọn nước score cao nhất theo trọng số tấn công → H2→H9
```

---

#### 11. AND-OR Search

**Vấn đề hiện tại:** Layout thẻ + danh sách, không rõ OR node vs AND node.

**Cột đề xuất:**

| Cột | Tên | Nội dung |
|---|---|---|
| 1 | **OR NODE (AI)** | Nước của Ta đang xét + guaranteed score tạm |
| 2 | **AND NODES (OPP)** | Tất cả phản công của Địch + score từng phản công |
| 3 | **WORST-CASE** | Phản công nguy hiểm nhất + guaranteed score cuối |

**Dòng mô tả mẫu:**
```
AND-OR OR node: Ta thử H2→E2
AND-OR AND nodes: Địch có 45 phản công, duyệt tất cả để tìm nguy hiểm nhất
AND-OR worst-case: Địch đi B7→B0 → score cho Ta = -280 → guaranteed(H2→E2) = -280
AND-OR OR node tiếp: Ta thử H2→G2 → guaranteed = -285 < -280 → H2→E2 vẫn tốt hơn
AND-OR kết thúc: chọn OR node có guaranteed cao nhất = -280 → H2→E2
```

---

#### 12. Belief State Search

**Vấn đề hiện tại:** Hiển thị rời rạc, không rõ luồng từ xác suất → điểm kỳ vọng.

**Cột đề xuất:**

| Cột | Tên | Nội dung |
|---|---|---|
| 1 | **OPPONENT STYLE** | Phong cách dự đoán + phân phối xác suất belief |
| 2 | **UTILITY ANALYSIS** | Điểm nước đi theo 3 phong cách giả định |
| 3 | **EXPECTED UTILITY** | Công thức E[U] + kết quả + xếp hạng |

**Dòng mô tả mẫu:**
```
Belief State: lịch sử trống → mặc định Địch aggressive
Belief State xác suất: P(aggressive)=0.6, P(defensive)=0.2, P(positional)=0.2
Belief State xét H2→E2: u_agg=15×1.5=22.5, u_def=160, u_pos=100
Belief State tính E[U]: 0.6×22.5 + 0.2×160 + 0.2×100 = 13.5+32+20 = 65.5
Belief State kết thúc: chọn nước E[U] cao nhất → H2→E2
```

---

### LEVEL 5 — CSP

---

#### 13. Backtracking MRV

**Vấn đề hiện tại:** Chỉ 2 cột, thiếu cột ASSIGNMENT.

**Cột đề xuất:**

| Cột | Tên | Nội dung |
|---|---|---|
| 1 | **VARIABLES (MRV)** | Danh sách quân + domain size, highlight quân MRV |
| 2 | **DOMAIN VALUES** | Các ô đích khả dĩ của quân được chọn |
| 3 | **ASSIGNMENT** | Điểm từng ô đích + nước được gán |

**Dòng mô tả mẫu:**
```
MRV liệt kê biến: Tốt A3 (domain=1), Tốt C3 (domain=1), Pháo B2 (domain=12)...
MRV chọn biến: Tốt A3 có domain nhỏ nhất = 1 → xét trước
MRV domain của A3: chỉ có 1 ô đích là A4
MRV gán A3→A4: score=0 → chọn A3→A4 (không có lựa chọn nào khác)
MRV kết thúc: assignment = A3→A4
```

---

#### 14. Min-Conflicts

**Vấn đề hiện tại:** 1 thẻ tóm tắt + 1 danh sách dọc.

**Cột đề xuất:**

| Cột | Tên | Nội dung |
|---|---|---|
| 1 | **CURRENT STATE** | Số xung đột hiện tại + danh sách quân bị đe dọa |
| 2 | **CONFLICT RESOLUTION** | Từng nước đi + số xung đột còn lại sau nước đó |
| 3 | **EVALUATED** | Điểm vị thế bàn cờ để tiebreak khi hòa xung đột |

**Dòng mô tả mẫu:**
```
Min-Conflicts: hiện tại có 2 xung đột (Mã B0 và Mã H0 đang bị đe dọa)
Min-Conflicts xét H2→E2: sau nước này còn 1 xung đột → tốt hơn hiện tại
Min-Conflicts xét H2→F2: sau nước này còn 1 xung đột, score=10 → bằng H2→E2
Min-Conflicts tiebreak: H2→E2 gặp trước → chọn H2→E2
Min-Conflicts kết thúc: giảm xung đột từ 2 xuống 1 → H2→E2
```

---

#### 15. AC-3

**Vấn đề hiện tại:** Nước được chọn hiển thị ở thanh ngang dưới cùng.

**Cột đề xuất:**

| Cột | Tên | Nội dung |
|---|---|---|
| 1 | **SAFE DOMAIN** | Các nước an toàn (không bị ăn bởi quân rẻ hơn) |
| 2 | **PRUNED DOMAIN** | Các nước bị loại + lý do cụ thể |
| 3 | **CHOSEN ASSIGNMENT** | Điểm các nước an toàn + nước được chọn |

**Dòng mô tả mẫu:**
```
AC-3 kiểm tra 44 nước: lọc các nước bị quân rẻ hơn của Địch tấn công
AC-3 kết quả lọc: 44 nước an toàn, 0 nước bị prune (khai cuộc chưa có bẫy)
AC-3 chấm điểm safe domain: H2→H9 score=290 → cao nhất
AC-3 kết thúc: không có nước bị prune, chọn safe move điểm cao nhất → H2→H9
```

---

### LEVEL 6 — Tìm Kiếm Đối Kháng

---

#### 16. Minimax

**Vấn đề hiện tại:** PATH dạng hình tròn nằm ngang chiếm nhiều diện tích, ít thông tin.

**Cột đề xuất:**

| Cột | Tên | Nội dung |
|---|---|---|
| 1 | **CURRENT PATH** | Chuỗi nước từ root dạng chữ: Ta→Địch→Ta |
| 2 | **NODE STATE** | MAX hay MIN + giá trị truyền ngược hiện tại |
| 3 | **SIBLINGS EVALUATED** | Điểm các nước anh em đã duyệt + best so far |

**Dòng mô tả mẫu:**
```
Minimax root: Ta thử B2→B9 (depth=3, MAX node)
Minimax depth=2: Địch phản công A9→B9 (MIN node, đang tìm nước tệ nhất cho Ta)
Minimax depth=1: Ta thử H2→H9 (MAX node)
Minimax depth=0: chạm đáy, evaluate_board() = 125 → truyền ngược lên
Minimax MIN node: nhận 125, cập nhật min_val = 125, thử phản công tiếp
Minimax MIN node: nhận -165, cập nhật min_val = -165 (tệ hơn cho Ta)
Minimax MAX node (root): nhận -165 cho nhánh B2→B9, so sánh với best = -inf → cập nhật
```

---

#### 17. Alpha-Beta

**Vấn đề hiện tại:** Tương tự Minimax, thiếu hiển thị rõ điều kiện cắt tỉa.

**Cột đề xuất:**

| Cột | Tên | Nội dung |
|---|---|---|
| 1 | **CURRENT PATH** | Chuỗi nước từ root dạng chữ |
| 2 | **BOUNDS (α / β)** | Giá trị alpha + beta hiện tại + trạng thái cắt tỉa |
| 3 | **EVALUATED & PRUNED** | Nước đã duyệt (kèm điểm) + nước bị cắt (nhãn CẮT TỈA) |

**Dòng mô tả mẫu:**
```
Alpha-Beta root: α=-∞, β=+∞, Ta thử B2→B9
Alpha-Beta depth=2 (MIN): nhận value=-330, cập nhật β=-330
Alpha-Beta depth=2 (MIN): α=-∞ < β=-330 → chưa cắt, tiếp tục
Alpha-Beta MAX node: α tăng lên 120
Alpha-Beta MIN node tiếp: β=80 ≤ α=120 → CẮT TỈA, bỏ qua các nhánh còn lại
```

---

#### 18. Expectimax

**Vấn đề hiện tại:** Công thức xác suất hiển thị ở đáy, không trực quan.

**Cột đề xuất:**

| Cột | Tên | Nội dung |
|---|---|---|
| 1 | **NODE STATE** | MAX node (Ta đi) hay CHANCE node (Địch đi) |
| 2 | **CHILD VALUES** | Điểm tất cả nhánh con từ node hiện tại |
| 3 | **PROBABILITY EVAL** | Công thức `0.7×Best + 0.3×Avg` + kết quả kỳ vọng |

**Dòng mô tả mẫu:**
```
Expectimax MAX node: Ta thử B2→B9
Expectimax CHANCE node: Địch không chơi tối ưu 100%, xét tất cả phản công
Expectimax child values: [125, 455, 490, 490, 577, ...]
Expectimax tính kỳ vọng: Best=125, Avg(others)=505
Expectimax E[V] = 0.7×125 + 0.3×505 = 87.5 + 151.5 = 239
Expectimax kết thúc: chọn root move có E[V] cao nhất → B2→B9
```

---

## Kế Hoạch Thực Hiện

### Bước 0 — Freeze Code AI (Không sửa logic thuật toán)
Tạo branch mới riêng cho UI fix, không động vào `level1.py` → `level6.py` về phần logic.

### Bước 1 — Cập Nhật Dataclass trong `step_recorder.py` ✅ Đã hoàn thành (2026-06-28)
Bổ sung đầy đủ các trường còn thiếu vào `ai/step_recorder.py`:

| Thuật toán | Trường cần thêm |
|---|---|
| BFS | `depth` trong mỗi node của queue |
| DFS | `backtrack_log: list` (nước đã undo + điểm trả về) |
| UCS | (đổi tên trường `explored` → `evaluated`) |
| Greedy | `candidates: list`, `evaluated: list` |
| A* | `g`, `h`, `f` riêng biệt thay vì chỉ `f` |
| IDA* | `iteration`, `threshold`, `status` (PASS/CẮT) |
| SA | `random_value`, `p_accept`, `decision` |
| Belief State | `u_agg`, `u_def`, `u_pos`, `expected_u` breakdown rõ |
| Minimax | `path: list`, `node_type` (MAX/MIN), `siblings: list` |
| Alpha-Beta | `alpha`, `beta`, `pruned: bool` |
| Expectimax | `node_type` (MAX/CHANCE), `child_values`, `best_res`, `others_avg` |

### Bước 2 — Cập Nhật Lời Ghi Bước trong AI Files
Chỉ sửa các lệnh `recorder.add_step(...)` để truyền thêm trường mới. Không sửa logic tính toán.

Ưu tiên sửa theo thứ tự:
1. UCS, Greedy (chỉ đổi tên trường, dễ nhất)
2. A*, IDA* (thêm breakdown g/h/f, sửa giá trị h sau make_move)
3. DFS (thêm backtrack_log)
4. SA (thêm random_value, p_accept)
5. Minimax, Alpha-Beta, Expectimax (thêm path, siblings, bounds)
6. Belief State (thêm breakdown utility)

### Bước 3 — Cập Nhật Renderer trong `gui/visualizer.py`

*(⚠️ **Lưu ý đồng bộ code:** Dù một số tài liệu nhật ký ghi đã làm Đợt 1, thực tế trong `gui/visualizer.py` hiện tại vẫn đang chạy code cũ với các cột `CURRENT`, `EXPLORED`, `FRONTIER`. Do đó, cần tiến hành tuần tự sau khi Bước 1 & 2 hoàn tất để tránh lỗi `AttributeError` khi Dataclass chưa có trường mới).*

Sửa chính xác các hàm render theo nhóm trong `gui/visualizer.py`:

| Nhóm | Hàm render thực tế | Thay đổi chính |
|---|---|---|
| **BFS / DFS** | `_render_bfs_dfs` | Đổi tên cột `QUEUE` → `QUEUE (FIFO)`.<br>Đổi `EXPLORED` → `EVALUATED` (với BFS) và `BACKTRACK LOG` (với DFS).<br>Bổ sung hiển thị `depth` và `backtrack_log`. |
| **UCS / Greedy / A* / IDA*** | `_render_search_3col`<br>`_render_ida_star` | Đổi `CURRENT` → `CURRENT MOVE`, `FRONTIER` → `FRONTIER (PQ)`, `EXPLORED` → `EVALUATED`.<br>Chuyển `Greedy` và `IDA*` sang cấu trúc 3 cột đồng bộ.<br>Hiển thị rõ breakdown công thức $f = g + h$ và threshold. |
| **Local Search** | `_render_candidates_list`<br>`_render_sa`<br>`_render_beam` | Chuyển `Hill Climbing` và `SA` sang layout 3 cột.<br>Đưa phần phân tích `Worst-case` của `Beam Search` từ thanh đáy lên thành cột thứ 3. |
| **Level 4** | `_render_level4`<br>(`_render_online`, `_render_andor`, `_render_belief`) | Chuẩn hóa toàn bộ 3 module con về layout 3 cột đồng bộ.<br>Thêm dòng mô tả trạng thái và chiến thuật động. |
| **CSP (Level 5)** | `_render_csp`<br>(`_render_backtrack`, `_render_min_conflicts`, `_render_ac3`) | Bổ sung cột thứ 3 `ASSIGNMENT` cho `Backtracking MRV`.<br>Chuyển `Min-Conflicts` và `AC-3` sang 3 cột rõ ràng (Safe/Pruned/Chosen). |
| **Level 6** | `_render_alpha_beta`<br>`_render_minimax_expectimax`<br>(`_render_minimax`, `_render_expectimax`) | Chuyển `PATH` từ hình tròn nằm ngang sang dạng chữ ở cột 1.<br>Làm nổi bật điều kiện cắt tỉa $\beta \le \alpha$ ở cột 2.<br>Bổ sung cột 3 giải thích công thức Expectimax $0.7 \times \text{Best} + 0.3 \times \text{Avg}$. |

### Bước 4 — Thêm Dòng Mô Tả Cho Tất Cả
Đây là bước quan trọng nhất. Mỗi bước phải có 1 dòng mô tả bằng lời ở trên cùng theo format:
```
[Thuật toán] [hành động]: [nước đi] → [kết quả] → [quyết định]
```

### Bước 5 — Kiểm Tra Nhất Quán
Sau khi sửa xong, chạy tất cả 18 thuật toán và kiểm tra:
- [ ] Mỗi bước có dòng mô tả bằng lời
- [ ] Không có cột nào trống vô nghĩa
- [ ] Tọa độ hiển thị dạng ký hiệu cờ (B2→H9), không phải tuple
- [ ] Tên cột đúng với lý thuyết từng thuật toán
- [ ] Nhất quán trong cùng nhóm thuật toán

---

## Tổng Hợp Thay Đổi Tên Cột

| Thuật toán | Cột 1 | Cột 2 | Cột 3 |
|---|---|---|---|
| BFS | CURRENT NODE | QUEUE (FIFO) | EVALUATED |
| DFS | CURRENT PATH | STACK | BACKTRACK LOG |
| UCS | CURRENT MOVE | FRONTIER (PQ) | EVALUATED |
| Greedy | CURRENT MOVE | CANDIDATES | EVALUATED |
| A* | CURRENT MOVE | FRONTIER (PQ) | EVALUATED |
| IDA* | ITERATION STATE | CURRENT NODE | CUTOFF / PASS |
| Hill Climbing | CURRENT STATE | NEIGHBORS | EVALUATED |
| Simulated Annealing | PARAMETERS | COMPARISON | DECISION |
| Beam Search | BEAMS (KEPT) | ELIMINATED | WORST-CASE |
| Online Search | ENVIRONMENT | WEIGHT ADJUST | EVALUATED |
| AND-OR Search | OR NODE (AI) | AND NODES (OPP) | WORST-CASE |
| Belief State | OPPONENT STYLE | UTILITY ANALYSIS | EXPECTED UTILITY |
| Backtracking MRV | VARIABLES (MRV) | DOMAIN VALUES | ASSIGNMENT |
| Min-Conflicts | CURRENT STATE | CONFLICT RESOLUTION | EVALUATED |
| AC-3 | SAFE DOMAIN | PRUNED DOMAIN | CHOSEN ASSIGNMENT |
| Minimax | CURRENT PATH | NODE STATE | SIBLINGS EVALUATED |
| Alpha-Beta | CURRENT PATH | BOUNDS (α / β) | EVALUATED & PRUNED |
| Expectimax | NODE STATE | CHILD VALUES | PROBABILITY EVAL |


---

## 📚 MỤC LỤC ĐỒ ÁN - ĐÃ HOÀN THÀNH

Đã tạo file **`MUC_LUC.md`** hoàn chỉnh cho báo cáo với cấu trúc:

### Các phần chính:

**I. TỔNG QUAN ĐỒ ÁN**
- Giới thiệu đề tài: Game Cờ Tướng với 18 thuật toán AI
- Yêu cầu bài toán & công nghệ

**II. PHÂN TÍCH VÀ THIẾT KẾ**
- Kiến trúc tổng thể
- **Bảng chi tiết 18 thuật toán theo 6 levels** với lý do chọn từng thuật toán
- Luật chơi Cờ Tướng

**III. CÀI ĐẶT CHI TIẾT**
- Module game/, ai/, gui/
- Chi tiết cài đặt từng thuật toán
- Report Mode flow

**IV. TESTING & KẾT QUẢ**
- **Bảng Win Rate** so sánh các thuật toán
- Kịch bản demo 4 Tier Full

**V. KẾT LUẬN**
- Kết quả đạt được
- Hướng phát triển

**PHỤ LỤC**
- Cấu trúc thư mục
- **Công thức toán học** cho 6 thuật toán chính
- Phím tắt, bảng giá trị quân
- Tài liệu tham khảo

### File đã tạo:
- `MUC_LUC.md` - ~500 dòng, format Markdown đầy đủ
- Sẵn sàng export sang Word/PDF cho báo cáo

