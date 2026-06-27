# AI Package Initialization
from ai.level1 import bfs_move, dfs_move, ucs_move
from ai.level2 import a_star_move, greedy_move, ida_star_move
from ai.level3 import beam_search_move, hill_climbing_move, simulated_annealing_move
from ai.level4 import and_or_search_move, belief_state_search_move, online_search_move
from ai.level5 import ac3_move, backtracking_mrv_move, min_conflicts_move
from ai.level6 import alpha_beta_move, expectimax_move, minimax_move

AI_REGISTRY = {
    "BFS": bfs_move,
    "DFS": dfs_move,
    "UCS": ucs_move,
    "Greedy": greedy_move,
    "A*": a_star_move,
    "IDA*": ida_star_move,
    "Hill Climbing": hill_climbing_move,
    "Simulated Annealing": simulated_annealing_move,
    "Beam Search": beam_search_move,
    "Online Search": online_search_move,
    "AND-OR Search": and_or_search_move,
    "Belief State": belief_state_search_move,
    "Backtracking": backtracking_mrv_move,
    "Min-Conflicts": min_conflicts_move,
    "AC-3": ac3_move,
    "Minimax": minimax_move,
    "Alpha-Beta": alpha_beta_move,
    "Expectimax": expectimax_move,
}
