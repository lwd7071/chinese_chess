import unittest

from game.board import Board
from game.pieces import Piece


class TestGeneral(unittest.TestCase):
    def test_general_palace_center(self):
        """
        Test Case 1: Red General at Palace center (8, 4).
        Should have exactly 4 valid orthogonal moves: (7, 4), (9, 4), (8, 3), (8, 5).
        """
        board = Board(setup=False)
        general = Piece("G", "red", (8, 4), "帥")
        board.matrix[8][4] = general

        raw_moves = general.get_raw_moves(board.matrix)
        expected_moves = {(7, 4), (9, 4), (8, 3), (8, 5)}

        self.assertEqual(len(raw_moves), 4)
        self.assertEqual(set(raw_moves), expected_moves)

    def test_general_palace_boundaries(self):
        """
        Test Case 2: Red General at Palace corner (9, 3).
        Should only have exactly 2 valid moves: (8, 3) (up) and (9, 4) (right).
        All moves out of the Palace (e.g. to (9, 2) left, or off-board) should be filtered.
        """
        board = Board(setup=False)
        general = Piece("G", "red", (9, 3), "帥")
        board.matrix[9][3] = general

        raw_moves = general.get_raw_moves(board.matrix)
        expected_moves = {(8, 3), (9, 4)}

        self.assertEqual(len(raw_moves), 2)
        self.assertEqual(set(raw_moves), expected_moves)

    def test_general_friendly_blocking(self):
        """
        Test Case 3: Red General at Palace center (8, 4) blocked by friendly piece at (7, 4).
        Should only have exactly 3 valid moves: (9, 4), (8, 3), (8, 5).
        """
        board = Board(setup=False)
        general = Piece("G", "red", (8, 4), "帥")
        board.matrix[8][4] = general

        # Friendly piece at (7, 4)
        friendly = Piece("R", "red", (7, 4), "俥")
        board.matrix[7][4] = friendly

        raw_moves = general.get_raw_moves(board.matrix)
        expected_moves = {(9, 4), (8, 3), (8, 5)}

        self.assertEqual(len(raw_moves), 3)
        self.assertEqual(set(raw_moves), expected_moves)

    def test_general_opponent_capture(self):
        """
        Test Case 4: Red General at Palace center (8, 4) with opponent piece at (7, 4).
        Should have exactly 4 valid moves, including capturing the opponent piece at (7, 4).
        """
        board = Board(setup=False)
        general = Piece("G", "red", (8, 4), "帥")
        board.matrix[8][4] = general

        # Opponent piece (black rook) at (7, 4)
        opponent = Piece("R", "black", (7, 4), "俥")
        board.matrix[7][4] = opponent

        raw_moves = general.get_raw_moves(board.matrix)
        expected_moves = {(7, 4), (9, 4), (8, 3), (8, 5)}

        self.assertEqual(len(raw_moves), 4)
        self.assertEqual(set(raw_moves), expected_moves)


if __name__ == "__main__":
    unittest.main()
