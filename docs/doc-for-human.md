# Nhật ký Kiểm thử TDD - Quân Xe (Rook), Quân Mã (Horse), Quân Tượng (Elephant), Quân Pháo (Cannon) & Quân Sĩ (Advisor)

Tài liệu này ghi lại quá trình kiểm thử TDD cho logic di chuyển của quân Xe (`R`) trong game cờ tướng.

## Mục tiêu kiểm thử
Đảm bảo quân Xe di chuyển đúng luật cờ tướng:
1. Đi thẳng, đi ngang không giới hạn số ô trên bàn cờ 9x10 trống.
2. Bị chặn bởi quân mình (đồng minh) và không được đi vượt qua quân đó.
3. Có thể ăn quân đối phương đứng trên đường đi thẳng/ngang, nhưng không được đi tiếp qua quân đối phương đó.

---

## Nhật ký tiến trình

### Khởi đầu (2026-06-20)
- Thiết lập kế hoạch TDD và chuẩn bị môi trường kiểm thử bằng `unittest`.
- Chuẩn bị file test `tests/test_rook.py`.
- **Trạng thái:** Đã hoàn thành toàn bộ 4 Test Case cho quân Xe.

### Nhật ký chi tiết:
1. **Test Case 1: Di chuyển trên bàn cờ trống**
   - **Mục tiêu:** Quân Xe tại `(4, 4)` trên bàn cờ trống phải đi được đến 17 ô hợp lệ.
   - **Kết quả:** Đã chạy unit test thành công. Code hiện tại xử lý chính xác việc đi thẳng và đi ngang không bị cản trở trên bàn cờ trống.

2. **Test Case 2: Bị cản bởi quân đồng minh**
   - **Mục tiêu:** Quân Xe đỏ tại `(9, 0)` bị cản bởi quân đỏ khác tại `(7, 0)`. Xe không được đi tới hoặc vượt qua `(7, 0)`.
   - **Kết quả:** Đã chạy unit test thành công. Quân Xe bị chặn đúng quy định và chỉ di chuyển tối đa tới `(8, 0)` ở cột dọc đó.

3. **Test Case 3: Ăn quân đối phương**
   - **Mục tiêu:** Quân Xe đỏ tại `(9, 0)` ăn quân đen tại `(7, 0)`. Xe được phép di chuyển tới `(8, 0)` và `(7, 0)` để ăn quân, nhưng không được đi tiếp qua `(7, 0)` (ví dụ `(6, 0)`).
   - **Kết quả:** Đã chạy unit test thành công. Xe ăn quân đối phương chính xác và dừng lại đúng ô của quân đối phương bị ăn.

4. **Test Case 4: Di chuyển ngang bị cản và ăn quân**
   - **Mục tiêu:** Quân Xe đỏ tại `(4, 4)` bị cản bởi quân đỏ khác tại `(4, 2)` (bên trái) và quân đối phương tại `(4, 7)` (bên phải). Xe chỉ được di chuyển ngang tới `(4, 3)` (bên trái) và `(4, 5), (4, 6), (4, 7)` (bên phải - ăn quân tại đây và dừng lại).
   - **Kết quả:** Đã chạy unit test thành công. Logic di chuyển ngang của quân Xe hoạt động chính xác với cả cản đồng minh lẫn ăn quân đối phương.

---

# Nhật ký Kiểm thử TDD - Quân Mã (Horse)

Tài liệu này ghi lại quá trình kiểm thử TDD cho logic di chuyển của quân Mã (`H`), đặc biệt là luật cản chân Mã.

## Mục tiêu kiểm thử
Đảm bảo quân Mã di chuyển đúng luật cờ tướng:
1. Di chuyển theo hình chữ L (đi thẳng/ngang 2 ô rồi rẽ ngang/dọc 1 ô) trên bàn cờ trống (tối đa 8 nước đi).
2. Luật cản chân Mã (bị chặn ở ô ngay sát bên cạnh theo hướng đi 2 ô) làm mất đi 2 nước đi tương ứng theo hướng đó.
3. Có thể ăn quân đối phương tại ô mục tiêu nếu đường đi không bị cản chân.
4. Xử lý chính xác các trường hợp biên bàn cờ (ví dụ ở góc/biên thì số nước đi hợp lệ bị giới hạn).

- **Trạng thái:** Đã hoàn thành toàn bộ 4 Test Case cho quân Mã.

### Nhật ký chi tiết:
1. **Test Case 1: Di chuyển trên bàn cờ trống**
   - **Mục tiêu:** Quân Mã tại `(4, 4)` trên bàn cờ trống phải đi được đúng 8 ô hình chữ L tương ứng.
   - **Kết quả:** Đã chạy unit test thành công. Code hiện tại xác định chính xác các nước đi L-shape từ tâm bàn cờ trống.

2. **Test Case 2: Bị cản chân Mã bởi quân đồng minh**
   - **Mục tiêu:** Quân Mã tại `(4, 4)` bị cản ở ô chân phía trên `(3, 4)`. Mã không được đi tới 2 ô mục tiêu dọc phía trên là `(2, 3)` và `(2, 5)`.
   - **Kết quả:** Đã chạy unit test thành công. Mã bị cản chân đúng quy luật cờ tướng và chỉ còn 6 nước đi hợp lệ.

3. **Test Case 3: Ăn quân đối phương**
   - **Mục tiêu:** Quân Mã tại `(4, 4)` ăn quân đối phương tại ô mục tiêu `(2, 3)` mà chân Mã `(3, 4)` không bị cản.
   - **Kết quả:** Đã chạy unit test thành công. Mã có thể nhảy đến ô mục tiêu chứa quân đối phương để ăn quân bình thường.

4. **Test Case 4: Kiểm thử ở góc/biên và cản chân phức tạp**
   - **Mục tiêu:** Quân Mã tại `(9, 1)` (gần góc bàn cờ) trên bàn cờ trống chỉ có 3 nước đi hợp lệ do giới hạn biên. Sau khi đặt quân cản chân tại `(8, 1)`, Mã chỉ còn duy nhất 1 nước đi hợp lệ tới `(8, 3)`.
   - **Kết quả:** Đã chạy unit test thành công. Code xử lý biên bàn cờ cực tốt và phản ứng cản chân chính xác trong các tình huống thực tế.

---

# Nhật ký Kiểm thử TDD - Quân Tượng (Elephant)

Tài liệu này ghi lại quá trình kiểm thử TDD cho logic di chuyển của quân Tượng (`E`), bao gồm cả luật không qua sông và luật cản mắt Tượng.

## Mục tiêu kiểm thử
Đảm bảo quân Tượng di chuyển đúng luật cờ tướng:
1. Di chuyển chéo chính xác 2 ô trên bàn cờ trống (tối đa 4 nước đi khi ở trung tâm).
2. Luật cản mắt Tượng (bị chặn ở ô chéo sát bên cạnh 1 bước) làm mất nước đi chéo tương ứng.
3. Không bao giờ được đi qua sông (chỉ hoạt động bên nửa sân nhà).
4. Có thể ăn quân đối phương tại ô mục tiêu chéo 2 bước nếu không bị cản mắt.

## Nhật ký tiến trình

- **Trạng thái:** Đã hoàn thành toàn bộ 4 Test Case cho quân Tượng.

### Nhật ký chi tiết:
1. **Test Case 1: Di chuyển trên bàn cờ trống**
   - **Mục tiêu:** Quân Tượng đỏ tại `(7, 4)` trên bàn cờ trống phải đi được đúng 4 ô chéo 2 bước.
   - **Kết quả:** Đã chạy unit test thành công. Code hiện tại xác định chính xác 4 nước đi chéo hợp lệ trong sân nhà.

2. **Test Case 2: Bị cản mắt Tượng bởi quân đồng minh**
   - **Mục tiêu:** Quân Tượng đỏ tại `(7, 4)` bị cản ở ô mắt Tượng `(8, 3)`. Tượng không được phép đi tới ô mục tiêu chéo dưới bên trái là `(9, 2)`.
   - **Kết quả:** Đã chạy unit test thành công. Tượng bị cản mắt đúng quy định và chỉ còn 3 nước đi hợp lệ.

3. **Test Case 3: Không được phép đi qua sông**
   - **Mục tiêu:** Quân Tượng đỏ tại `(5, 2)` (sát sông) không được di chuyển chéo qua sông tới `(3, 0)` hoặc `(3, 4)`. Chỉ được đi chéo lùi lại `(7, 0)` hoặc `(7, 4)`.
   - **Kết quả:** Đã chạy unit test thành công. Tượng đỏ bị giới hạn đúng trong nửa bàn cờ của mình (dòng 5 đến 9).

4. **Test Case 4: Ăn quân đối phương**
   - **Mục tiêu:** Quân Tượng đỏ tại `(7, 4)` ăn quân đối phương tại ô mục tiêu chéo `(9, 2)`. Mắt tượng `(8, 3)` trống.
   - **Kết quả:** Đã chạy unit test thành công. Tượng ăn quân đối phương chéo 2 bước thành công khi không bị cản mắt.

---

# Nhật ký Kiểm thử TDD - Quân Pháo (Cannon)

Tài liệu này ghi lại quá trình kiểm thử TDD cho logic di chuyển của quân Pháo (`C`), bao gồm cả luật di chuyển trượt không cản và luật ăn quân nhảy qua đúng 1 ngòi.

## Mục tiêu kiểm thử
Đảm bảo quân Pháo di chuyển đúng luật cờ tướng:
1. Di chuyển dọc/ngang không giới hạn ô trên bàn cờ trống giống quân Xe (không ngòi).
2. Di chuyển thường bị chặn bởi quân khác dọc đường đi (không thể đi qua hay đi tới ô đó).
3. Để ăn quân đối phương, phải đi dọc/ngang nhảy qua đúng 1 quân bất kỳ làm ngòi (và không được nhảy tới ô trống phía sau ngòi).
4. Không được phép ăn quân đối phương nếu không có ngòi hoặc có từ 2 ngòi trở lên.

## Nhật ký tiến trình

- **Trạng thái:** Đã hoàn thành toàn bộ 4 Test Case cho quân Pháo.

### Nhật ký chi tiết:
1. **Test Case 1: Di chuyển trên bàn cờ trống**
   - **Mục tiêu:** Quân Pháo tại `(4, 4)` trên bàn cờ trống đi được đúng 17 ô dọc và ngang.
   - **Kết quả:** Đã chạy unit test thành công. Code hiện tại xác định chính xác các nước đi thẳng và ngang không có ngòi.

2. **Test Case 2: Bị chặn di chuyển thường**
   - **Mục tiêu:** Đặt Pháo đỏ tại `(4, 4)` và quân đồng minh tại `(4, 2)`. Pháo chỉ được đi thường tới `(4, 3)` bên trái, không đi tới hoặc vượt qua `(4, 2)`.
   - **Kết quả:** Đã chạy unit test thành công. Pháo bị chặn đúng quy định khi di chuyển bình thường.

3. **Test Case 3: Ăn quân đối phương khi có đúng 1 quân làm ngòi**
   - **Mục tiêu:** Đặt Pháo đỏ tại `(4, 4)`, quân ngòi đồng minh tại `(4, 2)` và quân đối phương tại `(4, 0)`. Pháo đỏ được phép di chuyển tới `(4, 0)` để ăn quân, nhưng không được nhảy tới ô trống `(4, 1)`.
   - **Kết quả:** Đã chạy unit test thành công. Pháo nhảy ăn quân đối phương chính xác và không nhảy vào các ô trống sau ngòi.

4. **Test Case 4: Không được ăn quân khi không có ngòi hoặc có từ 2 ngòi trở lên**
   - **Mục tiêu:** 
     - Không ngòi: Pháo đỏ `(4, 4)` đối mặt với đen `(4, 2)` không được ăn quân đen.
     - Nhiều ngòi: Có hai quân cản trở `(4, 3)` và `(4, 2)` giữa Pháo đỏ `(4, 4)` và quân đen `(4, 0)`. Pháo đỏ không được nhảy ăn đen `(4, 0)`.
   - **Kết quả:** Đã chạy unit test thành công. Pháo kiểm soát số lượng ngòi nhảy ăn quân vô cùng chính xác theo luật cờ tướng.

---

# Nhật ký Kiểm thử TDD - Quân Sĩ (Advisor)

Tài liệu này ghi lại quá trình kiểm thử TDD cho logic di chuyển của quân Sĩ (`A`), bao gồm cả luật di chuyển chéo 1 bước và giới hạn trong Cung cấm.

## Mục tiêu kiểm thử
Đảm bảo quân Sĩ di chuyển đúng luật cờ tướng:
1. Di chuyển chéo chính xác 1 bước trên bàn cờ trống.
2. Tuyệt đối không di chuyển ra ngoài phạm vi Cung cấm (Palace).
3. Bị chặn bởi quân đồng minh tại ô mục tiêu chéo.
4. Có thể ăn quân đối phương đứng tại ô chéo trong Cung cấm.

## Nhật ký tiến trình

- **Trạng thái:** Đã hoàn thành toàn bộ 4 Test Case cho quân Sĩ.

### Nhật ký chi tiết:
1. **Test Case 1: Di chuyển từ tâm Cung cấm trên bàn cờ trống**
   - **Mục tiêu:** Quân Sĩ đỏ tại trung tâm Cung cấm `(8, 4)` trên bàn cờ trống phải đi được đúng 4 góc Cung cấm.
   - **Kết quả:** Đã chạy unit test thành công. Code hiện tại xác định chính xác các nước đi chéo 1 bước từ trung tâm.

2. **Test Case 2: Di chuyển từ góc Cung cấm (Giới hạn phạm vi)**
   - **Mục tiêu:** Quân Sĩ đỏ tại góc `(9, 3)` chỉ được phép di chuyển chéo vào tâm `(8, 4)`. Các ô chéo khác nằm ngoài Cung cấm phải bị loại bỏ.
   - **Kết quả:** Đã chạy unit test thành công. Sĩ được giới hạn đúng 100% trong Cung cấm.

3. **Test Case 3: Bị chặn di chuyển bởi quân đồng minh**
   - **Mục tiêu:** Quân Sĩ đỏ tại `(8, 4)` bị cản bởi quân đỏ tại góc `(7, 3)`. Sĩ không được phép di chuyển tới `(7, 3)`.
   - **Kết quả:** Đã chạy unit test thành công. Sĩ đỏ bị chặn bởi quân đồng minh chính xác.

4. **Test Case 4: Ăn quân đối phương**
   - **Mục tiêu:** Quân Sĩ đỏ tại `(8, 4)` ăn quân đối phương (Đen) đứng tại `(7, 3)`. Sĩ được di chuyển đến ô `(7, 3)` để ăn quân, và vẫn có đầy đủ các nước đi hợp lệ khác chéo 1 bước tới `(7, 5), (9, 3), (9, 5)`.
   - **Kết quả:** Đã chạy unit test thành công. Sĩ ăn quân đối phương chính xác trong phạm vi Cung cấm.

---

# Nhật ký Kiểm thử TDD - Quân Tốt / Chốt (Pawn)

Tài liệu này ghi lại quá trình kiểm thử TDD cho logic di chuyển của quân Tốt / Chốt (`P`), bao gồm di chuyển tiến thẳng trước sông và di chuyển ngang/dọc sau sông.

## Mục tiêu kiểm thử
Đảm bảo quân Tốt di chuyển đúng luật cờ tướng:
1. Di chuyển tiến thẳng 1 bước khi chưa qua sông (đối với đỏ là đi lên r giảm, đối với đen là đi xuống r tăng).
2. Sau khi qua sông (sông ở giữa dòng 4 và 5), được phép di chuyển tiến thẳng hoặc đi ngang sang trái/phải 1 bước.
3. Không bao giờ được phép đi lùi.
4. Bị chặn bởi quân đồng minh tại ô mục tiêu và ăn quân đối phương tại ô mục tiêu.

## Nhật ký tiến trình

- **Trạng thái:** Đã hoàn thành toàn bộ 4 Test Case cho quân Tốt.

### Nhật ký chi tiết:
1. **Test Case 1: Di chuyển của quân Tốt đỏ trước sông**
   - **Mục tiêu:** Quân Tốt đỏ tại `(6, 4)` (chưa qua sông) chỉ được di chuyển thẳng tiến lên ô `(5, 4)`.
   - **Kết quả:** Đã chạy unit test thành công.

2. **Test Case 2: Di chuyển của quân Tốt đỏ sau khi qua sông**
   - **Mục tiêu:** Quân Tốt đỏ tại `(4, 4)` (đã qua sông) được phép di chuyển tiến thẳng tới `(3, 4)` hoặc đi ngang sang trái `(4, 3)` và sang phải `(4, 5)`.
   - **Kết quả:** Đã chạy unit test thành công.

3. **Test Case 3: Bị chặn bởi đồng minh và ăn quân đối phương**
   - **Mục tiêu:** Quân Tốt đỏ tại `(4, 4)` bị cản phía trước bởi đồng minh tại `(3, 4)`, và có quân đen tại `(4, 3)`. Tốt chỉ được đi ngang ăn quân đen tại `(4, 3)` hoặc đi ngang sang phải `(4, 5)`.
   - **Kết quả:** Đã chạy unit test thành công.

4. **Test Case 4: Kiểm thử quân Tốt đen trước và sau sông**
   - **Mục tiêu:** 
     - Trước sông tại `(3, 4)`: Chỉ đi thẳng xuống `(4, 4)`.
     - Sau sông tại `(5, 4)`: Đi thẳng xuống `(6, 4)` hoặc sang ngang `(5, 3)`, `(5, 5)`.
   - **Kết quả:** Đã chạy unit test thành công.

---

# Nhật ký Kiểm thử TDD - Quân Tướng (General)

Tài liệu này ghi lại quá trình kiểm thử TDD cho logic di chuyển của quân Tướng (`G`), giới hạn trong Cung cấm và di chuyển thẳng/ngang.

## Mục tiêu kiểm thử
Đảm bảo quân Tướng di chuyển đúng luật cờ tướng:
1. Di chuyển thẳng/ngang 1 bước (lên, xuống, trái, phải).
2. Giới hạn tuyệt đối trong phạm vi Cung cấm (Palace) (Đỏ: dòng 7-9, cột 3-5; Đen: dòng 0-2, cột 3-5).
3. Bị chặn bởi quân đồng minh tại ô mục tiêu.
4. Ăn quân đối phương tại ô mục tiêu thẳng/ngang trong Cung cấm.

## Nhật ký tiến trình

- **Trạng thái:** Đã hoàn thành toàn bộ 4 Test Case cho quân Tướng.

### Nhật ký chi tiết:
1. **Test Case 1: Tướng đỏ ở tâm Cung cấm trên bàn cờ trống**
   - **Mục tiêu:** Tướng đỏ tại `(8, 4)` đi được 4 hướng trực giao: `{(7, 4), (9, 4), (8, 3), (8, 5)}`.
   - **Kết quả:** Đã chạy unit test thành công.

2. **Test Case 2: Tướng đỏ ở góc Cung cấm (Giới hạn phạm vi)**
   - **Mục tiêu:** Tướng đỏ tại góc `(9, 3)` chỉ được đi lên `(8, 3)` hoặc sang phải `(9, 4)`. Không được ra ngoài Cung cấm.
   - **Kết quả:** Đã chạy unit test thành công.

3. **Test Case 3: Bị chặn bởi đồng minh**
   - **Mục tiêu:** Tướng đỏ tại `(8, 4)` bị chặn bởi quân đỏ tại `(7, 4)`. Tướng chỉ còn 3 nước đi hợp lệ: `{(9, 4), (8, 3), (8, 5)}`.
   - **Kết quả:** Đã chạy unit test thành công.

4. **Test Case 4: Ăn quân đối phương**
   - **Mục tiêu:** Tướng đỏ tại `(8, 4)` ăn quân đen tại `(7, 4)` thành công.
   - **Kết quả:** Đã chạy unit test thành công.

