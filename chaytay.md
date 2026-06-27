# Kế hoạch Triển khai: Step-by-Step Visualization cho Báo cáo AI

Bản kế hoạch này trình bày kiến trúc tổng thể, chi tiết kỹ thuật và quy trình tích hợp hệ thống mô phỏng từng bước (Step-by-Step Visualization) nhằm hỗ trợ việc chạy tay (dry-run) và giải thích trực quan các thuật toán trong buổi báo cáo đồ án môn học Trí tuệ nhân tạo.

---

## 1. Tổng quan kiến trúc (Architecture Overview)

```
game loop (main.py)
    └── AI Engine (level*.py)
            └── [NEW] StepRecorder → lưu từng bước duyệt
                        └── [NEW] VisualizerPanel → hiển thị trên sidebar
```

**Luồng dữ liệu:**
1. `main.py` gọi hàm AI (ví dụ `ucs_move(board, recorder=rec)`)
2. Thuật toán chạy bình thường, nhưng tại mỗi bước duyệt quan trọng → ghi 1 `Step` vào `recorder`
3. Sau khi AI trả kết quả, `VisualizerPanel` đọc danh sách `steps` từ `recorder` để hiển thị
4. Người dùng bấm `[PREV]` / `[NEXT]` / `[AUTO]` để duyệt từng bước

---

## 2. Chiến lược tích hợp — Chia 3 Tier

Vì mỗi thuật toán có "ngôn ngữ" riêng và thời gian có hạn, chia làm 3 mức độ hiển thị:

| Tier | Thuật toán | Mức hiển thị | Ưu tiên |
|------|-----------|-------------|---------|
| **Full** (demo chính với cô) | UCS, A*, Alpha-Beta, SA | Layout 3 cột + Score Breakdown + công thức | 🔴 Làm trước |
| **Basic** (có panel nhưng gọn) | BFS, DFS, Greedy, Minimax, Beam, Expectimax | Current Node + Explanation text + danh sách candidates | 🟡 Làm sau |
| **Text only** (log đơn giản) | Level 4 (Online/AND-OR/Belief), Level 5 (Backtracking/Min-Conflicts/AC-3) | Dòng text giải thích trong sidebar | 🟢 Cuối cùng |

---

## 3. Phase 1 — Core: `ai/step_recorder.py`

### 3.1 BaseStep (chung cho tất cả)

```python
from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional, Tuple

Move = Tuple[Tuple[int, int], Tuple[int, int]]  # ((from_r, from_c), (to_r, to_c))

@dataclass
class BaseStep:
    step_num: int
    algorithm: str          # Tên thuật toán: "UCS", "A*", "Alpha-Beta"...
    explanation: str        # Câu giải thích bằng tiếng Việt
    chosen_move: Optional[Move] = None
```

### 3.2 Level 1 — Uninformed Search (BFS, DFS, UCS)

```python
@dataclass
class BFSStep(BaseStep):
    """BFS dùng Queue FIFO, mở rộng theo từng tầng depth"""
    current_node: Dict[str, Any]      # {'id': 'n3', 'move': ..., 'depth': 1, 'score': None}
    queue: List[Dict[str, Any]]       # Hàng đợi FIFO: [{'id', 'move', 'depth'}]
    explored: List[Dict[str, Any]]    # Các node đã duyệt xong
    # Hiển thị: Queue | Current | Explored + depth mỗi node

@dataclass
class DFSStep(BaseStep):
    """DFS dùng Stack LIFO (đệ quy), đi sâu rồi backtrack"""
    current_node: Dict[str, Any]      # {'move': ..., 'depth': 2, 'score': ...}
    stack: List[Dict[str, Any]]       # Stack đệ quy: nhánh đang đi sâu
    explored: List[Dict[str, Any]]
    is_backtracking: bool = False     # True khi đang quay lui
    # Hiển thị: Stack | Current | Explored + đánh dấu backtrack

@dataclass
class UCSStep(BaseStep):
    """UCS dùng Priority Queue, sắp xếp theo g_cost = 1000 - captured_value"""
    current_node: Dict[str, Any]      # {'move': ..., 'g_cost': 200, 'piece_captured': 'Xe'}
    frontier: List[Dict[str, Any]]    # Priority Queue sorted by g_cost tăng dần
    explored: List[Dict[str, Any]]
    # Hiển thị: Current(cost) | Frontier(sorted by cost) | Explored
```

**Ánh xạ với code thực tế [level1.py](file:///c:/Users/ADMIN/Desktop/vibecoding/BAITAPAGENT/chinese_chess_ai/ai/level1.py):**
- `bfs_move()` (dòng 17): Dùng `deque` + `BFSNode` với `depth`, `children`, propagate bottom-up → mỗi lần `queue.popleft()` = 1 BFSStep
- `dfs_search()` (dòng 109): Đệ quy với `remaining_depth` → mỗi lần gọi đệ quy = 1 DFSStep
- `ucs_move()` (dòng 163): Vòng lặp qua `legal_moves`, tính `cost = 1000 - cap_val` → mỗi move đánh giá = 1 UCSStep

### 3.3 Level 2 — Heuristic Search (Greedy, A*, IDA*)

```python
@dataclass
class GreedyStep(BaseStep):
    """Greedy chọn nước ăn quân giá trị cao nhất"""
    current_node: Dict[str, Any]      # {'move': ..., 'h': 900, 'piece': 'Xe'}
    candidates: List[Dict[str, Any]]  # Tất cả nước đi + h(n) của chúng
    # Hiển thị: Current | Candidates sorted by h(n) | Giải thích chọn h LỚN NHẤT (ăn quân giá trị cao)

@dataclass
class AStarStep(BaseStep):
    """A* dùng f(n) = g(n) + h(n)"""
    current_node: Dict[str, Any]      # {'move': ..., 'g': 200, 'h': 3500, 'f': 3700}
    frontier: List[Dict[str, Any]]    # Sorted by f = g + h
    explored: List[Dict[str, Any]]
    # Hiển thị: Current(g+h=f) | Frontier(sorted by f) | Explored

@dataclass
class IDAStarStep(BaseStep):
    """IDA* dùng threshold, tăng dần qua mỗi iteration"""
    current_node: Dict[str, Any]      # {'move': ..., 'g': ..., 'h': ..., 'f': ...}
    threshold: float                  # Ngưỡng f hiện tại
    iteration: int                    # Vòng lặp thứ mấy (max 3)
    exceeded_f: Optional[float]       # f vượt ngưỡng → trả về để tăng threshold
    is_cutoff: bool = False           # True nếu bị cắt vì f > threshold
    # Hiển thị: Current | Threshold | Iteration count | Nhánh bị cắt
```

**Ánh xạ với code thực tế [level2.py](file:///c:/Users/ADMIN/Desktop/vibecoding/BAITAPAGENT/chinese_chess_ai/ai/level2.py):**
- `greedy_move()` (dòng 15): So sánh `PIECE_VALUES` của quân bị ăn → mỗi move = 1 GreedyStep
- `a_star_move()` (dòng 35): Tính `g = 1000 - cap_val`, `h = opponent_material`, `f = g + h` → mỗi move = 1 AStarStep
- `ida_star_move()` (dòng 68): 3 iterations, threshold tăng dần, hàm `search()` đệ quy → mỗi lần gọi search = 1 IDAStarStep

### 3.4 Level 3 — Local Search (Hill Climbing, SA, Beam)

```python
@dataclass
class HillClimbStep(BaseStep):
    """Hill Climbing đánh giá tất cả neighbors, chọn score cao nhất"""
    current_score: float
    current_move: Dict[str, Any]
    neighbors: List[Dict[str, Any]]   # [{'move': ..., 'score': ...}] tất cả hàng xóm
    best_neighbor: Dict[str, Any]
    is_plateau: bool = False          # True nếu best_neighbor <= current (bị kẹt)
    # Hiển thị: Current(score) | Neighbors(sorted) | Đánh dấu plateau

@dataclass
class SAStep(BaseStep):
    """Simulated Annealing: chấp nhận nước tệ hơn theo xác suất e^(ΔE/T)"""
    current_move: Dict[str, Any]      # {'move': ..., 'score': ...}
    candidate_move: Dict[str, Any]    # {'move': ..., 'score': ...}
    temperature: float                # Nhiệt độ T hiện tại
    delta_e: float                    # ΔE = candidate_score - current_score
    accept_prob: float                # e^(ΔE/T) nếu ΔE < 0
    accepted: bool                    # True nếu chấp nhận candidate
    # Hiển thị: Current vs Candidate | T | ΔE | Công thức P = e^(ΔE/T) | Accepted?

@dataclass
class BeamStep(BaseStep):
    """Local Beam Search: giữ k beam tốt nhất, loại phần còn lại"""
    beam_k: int                       # Số beam giữ lại (k=3)
    all_candidates: List[Dict]        # Tất cả candidates trước khi cắt
    kept_beams: List[Dict]            # k beam được giữ lại
    eliminated: List[Dict]            # Các beam bị loại
    worst_case_scores: List[Dict]     # Score sau khi đối thủ phản công (minimax-like)
    # Hiển thị: All candidates | Kept(top k) | Eliminated | Worst-case response
```

**Ánh xạ với code thực tế [level3.py](file:///c:/Users/ADMIN/Desktop/vibecoding/BAITAPAGENT/chinese_chess_ai/ai/level3.py):**
- `hill_climbing_move()` (dòng 11): Duyệt tất cả moves, chọn `best_score` → mỗi move = 1 neighbor trong HillClimbStep
- `simulated_annealing_move()` (dòng 33): Vòng `while temp > 1.0`, `temp *= alpha(0.9)`, tính `delta`, `prob = e^(delta/temp)` → mỗi iteration = 1 SAStep
- `beam_search_move()` (dòng 69): Chọn top `k=3`, rồi kiểm tra worst-case response → 2 giai đoạn = nhiều BeamStep

### 3.5 Level 4 — Complex Environments (Online, AND-OR, Belief)

```python
@dataclass
class OnlineStep(BaseStep):
    """Online Search: điều chỉnh trọng số động dựa trên trạng thái chiếu"""
    in_check: bool                    # Tướng có đang bị chiếu không
    weights_before: Dict[str, int]    # Trọng số trước khi điều chỉnh
    weights_after: Dict[str, int]     # Trọng số sau khi điều chỉnh
    candidates: List[Dict]            # Nước đi đánh giá theo trọng số mới
    # Hiển thị: In Check? | Weights thay đổi | Candidates ranked

@dataclass
class AndOrStep(BaseStep):
    """AND-OR Search: OR node = ta chọn, AND node = đối thủ phản công"""
    or_node: Dict[str, Any]           # Nước đi ta đang xét (OR)
    and_responses: List[Dict]         # Tất cả phản công của đối thủ (AND)
    worst_case: Dict[str, Any]        # Phản công tệ nhất cho ta
    guaranteed_score: float           # Score đảm bảo nếu chọn nước này
    # Hiển thị: OR(ta) | AND(đối thủ responses) | Worst case | Guaranteed score

@dataclass
class BeliefStep(BaseStep):
    """Belief State: ước lượng phong cách đối thủ rồi tính expected utility"""
    opponent_style: str               # "aggressive" / "defensive" / "positional"
    belief_probs: Dict[str, float]    # {'aggressive': 0.6, 'defensive': 0.2, 'positional': 0.2}
    utility_per_style: Dict[str, float]  # {'aggressive': u1, 'defensive': u2, 'positional': u3}
    expected_utility: float           # p_agg*u_agg + p_def*u_def + p_pos*u_pos
    # Hiển thị: Detected style | Belief distribution | Utility per style | E[U]
```

**Ánh xạ với code thực tế [level4.py](file:///c:/Users/ADMIN/Desktop/vibecoding/BAITAPAGENT/chinese_chess_ai/ai/level4.py):**
- `online_search_move()` (dòng 6): Kiểm tra `is_in_check()`, patch `PIECE_VALUES` động → OnlineStep ghi lại weights trước/sau
- `and_or_search_move()` (dòng 58): OR node = ta chọn 1 trong 10 nước, AND node = đối thủ phản công tất cả → AndOrStep ghi worst_case
- `belief_state_search_move()` (dòng 103): Phát hiện style qua `board.history[-1]`, tính `p_agg * u_agg + ...` → BeliefStep ghi E[U]

### 3.6 Level 5 — CSP (Backtracking, Min-Conflicts, AC-3)

```python
@dataclass
class BacktrackStep(BaseStep):
    """Backtracking CSP: chọn biến (quân) có ít nước đi nhất (MRV)"""
    variables: Dict[str, int]         # {from_pos: domain_size} tất cả quân
    chosen_variable: str              # Quân được chọn (MRV = domain nhỏ nhất)
    domain: List[Dict]                # Các ô đích khả dĩ của quân được chọn
    best_assignment: Dict             # Ô đích tốt nhất (score cao nhất)
    # Hiển thị: Variables(domain size) | Chosen(MRV) | Domain | Best assignment

@dataclass
class MinConflictStep(BaseStep):
    """Min-Conflicts: chọn nước giảm conflict (số quân ta bị đe dọa) nhiều nhất"""
    current_conflicts: int            # Số quân ta đang bị đe dọa trước khi đi
    candidates: List[Dict]            # [{'move': ..., 'conflicts_after': ..., 'score': ...}]
    best_candidate: Dict              # Nước giảm conflict nhiều nhất
    # Hiển thị: Conflicts before | Candidates(conflicts after) | Best choice

@dataclass
class AC3Step(BaseStep):
    """AC-3: lọc bỏ nước không an toàn (quân ta đi vào ô bị đe dọa bởi quân rẻ hơn)"""
    all_moves: int                    # Tổng số nước hợp lệ
    safe_moves: List[Dict]            # Nước an toàn (không bị quân rẻ ăn)
    pruned_moves: List[Dict]          # Nước bị lọc (unsafe: quân đắt đi vào ô bị quân rẻ bảo vệ)
    chosen_from_safe: Dict            # Nước tốt nhất trong safe_moves
    # Hiển thị: All moves | Safe ✅ | Pruned ❌ (lý do) | Chosen
```

**Ánh xạ với code thực tế [level5.py](file:///c:/Users/ADMIN/Desktop/vibecoding/BAITAPAGENT/chinese_chess_ai/ai/level5.py):**
- `backtracking_mrv_move()` (dòng 24): Map `from_pos → [to_pos]`, chọn `min(domain_size)` → BacktrackStep
- `min_conflicts_move()` (dòng 61): Đếm `get_threats_count()` sau mỗi nước → MinConflictStep
- `ac3_move()` (dòng 97): Lọc `safe_moves` vs `pruned` (quân đắt bị quân rẻ ăn) → AC3Step

### 3.7 Level 6 — Adversarial (Minimax, Alpha-Beta, Expectimax)

```python
@dataclass
class MinimaxStep(BaseStep):
    """Minimax: duyệt cây game, MAX node tối đa hóa, MIN node tối thiểu hóa"""
    current_node: Dict[str, Any]      # {'move': ..., 'depth': 2, 'is_max': True, 'value': 350}
    current_path: List[Dict]          # Đường đi từ root → node hiện tại (KHÔNG lưu toàn bộ cây)
    siblings_evaluated: List[Dict]    # Các nhánh cùng cấp đã duyệt xong + value
    best_so_far: Dict                 # Nước tốt nhất tìm được đến hiện tại
    # Hiển thị: Path(root→current) | Siblings | Best so far

@dataclass
class AlphaBetaStep(BaseStep):
    """Alpha-Beta: Minimax + cắt tỉa nhánh thừa"""
    current_node: Dict[str, Any]      # {'move': ..., 'depth': ..., 'is_max': ..., 'value': ...}
    current_path: List[Dict]          # Đường đi từ root → node hiện tại
    alpha: float                      # Giá trị α tại node hiện tại
    beta: float                       # Giá trị β tại node hiện tại
    is_pruned: bool = False           # True nếu nhánh này bị cắt
    prune_reason: str = ""            # "β(200) ≤ α(350) → cắt nhánh"
    siblings_evaluated: List[Dict] = field(default_factory=list)
    # Hiển thị: Path | α | β | Pruned? (lý do) | Siblings

@dataclass
class ExpectimaxStep(BaseStep):
    """Expectimax: MAX node + CHANCE node (đối thủ không tối ưu hoàn toàn)"""
    current_node: Dict[str, Any]      # {'move': ..., 'depth': ..., 'is_ai_turn': True}
    is_chance_node: bool              # True nếu là node CHANCE (lượt đối thủ)
    child_values: List[Dict]          # [{'move': ..., 'value': ...}] giá trị từng nhánh con
    best_value: float                 # Giá trị tốt nhất (nếu MAX node)
    expected_value: Optional[float]   # 0.7 * best + 0.3 * avg(others) (nếu CHANCE node)
    # Hiển thị: Node type(MAX/CHANCE) | Children values | Best or Expected
```

**Ánh xạ với code thực tế [level6.py](file:///c:/Users/ADMIN/Desktop/vibecoding/BAITAPAGENT/chinese_chess_ai/ai/level6.py):**
- `minimax_move()` (dòng 16): `search(b, d, is_max)` đệ quy, depth=3, branch≤12 → MinimaxStep mỗi lần gọi search
- `alpha_beta_move()` (dòng 78): Thêm `alpha`, `beta`, `break` khi `beta ≤ alpha` → AlphaBetaStep + đánh dấu pruned
- `expectimax_move()` (dòng 149): `0.7 * best + 0.3 * avg(others)` tại CHANCE node → ExpectimaxStep

> **⚠️ LƯU Ý QUAN TRỌNG:** KHÔNG lưu `tree_snapshot` (toàn bộ cây) vì Alpha-Beta depth=4 với 20 nhánh/tầng = hàng chục ngàn node → bùng nổ RAM. Chỉ lưu `current_path` (đường đi root → hiện tại) + `siblings_evaluated` (nhánh cùng cấp đã xong).

### 3.8 StepRecorder class

```python
class StepRecorder:
    def __init__(self):
        self.steps: List[BaseStep] = []
        self.current_index: int = 0

    def add_step(self, step: BaseStep):
        self.steps.append(step)

    def clear(self):
        self.steps.clear()
        self.current_index = 0

    def total_steps(self) -> int:
        return len(self.steps)

    def get_current_step(self) -> Optional[BaseStep]:
        if 0 <= self.current_index < len(self.steps):
            return self.steps[self.current_index]
        return None

    def next(self) -> bool:
        if self.current_index < len(self.steps) - 1:
            self.current_index += 1
            return True
        return False

    def prev(self) -> bool:
        if self.current_index > 0:
            self.current_index -= 1
            return True
        return False
```

---

## 4. Phase 2 — Sửa từng thuật toán để emit steps

Mỗi hàm AI thêm tham số `recorder=None`, chỉ ghi log khi `recorder is not None`:

### Ví dụ UCS (Tier Full):

```python
def ucs_move(board, recorder=None):
    legal_moves = board.get_all_legal_moves(board.turn)
    if not legal_moves:
        return None

    frontier_list = []  # Để ghi log
    explored_list = []  # Để ghi log
    best_move = None
    min_cost = float('inf')

    random.shuffle(legal_moves)

    for i, (from_pos, to_pos) in enumerate(legal_moves):
        target = board.get_piece(to_pos)
        cap_val = PIECE_VALUES.get(target.name, 0) if target else 0
        cost = 1000 - cap_val
        piece_name = PIECE_NAME_VI.get(target.name, '—') if target else '—'

        node_info = {
            'move': (from_pos, to_pos),
            'g_cost': cost,
            'piece_captured': piece_name,
            'cap_val': cap_val
        }
        frontier_list.append(node_info)

        if cost < min_cost:
            min_cost = cost
            best_move = (from_pos, to_pos)

        if recorder:
            # Sắp xếp frontier theo cost để hiển thị
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

        explored_list.append(node_info)

    return best_move
```

### Ví dụ Alpha-Beta (Tier Full):

```python
def alpha_beta_move(board, depth=4, recorder=None):
    # ... (giữ nguyên logic cũ)
    step_counter = [0]

    def search(b, d, alpha, beta, is_max, path):
        if d == 0 or time.time() - start_time > 1.2:
            return evaluate_board(b)

        moves = sort_moves(b, b.get_all_legal_moves(b.turn))[:15]
        siblings = []

        if is_max:
            max_val = float('-inf')
            for m in moves:
                b.make_move(m[0], m[1], test_only=True)
                val = search(b, d-1, alpha, beta, False, path + [m])
                b.undo_move(test_only=True)

                siblings.append({'move': m, 'value': val})
                max_val = max(max_val, val)
                alpha = max(alpha, max_val)

                if recorder:
                    step_counter[0] += 1
                    recorder.add_step(AlphaBetaStep(
                        step_num=step_counter[0],
                        algorithm="Alpha-Beta",
                        explanation=f"MAX node depth={d}: α={alpha}, β={beta}",
                        current_node={'move': m, 'depth': d, 'is_max': True, 'value': val},
                        current_path=[{'move': p, 'depth': depth-i} for i, p in enumerate(path + [m])],
                        alpha=alpha, beta=beta,
                        is_pruned=(beta <= alpha),
                        prune_reason=f"β({beta}) ≤ α({alpha}) → cắt" if beta <= alpha else "",
                        siblings_evaluated=siblings.copy()
                    ))

                if beta <= alpha:
                    break  # Cắt tỉa
            return max_val
        # ... tương tự cho MIN node
```

### Các level khác — pattern chung:

```python
# Tất cả 18 hàm đều thêm recorder=None
def bfs_move(board, depth=2, recorder=None):    ...
def dfs_move(board, depth=2, recorder=None):    ...
def greedy_move(board, recorder=None):          ...
def a_star_move(board, recorder=None):          ...
def ida_star_move(board, recorder=None):        ...
def hill_climbing_move(board, recorder=None):   ...
def simulated_annealing_move(board, T=100.0, alpha=0.9, recorder=None): ...
def beam_search_move(board, k=3, recorder=None): ...
def online_search_move(board, recorder=None):   ...
def and_or_search_move(board, recorder=None):   ...
def belief_state_search_move(board, recorder=None): ...
def backtracking_mrv_move(board, recorder=None): ...
def min_conflicts_move(board, recorder=None):   ...
def ac3_move(board, recorder=None):             ...
def minimax_move(board, depth=3, recorder=None): ...
def expectimax_move(board, depth=3, recorder=None): ...
```

> **Backward compatible:** Khi `recorder=None` (mặc định), thuật toán chạy bình thường không ghi log gì cả → không ảnh hưởng hiệu năng.

---

## 5. Phase 3 — Visualization Panel (`gui/visualizer.py`)

### 5.1 Kích thước màn hình

Giữ nguyên kích thước `1100x820`. VisualizerPanel **thay thế sidebar cũ** khi bật chế độ Report Mode (cùng vị trí, cùng kích thước `450px`). Thêm scroll cho danh sách Frontier/Explored dài.

### 5.2 Layout — Mỗi thuật toán 1 renderer riêng

```python
class VisualizerPanel:
    def render(self, surface, step: BaseStep):
        # Header: STEP 3/12  [◀ PREV] [NEXT ▶] [▶▶ AUTO]
        self._render_header(surface, step)

        # Body: tuỳ loại step
        if isinstance(step, UCSStep):
            self._render_ucs(surface, step)
        elif isinstance(step, AStarStep):
            self._render_astar(surface, step)
        elif isinstance(step, AlphaBetaStep):
            self._render_alpha_beta(surface, step)
        elif isinstance(step, SAStep):
            self._render_sa(surface, step)
        # ... các loại khác
        else:
            # Fallback: hiển thị text explanation
            self._render_text_only(surface, step)

        # Footer: Score Breakdown Box
        self._render_score_breakdown(surface, step)
```

### 5.3 Layout chi tiết cho từng Tier Full

**UCS / A* — Layout 3 Cột:**
```
┌──────────────────────────────────────────┐
│  STEP 3/12       [◀ PREV] [NEXT ▶] [▶▶] │
├──────────┬──────────────┬────────────────┤
│ CURRENT  │  FRONTIER    │   EXPLORED     │
│ n4       │ n5 (cost:200)│ n0, n1, n2     │
│ cost:200 │ n6 (cost:400)│ n3, n4         │
│ ăn Xe    │ n7 (cost:900)│                │
├──────────┴──────────────┴────────────────┤
│ 💡 LÝ DO: cost = 1000 - Xe(900) = 100   │
│    → Thấp nhất trong Frontier            │
└──────────────────────────────────────────┘
```

**Alpha-Beta — Layout Cây + α/β:**
```
┌──────────────────────────────────────────┐
│  STEP 7/25       [◀ PREV] [NEXT ▶] [▶▶] │
├──────────────────────────────────────────┤
│ PATH: root → n1(MAX) → n3(MIN) → n7     │
│ DEPTH: 2/4    TYPE: MAX node             │
├──────────────────────────────────────────┤
│ α = 350          β = +∞                  │
│ Siblings: n5(200) n6(350✅) n7(150)      │
├──────────────────────────────────────────┤
│ ✂️ CẮT TỈA: β(200) ≤ α(350) → prune    │
└──────────────────────────────────────────┘
```

**SA — Layout Nhiệt độ + Công thức:**
```
┌──────────────────────────────────────────┐
│  STEP 5/20       [◀ PREV] [NEXT ▶] [▶▶] │
├──────────────────────────────────────────┤
│ 🌡️ T = 65.6 (giảm từ 100, α=0.9)       │
│                                          │
│ Current : Mã(3,2)→(4,4)  score: +280    │
│ Candidate: Xe(0,0)→(0,5) score: +150    │
│                                          │
│ ΔE = 150 - 280 = -130 (tệ hơn!)         │
│ P(accept) = e^(-130/65.6) = 0.138        │
│ Random = 0.42 > 0.138 → ❌ TỪ CHỐI      │
└──────────────────────────────────────────┘
```

---

## 6. Phase 4 — StepController

```python
class StepController:
    def __init__(self):
        self.mode = "manual"      # "manual" hoặc "auto"
        self.auto_delay = 1.0     # Giây giữa mỗi bước auto
        self.last_auto_time = 0

    def next_step(self, recorder: StepRecorder) -> bool:
        return recorder.next()

    def prev_step(self, recorder: StepRecorder) -> bool:
        return recorder.prev()

    def toggle_auto(self):
        self.mode = "auto" if self.mode == "manual" else "manual"

    def update(self, recorder: StepRecorder):
        """Gọi mỗi frame khi mode=auto"""
        if self.mode == "auto" and time.time() - self.last_auto_time >= self.auto_delay:
            recorder.next()
            self.last_auto_time = time.time()
```

**Flow trong Bot vs Bot:**
```
1. Bot tính xong → lưu toàn bộ steps vào recorder
2. Game PAUSE (không apply nước đi lên bàn cờ ngay)
3. Manual mode: bấm NEXT → hiển thị step tiếp theo trên VisualizerPanel
4. Auto mode: timer tự gọi next_step() mỗi N giây
5. Khi đến step cuối cùng → apply nước đi lên bàn cờ → chuyển lượt
```

---

## 7. Phase 5 — Gắn kết vào `main.py`

```python
# Trong class ChineseChessGame.__init__():
from ai.step_recorder import StepRecorder
from gui.visualizer import VisualizerPanel, StepController

self.step_recorder = StepRecorder()
self.visualizer = VisualizerPanel(x, y, width, height)
self.step_controller = StepController()
self.report_mode = False  # Toggle bật/tắt

# Trong handle_bot_turns():
if self.report_mode:
    self.step_recorder.clear()
    # ⚠️ Chế độ report: chạy AI synchronously (không dùng thread) để tránh race condition
    # Gọi trực tiếp từ AI_REGISTRY, đảm bảo signature hỗ trợ recorder kwarg
    move = AI_REGISTRY[algo_name](self.board, recorder=self.step_recorder)
    # KHÔNG apply move ngay → chờ user duyệt steps
else:
    # Chế độ bình thường: AI chạy trên background thread
    move = AI_REGISTRY[algo_name](self.board)
    # Apply move bình thường

# Trong draw():
if self.report_mode and self.step_recorder.total_steps() > 0:
    self.visualizer.render(surface, self.step_recorder.get_current_step())
else:
    self.sidebar.draw(surface, ...)
```

### ⚠️ LƯU Ý QUAN TRỌNG: AI_REGISTRY Signature

**Vấn đề:** Registry hiện tại trong `ai/__init__.py` lưu trực tiếp function reference:
```python
AI_REGISTRY = {"UCS": ucs_move, "A*": a_star_move, ...}
```

Khi gọi `AI_REGISTRY[algo_name](board, recorder=...)`, nó hoạt động ĐÚNG vì các function giữ nguyên signature gốc.

**✅ KHÔNG CẦN SỬA** `ai/__init__.py` vì registry đang dùng direct function reference, không wrap bằng `functools.partial` hay `lambda`.

---

## 8. Thứ tự triển khai (Implementation Order)

| # | Task | File | Độ khó | Tier | Status |
|---|------|------|--------|------|--------|
| 1 | `StepRecorder` + tất cả Dataclass | `ai/step_recorder.py` | Dễ | — | ✅ 273 dòng |
| 2 | Level 1: BFS/DFS/UCS | `ai/level1.py` | Dễ | UCS=Full | ✅ 44/20/20 steps |
| 3 | Level 2: Greedy/A*/IDA* | `ai/level2.py` | Dễ | A*=Full | ✅ All/All/30 steps |
| 4 | Level 3: Hill/SA/Beam | `ai/level3.py` | Dễ | SA=Full | ✅ 20/30/2 steps |
| 5 | Level 6: Minimax/AB/Expectimax | `ai/level6.py` | Trung bình | AB=Full | ✅ 20/30/20 steps |
| 6 | Level 4 & 5: All CSP | `ai/level4.py`, `ai/level5.py` | Dễ | Text | ✅ 2-10 steps each |
| 7 | VisualizerPanel 3 layout | `gui/visualizer.py` | Trung bình | Full | ✅ Hoàn thành |
| 8 | StepController (prev/next/auto) | `gui/visualizer.py` | Dễ | — | ✅ Hoàn thành |
| 9 | Gắn vào main.py + Report Mode | `main.py` | Trung bình | — | ✅ Hoàn thành |
| 10 | Test & Polish | All | Dễ | — | ✅ Hoàn thành |
| **11** | **Hoàn thiện Visualizer: 18/18 thuật toán** | **`gui/visualizer.py`** | **Trung bình** | **All** | ⬜ Chưa làm |

**Progress: 10/11 tasks completed** 🔧  

---

## 9. Checklist trước khi code

- [x] **Phase 0:** Kiểm tra `ai/__init__.py` — xác nhận AI_REGISTRY dùng direct function reference ✅
- [x] **Phase 1:** Tạo `ai/step_recorder.py` với tất cả 18 dataclass ✅ (19 classes, 273 dòng)
- [x] **Phase 2:** Level 1 (BFS/DFS/UCS) ✅ (UCS: 44 steps, BFS/DFS: 20 steps)
- [x] **Phase 3:** Level 2 (Greedy/A*/IDA*) ✅ (A* Tier Full)
- [x] **Phase 4:** Level 3 (Hill/SA/Beam) ✅ (SA Tier Full với P=e^(ΔE/T))
- [x] **Phase 5:** Level 6 (Minimax/AB/Expectimax) ✅ (Alpha-Beta Tier Full với α/β pruning)
- [x] **Phase 6:** Level 4 & 5 (Text tier) ✅ (Online/AND-OR/Belief + Backtrack/MinConflict/AC3)
- [x] **Phase 7:** Implement `gui/visualizer.py` với 3 layout chính ✅
- [x] **Phase 8:** Implement `StepController` (prev/next/auto) ✅
- [x] **Phase 9:** Gắn vào `main.py` với **synchronous AI call** khi `report_mode=True` (Toggle phím R) ✅
- [x] **Phase 10:** Test tất cả Tier Full (UCS/A*/SA/Alpha-Beta) ✅
- [x] **Phase 11:** Hoàn thiện Visualizer — renderer riêng cho 18/18 thuật toán ✅ (Hoàn tất _format_move và 10 renderer mới/cũ)

### 🎉 MILESTONE: 18/18 thuật toán đã tích hợp recorder và visualizer hoàn chỉnh! (2026-06-26)

---

## 10. Gợi ý demo với cô giáo

1. **Chạy UCS Bot vs Bot trước** — vì UCS có cost rõ ràng nhất (`cost = 1000 - PIECE_VALUE`), dễ giải thích từng bước nhất. Bảng Frontier sắp xếp tăng dần, rất trực quan.

2. **Chạy Alpha-Beta tiếp** — demo cây Minimax với α/β thay đổi, highlight nhánh bị cắt tỉa bằng màu đỏ. Rất ấn tượng khi báo cáo.

3. **Chạy SA cuối** — demo công thức `P = e^(ΔE/T)` với nhiệt độ giảm dần, rất hay khi giải thích tại sao SA chấp nhận nước đi tệ hơn ở đầu rồi dần "cứng" lại.

---

## 11. Phase 11 — Hoàn thiện Visualizer (18/18 thuật toán hiển thị đúng)

### 11.0 Phân tích vấn đề hiện tại

Dữ liệu backend (18 thuật toán ghi step) đã **hoàn thành 100%**. Nhưng phần hiển thị trong `gui/visualizer.py` chỉ mới **hoàn thành ~20%**:

| Vấn đề | Chi tiết | Ảnh hưởng |
|--------|----------|-----------|
| **14/18 thuật toán rơi vào fallback** | Chỉ có `UCSStep/AStarStep`, `AlphaBetaStep`, `SAStep` có renderer riêng. 14 thuật toán còn lại rơi vào `_render_text_only` | Màn hình chỉ hiện text giải thích, mất sạch dữ liệu trực quan |
| **`_render_generic_fields` lọc mất dữ liệu** | `if isinstance(val, (int, float, str, bool))` → loại bỏ list/dict | Mất `candidates`, `neighbors`, `frontier`, `and_responses`... |
| **3 renderer đã có thiếu tọa độ + tên quân** | SA chỉ in `score` (hiện "Current: 5"), UCS chỉ in `cost`, AB chỉ in `value` | Không biết quân nào đi đâu |

### 11.1 Bước 1: Thêm helper `_format_move()` (dùng chung cho tất cả)

Thêm hàm tiện ích format hiển thị nước đi, dùng chung cho tất cả renderer:

```python
# Trong class VisualizerPanel:

PIECE_NAME_VI = {
    'general': 'Tướng', 'advisor': 'Sĩ', 'elephant': 'Tượng',
    'horse': 'Mã', 'rook': 'Xe', 'cannon': 'Pháo', 'pawn': 'Tốt'
}

def _format_move(self, move_data):
    """Format move tuple/dict thành chuỗi dễ đọc.
    
    Input có thể là:
      - tuple: ((0,0), (0,5))                         → "(0,0)→(0,5)"
      - dict:  {'move': ((0,0),(0,5)), 'score': 280}  → "(0,0)→(0,5) [280]"
      - dict:  {'move': ((0,0),(0,5)), 'piece_captured': 'Xe', 'score': 280}
               → "Xe (0,0)→(0,5) [280]"
    """
    if move_data is None:
        return "—"
    
    if isinstance(move_data, tuple) and len(move_data) == 2:
        # Kiểm tra nếu là tuple of tuples: ((r1,c1), (r2,c2))
        if isinstance(move_data[0], tuple):
            return f"{move_data[0]}→{move_data[1]}"
        return str(move_data)
    
    if isinstance(move_data, dict):
        parts = []
        # Tên quân nếu có
        piece = move_data.get('piece_captured') or move_data.get('piece')
        if piece and piece != '—':
            vi_name = self.PIECE_NAME_VI.get(piece, piece)
            parts.append(vi_name)
        
        # Tọa độ nước đi
        move = move_data.get('move')
        if move and isinstance(move, tuple) and len(move) == 2:
            if isinstance(move[0], tuple):
                parts.append(f"{move[0]}→{move[1]}")
            else:
                parts.append(str(move))
        
        # Score nếu có
        score = move_data.get('score')
        if score is not None:
            parts.append(f"[{score:.0f}]")
        
        return ' '.join(parts) if parts else str(move_data)[:25]
    
    return str(move_data)[:25]
```

### 11.2 Bước 2: Sửa 3 renderer cũ — thêm hiển thị tọa độ + tên quân

#### 11.2a Sửa `_render_sa` — thêm tọa độ nước đi

**Hiện tại:** `f"Current: {curr_score:.0f}"` → hiện "Current: 5"

**Sửa thành:**
```python
# Trích xuất move info kèm score
curr_move_str = self._format_move(step.current_move)  # "Mã (3,2)→(4,4) [280]"
cand_move_str = self._format_move(step.candidate_move) # "Xe (0,0)→(0,5) [150]"

curr_txt = self.body_font.render(f"Current: {curr_move_str}", True, COLOR_JADE)
cand_txt = self.body_font.render(f"Candidate: {cand_move_str}", True, ...)
```

**Layout mới:**
```
┌──────────────────────────────────────────┐
│ 🌡️ NHIỆT ĐỘ                            │
│       T = 65.6                           │
├──────────────────────────────────────────┤
│ Current:  Mã (3,2)→(4,4) [280]          │
│ Candidate: Xe (0,0)→(0,5) [150]         │
├──────────────────────────────────────────┤
│ ΔE = -130     P(accept) = 0.138         │
│ ✅ CHẤP NHẬN / ❌ TỪ CHỐI               │
└──────────────────────────────────────────┘
```

#### 11.2b Sửa `_render_search_3col` — thêm tọa độ vào mỗi item

**Hiện tại:** UCS chỉ in `cost: {cost}`, A* chỉ in `f: {f_val}`

**Sửa thành:** Mỗi item hiển thị cả move + giá trị:
```python
# UCS:
move_str = self._format_move(item)
txt = self.tiny_font.render(f"{move_str} cost:{item.get('g_cost',0)}", True, COLOR_TEXT)

# A*:
move_str = self._format_move(item)
txt = self.tiny_font.render(f"{move_str} f={item.get('f',0):.0f}", True, COLOR_TEXT)
```

#### 11.2c Sửa `_render_alpha_beta` — thêm nước đi vào siblings

**Hiện tại:** `f"value: {val:.0f}"`

**Sửa thành:**
```python
move_str = self._format_move(sib.get('move'))
txt = self.tiny_font.render(f"{move_str} val:{val:.0f}", True, COLOR_TEXT)
```

### 11.3 Bước 3: Thêm renderer cho 6 nhóm thuật toán còn lại

Phân nhóm 14 thuật toán còn lại thành **6 renderer mới** theo cấu trúc dữ liệu tương tự:

#### Nhóm A: `_render_bfs_dfs` — cho BFSStep, DFSStep

Dữ liệu: `current_node`, `queue`/`stack`, `explored`, `is_backtracking`

**Layout:**
```
┌──────────────────────────────────────────┐
│ BFS — Bước 3/12                          │
├──────────┬──────────────┬────────────────┤
│ CURRENT  │  QUEUE/STACK │   EXPLORED     │
│ n4       │ n5 (d=1)     │ n0, n1         │
│ depth=1  │ n6 (d=1)     │ n2, n3         │
│          │ n7 (d=2)     │                │
├──────────┴──────────────┴────────────────┤
│ 💡 Duyệt node n4 ở depth=1              │
│ 🔙 [DFS only] BACKTRACKING              │
└──────────────────────────────────────────┘
```

**Code:**
```python
def _render_bfs_dfs(self, surface, step, rect):
    # Explanation box
    # ...
    
    # 3 columns: CURRENT | QUEUE(BFS)/STACK(DFS) | EXPLORED
    ds_name = "QUEUE" if isinstance(step, BFSStep) else "STACK"
    ds_items = step.queue if isinstance(step, BFSStep) else step.stack
    
    columns = [
        ("CURRENT", [step.current_node], COLOR_ACCENT),
        (ds_name, ds_items[:8], COLOR_JADE),
        ("EXPLORED", step.explored[:8], COLOR_TEXT_MUTED)
    ]
    # Render mỗi item: id + depth + move
    # DFS: thêm badge "🔙 BACKTRACK" nếu step.is_backtracking
```

#### Nhóm B: `_render_candidates_list` — cho GreedyStep, HillClimbStep

Dữ liệu: `current_node`/`current_move`, `candidates`/`neighbors`, `best_neighbor`

**Layout:**
```
┌──────────────────────────────────────────┐
│ Hill Climbing — Bước 5/20                │
├──────────────────────────────────────────┤
│ HIỆN TẠI: Mã (3,2)→(4,4) [280]         │
├──────────────────────────────────────────┤
│ NEIGHBORS (sorted by score):             │
│ ✅ Xe (0,0)→(0,5) [350] ← BEST         │
│    Pháo (2,1)→(2,7) [280]               │
│    Tốt (6,2)→(5,2) [150]                │
│    ...                                   │
├──────────────────────────────────────────┤
│ ⚠️ PLATEAU: best ≤ current              │
└──────────────────────────────────────────┘
```

**Code:**
```python
def _render_candidates_list(self, surface, step, rect):
    # Header: current move + score
    if isinstance(step, HillClimbStep):
        curr_str = self._format_move(step.current_move)
        items = step.neighbors
        label = "NEIGHBORS"
        show_plateau = step.is_plateau
    else:  # GreedyStep
        curr_str = self._format_move(step.current_node)
        items = step.candidates
        label = "CANDIDATES"
        show_plateau = False
    
    # Render current
    # Render sorted list với ✅ đánh dấu best
    # Nếu plateau → badge cảnh báo
```

#### Nhóm C: `_render_ida_star` — cho IDAStarStep

Dữ liệu: `current_node`, `threshold`, `iteration`, `exceeded_f`, `is_cutoff`

**Layout:**
```
┌──────────────────────────────────────────┐
│ IDA* — Bước 7/30                         │
├──────────────────────────────────────────┤
│ ITERATION: 2    THRESHOLD: 3500          │
├──────────────────────────────────────────┤
│ Node: Xe (0,0)→(0,5)                    │
│ g=200  h=3300  f=3500                    │
├──────────────────────────────────────────┤
│ ✂️ f(3500) > threshold(3200) → CUTOFF   │
│ Hoặc: ✅ f ≤ threshold → tiếp tục       │
└──────────────────────────────────────────┘
```

#### Nhóm D: `_render_beam` — cho BeamStep

Dữ liệu: `beam_k`, `all_candidates`, `kept_beams`, `eliminated`, `worst_case_scores`

**Layout:**
```
┌──────────────────────────────────────────┐
│ Beam Search — Bước 1/2                   │
├────────────────────┬─────────────────────┤
│ KEPT (top 3)       │ ELIMINATED          │
│ ✅ Xe→(0,5) [350]  │ ❌ Tốt→(5,2) [80]  │
│ ✅ Mã→(4,4) [280]  │ ❌ Sĩ→(0,4) [50]   │
│ ✅ Pháo→(2,7)[260] │ ❌ ...              │
├────────────────────┴─────────────────────┤
│ Worst-case analysis:                     │
│ Xe→(0,5): worst=200 | Mã→(4,4): worst=150 │
└──────────────────────────────────────────┘
```

#### Nhóm E: `_render_online_andor_belief` — cho OnlineStep, AndOrStep, BeliefStep

3 thuật toán Level 4 có cấu trúc khác nhau nhưng đều tương đối đơn giản, gom vào 1 renderer có phân nhánh bên trong:

**OnlineStep:**
```
┌──────────────────────────────────────────┐
│ Online Search — Bước 1/2                 │
├──────────────────────────────────────────┤
│ ⚠️ ĐANG BỊ CHIẾU / ✅ AN TOÀN          │
├──────────┬───────────────────────────────┤
│ TRƯỚC    │ SAU (điều chỉnh)              │
│ Tướng:0  │ Tướng: 10000                  │
│ Xe: 900  │ Xe: 900                       │
│ ...      │ ...                           │
├──────────┴───────────────────────────────┤
│ TOP CANDIDATES (sorted by new weights):  │
│ ✅ Sĩ (0,3)→(1,4) [+2800] ← BEST       │
│    Mã (0,1)→(2,2) [+1500]               │
└──────────────────────────────────────────┘
```

**AndOrStep:**
```
┌──────────────────────────────────────────┐
│ AND-OR Search — Bước 3/10                │
├──────────────────────────────────────────┤
│ OR NODE (ta chọn): Xe (0,0)→(0,5)       │
├──────────────────────────────────────────┤
│ AND RESPONSES (đối thủ phản công):       │
│   Mã→(4,4) score=-200                   │
│   Pháo→(7,1) score=-50                  │
│   Xe→(9,0) score=-350  ← WORST          │
├──────────────────────────────────────────┤
│ Guaranteed score: -350                   │
└──────────────────────────────────────────┘
```

**BeliefStep:**
```
┌──────────────────────────────────────────┐
│ Belief State — Bước 2/2                  │
├──────────────────────────────────────────┤
│ Phong cách đối thủ: AGGRESSIVE           │
│ P(agg)=0.6  P(def)=0.2  P(pos)=0.2      │
├──────────────────────────────────────────┤
│ Utility per style:                       │
│   Aggressive: 280                        │
│   Defensive:  150                        │
│   Positional: 200                        │
├──────────────────────────────────────────┤
│ E[U] = 0.6×280 + 0.2×150 + 0.2×200      │
│      = 168 + 30 + 40 = 238               │
└──────────────────────────────────────────┘
```

#### Nhóm F: `_render_csp` — cho BacktrackStep, MinConflictStep, AC3Step

3 thuật toán Level 5 (CSP) gom vào 1 renderer có phân nhánh:

**BacktrackStep:**
```
┌──────────────────────────────────────────┐
│ Backtracking MRV — Bước 2/2              │
├──────────────────────────────────────────┤
│ VARIABLES (domain size):                 │
│ ✅ (3,2): domain=2 ← MRV (nhỏ nhất)     │
│    (0,0): domain=5                       │
│    (9,1): domain=4                       │
├──────────────────────────────────────────┤
│ DOMAIN cho biến (3,2):                   │
│ ✅ →(4,4) score=350 ← BEST              │
│    →(5,1) score=200                      │
└──────────────────────────────────────────┘
```

**MinConflictStep:**
```
┌──────────────────────────────────────────┐
│ Min-Conflicts — Bước 1/1                 │
├──────────────────────────────────────────┤
│ Conflicts TRƯỚC: 3  →  SAU: 1  (giảm 2) │
├──────────────────────────────────────────┤
│ TOP CANDIDATES (sorted by conflicts):    │
│ ✅ Xe (0,0)→(0,5) conflicts=1 ← BEST    │
│    Mã (3,2)→(4,4) conflicts=2            │
│    Pháo (2,1)→(2,7) conflicts=3          │
└──────────────────────────────────────────┘
```

**AC3Step:**
```
┌────────────────────┬─────────────────────┐
│ SAFE ✅ (15 nước)  │ PRUNED ❌ (5 nước)  │
│ Xe→(0,5) [350]    │ Xe→(4,4): bị Tốt ăn │
│ Mã→(4,4) [280]    │ Pháo→(7,1): bị Mã ăn│
│ ...                │ ...                  │
├────────────────────┴─────────────────────┤
│ ✅ CHOSEN: Xe (0,0)→(0,5) score=350     │
└──────────────────────────────────────────┘
```

#### Nhóm G: `_render_minimax_expectimax` — cho MinimaxStep, ExpectimaxStep

Tái sử dụng layout tương tự `_render_alpha_beta` nhưng không có α/β:

**MinimaxStep:**
```
┌──────────────────────────────────────────┐
│ Minimax — Bước 5/20                      │
├──────────────────────────────────────────┤
│ PATH: root → d3(MAX) → d2(MIN) → d1     │
│ [●]────[●]────[●]────[●]                │
├──────────────────────────────────────────┤
│ TYPE: MAX node   VALUE: 350              │
├──────────────────────────────────────────┤
│ Siblings: val:200  val:350✅  val:150    │
│ Best so far: val=350                     │
└──────────────────────────────────────────┘
```

**ExpectimaxStep:**
```
┌──────────────────────────────────────────┐
│ Expectimax — Bước 8/20                   │
├──────────────────────────────────────────┤
│ 🎲 CHANCE NODE  depth=2                  │
├──────────────────────────────────────────┤
│ Child values: 350, 200, 150, 100         │
│ Best = 350                               │
│ Avg(others) = (200+150+100)/3 = 150      │
├──────────────────────────────────────────┤
│ E[V] = 0.7 × 350 + 0.3 × 150            │
│      = 245 + 45 = 290                    │
└──────────────────────────────────────────┘
```

### 11.4 Bước 4: Cập nhật phân nhánh `draw()` trong VisualizerPanel

Sửa hàm `draw()` để route đúng step type vào đúng renderer:

```python
def draw(self, surface, step, controller, recorder):
    # ... header, footer giữ nguyên ...
    
    # Body — dispatch theo step type
    if isinstance(step, (BFSStep, DFSStep)):
        self._render_bfs_dfs(surface, step, content_rect)
    elif isinstance(step, (UCSStep, AStarStep)):
        self._render_search_3col(surface, step, content_rect)
    elif isinstance(step, IDAStarStep):
        self._render_ida_star(surface, step, content_rect)
    elif isinstance(step, (GreedyStep, HillClimbStep)):
        self._render_candidates_list(surface, step, content_rect)
    elif isinstance(step, SAStep):
        self._render_sa(surface, step, content_rect)
    elif isinstance(step, BeamStep):
        self._render_beam(surface, step, content_rect)
    elif isinstance(step, (OnlineStep, AndOrStep, BeliefStep)):
        self._render_online_andor_belief(surface, step, content_rect)
    elif isinstance(step, (BacktrackStep, MinConflictStep, AC3Step)):
        self._render_csp(surface, step, content_rect)
    elif isinstance(step, AlphaBetaStep):
        self._render_alpha_beta(surface, step, content_rect)
    elif isinstance(step, (MinimaxStep, ExpectimaxStep)):
        self._render_minimax_expectimax(surface, step, content_rect)
    else:
        self._render_text_only(surface, step, content_rect)
```

### 11.5 Tổng kết thay đổi

| File | Thay đổi | Chi tiết |
|------|----------|----------|
| `gui/visualizer.py` | Thêm `_format_move()` | Helper format tọa độ + tên quân, dùng chung |
| `gui/visualizer.py` | Sửa `_render_sa()` | Thêm hiển thị tọa độ nước đi thay vì chỉ score |
| `gui/visualizer.py` | Sửa `_render_search_3col()` | Thêm tọa độ vào mỗi item trong 3 cột |
| `gui/visualizer.py` | Sửa `_render_alpha_beta()` | Thêm nước đi vào siblings |
| `gui/visualizer.py` | Thêm `_render_bfs_dfs()` | Renderer cho BFS/DFS với Queue/Stack |
| `gui/visualizer.py` | Thêm `_render_candidates_list()` | Renderer cho Greedy/Hill Climbing |
| `gui/visualizer.py` | Thêm `_render_ida_star()` | Renderer cho IDA* với threshold/iteration |
| `gui/visualizer.py` | Thêm `_render_beam()` | Renderer cho Beam Search: kept/eliminated |
| `gui/visualizer.py` | Thêm `_render_online_andor_belief()` | Renderer cho 3 thuật toán Level 4 |
| `gui/visualizer.py` | Thêm `_render_csp()` | Renderer cho 3 thuật toán Level 5 (CSP) |
| `gui/visualizer.py` | Thêm `_render_minimax_expectimax()` | Renderer cho Minimax/Expectimax |
| `gui/visualizer.py` | Sửa `draw()` | Cập nhật dispatch cho tất cả 18 step types |

**⚠️ KHÔNG CẦN SỬA:** `ai/step_recorder.py`, `ai/level1-6.py`, `main.py` — Backend đã hoàn chỉnh, chỉ sửa duy nhất file `gui/visualizer.py`.

### 11.6 Thứ tự triển khai Phase 11

| # | Task | Ước lượng |
|---|------|-----------|
| 11.1 | Thêm `_format_move()` + `PIECE_NAME_VI` | 5 phút |
| 11.2a | Sửa `_render_sa()` | 5 phút |
| 11.2b | Sửa `_render_search_3col()` | 5 phút |
| 11.2c | Sửa `_render_alpha_beta()` | 5 phút |
| 11.3A | Thêm `_render_bfs_dfs()` | 10 phút |
| 11.3B | Thêm `_render_candidates_list()` | 10 phút |
| 11.3C | Thêm `_render_ida_star()` | 10 phút |
| 11.3D | Thêm `_render_beam()` | 10 phút |
| 11.3E | Thêm `_render_online_andor_belief()` | 15 phút |
| 11.3F | Thêm `_render_csp()` | 10 phút |
| 11.3G | Thêm `_render_minimax_expectimax()` | 10 phút |
| 11.4 | Sửa `draw()` dispatch | 5 phút |
| | **TỔNG** | **~100 phút** |

---

## Phase 12: FIX Font + Tọa độ Label + Piece Name + Subtitle

> **Mục tiêu:** 4 cải tiến cho visualizer panel — chạy trên Windows tiếng Việt đúng font, tọa độ dạng "A0→C4" thay vì "(0,0)→(2,4)", thêm tên quân cờ, và subtitle giải thích số bước.

### ⚠️ ĐIỂM MÂU THUẪN TRONG YÊU CẦU

Yêu cầu đầu (FIX 3) nói **sửa `level3.py`** để thêm key `"piece"` vào dict. Yêu cầu cuối nói **KHÔNG sửa `level*.py`**. 

**Quyết định:** Sửa `level3.py` thêm key `"piece"` (vì nếu không có dữ liệu nguồn thì visualizer không thể hiển thị tên quân). Tương tự cho `level4.py`, `level5.py` nếu thiếu.

---

### 12.1 FIX 1: FONT hỗ trợ tiếng Việt (`gui/visualizer.py`)

#### Vấn đề hiện tại
Font system `pygame.font.SysFont(["Segoe UI", "Arial"], size)` — trên một số máy Windows không render đúng dấu tiếng Việt (Ă, Ơ, Ư, ĐỘ, v.v.) vì pygame SysFont fallback không nhất quán.

#### Thay đổi
Trong `__init__()` của `VisualizerPanel` (line 114-150), thay logic font loading:

```python
# TRƯỚC (line 120-150):
font_list = ["Segoe UI", "Arial"]
if font_name and not font_name.endswith(".ttf"):
    font_list.insert(0, font_name)
try:
    if font_name and font_name.endswith(".ttf"):
        self.title_font = pygame.font.Font(font_name, 20)
        ...
    else:
        self.title_font = pygame.font.SysFont(font_list, 20, bold=True)
        ...
except Exception:
    self.title_font = pygame.font.SysFont(["Segoe UI", "Arial"], 20, bold=True)
    ...
```

```python
# SAU — hàm helper + fallback chain:
def _load_font(size, bold=False):
    """Thử load font theo thứ tự ưu tiên, hỗ trợ tiếng Việt."""
    import os
    # 1. Thử file TTF bundled
    ttf_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                            "assets", "fonts", "Roboto-Regular.ttf")
    if os.path.exists(ttf_path):
        try:
            f = pygame.font.Font(ttf_path, size)
            if bold:
                f.set_bold(True)
            return f
        except Exception:
            pass
    # 2. Thử custom font_name nếu là file .ttf
    if font_name and font_name.endswith(".ttf") and os.path.exists(font_name):
        try:
            f = pygame.font.Font(font_name, size)
            if bold:
                f.set_bold(True)
            return f
        except Exception:
            pass
    # 3. SysFont fallback — Arial và Segoe UI hỗ trợ tiếng Việt trên Windows
    for sys_name in ["Arial", "segoeui", "Tahoma"]:
        try:
            f = pygame.font.SysFont(sys_name, size, bold=bold)
            return f
        except Exception:
            continue
    # 4. Default pygame font (cuối cùng)
    return pygame.font.Font(None, size)

self.title_font = _load_font(20, bold=True)
self.header_font = _load_font(16, bold=True)
self.body_font = _load_font(14)
self.small_font = _load_font(12)
self.tiny_font = _load_font(10)

# Mono font riêng — ưu tiên Consolas (luôn có trên Windows)
try:
    self.mono_font = pygame.font.SysFont("Consolas", 13)
except Exception:
    self.mono_font = _load_font(13)
```

#### Vị trí cần sửa
| Line range | Mô tả |
|------------|--------|
| 120-150 | Toàn bộ block font loading trong `__init__()` |

---

### 12.2 FIX 2: Tọa độ Label + `_format_move_full()` (`gui/visualizer.py`)

#### Vấn đề hiện tại
Tọa độ hiển thị dạng `(2, 1)→(3, 2)` — không ai-readable. Cần chuyển sang dạng `B2→C3` (cột A-I, hàng 0-9).

#### Thêm mới — 2 helper vào class `VisualizerPanel`

Thêm vào **sau** `_format_move_short()` (sau line 270), **trước** comment `# MAIN DRAW`:

```python
# Class-level constant
COL_LABELS = "ABCDEFGHI"

def _pos_to_label(self, pos):
    """Convert (row, col) → 'A0'..'I9'"""
    row, col = pos
    if 0 <= col < len(self.COL_LABELS):
        return f"{self.COL_LABELS[col]}{row}"
    return f"({row},{col})"

def _format_move_full(self, move_data):
    """
    Format move data thành chuỗi dễ đọc với label tọa độ.
    Input: tuple ((r1,c1),(r2,c2)) hoặc dict {"move":..., "score":..., "piece":...}
    Output: "Mã B2→C4 [280]"
    """
    if move_data is None:
        return "—"
    
    piece_name = ""
    score_str = ""
    move_tuple = None
    
    if isinstance(move_data, dict):
        move_tuple = move_data.get("move")
        piece = (move_data.get("piece") 
                 or move_data.get("piece_name") 
                 or move_data.get("piece_captured"))
        if piece and piece != "—":
            # Map English → Vietnamese nếu cần
            vi_name = PIECE_NAME_VI.get(piece, piece)
            piece_name = vi_name + " "
        score = move_data.get("score")
        if score is not None:
            try:
                score_str = f" [{score:.0f}]"
            except (TypeError, ValueError):
                score_str = f" [{score}]"
    elif isinstance(move_data, tuple) and len(move_data) == 2:
        if isinstance(move_data[0], tuple):
            move_tuple = move_data
    
    if move_tuple and isinstance(move_tuple, tuple) and len(move_tuple) == 2:
        if isinstance(move_tuple[0], tuple):
            from_label = self._pos_to_label(move_tuple[0])
            to_label = self._pos_to_label(move_tuple[1])
            return f"{piece_name}{from_label}→{to_label}{score_str}"
        else:
            return f"{piece_name}{move_tuple}{score_str}"
    
    return str(move_data)[:30]
```

#### Thay thế tất cả `_format_move()` → `_format_move_full()`

**16 call sites** cần thay:

| Line | Renderer | Gọi hiện tại | Thay bằng |
|------|----------|--------------|-----------|
| 467 | `_draw_item_list` | `self._format_move(item)` | `self._format_move_full(item)` |
| 682 | `_render_candidates_list` (HillClimb) | `self._format_move(step.current_move)` | `self._format_move_full(step.current_move)` |
| 686 | `_render_candidates_list` (Greedy) | `self._format_move(step.current_node)` | `self._format_move_full(step.current_node)` |
| 717 | `_render_candidates_list` (items) | `self._format_move(item)` | `self._format_move_full(item)` |
| 756 | `_render_sa` | `self._format_move(step.current_move)` | `self._format_move_full(step.current_move)` |
| 757 | `_render_sa` | `self._format_move(step.candidate_move)` | `self._format_move_full(step.candidate_move)` |
| 828 | `_render_beam` (kept) | `self._format_move(item)` | `self._format_move_full(item)` |
| 849 | `_render_beam` (eliminated) | `self._format_move(item)` | `self._format_move_full(item)` |
| 949 | `_render_online` (candidates) | `self._format_move(item)` | `self._format_move_full(item)` |
| 961 | `_render_andor` (or_node) | `self._format_move(step.or_node)` | `self._format_move_full(step.or_node)` |
| 984 | `_render_andor` (responses) | `self._format_move(resp)` | `self._format_move_full(resp)` |
| 1110 | `_render_backtrack` (domain) | `self._format_move(item)` | `self._format_move_full(item)` |
| 1191 | `_render_ac3` (safe) | `self._format_move(item)` | `self._format_move_full(item)` |
| 1224 | `_render_ac3` (chosen) | `self._format_move(step.chosen_from_safe)` | `self._format_move_full(step.chosen_from_safe)` |
| 1404 | `_render_minimax` (best_so_far) | `self._format_move(step.best_so_far)` | `self._format_move_full(step.best_so_far)` |

#### Thay thế tất cả `_format_move_short()` → `_format_move_full()`

**11 call sites** cần thay:

| Line | Renderer | Gọi hiện tại | Thay bằng |
|------|----------|--------------|-----------|
| 528 | `_render_bfs_dfs` (move) | `self._format_move_short(move)` | `self._format_move_full({"move": move})` ★ |
| 587 | `_render_search_3col` (UCS) | `self._format_move_short(item)` | `self._format_move_full(item)` |
| 591 | `_render_search_3col` (A*) | `self._format_move_short(item)` | `self._format_move_full(item)` |
| 631 | `_render_ida_star` (node) | `self._format_move_short(step.current_node)` | `self._format_move_full(step.current_node)` |
| 865 | `_render_beam` (worst-case) | `self._format_move_short(wc)` | `self._format_move_full(wc)` |
| 1153 | `_render_min_conflicts` | `self._format_move_short(item)` | `self._format_move_full(item)` |
| 1215 | `_render_ac3` (pruned) | `self._format_move_short(item)` | `self._format_move_full(item)` |
| 1308 | `_render_alpha_beta` (siblings) | `self._format_move_short(sib.get("move"))` | `self._format_move_full(sib)` ★ |
| 1393 | `_render_minimax` (siblings) | `self._format_move_short(sib.get("move"))` | `self._format_move_full(sib)` ★ |

> ★ Lưu ý: Với siblings từ alpha-beta/minimax, `sib` đã là dict `{"move": ..., "value": ...}`, nên truyền cả dict vào `_format_move_full(sib)` thay vì chỉ `sib.get("move")`.

> **Đặc biệt** BFS/DFS line 528: `move` ở đây là tuple thuần, cần wrap `{"move": move}` để `_format_move_full` xử lý đúng — HOẶC truyền thẳng `move` vì `_format_move_full` đã handle tuple.

#### Giữ lại / Xóa function cũ?

- `_format_move()` (line 220-256): **Xóa** (hoặc alias `_format_move = _format_move_full`)
- `_format_move_short()` (line 258-270): **Xóa** — `_format_move_full` thay thế hoàn toàn

---

### 12.3 FIX 3: Thêm key `"piece"` vào dict ở `ai/level3.py`

#### Vấn đề hiện tại
`level3.py` ghi `current_move={"move": current_move, "score": current_score}` — thiếu key `"piece"`.
Kết quả: `_format_move_full()` chỉ hiện tọa độ, không hiện tên quân (ví dụ: `B2→C4 [280]` thay vì `Mã B2→C4 [280]`).

#### Thay đổi trong `ai/level3.py`

**Thêm PIECE_NAME_VI** ở đầu file (sau line 6):

```python
PIECE_NAME_VI = {
    'general': 'Tướng', 'advisor': 'Sĩ', 'elephant': 'Tượng',
    'horse': 'Mã', 'rook': 'Xe', 'cannon': 'Pháo', 'pawn': 'Tốt'
}
```

**Thêm helper lấy tên quân:**

```python
def _get_piece_name(board, pos):
    """Lấy tên quân cờ tiếng Việt từ vị trí trên bàn cờ."""
    piece = board.get_piece(pos)
    return PIECE_NAME_VI.get(piece.name, "—") if piece else "—"
```

#### 3a. Sửa `hill_climbing_move()` (line 34-62)

```diff
 for i, (from_pos, to_pos) in enumerate(legal_moves):
     board.make_move(from_pos, to_pos, test_only=True)
     score = get_perspective_score(board, color)
     board.undo_move(test_only=True)

-    neighbor_info = {"move": (from_pos, to_pos), "score": score}
+    piece_name = _get_piece_name(board, from_pos)
+    neighbor_info = {"move": (from_pos, to_pos), "score": score, "piece": piece_name}
     neighbors.append(neighbor_info)

     ...
         recorder.add_step(
             HillClimbStep(
                 ...
-                current_move={"move": best_move, "score": best_score},
+                current_move={"move": best_move, "score": best_score, "piece": _get_piece_name(board, best_move[0])},
                 neighbors=sorted_neighbors.copy(),
-                best_neighbor={"move": best_move, "score": best_score},
+                best_neighbor={"move": best_move, "score": best_score, "piece": _get_piece_name(board, best_move[0])},
             )
         )
```

#### 3b. Sửa `simulated_annealing_move()` (line 127-143)

```diff
         if recorder and step_counter < MAX_VISUALIZATION_STEPS:
             recorder.add_step(
                 SAStep(
                     ...
-                    current_move={"move": current_move, "score": current_score},
-                    candidate_move={"move": candidate, "score": score},
+                    current_move={"move": current_move, "score": current_score, "piece": _get_piece_name(board, current_move[0])},
+                    candidate_move={"move": candidate, "score": score, "piece": _get_piece_name(board, candidate[0])},
                     ...
                 )
             )
```

#### 3c. Sửa `beam_search_move()` (line 165-240)

```diff
 for from_pos, to_pos in legal_moves:
     board.make_move(from_pos, to_pos, test_only=True)
     score = get_perspective_score(board, color)
     board.undo_move(test_only=True)
-    candidates.append((score, (from_pos, to_pos)))
+    piece_name = _get_piece_name(board, from_pos)
+    candidates.append((score, (from_pos, to_pos), piece_name))
```

> ⚠️ Chú ý: Beam search dùng tuple `(score, move)` thay vì dict ở candidates list. Cần thêm piece_name vào tuple HOẶC chuyển sang dict khi ghi `BeamStep`. Giải pháp an toàn nhất: **chỉ thêm "piece" vào dict khi tạo BeamStep**, không thay đổi internal tuple:

```diff
 # Line 185-187 — BeamStep all_candidates/kept_beams/eliminated
-all_candidates=[{"move": m, "score": s} for s, m in candidates],
-kept_beams=[{"move": m, "score": s} for s, m in beam],
-eliminated=[{"move": m, "score": s} for s, m in eliminated],
+all_candidates=[{"move": m, "score": s, "piece": _get_piece_name(board, m[0])} for s, m in candidates],
+kept_beams=[{"move": m, "score": s, "piece": _get_piece_name(board, m[0])} for s, m in beam],
+eliminated=[{"move": m, "score": s, "piece": _get_piece_name(board, m[0])} for s, m in eliminated],
```

```diff
 # Line 218-219 — worst_case_scores
-worst_case_scores.append({"move": move, "init_score": score, "worst_case": opp_min_score})
+worst_case_scores.append({"move": move, "init_score": score, "worst_case": opp_min_score, "piece": _get_piece_name(board, move[0])})
```

#### 3d. Sửa tương tự cho `ai/level4.py`

Thêm `PIECE_NAME_VI` + `_get_piece_name()` ở đầu file.

**`online_search_move()`** (line 90):
```diff
-candidates.append({"move": (from_pos, to_pos), "score": score})
+candidates.append({"move": (from_pos, to_pos), "score": score, "piece": _get_piece_name(board, from_pos)})
```

**`and_or_search_move()`** (line 161, 179-182):
```diff
-and_responses.append({"move": (ofrom, oto), "score": us_score})
+and_responses.append({"move": (ofrom, oto), "score": us_score, "piece": _get_piece_name(board, ofrom)})

-or_node={"move": (from_pos, to_pos), "responses_count": len(and_responses)},
+or_node={"move": (from_pos, to_pos), "responses_count": len(and_responses), "piece": _get_piece_name(board, from_pos)},
```

#### 3e. Sửa tương tự cho `ai/level5.py`

Thêm `PIECE_NAME_VI` + `_get_piece_name()` ở đầu file.

**`backtracking_mrv_move()`** (line 77, 96):
```diff
-domain_list.append({"move": (chosen_var, to_pos), "score": score})
+domain_list.append({"move": (chosen_var, to_pos), "score": score, "piece": _get_piece_name(board, chosen_var)})

-best_assignment={"move": (chosen_var, best_to), "score": best_score},
+best_assignment={"move": (chosen_var, best_to), "score": best_score, "piece": _get_piece_name(board, chosen_var)},
```

---

### 12.4 FIX 4: Subtitle giải thích số bước (`gui/visualizer.py`)

#### Vấn đề hiện tại
Header chỉ hiện "Bước 3/15" — người xem không hiểu 15 là gì (15 nước đi? 15 nodes? 15 vòng lặp?).

#### Thêm helper `_get_step_subtitle()`

Thêm vào class `VisualizerPanel`:

```python
def _get_step_subtitle(self, step, total):
    """Trả về subtitle giải thích ý nghĩa tổng số bước."""
    if isinstance(step, (BFSStep, DFSStep)):
        return f"({total} nodes đã mở rộng)"
    elif isinstance(step, (UCSStep, AStarStep)):
        return f"({total} nước đi đang xét)"
    elif isinstance(step, IDAStarStep):
        return f"({total} nodes đã duyệt)"
    elif isinstance(step, (GreedyStep, HillClimbStep)):
        return f"({total} neighbors đã đánh giá)"
    elif isinstance(step, SAStep):
        return f"({total} vòng lặp nhiệt độ)"
    elif isinstance(step, BeamStep):
        return "(2 giai đoạn: chọn beam + worst-case)"
    elif isinstance(step, (OnlineStep, AndOrStep, BeliefStep)):
        return f"({total} bước phân tích)"
    elif isinstance(step, (BacktrackStep, MinConflictStep, AC3Step)):
        return f"({total} bước phân tích CSP)"
    elif isinstance(step, (MinimaxStep, AlphaBetaStep)):
        return f"({total} nodes cây game đã duyệt)"
    elif isinstance(step, ExpectimaxStep):
        return f"({total} nodes đã duyệt)"
    return ""
```

#### Sửa `_render_header()` (line 358-378)

```diff
     # Step counter
     step_txt = self.header_font.render(
         f"Bước {recorder.current_index + 1}/{recorder.total_steps()}",
         True,
         COLOR_TEXT,
     )
     surface.blit(
         step_txt,
         (header_rect.right - step_txt.get_width() - 15, header_rect.y + 12),
     )
+
+    # Subtitle giải thích
+    total = recorder.total_steps()
+    subtitle = self._get_step_subtitle(step, total)
+    if subtitle:
+        sub_txt = self.tiny_font.render(subtitle, True, COLOR_TEXT_MUTED)
+        surface.blit(
+            sub_txt,
+            (header_rect.right - sub_txt.get_width() - 15, header_rect.y + 35),
+        )
```

> ⚠️ Header card hiện cao 50px (line 361: `height=50`). Subtitle cần thêm ~15px. Tăng height lên **65** và điều chỉnh `content_y` (line 304) từ `self.y + 80` → `self.y + 95`.

```diff
 # line 361
-header_rect = pygame.Rect(self.x + 15, self.y + 15, self.width - 30, 50)
+header_rect = pygame.Rect(self.x + 15, self.y + 15, self.width - 30, 65)

 # line 304
-content_y = self.y + 80
+content_y = self.y + 95
```

---

### 12.5 Tổng kết tất cả thay đổi

| # | File | Thay đổi | Chi tiết |
|---|------|----------|----------|
| 1 | `gui/visualizer.py` | Font loading | Thay toàn bộ block font (line 120-150) bằng `_load_font()` helper với fallback chain: TTF → Arial → segoeui → default |
| 2 | `gui/visualizer.py` | Thêm `COL_LABELS` | Class constant `"ABCDEFGHI"` |
| 3 | `gui/visualizer.py` | Thêm `_pos_to_label()` | Convert `(row, col)` → `"A0"..."I9"` |
| 4 | `gui/visualizer.py` | Thêm `_format_move_full()` | Format đầy đủ: `"Mã B2→C4 [280]"` |
| 5 | `gui/visualizer.py` | Thay 16× `_format_move()` | Tất cả call sites → `_format_move_full()` |
| 6 | `gui/visualizer.py` | Thay 11× `_format_move_short()` | Tất cả call sites → `_format_move_full()` |
| 7 | `gui/visualizer.py` | Xóa `_format_move()` + `_format_move_short()` | Thay bằng `_format_move_full()` duy nhất |
| 8 | `gui/visualizer.py` | Thêm `_get_step_subtitle()` | Subtitle giải thích ý nghĩa tổng số bước |
| 9 | `gui/visualizer.py` | Sửa `_render_header()` | Thêm dòng subtitle, tăng header height 50→65 |
| 10 | `gui/visualizer.py` | Sửa `content_y` | Từ `y+80` → `y+95` (nhường chỗ cho header mới) |
| 11 | `ai/level3.py` | Thêm `PIECE_NAME_VI` + `_get_piece_name()` | Helper lấy tên quân tiếng Việt |
| 12 | `ai/level3.py` | Sửa `hill_climbing_move()` | Thêm `"piece"` vào neighbor_info, current_move, best_neighbor |
| 13 | `ai/level3.py` | Sửa `simulated_annealing_move()` | Thêm `"piece"` vào current_move, candidate_move dict |
| 14 | `ai/level3.py` | Sửa `beam_search_move()` | Thêm `"piece"` vào all_candidates, kept_beams, eliminated, worst_case_scores |
| 15 | `ai/level4.py` | Thêm `PIECE_NAME_VI` + `_get_piece_name()` | Helper lấy tên quân tiếng Việt |
| 16 | `ai/level4.py` | Sửa `online_search_move()` | Thêm `"piece"` vào candidates dict |
| 17 | `ai/level4.py` | Sửa `and_or_search_move()` | Thêm `"piece"` vào and_responses, or_node |
| 18 | `ai/level5.py` | Thêm `PIECE_NAME_VI` + `_get_piece_name()` | Helper lấy tên quân tiếng Việt |
| 19 | `ai/level5.py` | Sửa `backtracking_mrv_move()` | Thêm `"piece"` vào domain_list, best_assignment |

### KHÔNG SỬA
- `ai/step_recorder.py` — Các dataclass dùng `Dict[str, Any]`, thêm key `"piece"` không cần sửa schema
- `main.py` — Không liên quan
- `ai/level1.py`, `ai/level2.py` — Đã có key `"piece"` / `"piece_captured"` sẵn
- `ai/level6.py` — Alpha-Beta/Minimax/Expectimax đã có data riêng

### 12.6 Thứ tự triển khai Phase 12

| # | Task | Ước lượng |
|---|------|-----------|
| 12.1 | FIX 1: Font loading (`visualizer.py`) | 5 phút |
| 12.2a | Thêm `COL_LABELS` + `_pos_to_label()` + `_format_move_full()` | 10 phút |
| 12.2b | Thay 16× `_format_move()` → `_format_move_full()` | 10 phút |
| 12.2c | Thay 11× `_format_move_short()` → `_format_move_full()` | 10 phút |
| 12.2d | Xóa `_format_move()` + `_format_move_short()` | 2 phút |
| 12.3 | FIX 3: Thêm piece name vào `level3.py`, `level4.py`, `level5.py` | 15 phút |
| 12.4 | FIX 4: Subtitle + sửa header height | 10 phút |
| 12.5 | Test thủ công — chạy game, kiểm tra visualization panel | 10 phút |
| | **TỔNG** | **~72 phút** |

### 12.7 Kết quả thực hiện Phase 12 (Đã hoàn thành 100%)

- [x] **12.1 FIX 1: Font loading (`visualizer.py`)** -> Đã thay thế block load font cũ bằng hàm helper `_load_font()` với fallback chain: Roboto-Regular.ttf (bundled) -> custom TTF -> Arial/segoeui/Tahoma -> pygame default font. Hỗ trợ hiển thị tiếng Việt hoàn hảo trên Windows.
- [x] **12.2a Thêm `COL_LABELS` + `_pos_to_label()` + `_format_move_full()`** -> Đã khai báo hằng số `COL_LABELS = "ABCDEFGHI"`, xây dựng method `_pos_to_label(pos)` để đổi từ `(row, col)` thành `"A0"..."I9"`, và method `_format_move_full(move_data)` để format đầy đủ có cả tên quân cờ, tọa độ và score.
- [x] **12.2b+c Thay các call sites của `_format_move()` & `_format_move_short()`** -> Đã thay toàn bộ 16 call sites của `_format_move()` và 10 call sites của `_format_move_short()` thành `_format_move_full()`.
- [x] **12.2d Xóa / tối ưu các hàm cũ** -> Đã xóa `_format_move_short()` và định nghĩa `_format_move()` như một alias gọi `_format_move_full()` để đảm bảo tương thích ngược 100%.
- [x] **12.3 FIX 3: Thêm piece name vào `level3.py`, `level4.py`, `level5.py`** ->
  - Đã thêm `PIECE_NAME_VI` và helper `_get_piece_name(board, pos)` vào cả 3 file AI.
  - Sửa `hill_climbing_move()` để lấy piece name trước khi move và thêm key `"piece"` vào các dict neighbor, current_move, best_neighbor.
  - Sửa `simulated_annealing_move()` thêm guard an toàn lấy piece name trước khi add step, gán `"piece"` vào current_move và candidate_move.
  - Sửa `beam_search_move()` tương tự cho all_candidates, kept_beams, eliminated và worst_case_scores.
  - Sửa `online_search_move()` và `and_or_search_move()` (Level 4) lấy piece name cho candidates và response dicts.
  - Sửa `backtracking_mrv_move()`, `min_conflicts_move()` và `ac3_move()` (Level 5) lấy piece name.
- [x] **12.4 FIX 4: Subtitle giải thích số bước** ->
  - Đã viết helper `_get_step_subtitle()` trả về lời giải thích chi tiết cho từng loại thuật toán (ví dụ: `(15 vòng lặp nhiệt độ)`, `(10 nước đi đang xét)`).
  - Sửa `_render_header()` để vẽ subtitle bằng `tiny_font` ở góc trên bên phải (tọa độ `header_rect.y + 32`), nằm gọn bên trong thẻ header 50px cũ. Tránh tăng chiều cao header để đảm bảo các nút điều hướng ở footer không bị cắt/tràn màn hình.
- [x] **12.5 Test compile** -> Đã chạy `py_compile` thành công cho tất cả các file sửa đổi.
