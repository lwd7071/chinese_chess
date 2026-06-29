# Level 6 AI: Minimax, Alpha-Beta Pruning, Expectimax
# Gói chứa các thuật toán tìm kiếm đối kháng kinh điển trên cây trò chơi: Minimax (duyệt cạn theo chiều sâu), Alpha-Beta Pruning (cắt tỉa nhánh tối ưu), và Expectimax (tìm kiếm với nút cơ hội/xác suất).
import time

from ai.eval import PIECE_VALUES, evaluate_board
from ai.step_recorder import (
    MAX_VISUALIZATION_STEPS,
    AlphaBetaStep,
    ExpectimaxStep,
    MinimaxStep,
    move_to_label,
)


def safe_format(val):
    """
    Hàm định dạng chuỗi an toàn cho các giá trị số hoặc vô cực (inf, -inf)
    để hiển thị trực quan đẹp mắt trên giao diện người dùng.
    """
    if val == float("inf"):
        return "∞"
    if val == float("-inf"):
        return "-∞"
    try:
        return f"{val:.0f}"
    except Exception:
        return str(val)


def sort_moves(board, moves):
    """
    Hàm sắp xếp các nước đi ưu tiên nhằm tối ưu hóa thuật toán cắt tỉa Alpha-Beta:
    Các nước đi mang tính chất ăn quân (captures) sẽ được xếp lên đầu, giúp nhanh chóng
    tìm thấy mốc alpha/beta tốt để cắt tỉa các nhánh không cần thiết.

    Args:
        board: Trạng thái bàn cờ
        moves: Danh sách các nước đi cần sắp xếp
    """

    def score_move(m):
        from_pos, to_pos = m
        targ = board.get_piece(to_pos)
        if targ:
            return 1000 + PIECE_VALUES.get(targ.name, 0)
        return 0

    return sorted(moves, key=score_move, reverse=True)


def minimax_move(board, depth=3, recorder=None):
    """
    Thuật toán Minimax với giới hạn độ sâu (Depth-limited Minimax Search).
    Dựa trên giả định đối thủ luôn chơi tối ưu để tối thiểu hóa điểm số của chúng ta:
    - Nút MAX (MAX nodes): Lượt của AI, cố gắng chọn nước đi có điểm số lớn nhất.
    - Nút MIN (MIN nodes): Lượt của đối thủ, cố gắng chọn nước đi làm điểm số của ta nhỏ nhất.

    Args:
        board: Trạng thái bàn cờ hiện tại
        depth: Độ sâu tìm kiếm tối đa
        recorder: Đối tượng ghi lại các bước tìm kiếm phục vụ trực quan hóa (nếu có)
    """
    color = board.turn
    legal_moves = board.get_all_legal_moves(color)
    if not legal_moves:
        return None

    # Sắp xếp các nước đi ưu tiên ăn quân để tăng hiệu quả duyệt
    sorted_moves = sort_moves(board, legal_moves)
    best_move = sorted_moves[0]
    best_score = float("-inf") if color == "red" else float("inf")

    step_counter = [0]

    def search(b, d, is_max, path):
        # Dừng tìm kiếm khi đạt độ sâu 0
        if d == 0:
            return evaluate_board(b)

        moves = b.get_all_legal_moves(b.turn)
        if not moves:
            # Hết nước đi hợp lệ (bị chiếu hết hoặc hòa)
            return float("-inf") if is_max else float("inf")

        # Giới hạn hệ số rẽ nhánh (branching factor) 12 nước tốt nhất để đảm bảo tốc độ
        ordered = sort_moves(b, moves)[:12]
        siblings = []

        if is_max:
            # Lượt của MAX: Tìm giá trị lớn nhất
            max_val = float("-inf")
            for m in ordered:
                b.make_move(m[0], m[1], test_only=True)
                val = search(b, d - 1, False, path + [m])
                b.undo_move(test_only=True)
                max_val = max(max_val, val)
                siblings.append({"move": m, "value": val})

                # Ghi lại thông tin nút MAX vào nhật ký
                if recorder and step_counter[0] < MAX_VISUALIZATION_STEPS:
                    recorder.add_step(
                        MinimaxStep(
                            step_num=step_counter[0] + 1,
                            algorithm="Minimax",
                            explanation=f"Minimax MAX node depth={d}, xét {move_to_label(m)}: value={val:.0f}",
                            current_node={
                                "move": m,
                                "depth": d,
                                "is_max": True,
                                "value": val,
                            },
                            current_path=[
                                {"move": p, "depth": depth - len(path) + i}
                                for i, p in enumerate(path + [m])
                            ],
                            siblings_evaluated=siblings.copy(),
                            best_so_far={"move": m, "value": max_val},
                            evaluated=siblings.copy(),
                        )
                    )
                    step_counter[0] += 1
            return max_val
        else:
            # Lượt của MIN: Tìm giá trị nhỏ nhất (đối thủ đi)
            min_val = float("inf")
            for m in ordered:
                b.make_move(m[0], m[1], test_only=True)
                val = search(b, d - 1, True, path + [m])
                b.undo_move(test_only=True)
                min_val = min(min_val, val)
                siblings.append({"move": m, "value": val})

                # Ghi lại thông tin nút MIN vào nhật ký
                if recorder and step_counter[0] < MAX_VISUALIZATION_STEPS:
                    recorder.add_step(
                        MinimaxStep(
                            step_num=step_counter[0] + 1,
                            algorithm="Minimax",
                            explanation=f"Minimax MIN node depth={d}, xét {move_to_label(m)}: value={val:.0f}",
                            current_node={
                                "move": m,
                                "depth": d,
                                "is_max": False,
                                "value": val,
                            },
                            current_path=[
                                {"move": p, "depth": depth - len(path) + i}
                                for i, p in enumerate(path + [m])
                            ],
                            siblings_evaluated=siblings.copy(),
                            best_so_far={"move": m, "value": min_val},
                            evaluated=siblings.copy(),
                        )
                    )
                    step_counter[0] += 1
            return min_val

    # Gọi hàm search cho các nước đi gốc (Root node)
    for m in sorted_moves[:15]:
        board.make_move(m[0], m[1], test_only=True)
        # Nếu AI là phe Đỏ (MAX), lượt tiếp theo là Đen (MIN, is_max=False)
        score = search(board, depth - 1, color == "black", [m])
        board.undo_move(test_only=True)

        if color == "red":
            if score > best_score:
                best_score = score
                best_move = m
        else:  # Black (nếu AI chơi phe Đen thì tìm điểm số nhỏ nhất vì evaluate_board tính theo Đỏ)
            if score < best_score:
                best_score = score
                best_move = m

    return best_move


def alpha_beta_move(board, depth=4, recorder=None):
    """
    Thuật toán Minimax kết hợp Cắt tỉa Alpha-Beta (Alpha-Beta Pruning).
    Giúp giảm thiểu đáng kể các nhánh tìm kiếm không cần thiết mà vẫn đảm bảo ra kết quả giống hệt Minimax.
    - Alpha (α): Giá trị tốt nhất (cao nhất) mà phe MAX có thể đảm bảo đạt được tính đến hiện tại.
    - Beta (β): Giá trị tốt nhất (thấp nhất) mà phe MIN có thể đảm bảo đạt được tính đến hiện tại.
    Điều kiện cắt tỉa: Khi β ≤ α, ta có thể cắt nhánh (prune) vì đối thủ sẽ không bao giờ cho phép nhánh đó xảy ra.

    Args:
        board: Trạng thái bàn cờ hiện tại
        depth: Độ sâu tìm kiếm tối đa (thường đi sâu hơn Minimax nhờ cắt tỉa)
        recorder: Đối tượng ghi lại các bước tìm kiếm phục vụ trực quan hóa (nếu có)
    """
    color = board.turn
    legal_moves = board.get_all_legal_moves(color)
    if not legal_moves:
        return None

    sorted_moves = sort_moves(board, legal_moves)
    best_move = sorted_moves[0]
    best_score = float("-inf") if color == "red" else float("inf")

    step_counter = [0]  # Phục vụ ghi nhật ký

    def search(b, d, alpha, beta, is_max, path):
        if d == 0:
            return evaluate_board(b)

        moves = b.get_all_legal_moves(b.turn)
        if not moves:
            return float("-inf") if is_max else float("inf")

        # Cho phép mở rộng nhánh nhiều hơn (15 nước) nhờ hiệu quả cắt tỉa
        ordered = sort_moves(b, moves)[:15]
        siblings = []

        if is_max:
            max_val = float("-inf")
            for m in ordered:
                b.make_move(m[0], m[1], test_only=True)
                val = search(b, d - 1, alpha, beta, False, path + [m])
                b.undo_move(test_only=True)

                siblings.append({"move": m, "value": val})
                max_val = max(max_val, val)
                old_alpha = alpha
                alpha = max(alpha, max_val)

                # Ghi lại bước đi và cập nhật trạng thái Alpha/Beta
                if recorder and step_counter[0] < MAX_VISUALIZATION_STEPS:
                    is_pruned = beta <= alpha
                    recorder.add_step(
                        AlphaBetaStep(
                            step_num=step_counter[0] + 1,
                            algorithm="Alpha-Beta",
                            explanation=f"Alpha-Beta MAX node depth={d}, xét {move_to_label(m)}: α={safe_format(old_alpha)}→{safe_format(alpha)}, β={safe_format(beta)}"
                            + (" → Cắt tỉa!" if is_pruned else ""),
                            current_node={
                                "move": m,
                                "depth": d,
                                "is_max": True,
                                "value": val,
                            },
                            current_path=[
                                {"move": p, "depth": depth - len(path) + i}
                                for i, p in enumerate(path + [m])
                            ],
                            alpha=alpha,
                            beta=beta,
                            is_pruned=is_pruned,
                            prune_reason=f"β({safe_format(beta)}) ≤ α({safe_format(alpha)}) → cắt nhánh"
                            if is_pruned
                            else "",
                            siblings_evaluated=siblings.copy(),
                            evaluated=siblings.copy(),
                        )
                    )
                    step_counter[0] += 1

                # Điều kiện cắt tỉa Beta (Beta cutoff)
                if beta <= alpha:
                    break
            return max_val
        else:
            min_val = float("inf")
            for m in ordered:
                b.make_move(m[0], m[1], test_only=True)
                val = search(b, d - 1, alpha, beta, True, path + [m])
                b.undo_move(test_only=True)

                siblings.append({"move": m, "value": val})
                min_val = min(min_val, val)
                old_beta = beta
                beta = min(beta, min_val)

                # Ghi lại bước đi và cập nhật trạng thái Alpha/Beta
                if recorder and step_counter[0] < MAX_VISUALIZATION_STEPS:
                    is_pruned = beta <= alpha
                    recorder.add_step(
                        AlphaBetaStep(
                            step_num=step_counter[0] + 1,
                            algorithm="Alpha-Beta",
                            explanation=f"Alpha-Beta MIN node depth={d}, xét {move_to_label(m)}: α={safe_format(alpha)}, β={safe_format(old_beta)}→{safe_format(beta)}"
                            + (" → Cắt tỉa!" if is_pruned else ""),
                            current_node={
                                "move": m,
                                "depth": d,
                                "is_max": False,
                                "value": val,
                            },
                            current_path=[
                                {"move": p, "depth": depth - len(path) + i}
                                for i, p in enumerate(path + [m])
                            ],
                            alpha=alpha,
                            beta=beta,
                            is_pruned=is_pruned,
                            prune_reason=f"β({safe_format(beta)}) ≤ α({safe_format(alpha)}) → cắt nhánh"
                            if is_pruned
                            else "",
                            siblings_evaluated=siblings.copy(),
                            evaluated=siblings.copy(),
                        )
                    )
                    step_counter[0] += 1

                # Điều kiện cắt tỉa Alpha (Alpha cutoff)
                if beta <= alpha:
                    break
            return min_val

    # Vòng lặp gốc (Root call)
    alpha = float("-inf")
    beta = float("inf")

    for m in sorted_moves[:20]:
        board.make_move(m[0], m[1], test_only=True)
        score = search(board, depth - 1, alpha, beta, color == "black", [m])
        board.undo_move(test_only=True)

        if color == "red":
            if score > best_score:
                best_score = score
                best_move = m
            alpha = max(alpha, score)
        else:  # Black
            if score < best_score:
                best_score = score
                best_move = m
            beta = min(beta, score)

    return best_move


def expectimax_move(board, depth=3, recorder=None):
    """
    Thuật toán Expectimax (Tìm kiếm Kỳ vọng).
    Sử dụng khi đối thủ không hoàn toàn chơi tối ưu (có yếu tố ngẫu nhiên hoặc sai lầm).
    Mô hình hóa đối thủ qua các nút Cơ hội (Chance nodes) với giả định xác suất:
    - 70% khả năng đối thủ sẽ đi nước đi tối ưu nhất (theo chuẩn Minimax).
    - 30% khả năng đối thủ sẽ đi một nước đi bất kỳ trong số các lựa chọn còn lại.
    Giá trị tại nút Cơ hội là Giá trị Kỳ vọng (Expected Value - E[V]).

    Args:
        board: Trạng thái bàn cờ hiện tại
        depth: Độ sâu tìm kiếm tối đa
        recorder: Đối tượng ghi lại các bước tìm kiếm phục vụ trực quan hóa (nếu có)
    """
    ai_color = board.turn
    legal_moves = board.get_all_legal_moves(ai_color)
    if not legal_moves:
        return None

    sorted_moves = sort_moves(board, legal_moves)
    best_move = sorted_moves[0]
    best_score = float("-inf") if ai_color == "red" else float("inf")

    step_counter = [0]

    def search(b, d, is_ai_turn):
        if d == 0:
            return evaluate_board(b)

        moves = b.get_all_legal_moves(b.turn)
        if not moves:
            # Kiểm tra phân định thắng thua
            if b.turn == ai_color:
                return float("-inf") if ai_color == "red" else float("inf")
            else:
                return float("inf") if ai_color == "red" else float("-inf")

        ordered = sort_moves(b, moves)[:10]

        if is_ai_turn:
            # Lượt của AI: Tối ưu hóa theo màu quân của AI
            if ai_color == "red":
                # AI phe Đỏ: Tìm giá trị lớn nhất (MAX)
                max_val = float("-inf")
                for m in ordered:
                    b.make_move(m[0], m[1], test_only=True)
                    val = search(b, d - 1, False)
                    b.undo_move(test_only=True)
                    max_val = max(max_val, val)
                return max_val
            else:
                # AI phe Đen: Tìm giá trị nhỏ nhất (MIN)
                min_val = float("inf")
                for m in ordered:
                    b.make_move(m[0], m[1], test_only=True)
                    val = search(b, d - 1, False)
                    b.undo_move(test_only=True)
                    min_val = min(min_val, val)
                return min_val
        else:
            # Lượt của đối thủ: Nút Cơ hội (Chance node)
            results = []
            for m in ordered:
                b.make_move(m[0], m[1], test_only=True)
                val = search(b, d - 1, True)
                b.undo_move(test_only=True)
                results.append(val)

            num_moves = len(results)
            if num_moves == 1:
                return results[0]

            # Nếu đối thủ là Đen (AI là Đỏ), đối thủ muốn điểm nhỏ nhất -> sắp xếp tăng dần
            # Nếu đối thủ là Đỏ (AI là Đen), đối thủ muốn điểm lớn nhất -> sắp xếp giảm dần
            if ai_color == "red":
                results.sort()
            else:
                results.sort(reverse=True)

            best_res = results[0]
            others_avg = sum(results[1:]) / (num_moves - 1)

            # Công thức Giá trị kỳ vọng: E[V] = 0.7 * Tốt_nhất + 0.3 * Trung_bình_còn_lại
            expected_val = 0.7 * best_res + 0.3 * others_avg

            # Ghi lại nút Cơ hội vào nhật ký trực quan
            if recorder and step_counter[0] < MAX_VISUALIZATION_STEPS:
                eval_list = [{"move": m, "value": v} for m, v in zip(ordered, results, strict=False)]
                recorder.add_step(
                    ExpectimaxStep(
                        step_num=step_counter[0] + 1,
                        algorithm="Expectimax",
                        explanation=f"Expectimax CHANCE node depth={d}: E[V]={expected_val:.0f} (70% best + 30% avg)",
                        current_node={"depth": d, "is_ai_turn": is_ai_turn},
                        is_chance_node=True,
                        child_values=[{"value": v} for v in results],
                        best_value=best_res,
                        expected_value=expected_val,
                        evaluated=eval_list,
                    )
                )
                step_counter[0] += 1

            return expected_val

    # Duyệt vòng lặp gốc (Root call) cho các nước đi đầu tiên của AI
    for m in sorted_moves[:12]:
        board.make_move(m[0], m[1], test_only=True)
        score = search(board, depth - 1, False)  # Lượt tiếp theo là đối thủ (nút Cơ hội)
        board.undo_move(test_only=True)

        if ai_color == "red":
            if score > best_score:
                best_score = score
                best_move = m
        else:  # Black
            if score < best_score:
                best_score = score
                best_move = m

    return best_move
