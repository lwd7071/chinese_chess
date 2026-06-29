# Level 1 AI: BFS, DFS, UCS
# Gói chứa các thuật toán tìm kiếm mù (uninformed search) cơ bản: Tìm kiếm theo chiều rộng (BFS), Tìm kiếm theo chiều sâu (DFS), và Tìm kiếm chi phí đồng nhất (UCS).
import random
from collections import deque

from ai.eval import PIECE_VALUES, evaluate_board
from ai.step_recorder import (
    BFSStep,
    DFSStep,
    UCSStep,
    move_to_label,
)

# Bảng dịch tên các quân cờ sang tiếng Việt phục vụ cho hiển thị giao diện và giải thích bước đi
PIECE_NAME_VI = {
    "general": "Tướng",
    "advisor": "Sĩ",
    "elephant": "Tượng",
    "horse": "Mã",
    "rook": "Xe",
    "cannon": "Pháo",
    "pawn": "Tốt",
}


class BFSNode:
    """
    Lớp đại diện cho một nút trong cây tìm kiếm BFS.
    Lưu trữ thông tin trạng thái bàn cờ, nước đi, độ sâu và điểm số đánh giá.
    """
    def __init__(self, node_id, parent_id, root_move, move, board, depth):
        self.id = node_id  # ID duy nhất của nút
        self.parent_id = parent_id  # ID của nút cha
        self.root_move = root_move  # Nước đi gốc từ trạng thái ban đầu (để chọn nước đi cuối cùng)
        self.move = move  # Nước đi dẫn đến trạng thái này
        self.board = board  # Trạng thái bàn cờ tại nút này
        self.depth = depth  # Độ sâu của nút trong cây tìm kiếm
        self.children = []  # Danh sách ID các nút con
        self.score = None  # Điểm số đánh giá của nút (được tính toán từ lá và truyền ngược lên)


def bfs_move(board, depth=2, recorder=None):
    """
    Thuật toán tìm kiếm theo chiều rộng (BFS - Breadth-First Search).
    Thực hiện tìm kiếm giới hạn độ sâu (depth-limited) và lan truyền điểm số đánh giá theo logic Minimax.

    Args:
        board: Trạng thái bàn cờ hiện tại
        depth: Độ sâu tìm kiếm tối đa
        recorder: Đối tượng ghi lại các bước tìm kiếm phục vụ trực quan hóa (nếu có)
    """
    ai_color = board.turn
    legal_moves = board.get_all_legal_moves(ai_color)
    if not legal_moves:
        return None

    # 1. Khởi tạo nút gốc giả lập (synthetic root node) đại diện cho trạng thái hiện tại
    root_node = BFSNode(
        node_id=0, parent_id=None, root_move=None, move=None, board=board, depth=0
    )
    nodes = {0: root_node}
    node_id_counter = 0

    # 2. Hàng đợi BFS và đưa các nút ở độ sâu 1 (các nước đi hợp lệ đầu tiên) vào hàng đợi
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
            depth=1,
        )
        root_node.children.append(node.id)
        nodes[node.id] = node
        queue.append(node)

    # 3. Quá trình khai triển theo từng tầng (level-order expansion)
    while queue:
        curr = queue.popleft()

        # Dừng khai triển nếu đã đạt tới độ sâu tối đa quy định
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
                depth=curr.depth + 1,
            )
            curr.children.append(child.id)
            nodes[child.id] = child
            queue.append(child)

    # 4. Tính toán điểm số cho các nút lá (các nút không có nút con) bằng hàm đánh giá trạng thái
    for node in nodes.values():
        if node.id == 0:
            continue
        if len(node.children) == 0:
            node.score = evaluate_board(node.board)

    # 5. Lan truyền điểm số từ dưới lên trên (bottom-up) theo nguyên tắc Minimax
    sorted_node_ids = sorted(
        nodes.keys(), key=lambda nid: nodes[nid].depth, reverse=True
    )
    for nid in sorted_node_ids:
        node = nodes[nid]
        if len(node.children) > 0:
            child_scores = [nodes[cid].score for cid in node.children]
            # Nếu lượt của Đỏ, chọn điểm số lớn nhất (Max). Ngược lại chọn nhỏ nhất (Min).
            if node.board.turn == "red":
                node.score = max(child_scores)
            else:
                node.score = min(child_scores)

    # 6. Ghi lại các bước duyệt tại độ sâu 1 cùng điểm số Minimax đã tính toán để hiển thị lên GUI
    if recorder:
        explored_nodes = []
        for idx, cid in enumerate(root_node.children):
            cnode = nodes[cid]
            # Xử lý định dạng tên quân cờ
            target = board.get_piece(cnode.move[1])
            piece_key = target.name if target else board.get_piece(cnode.move[0]).name
            char_to_key = {
                "G": "general", "A": "advisor", "E": "elephant",
                "H": "horse", "R": "rook", "C": "cannon", "P": "pawn"
            }
            key = char_to_key.get(piece_key, piece_key)
            piece_vi = PIECE_NAME_VI.get(key, "—")

            node_info = {
                "id": f"n{cnode.id}",
                "move": cnode.move,
                "depth": 1,
                "score": cnode.score,
                "piece": piece_vi,
            }
            explored_nodes.append(node_info)

            queue_info = []
            for remaining_cid in root_node.children[idx + 1 : idx + 1 + 10]:
                rcnode = nodes[remaining_cid]
                rtarget = board.get_piece(rcnode.move[1])
                rpiece_key = rtarget.name if rtarget else board.get_piece(rcnode.move[0]).name
                rkey = char_to_key.get(rpiece_key, rpiece_key)
                rpiece_vi = PIECE_NAME_VI.get(rkey, rkey)
                queue_info.append({
                    "id": f"n{rcnode.id}",
                    "move": rcnode.move,
                    "depth": 1,
                    "piece": rpiece_vi,
                })

            recorder.add_step(
                BFSStep(
                    step_num=idx + 1,
                    algorithm="BFS",
                    explanation=f"BFS xét nước {cnode.move[0]}→{cnode.move[1]}: score = {cnode.score} ({piece_vi})",
                    current_node=node_info,
                    queue=queue_info,
                    explored=explored_nodes.copy(),
                    evaluated=explored_nodes.copy(),
                )
            )

    # 7. Lựa chọn nước đi tốt nhất trong các nước đi gốc (root moves)
    best_move = None
    if ai_color == "red":
        best_score = float("-inf")
        for cid in root_node.children:
            cnode = nodes[cid]
            if cnode.score > best_score:
                best_score = cnode.score
                best_move = cnode.root_move
    else:
        best_score = float("inf")
        for cid in root_node.children:
            cnode = nodes[cid]
            if cnode.score < best_score:
                best_score = cnode.score
                best_move = cnode.root_move

    return best_move


def dfs_move(board, depth=2, recorder=None):
    """
    Thuật toán tìm kiếm theo chiều sâu (DFS - Depth-First Search).
    Thực hiện duyệt sâu dần với giới hạn độ sâu (depth-limited) và tính điểm theo logic Minimax.

    Args:
        board: Trạng thái bàn cờ hiện tại
        depth: Độ sâu tìm kiếm tối đa
        recorder: Đối tượng ghi lại các bước tìm kiếm phục vụ trực quan hóa (nếu có)
    """
    ai_color = board.turn
    legal_moves = board.get_all_legal_moves(ai_color)
    if not legal_moves:
        return None

    # Nếu có đối tượng recorder, tiến hành duyệt có ghi lại log từng bước nhảy và quay lui (backtracking)
    if recorder:
        step_num = [0]
        explored_nodes = []
        backtrack_log = []
        best_move = legal_moves[0]
        best_score = float("-inf") if ai_color == "red" else float("inf")

        def dfs_record(board, current_path_moves, current_path_pieces, remaining_depth, node_id_prefix):
            """
            Hàm đệ quy thực hiện duyệt theo chiều sâu và ghi chép nhật ký bước đi (stack & backtrack).
            """
            nonlocal best_move, best_score
            curr_depth = depth - remaining_depth

            # Chạm giới hạn độ sâu: trả về điểm đánh giá trạng thái hiện tại
            if remaining_depth == 0:
                return evaluate_board(board)

            moves = board.get_all_legal_moves(board.turn)
            if not moves:
                return evaluate_board(board)

            turn_color = board.turn
            is_red = (turn_color == "red")
            best_val = float("-inf") if is_red else float("inf")

            for idx, m in enumerate(moves):
                # Xử lý định dạng tên quân cờ tiếng Việt
                target = board.get_piece(m[1])
                piece_key = target.name if target else board.get_piece(m[0]).name
                char_to_key = {
                    "G": "general", "A": "advisor", "E": "elephant",
                    "H": "horse", "R": "rook", "C": "cannon", "P": "pawn"
                }
                key = char_to_key.get(piece_key, piece_key)
                piece_vi = PIECE_NAME_VI.get(key, "—")

                # Thử thực hiện nước đi
                board.make_move(m[0], m[1], test_only=True)

                child_node_id = f"{node_id_prefix}_{idx + 1}" if node_id_prefix else f"n{idx + 1}"

                # Lập thông tin ngăn xếp (stack) cho đường đi hiện tại
                new_moves = current_path_moves + [m]
                new_pieces = current_path_pieces + [piece_vi]
                stack_info = []
                for i in range(len(new_moves)):
                    stack_info.append({
                        "id": f"{node_id_prefix if i == 0 else ''}",
                        "move": new_moves[i],
                        "depth": i + 1,
                        "piece": new_pieces[i]
                    })

                node_info = {
                    "id": child_node_id,
                    "move": m,
                    "depth": curr_depth + 1,
                    "piece": piece_vi,
                    "score": None
                }

                step_num[0] += 1
                move_lbl = move_to_label(m)
                role = "Ta" if turn_color == ai_color else "Địch"

                # Nếu là tầng áp chót (chạm đáy), tiến hành đánh giá điểm và ghi log
                if remaining_depth - 1 == 0:
                    val = evaluate_board(board)
                    node_info["score"] = val
                    explanation = f"DFS chạm đáy: {role} đi {move_lbl} (depth={curr_depth + 1}), điểm = {val}"
                    explored_nodes.append(node_info)

                    recorder.add_step(
                        DFSStep(
                            step_num=step_num[0],
                            algorithm="DFS",
                            explanation=explanation,
                            current_node=node_info,
                            stack=stack_info.copy(),
                            explored=explored_nodes.copy(),
                            backtrack_log=backtrack_log.copy(),
                            is_backtracking=False
                        )
                    )
                else:
                    # Ghi log quá trình tiếp tục đi sâu xuống tầng dưới
                    explanation = f"DFS đi sâu: {role} đi {move_lbl} (depth={curr_depth + 1})"
                    recorder.add_step(
                        DFSStep(
                            step_num=step_num[0],
                            algorithm="DFS",
                            explanation=explanation,
                            current_node=node_info,
                            stack=stack_info.copy(),
                            explored=explored_nodes.copy(),
                            backtrack_log=backtrack_log.copy(),
                            is_backtracking=False
                        )
                    )

                    val = dfs_record(board, new_moves, new_pieces, remaining_depth - 1, child_node_id)

                # Cập nhật giá trị tốt nhất theo logic Minimax
                if is_red:
                    if val > best_val:
                        best_val = val
                        if curr_depth == 0:
                            best_move = m
                            best_score = val
                else:
                    if val < best_val:
                        best_val = val
                        if curr_depth == 0:
                            best_move = m
                            best_score = val

                # Hoàn trả (undo) nước đi để tiếp tục duyệt nghiệm khác
                board.undo_move(test_only=True)

                backtrack_info = {
                    "id": child_node_id,
                    "move": m,
                    "depth": curr_depth + 1,
                    "piece": piece_vi,
                    "score": val
                }
                backtrack_log.append(backtrack_info)

                step_num[0] += 1
                if curr_depth == 0:
                    explanation = f"DFS backtrack: undo {role} đi {move_lbl}, trả score = {val} về root, so sánh với best hiện tại"
                else:
                    parent_opt = "max_val" if board.turn == "red" else "min_val"
                    explanation = f"DFS backtrack: undo {role} đi {move_lbl}, cập nhật {parent_opt} = {best_val}, thử phản công tiếp theo của {role}"

                parent_stack = []
                for i in range(len(current_path_moves)):
                    parent_stack.append({
                        "id": f"{node_id_prefix if i == 0 else ''}",
                        "move": current_path_moves[i],
                        "depth": i + 1,
                        "piece": current_path_pieces[i]
                    })

                recorder.add_step(
                    DFSStep(
                        step_num=step_num[0],
                        algorithm="DFS",
                        explanation=explanation,
                        current_node=backtrack_info,
                        stack=parent_stack,
                        explored=explored_nodes.copy(),
                        backtrack_log=backtrack_log.copy(),
                        is_backtracking=True
                    )
                )

            return best_val

        dfs_record(board, [], [], depth, "")
        return best_move

    # Hàm tìm kiếm Minimax im lặng (silent) để tính toán điểm số nhanh khi không cần trực quan hóa
    def dfs_eval(board, remaining_depth):
        if remaining_depth == 0:
            return evaluate_board(board)

        moves = board.get_all_legal_moves(board.turn)
        if not moves:
            return evaluate_board(board)

        if board.turn == "red":
            max_val = float("-inf")
            for m in moves:
                board.make_move(m[0], m[1], test_only=True)
                val = dfs_eval(board, remaining_depth - 1)
                board.undo_move(test_only=True)
                max_val = max(max_val, val)
            return max_val
        else:
            min_val = float("inf")
            for m in moves:
                board.make_move(m[0], m[1], test_only=True)
                val = dfs_eval(board, remaining_depth - 1)
                board.undo_move(test_only=True)
                min_val = min(min_val, val)
            return min_val

    best_move = None
    best_score = float("-inf") if ai_color == "red" else float("inf")
    move_scores = {}

    # Duyệt qua các nước đi hợp lệ ban đầu để tìm nước đi có điểm số tối ưu nhất
    for move in legal_moves:
        board.make_move(move[0], move[1], test_only=True)
        score = dfs_eval(board, depth - 1)
        board.undo_move(test_only=True)
        move_scores[move] = score

        if ai_color == "red":
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
    Thuật toán tìm kiếm chi phí đồng nhất (UCS - Uniform-Cost Search).
    Định nghĩa chi phí (Cost) = 1000 - giá trị quân cờ bị ăn (captured_piece_value).
    Thuật toán tìm kiếm nước đi giúp giảm thiểu tối đa chi phí (tương đương với việc ưu tiên ăn quân có giá trị lớn nhất).

    Args:
        board: Trạng thái bàn cờ hiện tại
        recorder: Đối tượng ghi lại các bước tìm kiếm phục vụ trực quan hóa (nếu có)
    """
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None

    # Bảng dịch tên các quân cờ sang tiếng Việt phục vụ hiển thị trực quan
    PIECE_NAME_VI = {
        "general": "Tướng",
        "advisor": "Sĩ",
        "elephant": "Tượng",
        "horse": "Mã",
        "rook": "Xe",
        "cannon": "Pháo",
        "pawn": "Tốt",
    }

    best_move = None
    min_cost = float("inf")

    # Xáo trộn danh sách nước đi để tránh lặp lại một mẫu hành vi cố định khi các chi phí bằng nhau
    random.shuffle(legal_moves)

    # Danh sách theo dõi biên (frontier) và các nút đã duyệt (explored) cho mục đích hiển thị
    frontier_list = []
    explored_list = []

    for i, (from_pos, to_pos) in enumerate(legal_moves):
        target = board.get_piece(to_pos)

        # Tính toán chi phí: nước đi ăn quân càng lớn thì chi phí càng nhỏ
        cap_val = PIECE_VALUES.get(target.name, 0) if target else 0
        cost = 1000 - cap_val

        char_to_key = {
            "G": "general",
            "A": "advisor",
            "E": "elephant",
            "H": "horse",
            "R": "rook",
            "C": "cannon",
            "P": "pawn",
        }
        key = char_to_key.get(target.name, target.name) if target else None
        piece_name = PIECE_NAME_VI.get(key, "—") if key else "—"

        # Tạo thông tin nút cho nước đi hiện tại
        node_info = {
            "move": (from_pos, to_pos),
            "g_cost": cost,
            "piece_captured": piece_name,
            "cap_val": cap_val,
        }

        # Đưa vào danh sách biên (sẽ được sắp xếp theo chi phí trước khi ghi nhận)
        frontier_list.append(node_info)

        # Cập nhật nước đi có chi phí thấp nhất
        if cost < min_cost:
            min_cost = cost
            best_move = (from_pos, to_pos)

        # Ghi lại bước đi nếu có recorder
        if recorder:
            # Sắp xếp danh sách biên theo chi phí g_cost tăng dần để hiển thị trực quan
            sorted_frontier = sorted(frontier_list, key=lambda x: x["g_cost"])

            recorder.add_step(
                UCSStep(
                    step_num=i + 1,
                    algorithm="UCS",
                    explanation=f"Xét nước {from_pos}→{to_pos}: cost = 1000 - {cap_val}({piece_name}) = {cost}",
                    chosen_move=best_move,
                    current_node=node_info,
                    frontier=sorted_frontier.copy(),
                    explored=explored_list.copy(),
                )
            )

        # Chuyển nút hiện tại vào danh sách đã kiểm tra
        explored_list.append(node_info)

    return best_move
