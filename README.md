# Cờ Tướng AI - Xiangqi AI Game

> **Đồ án môn học:** Trí tuệ nhân tạo (HK2 - Năm học 2026–2027)  
> **Đơn vị đào tạo:** Đại học Sư Phạm Kỹ Thuật TP.HCM (HCMUTE)  
> **Giảng viên hướng dẫn:** TS. Phan Thị Huyền Trang  
> **Nhóm sinh viên thực hiện:** Nhóm 1 - Cờ tướng 6 level

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1-red)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## Thành viên nhóm

| Họ và Tên | Mã Sinh Viên | Liên hệ (Email) |
| :--- | :--- | :--- |
| Lương Viết Vĩ Đông | 24110202 | 24110202@student.hcmute.edu.vn |
| Trần Lê Thái | 24110331 | 24110331@student.hcmute.edu.vn |
| Nguyễn Minh Trí | 24110359 | 24110359@student.hcmute.edu.vn |

---

## Giới thiệu chung

**Cờ Tướng AI (Xiangqi AI)** là trò chơi cờ tướng ngoại tuyến được phát triển bằng ngôn ngữ **Python** và thư viện đồ họa **Pygame**. Trò chơi tích hợp công cụ AI thông minh hỗ trợ 6 cấp độ đối thủ máy từ cơ bản đến nâng cao, ứng dụng các lớp thuật toán tìm kiếm kinh điển và hiện đại trong Trí tuệ nhân tạo.

---

## Cấu trúc thư mục

```bash
chinese_chess/
├── ai/
│   ├── __init__.py           # Đăng ký và quản lý danh sách thuật toán AI
│   ├── eval.py               # Hàm lượng giá trạng thái bàn cờ (Heuristic evaluation)
│   ├── level1.py             # Bot cấp 1: BFS / DFS / UCS (Tìm kiếm mù)
│   ├── level2.py             # Bot cấp 2: Greedy / A* / IDA* (Tìm kiếm Heuristic)
│   ├── level3.py             # Bot cấp 3: Hill Climbing / Simulated Annealing / Local Beam Search
│   ├── level4.py             # Bot cấp 4: Online Search / AND-OR Search / Belief State Search
│   ├── level5.py             # Bot cấp 5: CSP (Constraint Satisfaction Problem với MRV & Min-Conflicts)
│   └── level6.py             # Bot cấp 6: Minimax kết hợp cắt tỉa đối kháng Alpha-Beta / Expectimax
├── game/
│   ├── board.py              # Xử lý logic bàn cờ, lịch sử nước đi, kiểm tra lặp trạng thái
│   ├── pieces.py             # Định nghĩa quân cờ và luật di chuyển pseudo-legal cho 7 quân cờ
│   └── rules.py              # Xác định trạng thái chiếu tướng (check), chiếu bí (mate), hết nước đi (stalemate)
├── gui/
│   ├── menu.py               # Giao diện Menu chính và màn hình chọn thuật toán AI
│   ├── renderer.py           # Vẽ bàn cờ, quân cờ (Hán tự/Latinh), các hiệu ứng gợi ý & chiếu tướng
│   ├── sidebar.py            # Bảng điều khiển bên phải (Xem lượt đi, hoàn nước, gợi ý)
│   └── sound.py              # Trình quản lý và tổng hợp âm thanh (di chuyển, ăn quân, chiếu tướng)
├── tests/
│   └── test_*.py             # Hệ thống unit test chi tiết kiểm thử TDD từng quân cờ và logic AI
├── docs/
│   ├── doc-for-human.md      # Nhật ký kiểm thử TDD và tài liệu cho lập trình viên
│   └── doc-for-agents        # Tài liệu hướng dẫn tích hợp dành cho AI Agents
├── image_readme/             # Thư mục chứa các ảnh chụp màn hình giới thiệu
├── main.py                   # Điểm khởi chạy chính của trò chơi (Pygame controller)
├── requirements.txt          # Danh sách thư viện phụ thuộc của dự án
└── README.md
```

---

## Các tính năng chính

- **2 Chế độ chơi linh hoạt**:
  - **Người đấu Bot (Human vs Bot)**: Người chơi (quân Đỏ) thi đấu với Bot AI (quân Đen) tự chọn.
  - **Bot đấu Bot (Bot vs Bot)**: Hai thuật toán AI tự động thi đấu đối đầu với nhau (hỗ trợ thanh trượt điều chỉnh tốc độ).
- **Hệ thống AI 6 cấp độ**: Tích hợp các thuật toán tìm kiếm đa dạng ứng với từng cấp độ khó.
- **Hoàn nước (Undo)**: Cho phép quay lại các nước đi trước đó (hoàn 2 nước trong Human vs Bot hoặc 1 nước trong Bot vs Bot).
- **Gợi ý nước đi (Hint)**: Hỗ trợ tìm kiếm nước đi tối ưu tức thời thông qua tìm kiếm Alpha-Beta độ sâu cao.
- **Đa luồng tính toán (Threading)**: Các thuật toán AI tính toán trên luồng nền giúp giao diện Pygame mượt mà, không bị đơ/treo.
- **Hiệu ứng & Âm thanh**:
  - Âm thanh sinh động tổng hợp trực tiếp bằng mã nguồn (Move, Capture, Check).
  - Tự động hiển thị chữ Hán cổ truyền hoặc ký tự Latin viết tắt tùy chỉnh.
  - Hiệu ứng phát sáng màu đỏ (glow) cảnh báo xung quanh tướng đang bị chiếu.

---

## Chi tiết 6 cấp độ AI

1. **Level 1: BFS / DFS / UCS**
   - Áp dụng các thuật toán tìm kiếm mù (Uninformed Search). UCS được tinh chỉnh để tối ưu hóa việc ăn các quân cờ lớn của đối phương.
2. **Level 2: Greedy / A\* / IDA\***
   - Áp dụng tìm kiếm Heuristic (Informed Search) đánh giá tổng lực đối thủ còn lại để tìm đường đi ngắn nhất đến chiến thắng.
3. **Level 3: Hill Climbing / SA / Beam**
   - Áp dụng thuật toán tìm kiếm cục bộ (Local Search). Trong đó Simulated Annealing (SA) chấp nhận các bước đi ngẫu nhiên dựa trên nhiệt độ để tránh tối ưu cục bộ.
4. **Level 4: Online / AND-OR / Belief**
   - Lập kế hoạch AND-OR đối phó với sự cố và môi trường không chắc chắn, duy trì tập trạng thái Belief.
5. **Level 5: CSP (MRV / Min-Conflicts)**
   - Mô hình hóa dưới dạng Bài toán thỏa mãn ràng buộc (Constraint Satisfaction Problem), né tránh các ô nguy hiểm và ưu tiên bảo vệ Tướng.
6. **Level 6: Minimax / Alpha-Beta**
   - Đối kháng chuyên sâu, dự đoán trước 4-6 nước đi tiếp theo kết hợp cắt tỉa Alpha-Beta tối ưu hóa không gian tìm kiếm.

---

## Giao diện ứng dụng

### 1. Menu chính & Lựa chọn chế độ chơi
Người chơi có thể lựa chọn chơi trực tiếp với máy tính (Người đấu Bot) hoặc quan sát hai thuật toán AI so tài với nhau (Bot đấu Bot).

![Menu chính](image_readme/menu_mode.png)

### 2. Chọn cấp độ đối thủ AI
Bảng lựa chọn 6 cấp độ AI tương ứng với các nhóm thuật toán học trên lớp.

![Màn hình chọn cấp độ](image_readme/menu_level.png)

### 3. Giao diện bàn cờ trò chơi
Bàn cờ cờ tướng 9x10 truyền thống trực quan, tích hợp bảng điều khiển thông minh bên phải để tương tác các tính năng phụ trợ (Undo, Hint, Reset).

![Bàn cờ](image_readme/game_board.png)

---

## Cài đặt và chạy dự án

### Yêu cầu hệ thống
* Python phiên bản 3.10 trở lên (khuyên dùng Python 3.13)
* Hệ điều hành: Windows, macOS hoặc Linux

### Hướng dẫn cài đặt

**Bước 1: Clone kho lưu trữ về máy**
```bash
git clone https://github.com/lwd7071/chinese_chess.git
cd chinese_chess
```

**Bước 2: Khởi tạo và kích hoạt môi trường ảo (khuyên dùng)**
* **Trên Windows (PowerShell)**:
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
* **Trên macOS/Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

**Bước 3: Cài đặt các thư viện cần thiết**
```bash
pip install -r requirements.txt
```

**Bước 4: Chạy ứng dụng**
```bash
python main.py
```

---

## Liên hệ
* **Giảng viên hướng dẫn**: TS. Phan Thị Huyền Trang
* **Sinh viên thực hiện**: Nhóm 1 - Cờ tướng 6 level (HCMUTE)
* **Kho lưu trữ chính**: https://github.com/lwd7071/chinese_chess


| Current Node (Node hiện tại) | Frontier (Hàng đợi ưu tiên - Sorted by Cost) | Explored (Tập đã duyệt) |
|----------|----------|----------|
| **Khởi tạo**<br>- Chưa chọn node nào. | **[n0]** (Trạng thái bắt đầu - Root)<br>- Tổng Cost: g(n₀) = 0 | {} |
| **Bước 1: Duyệt node n0**<br>- Đang xét: n0 (Lượt Đỏ)<br>- Phát triển các nước đi tiếp theo của Xe Đỏ:<br>&nbsp;&nbsp;• n1: Ăn Xe Đen tại (7,0), Cost = 100<br>&nbsp;&nbsp;• n2: Ăn Tốt Đen tại (9,1), Cost = 900<br>&nbsp;&nbsp;• n3: Đi ngang không ăn quân, Cost = 1000 | [n1 (Cost: 100), n2 (Cost: 900), n3 (Cost: 1000)]<br>(Hàng đợi tự động sắp xếp theo tổng chi phí tăng dần) | {n0} |
| **Bước 2: Lấy n1 ra khỏi Frontier**<br>- Đang xét: n1 (Lượt Đen phản công)<br>- Phát triển các nước đi tiếp theo của Đen từ n1:<br>&nbsp;&nbsp;• n4: Xe Đen tại (7,8) ăn Xe Đỏ vừa đi tới (7,0)<br>&nbsp;&nbsp;• Cost bước này = 100<br>&nbsp;&nbsp;• Tổng chi phí lũy kế: g(n₄) = 100 + 100 = 200 | [n4 (Cost: 200), n2 (Cost: 900), n3 (Cost: 1000)]<br>(Node n4 được đẩy vào và chen lên đầu vì chi phí lũy kế thấp hơn) | {n0, n1} |
| **Bước 3: Lấy n4 ra khỏi Frontier**<br>- Đang xét: n4 (Lượt Đỏ)<br>- Xe Đỏ đã bị tiêu diệt sau nước phản công của Đen.<br>- Nhánh này trở nên bất lợi nếu đánh giá sâu hơn. | [n2 (Cost: 900), n3 (Cost: 1000)] | {n0, n1, n4} |
| **Bước 4: Lấy n2 ra khỏi Frontier**<br>- Đang xét: n2 (Xe Đỏ ăn Tốt Đen an toàn)<br>- Chi phí ban đầu cao hơn nhánh n1.<br>- Tuy nhiên khi xét sâu hơn, nhánh này tránh được phản công mất Xe nên có thể trở thành phương án tối ưu hơn. | [n3 (Cost: 1000), ...] | {n0, n1, n4, n2} |