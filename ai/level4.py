# Level 4 AI: Online Search, AND-OR Search, Belief State Search
import random

from ai.level3 import get_perspective_score
from ai.step_recorder import AndOrStep, BeliefStep, OnlineStep


def online_search_move(board, recorder=None):
    """
    Online Search (Dynamic Strategy Adjustment):
    If our general is in check, we dynamically update our evaluation coefficients
    to prioritize defensive pieces (Sĩ, Tượng) and safety.
    If we are safe, we value attacking pieces (Xe, Pháo, Mã) and center control.

    Args:
        board: Current board state
        recorder: Optional StepRecorder for visualization
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None

    color = board.turn
    in_check = board.is_in_check(color)

    # Define dynamic weights
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
        # Increase values of defensive advisors and elephants to prioritize protection
        weights_after = weights_before.copy()
        weights_after["advisor"] = 400
        weights_after["elephant"] = 350
    else:
        # Increase values of attacking pieces for aggressive push
        weights_after = weights_before.copy()
        weights_after["rook"] = 1100
        weights_after["cannon"] = 550
        weights_after["horse"] = 400

    # Record initial state if recorder provided
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

    # Temporary patch of values
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

    # Run Hill Climbing on the updated evaluation function
    best_move = None
    best_score = float("-inf")
    random.shuffle(legal_moves)
    candidates = []

    for _i, (from_pos, to_pos) in enumerate(legal_moves):
        board.make_move(from_pos, to_pos, test_only=True)
        score = get_perspective_score(board, color)
        board.undo_move(test_only=True)

        candidates.append({"move": (from_pos, to_pos), "score": score})

        if score > best_score:
            best_score = score
            best_move = (from_pos, to_pos)

    # Record final selection
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

    # Restore original values
    eval_mod.PIECE_VALUES.update(original_values)
    return best_move


def and_or_search_move(board, recorder=None):
    """
    AND-OR search for deterministic, fully observable games (Xiangqi).

    Standard interpretation:
    - OR nodes: AI's turn (choose the best move that leads to a win).
    - AND nodes: Opponent's turn (AI must handle all possible opponent moves).

    This function uses a depth-limited AND-OR search to select a move.

    Args:
        board: Current board state
        recorder: Optional StepRecorder for visualization
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None

    color = board.turn
    random.shuffle(legal_moves)
    best_move = legal_moves[0]
    best_guaranteed_score = float("-inf")

    # We examine up to 10 moves for speed
    for i, (from_pos, to_pos) in enumerate(legal_moves[:10]):
        board.make_move(from_pos, to_pos, test_only=True)

        opp_moves = board.get_all_legal_moves(board.turn)
        and_responses = []

        if not opp_moves:
            # Checkmate for opponent - win for us!
            worst_case_score = float("inf")
        else:
            worst_case_score = float("inf")
            worst_case_move = None
            # Opponent plays to minimize our score (AND nodes)
            for ofrom, oto in opp_moves:
                board.make_move(ofrom, oto, test_only=True)
                us_score = get_perspective_score(board, color)
                board.undo_move(test_only=True)

                and_responses.append({"move": (ofrom, oto), "score": us_score})

                if us_score < worst_case_score:
                    worst_case_score = us_score
                    worst_case_move = (ofrom, oto)

        board.undo_move(test_only=True)

        # Record step if recorder provided (limit to 10)
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
                    },
                    and_responses=and_responses[:5],  # Limit to 5 for display
                    worst_case={"move": worst_case_move, "score": worst_case_score}
                    if worst_case_move
                    else {},
                    guaranteed_score=worst_case_score,
                )
            )

        if worst_case_score > best_guaranteed_score:
            best_guaranteed_score = worst_case_score
            best_move = (from_pos, to_pos)

    return best_move


def belief_state_search_move(board, recorder=None):
    """
    Belief State Search:
    We maintain a belief probability distribution of the opponent's strategy:
    - 50% Aggressive (prioritizes captures)
    - 30% Defensive (prioritizes protecting pieces)
    - 20% Positional (prioritizes space control)
    We select the move that yields the highest expected value over this belief state.

    Args:
        board: Current board state
        recorder: Optional StepRecorder for visualization
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None

    color = board.turn
    random.shuffle(legal_moves)

    # Detect opponent's last move type to update belief distribution dynamically
    # For example, if opponent just captured a piece, they are likely aggressive.
    # We check board history
    opp_style = "aggressive"
    if board.history:
        _, to_pos, captured, _ = board.history[-1]
        if captured:
            opp_style = "aggressive"
        else:
            opp_style = "defensive" if to_pos[0] in [0, 1, 2, 7, 8, 9] else "positional"

    # Belief probabilities
    if opp_style == "aggressive":
        p_agg, p_def, p_pos = 0.6, 0.2, 0.2
    elif opp_style == "defensive":
        p_agg, p_def, p_pos = 0.2, 0.6, 0.2
    else:
        p_agg, p_def, p_pos = 0.2, 0.2, 0.6

    # Record detected style
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

    # Helper to calculate positional value of a board from perspective of a strategy
    def get_strategy_score(board, style):
        base = get_perspective_score(board, color)
        if style == "aggressive":
            # Material value is dominant
            return base * 1.5
        elif style == "defensive":
            # Guard safety is dominant
            g_pos = board.get_general_pos(color)
            if g_pos:
                # Add score for having many defenders close to general
                defenders = 0
                gr, gc = g_pos
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        p = board.get_piece((gr + dr, gc + dc))
                        if p and p.color == color:
                            defenders += 1
                return base + defenders * 50
            return base
        else:  # positional (center control)
            # Pawn and Knight position
            center_score = 0
            for r in range(3, 7):
                for c in range(2, 7):
                    p = board.matrix[r][c]
                    if p and p.color == color:
                        center_score += 30
            return base + center_score

    best_move = legal_moves[0]
    best_expected_utility = float("-inf")

    for from_pos, to_pos in legal_moves[:12]:
        board.make_move(from_pos, to_pos, test_only=True)

        # Expected utility over the belief distribution
        u_agg = get_strategy_score(board, "aggressive")
        u_def = get_strategy_score(board, "defensive")
        u_pos = get_strategy_score(board, "positional")

        expected_utility = p_agg * u_agg + p_def * u_def + p_pos * u_pos
        board.undo_move(test_only=True)

        if expected_utility > best_expected_utility:
            best_expected_utility = expected_utility
            best_move = (from_pos, to_pos)

    # Record final selection
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
