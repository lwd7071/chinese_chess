# AI Package Initialization
from ai.level1 import bfs_move, dfs_move, ucs_move
from ai.level2 import greedy_move, a_star_move, ida_star_move
from ai.level3 import hill_climbing_move, simulated_annealing_move, beam_search_move
from ai.level4 import online_search_move, and_or_search_move, belief_state_search_move
from ai.level5 import backtracking_mrv_move, min_conflicts_move, ac3_move
from ai.level6 import minimax_move, alpha_beta_move, expectimax_move

AI_REGISTRY = {
    # Level 1
    "Level 1: BFS Bot": bfs_move,
    "Level 1: DFS Bot": dfs_move,
    "Level 1: UCS Bot": ucs_move,
    "Level 1: BFS/DFS/UCS": ucs_move,
    
    # Level 2
    "Level 2: Greedy Bot": greedy_move,
    "Level 2: A* Bot": a_star_move,
    "Level 2: IDA* Bot": ida_star_move,
    "Level 2: Greedy/A*/IDA*": ida_star_move,
    
    # Level 3
    "Level 3: Hill Climbing Bot": hill_climbing_move,
    "Level 3: Simulated Annealing Bot": simulated_annealing_move,
    "Level 3: Beam Search Bot": beam_search_move,
    "Level 3: Hill Climbing/SA/Beam": beam_search_move,
    
    # Level 4
    "Level 4: Online Search Bot": online_search_move,
    "Level 4: AND-OR Bot": and_or_search_move,
    "Level 4: Belief State Bot": belief_state_search_move,
    "Level 4: Online/AND-OR/Belief": and_or_search_move,
    
    # Level 5
    "Level 5: Backtracking CSP Bot": backtracking_mrv_move,
    "Level 5: Min-Conflicts Bot": min_conflicts_move,
    "Level 5: AC-3 Bot": ac3_move,
    "Level 5: CSP (MRV/Min-Conflicts)": min_conflicts_move,
    
    # Level 6
    "Level 6: Minimax Bot": minimax_move,
    "Level 6: Alpha-Beta Bot": alpha_beta_move,
    "Level 6: Expectimax Bot": expectimax_move,
    "Level 6: Minimax/Alpha-Beta": alpha_beta_move
}
