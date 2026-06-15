# Tài Liệu Giải Thuật Hệ Thống AI - Cờ Tướng AI

Tài liệu này giải thích chi tiết các thuật toán AI được tích hợp trong dự án, tương ứng từ **Level 1** đến **Level 6** trong thư mục [ai](file:///c:/Users/ADMIN/Documents/MyProject/chinese_chess/ai/).

---

## 📂 Tổng Quan Các Cấp Độ AI

Hệ thống AI được phân cấp để người dùng có thể so sánh hiệu quả giữa các lớp giải thuật khác nhau trong Khoa học Máy tính:

```
ai/
├── level1.py   # Uninformed Search (BFS, DFS, UCS)
├── level2.py   # Informed Search (Greedy, A*, IDA*)
├── level3.py   # Local Search (Hill Climbing, Simulated Annealing, Beam Search)
├── level4.py   # Search with Uncertainty (Online Search, AND-OR Search, Belief State)
├── level5.py   # Constraint Satisfaction Problems (Backtracking MRV, Min-Conflicts, AC-3)
└── level6.py   # Adversarial Search (Minimax, Alpha-Beta, Expectimax)
```

---

## 🤖 Chi Tiết Giải Thuật Từng Cấp Độ

### 🔴 Level 1: Uninformed Search (Tìm kiếm mù)
*Các giải thuật cơ bản không có thông tin về mục tiêu hay giá trị bàn cờ.*
1. **BFS (Breadth-First Search)**: Do giới hạn độ sâu là 1 lượt đi, thuật toán lấy nước đi đầu tiên trong danh sách các nước đi hợp lệ (`legal_moves[0]`).
2. **DFS (Depth-First Search)**: Tương tự như BFS nhưng lấy nước đi cuối cùng trong ngăn xếp các nước đi hợp lệ (`legal_moves[-1]`).
3. **UCS (Uniform Cost Search)**: Xác định chi phí của nước đi qua lượng giá quân bị ăn: `cost = 1000 - giá_trị_quân_bị_ăn`. Thuật toán chọn nước đi có chi phí thấp nhất (tương đương với việc ưu tiên ăn quân có giá trị cao nhất).

### 🟡 Level 2: Informed Search (Tìm kiếm có thông tin)
*Sử dụng tri thức hoặc hàm Heuristic để hướng dẫn quá trình tìm kiếm.*
1. **Greedy (Tìm kiếm tham lam)**: Duyệt qua toàn bộ nước đi hợp lệ, nếu có nước đi ăn quân, nó sẽ chọn ăn quân có giá trị lớn nhất trong `PIECE_VALUES` (Xe: 900, Pháo: 450, Mã: 300, v.v.). Nếu không có quân để ăn, nó sẽ chọn ngẫu nhiên.
2. **A\* Search**: Lượng giá nước đi bằng hàm $f(n) = g(n) + h(n)$:
   - Chi phí thực tế $g(n) = 1000 - \text{giá trị quân ăn được}$.
   - Ước lượng tương lai $h(n) = \text{tổng giá trị các quân còn lại của đối thủ}$.
   AI sẽ chọn nước đi tối thiểu hóa hàm $f(n)$.
3. **IDA\* (Iterative Deepening A\*)**: Thực hiện tìm kiếm A\* giới hạn theo ngưỡng chi phí $f$, tăng dần ngưỡng sau mỗi vòng lặp để tìm kiếm sâu hơn mà không tiêu tốn quá nhiều bộ nhớ.

### 🟢 Level 3: Local Search (Tìm kiếm cục bộ)
*Tập trung vào tối ưu hóa trạng thái hiện tại thay vì tìm đường đi từ gốc.*
1. **Hill Climbing (Leo đồi)**: Đánh giá tất cả các trạng thái bàn cờ đạt được sau 1 nước đi bằng hàm [evaluate_board](file:///c:/Users/ADMIN/Documents/MyProject/chinese_chess/ai/eval.py#L87), sau đó chọn nước đi dẫn tới trạng thái có điểm số cao nhất.
2. **Simulated Annealing (Luyện kim giả lập)**: Chọn nước đi ngẫu nhiên. Nếu tốt hơn nước đi hiện tại, nó sẽ chấp nhận. Nếu tệ hơn, nó vẫn có khả năng chấp nhận dựa trên xác suất Boltzmann $e^{\Delta / T}$ (với $T$ giảm dần theo thời gian). Giúp AI thoát khỏi các cực trị cục bộ.
3. **Local Beam Search (Tìm kiếm chùm tia cục bộ)**: Giữ lại $k$ nước đi tốt nhất ở lượt này, sau đó đánh giá phản ứng tốt nhất của đối thủ đối với từng nước đi đó, chọn nước đi có kết quả an toàn nhất ở lượt sau (Minimax chùm tia).

### 🔵 Level 4: Search with Uncertainty (Tìm kiếm trong môi trường bất định)
*Mô phỏng việc đưa ra quyết định khi không chắc chắn về môi trường hoặc chiến thuật đối thủ.*
1. **Online Search (Tìm kiếm trực tuyến)**: Điều chỉnh động trọng số giá trị các quân cờ tùy thuộc vào tình trạng bàn cờ. Nếu Tướng đang bị chiếu (`is_in_check`), AI tăng trọng số quân Sĩ/Tượng lên cao để ưu tiên phòng thủ. Ngược lại, nó tăng trọng số các quân Xe/Pháo/Mã để tấn công mạnh mẽ hơn.
2. **AND-OR Search**: Xem các nước đi của mình là các nhánh lựa chọn (OR), và các phản ứng của đối thủ là các trường hợp phải vượt qua (AND). AI chọn nước đi đảm bảo điểm số tối thiểu tốt nhất sau khi đối thủ phản hồi.
3. **Belief State Search**: Duy trì một phân phối xác suất về lối chơi của đối thủ (Tấn công, Phòng thủ, hay Kiểm soát không gian) dựa trên lịch sử đi quân gần nhất, sau đó chọn nước đi tối ưu hóa giá trị kỳ vọng trên phân phối đó.

### 🟣 Level 5: Constraint Satisfaction Problems (CSP - Thỏa mãn ràng buộc)
*Giải quyết bài toán bằng cách coi các quân cờ là biến và các vị trí đi quân là miền giá trị bị ràng buộc.*
1. **Backtracking với MRV (Minimum Remaining Values)**: Lựa chọn quân cờ có số lượng nước đi hợp lệ ít nhất (biến bị ràng buộc nhiều nhất) để đi trước, nhằm thu hẹp không gian bài toán nhanh nhất.
2. **Min-Conflicts**: Lựa chọn nước đi làm giảm thiểu tối đa số lượng quân cờ của phe mình đang bị đối thủ đe dọa (giảm xung đột trực tiếp).
3. **AC-3 (Arc Consistency)**: Lọc bỏ các nước đi không nhất quán (ví dụ: đi Xe vào ô bị tốt đối thủ canh giữ mà không có quân bảo vệ - trao đổi không an toàn). Chọn nước đi tốt nhất trong số các nước đi an toàn còn lại.

### 🟤 Level 6: Adversarial Search (Tìm kiếm đối kháng)
*Các thuật toán đỉnh cao mô phỏng trò chơi cờ giữa hai đối thủ thông minh.*
1. **Minimax**: Tìm kiếm duyệt cây trò chơi ở độ sâu xác định (mặc định là 3), giả định đối thủ luôn đi nước đi tối ưu nhất để giảm thiểu điểm số của mình.
2. **Alpha-Beta Pruning**: Tối ưu hóa Minimax bằng cách cắt bỏ các nhánh tìm kiếm chắc chắn không ảnh hưởng đến kết quả cuối cùng nhờ hai biến giới hạn `alpha` (điểm tối thiểu bên MAX được đảm bảo) và `beta` (điểm tối đa bên MIN được đảm bảo). Cho phép tìm kiếm sâu hơn (độ sâu 4).
3. **Expectimax**: Thay thế các nút MIN của đối thủ bằng nút Chance (cơ hội). Giả định đối thủ chơi tối ưu với xác suất 70%, và đi ngẫu nhiên với xác suất 30%, tính toán giá trị kỳ vọng để đưa ra nước đi tốt nhất.

---

## 📈 Hàm Lượng Giá Bàn Cờ (Evaluation Function)

Hàm lượng giá nằm ở [eval.py](file:///c:/Users/ADMIN/Documents/MyProject/chinese_chess/ai/eval.py) tính toán điểm số bàn cờ từ góc nhìn của quân Đỏ:
$$\text{Score} = (\text{Material}_{\text{Red}} + \text{Positional}_{\text{Red}}) - (\text{Material}_{\text{Black}} + \text{Positional}_{\text{Black}})$$

- **Material (Giá trị quân cờ)**: Tướng (10000), Xe (900), Pháo (450), Mã (300), Sĩ/Tượng (200), Tốt (100).
- **Positional (Vị trí)**: Sử dụng bảng vị trí **PST (Piece-Square Tables)** để khuyến khích:
  - Tốt tiến sâu vào sân đối phương và chiếm trung lộ.
  - Mã đi vào trung tâm, tránh rìa bàn cờ.
  - Pháo đứng ở các hàng phòng thủ hoặc trung lộ để làm ngòi.
  - Xe chiếm các hàng/cột mở thông thoáng.
  - Sĩ/Tượng bảo vệ cung Tướng.
