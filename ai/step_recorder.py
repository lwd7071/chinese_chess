"""
Step Recorder Module - Step-by-Step Visualization for AI Algorithms

Module này định nghĩa các dataclass để ghi lại từng bước thực thi của 18 thuật toán AI,
phục vụ mục đích demo và báo cáo trực quan trong buổi thuyết trình đồ án.

Author: Nhóm 1 - Cờ tướng 6 level
Date: 2026-06-25
"""

import threading
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

# Type alias cho dễ đọc
Move = Tuple[Tuple[int, int], Tuple[int, int]]  # ((from_r, from_c), (to_r, to_c))

MAX_VISUALIZATION_STEPS = 10000


def pos_to_label(pos: Optional[Tuple[int, int]]) -> str:
    """Chuyển đổi tọa độ (row, col) sang ký hiệu cờ, ví dụ: (7, 1) -> 'B7'"""
    if not pos or not isinstance(pos, (tuple, list)) or len(pos) < 2:
        return "—"
    r, c = pos
    if 0 <= c <= 8 and 0 <= r <= 9:
        return f"{chr(65 + c)}{r}"
    return f"({r},{c})"


def move_to_label(move: Optional[Move]) -> str:
    """Chuyển đổi move ((r1, c1), (r2, c2)) sang chuỗi ký hiệu, ví dụ: 'B7→B0'"""
    if not move or not isinstance(move, (tuple, list)) or len(move) < 2:
        return "—"
    return f"{pos_to_label(move[0])}→{pos_to_label(move[1])}"



# ============================================================================
# BASE DATACLASS
# ============================================================================


@dataclass
class BaseStep:
    """Base class chung cho tất cả các step"""

    step_num: int
    algorithm: str  # Tên thuật toán: "UCS", "A*", "Alpha-Beta"...
    explanation: str  # Câu giải thích bằng tiếng Việt
    chosen_move: Optional[Move] = None


# ============================================================================
# LEVEL 1 - UNINFORMED SEARCH (BFS, DFS, UCS)
# ============================================================================


@dataclass
class BFSStep(BaseStep):
    """BFS dùng Queue FIFO, mở rộng theo từng tầng depth"""

    current_node: Dict[str, Any] = field(
        default_factory=dict
    )  # {'id': 'n3', 'move': ..., 'depth': 1, 'score': None}
    queue: List[Dict[str, Any]] = field(
        default_factory=list
    )  # Hàng đợi FIFO: [{'id', 'move', 'depth'}]
    explored: List[Dict[str, Any]] = field(
        default_factory=list
    )  # Các node đã duyệt xong
    evaluated: List[Dict[str, Any]] = field(default_factory=list)
    current_depth: int = 0


@dataclass
class DFSStep(BaseStep):
    """DFS dùng Stack LIFO (đệ quy), đi sâu rồi backtrack"""

    current_node: Dict[str, Any] = field(
        default_factory=dict
    )  # {'move': ..., 'depth': 2, 'score': ...}
    stack: List[Dict[str, Any]] = field(
        default_factory=list
    )  # Stack đệ quy: nhánh đang đi sâu
    explored: List[Dict[str, Any]] = field(default_factory=list)
    backtrack_log: List[Dict[str, Any]] = field(default_factory=list)
    is_backtracking: bool = False  # True khi đang quay lui


@dataclass
class UCSStep(BaseStep):
    """UCS dùng Priority Queue, sắp xếp theo g_cost = 1000 - captured_value"""

    current_node: Dict[str, Any] = field(
        default_factory=dict
    )  # {'move': ..., 'g_cost': 200, 'piece_captured': 'Xe'}
    frontier: List[Dict[str, Any]] = field(
        default_factory=list
    )  # Priority Queue sorted by g_cost tăng dần
    explored: List[Dict[str, Any]] = field(default_factory=list)
    evaluated: List[Dict[str, Any]] = field(default_factory=list)


# ============================================================================
# LEVEL 2 - HEURISTIC SEARCH (Greedy, A*, IDA*)
# ============================================================================


@dataclass
class GreedyStep(BaseStep):
    """Greedy chọn nước ăn quân giá trị cao nhất"""

    current_node: Dict[str, Any] = field(
        default_factory=dict
    )  # {'move': ..., 'h': 900, 'piece': 'Xe'}
    candidates: List[Dict[str, Any]] = field(
        default_factory=list
    )  # Tất cả nước đi + h(n) của chúng
    evaluated: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class AStarStep(BaseStep):
    """A* dùng f(n) = g(n) + h(n)"""

    current_node: Dict[str, Any] = field(
        default_factory=dict
    )  # {'move': ..., 'g': 200, 'h': 3500, 'f': 3700}
    frontier: List[Dict[str, Any]] = field(default_factory=list)  # Sorted by f = g + h
    explored: List[Dict[str, Any]] = field(default_factory=list)
    evaluated: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class IDAStarStep(BaseStep):
    """IDA* dùng threshold, tăng dần qua mỗi iteration"""

    current_node: Dict[str, Any] = field(
        default_factory=dict
    )  # {'move': ..., 'g': ..., 'h': ..., 'f': ...}
    threshold: float = float("inf")  # Ngưỡng f hiện tại
    iteration: int = 0  # Vòng lặp thứ mấy (max 3)
    exceeded_f: Optional[float] = None  # f vượt ngưỡng → trả về để tăng threshold
    is_cutoff: bool = False  # True nếu bị cắt vì f > threshold
    status: str = ""
    evaluated: List[Dict[str, Any]] = field(default_factory=list)


# ============================================================================
# LEVEL 3 - LOCAL SEARCH (Hill Climbing, SA, Beam)
# ============================================================================


@dataclass
class HillClimbStep(BaseStep):
    """Hill Climbing đánh giá tất cả neighbors, chọn score cao nhất"""

    current_score: float = 0.0
    current_move: Dict[str, Any] = field(default_factory=dict)
    neighbors: List[Dict[str, Any]] = field(
        default_factory=list
    )  # [{'move': ..., 'score': ...}] tất cả hàng xóm
    best_neighbor: Dict[str, Any] = field(default_factory=dict)
    is_plateau: bool = False  # True nếu best_neighbor <= current (bị kẹt)
    evaluated: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class SAStep(BaseStep):
    """Simulated Annealing: chấp nhận nước tệ hơn theo xác suất e^(ΔE/T)"""

    current_move: Dict[str, Any] = field(
        default_factory=dict
    )  # {'move': ..., 'score': ...}
    candidate_move: Dict[str, Any] = field(
        default_factory=dict
    )  # {'move': ..., 'score': ...}
    temperature: float = 100.0  # Nhiệt độ T hiện tại
    delta_e: float = 0.0  # ΔE = candidate_score - current_score
    accept_prob: float = 0.0  # e^(ΔE/T) nếu ΔE < 0
    accepted: bool = False  # True nếu chấp nhận candidate
    random_value: float = 0.0
    decision: str = ""
    evaluated: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class BeamStep(BaseStep):
    """Local Beam Search: giữ k beam tốt nhất, loại phần còn lại"""

    beam_k: int = 3  # Số beam giữ lại (k=3)
    all_candidates: List[Dict] = field(
        default_factory=list
    )  # Tất cả candidates trước khi cắt
    kept_beams: List[Dict] = field(default_factory=list)  # k beam được giữ lại
    eliminated: List[Dict] = field(default_factory=list)  # Các beam bị loại
    worst_case_scores: List[Dict] = field(
        default_factory=list
    )  # Score sau khi đối thủ phản công (minimax-like)
    evaluated: List[Dict[str, Any]] = field(default_factory=list)


# ============================================================================
# LEVEL 4 - COMPLEX ENVIRONMENTS (Online, AND-OR, Belief)
# ============================================================================


@dataclass
class OnlineStep(BaseStep):
    """Online Search: điều chỉnh trọng số động dựa trên trạng thái chiếu"""

    in_check: bool = False  # Tướng có đang bị chiếu không
    weights_before: Dict[str, int] = field(
        default_factory=dict
    )  # Trọng số trước khi điều chỉnh
    weights_after: Dict[str, int] = field(
        default_factory=dict
    )  # Trọng số sau khi điều chỉnh
    candidates: List[Dict] = field(
        default_factory=list
    )  # Nước đi đánh giá theo trọng số mới
    evaluated: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class AndOrStep(BaseStep):
    """AND-OR Search: OR node = ta chọn, AND node = đối thủ phản công"""

    or_node: Dict[str, Any] = field(default_factory=dict)  # Nước đi ta đang xét (OR)
    and_responses: List[Dict] = field(
        default_factory=list
    )  # Tất cả phản công của đối thủ (AND)
    worst_case: Dict[str, Any] = field(default_factory=dict)  # Phản công tệ nhất cho ta
    guaranteed_score: float = 0.0  # Score đảm bảo nếu chọn nước này
    evaluated: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class BeliefStep(BaseStep):
    """Belief State: ước lượng phong cách đối thủ rồi tính expected utility"""

    opponent_style: str = "unknown"  # "aggressive" / "defensive" / "positional"
    belief_probs: Dict[str, float] = field(
        default_factory=dict
    )  # {'aggressive': 0.6, 'defensive': 0.2, 'positional': 0.2}
    utility_per_style: Dict[str, float] = field(
        default_factory=dict
    )  # {'aggressive': u1, 'defensive': u2, 'positional': u3}
    expected_utility: float = 0.0  # p_agg*u_agg + p_def*u_def + p_pos*u_pos
    u_agg: float = 0.0
    u_def: float = 0.0
    u_pos: float = 0.0
    evaluated: List[Dict[str, Any]] = field(default_factory=list)


# ============================================================================
# LEVEL 5 - CSP (Backtracking, Min-Conflicts, AC-3)
# ============================================================================


@dataclass
class BacktrackStep(BaseStep):
    """Backtracking CSP: chọn biến (quân) có ít nước đi nhất (MRV)"""

    variables: Dict[str, int] = field(
        default_factory=dict
    )  # {from_pos: domain_size} tất cả quân
    chosen_variable: str = ""  # Quân được chọn (MRV = domain nhỏ nhất)
    domain: List[Dict] = field(
        default_factory=list
    )  # Các ô đích khả dĩ của quân được chọn
    best_assignment: Dict = field(
        default_factory=dict
    )  # Ô đích tốt nhất (score cao nhất)
    evaluated: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class MinConflictStep(BaseStep):
    """Min-Conflicts: chọn nước giảm conflict (số quân ta bị đe dọa) nhiều nhất"""

    current_conflicts: int = 0  # Số quân ta đang bị đe dọa trước khi đi
    candidates: List[Dict] = field(
        default_factory=list
    )  # [{'move': ..., 'conflicts_after': ..., 'score': ...}]
    best_candidate: Dict = field(default_factory=dict)  # Nước giảm conflict nhiều nhất
    evaluated: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class AC3Step(BaseStep):
    """AC-3: lọc bỏ nước không an toàn (quân ta đi vào ô bị đe dọa bởi quân rẻ hơn)"""

    all_moves: int = 0  # Tổng số nước hợp lệ
    safe_moves: List[Dict] = field(
        default_factory=list
    )  # Nước an toàn (không bị quân rẻ ăn)
    pruned_moves: List[Dict] = field(
        default_factory=list
    )  # Nước bị lọc (unsafe: quân đắt đi vào ô bị quân rẻ bảo vệ)
    chosen_from_safe: Dict = field(
        default_factory=dict
    )  # Nước tốt nhất trong safe_moves
    evaluated: List[Dict[str, Any]] = field(default_factory=list)


# ============================================================================
# LEVEL 6 - ADVERSARIAL (Minimax, Alpha-Beta, Expectimax)
# ============================================================================


@dataclass
class MinimaxStep(BaseStep):
    """Minimax: duyệt cây game, MAX node tối đa hóa, MIN node tối thiểu hóa"""

    current_node: Dict[str, Any] = field(
        default_factory=dict
    )  # {'move': ..., 'depth': 2, 'is_max': True, 'value': 350}
    current_path: List[Dict] = field(
        default_factory=list
    )  # Đường đi từ root → node hiện tại (KHÔNG lưu toàn bộ cây)
    siblings_evaluated: List[Dict] = field(
        default_factory=list
    )  # Các nhánh cùng cấp đã duyệt xong + value
    best_so_far: Dict = field(
        default_factory=dict
    )  # Nước tốt nhất tìm được đến hiện tại
    node_type: str = "MAX"
    evaluated: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class AlphaBetaStep(BaseStep):
    """Alpha-Beta: Minimax + cắt tỉa nhánh thừa"""

    current_node: Dict[str, Any] = field(
        default_factory=dict
    )  # {'move': ..., 'depth': ..., 'is_max': ..., 'value': ...}
    current_path: List[Dict] = field(
        default_factory=list
    )  # Đường đi từ root → node hiện tại
    alpha: float = float("-inf")  # Giá trị α tại node hiện tại
    beta: float = float("inf")  # Giá trị β tại node hiện tại
    is_pruned: bool = False  # True nếu nhánh này bị cắt
    prune_reason: str = ""  # "β(200) ≤ α(350) → cắt nhánh"
    siblings_evaluated: List[Dict] = field(default_factory=list)
    evaluated_and_pruned: List[Dict[str, Any]] = field(default_factory=list)
    evaluated: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ExpectimaxStep(BaseStep):
    """Expectimax: MAX node + CHANCE node (đối thủ không tối ưu hoàn toàn)"""

    current_node: Dict[str, Any] = field(
        default_factory=dict
    )  # {'move': ..., 'depth': ..., 'is_ai_turn': True}
    is_chance_node: bool = False  # True nếu là node CHANCE (lượt đối thủ)
    child_values: List[Dict] = field(
        default_factory=list
    )  # [{'move': ..., 'value': ...}] giá trị từng nhánh con
    best_value: float = 0.0  # Giá trị tốt nhất (nếu MAX node)
    expected_value: Optional[float] = (
        None  # 0.7 * best + 0.3 * avg(others) (nếu CHANCE node)
    )
    node_type: str = "MAX"
    best_res: float = 0.0
    others_avg: float = 0.0
    evaluated: List[Dict[str, Any]] = field(default_factory=list)


# ============================================================================
# STEP RECORDER CLASS
# ============================================================================


class StepRecorder:
    """
    Quản lý danh sách các bước thực thi của thuật toán AI.

    Được truyền vào các hàm AI như optional parameter:
        ucs_move(board, recorder=StepRecorder())

    Thuật toán gọi recorder.add_step() tại mỗi bước quan trọng.
    GUI đọc recorder.get_current_step() để hiển thị trên VisualizerPanel.
    """

    def __init__(self):
        self.steps: List[BaseStep] = []
        self.current_index: int = 0
        self.lock = threading.Lock()

    def add_step(self, step: BaseStep):
        """Thêm 1 bước thực thi vào danh sách"""
        with self.lock:
            self.steps.append(step)

    def clear(self):
        """Xóa tất cả steps và reset index về 0"""
        with self.lock:
            self.steps.clear()
            self.current_index = 0

    def total_steps(self) -> int:
        """Trả về tổng số bước đã ghi"""
        with self.lock:
            return len(self.steps)

    def get_current_step(self) -> Optional[BaseStep]:
        """Trả về step hiện tại dựa trên current_index"""
        with self.lock:
            if 0 <= self.current_index < len(self.steps):
                return self.steps[self.current_index]
            return None

    def next(self) -> bool:
        """Di chuyển tới step tiếp theo. Return True nếu thành công."""
        with self.lock:
            if self.current_index < len(self.steps) - 1:
                self.current_index += 1
                return True
            return False

    def prev(self) -> bool:
        """Di chuyển về step trước đó. Return True nếu thành công."""
        with self.lock:
            if self.current_index > 0:
                self.current_index -= 1
                return True
            return False

    def reset_to_start(self):
        """Reset index về bước đầu tiên"""
        with self.lock:
            self.current_index = 0

    def reset_to_end(self):
        """Nhảy tới bước cuối cùng"""
        with self.lock:
            if self.steps:
                self.current_index = len(self.steps) - 1
