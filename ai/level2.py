# Level 2 AI: Greedy, A*, IDA*
# Gói chứa các thuật toán tìm kiếm có thông tin (informed search) dựa trên hàm đánh giá heuristic: Greedy Best-First Search, A*, và IDA*.
import random

from ai.eval import PIECE_VALUES
from ai.step_recorder import MAX_VISUALIZATION_STEPS, AStarStep, GreedyStep, IDAStarStep


def get_opponent_material(board, color):
    """
    Hàm tính tổng giá trị vật chất (tổng điểm các quân cờ) hiện có của đối thủ trên bàn cờ.
    Được sử dụng làm hàm heuristic h(n) để ước lượng sức mạnh còn lại của đối thủ.

    Args:
        board: Trạng thái bàn cờ
        color: Màu quân của phía AI hiện tại (red hoặc black)
    """
    opp = "black" if color == "red" else "red"
    total = 0
    # Duyệt qua toàn bộ bàn cờ để tổng hợp điểm số các quân cờ của đối thủ
    for r in range(10):
        for c in range(9):
            p = board.matrix[r][c]
            if p and p.color == opp:
                total += PIECE_VALUES.get(p.name, 0)
    return total


def greedy_move(board, recorder=None):
    """
    Thuật toán tìm kiếm Tham lam (Greedy Best-First Search).
    Thuật toán luôn ưu tiên chọn nước đi ăn quân đối thủ có giá trị cao nhất tại bước hiện tại.
    Nếu không có quân nào để ăn, thuật toán sẽ chọn ngẫu nhiên một nước đi hợp lệ.

    Args:
        board: Trạng thái bàn cờ hiện tại
        recorder: Đối tượng ghi lại các bước tìm kiếm phục vụ trực quan hóa (nếu có)
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None

    # Bảng dịch tên các quân cờ sang tiếng Việt phục vụ hiển thị
    PIECE_NAME_VI = {
        "general": "Tướng",
        "advisor": "Sĩ",
        "elephant": "Tượng",
        "horse": "Mã",
        "rook": "Xe",
        "cannon": "Pháo",
        "pawn": "Tốt",
    }

    # Xáo trộn danh sách nước đi để tạo sự đa dạng khi các nước đi có cùng giá trị heuristic
    random.shuffle(legal_moves)
    best_move = legal_moves[0]
    max_val = -1

    # Tạo trước danh sách thông tin các nút ứng viên (candidates)
    all_nodes = []
    for m in legal_moves:
        target = board.get_piece(m[1])
        # h(n) trong Greedy ở đây chính là giá trị quân cờ ăn được tại vị trí đích
        val = PIECE_VALUES.get(target.name, 0) if target else 0
        char_to_key = {
            "G": "general",
            "A": "advisor",
            "E": "elephant",
            "H": "horse",
            "R": "rook",
            "C": "cannon",
            "P": "pawn",
        }
        key = char_to_key.get(target.name, target.name) if target else None
        piece_name = PIECE_NAME_VI.get(key, "—") if key else "—"

        all_nodes.append({
            "move": m,
            "h": val,
            "piece": piece_name,
        })

    evaluated_so_far = []

    # Duyệt qua các ứng viên để tìm nước đi có h(n) lớn nhất
    for i, candidate_info in enumerate(all_nodes):
        val = candidate_info["h"]
        m = candidate_info["move"]

        evaluated_so_far.append(candidate_info)
        remaining_candidates = all_nodes[i + 1:]

        if val > max_val:
            max_val = val
            best_move = m

        # Ghi lại bước tìm kiếm nếu có đối tượng recorder
        if recorder and i < MAX_VISUALIZATION_STEPS:
            recorder.add_step(
                GreedyStep(
                    step_num=i + 1,
                    algorithm="Greedy",
                    explanation=f"Xét nước {m[0]}→{m[1]}: h={val} ({candidate_info['piece']}), chọn h LỚN NHẤT",
                    chosen_move=best_move,
                    current_node=candidate_info,
                    candidates=remaining_candidates.copy(),
                    evaluated=evaluated_so_far.copy(),
                )
            )

    return best_move


def a_star_move(board, recorder=None):
    """
    Thuật toán tìm kiếm A* (A* Search).
    Đánh giá mỗi nút dựa trên hàm f(n) = g(n) + h(n), trong đó:
    - g(n) = 1000 - giá trị quân bị ăn (chi phí thực tế để đạt đến trạng thái này, ăn quân to thì chi phí nhỏ).
    - h(n) = tổng giá trị quân cờ còn lại của đối thủ (heuristic ước lượng chi phí còn lại để chiến thắng).
    Thuật toán tìm nước đi có f(n) nhỏ nhất.

    Args:
        board: Trạng thái bàn cờ hiện tại
        recorder: Đối tượng ghi lại các bước tìm kiếm phục vụ trực quan hóa (nếu có)
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None

    # Bảng dịch tên các quân cờ sang tiếng Việt
    PIECE_NAME_VI = {
        "general": "Tướng",
        "advisor": "Sĩ",
        "elephant": "Tượng",
        "horse": "Mã",
        "rook": "Xe",
        "cannon": "Pháo",
        "pawn": "Tốt",
    }

    random.shuffle(legal_moves)
    best_move = None
    min_f = float("inf")
    ai_color = board.turn

    # Danh sách tập biên (frontier) và tập đã duyệt (explored) phục vụ trực quan hóa
    frontier_list = []
    explored_list = []

    for i, (from_pos, to_pos) in enumerate(legal_moves):
        # Mô phỏng nước đi và tính g(n)
        target = board.get_piece(to_pos)
        cap_val = PIECE_VALUES.get(target.name, 0) if target else 0
        char_to_key = {
            "G": "general",
            "A": "advisor",
            "E": "elephant",
            "H": "horse",
            "R": "rook",
            "C": "cannon",
            "P": "pawn",
        }
        key = char_to_key.get(target.name, target.name) if target else None
        piece_name = PIECE_NAME_VI.get(key, "—") if key else "—"

        # g(n) = chi phí thực tế đi tới nút này
        g = 1000 - cap_val

        # Thử thực hiện nước đi để tính toán giá trị heuristic h(n) (lực lượng còn lại của địch)
        board.make_move(from_pos, to_pos, test_only=True)
        h = get_opponent_material(board, ai_color)  # Tổng vật chất đối thủ
        board.undo_move(test_only=True)

        # f(n) = g(n) + h(n)
        f = g + h

        node_info = {
            "move": (from_pos, to_pos),
            "g": g,
            "h": h,
            "f": f,
            "piece_captured": piece_name,
            "cap_val": cap_val,
        }

        # Đưa nút vào danh sách tập biên
        frontier_list.append(node_info)

        # Cập nhật nước đi có f(n) nhỏ nhất
        if f < min_f:
            min_f = f
            best_move = (from_pos, to_pos)

        # Ghi lại bước đi nếu có recorder
        if recorder:
            # Sắp xếp tập biên theo giá trị f tăng dần để hiển thị trực quan
            sorted_frontier = sorted(frontier_list, key=lambda x: x["f"])
            recorder.add_step(
                AStarStep(
                    step_num=i + 1,
                    algorithm="A*",
                    explanation=f"Xét nước {from_pos}→{to_pos}: g={g} (1000-{cap_val}), h={h} (vật chất đối thủ), f={f}",
                    chosen_move=best_move,
                    current_node=node_info,
                    frontier=sorted_frontier.copy(),
                    explored=explored_list.copy(),
                )
            )

        # Chuyển nút vào danh sách đã kiểm tra
        explored_list.append(node_info)

    return best_move


def ida_star_move(board, recorder=None):
    """
    Thuật toán IDA* (Iterative Deepening A*).
    Kết hợp giữa cơ chế duyệt sâu lặp (Iterative Deepening) và hàm đánh giá của A*.
    Thuật toán duyệt cây tìm kiếm theo chiều sâu nhưng cắt tỉa các nhánh có chi phí f(n) vượt quá ngưỡng (threshold).
    Sau mỗi lần lặp, ngưỡng threshold sẽ được tăng lên bằng giá trị f(n) nhỏ nhất vượt ngưỡng ở lần lặp trước.

    Args:
        board: Trạng thái bàn cờ hiện tại
        recorder: Đối tượng ghi lại các bước tìm kiếm phục vụ trực quan hóa (nếu có)
    """
    # Lấy danh sách các nước đi hợp lệ hiện tại
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None

    random.shuffle(legal_moves)
    step_counter = [0]  # Biến đếm số bước dùng cho việc ghi log
    ai_color = board.turn

    def search(from_pos, to_pos, g, depth, threshold):
        """
        Hàm đệ quy thực hiện tìm kiếm theo chiều sâu với ngưỡng threshold của IDA*.
        """
        # Thử thực hiện nước đi
        board.make_move(from_pos, to_pos, test_only=True)

        # Tính toán heuristic h(n) và f(n)
        h = get_opponent_material(board, ai_color)
        f = g + h

        # Ghi lại bước tìm kiếm nếu có recorder (giới hạn tối đa MAX_VISUALIZATION_STEPS bước)
        if recorder and step_counter[0] < MAX_VISUALIZATION_STEPS:
            recorder.add_step(
                IDAStarStep(
                    step_num=step_counter[0] + 1,
                    algorithm="IDA*",
                    explanation=f"IDA* node {from_pos}→{to_pos}: f={f}, threshold={threshold}, depth={depth}",
                    current_node={"move": (from_pos, to_pos), "g": g, "h": h, "f": f},
                    threshold=threshold,
                    iteration=0,  # Sẽ được cập nhật ở vòng lặp bên ngoài
                    exceeded_f=f if f > threshold else None,
                    is_cutoff=(f > threshold),
                )
            )
            step_counter[0] += 1

        # Nếu chi phí f(n) vượt quá ngưỡng, cắt tỉa nhánh này và trả về f(n)
        if f > threshold:
            board.undo_move(test_only=True)
            return f, None

        # Nếu đã đạt độ sâu tối đa hoặc hết nước đi, trả về kết quả
        if depth == 0 or not board.get_all_legal_moves(board.turn):
            board.undo_move(test_only=True)
            return f, (from_pos, to_pos)

        # Bước đệ quy: tính toán nước đi tiếp theo của đối thủ (next ply).
        # Đối thủ muốn tối đa hóa lợi thế của họ, tức là làm tăng f(n) từ góc nhìn của ta.
        opp_moves = board.get_all_legal_moves(board.turn)
        max_t = -1
        any_cutoff = False

        # Duyệt qua các nước đi của đối thủ
        for ofrom, oto in opp_moves:
            otarg = board.get_piece(oto)
            ocap_val = PIECE_VALUES.get(otarg.name, 0) if otarg else 0

            # Chi phí g(n) từ góc nhìn của ta sẽ tăng lên nếu đối thủ ăn quân của ta
            next_g = g + ocap_val

            t, sol = search(ofrom, oto, next_g, depth - 1, threshold)
            if sol is None:
                any_cutoff = True
                if t > max_t:
                    max_t = t
            else:
                if t > max_t:
                    max_t = t

        board.undo_move(test_only=True)
        if any_cutoff:
            return max_t, None
        return max_t, (from_pos, to_pos)

    # Vòng lặp tăng dần ngưỡng tìm kiếm (Iterative deepening loop)
    threshold = get_opponent_material(board, board.turn)  # Ngưỡng ban đầu là tổng vật chất hiện tại của đối thủ

    for iteration in range(3):  # Giới hạn tối đa 3 lần lặp để tránh thuật toán chạy quá chậm
        if recorder and step_counter[0] < MAX_VISUALIZATION_STEPS:
            recorder.add_step(
                IDAStarStep(
                    step_num=step_counter[0] + 1,
                    algorithm="IDA*",
                    explanation=f"IDA* Iteration {iteration + 1}: threshold={threshold}",
                    iteration=iteration + 1,
                    threshold=threshold,
                )
            )
            step_counter[0] += 1

        min_exceeded = float("inf")
        best_f = float("inf")
        best_move_this_iter = None

        for from_pos, to_pos in legal_moves:
            target = board.get_piece(to_pos)
            cap_val = PIECE_VALUES.get(target.name, 0) if target else 0
            g = 1000 - cap_val

            t, sol = search(from_pos, to_pos, g, 1, threshold)  # Duyệt độ sâu 1 ply
            if sol is not None:
                if t < best_f:
                    best_f = t
                    best_move_this_iter = (from_pos, to_pos)
            else:
                if t < min_exceeded:
                    min_exceeded = t

        if best_move_this_iter is not None:
            return best_move_this_iter

        if min_exceeded == float("inf"):
            break
        threshold = min_exceeded

    return greedy_move(board)  # Dự phòng quay về Greedy nếu vượt giới hạn tìm kiếm

