# Hướng Dẫn Đọc Giao Diện Chạy Tay & Cơ Chế 18 Thuật Toán AI

Tài liệu này được biên soạn nhằm giải thích chi tiết, dễ hiểu bằng tiếng Việt về cách hoạt động, cơ chế chọn quân cờ để xét/đi, và cách đọc hiểu bảng thông số chạy tay (visualizer) của toàn bộ **18 thuật toán AI** trong dự án Cờ Tướng. Tài liệu này cực kỳ hữu ích để bạn chuẩn bị cho nội dung báo cáo và thuyết trình đồ án trước giảng viên.

---

## I. HƯỚNG DẪN ĐỌC TỌA ĐỘ BÀN CỜ & NHẬN DIỆN QUÂN CỜ

Khi chạy tay, thuật toán sẽ ghi nhận các nước đi dưới dạng tọa độ xuất phát và đích đến, ví dụ: `A0→A1`. Để biết ngay quân cờ nào đang di chuyển mà không cần nhìn bàn cờ, bạn hãy nhớ vị trí xếp cờ mặc định ở hàng dưới cùng (hàng số `0` của bên Đỏ, hoặc hàng số `9` của bên Đen):

### 1. Bản đồ tọa độ hàng biên
*   **Cột A0 và I0 / A9 và I9:** Quân **Xe**
*   **Cột B0 và H0 / B9 và H9:** Quân **Mã**
*   **Cột C0 và G0 / C9 và G9:** Quân **Tượng**
*   **Cột D0 và F0 / D9 và F9:** Quân **Sĩ**
*   **Cột E0 / E9:** Quân **Tướng**

### 2. Ví dụ thực tế từ bảng chạy tay
*   `n1: A0→A1`: Điểm đi là `A0` $\rightarrow$ Quân **Xe** tiến 1 ô lên `A1`.
*   `n3: B0→C2`: Điểm đi là `B0` $\rightarrow$ Quân **Mã** nhảy chữ L lên `C2`.
*   `n7: D0→E1`: Điểm đi là `D0` $\rightarrow$ Quân **Sĩ** đi chéo lên tâm cung cấm `E1`.

---

## II. GIẢI THÍCH CHI TIẾT 18 THUẬT TOÁN AI (LEVEL 1 ĐẾN LEVEL 6)

---

### LEVEL 1: TÌM KIẾM MÙ (UNINFORMED SEARCH)

Các thuật toán này đi tìm nước đi mà không có bất kỳ ước lượng thông minh nào về tương lai, chỉ duyệt thuần túy theo cấu trúc hình học của cây nước đi.

#### 1. BFS (Breadth-First Search - Tìm kiếm theo chiều rộng)
*   **Ý nghĩa:** Duyệt đều theo từng tầng. Tìm hết tất cả các nước đi khả dĩ ở lượt này, rồi mới xét đến các nước đi ở lượt tiếp theo.
*   **Cách chọn quân để xét:** Sinh ra toàn bộ các nước đi hợp lệ cho tất cả các quân cờ hiện tại. Đẩy tất cả vào hàng đợi.
*   **Cách chọn quân để đi:** Chọn nước đi dẫn đến kết quả tối ưu sau khi đã duyệt qua toàn bộ các nhánh ở cùng độ sâu.
*   **Cách đọc giao diện chạy tay:**
    *   `CURRENT`: Node hiện tại đang được lấy ra phân tích (ví dụ: `n1: A0→A1`).
    *   `QUEUE`: Hàng đợi các nước đi đang chờ được xét. Nước đi nào được sinh ra trước sẽ nằm ở đầu hàng và được xét trước (FIFO).
    *   `EXPLORED`: Danh sách các nước đi đã phân tích xong.

#### 2. DFS (Depth-First Search - Tìm kiếm theo chiều sâu)
*   **Ý nghĩa:** Đi sâu hết mức có thể vào một nhánh nước đi (ví dụ: giả lập Ta đi $\rightarrow$ Địch đi $\rightarrow$ Ta đi... liên tục theo 1 kịch bản) cho đến khi đạt giới hạn độ sâu, rồi mới quay lui (backtrack) thử kịch bản khác.
*   **Cách chọn quân để xét:** Chọn nước đi hợp lệ đầu tiên gặp được, thực hiện thử, rồi lập tức chọn tiếp nước đi tiếp theo từ bàn cờ mới đó mà không dừng lại xét các nước đi khác cùng cấp.
*   **Cách chọn quân để đi:** Chọn nước đi thuộc nhánh kịch bản mang lại điểm số cao nhất sau khi đã đi sâu phân tích.
*   **Cách đọc giao diện chạy tay:**
    *   `STACK`: Ngăn xếp chứa chuỗi kịch bản nước đi đang đi sâu (LIFO). Node ở cuối danh sách là node mới nhất.
    *   `🔙 BACKTRACKING`: Khi chữ này sáng lên, nghĩa là nhánh hiện tại đã đi hết độ sâu giới hạn, thuật toán đang rút lại nước đi để quay ngược lên tầng trên thử nhánh khác.

#### 3. UCS (Uniform Cost Search - Tìm kiếm chi phí đồng nhất)
*   **Ý nghĩa:** Tìm đường đi có tổng chi phí thấp nhất. Trong cờ tướng, nước đi có ích nhất là nước ăn được quân to của đối thủ.
*   **Công thức tính chi phí (Cost):** `g(n) = 1000 - Giá trị quân cờ bị ăn`.
    *   Ăn quân **Xe** (90 điểm): Chi phí rất thấp `1000 - 90 = 910`.
    *   Không ăn quân (0 điểm): Chi phí tối đa `1000 - 0 = 1000`.
*   **Cách chọn quân để xét:** Thuật toán sử dụng Hàng đợi ưu tiên (Priority Queue) để sắp xếp các nước đi. Nước đi nào có **chi phí thấp nhất** (tức là nước đi ăn quân to nhất của đối thủ) sẽ được xếp lên đầu và lấy ra xét trước.
*   **Cách chọn quân để đi:** Chọn nước đi có chi phí tích lũy thấp nhất.
*   **Cách đọc giao diện chạy tay:**
    *   `FRONTIER`: Danh sách các nước đi đang chờ xét, được tự động sắp xếp theo chi phí tăng dần. Bạn sẽ thấy các nước đi ăn quân lớn luôn nằm ở trên cùng.
    *   `g_cost`: Chi phí của nước đi đó. Số càng nhỏ nước đi càng được ưu tiên.

---

### LEVEL 2: TÌM KIẾM HEURISTIC (HEURISTIC SEARCH)

Các thuật toán này sử dụng các hàm đánh giá thông minh (Heuristic) để hướng luồng tìm kiếm vào các nhánh có lợi, thay vì duyệt mù quáng.

#### 4. Greedy (Tìm kiếm tham ăn)
*   **Ý nghĩa:** Cực kỳ tham lam, chỉ quan tâm đến lợi ích trước mắt.
*   **Cách chọn quân để xét & đi:** Tại mỗi bước đi, thuật toán đánh giá tất cả các nước đi hợp lệ và chọn ngay nước đi có hàm Heuristic $h(n)$ **lớn nhất** (tức là nước ăn được quân cờ có trị giá cao nhất của đối thủ tại lượt đó, ví dụ ăn Xe hoặc Pháo). Nếu không ăn được quân, nó đi ngẫu nhiên.
*   **Cách đọc giao diện chạy tay:**
    *   `CANDIDATES`: Danh sách các nước đi được xếp hạng theo giá trị quân ăn được giảm dần.
    *   Nước đi có ký hiệu `✅` và chữ `BEST` ở đầu danh sách luôn là nước ăn quân to nhất.

#### 5. A* (A-Star)
*   **Ý nghĩa:** Thuật toán tìm kiếm tối ưu nổi tiếng nhất. Nó cân bằng giữa chi phí thực tế đã bỏ ra và ước lượng khoảng cách thông minh đến chiến thắng trong tương lai.
*   **Công thức:** $f(n) = g(n) + h(n)$.
    *   $g(n)$: Chi phí thực tế đã đi (`1000 - Giá trị quân bị ăn`).
    *   $h(n)$: Giá trị cờ của đối thủ còn lại trên bàn (đối thủ càng ít cờ, hàm Heuristic $h(n)$ càng nhỏ, tức là ta càng gần chiến thắng).
*   **Cách chọn quân để xét & đi:** Sắp xếp tất cả các nước đi trong `FRONTIER` theo điểm số $f(n)$ tăng dần. Nước đi nào có tổng điểm $f(n)$ **nhỏ nhất** sẽ được ưu tiên lấy ra xét và chọn đi.
*   **Cách đọc giao diện chạy tay:**
    *   Bảng thông số hiển thị rõ ràng: `f = g + h`.
    *   `CURRENT`: Nước đi đang được xét với chi tiết điểm số thành phần $g$ và $h$.
    *   `FRONTIER`: Sắp xếp các nước đi ưu tiên tăng dần theo điểm $f$.

#### 6. IDA* (Iterative Deepening A*)
*   **Ý nghĩa:** Kết hợp ưu điểm tiết kiệm bộ nhớ của DFS và tính tối ưu của A*. Nó chạy DFS lặp đi lặp lại với một ngưỡng giới hạn điểm số (threshold) tăng dần qua mỗi vòng lặp.
*   **Cách chọn quân để xét & đi:** Duyệt DFS. Nếu một nước đi có điểm số $f(n) > \text{threshold}$ hiện tại, thuật toán lập tức cắt bỏ nhánh đó không xét nữa (`cutoff`). Nếu duyệt hết mà không tìm được nước đi thỏa mãn, nó tăng ngưỡng `threshold` lên và lặp lại vòng mới.
*   **Cách đọc giao diện chạy tay:**
    *   `Threshold`: Ngưỡng giới hạn điểm số của vòng lặp hiện tại.
    *   `Iteration`: Vòng lặp thứ mấy (1, 2 hoặc 3).
    *   `✂️ CUTOFF`: Nhãn cảnh báo màu đỏ xuất hiện khi một nước đi bị cắt bỏ do vượt ngưỡng.

---

### LEVEL 3: TÌM KIẾM CỤC BỘ (LOCAL SEARCH)

Thích hợp cho các bài toán có không gian tìm kiếm cực lớn, tập trung tối ưu hóa trạng thái hiện tại bằng các phép biến đổi lân cận.

#### 7. Hill Climbing (Leo đồi)
*   **Ý nghĩa:** Giống như một người leo núi trong sương mù, chỉ nhìn thấy các bước chân xung quanh mình và luôn chọn bước đi lên cao nhất.
*   **Cách chọn quân để xét & đi:** Đánh giá điểm số của bàn cờ ở tất cả các nước đi lân cận (neighbors). Chọn nước đi có điểm số cao hơn trạng thái hiện tại nhiều nhất để đi.
*   **Hiện tượng Plateau (Kẹt ở sườn đồi):** Nếu tất cả các nước đi xung quanh đều có điểm bằng hoặc tệ hơn nước hiện tại, thuật toán sẽ dừng lại (bị kẹt ở đỉnh cục bộ) dù đó chưa phải là nước đi tối ưu nhất toàn cục.
*   **Cách đọc giao diện chạy tay:**
    *   `NEIGHBORS`: Danh sách các nước đi lân cận sắp xếp theo điểm số bàn cờ giảm dần.
    *   `⚠️ PLATEAU`: Cảnh báo màu đỏ xuất hiện khi thuật toán bị kẹt (không tìm thấy nước lân cận nào tốt hơn nước hiện tại).

#### 8. Simulated Annealing (Luyện kim)
*   **Ý nghĩa:** Mô phỏng quá trình làm nguội kim loại. Ở giai đoạn đầu (nhiệt độ $T$ rất cao), thuật toán sẵn sàng chấp nhận các nước đi tệ hơn nước hiện tại với một xác suất nhất định để thoát khỏi các bẫy đỉnh cục bộ (Plateau). Càng về sau (nhiệt độ $T$ giảm dần), thuật toán càng khắt khe và chỉ chấp nhận các nước đi thực sự tốt.
*   **Công thức xác suất chấp nhận nước đi tệ:** $P = e^{\Delta E / T}$ (với $\Delta E$ là độ chênh lệch điểm số tệ đi, $T$ là nhiệt độ).
*   **Cách chọn quân để xét & đi:** Chọn ngẫu nhiên một nước đi lân cận làm ứng viên (candidate). Nếu ứng viên tốt hơn, đi ngay. Nếu ứng viên tệ hơn, tính xác suất $P$. Nếu một số ngẫu nhiên từ 0 đến 1 nhỏ hơn $P$, thuật toán vẫn chấp nhận đi nước tệ đó để thăm dò.
*   **Cách đọc giao diện chạy tay:**
    *   `🌡️ T`: Nhiệt độ hiện tại, giảm dần qua mỗi bước duyệt.
    *   `ΔE`: Độ chênh lệch điểm (số âm nghĩa là nước đi ứng viên tệ hơn nước hiện tại).
    *   `P(accept)`: Xác suất chấp nhận nước đi tệ đó.
    *   `✅ CHẤP NHẬN` hoặc `❌ TỪ CHỐI`: Quyết định cuối cùng của thuật toán đối với nước đi thử nghiệm.

#### 9. Beam Search (Tìm kiếm chùm tia)
*   **Ý nghĩa:** Hạn chế không gian tìm kiếm bằng cách chỉ giữ lại một số lượng nhánh tốt nhất cố định ở mỗi tầng, thay vì giữ toàn bộ cây nước đi.
*   **Cách chọn quân để xét & đi:** Tại mỗi tầng, thuật toán đánh giá tất cả các nước đi và chỉ chọn giữ lại đúng $k = 3$ nước đi có điểm số cao nhất (gọi là 3 chùm tia - beams). Tất cả các nước đi khác kém điểm hơn đều bị tiêu diệt (loại bỏ) ngay lập tức.
*   **Cách đọc giao diện chạy tay:**
    *   `KEPT (top 3)`: 3 nước đi tốt nhất được giữ lại để tiếp tục phát triển ở tầng sau.
    *   `ELIMINATED`: Danh sách các nước đi bị loại bỏ thẳng tay để tiết kiệm bộ nhớ.

---

### LEVEL 4: MÔI TRƯỜNG PHỨC TẠP (COMPLEX ENVIRONMENTS)

Đối phó với các tình huống biến động, thông tin không chắc chắn hoặc hành vi bất thường của đối thủ.

#### 10. Online Search (Tìm kiếm trực tuyến)
*   **Ý nghĩa:** Khả năng phản ứng cực kỳ nhanh nhạy trước các mối đe dọa trực tiếp.
*   **Cách chọn quân để xét & đi:** Thuật toán liên tục kiểm tra xem Tướng của mình có đang bị chiếu hay không. Nếu phát hiện đang bị chiếu (`In Check`), thuật toán sẽ lập tức **điều chỉnh tăng vọt trọng số giá trị của các quân cờ phòng thủ** (như Sĩ, Tượng) và ưu tiên tuyệt đối các nước đi bảo vệ Tướng hoặc cản đường chiếu, bỏ qua các kế hoạch tấn công khác.
*   **Cách đọc giao diện chạy tay:**
    *   `⚠️ ĐANG BỊ CHIẾU` hoặc `✅ AN TOÀN`: Trạng thái nguy hiểm của Tướng.
    *   `TRƯỚC` và `SAU`: Bảng so sánh giá trị các quân cờ được điều chỉnh động (ví dụ: Sĩ tăng từ 20 lên 100 điểm khi bị chiếu).

#### 11. AND-OR Search (Tìm kiếm AND-OR)
*   **Ý nghĩa:** Lập kế hoạch trong môi trường có đối thủ đối kháng. Ta coi nước đi của mình là **OR node** (ta chủ động chọn nước tốt nhất cho mình), và nước phản công của đối thủ là **AND node** (đối thủ sẽ tìm mọi cách đi nước hiểm nhất để dồn ta vào thế bí).
*   **Cách chọn quân để xét & đi:** Với mỗi nước đi của ta (OR), thuật toán giả định đối thủ sẽ phản công bằng tất cả các nước đi có thể (AND) và tìm nước đi tệ nhất của đối thủ đối với ta (`worst_case`). Thuật toán sẽ chọn nước đi OR nào mà trong tình huống tệ nhất đó, ta vẫn đạt được điểm số đảm bảo (`guaranteed_score`) cao nhất.
*   **Cách đọc giao diện chạy tay:**
    *   `OR NODE (ta)`: Nước đi của ta đang được phân tích.
    *   `AND RESPONSES`: Tất cả các phương án phản công của đối thủ. Nước phản công hiểm nhất được đánh dấu `← WORST` bằng màu đỏ.
    *   `Guaranteed score`: Điểm số chắc chắn đạt được nếu đi nước này.

#### 12. Belief State (Trạng thái niềm tin)
*   **Ý nghĩa:** "Biết địch biết ta, trăm trận trăm thắng". Thuật toán tự xây dựng một mô hình đánh giá phong cách chơi của đối thủ dựa trên lịch sử các nước đi trước đó của họ.
*   **Cách chọn quân để xét & đi:** Tính toán xác suất đối thủ thuộc phong cách nào: **Tấn công** (Aggressive), **Phòng thủ** (Defensive), hay **Kiểm soát** (Positional). Sau đó, với mỗi nước đi của mình, thuật toán tính toán **Lợi ích kỳ vọng (Expected Utility)** bằng cách nhân xác suất phong cách với điểm số tương ứng. Nước đi nào có lợi ích kỳ vọng cao nhất sẽ được chọn.
*   **Cách đọc giao diện chạy tay:**
    *   `Phong cách`: Phong cách của đối thủ mà thuật toán tin tưởng nhất (ví dụ: AGGRESSIVE).
    *   `P(style)`: Phân phối xác suất niềm tin (ví dụ: P(Tấn công)=0.7, P(Phòng thủ)=0.2...).
    *   `E[U]`: Điểm lợi ích kỳ vọng của nước đi được chọn.

---

### LEVEL 5: BÀI TOÁN CSP (CONSTRAINT SATISFACTION)

Coi bàn cờ tướng như một bài toán ràng buộc vị trí, tập trung tối ưu hóa sự an toàn và cấu trúc đội hình.

#### 13. Backtracking MRV (Minimum Remaining Values)
*   **Ý nghĩa:** Khi có quá nhiều quân cờ có thể đi, thuật toán áp dụng heuristics MRV (Giá trị còn lại tối thiểu) để chọn quân cờ đang bị hạn chế nước đi nhất (bị vây hãm hoặc ít ô đi nhất) để ưu tiên xử lý trước, giúp thu hẹp cây quyết định cực kỳ nhanh chóng.
*   **Cách chọn quân để xét & đi:** Coi mỗi quân cờ là một biến số. Đếm số ô đích hợp lệ (domain size) của từng quân cờ. Chọn quân cờ có **domain size nhỏ nhất** (nhưng phải lớn hơn 0) để thực hiện tìm kiếm nước đi tối ưu cho quân đó trước.
*   **Cách đọc giao diện chạy tay:**
    *   `VARIABLES`: Danh sách các quân cờ kèm số lượng ô đi hợp lệ của chúng.
    *   Quân cờ được chọn xử lý trước được đánh dấu `← MRV` kèm ký hiệu `✅`.

#### 14. Min-Conflicts (Tối thiểu hóa xung đột)
*   **Ý nghĩa:** Tập trung tối đa vào việc bảo vệ an toàn cho các quân cờ của mình, giảm thiểu sơ hở.
*   **Định nghĩa xung đột (Conflict):** Số lượng quân cờ của ta đang nằm trong tầm ngắm đe dọa (bị bắt) bởi các quân cờ của đối thủ.
*   **Cách chọn quân để xét & đi:** Thuật toán duyệt qua tất cả các nước đi hợp lệ và đếm số lượng quân bị đe dọa sau khi đi nước đó. Nước đi nào làm **giảm thiểu tối đa số quân bị đe dọa** (giảm xung đột xuống thấp nhất) sẽ được ưu tiên chọn đi.
*   **Cách đọc giao diện chạy tay:**
    *   `Conflicts`: Điểm xung đột thay đổi từ bao nhiêu về bao nhiêu (ví dụ: `Conflicts: 3 → 1 (giảm 2)`).
    *   `CANDIDATES`: Danh sách các nước đi xếp hạng theo số lượng xung đột còn lại tăng dần.

#### 15. AC-3 (Arc Consistency - Nhất quán cung)
*   **Ý nghĩa:** Bộ lọc an toàn thông minh. Trước khi tính toán sâu, thuật toán lọc bỏ ngay lập tức các nước đi "tự sát" hoặc đi vào thế bất lợi rõ ràng để không làm mất thời gian tính toán của máy.
*   **Cách chọn quân để xét & đi:** Thuật toán chạy thuật toán AC-3 để lọc các nước đi hợp lệ thành hai nhóm:
    *   `Safe Moves`: Nước đi an toàn (không đi vào ô bị quân rẻ tiền hơn của đối thủ đe dọa mà không có quân bảo vệ).
    *   `Pruned Moves`: Nước đi nguy hiểm bị loại bỏ ngay (ví dụ: Xe đắt tiền đi vào ô bị Tốt đối thủ canh giữ).
    *   Cuối cùng, thuật toán chỉ chọn nước đi tốt nhất nằm trong nhóm **Safe Moves**.
*   **Cách đọc giao diện chạy tay:**
    *   `SAFE`: Danh sách các nước đi an toàn được giữ lại.
    *   `PRUNED`: Danh sách các nước đi bị loại bỏ kèm lý do cụ thể bằng màu đỏ (ví dụ: `Xe: bị Tốt đe dọa`).

---

### LEVEL 6: DỰ ĐOÁN ĐỐI KHÁNG (ADVERSARIAL SEARCH)

Các thuật toán đỉnh cao của AI cờ tướng, có khả năng nhìn xa trông rộng nhiều nước đi bằng cách dự đoán chính xác phản ứng tối ưu của đối thủ.

#### 16. Minimax
*   **Ý nghĩa:** Cốt lõi của lý thuyết trò chơi đối kháng. Thuật toán giả định cả hai bên đều chơi tối ưu hoàn hảo. Ta (MAX) luôn muốn tối đa hóa điểm số của mình, còn đối thủ (MIN) luôn muốn chọn nước đi làm tối thiểu hóa điểm số của ta ở lượt của họ.
*   **Cách chọn quân để xét & đi:** Thuật toán xây dựng cây trò chơi luân phiên: Tầng của ta (MAX) $\rightarrow$ Tầng đối thủ (MIN) $\rightarrow$ Tầng của ta (MAX)... đi sâu 3 tầng. Điểm số từ các lá ở tầng sâu nhất sẽ được truyền ngược lên trên (propagate bottom-up) theo nguyên tắc: tầng MAX lấy điểm lớn nhất từ các con, tầng MIN lấy điểm nhỏ nhất từ các con. Nước đi ở gốc có điểm truyền ngược cao nhất sẽ được chọn.
*   **Cách đọc giao diện chạy tay:**
    *   `PATH`: Con đường đi từ trạng thái gốc hiện tại đến node đang được lượng giá (ví dụ: `root → Xe A0→A1 (MAX) → Pháo B2→B5 (MIN)`).
    *   `Siblings`: Các nước đi cùng cấp và điểm số tương ứng của chúng đã được duyệt xong.

#### 17. Alpha-Beta (Minimax kết hợp cắt tỉa Alpha-Beta)
*   **Ý nghĩa:** Bản nâng cấp kinh điển của Minimax. Nó mang lại kết quả giống hệt Minimax nhưng tốc độ nhanh gấp hàng chục lần nhờ khả năng **cắt bỏ ngay lập tức các nhánh chắc chắn không mang lại kết quả tốt hơn** các nhánh đã duyệt trước đó.
*   **Hai tham số định nghĩa:**
    *   $\alpha$ (Alpha): Điểm số tối thiểu mà người chơi MAX (ta) chắc chắn đã đạt được ở các nhánh trước.
    *   $\beta$ (Beta): Điểm số tối đa mà người chơi MIN (đối thủ) chắc chắn có thể giới hạn ta ở các nhánh trước.
*   **Cơ chế cắt tỉa:** Khi đang duyệt tại một node, nếu thuật toán phát hiện điểm số hiện tại làm cho $\beta \le \alpha$, điều đó có nghĩa là đối thủ chắc chắn sẽ đi một nước khác để ngăn ta đạt đến trạng thái này, hoặc ta chắc chắn có lựa chọn khác tốt hơn. Thuật toán lập tức **ngừng duyệt tất cả các nhánh con còn lại của node này** (cắt tỉa nhánh - pruning).
*   **Cách đọc giao diện chạy tay:**
    *   `α` và `β`: Giá trị Alpha và Beta cập nhật theo thời gian thực tại node hiện tại.
    *   `✂️ [Lý do cắt]`: Dòng thông báo màu đỏ hiển thị khi xảy ra cắt tỉa (ví dụ: `✂️ β(200) <= α(350) -> cắt nhánh`).

#### 18. Expectimax
*   **Ý nghĩa:** Dùng để đối phó với những đối thủ không chơi tối ưu hoàn hảo (ví dụ: người chơi nghiệp dư thường đi những nước cờ ngẫu nhiên, mắc sai lầm hoặc không chọn nước hiểm nhất).
*   **Cách chọn quân để xét & đi:** Thay vì coi lượt của đối thủ là một node tối thiểu hóa điểm số cực đoan (MIN node) giống Minimax, Expectimax coi lượt của đối thủ là một **CHANCE node (Node cơ hội/ngẫu nhiên)**. Điểm số truyền ngược từ lượt đối thủ sẽ được tính theo công thức giá trị kỳ vọng (trung bình có trọng số):
    $$\text{Expected Value} = 0.7 \times (\text{Nước đi tốt nhất của đối thủ}) + 0.3 \times (\text{Trung bình điểm các nước đi khác})$$
    Điều này giúp AI chọn nước đi mang tính thực tế và linh hoạt hơn, sẵn sàng gài bẫy nếu biết đối thủ dễ đi sai.
*   **Cách đọc giao diện chạy tay:**
    *   `Node type`: Hiển thị rõ node hiện tại là `MAX NODE` (lượt của ta) hay `CHANCE NODE` (lượt đối thủ).
    *   `Expected Value`: Điểm kỳ vọng được tính toán tại CHANCE node để truyền ngược lên trên.
