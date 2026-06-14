# Level 6 AI: Minimax, Alpha-Beta Pruning, Expectimax
import time
import random
from ai.eval import evaluate_board, PIECE_VALUES

def sort_moves(board, moves):
    """Sorts moves to optimize Alpha-Beta pruning: captures first, then other moves"""
    def score_move(m):
        from_pos, to_pos = m
        targ = board.get_piece(to_pos)
        if targ:
            return 1000 + PIECE_VALUES.get(targ.name, 0)
        return 0
    return sorted(moves, key=score_move, reverse=True)

def minimax_move(board, depth=3):
    """
    Minimax search with depth-limiting.
    Assumes opponent plays optimally to minimize our payoff.
    """
    color = board.turn
    legal_moves = board.get_all_legal_moves(color)
    if not legal_moves:
        return None
        
    sorted_moves = sort_moves(board, legal_moves)
    best_move = sorted_moves[0]
    best_score = float('-inf') if color == 'red' else float('inf')
    
    # We limit execution time to 1.5 seconds max
    start_time = time.time()
    
    def search(b, d, is_max):
        if d == 0 or time.time() - start_time > 1.2:
            return evaluate_board(b)
            
        moves = b.get_all_legal_moves(b.turn)
        if not moves:
            # Checkmate or stalemate
            return float('-inf') if is_max else float('inf')
            
        ordered = sort_moves(b, moves)[:12] # Limit branching factor for speed
        
        if is_max:
            max_val = float('-inf')
            for m in ordered:
                b.make_move(m[0], m[1])
                val = search(b, d - 1, False)
                b.undo_move()
                max_val = max(max_val, val)
            return max_val
        else:
            min_val = float('inf')
            for m in ordered:
                b.make_move(m[0], m[1])
                val = search(b, d - 1, True)
                b.undo_move()
                min_val = min(min_val, val)
            return min_val

    # Root call
    for m in sorted_moves[:15]:
        board.make_move(m[0], m[1])
        score = search(board, depth - 1, color == 'black') # Black is min (if color is red, next player is black/min)
        board.undo_move()
        
        if color == 'red':
            if score > best_score:
                best_score = score
                best_move = m
        else: # Black
            if score < best_score:
                best_score = score
                best_move = m
                
    return best_move

def alpha_beta_move(board, depth=4):
    """
    Minimax search with Alpha-Beta Pruning.
    Prunes branches that cannot influence the final decision, allowing deeper search.
    """
    color = board.turn
    legal_moves = board.get_all_legal_moves(color)
    if not legal_moves:
        return None
        
    sorted_moves = sort_moves(board, legal_moves)
    best_move = sorted_moves[0]
    best_score = float('-inf') if color == 'red' else float('inf')
    
    start_time = time.time()
    
    def search(b, d, alpha, beta, is_max):
        if d == 0 or time.time() - start_time > 1.2:
            return evaluate_board(b)
            
        moves = b.get_all_legal_moves(b.turn)
        if not moves:
            return float('-inf') if is_max else float('inf')
            
        ordered = sort_moves(b, moves)[:15] # higher branch allowance due to pruning
        
        if is_max:
            max_val = float('-inf')
            for m in ordered:
                b.make_move(m[0], m[1])
                val = search(b, d - 1, alpha, beta, False)
                b.undo_move()
                max_val = max(max_val, val)
                alpha = max(alpha, max_val)
                if beta <= alpha:
                    break # Beta cutoff
            return max_val
        else:
            min_val = float('inf')
            for m in ordered:
                b.make_move(m[0], m[1])
                val = search(b, d - 1, alpha, beta, True)
                b.undo_move()
                min_val = min(min_val, val)
                beta = min(beta, min_val)
                if beta <= alpha:
                    break # Alpha cutoff
            return min_val

    # Root call
    alpha = float('-inf')
    beta = float('inf')
    
    for m in sorted_moves[:20]:
        board.make_move(m[0], m[1])
        score = search(board, depth - 1, alpha, beta, color == 'black')
        board.undo_move()
        
        if color == 'red':
            if score > best_score:
                best_score = score
                best_move = m
            alpha = max(alpha, score)
        else: # Black
            if score < best_score:
                best_score = score
                best_move = m
            beta = min(beta, score)
            
    return best_move

def expectimax_move(board, depth=3):
    """
    Expectimax Search:
    Assumes opponent does not play fully optimally, but has:
    - 70% chance of making the best minimax move.
    - 30% chance of making a random move.
    We compute expected values at MIN nodes.
    """
    color = board.turn
    legal_moves = board.get_all_legal_moves(color)
    if not legal_moves:
        return None
        
    sorted_moves = sort_moves(board, legal_moves)
    best_move = sorted_moves[0]
    best_score = float('-inf') if color == 'red' else float('inf')
    
    start_time = time.time()
    
    def search(b, d, is_max):
        if d == 0 or time.time() - start_time > 1.2:
            return evaluate_board(b)
            
        moves = b.get_all_legal_moves(b.turn)
        if not moves:
            return float('-inf') if is_max else float('inf')
            
        ordered = sort_moves(b, moves)[:10]
        
        if is_max:
            max_val = float('-inf')
            for m in ordered:
                b.make_move(m[0], m[1])
                val = search(b, d - 1, False)
                b.undo_move()
                max_val = max(max_val, val)
            return max_val
        else:
            # Chance node (Expected value)
            # Evaluate all moves
            results = []
            for m in ordered:
                b.make_move(m[0], m[1])
                val = search(b, d - 1, True)
                b.undo_move()
                results.append(val)
                
            results.sort() # Min wants lowest cost values
            
            # 70% probability to choose the best move (lowest score for RED, highest for BLACK)
            # 30% probability distributed uniformly among remaining moves
            num_moves = len(results)
            if num_moves == 1:
                return results[0]
                
            best_res = results[0]
            others_avg = sum(results[1:]) / (num_moves - 1)
            
            expected_val = 0.7 * best_res + 0.3 * others_avg
            return expected_val

    # Root call
    for m in sorted_moves[:12]:
        board.make_move(m[0], m[1])
        score = search(board, depth - 1, color == 'black')
        board.undo_move()
        
        if color == 'red':
            if score > best_score:
                best_score = score
                best_move = m
        else: # Black
            if score < best_score:
                best_score = score
                best_move = m
                
    return best_move
