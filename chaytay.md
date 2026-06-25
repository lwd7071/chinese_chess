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

**Progress: 10/10 tasks completed (100%)** 🎯  
**Time spent: ~4 hours** ⏱️  
**Time remaining: 0 hours (Hoàn tất)** 📅

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

### 🎉 MILESTONE: 18/18 thuật toán đã tích hợp recorder! (2026-06-25)

## 10. Gợi ý demo với cô giáo

1. **Chạy UCS Bot vs Bot trước** — vì UCS có cost rõ ràng nhất (`cost = 1000 - PIECE_VALUE`), dễ giải thích từng bước nhất. Bảng Frontier sắp xếp tăng dần, rất trực quan.

2. **Chạy Alpha-Beta tiếp** — demo cây Minimax với α/β thay đổi, highlight nhánh bị cắt tỉa bằng màu đỏ. Rất ấn tượng khi báo cáo.

3. **Chạy SA cuối** — demo công thức `P = e^(ΔE/T)` với nhiệt độ giảm dần, rất hay khi giải thích tại sao SA chấp nhận nước đi tệ hơn ở đầu rồi dần "cứng" lại.
