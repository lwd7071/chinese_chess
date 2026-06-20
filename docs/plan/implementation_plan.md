# Kế Hoạch Triển Khai: Sửa Lỗi Logic Expectimax (ai/level6.py)

Tài liệu này trình bày kế hoạch chi tiết nhằm sửa lỗi logic của thuật toán Expectimax trong tệp [level6.py](file:///c:/Users/ADMIN/Documents/MyProject/chinese_chess/ai/level6.py) để AI hoạt động chính xác khi cầm quân Đen (Black).

---

## 📊 Đánh Giá & Đánh Giá Độ Phức Tạp (Self-Rating & Impact Assessment)

- **Độ phức tạp (Complexity)**: **Thấp - Trung bình (Low-Medium)**
  - Thay đổi tập trung vào duy nhất một hàm `expectimax_move` và hàm tìm kiếm đệ quy nội bộ `search`.
- **Rủi ro ảnh hưởng (Risk of Regression)**: **Thấp (Low)**
  - Các thay đổi chỉ tác động đến giải thuật **Expectimax Bot** (Level 6). Các thuật toán khác như Minimax, Alpha-Beta hay các thuật toán tìm kiếm cấp thấp hoàn toàn độc lập và không bị ảnh hưởng.
- **Thời gian ước lượng (Estimated Effort)**: **15 - 30 phút**
  - Bao gồm thời gian chỉnh sửa mã nguồn và chạy thử nghiệm đối chiếu giữa các chế độ chơi.

---

## 🔍 Phân Tích Lỗi Hiện Tại & Giải Pháp

### Vấn đề hiện tại:
Hàm `expectimax_move` đang giả định cố định:
- Nút **MAX** luôn thuộc về quân Đỏ (Red).
- Nút **Chance** (tính trung bình cộng có trọng số) luôn thuộc về quân Đen (Black).
- Trình tự sắp xếp danh sách kết quả `results.sort()` luôn giả định đối thủ muốn giảm thiểu điểm số (tối thiểu hóa), tức là sắp xếp tăng dần để lấy nước đi tệ nhất cho Red ở `results[0]`.

Điều này khiến cho khi AI cầm quân Đen (Black), nó tự coi lượt của mình là Chance Node (đi ngẫu nhiên 30%) và lượt của đối phương (Red) là nút tối ưu tuyệt đối, dẫn đến các nước đi tự sát hoặc thiếu logic của quân Đen.

### Giải pháp sửa đổi:
1. **Lưu trữ màu quân của AI**: Lưu `ai_color = board.turn` từ đầu hàm.
2. **Đổi tham số đệ quy**: Thay đổi hàm `search(b, d, is_max)` thành `search(b, d, is_ai_turn)`.
3. **Quyết định nút tối ưu động**:
   - Nếu là lượt của AI (`is_ai_turn == True`):
     - Nếu `ai_color == 'red'`: Sử dụng chiến thuật **MAX** (tối đa hóa điểm số).
     - Nếu `ai_color == 'black'`: Sử dụng chiến thuật **MIN** (tối thiểu hóa điểm số).
   - Nếu là lượt của đối thủ (`is_ai_turn == False`): Đây là nút **Chance**.
4. **Tính toán giá trị kỳ vọng động**:
   - Sau khi gọi đệ quy các nước đi của đối thủ và lưu điểm số vào `results`:
     - Nếu đối thủ là quân Đen (`ai_color == 'red'`): Đối thủ muốn giảm thiểu điểm số $\rightarrow$ Sắp xếp tăng dần (`results.sort()`) để phần tử `results[0]` là nước đi tốt nhất của đối thủ (tệ nhất cho Red).
     - Nếu đối thủ là quân Đỏ (`ai_color == 'black'`): Đối thủ muốn tối đa hóa điểm số $\rightarrow$ Sắp xếp giảm dần (`results.sort(reverse=True)`) để phần tử `results[0]` là nước đi tốt nhất của đối thủ (cao nhất cho Red).
5. **Cập nhật điều kiện biên**:
   - Khi không còn nước đi hợp lệ (`not moves`):
     - Nếu đang ở lượt của AI (`b.turn == ai_color`): AI đã thua $\rightarrow$ Trả về `-inf` nếu AI là Red, `inf` nếu AI là Black.
     - Nếu đang ở lượt của đối thủ (`b.turn != ai_color`): Đối thủ đã thua (AI thắng) $\rightarrow$ Trả về `inf` nếu AI là Red, `-inf` nếu AI là Black.

---

## 🛠️ Chi Tiết Thay Đổi Mã Nguồn

### Tệp tin: [level6.py](file:///c:/Users/ADMIN/Documents/MyProject/chinese_chess/ai/level6.py)

#### [MODIFY] `expectimax_move`

```python
def expectimax_move(board, depth=3):
    """
    Expectimax Search:
    Assumes opponent does not play fully optimally, but has:
    - 70% chance of making the best minimax move.
    - 30% chance of making a random move.
    We compute expected values at opponent's nodes (Chance nodes).
    """
    ai_color = board.turn
    legal_moves = board.get_all_legal_moves(ai_color)
    if not legal_moves:
        return None
        
    sorted_moves = sort_moves(board, legal_moves)
    best_move = sorted_moves[0]
    best_score = float('-inf') if ai_color == 'red' else float('inf')
    
    start_time = time.time()
    
    def search(b, d, is_ai_turn):
        if d == 0 or time.time() - start_time > 1.2:
            return evaluate_board(b)
            
        moves = b.get_all_legal_moves(b.turn)
        if not moves:
            # The player whose turn it is has lost
            if b.turn == ai_color:
                return float('-inf') if ai_color == 'red' else float('inf')
            else:
                return float('inf') if ai_color == 'red' else float('-inf')
            
        ordered = sort_moves(b, moves)[:10]
        
        if is_ai_turn:
            # AI's turn: Optimize based on AI's color
            if ai_color == 'red':
                # Red AI maximizes
                max_val = float('-inf')
                for m in ordered:
                    b.make_move(m[0], m[1])
                    val = search(b, d - 1, False)
                    b.undo_move()
                    max_val = max(max_val, val)
                return max_val
            else:
                # Black AI minimizes
                min_val = float('inf')
                for m in ordered:
                    b.make_move(m[0], m[1])
                    val = search(b, d - 1, False)
                    b.undo_move()
                    min_val = min(min_val, val)
                return min_val
        else:
            # Opponent's turn: Chance node
            results = []
            for m in ordered:
                b.make_move(m[0], m[1])
                val = search(b, d - 1, True)
                b.undo_move()
                results.append(val)
                
            num_moves = len(results)
            if num_moves == 1:
                return results[0]
                
            # If opponent is Black (AI is Red), opponent minimizes -> sort ascending
            # If opponent is Red (AI is Black), opponent maximizes -> sort descending
            if ai_color == 'red':
                results.sort()
            else:
                results.sort(reverse=True)
                
            best_res = results[0]
            others_avg = sum(results[1:]) / (num_moves - 1)
            
            expected_val = 0.7 * best_res + 0.3 * others_avg
            return expected_val

    # Root call (AI's first moves)
    for m in sorted_moves[:12]:
        board.make_move(m[0], m[1])
        score = search(board, depth - 1, False) # Next turn is opponent's (Chance)
        board.undo_move()
        
        if ai_color == 'red':
            if score > best_score:
                best_score = score
                best_move = m
        else: # Black
            if score < best_score:
                best_score = score
                best_move = m
                
    return best_move
```

---

## 📈 Kế Hoạch Xác Minh (Verification Plan)

### Kiểm thử thủ công:
1. Chạy trò chơi: `python main.py`
2. Chọn chế độ chơi **Người vs Máy (Human vs Bot)**:
   - Cấu hình AI cầm quân Đen (Black) dùng thuật toán **Expectimax**.
   - Người chơi cầm quân Đỏ đi thử một vài nước.
   - Kiểm tra xem AI quân Đen có đưa ra nước đi phòng thủ / tấn công hợp lý và bảo vệ Tướng chính xác hay không.
3. Chọn chế độ chơi **Máy vs Máy (Bot vs Bot)**:
   - Cấu hình quân Đen dùng **Expectimax**, quân Đỏ dùng **Alpha-Beta**.
   - Quan sát trận đấu diễn ra để đảm bảo quân Đen chơi phòng thủ, ăn quân tối ưu và không có hành vi tự sát.
