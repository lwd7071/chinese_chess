# Level 5 AI: Backtracking CSP (MRV), Min-Conflicts, AC-3
import random

from ai.eval import PIECE_VALUES
from ai.level3 import get_perspective_score
from ai.step_recorder import (
    AC3Step,
    BacktrackStep,
    MinConflictStep,
    move_to_label,
    pos_to_label,
)

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
    """Lấy tên quân cờ tiếng Việt từ vị trí trên bàn cờ."""
    if not pos:
        return "—"
    piece = board.get_piece(pos)
    return PIECE_NAME_VI.get(piece.name, "—") if piece else "—"


def get_threats_count(board, color):
    """Counts how many pieces of the given color are currently under direct threat from opponent"""
    opp = "black" if color == "red" else "red"
    threatened = set()

    # Generate all opponent raw attacks
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
    Backtracking with MRV (Minimum Remaining Values):
    We select the piece (Variable) that has the FEWEST legal destination moves (Domain).
    We move it to the square that yields the highest evaluation score.

    Args:
        board: Current board state
        recorder: Optional StepRecorder for visualization
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None

    color = board.turn

    # Variables: pieces that have at least 1 legal move
    # Map from_pos -> list of target positions
    var_domains = {}
    for from_pos, to_pos in legal_moves:
        if from_pos not in var_domains:
            var_domains[from_pos] = []
        var_domains[from_pos].append(to_pos)

    # Record all variables with domain sizes
    if recorder:
        variables_info = {pos_to_label(pos): len(domain) for pos, domain in var_domains.items()}
        recorder.add_step(
            BacktrackStep(
                step_num=1,
                algorithm="Backtracking MRV",
                explanation=f"Backtracking MRV: Tính domain size cho {len(var_domains)} biến (quân cờ có thể di chuyển)",
                variables=variables_info,
                chosen_variable="",
                domain=[],
                best_assignment={},
                evaluated=[],
            )
        )

    # MRV: Choose the variable (from_pos) with the smallest domain (fewest moves)
    chosen_var = min(var_domains.keys(), key=lambda x: len(var_domains[x]))
    domain_list = []

    # Find the best value (to_pos) for the chosen variable
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

    # Record MRV selection
    if recorder:
        recorder.add_step(
            BacktrackStep(
                step_num=2,
                algorithm="Backtracking MRV",
                explanation=f"Backtracking MRV chọn biến {pos_to_label(chosen_var)} (domain={len(var_domains[chosen_var])} - nhỏ nhất), nước đi {move_to_label((chosen_var, best_to))}",
                chosen_move=(chosen_var, best_to),
                variables={
                    pos_to_label(pos): len(domain) for pos, domain in var_domains.items()
                },
                chosen_variable=pos_to_label(chosen_var),
                domain=domain_list,
                best_assignment={"move": (chosen_var, best_to), "score": best_score, "piece": piece_name},
                evaluated=domain_list.copy(),
            )
        )

    return (chosen_var, best_to)


def min_conflicts_move(board, recorder=None):
    """
    Min-Conflicts:
    Conflicts = Number of our pieces under attack.
    We choose the move that minimizes the number of our pieces under threat.

    Args:
        board: Current board state
        recorder: Optional StepRecorder for visualization
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None

    color = board.turn
    random.shuffle(legal_moves)

    # Current conflicts before any move
    current_conflicts = get_threats_count(board, color)

    best_move = legal_moves[0]
    min_conflicts = float("inf")

    # We want to break ties with the evaluation function
    best_score = float("-inf")
    candidates = []

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

    # Record step
    if recorder:
        sorted_candidates = sorted(
            candidates, key=lambda x: (x["conflicts_after"], -x["score"])
        )[:10]
        best_piece_name = _get_piece_name(board, best_move[0])
        recorder.add_step(
            MinConflictStep(
                step_num=1,
                algorithm="Min-Conflicts",
                explanation=f"Min-Conflicts chọn {move_to_label(best_move)}: Conflicts trước={current_conflicts}, sau={min_conflicts} (giảm {current_conflicts - min_conflicts})",
                chosen_move=best_move,
                current_conflicts=current_conflicts,
                candidates=sorted_candidates,
                best_candidate={
                    "move": best_move,
                    "conflicts_after": min_conflicts,
                    "score": best_score,
                    "piece": best_piece_name,
                },
                evaluated=candidates.copy(),
            )
        )

    return best_move


def ac3_move(board, recorder=None):
    """
    AC-3 (Arc Consistency):
    Prunes target cells that are unsafe (guarded by a piece of lower value).
    For example, a Rook moving to a cell guarded by a Pawn will be pruned.
    If some moves remain, we pick the best one using evaluation.
    If all moves are pruned, we select the best move from the original list (fallback).

    Args:
        board: Current board state
        recorder: Optional StepRecorder for visualization
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None

    color = board.turn
    opp = "black" if color == "red" else "red"

    # Prune unsafe moves (AC-3 check)
    safe_moves = []
    pruned_moves = []

    for from_pos, to_pos in legal_moves:
        piece = board.get_piece(from_pos)
        p_val = PIECE_VALUES.get(piece.name, 0)

        # Test move
        board.make_move(from_pos, to_pos, test_only=True)

        # Check if the target position is under attack by a cheaper opponent piece
        is_unsafe = False
        attacker_name = None
        for r in range(10):
            for c in range(9):
                p = board.matrix[r][c]
                if p and p.color == opp:
                    if to_pos in p.get_raw_moves(board.matrix):
                        # Opponent piece can capture us
                        opp_val = PIECE_VALUES.get(p.name, 0)
                        if opp_val < p_val:
                            # It's an unsafe trade! (e.g. Rook captured by Cannon/Pawn)
                            is_unsafe = True
                            attacker_name = p.name
                            break
            if is_unsafe:
                break

        board.undo_move(test_only=True)

        if not is_unsafe:
            safe_moves.append((from_pos, to_pos))
        else:
            pruned_moves.append(
                {
                    "move": (from_pos, to_pos),
                    "reason": f"{PIECE_NAME_VI.get(piece.name, piece.name)}({p_val}) bị {PIECE_NAME_VI.get(attacker_name, attacker_name)}({PIECE_VALUES.get(attacker_name, 0)}) ăn",
                    "piece": PIECE_NAME_VI.get(piece.name, piece.name),
                }
            )

    # Select from safe moves if available, otherwise fallback to all legal moves
    candidates = safe_moves if safe_moves else legal_moves

    random.shuffle(candidates)
    best_move = candidates[0]
    best_score = float("-inf")
    safe_list_scores = []

    for from_pos, to_pos in candidates:
        board.make_move(from_pos, to_pos, test_only=True)
        score = get_perspective_score(board, color)
        board.undo_move(test_only=True)
        safe_list_scores.append({"move": (from_pos, to_pos), "score": score, "piece": _get_piece_name(board, from_pos)})
        if score > best_score:
            best_score = score
            best_move = (from_pos, to_pos)

    # Record step
    if recorder:
        recorder.add_step(
            AC3Step(
                step_num=1,
                algorithm="AC-3",
                explanation=f"AC-3: Lọc {len(pruned_moves)}/{len(legal_moves)} nước không an toàn, chọn {move_to_label(best_move)} từ {len(candidates)} nước an toàn",
                chosen_move=best_move,
                all_moves=len(legal_moves),
                safe_moves=safe_list_scores[:10],
                pruned_moves=pruned_moves[:10],
                chosen_from_safe={"move": best_move, "score": best_score, "piece": _get_piece_name(board, best_move[0])},
                evaluated=safe_list_scores.copy(),
            )
        )

    return best_move
