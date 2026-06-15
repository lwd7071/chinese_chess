# Cờ Tướng AI - Xiangqi AI Game Dashboard

Dự án phát triển trò chơi Cờ Tướng (Xiangqi) tích hợp giao diện người dùng bằng **Pygame** và hệ thống AI mô phỏng nhiều thuật toán tìm kiếm và giải quyết vấn đề kinh điển trong Khoa học Máy tính.

---

## 👥 Nhóm Phát Triển (Authors)
* **Trần Lê Thái**
* **Nguyễn Minh Trí**
* **Lương Viết Vĩ Đông**

---

## 🎮 Các Tính Năng Chính
1. **Chế độ chơi đa dạng**:
   - **Người vs Máy (Human vs Bot)**: Người chơi cầm quân Đỏ đấu với thuật toán AI cầm quân Đen.
   - **Máy vs Máy (Bot vs Bot)**: Cho phép chọn hai thuật toán AI khác nhau để tự động thi đấu và so tài với nhau (có thanh trượt điều chỉnh tốc độ đi quân).
2. **Hệ thống AI đa cấp độ (Level 1 - Level 6)**:
   - **Level 1 (Uninformed Search)**: BFS, DFS, UCS.
   - **Level 2 (Informed Search)**: Greedy, A*, IDA*.
   - **Level 3 (Local Search)**: Hill Climbing, Simulated Annealing, Beam Search.
   - **Level 4 (Search with Uncertainty)**: Online Search, AND-OR Search, Belief State.
   - **Level 5 (Constraint Satisfaction - CSP)**: Backtracking (MRV), Min-Conflicts, AC-3.
   - **Level 6 (Adversarial Search)**: Minimax, Alpha-Beta, Expectimax.
3. **Hiệu ứng âm thanh & hình ảnh**:
   - Tự động phát hiện và hỗ trợ hiển thị chữ Hán cổ truyền trên quân cờ (nếu máy có font tương thích) hoặc ký tự Latinh viết tắt.
   - Âm thanh được tổng hợp trực tiếp bằng chương trình (di chuyển, ăn quân, chiếu tướng) mượt mà bằng thư viện `numpy` hoặc fallback bằng tiếng `beep` của hệ thống.
   - Hiệu ứng phát sáng màu đỏ xung quanh tướng khi bị chiếu tướng và chỉ dẫn các nước đi hợp lệ.

---

## 🛠️ Yêu Cầu Hệ Thống & Cài Đặt

### 1. Tạo Môi Trường Ảo (Virtual Environment)
Mở terminal tại thư mục gốc của dự án và chạy lệnh:
```bash
python -m venv venv
```

### 2. Kích Hoạt Môi Trường Ảo
- **Trên Windows (PowerShell)**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Trên Windows (Command Prompt - CMD)**:
  ```cmd
  .\venv\Scripts\activate.bat
  ```
- **Trên Windows (Git Bash / Bash)**:
  ```bash
  source venv/Scripts/activate
  ```
- **Trên macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 3. Cài Đặt Các Thư Viện Cần Thiết
Kích hoạt môi trường ảo xong, chạy lệnh cài đặt:
```bash
pip install -r requirements.txt
```

---

## 🚀 Cách Chạy Trò Chơi
Sau khi đã hoàn tất các bước trên, khởi chạy trò chơi bằng lệnh:
```bash
python main.py
```
Giao diện Menu chính sẽ hiện lên để bạn chọn chế độ chơi (Human vs Bot hoặc Bot vs Bot), lựa chọn thuật toán AI tương ứng cho từng bên, sau đó bấm **BẮT ĐẦU** để chơi.

---

## 📁 Cấu Trúc Thư Mục Dự Án
- `main.py`: Tệp khởi chạy chính của trò chơi (điều phối Game Loop, GUI và luồng tính toán AI).
- `game/`: Định nghĩa bàn cờ (`board.py`), các quân cờ (`pieces.py`) và luật chơi cờ tướng (`rules.py`).
- `gui/`: Xử lý giao diện đồ họa (`renderer.py`), thanh menu điều khiển (`sidebar.py`, `menu.py`) và âm thanh (`sound.py`).
- `ai/`: Chứa các thuật toán AI phân loại theo các cấp độ từ Level 1 đến Level 6 và hàm lượng giá bàn cờ (`eval.py`).
- `requirements.txt`: Danh sách các thư viện phụ thuộc (`pygame`, `numpy`).
- `.gitignore`: Cấu hình bỏ qua các tệp không cần thiết khi đẩy lên Git (venv, pycache, v.v.).
