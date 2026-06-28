# Sửa hệ thống tọa độ: Giữ lại 2 cạnh (Dưới + Phải), Cột đánh từ Phải sang Trái (A→I)

## Bối cảnh

Hiện tại bàn cờ đang hiển thị tọa độ trên **cả 4 cạnh**:
- **Trên:** A B C D E F G H I (góc nhìn Đen)
- **Dưới:** I H G F E D C B A (góc nhìn Đỏ, đảo ngược)
- **Trái:** 0 1 2 3 4 5 6 7 8 9 (góc nhìn Đen)
- **Phải:** 9 8 7 6 5 4 3 2 1 0 (góc nhìn Đỏ, đảo ngược)

**Yêu cầu:** 
- Chỉ giữ lại **cạnh Dưới** và **cạnh Phải** (xóa cạnh Trên và cạnh Trái).
- Cột đánh từ **Phải sang Trái** (A B C D E F G H I) theo chuẩn truyền thống của cờ tướng (từ cánh phải của bên Đỏ).
- Hàng đánh từ **Trên xuống Dưới** (0 1 2 3 4 5 6 7 8 9).
- Thống nhất toàn bộ hệ thống sang **1 hệ tọa độ tuyệt đối duy nhất** này (không phân biệt Đen/Đỏ).

---

## Quy ước tọa độ thống nhất sau khi sửa

| Vị trí trên bàn cờ | Hiển thị | Mapping từ `(row, col)` nội bộ |
|---------------------|----------|--------------------------------|
| **Cạnh dưới** (cột) | A B C D E F G H I (từ phải sang trái) | `col=8` → `A`, `col=7` → `B` ... `col=0` → `I` |
| **Cạnh phải** (hàng) | 0 1 2 3 4 5 6 7 8 9 (từ trên xuống) | `row=0` → `0`, `row=1` → `1` ... `row=9` → `9` |

**Công thức Mapping:** `(row, col)` → `f"{chr(65 + (8 - col))}{row}"`

**Ví dụ thực tế:**
- Pháo đỏ ở `(7, 7)` → **B7** (cột B, hàng 7)
- Pháo đỏ ở `(7, 1)` → **H7** (cột H, hàng 7)
- Mã đen ở `(0, 7)` → **B0** (cột B, hàng 0)
- Mã đen ở `(0, 1)` → **H0** (cột H, hàng 0)
- Pháo H7→H0 ăn Mã = `(7, 1)→(0, 1)` → **H7→H0**

---

## Proposed Changes

### Component 1: Renderer — Vẽ tọa độ trên bàn cờ

#### [MODIFY] gui/renderer.py

Trong method `draw_coordinate_labels()` (dòng 417–462):

1. **Xóa phần vẽ cạnh Trên** (dòng 432–437): Xóa toàn bộ block vẽ `col_char_top`.
2. **Cạnh Dưới** (dòng 439–444): Vẫn giữ nguyên công thức hiện tại của Pygame vì nó đã đánh từ phải sang trái (`I` ở trái, `A` ở phải):
   ```python
   col_char_bottom = chr(65 + (8 - c))  # c=0 là I, c=8 là A (đúng chuẩn phải sang trái)
   ```
3. **Xóa phần vẽ cạnh Trái** (dòng 450–455): Xóa toàn bộ block vẽ `row_char_left`.
4. **Sửa cạnh Phải** (dòng 457–462): Đổi từ đảo ngược `9→0` thành thuận `0→9`:
   ```python
   # Cũ:  row_char_right = str(9 - r)
   # Mới: row_char_right = str(r)
   ```

---

### Component 2: Visualizer — Panel hiển thị thuật toán (Report Mode)

#### [MODIFY] gui/visualizer.py

**2a. Method `_pos_to_label_with_color()` (dòng 478–488):**  
Bỏ logic phân biệt `color`, áp dụng trọn vẹn công thức `8 - col` và `str(row)`:
```python
def _pos_to_label_with_color(self, pos, color):
    row, col = pos
    if 0 <= col < len(self.COL_LABELS) and 0 <= row <= 9:
        col_char = self.COL_LABELS[8 - col]   # A ở phải, I ở trái
        row_char = str(row)                   # 0 ở trên, 9 ở dưới
        return f"{col_char}{row_char}"
    return f"({row},{col})"
```

**2b. Class `EmojiSafeFont.clean_coordinates()` (dòng 164–204):**  
Bỏ logic phân biệt `color`, áp dụng chuẩn chung:
```python
# Cũ:  if color == "black": col_labels[col] / str(row)
#      else:                col_labels[8-col] / str(9-row)
# Mới: Luôn dùng col_labels[8 - col] và str(row)
```

---

### Component 3: Sidebar — Lịch sử nước đi

#### [MODIFY] gui/sidebar.py

Method `format_square()` (dòng 278–279):
```python
# Cũ:  return f"{chr(65 + pos[1])}{pos[0]}"
# Mới: return f"{chr(65 + (8 - pos[1]))}{pos[0]}"
```

---

### Component 4: Step Recorder — Hàm tiện ích tọa độ

#### [MODIFY] ai/step_recorder.py

Hàm `pos_to_label()` (dòng 21–28):
```python
# Cũ:  return f"{chr(65 + c)}{r}"
# Mới: return f"{chr(65 + (8 - c))}{r}"
```

---

### Component 5: AI Level modules — Chuỗi `explanation`

#### Các file: level1.py, level2.py, level3.py, level4.py, level5.py, level6.py

Các chuỗi `explanation` nhúng trực tiếp `{from_pos}→{to_pos}` (dạng tuple `(7,1)→(0,1)`).  
Class `EmojiSafeFont.clean_coordinates()` tự động chuyển `(r,c)` thành label khi render GUI.

> **Không cần sửa** các file AI. Chỉ cần `clean_coordinates()` ở Component 2b hoạt động đúng là toàn bộ explanation sẽ hiển thị đúng tọa độ mới.

---

## Tổng kết

| File | Thay đổi | Cần sửa? |
|------|----------|:--------:|
| `gui/renderer.py` | Xóa cạnh Trên + Trái, giữ cạnh Dưới (A ở phải), sửa cạnh Phải thành 0→9 | ✅ Có |
| `gui/visualizer.py` | Bỏ logic black/red, đồng bộ `col_labels[8-col]` và `str(row)` | ✅ Có |
| `gui/sidebar.py` | Sửa `format_square` sang `8 - pos[1]` | ✅ Có |
| `ai/step_recorder.py` | Sửa `pos_to_label` sang `8 - c` | ✅ Có |
| `ai/level*.py` | Tự động đúng nhờ `clean_coordinates()` | ❌ Không |

---

## Verification Plan

### Automated Tests
```powershell
python -m ruff check .
python run_evals.py
```

### Manual Verification
1. Chạy `python main.py` → kiểm tra bàn cờ chỉ có tọa độ ở **cạnh Dưới** (đánh từ phải sang trái A→I) và **cạnh Phải** (0→9).
2. Chế độ bot vs người → kiểm tra sidebar hiển thị đúng tọa độ lịch sử nước đi (ví dụ Pháo phải Đỏ đi đầu hiển thị B7).
3. Chế độ Report Mode → kiểm tra panel visualizer hiển thị tọa độ nhất quán.
4. Kiểm tra chuỗi explanation trong bảng visualizer không bị sai tọa độ.
