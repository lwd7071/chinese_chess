# Level 3 AI: Hill Climbing, Simulated Annealing, Beam Search
# Gói chứa các thuật toán tìm kiếm cục bộ (local search): Leo đồi (Hill Climbing), Luyện kim mô phỏng (Simulated Annealing), và Tìm kiếm chùm (Beam Search).
import math
import random

from ai.eval import evaluate_board
from ai.step_recorder import MAX_VISUALIZATION_STEPS, BeamStep, HillClimbStep, SAStep

# Bảng dịch tên các quân cờ sang tiếng Việt phục vụ hiển thị trực quan trên giao diện
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
    Hàm phụ trợ lấy tên quân cờ tiếng Việt từ vị trí cụ thể trên bàn cờ.

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


def get_perspective_score(board, color):
    """
    Hàm trả về điểm số đánh giá bàn cờ theo góc nhìn của một phe cụ thể (color).
    Nếu là phe Đỏ, giữ nguyên điểm từ evaluate_board (vốn tính theo Đỏ).
    Nếu là phe Đen, đảo dấu điểm số.

    Args:
        board: Trạng thái bàn cờ
        color: Màu quân của phe cần tính điểm ('red' hoặc 'black')
    """
    scr = evaluate_board(board)
    return scr if color == "red" else -scr


def hill_climbing_move(board, recorder=None):
    """
    Thuật toán Leo đồi (Hill Climbing Search).
    Thuật toán duyệt qua tất cả các nước đi hợp lệ hiện tại (các nút láng giềng - neighbors),
    tính toán điểm số đánh giá của từng trạng thái láng giềng và chọn láng giềng có điểm số cao nhất.

    Args:
        board: Trạng thái bàn cờ hiện tại
        recorder: Đối tượng ghi lại các bước tìm kiếm phục vụ trực quan hóa (nếu có)
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None

    random.shuffle(legal_moves)
    best_move = legal_moves[0]
    best_score = float("-inf")

    color = board.turn

    # Khởi tạo danh sách toàn bộ các trạng thái láng giềng (neighbor nodes)
    all_neighbors = []
    for m in legal_moves:
        piece_name = _get_piece_name(board, m[0])
        # Mô phỏng nước đi để tính điểm số láng giềng
        board.make_move(m[0], m[1], test_only=True)
        score = get_perspective_score(board, color)
        board.undo_move(test_only=True)

        all_neighbors.append({
            "move": m,
            "score": score,
            "piece": piece_name,
        })

    evaluated_so_far = []

    # Duyệt qua từng láng giềng để tìm trạng thái có điểm số cao nhất
    for i, neighbor_info in enumerate(all_neighbors):
        score = neighbor_info["score"]
        m = neighbor_info["move"]

        evaluated_so_far.append(neighbor_info)
        remaining_neighbors = all_neighbors[i + 1:]

        # Cập nhật nếu tìm thấy láng giềng tốt hơn
        if score > best_score:
            best_score = score
            best_move = m

        # Ghi lại bước đi nếu có recorder
        if recorder and i < MAX_VISUALIZATION_STEPS:
            best_piece_name = _get_piece_name(board, best_move[0])
            recorder.add_step(
                HillClimbStep(
                    step_num=i + 1,
                    algorithm="Hill Climbing",
                    explanation=f"Xét nước {m[0]}→{m[1]}: score={score:.0f}, tìm neighbor tốt nhất",
                    chosen_move=best_move,
                    current_score=best_score,
                    current_move={"move": best_move, "score": best_score, "piece": best_piece_name},
                    neighbors=remaining_neighbors.copy(),
                    best_neighbor={"move": best_move, "score": best_score, "piece": best_piece_name},
                    is_plateau=(score <= best_score and i > 0), # Trạng thái cao nguyên (plateau) khi điểm bằng nhau
                    evaluated=evaluated_so_far.copy(),
                )
            )

    return best_move


def simulated_annealing_move(board, T=100.0, alpha=0.9, recorder=None):
    """
    Thuật toán Luyện kim mô phỏng (Simulated Annealing).
    Lấy cảm hứng từ quá trình luyện kim, thuật toán cho phép chấp nhận các nước đi có điểm số kém hơn
    với một xác suất giảm dần theo nhiệt độ T (dựa trên phân phối Boltzmann).
    Giúp thuật toán có khả năng thoát khỏi các đỉnh địa phương (local maxima) ở đầu quá trình tìm kiếm.

    Args:
        board: Trạng thái bàn cờ hiện tại
        T: Nhiệt độ khởi đầu (Initial temperature)
        alpha: Tốc độ hạ nhiệt (Cooling rate, 0 < alpha < 1)
        recorder: Đối tượng ghi lại các bước tìm kiếm phục vụ trực quan hóa (nếu có)
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None

    color = board.turn
    current_score = get_perspective_score(board, color)

    # Khởi tạo nút xuất phát bằng cách chọn ngẫu nhiên một nước đi đầu tiên
    random.shuffle(legal_moves)
    current_move = legal_moves[0]
    board.make_move(current_move[0], current_move[1], test_only=True)
    current_score = get_perspective_score(board, color)
    board.undo_move(test_only=True)

    # Các biến lưu trữ trạng thái tốt nhất từng tìm thấy trong suốt quá trình
    best_move_ever = current_move
    best_score_ever = current_score

    temp = T
    step_counter = 0

    # Vòng lặp mô phỏng quá trình hạ nhiệt cho đến khi nhiệt độ đủ thấp
    while temp > 1.0:
        # Chọn ngẫu nhiên một nước đi ứng viên
        candidate = random.choice(legal_moves)
        board.make_move(candidate[0], candidate[1], test_only=True)
        score = get_perspective_score(board, color)
        board.undo_move(test_only=True)

        delta = score - current_score
        accepted = False
        accept_prob = 0.0

        if delta > 0:
            # Nước đi tốt hơn: luôn luôn chấp nhận (xác suất = 1.0)
            current_move = candidate
            current_score = score
            accepted = True
            accept_prob = 1.0
        else:
            # Nước đi tệ hơn: tính xác suất chấp nhận dựa trên công thức Boltzmann P = exp(ΔE / T)
            accept_prob = math.exp(delta / temp)
            if random.random() < accept_prob:
                current_move = candidate
                current_score = score
                accepted = True

        # Theo dõi và cập nhật nước đi tối ưu toàn cục
        if score > best_score_ever:
            best_score_ever = score
            best_move_ever = candidate

        # Ghi lại nhật ký bước đi nếu có recorder
        if recorder and step_counter < MAX_VISUALIZATION_STEPS:
            curr_piece = _get_piece_name(board, current_move[0]) if current_move else "—"
            cand_piece = _get_piece_name(board, candidate[0]) if candidate else "—"
            recorder.add_step(
                SAStep(
                    step_num=step_counter + 1,
                    algorithm="Simulated Annealing",
                    explanation=f"T={temp:.1f}, ΔE={delta:.0f}, P(accept)={accept_prob:.3f} → {'✅ Chấp nhận' if accepted else '❌ Từ chối'}",
                    chosen_move=best_move_ever,
                    current_move={"move": current_move, "score": current_score, "piece": curr_piece},
                    candidate_move={"move": candidate, "score": score, "piece": cand_piece},
                    temperature=temp,
                    delta_e=delta,
                    accept_prob=accept_prob,
                    accepted=accepted,
                )
            )
            step_counter += 1

        # Giảm nhiệt độ theo hệ số alpha
        temp *= alpha

    return best_move_ever


def beam_search_move(board, k=3, recorder=None):
    """
    Thuật toán tìm kiếm chùm cục bộ (Local Beam Search).
    Tại mỗi bước, thuật toán chỉ duy trì danh sách k trạng thái (beams) hứa hẹn nhất.
    Sau đó, mô phỏng phản đòn của đối thủ cho từng beam và chọn ra beam mang lại kết quả xấu nhất (worst-case) cao nhất.
    (Cách tiếp cận Beam Search kết hợp đánh giá rủi ro theo hướng Minimax).

    Args:
        board: Trạng thái bàn cờ hiện tại
        k: Số lượng luồng (beams) tối đa được giữ lại
        recorder: Đối tượng ghi lại các bước tìm kiếm phục vụ trực quan hóa (nếu có)
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None

    color = board.turn

    # Lập danh sách điểm số cho toàn bộ các nước đi hợp lệ ban đầu
    candidates = []
    for from_pos, to_pos in legal_moves:
        board.make_move(from_pos, to_pos, test_only=True)
        score = get_perspective_score(board, color)
        board.undo_move(test_only=True)
        candidates.append((score, (from_pos, to_pos)))

    # Sắp xếp các ứng viên giảm dần theo điểm và chọn ra k luồng (beams) tốt nhất
    candidates.sort(key=lambda x: x[0], reverse=True)
    beam = candidates[:k]
    eliminated = candidates[k:]

    # Ghi lại bước chọn lọc danh sách beams ban đầu
    if recorder:
        recorder.add_step(
            BeamStep(
                step_num=1,
                algorithm="Beam Search",
                explanation=f"Chọn top {k} beams từ {len(candidates)} candidates, loại bỏ {len(eliminated)}",
                beam_k=k,
                all_candidates=[{"move": m, "score": s, "piece": _get_piece_name(board, m[0])} for s, m in candidates],
                kept_beams=[{"move": m, "score": s, "piece": _get_piece_name(board, m[0])} for s, m in beam],
                eliminated=[{"move": m, "score": s, "piece": _get_piece_name(board, m[0])} for s, m in eliminated],
                worst_case_scores=[],
            )
        )

    # Đối với mỗi candidate trong danh sách beam, kiểm tra phản ứng tốt nhất của đối thủ
    # (tức là nước đi khiến điểm số của ta giảm thấp nhất - Minimax)
    best_beam_move = beam[0][1]
    best_beam_score = float("-inf")
    worst_case_scores = []

    for _idx, (score, move) in enumerate(beam):
        board.make_move(move[0], move[1], test_only=True)

        # Lấy các nước đi phản đòn của đối thủ
        opp_moves = board.get_all_legal_moves(board.turn)
        if not opp_moves:
            # Nếu đối thủ bị chiếu hết hoặc không có nước đi
            opp_min_score = float("inf")  # Tình huống cực kỳ tốt cho ta
        else:
            opp_min_score = float("inf")
            for ofrom, oto in opp_moves:
                board.make_move(ofrom, oto, test_only=True)
                # Tính điểm từ góc nhìn của ta
                us_score = get_perspective_score(board, color)
                board.undo_move(test_only=True)
                if us_score < opp_min_score:
                    opp_min_score = us_score

        board.undo_move(test_only=True)

        # Lưu lại phân tích rủi ro xấu nhất (worst case) cho chùm hiện tại
        worst_case_scores.append(
            {"move": move, "init_score": score, "worst_case": opp_min_score, "piece": _get_piece_name(board, move[0])}
        )

        # Chọn beam có điểm số rủi ro xấu nhất là cao nhất (tối ưu hóa rủi ro)
        if opp_min_score > best_beam_score:
            best_beam_score = opp_min_score
            best_beam_move = move

    # Ghi lại bước chọn lọc cuối cùng kèm phân tích worst-case
    if recorder:
        recorder.add_step(
            BeamStep(
                step_num=2,
                algorithm="Beam Search",
                explanation=f"Đánh giá worst-case response, chọn beam có worst-case score cao nhất: {best_beam_score:.0f}",
                chosen_move=best_beam_move,
                beam_k=k,
                all_candidates=[{"move": m, "score": s, "piece": _get_piece_name(board, m[0])} for s, m in candidates],
                kept_beams=[{"move": m, "score": s, "piece": _get_piece_name(board, m[0])} for s, m in beam],
                eliminated=[{"move": m, "score": s, "piece": _get_piece_name(board, m[0])} for s, m in eliminated],
                worst_case_scores=worst_case_scores,
            )
        )

    return best_beam_move

