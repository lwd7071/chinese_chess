# Level 1 AI: BFS, DFS, UCS
import random
from ai.eval import PIECE_VALUES

def bfs_move(board):
    """BFS: Selects the first legal move in BFS expansion (first valid move at depth 1)"""
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None
    # BFS: FIFO queue. We explore level 1, so the first move popped is just the first legal move
    return legal_moves[0]

def dfs_move(board):
    """DFS: Selects the first legal move found in DFS expansion (depth first)"""
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None
    # DFS: LIFO stack. The first move popped is the last legal move
    return legal_moves[-1]

def ucs_move(board):
    """
    UCS: Cost = 1000 - captured_piece_value.
    Finds the move that minimizes the cost (prioritizes highest value capture).
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None
        
    best_move = None
    min_cost = float('inf')
    
    # Shuffle to avoid deterministic behavior when costs are equal
    random.shuffle(legal_moves)
    
    for from_pos, to_pos in legal_moves:
        target = board.get_piece(to_pos)
        
        # Calculate cost
        cap_val = PIECE_VALUES.get(target.name, 0) if target else 0
        cost = 1000 - cap_val
        
        if cost < min_cost:
            min_cost = cost
            best_move = (from_pos, to_pos)
            
    return best_move
