# Báo Cáo Code Review - Dự Án Cờ Tướng AI

Dưới đây là đánh giá chi tiết về cấu trúc mã nguồn, chất lượng lập trình, các lỗi logic (bug) tiềm ẩn và đề xuất cải tiến cho dự án Cờ Tướng AI.

---

## 📊 Tổng Quan Đánh Giá

| Tiêu Chí | Đánh Giá | Chi Tiết |
| :--- | :--- | :--- |
| **Cấu Trúc Dự Án** | **Khá** | Tổ chức module rõ ràng (`game`, `gui`, `ai`), giao diện `pygame` mượt mà, hỗ trợ đa luồng để tránh đơ giao diện khi AI đang tính toán. |
| **Chất Lượng Thuật Toán** | **Trung Bình** | Triển khai sáng tạo nhiều loại thuật toán. Tuy nhiên, nhiều thuật toán tìm kiếm đơn tác nhân (BFS, DFS, A*) bị đơn giản hóa quá mức và có lỗi logic khi chạy thực tế. |
| **Độ Tin Cậy & Kiểm Thử** | **Yếu** | Hoàn toàn chưa có bộ mã kiểm thử tự động (Unit Tests / Integration Tests). |
| **Hiệu Năng & Tối Ưu** | **Trung Bình** | Các thuật toán cấp cao (Minimax, Alpha-Beta) có giới hạn thời gian chạy (1.2s) để tránh treo, nhưng việc cắt tỉa và sắp xếp nước đi chưa được tối ưu triệt để. |

---

## 🔍 Chi Tiết Các Vấn Đề Quan Trọng (Critical & High Issues)

### 1. [HIGH] Lỗi Logic Trong Expectimax Khi Cầm Quân Đen (Black)
* **Tệp tin**: [level6.py](file:///c:/Users/ADMIN/Documents/MyProject/chinese_chess/ai/level6.py) (Hàm `expectimax_move`)
* **Mô tả**: Thuật toán Expectimax giả định người chơi là quân Đỏ (MAX) và đối thủ là quân Đen (MIN/Chance). Khi AI được cấu hình cầm quân Đen (Black), nó vẫn coi lượt của quân Đen là các nút Chance (nước đi ngẫu nhiên 30%) và lượt của quân Đỏ là nút MAX (tối ưu hóa).
* **Hậu quả**: AI cầm quân Đen sẽ tự đánh giá rằng bản thân nó sẽ đi quân ngẫu nhiên 30%, dẫn đến việc chọn nước đi không tối ưu cho chính mình.
* **Đề xuất sửa đổi**:
  Thay đổi logic để xác định nút MAX và nút Chance động dựa trên màu quân mà AI đang cầm:
  ```python
  # Thay vì cố định is_max và Chance node theo màu Red/Black:
  # Xác định động: Lượt của bản thân AI = Nút Tối ưu (Min hoặc Max tùy thuộc màu quân)
  # Lượt của đối thủ = Nút Chance (Tính giá trị kỳ vọng)
  ```

### 2. [HIGH] Cắt Tỉa Tùy Tiện Trong Local Beam Search
* **Tệp tin**: [level3.py](file:///c:/Users/ADMIN/Documents/MyProject/chinese_chess/ai/level3.py) (Hàm `beam_search_move`)
* **Mô tả**: Ở dòng 103:
  ```python
  for ofrom, oto in opp_moves[:10]: # Limit branching factor for speed
  ```
  Danh sách `opp_moves` (các nước đi hợp lệ của đối thủ) hoàn toàn chưa được sắp xếp. Việc lấy trực tiếp `opp_moves[:10]` là lấy ngẫu nhiên 10 nước đi đầu tiên trong danh sách thô.
* **Hậu quả**: AI có thể bỏ sót hoàn toàn nước đi cực tốt của đối thủ (ví dụ: ăn Xe, chiếu bí) nếu nước đi đó nằm ở vị trí thứ 11 trở đi, khiến AI đánh giá sai lệch hoàn toàn giá trị của nước đi hiện tại.
* **Đề xuất sửa đổi**:
  Hãy sắp xếp danh sách `opp_moves` bằng hàm `sort_moves` (ưu tiên ăn quân trước) trước khi cắt lấy 10 phần tử đầu tiên.

### 3. [MEDIUM] Hiểu Sai Khái Niệm AND-OR Search
* **Tệp tin**: [level4.py](file:///c:/Users/ADMIN/Documents/MyProject/chinese_chess/ai/level4.py) (Hàm `and_or_search_move`)
* **Mô tả**: Docstring ghi: *"We treat our moves as AND nodes and the opponent's responses as OR nodes"*.
* **Giải thích**: Theo định nghĩa chuẩn của cây tìm kiếm AND-OR trong AI:
  - Nút **OR** đại diện cho lượt của ta (ta chỉ cần chọn *một* trong các nước đi dẫn đến chiến thắng).
  - Nút **AND** đại diện cho lượt của đối thủ (ta phải chống đỡ được *tất cả* các phản hồi có thể xảy ra của đối thủ).
  Thực tế mã nguồn đang chạy đúng theo bản chất của 2-ply Minimax nhưng phần diễn giải khái niệm trong tài liệu bị ngược.

---

## 🛠️ Nhận Xét Về Các Thuật Toán Cấp Thấp (Level 1 - Level 2)

### 1. BFS & DFS Đơn Giản Hóa Quá Mức (Trivial Implementation)
* **Tệp tin**: [level1.py](file:///c:/Users/ADMIN/Documents/MyProject/chinese_chess/ai/level1.py)
* BFS trả về `legal_moves[0]` và DFS trả về `legal_moves[-1]`. Vì thuật toán chỉ tìm kiếm ở độ sâu 1 (depth=1), hàng đợi FIFO (BFS) chỉ đơn giản là lấy phần tử đầu tiên và LIFO (DFS) lấy phần tử cuối cùng.
* **Nhận xét**: Đây không phải là thuật toán duyệt cây tìm kiếm thực tế mà chỉ là lấy phần tử đầu/cuối của danh sách nước đi thô.

### 2. UCS và Greedy Trùng Lặp Bản Chất
* UCS định nghĩa giá trị chi phí `cost = 1000 - cap_val` (ưu tiên ăn quân giá trị cao để giảm chi phí). Thuật toán này có kết quả trả về hoàn toàn tương đương với thuật toán `Greedy` ở Level 2.

### 3. A* và IDA* Sử Dụng Trên Trò Chơi Đối Kháng 2 Người
* **Tệp tin**: [level2.py](file:///c:/Users/ADMIN/Documents/MyProject/chinese_chess/ai/level2.py)
* A* và IDA* vốn là thuật toán tìm kiếm đường đi đơn tác nhân (Single-agent pathfinding). Khi áp dụng vào game đối kháng 2 người, việc định nghĩa hàm heuristic $h(n)$ là tổng giá trị quân cờ còn lại của đối thủ sẽ hoạt động giống như một bộ định giá tham lam tĩnh (Static Greedy Evaluation) chứ không thực sự tìm kiếm chuỗi nước đi tối ưu trước đối thủ thông minh.

---

## 💡 Đề Xuất Cải Tiến Tổng Thể

1. **Bổ Sung Unit Tests**:
   - Cần viết các tệp kiểm thử tự động cho phần luật chơi ([rules.py](file:///c:/Users/ADMIN/Documents/MyProject/chinese_chess/game/rules.py)) như: kiểm tra trạng thái chiếu tướng, chiếu bí, hết nước đi (stalemate) và luật cấm lộ mặt tướng.
2. **Đồng Bộ Luồng Tính Toán (Thread Safety)**:
   - Trong [main.py](file:///c:/Users/ADMIN/Documents/MyProject/chinese_chess/main.py), biến `self.ai_result` được ghi từ luồng nền (`calculate()`) và đọc/xóa ở luồng chính mà không dùng khóa (`Lock`). Mặc dù GIL của Python tự bảo vệ các thao tác gán cơ bản, việc sử dụng cơ chế an toàn luồng rõ ràng hơn sẽ tránh được các hành vi bất thường khi mở rộng tính năng.
3. **Tối Ưu Hóa Bộ Nhớ**:
   - Khi sao chép bàn cờ (`board.copy()`), cấu trúc dữ liệu hiện tại sao chép toàn bộ ma trận 10x9 chứa các đối tượng `Piece`. Để AI tìm kiếm sâu hơn (depth >= 5), nên chuyển sang biểu diễn bàn cờ dạng mảng số nguyên phẳng (Integer Array / Bitboard) để tăng tốc độ sao chép và tính toán nước đi hợp lệ lên gấp 10-100 lần.
