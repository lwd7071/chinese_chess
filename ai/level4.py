# Level 4 AI: Online Search, AND-OR Search, Belief State Search
import random
from ai.eval import evaluate_board, PIECE_VALUES
from ai.level3 import get_perspective_score

def online_search_move(board):
    """
    Online Search (Dynamic Strategy Adjustment):
    If our general is in check, we dynamically update our evaluation coefficients
    to prioritize defensive pieces (Sĩ, Tượng) and safety.
    If we are safe, we value attacking pieces (Xe, Pháo, Mã) and center control.
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None
        
    color = board.turn
    in_check = board.is_in_check(color)
    
    # Define dynamic weights
    weights = {
        'G': 10000, 'R': 900, 'C': 450, 'H': 300, 'E': 200, 'A': 200, 'P': 100
    }
    
    if in_check:
        # Increase values of defensive advisors and elephants to prioritize protection
        weights['A'] = 400
        weights['E'] = 350
    else:
        # Increase values of attacking pieces for aggressive push
        weights['R'] = 1100
        weights['C'] = 550
        weights['H'] = 400
        
    # Temporary patch of values
    import ai.eval as eval_mod
    original_values = eval_mod.PIECE_VALUES.copy()
    eval_mod.PIECE_VALUES.update(weights)
    
    # Run Hill Climbing on the updated evaluation function
    best_move = None
    best_score = float('-inf')
    random.shuffle(legal_moves)
    
    for from_pos, to_pos in legal_moves:
        board.make_move(from_pos, to_pos, test_only=True)
        score = get_perspective_score(board, color)
        board.undo_move(test_only=True)
        
        if score > best_score:
            best_score = score
            best_move = (from_pos, to_pos)
            
    # Restore original values
    eval_mod.PIECE_VALUES.update(original_values)
    return best_move

def and_or_search_move(board):
    """
    AND-OR search for deterministic, fully observable games (Xiangqi).
    
    Standard interpretation:
    - OR nodes: AI's turn (choose the best move that leads to a win).
    - AND nodes: Opponent's turn (AI must handle all possible opponent moves).
    
    This function uses a depth-limited AND-OR search to select a move.
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None
        
    color = board.turn
    random.shuffle(legal_moves)
    best_move = legal_moves[0]
    best_guaranteed_score = float('-inf')
    
    # We examine up to 10 moves for speed
    for from_pos, to_pos in legal_moves[:10]:
        board.make_move(from_pos, to_pos, test_only=True)
        
        opp_moves = board.get_all_legal_moves(board.turn)
        if not opp_moves:
            # Checkmate for opponent - win for us!
            worst_case_score = float('inf')
        else:
            worst_case_score = float('inf')
            # Opponent plays to minimize our score (AND nodes)
            for ofrom, oto in opp_moves:
                board.make_move(ofrom, oto, test_only=True)
                us_score = get_perspective_score(board, color)
                board.undo_move(test_only=True)
                if us_score < worst_case_score:
                    worst_case_score = us_score
                    
        board.undo_move(test_only=True)
        
        if worst_case_score > best_guaranteed_score:
            best_guaranteed_score = worst_case_score
            best_move = (from_pos, to_pos)
            
    return best_move

def belief_state_search_move(board):
    """
    Belief State Search:
    We maintain a belief probability distribution of the opponent's strategy:
    - 50% Aggressive (prioritizes captures)
    - 30% Defensive (prioritizes protecting pieces)
    - 20% Positional (prioritizes space control)
    We select the move that yields the highest expected value over this belief state.
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
        else: # positional (center control)
            # Pawn and Knight position
            center_score = 0
            for r in range(3, 7):
                for c in range(2, 7):
                    p = board.matrix[r][c]
                    if p and p.color == color:
                        center_score += 30
            return base + center_score

    best_move = legal_moves[0]
    best_expected_utility = float('-inf')
    
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
            
    return best_move
