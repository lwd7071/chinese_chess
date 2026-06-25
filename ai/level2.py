# Level 2 AI: Greedy, A*, IDA*
import random
from ai.eval import PIECE_VALUES
from ai.step_recorder import GreedyStep, AStarStep, IDAStarStep, MAX_VISUALIZATION_STEPS


def get_opponent_material(board, color):
    opp = 'black' if color == 'red' else 'red'
    total = 0
    for r in range(10):
        for c in range(9):
            p = board.matrix[r][c]
            if p and p.color == opp:
                total += PIECE_VALUES.get(p.name, 0)
    return total

def greedy_move(board, recorder=None):
    """
    Greedy: Picks the move that captures the highest value opponent piece, otherwise chooses randomly
    
    Args:
        board: Current board state
        recorder: Optional StepRecorder for visualization
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None
    
    # Mapping piece names to Vietnamese
    PIECE_NAME_VI = {
        'general': 'Tướng', 'advisor': 'Sĩ', 'elephant': 'Tượng',
        'horse': 'Mã', 'rook': 'Xe', 'cannon': 'Pháo', 'pawn': 'Tốt'
    }
    
    random.shuffle(legal_moves)
    best_move = legal_moves[0]
    max_val = -1
    
    # For visualization
    candidates = []
    
    for i, (from_pos, to_pos) in enumerate(legal_moves):
        target = board.get_piece(to_pos)
        val = PIECE_VALUES.get(target.name, 0) if target else 0
        piece_name = PIECE_NAME_VI.get(target.name, '—') if target else '—'
        
        # Build candidate info
        candidate_info = {
            'move': (from_pos, to_pos),
            'h': val,  # h(n) = value of captured piece
            'piece': piece_name
        }
        candidates.append(candidate_info)
        
        if val > max_val:
            max_val = val
            best_move = (from_pos, to_pos)
        
        # Record step if recorder provided (only first MAX_VISUALIZATION_STEPS to avoid clutter)
        if recorder and i < MAX_VISUALIZATION_STEPS:
            # Sort candidates by h descending (highest value first)
            sorted_candidates = sorted(candidates, key=lambda x: x['h'], reverse=True)
            recorder.add_step(GreedyStep(
                step_num=i + 1,
                algorithm="Greedy",
                explanation=f"Xét nước {from_pos}→{to_pos}: h={val} ({piece_name}), chọn h LỚN NHẤT",
                chosen_move=best_move,
                current_node=candidate_info,
                candidates=sorted_candidates.copy()
            ))
    
    return best_move

def a_star_move(board, recorder=None):
    """
    A* Search: f(n) = g(n) + h(n)
    g(n) = 1000 - captured_piece_value (cost to reach this state)
    h(n) = total remaining opponent material value (heuristic)
    
    Args:
        board: Current board state
        recorder: Optional StepRecorder for visualization
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None
    
    # Mapping piece names to Vietnamese
    PIECE_NAME_VI = {
        'general': 'Tướng', 'advisor': 'Sĩ', 'elephant': 'Tượng',
        'horse': 'Mã', 'rook': 'Xe', 'cannon': 'Pháo', 'pawn': 'Tốt'
    }
    
    random.shuffle(legal_moves)
    best_move = None
    min_f = float('inf')
    
    # For visualization
    frontier_list = []
    explored_list = []
    
    for i, (from_pos, to_pos) in enumerate(legal_moves):
        # Simulate move
        target = board.get_piece(to_pos)
        cap_val = PIECE_VALUES.get(target.name, 0) if target else 0
        piece_name = PIECE_NAME_VI.get(target.name, '—') if target else '—'
        
        # g(n) = cost to reach this node
        g = 1000 - cap_val
        
        # Make move to calculate remaining opponent material h(n)
        board.make_move(from_pos, to_pos, test_only=True)
        h = get_opponent_material(board, board.turn)  # opposite side material
        board.undo_move(test_only=True)
        
        # f(n) = g(n) + h(n)
        f = g + h
        
        # Build node info
        node_info = {
            'move': (from_pos, to_pos),
            'g': g,
            'h': h,
            'f': f,
            'piece_captured': piece_name,
            'cap_val': cap_val
        }
        
        # Add to frontier
        frontier_list.append(node_info)
        
        # Update best move
        if f < min_f:
            min_f = f
            best_move = (from_pos, to_pos)
        
        # Record step if recorder provided
        if recorder:
            # Sort frontier by f for visualization
            sorted_frontier = sorted(frontier_list, key=lambda x: x['f'])
            recorder.add_step(AStarStep(
                step_num=i + 1,
                algorithm="A*",
                explanation=f"Xét nước {from_pos}→{to_pos}: g={g} (1000-{cap_val}), h={h} (vật chất đối thủ), f={f}",
                chosen_move=best_move,
                current_node=node_info,
                frontier=sorted_frontier.copy(),
                explored=explored_list.copy()
            ))
        
        # Move to explored
        explored_list.append(node_info)
    
    return best_move

def ida_star_move(board, recorder=None):
    """
    IDA*: Iterative Deepening A* (depth-limited A* search).
    Runs A* with a threshold on f-cost, increasing the threshold on each iteration.
    
    Args:
        board: Current board state
        recorder: Optional StepRecorder for visualization
    """
    # For a turn-based board game, we can run a 2-ply IDA* search
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None
    
    random.shuffle(legal_moves)
    step_counter = [0]  # For recording
    
    def search(from_pos, to_pos, g, depth, threshold):
        # Simulate move
        board.make_move(from_pos, to_pos, test_only=True)
        
        # Heuristic h(n)
        h = get_opponent_material(board, board.turn)
        f = g + h
        
        # Record step if recorder provided (limit to MAX_VISUALIZATION_STEPS steps)
        if recorder and step_counter[0] < MAX_VISUALIZATION_STEPS:
            recorder.add_step(IDAStarStep(
                step_num=step_counter[0] + 1,
                algorithm="IDA*",
                explanation=f"IDA* node {from_pos}→{to_pos}: f={f}, threshold={threshold}, depth={depth}",
                current_node={'move': (from_pos, to_pos), 'g': g, 'h': h, 'f': f},
                threshold=threshold,
                iteration=0,  # Will be updated in outer loop
                exceeded_f=f if f > threshold else None,
                is_cutoff=(f > threshold)
            ))
            step_counter[0] += 1
        
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
        if recorder and step_counter[0] < MAX_VISUALIZATION_STEPS:
            recorder.add_step(IDAStarStep(
                step_num=step_counter[0] + 1,
                algorithm="IDA*",
                explanation=f"IDA* Iteration {iteration + 1}: threshold={threshold}",
                iteration=iteration + 1,
                threshold=threshold
            ))
            step_counter[0] += 1
        
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
