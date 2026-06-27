import unittest

from game.board import Board
from game.pieces import Piece


class TestRook(unittest.TestCase):
    def test_rook_empty_board(self):
        """
        Test Case 1: Rook on an empty board at (4, 4) should be able to move
        to all 17 orthogonal squares on the 9x10 grid (9 in column 4, 8 in row 4).
        """
        board = Board(setup=False)
        rook = Piece("R", "red", (4, 4), "俥")
        board.matrix[4][4] = rook

        raw_moves = rook.get_raw_moves(board.matrix)

        # Expected moves along row 4 (excluding (4, 4))
        expected_row_moves = [(4, c) for c in range(9) if c != 4]
        # Expected moves along col 4 (excluding (4, 4))
        expected_col_moves = [(r, 4) for r in range(10) if r != 4]

        expected_moves = set(expected_row_moves + expected_col_moves)

        self.assertEqual(len(raw_moves), 17)
        self.assertEqual(set(raw_moves), expected_moves)

    def test_rook_blocked_by_friendly_piece(self):
        """
        Test Case 2: Rook on (9, 0) blocked by friendly piece at (7, 0).
        Rook can only move to (8, 0) vertically, and (9, 1)..(9, 8) horizontally.
        """
        board = Board(setup=False)
        rook = Piece("R", "red", (9, 0), "俥")
        board.matrix[9][0] = rook

        # Friendly piece at (7, 0)
        friendly = Piece("A", "red", (7, 0), "仕")
        board.matrix[7][0] = friendly

        raw_moves = rook.get_raw_moves(board.matrix)

        expected_moves = set([(8, 0)] + [(9, c) for c in range(1, 9)])

        self.assertEqual(len(raw_moves), 9)
        self.assertEqual(set(raw_moves), expected_moves)

    def test_rook_capture_opponent_piece(self):
        """
        Test Case 3: Rook on (9, 0) captures opponent piece at (7, 0).
        Rook can move to (8, 0) and (7, 0) vertically, and (9, 1)..(9, 8) horizontally.
        """
        board = Board(setup=False)
        rook = Piece("R", "red", (9, 0), "俥")
        board.matrix[9][0] = rook

        # Opponent piece at (7, 0)
        opponent = Piece("A", "black", (7, 0), "士")
        board.matrix[7][0] = opponent

        raw_moves = rook.get_raw_moves(board.matrix)

        expected_moves = set([(8, 0), (7, 0)] + [(9, c) for c in range(1, 9)])

        self.assertEqual(len(raw_moves), 10)
        self.assertEqual(set(raw_moves), expected_moves)

    def test_rook_horizontal_blocking_and_capture(self):
        """
        Test Case 4: Rook on (4, 4) with friendly piece at (4, 2) and opponent piece at (4, 7).
        Vertical: 9 squares in column 4 (all except (4, 4)).
        Horizontal left: (4, 3) is valid, (4, 2) is blocked.
        Horizontal right: (4, 5), (4, 6), (4, 7) are valid, (4, 8) is blocked after capture.
        Total expected moves: 9 + 1 + 3 = 13 moves.
        """
        board = Board(setup=False)
        rook = Piece("R", "red", (4, 4), "俥")
        board.matrix[4][4] = rook

        # Friendly piece at (4, 2)
        friendly = Piece("A", "red", (4, 2), "仕")
        board.matrix[4][2] = friendly

        # Opponent piece at (4, 7)
        opponent = Piece("A", "black", (4, 7), "士")
        board.matrix[4][7] = opponent

        raw_moves = rook.get_raw_moves(board.matrix)

        expected_vertical = [(r, 4) for r in range(10) if r != 4]
        expected_horizontal = [(4, 3), (4, 5), (4, 6), (4, 7)]
        expected_moves = set(expected_vertical + expected_horizontal)

        self.assertEqual(len(raw_moves), 13)
        self.assertEqual(set(raw_moves), expected_moves)


if __name__ == "__main__":
    unittest.main()
