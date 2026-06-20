# Level 2 AI: Greedy, A*, IDA*
import random
from ai.eval import PIECE_VALUES

def get_opponent_material(board, color):
    opp = 'black' if color == 'red' else 'red'
    total = 0
    for r in range(10):
        for c in range(9):
            p = board.matrix[r][c]
            if p and p.color == opp:
                total += PIECE_VALUES.get(p.name, 0)
    return total

def greedy_move(board):
    """Greedy: Picks the move that captures the highest value opponent piece, otherwise chooses randomly"""
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None
        
    random.shuffle(legal_moves)
    best_move = legal_moves[0]
    max_val = -1
    
    for from_pos, to_pos in legal_moves:
        target = board.get_piece(to_pos)
        if target:
            val = PIECE_VALUES.get(target.name, 0)
            if val > max_val:
                max_val = val
                best_move = (from_pos, to_pos)
                
    return best_move

def a_star_move(board):
    """
    A* Search: f(n) = g(n) + h(n)
    g(n) = 1000 - captured_piece_value
    h(n) = total remaining opponent material value
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None
        
    random.shuffle(legal_moves)
    best_move = None
    min_f = float('inf')
    
    for from_pos, to_pos in legal_moves:
        # Simulate move
        target = board.get_piece(to_pos)
        cap_val = PIECE_VALUES.get(target.name, 0) if target else 0
        
        g = 1000 - cap_val
        
        # Make move to calculate remaining opponent material h(n)
        board.make_move(from_pos, to_pos, test_only=True)
        h = get_opponent_material(board, board.turn) # opposite side material
        board.undo_move(test_only=True)
        
        f = g + h
        if f < min_f:
            min_f = f
            best_move = (from_pos, to_pos)
            
    return best_move

def ida_star_move(board):
    """
    IDA*: Iterative Deepening A* (depth-limited A* search).
    Runs A* with a threshold on f-cost, increasing the threshold on each iteration.
    """
    # For a turn-based board game, we can run a 2-ply IDA* search
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None
        
    random.shuffle(legal_moves)
    
    def search(from_pos, to_pos, g, depth, threshold):
        # Simulate move
        board.make_move(from_pos, to_pos, test_only=True)
        
        # Heuristic h(n)
        h = get_opponent_material(board, board.turn)
        f = g + h
        
        if f > threshold:
            board.undo_move(test_only=True)
            return f, None
            
        if depth == 0 or not board.get_all_legal_moves(board.turn):
            board.undo_move(test_only=True)
            return f, (from_pos, to_pos)
            
        # Recursive step: next ply (opponent's turn)
        # Opponent wants to maximize their result, which means minimizing f from our perspective.
        opp_moves = board.get_all_legal_moves(board.turn)
        min_t = float('inf')
        best_suc_move = None
        
        # Sort opponent moves greedily to speed up
        for ofrom, oto in opp_moves:
            otarg = board.get_piece(oto)
            ocap_val = PIECE_VALUES.get(otarg.name, 0) if otarg else 0
            
            # g cost from our perspective increases if opponent captures our pieces
            next_g = g + ocap_val
            
            t, sol = search(ofrom, oto, next_g, depth - 1, threshold)
            if sol is not None:
                board.undo_move(test_only=True)
                return t, (from_pos, to_pos)
            if t < min_t:
                min_t = t
                
        board.undo_move(test_only=True)
        return min_t, None

    # Iterative deepening loop
    threshold = get_opponent_material(board, board.turn) # initial remaining material
    best_move = legal_moves[0]
    
    for iteration in range(3): # Max 3 iterations to prevent slow down
        min_exceeded = float('inf')
        for from_pos, to_pos in legal_moves:
            target = board.get_piece(to_pos)
            cap_val = PIECE_VALUES.get(target.name, 0) if target else 0
            g = 1000 - cap_val
            
            t, sol = search(from_pos, to_pos, g, 1, threshold) # depth 1
            if sol is not None:
                return (from_pos, to_pos)
            if t < min_exceeded:
                min_exceeded = t
        if min_exceeded == float('inf'):
            break
        threshold = min_exceeded
        
    return greedy_move(board) # Fallback to greedy if limit exceeded
