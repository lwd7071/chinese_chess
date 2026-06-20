# Level 3 AI: Hill Climbing, Simulated Annealing, Beam Search
import random
import math
from ai.eval import evaluate_board

def get_perspective_score(board, color):
    # Returns board score from color's perspective
    scr = evaluate_board(board)
    return scr if color == 'red' else -scr

def hill_climbing_move(board):
    """Hill Climbing: Evaluates all legal moves, selects the one with the highest evaluation score"""
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None
        
    random.shuffle(legal_moves)
    best_move = legal_moves[0]
    best_score = float('-inf')
    
    color = board.turn
    for from_pos, to_pos in legal_moves:
        board.make_move(from_pos, to_pos, test_only=True)
        score = get_perspective_score(board, color)
        board.undo_move(test_only=True)
        
        if score > best_score:
            best_score = score
            best_move = (from_pos, to_pos)
            
    return best_move

def simulated_annealing_move(board, T=100.0, alpha=0.9):
    """Simulated Annealing: Picks random moves, accepts worse moves with decreasing probability"""
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None
        
    color = board.turn
    current_score = get_perspective_score(board, color)
    
    # We iterate a few times simulating cooling, and return the final state move
    # Since we must return a single move, we can pick a starting candidate and look at its neighbors
    random.shuffle(legal_moves)
    best_move = legal_moves[0]
    
    temp = T
    while temp > 1.0:
        candidate = random.choice(legal_moves)
        board.make_move(candidate[0], candidate[1], test_only=True)
        score = get_perspective_score(board, color)
        board.undo_move(test_only=True)
        
        delta = score - current_score
        if delta > 0:
            best_move = candidate
            current_score = score
        else:
            # Boltzmann probability
            prob = math.exp(delta / temp)
            if random.random() < prob:
                best_move = candidate
                current_score = score
                
        temp *= alpha
        
    return best_move

def beam_search_move(board, k=3):
    """Local Beam Search: Keeps k best candidate moves, evaluates their responses, and picks the best"""
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
    
    # For each candidate in beam, check the opponent's best response (min score for us)
    # and find the candidate that has the best worst-case response (Minimax-like beam search)
    best_beam_move = beam[0][1]
    best_beam_score = float('-inf')
    
    for score, move in beam:
        board.make_move(move[0], move[1], test_only=True)
        
        # Opponent moves (minimize our score)
        opp_moves = board.get_all_legal_moves(board.turn)
        if not opp_moves:
            # Checkmate or stalemate
            opp_min_score = float('inf') # very good for us
        else:
            opp_min_score = float('inf')
            for ofrom, oto in opp_moves: # Limit branching factor for speed
                board.make_move(ofrom, oto, test_only=True)
                # Score from our perspective
                us_score = get_perspective_score(board, color)
                board.undo_move(test_only=True)
                if us_score < opp_min_score:
                    opp_min_score = us_score
                    
        board.undo_move(test_only=True)
        
        if opp_min_score > best_beam_score:
            best_beam_score = opp_min_score
            best_beam_move = move
            
    return best_beam_move
