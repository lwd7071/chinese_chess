import unittest

from game.board import Board
from game.pieces import Piece


class TestAdvisor(unittest.TestCase):
    def test_advisor_palace_center(self):
        """
        Test Case 1: Red Advisor at center of Palace (8, 4) on an empty board.
        Should have exactly 4 diagonal moves to the corners of the Palace.
        """
        board = Board(setup=False)
        advisor = Piece("A", "red", (8, 4), "仕")
        board.matrix[8][4] = advisor

        raw_moves = advisor.get_raw_moves(board.matrix)

        expected_moves = {
            (7, 3),
            (7, 5),  # top corners
            (9, 3),
            (9, 5),  # bottom corners
        }

        self.assertEqual(len(raw_moves), 4)
        self.assertEqual(set(raw_moves), expected_moves)

    def test_advisor_palace_corners(self):
        """
        Test Case 2: Red Advisor at palace corner (9, 3) on an empty board.
        Should only have exactly 1 valid diagonal move to the center of the Palace (8, 4).
        """
        board = Board(setup=False)
        advisor = Piece("A", "red", (9, 3), "仕")
        board.matrix[9][3] = advisor

        raw_moves = advisor.get_raw_moves(board.matrix)

        expected_moves = {(8, 4)}

        self.assertEqual(len(raw_moves), 1)
        self.assertEqual(set(raw_moves), expected_moves)

    def test_advisor_friendly_blocking(self):
        """
        Test Case 3: Red Advisor at palace center (8, 4) blocked by friendly piece at (7, 3).
        Should only have exactly 3 valid diagonal moves: (7, 5), (9, 3), (9, 5).
        """
        board = Board(setup=False)
        advisor = Piece("A", "red", (8, 4), "仕")
        board.matrix[8][4] = advisor

        # Friendly piece blocking at (7, 3)
        friendly = Piece("R", "red", (7, 3), "俥")
        board.matrix[7][3] = friendly

        raw_moves = advisor.get_raw_moves(board.matrix)

        expected_moves = {
            (7, 5),  # top-right
            (9, 3),
            (9, 5),  # bottom corners
        }

        self.assertEqual(len(raw_moves), 3)
        self.assertEqual(set(raw_moves), expected_moves)

    def test_advisor_capture_opponent(self):
        """
        Test Case 4: Red Advisor at palace center (8, 4) with opponent piece at (7, 3).
        Should have exactly 4 valid diagonal moves, including capturing the opponent piece at (7, 3).
        """
        board = Board(setup=False)
        advisor = Piece("A", "red", (8, 4), "仕")
        board.matrix[8][4] = advisor

        # Opponent piece (black rook) at (7, 3)
        opponent = Piece("R", "black", (7, 3), "俥")
        board.matrix[7][3] = opponent

        raw_moves = advisor.get_raw_moves(board.matrix)

        expected_moves = {
            (7, 3),
            (7, 5),  # top corners (7, 3 is capture)
            (9, 3),
            (9, 5),  # bottom corners
        }

        self.assertEqual(len(raw_moves), 4)
        self.assertEqual(set(raw_moves), expected_moves)


if __name__ == "__main__":
    unittest.main()
