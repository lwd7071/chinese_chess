# Level 4 AI: Online Search, AND-OR Search, Belief State Search
# Gói chứa các thuật toán tìm kiếm nâng cao trong môi trường động hoặc có yếu tố bất định: Online Search (chỉnh trọng số động), AND-OR Search (tìm kiếm cây điều kiện), và Belief State Search (tìm kiếm theo trạng thái niềm tin).
import random

from ai.level3 import get_perspective_score
from ai.step_recorder import AndOrStep, BeliefStep, OnlineStep

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


def online_search_move(board, recorder=None):
    """
    Thuật toán tìm kiếm trực tuyến (Online Search - Điều chỉnh chiến lược động).
    Dựa trên tình huống thực tế trên bàn cờ để thay đổi trọng số đánh giá quân cờ:
    - Nếu Tướng đang bị chiếu (in check): Tăng mạnh giá trị của Sĩ và Tượng để ưu tiên cố thủ, bảo vệ Tướng.
    - Nếu Tướng an toàn: Tăng giá trị của các quân tấn công (Xe, Pháo, Mã) để ưu tiên thế trận tấn công và kiểm soát trung tâm.

    Args:
        board: Trạng thái bàn cờ hiện tại
        recorder: Đối tượng ghi lại các bước tìm kiếm phục vụ trực quan hóa (nếu có)
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None

    color = board.turn
    in_check = board.is_in_check(color)

    # Định nghĩa bộ trọng số chuẩn ban đầu
    weights_before = {
        "general": 10000,
        "rook": 900,
        "cannon": 450,
        "horse": 300,
        "elephant": 200,
        "advisor": 200,
        "pawn": 100,
    }

    if in_check:
        # Tướng bị chiếu: Tăng giá trị Sĩ (200 -> 400) và Tượng (200 -> 350) nhằm bọc lót
        weights_after = weights_before.copy()
        weights_after["advisor"] = 400
        weights_after["elephant"] = 350
    else:
        # Tướng an toàn: Tăng giá trị các quân chủ lực Xe (900 -> 1100), Pháo (450 -> 550), Mã (300 -> 400)
        weights_after = weights_before.copy()
        weights_after["rook"] = 1100
        weights_after["cannon"] = 550
        weights_after["horse"] = 400

    # Ghi lại bước khởi tạo và điều chỉnh trọng số nếu có recorder
    if recorder:
        recorder.add_step(
            OnlineStep(
                step_num=1,
                algorithm="Online Search",
                explanation=f"{'⚠️ Đang bị chiếu' if in_check else '✅ An toàn'} → Điều chỉnh trọng số động",
                in_check=in_check,
                weights_before=weights_before,
                weights_after=weights_after,
                candidates=[],
            )
        )

    # Can thiệp tạm thời vào bảng PIECE_VALUES trong module ai.eval
    import ai.eval as eval_mod

    original_values = eval_mod.PIECE_VALUES.copy()
    eval_mod.PIECE_VALUES.update(
        {
            "general": weights_after["general"],
            "rook": weights_after["rook"],
            "cannon": weights_after["cannon"],
            "horse": weights_after["horse"],
            "elephant": weights_after["elephant"],
            "advisor": weights_after["advisor"],
            "pawn": weights_after["pawn"],
        }
    )

    # Chạy thuật toán tìm kiếm (theo mô hình Hill Climbing) với hàm đánh giá đã thay đổi trọng số
    best_move = None
    best_score = float("-inf")
    random.shuffle(legal_moves)
    candidates = []

    for _i, (from_pos, to_pos) in enumerate(legal_moves):
        piece_name = _get_piece_name(board, from_pos)
        board.make_move(from_pos, to_pos, test_only=True)
        score = get_perspective_score(board, color)
        board.undo_move(test_only=True)

        candidates.append({"move": (from_pos, to_pos), "score": score, "piece": piece_name})

        if score > best_score:
            best_score = score
            best_move = (from_pos, to_pos)

    # Ghi lại bước lựa chọn nước đi tốt nhất
    if recorder:
        sorted_candidates = sorted(candidates, key=lambda x: x["score"], reverse=True)[
            :10
        ]
        recorder.add_step(
            OnlineStep(
                step_num=2,
                algorithm="Online Search",
                explanation=f"Chọn nước tốt nhất với trọng số mới: score={best_score:.0f}",
                chosen_move=best_move,
                in_check=in_check,
                weights_before=weights_before,
                weights_after=weights_after,
                candidates=sorted_candidates,
            )
        )

    # Khôi phục lại giá trị gốc của bảng PIECE_VALUES
    eval_mod.PIECE_VALUES.update(original_values)
    return best_move


def and_or_search_move(board, recorder=None):
    """
    Thuật toán tìm kiếm AND-OR (AND-OR Tree Search).
    Thích hợp cho các trò chơi có tính đối kháng và hoàn toàn quan sát được như Cờ tướng.
    Quy tắc giải thích:
    - Các nút OR (OR nodes): Lượt của AI (chọn ra nước đi mang lại kết quả tốt nhất trong các lựa chọn).
    - Các nút AND (AND nodes): Lượt của đối thủ (AI phải đối phó với TẤT CẢ các nước đi phản đòn có thể có của đối thủ).

    Thuật toán tìm kiếm nước đi có khả năng đảm bảo kết quả tệ nhất (worst-case) là cao nhất.

    Args:
        board: Trạng thái bàn cờ hiện tại
        recorder: Đối tượng ghi lại các bước tìm kiếm phục vụ trực quan hóa (nếu có)
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None

    color = board.turn
    random.shuffle(legal_moves)
    best_move = legal_moves[0]
    best_guaranteed_score = float("-inf")

    # Kiểm tra toàn bộ các nước đi hợp lệ để tìm nước đi có bảo đảm worst-case tốt nhất
    for i, (from_pos, to_pos) in enumerate(legal_moves):
        or_piece_name = _get_piece_name(board, from_pos)
        board.make_move(from_pos, to_pos, test_only=True)

        opp_moves = board.get_all_legal_moves(board.turn)
        and_responses = []

        if not opp_moves:
            # Đối thủ bị chiếu hết - phần thắng thuộc về AI!
            worst_case_score = float("inf")
            worst_case_move = None
            worst_case_piece = "—"
        else:
            worst_case_score = float("inf")
            worst_case_move = None
            worst_case_piece = "—"
            # Đối thủ đóng vai trò nút AND, luôn đi nước làm tối thiểu hóa điểm số của AI
            for ofrom, oto in opp_moves:
                opp_piece = _get_piece_name(board, ofrom)
                board.make_move(ofrom, oto, test_only=True)
                us_score = get_perspective_score(board, color)
                board.undo_move(test_only=True)

                and_responses.append({"move": (ofrom, oto), "score": us_score, "piece": opp_piece})

                if us_score < worst_case_score:
                    worst_case_score = us_score
                    worst_case_move = (ofrom, oto)
                    worst_case_piece = opp_piece

        board.undo_move(test_only=True)

        # Ghi lại bước tìm kiếm nếu có recorder (giới hạn hiển thị 10 bước)
        if recorder and i < 10:
            recorder.add_step(
                AndOrStep(
                    step_num=i + 1,
                    algorithm="AND-OR Search",
                    explanation=f"OR node: {from_pos}→{to_pos}, worst-case score={worst_case_score:.0f}",
                    chosen_move=best_move
                    if worst_case_score > best_guaranteed_score
                    else None,
                    or_node={
                        "move": (from_pos, to_pos),
                        "responses_count": len(and_responses),
                        "piece": or_piece_name,
                    },
                    and_responses=and_responses[:5],  # Giới hạn 5 phản đòn để tránh rối mắt trên giao diện
                    worst_case={"move": worst_case_move, "score": worst_case_score, "piece": worst_case_piece}
                    if worst_case_move
                    else {},
                    guaranteed_score=worst_case_score,
                )
            )

        # Lựa chọn nước đi giúp AI có điểm bảo đảm (guaranteed score) cao nhất
        if worst_case_score > best_guaranteed_score:
            best_guaranteed_score = worst_case_score
            best_move = (from_pos, to_pos)

    return best_move


def belief_state_search_move(board, recorder=None):
    """
    Thuật toán tìm kiếm Không gian niềm tin (Belief State Search).
    Thuật toán duy trì một phân phối xác suất niềm tin về phong cách/chiến lược hiện tại của đối thủ:
    - Phong cách Hổ báo / Tấn công (Aggressive): Ưu tiên ăn quân (50% hoặc 60% tùy lịch sử).
    - Phong cách Phòng ngự (Defensive): Ưu tiên bảo vệ quân và cung Tướng (30% hoặc 60%).
    - Phong cách Trận địa (Positional): Ưu tiên chiếm lĩnh không gian, khu vực trung tâm (20% hoặc 60%).
    AI tính toán độ thỏa dụng kỳ vọng (Expected Utility) trên các phân phối này và chọn nước đi có kỳ vọng cao nhất.

    Args:
        board: Trạng thái bàn cờ hiện tại
        recorder: Đối tượng ghi lại các bước tìm kiếm phục vụ trực quan hóa (nếu có)
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None

    color = board.turn
    random.shuffle(legal_moves)

    # Phân tích lịch sử nước đi gần nhất của đối thủ để tự động cập nhật phân phối niềm tin
    # Ví dụ: nếu đối thủ vừa ăn quân, khả năng cao họ đang theo phong cách Aggressive.
    opp_style = "aggressive"
    if board.history:
        _, to_pos, captured, _ = board.history[-1]
        if captured:
            opp_style = "aggressive"
        else:
            # Nếu lùi hoặc đi quân trong cung tướng thì khả năng là Defensive, ngược lại là Positional
            opp_style = "defensive" if to_pos[0] in [0, 1, 2, 7, 8, 9] else "positional"

    # Gán trọng số xác suất dựa trên phong cách dự đoán được
    if opp_style == "aggressive":
        p_agg, p_def, p_pos = 0.6, 0.2, 0.2
    elif opp_style == "defensive":
        p_agg, p_def, p_pos = 0.2, 0.6, 0.2
    else:
        p_agg, p_def, p_pos = 0.2, 0.2, 0.6

    # Ghi lại phong cách đối thủ phát hiện được
    if recorder:
        recorder.add_step(
            BeliefStep(
                step_num=1,
                algorithm="Belief State",
                explanation=f"Phát hiện phong cách đối thủ: {opp_style.upper()}",
                opponent_style=opp_style,
                belief_probs={
                    "aggressive": p_agg,
                    "defensive": p_def,
                    "positional": p_pos,
                },
                utility_per_style={},
                expected_utility=0.0,
            )
        )

    # Hàm phụ trợ tính toán độ thỏa dụng (score) của bàn cờ tùy theo góc nhìn của từng phong cách
    def get_strategy_score(board, style):
        base = get_perspective_score(board, color)
        if style == "aggressive":
            # Giá trị vật chất đóng vai trò chủ đạo
            return base * 1.5
        elif style == "defensive":
            # Sự an toàn của Tướng đóng vai trò chủ đạo
            g_pos = board.get_general_pos(color)
            if g_pos:
                # Cộng điểm nếu có nhiều quân đồng minh đứng xung quanh bảo vệ Tướng
                defenders = 0
                gr, gc = g_pos
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        p = board.get_piece((gr + dr, gc + dc))
                        if p and p.color == color:
                            defenders += 1
                return base + defenders * 50
            return base
        else:  # Phong cách Trận địa (positional - kiểm soát trung tâm)
            # Thưởng điểm cho Tốt và Mã chiếm lĩnh khu vực trung tâm bàn cờ
            center_score = 0
            for r in range(3, 7):
                for c in range(2, 7):
                    p = board.matrix[r][c]
                    if p and p.color == color:
                        center_score += 30
            return base + center_score

    best_move = legal_moves[0]
    best_expected_utility = float("-inf")

    # Duyệt qua các nước đi để tính độ thỏa dụng kỳ vọng
    for from_pos, to_pos in legal_moves:
        board.make_move(from_pos, to_pos, test_only=True)

        # Tính độ thỏa dụng cho từng tình huống phong cách
        u_agg = get_strategy_score(board, "aggressive")
        u_def = get_strategy_score(board, "defensive")
        u_pos = get_strategy_score(board, "positional")

        # Độ thỏa dụng kỳ vọng E[U] = tổng (xác suất * độ thỏa dụng)
        expected_utility = p_agg * u_agg + p_def * u_def + p_pos * u_pos
        board.undo_move(test_only=True)

        if expected_utility > best_expected_utility:
            best_expected_utility = expected_utility
            best_move = (from_pos, to_pos)

    # Ghi lại bước lựa chọn nước đi cuối cùng
    if recorder:
        board.make_move(best_move[0], best_move[1], test_only=True)
        u_agg = get_strategy_score(board, "aggressive")
        u_def = get_strategy_score(board, "defensive")
        u_pos = get_strategy_score(board, "positional")
        board.undo_move(test_only=True)

        recorder.add_step(
            BeliefStep(
                step_num=2,
                algorithm="Belief State",
                explanation=f"E[U]={best_expected_utility:.0f} = {p_agg:.1f}*{u_agg:.0f} + {p_def:.1f}*{u_def:.0f} + {p_pos:.1f}*{u_pos:.0f}",
                chosen_move=best_move,
                opponent_style=opp_style,
                belief_probs={
                    "aggressive": p_agg,
                    "defensive": p_def,
                    "positional": p_pos,
                },
                utility_per_style={
                    "aggressive": u_agg,
                    "defensive": u_def,
                    "positional": u_pos,
                },
                expected_utility=best_expected_utility,
            )
        )

    return best_move
