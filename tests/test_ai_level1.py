import os
import sys
import unittest

# Adjust path to find modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.level1 import bfs_move, dfs_move
from game.board import Board
from game.pieces import Piece


class TestLevel1Search(unittest.TestCase):
    def setUp(self):
        # Setup a standard trap board:
        # Red Rook at (9, 0)
        # Red General at (9, 4), Black General at (0, 4)
        # Red Pawn at (6, 4) to block the face-off threat
        # Target A (trap): Black Rook at (7, 0) - high value but guarded by Black Rook at (7, 8)
        # Target B (safe): Black Pawn at (9, 1) - low value but safe
        self.trap_board = Board(setup=False)
        self.trap_board.turn = "red"

        self.trap_board.matrix[0][4] = Piece("G", "black", (0, 4), "將")
        self.trap_board.matrix[9][4] = Piece("G", "red", (9, 4), "帥")
        self.trap_board.matrix[6][4] = Piece("P", "red", (6, 4), "兵")

        self.trap_board.matrix[9][0] = Piece("R", "red", (9, 0), "俥")
        self.trap_board.matrix[7][0] = Piece("R", "black", (7, 0), "車")
        self.trap_board.matrix[9][1] = Piece("P", "black", (9, 1), "卒")
        self.trap_board.matrix[7][8] = Piece("R", "black", (7, 8), "車")

        # Setup a minimization board for Black:
        # Black turn
        # Black Rook at (0, 0)
        # Black General at (0, 4), Red General at (9, 4)
        # Red Pawn at (5, 4) to block the face-off threat
        # Target 1 (expensive): Red Rook at (0, 3) - value 900
        # Target 2 (cheap): Red Pawn at (3, 0) - value 100
        self.black_board = Board(setup=False)
        self.black_board.turn = "black"

        self.black_board.matrix[0][4] = Piece("G", "black", (0, 4), "將")
        self.black_board.matrix[9][4] = Piece("G", "red", (9, 4), "帥")
        self.black_board.matrix[5][4] = Piece("P", "red", (5, 4), "兵")

        self.black_board.matrix[0][0] = Piece("R", "black", (0, 0), "車")
        self.black_board.matrix[0][3] = Piece("R", "red", (0, 3), "俥")
        self.black_board.matrix[3][0] = Piece("P", "red", (3, 0), "兵")

    def test_bfs_move_avoids_trap_at_depth_2(self):
        """
        Verify that bfs_move at depth 2 avoids the trap at (7, 0)
        and instead captures the safe pawn at (9, 1).
        """
        # Arrange is done in setUp
        # Act
        move = bfs_move(self.trap_board, depth=2)
        # Assert
        self.assertEqual(
            move,
            ((9, 0), (9, 1)),
            "BFS should choose safe Pawn capture at (9, 1) rather than the trap at (7, 0)",
        )

    def test_dfs_move_avoids_trap_at_depth_2(self):
        """
        Verify that dfs_move at depth 2 avoids the trap at (7, 0)
        and instead captures the safe pawn at (9, 1).
        """
        # Arrange is done in setUp
        # Act
        move = dfs_move(self.trap_board, depth=2)
        # Assert
        self.assertEqual(
            move,
            ((9, 0), (9, 1)),
            "DFS should choose safe Pawn capture at (9, 1) rather than the trap at (7, 0)",
        )

    def test_bfs_move_minimizes_score_for_black(self):
        """
        Verify that bfs_move as Black minimizes the board score,
        thus choosing to capture the expensive Red Rook at (0, 3).
        """
        # Arrange is done in setUp
        # Act
        move = bfs_move(self.black_board, depth=2)
        # Assert
        self.assertEqual(
            move,
            ((0, 0), (0, 3)),
            "BFS as Black should choose to capture Red Rook at (0, 3) to minimize score",
        )

    def test_dfs_move_minimizes_score_for_black(self):
        """
        Verify that dfs_move as Black minimizes the board score,
        thus choosing to capture the expensive Red Rook at (0, 3).
        """
        # Arrange is done in setUp
        # Act
        move = dfs_move(self.black_board, depth=2)
        # Assert
        self.assertEqual(
            move,
            ((0, 0), (0, 3)),
            "DFS as Black should choose to capture Red Rook at (0, 3) to minimize score",
        )

    def test_default_depth_is_two_for_both_searches(self):
        """
        Verify that calling bfs_move and dfs_move without the depth argument
        defaults to depth 2 (and thus successfully avoids the trap).
        """
        # Arrange is done in setUp
        # Act
        move_bfs = bfs_move(self.trap_board)
        move_dfs = dfs_move(self.trap_board)
        # Assert
        self.assertEqual(
            move_bfs,
            ((9, 0), (9, 1)),
            "BFS should default to depth 2 and choose (9, 1)",
        )
        self.assertEqual(
            move_dfs,
            ((9, 0), (9, 1)),
            "DFS should default to depth 2 and choose (9, 1)",
        )


if __name__ == "__main__":
    unittest.main()
