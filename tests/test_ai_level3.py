import os
import sys
import unittest

# Adjust path to find modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.level3 import beam_search_move
from game.board import Board
from game.pieces import Piece


class TestBeamSearchTruncation(unittest.TestCase):
    def test_beam_search_does_not_miss_critical_opponent_move(self):
        """
        Verify that beam_search_move does not miss a critical opponent capture
        that is positioned late in the opponent's moves list due to arbitrary truncation.
        """
        board = Board(setup=False)
        board.turn = "red"  # Red's turn

        # Place Generals (with blocking Elephant at (7, 4) to prevent face-off check)
        board.matrix[0][4] = Piece("G", "black", (0, 4), "將")
        board.matrix[9][4] = Piece("G", "red", (9, 4), "帥")
        board.matrix[6][4] = Piece("P", "red", (6, 4), "兵")

        # Place Red Rook at (9, 0)
        board.matrix[9][0] = Piece("R", "red", (9, 0), "俥")

        # Place many Black Pawns at rows 3 and 4 to fill up the first 10+ opponent moves
        # Evaluated from top-left to bottom-right:
        # Row 3 pawns:
        board.matrix[3][0] = Piece("P", "black", (3, 0), "卒")
        board.matrix[3][2] = Piece("P", "black", (3, 2), "卒")
        board.matrix[3][4] = Piece("P", "black", (3, 4), "卒")
        board.matrix[3][6] = Piece("P", "black", (3, 6), "卒")
        board.matrix[3][8] = Piece("P", "black", (3, 8), "卒")
        # Row 4 pawns:
        board.matrix[4][0] = Piece("P", "black", (4, 0), "卒")
        board.matrix[4][2] = Piece("P", "black", (4, 2), "卒")
        board.matrix[4][4] = Piece("P", "black", (4, 4), "卒")
        board.matrix[4][6] = Piece("P", "black", (4, 6), "卒")
        board.matrix[4][8] = Piece("P", "black", (4, 8), "卒")

        # Targets for Red Rook:
        # 1. Black Rook at (7, 0) - high value capture but vulnerable
        board.matrix[7][0] = Piece("R", "black", (7, 0), "車")
        # 2. Black Pawn at (9, 1) - lower value capture but safe
        board.matrix[9][1] = Piece("P", "black", (9, 1), "卒")

        # Threatening Black Rook at (7, 8) [row 7, col 8]
        # This will be evaluated LAST, well beyond the 10th index in the unsorted moves list.
        # If Red Rook moves to (7, 0), Black Rook can capture it at (7, 0).
        board.matrix[7][8] = Piece("R", "black", (7, 8), "車")

        # Run beam search with beam width k=3
        best_move = beam_search_move(board, k=3)

        # If the bug exists (arbitrary truncation of opponent's moves to top 10 unsorted),
        # Red will think capturing Rook at (7, 0) is safe and choose ((9, 0), (7, 0)).
        # If the bug is fixed, Red will see the capture threat and choose the safe ((9, 0), (9, 1)).
        self.assertEqual(
            best_move,
            ((9, 0), (9, 1)),
            "Should choose the safe capture at (9, 1) rather than the trap at (7, 0)",
        )


if __name__ == "__main__":
    unittest.main()
