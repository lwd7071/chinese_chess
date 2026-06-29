# Level 5 AI: Backtracking CSP (MRV), Min-Conflicts, AC-3
# Gói chứa các thuật toán giải quyết bài toán Thỏa mãn Ràng buộc (Constraint Satisfaction Problems - CSP): Quay lui với mảng chọn MRV (Backtracking MRV), Tối thiểu hóa xung đột (Min-Conflicts), và Tương thích cung AC-3 (Arc Consistency).
import random

from ai.eval import PIECE_VALUES
from ai.level3 import get_perspective_score
from ai.step_recorder import AC3Step, BacktrackStep, MinConflictStep

# Bảng dịch tên các quân cờ sang tiếng Việt phục vụ hiển thị trực quan
PIECE_NAME_VI = {
    "general": "Tướng",
    "advisor": "Sĩ",
    "elephant": "Tượng",
    "horse": "Mã",
    "rook": "Xe",
    "cannon": "Pháo",
    "pawn": "Tốt",
}


def _get_piece_name(board, pos):
    """
    Hàm phụ trợ lấy tên quân cờ tiếng Việt từ vị trí trên bàn cờ.

    Args:
        board: Trạng thái bàn cờ
        pos: Tọa độ (hàng, cột) của quân cờ
    """
    if not pos:
        return "—"
    piece = board.get_piece(pos)
    if not piece:
        return "—"
    char_to_key = {
        "G": "general",
        "A": "advisor",
        "E": "elephant",
        "H": "horse",
        "R": "rook",
        "C": "cannon",
        "P": "pawn",
    }
    key = char_to_key.get(piece.name, piece.name)
    return PIECE_NAME_VI.get(key, "—")


def get_threats_count(board, color):
    """
    Hàm tính toán số lượng quân cờ của một phe (color) đang bị đối phương đe dọa (tấn công trực tiếp).
    Được sử dụng làm hàm chi phí (conflicts) trong thuật toán Min-Conflicts.

    Args:
        board: Trạng thái bàn cờ
        color: Màu quân của phe cần kiểm tra ('red' hoặc 'black')
    """
    opp = "black" if color == "red" else "red"
    threatened = set()

    # Tạo toàn bộ các nước đi/tấn công thô (raw moves) của đối thủ
    for r in range(10):
        for c in range(9):
            p = board.matrix[r][c]
            if p and p.color == opp:
                raw_moves = p.get_raw_moves(board.matrix)
                for tr, tc in raw_moves:
                    targ = board.matrix[tr][tc]
                    if targ and targ.color == color:
                        threatened.add(targ.pos)

    return len(threatened)


def backtracking_mrv_move(board, recorder=None):
    """
    Thuật toán Quay lui kết hợp Heuristic MRV (Minimum Remaining Values).
    Mô hình hóa dưới dạng bài toán CSP:
    - Biến (Variables): Các quân cờ hiện tại có ít nhất 1 nước đi hợp lệ.
    - Miền giá trị (Domain): Danh sách các vị trí đích đến hợp lệ của quân cờ đó.
    Heuristic MRV: Ưu tiên chọn Biến (quân cờ) có miền giá trị nhỏ nhất (ít nước đi nhất) để xử lý trước.
    Sau đó, chọn giá trị (nước đi) mang lại điểm số đánh giá cao nhất.

    Args:
        board: Trạng thái bàn cờ hiện tại
        recorder: Đối tượng ghi lại các bước tìm kiếm phục vụ trực quan hóa (nếu có)
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None

    color = board.turn

    # Lập bản đồ ánh xạ từ vị trí quân cờ (tên Biến) đến danh sách các nước đi (Miền giá trị)
    var_domains = {}
    for from_pos, to_pos in legal_moves:
        if from_pos not in var_domains:
            var_domains[from_pos] = []
        var_domains[from_pos].append(to_pos)

    # Ghi lại thông tin toàn bộ các Biến và kích thước Miền giá trị tương ứng
    if recorder:
        variables_info = {str(pos): len(domain) for pos, domain in var_domains.items()}
        recorder.add_step(
            BacktrackStep(
                step_num=1,
                algorithm="Backtracking MRV",
                explanation=f"Tính domain size cho {len(var_domains)} biến (quân cờ)",
                variables=variables_info,
            )
        )

    # Heuristic MRV: Chọn biến (tọa độ quân cờ) có domain nhỏ nhất (ít sự lựa chọn nhất)
    chosen_var = min(var_domains.keys(), key=lambda x: len(var_domains[x]))
    domain_list = []

    # Tìm giá trị (to_pos) tốt nhất cho biến vừa chọn dựa trên điểm đánh giá bàn cờ
    best_to = var_domains[chosen_var][0]
    best_score = float("-inf")

    piece_name = _get_piece_name(board, chosen_var)
    for to_pos in var_domains[chosen_var]:
        board.make_move(chosen_var, to_pos, test_only=True)
        score = get_perspective_score(board, color)
        board.undo_move(test_only=True)

        domain_list.append({"move": (chosen_var, to_pos), "score": score, "piece": piece_name})

        if score > best_score:
            best_score = score
            best_to = to_pos

    # Ghi lại quyết định chọn biến MRV và giá trị gán tốt nhất
    if recorder:
        recorder.add_step(
            BacktrackStep(
                step_num=2,
                algorithm="Backtracking MRV",
                explanation=f"MRV chọn biến {chosen_var} (domain={len(var_domains[chosen_var])} - nhỏ nhất), score={best_score:.0f}",
                chosen_move=(chosen_var, best_to),
                variables={
                    str(pos): len(domain) for pos, domain in var_domains.items()
                },
                chosen_variable=str(chosen_var),
                domain=domain_list,
                best_assignment={"move": (chosen_var, best_to), "score": best_score, "piece": piece_name},
            )
        )

    return (chosen_var, best_to)


def min_conflicts_move(board, recorder=None):
    """
    Thuật toán Tối thiểu hóa Xung đột (Min-Conflicts).
    Trong bài toán này: Xung đột (Conflicts) = Số lượng quân cờ của ta đang bị đối phương đe dọa.
    Thuật toán chọn ra nước đi làm giảm thiểu tối đa số lượng xung đột hiện tại trên bàn cờ.
    Nếu các nước đi có số lượng xung đột bằng nhau, sử dụng điểm số đánh giá bàn cờ để phá vỡ thế cân bằng (break ties).

    Args:
        board: Trạng thái bàn cờ hiện tại
        recorder: Đối tượng ghi lại các bước tìm kiếm phục vụ trực quan hóa (nếu có)
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None

    color = board.turn
    random.shuffle(legal_moves)

    # Đếm số lượng xung đột ban đầu trước khi đi
    current_conflicts = get_threats_count(board, color)

    best_move = legal_moves[0]
    min_conflicts = float("inf")

    # Điểm đánh giá dùng để so sánh giữa các nước đi có cùng số lượng xung đột
    best_score = float("-inf")
    candidates = []

    # Thử từng nước đi và tính toán số lượng xung đột còn lại
    for from_pos, to_pos in legal_moves:
        piece_name = _get_piece_name(board, from_pos)
        board.make_move(from_pos, to_pos, test_only=True)
        conflicts = get_threats_count(board, color)
        score = get_perspective_score(board, color)
        board.undo_move(test_only=True)

        candidates.append(
            {"move": (from_pos, to_pos), "conflicts_after": conflicts, "score": score, "piece": piece_name}
        )

        if conflicts < min_conflicts:
            min_conflicts = conflicts
            best_move = (from_pos, to_pos)
            best_score = score
        elif conflicts == min_conflicts:
            if score > best_score:
                best_score = score
                best_move = (from_pos, to_pos)

    # Ghi lại kết quả tìm kiếm Min-Conflicts
    if recorder:
        sorted_candidates = sorted(
            candidates, key=lambda x: (x["conflicts_after"], -x["score"])
        )[:10]
        best_piece_name = _get_piece_name(board, best_move[0])
        recorder.add_step(
            MinConflictStep(
                step_num=1,
                algorithm="Min-Conflicts",
                explanation=f"Conflicts trước={current_conflicts}, sau={min_conflicts} (giảm {current_conflicts - min_conflicts})",
                chosen_move=best_move,
                current_conflicts=current_conflicts,
                candidates=sorted_candidates,
                best_candidate={
                    "move": best_move,
                    "conflicts_after": min_conflicts,
                    "score": best_score,
                    "piece": best_piece_name,
                },
            )
        )

    return best_move


def ac3_move(board, recorder=None):
    """
    Thuật toán Tương thích Cung AC-3 (Arc Consistency 3).
    Thuật toán kiểm tra và cắt tỉa (prune) các nước đi dẫn đến ô cờ không an toàn (bị kiểm soát bởi quân địch có giá trị thấp hơn).
    Ví dụ: Xe di chuyển vào ô đang bị Tốt hoặc Pháo đối phương kiểm soát sẽ bị loại bỏ ngay lập tức (tránh các pha đổi quân lỗ).
    Sau khi loại bỏ các nước đi rủi ro, thuật toán chọn ra nước đi tốt nhất trong số các nước đi an toàn (safe moves).
    Nếu tất cả các nước đi đều bị loại bỏ, thuật toán sử dụng lại danh sách ban đầu làm phương án dự phòng (fallback).

    Args:
        board: Trạng thái bàn cờ hiện tại
        recorder: Đối tượng ghi lại các bước tìm kiếm phục vụ trực quan hóa (nếu có)
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None

    color = board.turn
    opp = "black" if color == "red" else "red"

    # Lọc danh sách các nước đi an toàn (AC-3 arc check)
    safe_moves = []
    pruned_moves = []

    for from_pos, to_pos in legal_moves:
        piece = board.get_piece(from_pos)
        p_val = PIECE_VALUES.get(piece.name, 0)

        # Mô phỏng nước đi
        board.make_move(from_pos, to_pos, test_only=True)

        # Kiểm tra xem ô đích đến có nằm trong tầm ngắm của quân đối phương rẻ hơn hay không
        is_unsafe = False
        attacker_name = None
        for r in range(10):
            for c in range(9):
                p = board.matrix[r][c]
                if p and p.color == opp:
                    if to_pos in p.get_raw_moves(board.matrix):
                        # Quân địch có thể ăn được quân ta tại vị trí đích
                        opp_val = PIECE_VALUES.get(p.name, 0)
                        if opp_val < p_val:
                            # Đổi quân bất lợi! (VD: Xe bị Pháo/Tốt ăn)
                            is_unsafe = True
                            attacker_name = p.name
                            break
            if is_unsafe:
                break

        board.undo_move(test_only=True)

        if not is_unsafe:
            safe_moves.append((from_pos, to_pos))
        else:
            char_to_key = {
                "G": "general", "A": "advisor", "E": "elephant",
                "H": "horse", "R": "rook", "C": "cannon", "P": "pawn",
            }
            p_key = char_to_key.get(piece.name, piece.name)
            a_key = char_to_key.get(attacker_name, attacker_name) if attacker_name else ""
            p_vi = PIECE_NAME_VI.get(p_key, p_key)
            a_vi = PIECE_NAME_VI.get(a_key, a_key)
            pruned_moves.append(
                {
                    "move": (from_pos, to_pos),
                    "reason": f"{p_vi}({p_val}) bị {a_vi}({PIECE_VALUES.get(attacker_name, 0)}) ăn",
                    "piece": p_vi,
                }
            )

    # Chọn từ danh sách an toàn nếu có, nếu không thì dùng danh sách gốc
    candidates = safe_moves if safe_moves else legal_moves

    random.shuffle(candidates)
    best_move = candidates[0]
    best_score = float("-inf")

    # Đánh giá điểm số để chọn ra nước đi tối ưu nhất
    for from_pos, to_pos in candidates:
        board.make_move(from_pos, to_pos, test_only=True)
        score = get_perspective_score(board, color)
        board.undo_move(test_only=True)
        if score > best_score:
            best_score = score
            best_move = (from_pos, to_pos)

    # Ghi lại bước lọc AC-3 và sự lựa chọn nước đi
    if recorder:
        recorder.add_step(
            AC3Step(
                step_num=1,
                algorithm="AC-3",
                explanation=f"Lọc {len(pruned_moves)}/{len(legal_moves)} nước không an toàn, còn {len(safe_moves)} nước an toàn",
                chosen_move=best_move,
                all_moves=len(legal_moves),
                safe_moves=[
                    {"move": m, "score": best_score if m == best_move else 0, "piece": _get_piece_name(board, m[0])}
                    for m in safe_moves[:10]
                ],
                pruned_moves=pruned_moves[:10],
                chosen_from_safe={"move": best_move, "score": best_score, "piece": _get_piece_name(board, best_move[0])},
            )
        )

    return best_move
