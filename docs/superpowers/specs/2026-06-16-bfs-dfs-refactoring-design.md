# Spec: BFS & DFS Search Refactoring

**Date**: 2026-06-16  
**Status**: Approved  
**Author**: Antigravity  

## 1. Goal Description

Currently, the BFS and DFS algorithms in `ai/level1.py` are oversimplified: BFS selects the first legal move, and DFS selects the last legal move. With a search depth of only 1, the FIFO queue and LIFO stack structures serve no purpose. The goal of this change is to implement real depth-limited BFS and DFS searches (default depth of 2 plies) that traverse the game tree and select the optimal move by propagating board evaluation scores up from the leaf nodes using minimax logic.

## 2. Proposed Changes

### Public API
* Update the Level 1 search signatures to accept an optional depth while preserving existing callers:
  * `def bfs_move(board, depth=2)`
  * `def dfs_move(board, depth=2)`
* `evaluate_board(board)` returns a Red-positive score. Red should maximize this score; Black should minimize it.
* Both functions should return `None` when the side to move has no legal moves.

### BFS (Breadth-First Search) Implementation
* **Data Structure**: Use `collections.deque` to perform a level-order traversal.
* **Node Tracking**: Store enough metadata to propagate scores after traversal:
  * `id`: stable node identifier.
  * `parent_id`: parent node identifier, or `None` for synthetic/root nodes.
  * `root_move`: the first move made from the original board.
  * `move`: the move that produced this node.
  * `board`: the board state after applying `move`.
  * `depth`: ply depth from the original board.
  * `children`: list of child node ids.
  * `score`: leaf evaluation or propagated minimax value.
* **Algorithm**:
  1. Read `ai_color = board.turn` and get all root legal moves.
  2. For each root move, create `board.copy()`, apply the move with `make_move`, create a depth-1 node, and enqueue that node.
  3. Perform level-order expansion: dequeue a node, generate moves for `node.board.turn`, apply each move on a copied board, create child nodes, and enqueue them until `node.depth == depth`.
  4. Treat a node as a leaf when it reaches `depth` or when the side to move has no legal moves. Set `node.score = evaluate_board(node.board)` for normal leaves.
  5. Propagate scores from deepest nodes back to depth 1:
     * If a parent node has no children, keep its leaf score.
     * If `parent.board.turn == 'red'`, set `parent.score = max(child.score for child in parent.children)`.
     * If `parent.board.turn == 'black'`, set `parent.score = min(child.score for child in parent.children)`.
  6. Select among depth-1 root nodes:
     * Red AI returns the `root_move` with the highest propagated score.
     * Black AI returns the `root_move` with the lowest propagated score.
* **Tradeoff**: BFS needs multiple board states alive at once, so using `board.copy()` is acceptable for the default depth of 2 but can become memory-heavy at larger depths. Keep the default small, and consider a branching limit or a different search strategy before increasing it.

### DFS (Depth-First Search) Implementation
* **Data Structure**: Use standard recursive call stack to traverse depth-first.
* **State Management**: Prefer `board.make_move(...)` and `board.undo_move()` inside recursion instead of copying boards at each node. This follows the existing `ai/level6.py` minimax pattern and avoids unnecessary allocation.
* **Algorithm**:
  1. Read `ai_color = board.turn` and get all root legal moves.
  2. For each root move, call `board.make_move(from_pos, to_pos)`, then evaluate the resulting position with `dfs_search(board, depth - 1)`, and finally call `board.undo_move()`.
  3. `dfs_search(board, remaining_depth)`:
     * Return `evaluate_board(board)` when `remaining_depth == 0`.
     * Generate legal moves for `board.turn`.
     * Return `evaluate_board(board)` if there are no legal moves.
     * If `board.turn == 'red'`, recursively evaluate every child and return the maximum score.
     * If `board.turn == 'black'`, recursively evaluate every child and return the minimum score.
  4. Select among root moves:
     * Red AI returns the move with the highest minimax score.
     * Black AI returns the move with the lowest minimax score.

### Terminal States
* For this Level 1 refactor, terminal no-move positions may use `evaluate_board(board)` to keep behavior simple and consistent with a shallow learner.
* A future improvement can assign checkmate-specific sentinel values, but that is out of scope for this change.

## 3. Verification Plan

### Automated Tests
* We will create a new test suite `tests/test_ai_level1.py` with unit tests for:
  1. `bfs_move` chooses the safe move in a depth-2 trap position where a tempting high-value capture can be recaptured by the opponent.
  2. `dfs_move` chooses the safe move in the same depth-2 trap position.
  3. `bfs_move` chooses the minimizing move for Black when `board.turn = 'black'`.
  4. `dfs_move` chooses the minimizing move for Black when `board.turn = 'black'`.
  5. The default depth is 2 for both `bfs_move` and `dfs_move`, either by checking the function signatures or by using a trap position that only resolves correctly at depth 2.
* Update `run_evals.py` so the `ai-level-behavior` capability also runs `tests/test_ai_level1.py`.
* Run `venv\Scripts\python -m unittest tests/test_ai_level1.py`.
* Run `venv\Scripts\python run_evals.py` to ensure no regressions are introduced.

### Manual Verification
* Run bot vs. bot simulations in the UI using BFS or DFS bots to verify they move intelligently and don't crash.
