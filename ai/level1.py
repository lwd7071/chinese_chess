# Level 1 AI: BFS, DFS, UCS
import random
from collections import deque
from ai.eval import evaluate_board, PIECE_VALUES
from ai.step_recorder import BFSStep, DFSStep, UCSStep, MAX_VISUALIZATION_STEPS


class BFSNode:
    def __init__(self, node_id, parent_id, root_move, move, board, depth):
        self.id = node_id
        self.parent_id = parent_id
        self.root_move = root_move
        self.move = move
        self.board = board
        self.depth = depth
        self.children = []
        self.score = None

def bfs_move(board, depth=2, recorder=None):
    """
    BFS: Depth-limited breadth-first search propagating evaluations using minimax logic.
    
    Args:
        board: Current board state
        depth: Maximum search depth
        recorder: Optional StepRecorder for visualization
    """
    ai_color = board.turn
    legal_moves = board.get_all_legal_moves(ai_color)
    if not legal_moves:
        return None

    # 1. Create synthetic root node
    root_node = BFSNode(node_id=0, parent_id=None, root_move=None, move=None, board=board, depth=0)
    nodes = {0: root_node}
    node_id_counter = 0

    # 2. Enqueue depth-1 nodes
    queue = deque()
    explored_nodes = []
    
    for move in legal_moves:
        node_id_counter += 1
        next_board = board.copy()
        next_board.make_move(move[0], move[1], test_only=True)
        node = BFSNode(
            node_id=node_id_counter,
            parent_id=0,
            root_move=move,
            move=move,
            board=next_board,
            depth=1
        )
        root_node.children.append(node.id)
        nodes[node.id] = node
        queue.append(node)

    # 3. Perform level-order expansion
    step_counter = 0
    while queue:
        curr = queue.popleft()
        
        # Record step if recorder provided
        if recorder and step_counter < MAX_VISUALIZATION_STEPS:  # Limit steps to avoid too many
            queue_info = [{'id': f'n{n.id}', 'move': n.move, 'depth': n.depth} for n in list(queue)[:10]]
            recorder.add_step(BFSStep(
                step_num=step_counter + 1,
                algorithm="BFS",
                explanation=f"Duyệt node n{curr.id} ở depth={curr.depth}, mở rộng các nước đi tiếp theo",
                current_node={'id': f'n{curr.id}', 'move': curr.move, 'depth': curr.depth, 'score': curr.score},
                queue=queue_info,
                explored=explored_nodes.copy()
            ))
            step_counter += 1
        
        explored_nodes.append({'id': f'n{curr.id}', 'move': curr.move, 'depth': curr.depth})
        
        if curr.depth >= depth:
            continue
        
        moves = curr.board.get_all_legal_moves(curr.board.turn)
        for move in moves:
            node_id_counter += 1
            next_board = curr.board.copy()
            next_board.make_move(move[0], move[1], test_only=True)
            child = BFSNode(
                node_id=node_id_counter,
                parent_id=curr.id,
                root_move=curr.root_move,
                move=move,
                board=next_board,
                depth=curr.depth + 1
            )
            curr.children.append(child.id)
            nodes[child.id] = child
            queue.append(child)

    # 4. Treat nodes without children as leaves and evaluate them
    for node in nodes.values():
        if node.id == 0:
            continue
        if len(node.children) == 0:
            node.score = evaluate_board(node.board)

    # 5. Propagate scores bottom-up
    sorted_node_ids = sorted(nodes.keys(), key=lambda nid: nodes[nid].depth, reverse=True)
    for nid in sorted_node_ids:
        node = nodes[nid]
        if len(node.children) > 0:
            child_scores = [nodes[cid].score for cid in node.children]
            if node.board.turn == 'red':
                node.score = max(child_scores)
            else:
                node.score = min(child_scores)

    # 6. Select among root moves
    best_move = None
    if ai_color == 'red':
        best_score = float('-inf')
        for cid in root_node.children:
            cnode = nodes[cid]
            if cnode.score > best_score:
                best_score = cnode.score
                best_move = cnode.root_move
    else:
        best_score = float('inf')
        for cid in root_node.children:
            cnode = nodes[cid]
            if cnode.score < best_score:
                best_score = cnode.score
                best_move = cnode.root_move

    return best_move

def dfs_move(board, depth=2, recorder=None):
    """
    DFS: Depth-limited depth-first search propagating evaluations using minimax logic.
    
    Args:
        board: Current board state
        depth: Maximum search depth
        recorder: Optional StepRecorder for visualization
    """
    ai_color = board.turn
    legal_moves = board.get_all_legal_moves(ai_color)
    if not legal_moves:
        return None
    
    step_counter = [0]  # Use list to allow mutation in nested function
    stack_trace = []
    explored_nodes = []
    
    def dfs_search_with_recording(board, remaining_depth, current_stack):
        if remaining_depth == 0:
            return evaluate_board(board)
            
        moves = board.get_all_legal_moves(board.turn)
        if not moves:
            return evaluate_board(board)
        
        # Record step if recorder provided (limit to avoid explosion)
        if recorder and step_counter[0] < MAX_VISUALIZATION_STEPS:
            recorder.add_step(DFSStep(
                step_num=step_counter[0] + 1,
                algorithm="DFS",
                explanation=f"DFS ở depth={depth - remaining_depth}, duyệt {len(moves)} nước đi",
                current_node={'depth': depth - remaining_depth, 'score': None},
                stack=current_stack.copy(),
                explored=explored_nodes.copy(),
                is_backtracking=False
            ))
            step_counter[0] += 1
        
        if board.turn == 'red':
            max_val = float('-inf')
            for m in moves:
                board.make_move(m[0], m[1], test_only=True)
                new_stack = current_stack + [{'move': m, 'depth': depth - remaining_depth + 1}]
                val = dfs_search_with_recording(board, remaining_depth - 1, new_stack)
                board.undo_move(test_only=True)
                max_val = max(max_val, val)
            return max_val
        else:
            min_val = float('inf')
            for m in moves:
                board.make_move(m[0], m[1], test_only=True)
                new_stack = current_stack + [{'move': m, 'depth': depth - remaining_depth + 1}]
                val = dfs_search_with_recording(board, remaining_depth - 1, new_stack)
                board.undo_move(test_only=True)
                min_val = min(min_val, val)
            return min_val
    
    best_move = None
    best_score = float('-inf') if ai_color == 'red' else float('inf')
    
    for move in legal_moves:
        board.make_move(move[0], move[1], test_only=True)
        score = dfs_search_with_recording(board, depth - 1, [{'move': move, 'depth': 1}])
        board.undo_move(test_only=True)
        
        if ai_color == 'red':
            if score > best_score:
                best_score = score
                best_move = move
        else:
            if score < best_score:
                best_score = score
                best_move = move
                
    return best_move


def ucs_move(board, recorder=None):
    """
    UCS: Cost = 1000 - captured_piece_value.
    Finds the move that minimizes the cost (prioritizes highest value capture).
    
    Args:
        board: Current board state
        recorder: Optional StepRecorder for visualization
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None
    
    # Mapping piece names to Vietnamese for better visualization
    PIECE_NAME_VI = {
        'general': 'Tướng',
        'advisor': 'Sĩ',
        'elephant': 'Tượng',
        'horse': 'Mã',
        'rook': 'Xe',
        'cannon': 'Pháo',
        'pawn': 'Tốt'
    }
    
    best_move = None
    min_cost = float('inf')
    
    # Shuffle to avoid deterministic behavior when costs are equal
    random.shuffle(legal_moves)
    
    # For visualization: track frontier and explored
    frontier_list = []
    explored_list = []
    
    for i, (from_pos, to_pos) in enumerate(legal_moves):
        target = board.get_piece(to_pos)
        
        # Calculate cost
        cap_val = PIECE_VALUES.get(target.name, 0) if target else 0
        cost = 1000 - cap_val
        piece_name = PIECE_NAME_VI.get(target.name, '—') if target else '—'
        
        # Build node info for this move
        node_info = {
            'move': (from_pos, to_pos),
            'g_cost': cost,
            'piece_captured': piece_name,
            'cap_val': cap_val
        }
        
        # Add to frontier (will be sorted before recording)
        frontier_list.append(node_info)
        
        # Update best move
        if cost < min_cost:
            min_cost = cost
            best_move = (from_pos, to_pos)
        
        # Record step if recorder is provided
        if recorder:
            # Sort frontier by cost for visualization
            sorted_frontier = sorted(frontier_list, key=lambda x: x['g_cost'])
            
            recorder.add_step(UCSStep(
                step_num=i + 1,
                algorithm="UCS",
                explanation=f"Xét nước {from_pos}→{to_pos}: cost = 1000 - {cap_val}({piece_name}) = {cost}",
                chosen_move=best_move,
                current_node=node_info,
                frontier=sorted_frontier.copy(),
                explored=explored_list.copy()
            ))
        
        # Move current node to explored
        explored_list.append(node_info)
    
    return best_move
