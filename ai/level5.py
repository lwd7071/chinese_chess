# Level 5 AI: Backtracking CSP (MRV), Min-Conflicts, AC-3
import random
from ai.eval import PIECE_VALUES
from ai.level3 import get_perspective_score

def get_threats_count(board, color):
    """Counts how many pieces of the given color are currently under direct threat from opponent"""
    opp = 'black' if color == 'red' else 'red'
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

def backtracking_mrv_move(board):
    """
    Backtracking with MRV (Minimum Remaining Values):
    We select the piece (Variable) that has the FEWEST legal destination moves (Domain).
    We move it to the square that yields the highest evaluation score.
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
        
    # MRV: Choose the variable (from_pos) with the smallest domain (fewest moves)
    chosen_var = min(var_domains.keys(), key=lambda x: len(var_domains[x]))
    
    # Find the best value (to_pos) for the chosen variable
    best_to = var_domains[chosen_var][0]
    best_score = float('-inf')
    
    for to_pos in var_domains[chosen_var]:
        board.make_move(chosen_var, to_pos)
        score = get_perspective_score(board, color)
        board.undo_move()
        if score > best_score:
            best_score = score
            best_to = to_pos
            
    return (chosen_var, best_to)

def min_conflicts_move(board):
    """
    Min-Conflicts:
    Conflicts = Number of our pieces under attack.
    We choose the move that minimizes the number of our pieces under threat.
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None
        
    color = board.turn
    random.shuffle(legal_moves)
    
    best_move = legal_moves[0]
    min_conflicts = float('inf')
    
    # We want to break ties with the evaluation function
    best_score = float('-inf')
    
    for from_pos, to_pos in legal_moves:
        board.make_move(from_pos, to_pos)
        conflicts = get_threats_count(board, color)
        score = get_perspective_score(board, color)
        board.undo_move()
        
        if conflicts < min_conflicts:
            min_conflicts = conflicts
            best_move = (from_pos, to_pos)
            best_score = score
        elif conflicts == min_conflicts:
            if score > best_score:
                best_score = score
                best_move = (from_pos, to_pos)
                
    return best_move

def ac3_move(board):
    """
    AC-3 (Arc Consistency):
    Prunes target cells that are unsafe (guarded by a piece of lower value).
    For example, a Rook moving to a cell guarded by a Pawn will be pruned.
    If some moves remain, we pick the best one using evaluation.
    If all moves are pruned, we select the best move from the original list (fallback).
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None
        
    color = board.turn
    opp = 'black' if color == 'red' else 'red'
    
    # Prune unsafe moves (AC-3 check)
    safe_moves = []
    
    for from_pos, to_pos in legal_moves:
        piece = board.get_piece(from_pos)
        p_val = PIECE_VALUES.get(piece.name, 0)
        
        # Test move
        board.make_move(from_pos, to_pos)
        
        # Check if the target position is under attack by a cheaper opponent piece
        is_unsafe = False
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
                            break
            if is_unsafe:
                break
                
        board.undo_move()
        if not is_unsafe:
            safe_moves.append((from_pos, to_pos))
            
    # Select from safe moves if available, otherwise fallback to all legal moves
    candidates = safe_moves if safe_moves else legal_moves
    
    random.shuffle(candidates)
    best_move = candidates[0]
    best_score = float('-inf')
    
    for from_pos, to_pos in candidates:
        board.make_move(from_pos, to_pos)
        score = get_perspective_score(board, color)
        board.undo_move()
        if score > best_score:
            best_score = score
            best_move = (from_pos, to_pos)
            
    return best_move
