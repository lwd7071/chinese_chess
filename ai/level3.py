# Level 3 AI: Hill Climbing, Simulated Annealing, Beam Search
import math
import random

from ai.eval import evaluate_board
from ai.step_recorder import MAX_VISUALIZATION_STEPS, BeamStep, HillClimbStep, SAStep


def get_perspective_score(board, color):
    # Returns board score from color's perspective
    scr = evaluate_board(board)
    return scr if color == "red" else -scr


def hill_climbing_move(board, recorder=None):
    """
    Hill Climbing: Evaluates all legal moves, selects the one with the highest evaluation score

    Args:
        board: Current board state
        recorder: Optional StepRecorder for visualization
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None

    random.shuffle(legal_moves)
    best_move = legal_moves[0]
    best_score = float("-inf")

    color = board.turn
    neighbors = []

    for i, (from_pos, to_pos) in enumerate(legal_moves):
        board.make_move(from_pos, to_pos, test_only=True)
        score = get_perspective_score(board, color)
        board.undo_move(test_only=True)

        neighbor_info = {"move": (from_pos, to_pos), "score": score}
        neighbors.append(neighbor_info)

        if score > best_score:
            best_score = score
            best_move = (from_pos, to_pos)

        # Record step if recorder provided (limit to MAX_VISUALIZATION_STEPS steps)
        if recorder and i < MAX_VISUALIZATION_STEPS:
            # Sort neighbors by score descending for visualization
            sorted_neighbors = sorted(neighbors, key=lambda x: x["score"], reverse=True)
            recorder.add_step(
                HillClimbStep(
                    step_num=i + 1,
                    algorithm="Hill Climbing",
                    explanation=f"Xét nước {from_pos}→{to_pos}: score={score}, tìm neighbor tốt nhất",
                    chosen_move=best_move,
                    current_score=best_score,
                    current_move={"move": best_move, "score": best_score},
                    neighbors=sorted_neighbors.copy(),
                    best_neighbor={"move": best_move, "score": best_score},
                    is_plateau=(score <= best_score and i > 0),
                )
            )

    return best_move


def simulated_annealing_move(board, T=100.0, alpha=0.9, recorder=None):
    """
    Simulated Annealing: Picks random moves, accepts worse moves with decreasing probability

    Args:
        board: Current board state
        T: Initial temperature
        alpha: Cooling rate (0 < alpha < 1)
        recorder: Optional StepRecorder for visualization
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None

    color = board.turn
    current_score = get_perspective_score(board, color)

    # We iterate a few times simulating cooling, and return the final state move
    # Since we must return a single move, we can pick a starting candidate and look at its neighbors
    random.shuffle(legal_moves)
    current_move = legal_moves[0]
    board.make_move(current_move[0], current_move[1], test_only=True)
    current_score = get_perspective_score(board, color)
    board.undo_move(test_only=True)

    best_move_ever = current_move
    best_score_ever = current_score

    temp = T
    step_counter = 0

    while temp > 1.0:
        candidate = random.choice(legal_moves)
        board.make_move(candidate[0], candidate[1], test_only=True)
        score = get_perspective_score(board, color)
        board.undo_move(test_only=True)

        delta = score - current_score
        accepted = False
        accept_prob = 0.0

        if delta > 0:
            # Better move, always accept
            current_move = candidate
            current_score = score
            accepted = True
            accept_prob = 1.0
        else:
            # Worse move, accept with Boltzmann probability
            accept_prob = math.exp(delta / temp)
            if random.random() < accept_prob:
                current_move = candidate
                current_score = score
                accepted = True

        # Track global best
        if score > best_score_ever:
            best_score_ever = score
            best_move_ever = candidate

        # Record step if recorder provided (limit to MAX_VISUALIZATION_STEPS steps)
        if recorder and step_counter < MAX_VISUALIZATION_STEPS:
            recorder.add_step(
                SAStep(
                    step_num=step_counter + 1,
                    algorithm="Simulated Annealing",
                    explanation=f"T={temp:.1f}, ΔE={delta:.0f}, P(accept)={accept_prob:.3f} → {'✅ Chấp nhận' if accepted else '❌ Từ chối'}",
                    chosen_move=best_move_ever,
                    current_move={"move": current_move, "score": current_score},
                    candidate_move={"move": candidate, "score": score},
                    temperature=temp,
                    delta_e=delta,
                    accept_prob=accept_prob,
                    accepted=accepted,
                )
            )
            step_counter += 1

        temp *= alpha

    return best_move_ever


def beam_search_move(board, k=3, recorder=None):
    """
    Local Beam Search: Keeps k best candidate moves, evaluates their responses, and picks the best

    Args:
        board: Current board state
        k: Number of beams to keep
        recorder: Optional StepRecorder for visualization
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None

    color = board.turn

    # Generate initial k best moves
    candidates = []
    for from_pos, to_pos in legal_moves:
        board.make_move(from_pos, to_pos, test_only=True)
        score = get_perspective_score(board, color)
        board.undo_move(test_only=True)
        candidates.append((score, (from_pos, to_pos)))

    candidates.sort(key=lambda x: x[0], reverse=True)
    beam = candidates[:k]
    eliminated = candidates[k:]

    # Record initial beam selection
    if recorder:
        recorder.add_step(
            BeamStep(
                step_num=1,
                algorithm="Beam Search",
                explanation=f"Chọn top {k} beams từ {len(candidates)} candidates, loại bỏ {len(eliminated)}",
                beam_k=k,
                all_candidates=[{"move": m, "score": s} for s, m in candidates],
                kept_beams=[{"move": m, "score": s} for s, m in beam],
                eliminated=[{"move": m, "score": s} for s, m in eliminated],
                worst_case_scores=[],
            )
        )

    # For each candidate in beam, check the opponent's best response (min score for us)
    # and find the candidate that has the best worst-case response (Minimax-like beam search)
    best_beam_move = beam[0][1]
    best_beam_score = float("-inf")
    worst_case_scores = []

    for _idx, (score, move) in enumerate(beam):
        board.make_move(move[0], move[1], test_only=True)

        # Opponent moves (minimize our score)
        opp_moves = board.get_all_legal_moves(board.turn)
        if not opp_moves:
            # Checkmate or stalemate
            opp_min_score = float("inf")  # very good for us
        else:
            opp_min_score = float("inf")
            for ofrom, oto in opp_moves:  # Limit branching factor for speed
                board.make_move(ofrom, oto, test_only=True)
                # Score from our perspective
                us_score = get_perspective_score(board, color)
                board.undo_move(test_only=True)
                if us_score < opp_min_score:
                    opp_min_score = us_score

        board.undo_move(test_only=True)

        worst_case_scores.append(
            {"move": move, "init_score": score, "worst_case": opp_min_score}
        )

        if opp_min_score > best_beam_score:
            best_beam_score = opp_min_score
            best_beam_move = move

    # Record final selection with worst-case analysis
    if recorder:
        recorder.add_step(
            BeamStep(
                step_num=2,
                algorithm="Beam Search",
                explanation=f"Đánh giá worst-case response, chọn beam có worst-case score cao nhất: {best_beam_score:.0f}",
                chosen_move=best_beam_move,
                beam_k=k,
                all_candidates=[{"move": m, "score": s} for s, m in candidates],
                kept_beams=[{"move": m, "score": s} for s, m in beam],
                eliminated=[{"move": m, "score": s} for s, m in eliminated],
                worst_case_scores=worst_case_scores,
            )
        )

    return best_beam_move
