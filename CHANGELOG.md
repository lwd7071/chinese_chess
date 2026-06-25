# Nhật ký thay đổi (CHANGELOG) - Hệ thống EXP, Chỉ số AI & Điều khiển Bot Song song

Tài liệu này ghi lại toàn bộ các thay đổi và tính năng được thêm mới từ yêu cầu đầu tiên của bạn cho đến thời điểm hiện tại. Tất cả mã nguồn đã được tích hợp, tối ưu hóa và kiểm thử thành công.

---

## Tóm tắt các tính năng đã thực hiện

### 1. Hệ thống điểm kinh nghiệm (EXP) trận đấu
* **Giá trị quân cờ chuẩn:** Định nghĩa bảng điểm số cho các quân cờ còn lại của bên thắng cuộc:
  - Xe (`R`): 90 điểm
  - Pháo (`C`): 45 điểm
  - Mã (`H`): 45 điểm
  - Tượng (`E`): 20 điểm
  - Sĩ (`A`): 20 điểm
  - Tốt (`P`): 10 điểm
  - Tướng (`G`): 0 điểm
* **Hàm tính toán độc lập (`main.py`):**
  - `calculate_remaining_piece_score(board, winner_color)`: Tính tổng điểm các quân cờ còn sống của bên thắng.
  - `calculate_win_exp(board, winner_color)`: Áp dụng công thức tính EXP thắng trận: $\text{EXP} = 100 + \frac{\text{tổng\_điểm\_quân\_cờ}}{2}$.
* **Cập nhật và lưu trữ hồ sơ:**
  - Phần thưởng EXP của Người chơi (Đỏ) được cộng trực tiếp và lưu trữ bền vững vào hồ sơ `profile.json` thông qua cấu trúc lớp `Settings` trong `gui/settings.py`.
  - EXP của đối thủ Bot (Đen) được cập nhật tạm thời trong phiên chơi hiện tại.
  - Cập nhật biến cờ hiệu `self.exp_awarded` để bảo đảm EXP chỉ được trao duy nhất một lần khi trận đấu kết thúc.
* **Giao diện hiển thị đồng bộ:** Hiển thị điểm số EXP thời gian thực của cả hai bên trên bảng thông tin Sidebar ("Red EXP: X", "Black EXP: Y") và hiển thị thông báo nhận EXP rõ ràng tại màn hình kết thúc game.

### 2. Quản lý chỉ số AI tìm kiếm thông minh (Node, Frontier, Explored)
* **Tự động đóng băng theo lượt:**
  - Ở chế độ Người đấu Bot, các chỉ số tính toán AI chỉ tăng và chuyển động khi đến lượt của Bot tính toán. Khi đến lượt của Người chơi, các chỉ số này sẽ **tự động đứng yên (đóng băng)** vì con người tự suy nghĩ.
* **Cộng dồn đột biến sau nước đi:**
  - Sau mỗi nước đi của Bot, các chỉ số tính toán sẽ được cộng dồn thêm một lượng ngẫu nhiên lớn nhằm phản ánh khối lượng công việc Bot đã thực hiện. Nước đi của con người sẽ không cộng dồn các chỉ số này.
* **Đóng băng khi kết thúc game:**
  - Khi trận đấu kết thúc (Thắng/Thua/Hòa/Đầu hàng), thanh tiến trình sẽ chuyển sang trạng thái tĩnh và hiển thị dòng chữ **"KẾT THÚC"** màu xanh ngọc, đồng thời đóng băng toàn bộ chỉ số AI.

### 3. Giao diện thay đổi thuật toán Bot động & Dropdown song song
* **Hai dropdown song song trong chế độ Bot đấu Bot:**
  - Ở chế độ Bot đấu Bot, sidebar tự động hiển thị **2 nút dropdown song song** cạnh nhau (màu Đỏ cho Bot Đỏ và màu Vàng cho Bot Đen).
  - Cho phép người chơi thay đổi thuật toán độc lập cho từng Bot ngay trong lúc trận đấu đang diễn ra để đổi tư duy cho Bot.
* **Định vị và co giãn thông minh:**
  - Dropdown mở rộng của từng bên được căn chỉnh chuẩn xác dưới nút kích hoạt của bên đó với chiều rộng thu hẹp bằng một nửa.
  - Tên thuật toán dài được đo đạc tự động và cắt ngắn bằng dấu `...` để vừa vặn trong khung hẹp mà không bị tràn hay đè lên các thành phần khác.
* **Cập nhật cấp độ thuật toán tự động:**
  - Khi chọn thuật toán mới từ dropdown, hệ thống tự động tra cứu cấp độ tương ứng (từ L1 đến L6) trong danh sách `ALGO_OPTIONS` và cập nhật tức thì trên giao diện (ví dụ: hiển thị `L6: Expectimax` thay vì chỉ có tên thuật toán).

### 4. Khắc phục lỗi và tối ưu hóa hệ thống
* **Sửa lỗi out game:**
  - Khắc phục triệt để lỗi `UnboundLocalError: cannot access local variable 'is_bot_thinking'` bằng cách đưa biến về phạm vi ngoài vòng lặp thời gian.
  - Khắc phục lỗi `NameError: name 'COLOR_GOLD' is not defined` bằng cách thay thế bằng hằng số màu sắc chuẩn `COLOR_ACCENT`.
* **Vẽ an toàn (Defensive Rendering):**
  - Bổ sung kiểm tra `None` cho cấp độ Bot trong `main.py` để tránh lỗi `TypeError` khi khởi tạo trực tiếp hoặc chạy trong môi trường kiểm thử.

---

## Chi tiết các tệp đã sửa đổi

### 1. [main.py](file:///c:/Users/nguye/Downloads/chinese_chess-dev/chinese_chess-dev/main.py)
* **Thêm các hàm tính EXP cấp module:**
  ```python
  def calculate_remaining_piece_score(board, winner_color):
      # Định nghĩa điểm số và tính tổng quân còn sống của bên thắng...
  
  def calculate_win_exp(board, winner_color):
      # Tính toán EXP theo công thức...
  ```
* **Khởi tạo trạng thái EXP tại `__init__`:**
  ```python
  self.red_exp = self.settings.data.get("exp", 0)
  self.black_exp = 0
  self.exp_awarded = False
  ```
* **Xử lý sự kiện thay đổi thuật toán song song:**
  ```python
  if action.startswith("select_algo:") or action.startswith("select_algo_red:") or action.startswith("select_algo_black:"):
      # Tra cứu cấp độ thuật toán và gán cho Bot tương ứng (Red/Black)...
  ```
* **Vẽ an toàn trong `draw_game_screen`:**
  ```python
  red_bot_lvl = self.menu.red_bot_level if self.menu.red_bot_level is not None else 0
  black_bot_lvl = self.menu.black_bot_level if self.menu.black_bot_level is not None else 0
  red_bot = f"L{red_bot_lvl + 1}: {self.menu.red_bot_algo}" if self.menu.red_bot_algo and self.menu.red_bot_algo != "Human" else "Human"
  black_bot = f"L{black_bot_lvl + 1}: {self.menu.black_bot_algo}" if self.menu.black_bot_algo else ""
  ```

### 2. [gui/sidebar.py](file:///c:/Users/nguye/Downloads/chinese_chess-dev/chinese_chess-dev/gui/sidebar.py)
* **Vẽ hai dropdown song song cho chế độ Bot đấu Bot:**
  - Chia nhỏ tọa độ `self.dropdown_rect` thành `dropdown_rect_red` và `dropdown_rect_black`.
  - Hiển thị thông tin thuật toán hiện tại tương ứng với màu sắc Đỏ/Vàng đặc trưng.
* **Mở rộng dropdown thông minh:**
  - Tự động xác định bên đang mở (`self.dropdown_open == "red"` hoặc `"black"`) để định vị hộp danh sách và kiểm tra lựa chọn hiện tại (`is_currently_selected`).
  - Thêm cơ chế đo chiều rộng văn bản và tự động thêm dấu `...` nếu tên thuật toán quá dài.
* **Bắt sự kiện click chuột tách biệt:**
  - Cập nhật `handle_event` để lắng nghe click riêng vào nút bấm của từng bên và trả về chuỗi hành động riêng biệt.
* **Đóng băng chỉ số AI:**
  - Cập nhật các chỉ số `sim_nodes`, `sim_frontier`, `sim_explored` dựa trên trạng thái `is_bot_thinking` và `is_game_over`.

### 3. [gui/settings.py](file:///c:/Users/nguye/Downloads/chinese_chess-dev/chinese_chess-dev/gui/settings.py)
* Cập nhật phương thức `add_match_record(self, result, duration_str="00:00", gold_change=0, exp_gained=0)` để ghi nhận lượng EXP nhận được và cộng dồn bền vững vào cấu trúc dữ liệu cấu hình, sau đó tự động lưu vào tệp `profile.json`.

---

## Xác minh & Kiểm thử

1. **Bộ kiểm thử tự động chuyên biệt (`tests/test_exp.py`):**
   - Đã viết các trường hợp kiểm thử để kiểm tra giá trị của từng quân cờ và công thức tính EXP thắng cuộc. Tất cả đều vượt qua (**PASS**).
2. **Kịch bản kiểm thử luồng sự kiện (`scratch/test_dropdown_flow.py`):**
   - Mô phỏng toàn bộ hành vi mở dropdown, cuộn chuột và thay đổi thuật toán của cả hai Bot ở cả hai chế độ chơi để đảm bảo không xảy ra lỗi crash hay NameError. Kết quả vượt qua (**PASS**).
3. **Bộ kiểm thử tích hợp hệ thống (`run_evals.py`):**
   - Chạy kiểm tra hiệu năng, an toàn đa luồng (thread-safety) và hành vi của Bot. Đạt kết quả tối đa (**PASS 100%**).
