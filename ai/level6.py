# Level 6 AI: Minimax, Alpha-Beta Pruning, Expectimax
import time

from ai.eval import PIECE_VALUES, evaluate_board
from ai.step_recorder import (
    MAX_VISUALIZATION_STEPS,
    AlphaBetaStep,
    ExpectimaxStep,
    MinimaxStep,
    move_to_label,
    pos_to_label,
)


def safe_format(val):
    if val == float("inf"):
        return "∞"
    if val == float("-inf"):
        return "-∞"
    try:
        return f"{val:.0f}"
    except Exception:
        return str(val)


def sort_moves(board, moves):
    """Sorts moves to optimize Alpha-Beta pruning: captures first, then other moves"""

    def score_move(m):
        from_pos, to_pos = m
        targ = board.get_piece(to_pos)
        if targ:
            return 1000 + PIECE_VALUES.get(targ.name, 0)
        return 0

    return sorted(moves, key=score_move, reverse=True)


def minimax_move(board, depth=3, recorder=None):
    """
    Minimax search with depth-limiting.
    Assumes opponent plays optimally to minimize our payoff.

    Args:
        board: Current board state
        depth: Maximum search depth
        recorder: Optional StepRecorder for visualization
    """
    color = board.turn
    legal_moves = board.get_all_legal_moves(color)
    if not legal_moves:
        return None

    sorted_moves = sort_moves(board, legal_moves)
    best_move = sorted_moves[0]
    best_score = float("-inf") if color == "red" else float("inf")

    # We limit execution time to 1.5 seconds max
    start_time = time.time()
    step_counter = [0]

    def search(b, d, is_max, path):
        if d == 0 or time.time() - start_time > 1.2:
            return evaluate_board(b)

        moves = b.get_all_legal_moves(b.turn)
        if not moves:
            # Checkmate or stalemate
            return float("-inf") if is_max else float("inf")

        ordered = sort_moves(b, moves)[:12]  # Limit branching factor for speed
        siblings = []

        if is_max:
            max_val = float("-inf")
            for m in ordered:
                b.make_move(m[0], m[1], test_only=True)
                val = search(b, d - 1, False, path + [m])
                b.undo_move(test_only=True)
                max_val = max(max_val, val)
                siblings.append({"move": m, "value": val})

                # Record step (limit to MAX_VISUALIZATION_STEPS)
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
            min_val = float("inf")
            for m in ordered:
                b.make_move(m[0], m[1], test_only=True)
                val = search(b, d - 1, True, path + [m])
                b.undo_move(test_only=True)
                min_val = min(min_val, val)
                siblings.append({"move": m, "value": val})

                # Record step (limit to MAX_VISUALIZATION_STEPS)
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

    # Root call
    for m in sorted_moves[:15]:
        board.make_move(m[0], m[1], test_only=True)
        score = search(
            board, depth - 1, color == "black", [m]
        )  # Black is min (if color is red, next player is black/min)
        board.undo_move(test_only=True)

        if color == "red":
            if score > best_score:
                best_score = score
                best_move = m
        else:  # Black
            if score < best_score:
                best_score = score
                best_move = m

    return best_move


def alpha_beta_move(board, depth=4, recorder=None):
    """
    Minimax search with Alpha-Beta Pruning.
    Prunes branches that cannot influence the final decision, allowing deeper search.

    Args:
        board: Current board state
        depth: Maximum search depth
        recorder: Optional StepRecorder for visualization
    """
    color = board.turn
    legal_moves = board.get_all_legal_moves(color)
    if not legal_moves:
        return None

    sorted_moves = sort_moves(board, legal_moves)
    best_move = sorted_moves[0]
    best_score = float("-inf") if color == "red" else float("inf")

    start_time = time.time()
    step_counter = [0]  # For recording

    def search(b, d, alpha, beta, is_max, path):
        if d == 0 or time.time() - start_time > 1.2:
            return evaluate_board(b)

        moves = b.get_all_legal_moves(b.turn)
        if not moves:
            return float("-inf") if is_max else float("inf")

        ordered = sort_moves(b, moves)[:15]  # higher branch allowance due to pruning
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

                # Record step if recorder provided (limit to MAX_VISUALIZATION_STEPS)
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

                if beta <= alpha:
                    break  # Beta cutoff
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

                # Record step if recorder provided (limit to MAX_VISUALIZATION_STEPS)
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

                if beta <= alpha:
                    break  # Alpha cutoff
            return min_val

    # Root call
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
    Expectimax Search:
    Assumes opponent does not play fully optimally, but has:
    - 70% chance of making the best minimax move.
    - 30% chance of making a random move.
    We compute expected values at opponent's nodes (Chance nodes).

    Args:
        board: Current board state
        depth: Maximum search depth
        recorder: Optional StepRecorder for visualization
    """
    ai_color = board.turn
    legal_moves = board.get_all_legal_moves(ai_color)
    if not legal_moves:
        return None

    sorted_moves = sort_moves(board, legal_moves)
    best_move = sorted_moves[0]
    best_score = float("-inf") if ai_color == "red" else float("inf")

    start_time = time.time()
    step_counter = [0]

    def search(b, d, is_ai_turn):
        if d == 0 or time.time() - start_time > 1.2:
            return evaluate_board(b)

        moves = b.get_all_legal_moves(b.turn)
        if not moves:
            # The player whose turn it is has lost
            if b.turn == ai_color:
                return float("-inf") if ai_color == "red" else float("inf")
            else:
                return float("inf") if ai_color == "red" else float("-inf")

        ordered = sort_moves(b, moves)[:10]

        if is_ai_turn:
            # AI's turn: Optimize based on AI's color
            if ai_color == "red":
                # Red AI maximizes
                max_val = float("-inf")
                for m in ordered:
                    b.make_move(m[0], m[1], test_only=True)
                    val = search(b, d - 1, False)
                    b.undo_move(test_only=True)
                    max_val = max(max_val, val)
                return max_val
            else:
                # Black AI minimizes
                min_val = float("inf")
                for m in ordered:
                    b.make_move(m[0], m[1], test_only=True)
                    val = search(b, d - 1, False)
                    b.undo_move(test_only=True)
                    min_val = min(min_val, val)
                return min_val
        else:
            # Opponent's turn: Chance node
            results = []
            for m in ordered:
                b.make_move(m[0], m[1], test_only=True)
                val = search(b, d - 1, True)
                b.undo_move(test_only=True)
                results.append(val)

            num_moves = len(results)
            if num_moves == 1:
                return results[0]

            # If opponent is Black (AI is Red), opponent minimizes -> sort ascending
            # If opponent is Red (AI is Black), opponent maximizes -> sort descending
            if ai_color == "red":
                results.sort()
            else:
                results.sort(reverse=True)

            best_res = results[0]
            others_avg = sum(results[1:]) / (num_moves - 1)

            expected_val = 0.7 * best_res + 0.3 * others_avg

            # Record step (limit to MAX_VISUALIZATION_STEPS)
            if recorder and step_counter[0] < MAX_VISUALIZATION_STEPS:
                eval_list = [{"move": m, "value": v} for m, v in zip(ordered, results)]
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

    # Root call (AI's first moves)
    for m in sorted_moves[:12]:
        board.make_move(m[0], m[1], test_only=True)
        score = search(board, depth - 1, False)  # Next turn is opponent's (Chance)
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
