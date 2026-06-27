# TỔNG HỢP VÀ GIẢI THÍCH CHI TIẾT 18 THUẬT TOÁN AI TRONG CỜ TƯỚNG

Tài liệu này tổng hợp toàn bộ 18 thuật toán tìm kiếm và lựa chọn nước đi được triển khai trong dự án Chinese Chess AI (chia thành 6 cấp độ từ cơ bản đến nâng cao). Mỗi thuật toán có chiến lược phân tích, ưu/nhược điểm và cách tiếp cận thế cờ khác nhau.

---

## MÔ HÌNH PEAS CỦA AI CỜ TƯỚNG (PEAS SPECIFICATION)

Mô hình **PEAS** (Performance, Environment, Actuators, Sensors) giúp định hình rõ toàn bộ hệ thống tác nhân AI trong bài toán chơi cờ tướng của dự án này:

*   **P - Performance Measure (Thước đo hiệu suất):**
    *   **Mục tiêu tối thượng:** Chiến thắng ván cờ (Chiếu bí Tướng đối phương).
    *   **Hiệu suất chiến thuật:** Tối đa hóa điểm số thế cờ (ăn quân giá trị cao của đối phương, bảo vệ quân ta), duy trì ưu thế vị trí (chiếm lộ, vượt sông).
    *   **Tốc độ & Hiệu quả:** Thời gian ra quyết định nhanh chóng, tuân thủ tuyệt đối luật lệ cờ tướng (không tạo nước đi lậu).
*   **E - Environment (Môi trường hoạt động):**
    *   **Không gian vật lý/ảo:** Bàn cờ tướng dạng lưới tọa độ $10 \times 9$, chứa tối đa 32 quân cờ.
    *   **Đối tượng tương tác:** Đối thủ (Người chơi hoặc một Tác nhân AI khác).
    *   **Đặc tính môi trường:** 
        *   *Hoàn toàn quan sát được (Fully Observable):* AI thấy toàn bộ vị trí các quân trên bàn cờ.
        *   *Đối kháng & Chiến lược (Adversarial):* Bàn cờ hai người chơi mang tính tổng không (Zero-sum).
        *   *Tĩnh (Static):* Trạng thái bàn cờ không tự thay đổi trong lúc AI đang suy nghĩ.
        *   *Rời rạc (Discrete):* Các nước đi và tọa độ đếm được rõ ràng theo từng lượt (Sequential).
*   **A - Actuators (Cơ cấu tác động / Hành động):**
    *   **Cơ chế chuyển động:** Cập nhật vị trí quân cờ mới trên cấu trúc dữ liệu ma trận bàn cờ (hàm `make_move`).
    *   **Giao tiếp & Giao diện:** Gửi tín hiệu nước đi tới GUI (giao diện Pygame) để thay đổi vị trí đồ họa, ghi lại lịch sử nước đi và log phân tích (thông qua `StepRecorder`).
*   **S - Sensors (Cảm biến / Tiếp nhận thông tin):**
    *   **Cảm biến thế cờ:** Nhận biết cấu trúc ma trận trạng thái hiện tại (`board.matrix`), xác định lượt đi hiện tại (`board.turn`).
    *   **Tín hiệu người dùng:** Nhận thông tin nước đi của đối thủ truyền vào từ giao diện tương tác (sự kiện click chuột hoặc nước cờ từ hệ thống).

---

## BẢNG TỔNG QUAN HỆ THỐNG THUẬT TOÁN

| Level | Nhóm Thuật Toán | Các Thuật Toán Chi Tiết | Đặc Điểm Chính | File Triển Khai |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Tìm kiếm mù** *(Uninformed Search)* | BFS, DFS, UCS | Duyệt ngẫu nhiên hoặc theo cấu trúc cây cơ bản, không có định hướng thông minh. | [level1.py](file:///c:/Users/ADMIN/Desktop/vibecoding/BAITAPAGENT/chinese_chess_ai/ai/level1.py) |
| **2** | **Tìm kiếm Heuristic** *(Informed Search)* | Greedy, A*, IDA* | Dùng hàm đánh giá (Heuristic) để định hướng tìm kiếm, ưu tiên các nước cờ tiềm năng. | [level2.py](file:///c:/Users/ADMIN/Desktop/vibecoding/BAITAPAGENT/chinese_chess_ai/ai/level2.py) |
| **3** | **Tìm kiếm Cục bộ** *(Local Search)* | Hill Climbing, Simulated Annealing, Beam Search | Tối ưu hóa thế cờ dựa trên trạng thái lân cận hiện tại, tiết kiệm bộ nhớ. | [level3.py](file:///c:/Users/ADMIN/Desktop/vibecoding/BAITAPAGENT/chinese_chess_ai/ai/level3.py) |
| **4** | **Tìm kiếm Môi trường** *(Advanced Search)* | Online Search, AND-OR Search, Belief State | Quản lý tình huống đa nhánh, phân tích kế hoạch ứng phó cho nhiều kịch bản. | [level4.py](file:///c:/Users/ADMIN/Desktop/vibecoding/BAITAPAGENT/chinese_chess_ai/ai/level4.py) |
| **5** | **Thỏa mãn Ràng buộc** *(CSP / Constraints)* | Backtracking + MRV, Min-Conflicts, AC-3 | Hướng tiếp cận phòng thủ và gán vị trí, giảm thiểu nguy hiểm và loại bỏ nước đi xấu. | [level5.py](file:///c:/Users/ADMIN/Desktop/vibecoding/BAITAPAGENT/chinese_chess_ai/ai/level5.py) |
| **6** | **Tìm kiếm Đối kháng** *(Adversarial Search)* | Minimax, Alpha-Beta Pruning, Expectimax | Chuẩn mực trong AI đánh cờ, tính toán đa chiều cả kế hoạch của ta và phản ứng của địch. | [level6.py](file:///c:/Users/ADMIN/Desktop/vibecoding/BAITAPAGENT/chinese_chess_ai/ai/level6.py) |

---

## HỆ THỐNG CHẤM ĐIỂM VÀ ĐÁNH GIÁ THẾ CỜ (BOARD EVALUATION)

Để các thuật toán tìm kiếm (đặc biệt là nhóm Heuristic và Tìm kiếm đối kháng) biết được nước đi nào là tốt hay xấu, AI sử dụng một hàm đánh giá thế cờ tổng quát. Toàn bộ quy tắc và logic tính điểm này được triển khai trong file **[eval.py](file:///c:/Users/ADMIN/Desktop/vibecoding/BAITAPAGENT/chinese_chess_ai/ai/eval.py)** thông qua hàm `evaluate_board(board)`.

### 1. Góc nhìn tính điểm (Perspective)
Điểm số tổng hợp được tính theo góc nhìn của quân **Đỏ (RED)**:
$$\text{Score} = (\text{Điểm Lực Lượng Đỏ} + \text{Điểm Vị Trí Đỏ}) - (\text{Điểm Lực Lượng Đen} + \text{Điểm Vị Trí Đen})$$
*   **Điểm số > 0:** Quân Đỏ đang chiếm ưu thế.
*   **Điểm số < 0:** Quân Đen đang chiếm ưu thế.
*   **Điểm số = 0:** Thế trận cân bằng.

---

### 2. Tiêu chí 1: Chênh lệch lực lượng (Material Score)
Mỗi quân cờ trên bàn được gán một giá trị cố định (`PIECE_VALUES`) phản ánh tầm quan trọng và sức mạnh tác chiến của nó trong bàn cờ cờ tướng:
*   **Tướng (G - General):** `10,000` điểm (Quân tối quan trọng, mất Tướng là thua).
*   **Xe (R - Rook):** `900` điểm (Quân cơ động và mạnh nhất bàn cờ).
*   **Pháo (C - Cannon):** `450` điểm (Mạnh nhờ khả năng tấn công từ xa qua ngòi).
*   **Mã (H - Horse):** `300` điểm (Tác chiến tầm trung, có thể bị cản chân).
*   **Tượng (E - Elephant):** `200` điểm (Phòng thủ, bảo vệ trận địa nhà, không qua sông).
*   **Sĩ (A - Advisor):** `200` điểm (Bảo vệ sát Tướng trong Cửu cung).
*   **Tốt (P - Pawn):** `100` điểm (Giá trị cơ bản, tăng mạnh khi sang sông).

---

### 3. Tiêu chí 2: Ưu thế vị trí (Positional Score / Piece-Square Tables)
Để giúp AI biết cách bố trí quân cờ vào các vị trí đắc địa (chẳng hạn như chiếm lộ đẹp, đưa Tốt sang sông, xuất Xe sớm), AI sử dụng các Bảng điểm vị trí (Piece-Square Tables - PST). Bảng điểm này định nghĩa điểm thưởng cho từng ô trên lưới bàn cờ $10 \times 9$:

*   **Tốt (`PST_PAWN_RED`):** 
    *   Khi chưa sang sông (hàng 5-9 của Đỏ): Điểm thưởng = `0`.
    *   Vừa qua sông (hàng 4): Bắt đầu nhận điểm thưởng (`+6` đến `+15`).
    *   Tiến sâu vào lãnh thổ địch và tiến gần áp sát trung tâm (hàng 1-3): Điểm thưởng tăng vọt lên tới `+30` điểm.
*   **Mã (`PST_KNIGHT_RED`):** 
    *   Mã đứng ở các ô rìa/góc bàn cờ bị phạt điểm (`-5` điểm) do bị hạn chế hướng đi.
    *   Mã phát triển lên các đường trung tâm và tiến lên phía trước nhận điểm thưởng cao (lên tới `+20` điểm).
*   **Pháo (`PST_CANNON_RED`):** 
    *   Được cộng điểm cao khi duy trì ở hàng phòng thủ thứ 3 (`+15` điểm) để làm pháo đầu hoặc giữ ngòi phòng ngự.
    *   Thích hợp kiểm soát các cột trung tâm.
*   **Xe (`PST_ROOK_RED`):** 
    *   Khuyến khích xuất Xe sớm và chiếm các cột mở, hàng dọc thông thoáng.
    *   Đứng ở các vị trí cởi mở nhận điểm thưởng từ `+10` đến `+20` điểm.
*   **Sĩ và Tượng (`PST_DEFENSIVE`):** 
    *   Chỉ nhận điểm thưởng khi tụ về sát Cửu cung và trung tâm cung phòng thủ (`+10` điểm) để duy trì cấu trúc bảo vệ Tướng kiên cố.

---

### 4. Quy tắc đối xứng cho quân Đen
Vì bảng PST mặc định được thiết kế từ dưới nhìn lên cho quân Đỏ, đối với các quân cờ của bên **Đen (BLACK)**, hàm `evaluate_board` tự động áp dụng phép biến đổi gương (mirroring) để tra cứu điểm vị trí chính xác:
*   **Lật ngược hàng ngang (Vertical Mirror):** `mr = 9 - r`
*   **Lật ngược cột dọc (Horizontal Mirror):** `mc = 8 - c`

Nhờ sự kết hợp chặt chẽ giữa **Lực lượng** và **Vị trí** trong [eval.py](file:///c:/Users/ADMIN/Desktop/vibecoding/BAITAPAGENT/chinese_chess_ai/ai/eval.py), AI có khả năng đưa ra quyết định cực kỳ tự nhiên, biết thí quân nhỏ để chiếm vị trí đẹp hoặc tổ chức tấn công tổng lực đúng thời điểm.

---

## CHI TIẾT CÁCH HOẠT ĐỘNG CỦA TỪNG THUẬT TOÁN

### LEVEL 1: TÌM KIẾM MÙ (UNINFORMED SEARCH)

#### 1. BFS (Breadth-First Search - Tìm kiếm theo chiều rộng)
*   **Nguyên lý hoạt động:** Sử dụng cấu trúc Hàng đợi (Queue - FIFO). Thuật toán mở rộng toàn bộ các nước đi có thể có ở độ sâu 1, sau đó mới tiến xuống mở rộng tất cả các nút ở độ sâu 2.
*   **Ứng dụng trong Cờ Tướng:** AI khám phá cạn kiệt mọi kịch bản ngắn hạn trước khi nhìn sâu hơn. Giúp AI không bỏ sót bất kỳ nước đi hợp lệ nào ở tầm gần, nhưng tốn rất nhiều bộ nhớ khi số lượng nước đi lớn.

#### 2. DFS (Depth-First Search - Tìm kiếm theo chiều sâu)
*   **Nguyên lý hoạt động:** Sử dụng cấu trúc Ngăn xếp (Stack - LIFO). Thuật toán ưu tiên đi sâu vào một nhánh cụ thể cho đến khi đạt giới hạn độ sâu (depth limit), sau đó quay lui (backtrack) để khám phá các nhánh khác.
*   **Ứng dụng trong Cờ Tướng:** AI "ám ảnh" tính toán triệt để một kịch bản chuỗi nước đi (ví dụ: chuỗi nước thí quân ăn Xe) trước khi xét đến các kịch bản khác. Dùng ít bộ nhớ hơn BFS nhưng dễ bị sa đà vào các nhánh cờ không quan trọng.

#### 3. UCS (Uniform Cost Search - Tìm kiếm chi phí đồng nhất)
*   **Nguyên lý hoạt động:** Sử dụng Hàng đợi ưu tiên (Priority Queue). Mở rộng các nút dựa trên "chi phí tích lũy" ít nhất thay vì đếm số bước đi.
*   **Ứng dụng trong Cờ Tướng:** Các nước đi được gán trọng số rủi ro hoặc chi phí hoạt động (ví dụ: di chuyển Tướng có rủi ro cao hơn di chuyển Tốt). AI sẽ ưu tiên tính toán các phương án an toàn, ít tốn kém chi phí hành động nhất trước.

---

### LEVEL 2: TÌM KIẾM CÓ THÔNG TIN / HEURISTIC (INFORMED SEARCH)

#### 4. Greedy (Greedy Best-First Search - Tìm kiếm tham lam)
*   **Nguyên lý hoạt động:** Thuật toán luôn chọn mở rộng nút con có điểm số đánh giá (Heuristic $h(n)$) cao nhất ngay tức khắc mà không cần tính đến độ sâu tương lai.
*   **Ứng dụng trong Cờ Tướng:** AI thể hiện lối chơi "tham ăn". Nếu thấy một nước đi ăn được quân lớn (như Xe, Pháo) hoặc tạo thế chiếu Tướng, AI sẽ lập tức thực hiện mà không quan tâm nước tiếp theo có bị đối phương gài bẫy hay không.

#### 5. A* (A-Star Search)
*   **Nguyên lý hoạt động:** Tối ưu hóa con đường tìm kiếm bằng hàm $f(n) = g(n) + h(n)$, trong đó $g(n)$ là chi phí đã đi và $h(n)$ là ước lượng heuristic về thế cờ.
*   **Ứng dụng trong Cờ Tướng:** AI đạt sự cân bằng hoàn hảo giữa nỗ lực/bước đi cần thiết $g(n)$ và lợi thế thế cờ đạt được $h(n)$. AI không vội vã tham lam mà tính toán đường lối bài bản để giành lợi thế vững chắc.

#### 6. IDA* (Iterative Deepening A*)
*   **Nguyên lý hoạt động:** Kết hợp cấu trúc duyệt ít tốn bộ nhớ của DFS với hàm ước lượng thông minh $f(n)$ của A*. Tìm kiếm được lặp lại với các ngưỡng điểm (threshold) tăng dần.
*   **Ứng dụng trong Cờ Tướng:** Vừa giữ được sự thông minh, định hướng chính xác của A*, vừa giải quyết được nhược điểm tốn bộ nhớ, cho phép AI phân tích thế cờ hiệu quả trên các máy tính có tài nguyên giới hạn.

---

### LEVEL 3: TÌM KIẾM CỤC BỘ & TỐI ƯU HÓA (LOCAL SEARCH)

#### 7. Hill Climbing (Leo đồi)
*   **Nguyên lý hoạt động:** Bắt đầu từ thế cờ hiện tại, AI thử các nước đi lân cận và ngay lập tức di chuyển đến trạng thái có điểm số cao hơn. Thuật toán dừng lại khi xung quanh không có nước nào điểm cao hơn hiện tại (đạt đỉnh).
*   **Ứng dụng trong Cờ Tướng:** Nhanh chóng tìm ra nước đi giúp nâng điểm số bàn cờ. Tuy nhiên, AI dễ bị kẹt ở "đỉnh cục bộ" (local optima) – không dám đi các nước lùi quân chiến thuật hoặc thí quân nhằm đạt lợi thế lớn hơn sau này.

#### 8. Simulated Annealing (Luyện kim / Ủ thép)
*   **Nguyên lý hoạt động:** Dựa trên quá trình làm nguội kim loại. Khi "nhiệt độ" $T$ còn cao (đầu trận/lúc mới suy nghĩ), thuật toán cho phép AI chọn cả những nước đi làm giảm điểm số với xác suất nhất định. Khi $T$ giảm dần, AI mới siết chặt việc chọn nước tốt.
*   **Ứng dụng trong Cờ Tướng:** Khắc phục triệt để nhược điểm của Hill Climbing. Thỉnh thoảng AI sẽ tung ra các nước đi mạo hiểm, thí quân hoặc các nước đi chờ cực kỳ khó lường để bứt phá khỏi thế trận bế tắc.

#### 9. Beam Search (Tìm kiếm theo chùm)
*   **Nguyên lý hoạt động:** Biến thể của BFS nhưng ở mỗi tầng độ sâu, thuật toán chỉ giữ lại đúng $K$ nút tốt nhất (Beam width) và loại bỏ toàn bộ các nhánh còn lại.
*   **Ứng dụng trong Cờ Tướng:** Giúp AI tập trung toàn bộ năng lực tính toán vào $K$ phương án tiềm năng nhất (ví dụ: 5 nước đi hàng đầu). Giảm thiểu đáng kể thời gian suy nghĩ của AI.

---

### LEVEL 4: TÌM KIẾM MÔI TRƯỜNG PHỨC TẠP (ADVANCED SEARCH)

#### 10. Online Search (Tìm kiếm trực tuyến)
*   **Nguyên lý hoạt động:** Kết hợp giữa việc tính toán và thực thi trực tiếp trong thời gian thực thay vì lập trọn vẹn kế hoạch rồi mới chạy.
*   **Ứng dụng trong Cờ Tướng:** Phù hợp khi AI chơi trong môi trường phản hồi nhanh, AI đi nước cờ thăm dò và lập tức điều chỉnh chiến lược theo động thái của đối thủ trên bàn cờ thực tế.

#### 11. AND-OR Search (Tìm kiếm AND-OR)
*   **Nguyên lý hoạt động:** Phân chia không gian tìm kiếm thành các nút OR (lượt của AI, chọn 1 phương án tốt nhất) và nút AND (lượt đối thủ, AI phải tính toán đáp trả *toàn bộ* các phương án đối thủ có thể đi).
*   **Ứng dụng trong Cờ Tướng:** Rất mạnh trong việc tính các đòn sấm sét (chiếu bí liên tục). Để chắc chắn ép bí đối phương, AI phải đảm bảo dù đối phương chọn phương án trốn chạy nào (AND), AI cũng có nước đi tiếp theo (OR) để chiến thắng.

#### 12. Belief State Search (Tìm kiếm không gian niềm tin)
*   **Nguyên lý hoạt động:** Duy trì một tập hợp các trạng thái khả dĩ (belief state) và xử lý tối ưu trên tập trạng thái đó thay vì một trạng thái đơn lẻ.
*   **Ứng dụng trong Cờ Tướng:** Được AI sử dụng khi phân tích các thế cờ mờ hoặc dự đoán cụm chiến thuật của đối thủ, giúp AI linh hoạt chuẩn bị phương án phòng ứng cho nhiều kịch bản cùng lúc.

---

### LEVEL 5: THỎA MÃN RÀNG BUỘC (CONSTRAINT SATISFACTION - CSP)

#### 13. Backtracking + MRV (Quay lui kết hợp Minimum Remaining Values)
*   **Nguyên lý hoạt động:** Xem xét việc chọn nước đi như bài toán thỏa mãn điều kiện an toàn. Ưu tiên chọn giải quyết biến có ít lựa chọn hợp lệ nhất (MRV).
*   **Ứng dụng trong Cờ Tướng:** AI quét qua các quân cờ của mình, quân nào đang bị đối phương truy sát hoặc có ít nước chạy trốn nhất sẽ được bế lên bàn tính toán trước để kịp thời giải nguy.

#### 14. Min-Conflicts (Tối thiểu hóa xung đột)
*   **Nguyên lý hoạt động:** Ưu tiên điều chỉnh các biến đang gây ra sự xung đột lớn nhất để đưa toàn bộ hệ thống về trạng thái hài hòa.
*   **Ứng dụng trong Cờ Tướng:** Đỉnh cao trong lối chơi phòng thủ. AI tìm cách gán vị trí cho các quân cờ sao cho giảm thiểu tối đa các "xung đột" (tức là số lượng quân ta đang nằm trong tầm ngắm của đối phương).

#### 15. AC-3 (Arc Consistency 3)
*   **Nguyên lý hoạt động:** Thuật toán kiểm tra tính nhất quán giữa các cặp biến (cung), gạt bỏ ngay lập tức các giá trị gây vi phạm ràng buộc.
*   **Ứng dụng trong Cờ Tướng:** Bộ lọc sơ tuyển cực mạnh. Trước khi tìm kiếm sâu, AC-3 loại bỏ toàn bộ các nước đi sai lầm chết người (như đi Tướng ra ngoài cung, để lộ mặt Tướng, hoặc tự nộp quân vào mồm địch), thu hẹp danh sách nước đi an toàn.

---

### LEVEL 6: TÌM KIẾM ĐỐI KHÁNG (ADVERSARIAL SEARCH)

#### 16. Minimax
*   **Nguyên lý hoạt động:** Xây dựng cây trò chơi đối kháng tổng không (Zero-sum). AI đóng vai trò MAX (muốn chọn nhánh điểm cao nhất) và giả định đối thủ là MIN (luôn chọn nhánh dìm điểm AI xuống thấp nhất).
*   **Ứng dụng trong Cờ Tướng:** Mang lại thế trận cực kỳ an toàn và vững chắc vì AI luôn tính đến kịch bản đối phương đáp trả bằng nước đi hiểm hóc nhất. Tuy nhiên, nhược điểm lớn là tốc độ cực kỳ chậm khi duyệt sâu.

#### 17. Alpha-Beta Pruning (Minimax cắt tỉa Alpha-Beta)
*   **Nguyên lý hoạt động:** Nâng cấp từ Minimax bằng cách duy trì hai biến số $\alpha$ (thế cờ tốt nhất cho MAX) và $\beta$ (thế cờ tốt nhất cho MIN). Ngay khi phát hiện một nhánh cờ không thể mang lại kết quả tốt hơn các lựa chọn trước đó ($\beta \le \alpha$), toàn bộ nhánh đó sẽ bị cắt tỉa (loại bỏ khỏi tính toán).
*   **Ứng dụng trong Cờ Tướng:** Đây là **tiêu chuẩn vàng** của tất cả các engine cờ chuyên nghiệp. Việc cắt tỉa các nhánh cờ thừa thãi giúp AI tăng độ sâu tính toán (depth) lên gấp đôi so với Minimax truyền thống trong cùng một mốc thời gian, tạo ra lối chơi sắc bén và vô cùng mạnh mẽ.

#### 18. Expectimax
*   **Nguyên lý hoạt động:** Thay thế tầng MIN của đối thủ bằng tầng CHANCE (nút Xác suất / Kỳ vọng). Thay vì giả định đối thủ luôn chơi nước đi hoàn hảo nhất, thuật toán tính điểm trung bình kỳ vọng của tất cả các phản ứng khả dĩ.
*   **Ứng dụng trong Cờ Tướng:** Thuật toán tuyệt vời khi AI thi đấu với người chơi nghiệp dư. AI hiểu rằng con người có thể mắc sai lầm, do đó thay vì co cụm phòng thủ tuyệt đối như Minimax, AI sẵn sàng tung ra các đòn đánh táo bạo, giăng bẫy với hy vọng đối phương đi nước cờ yếu.
