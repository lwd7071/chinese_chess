import unittest

from game.board import Board
from game.pieces import Piece


class TestCannon(unittest.TestCase):
    def test_cannon_empty_board(self):
        """
        Test Case 1: Cannon at (4, 4) on an empty board.
        Should behave like a Rook (17 valid orthogonal moves).
        """
        board = Board(setup=False)
        cannon = Piece("C", "red", (4, 4), "炮")
        board.matrix[4][4] = cannon

        raw_moves = cannon.get_raw_moves(board.matrix)

        # Expected moves along row 4 (excluding (4, 4))
        expected_row_moves = [(4, c) for c in range(9) if c != 4]
        # Expected moves along col 4 (excluding (4, 4))
        expected_col_moves = [(r, 4) for r in range(10) if r != 4]

        expected_moves = set(expected_row_moves + expected_col_moves)

        self.assertEqual(len(raw_moves), 17)
        self.assertEqual(set(raw_moves), expected_moves)

    def test_cannon_blocked_no_capture(self):
        """
        Test Case 2: Cannon at (4, 4) with friendly piece at (4, 2) (no opponent beyond).
        Cannon should only be able to move to (4, 3) left, 9 vertical squares, and 4 right squares.
        Total expected moves: 14.
        """
        board = Board(setup=False)
        cannon = Piece("C", "red", (4, 4), "炮")
        board.matrix[4][4] = cannon

        # Friendly piece at (4, 2)
        friendly = Piece("A", "red", (4, 2), "仕")
        board.matrix[4][2] = friendly

        raw_moves = cannon.get_raw_moves(board.matrix)

        expected_vertical = [(r, 4) for r in range(10) if r != 4]
        expected_horizontal_right = [(4, c) for c in range(5, 9)]
        expected_horizontal_left = [(4, 3)]
        expected_moves = set(
            expected_vertical + expected_horizontal_right + expected_horizontal_left
        )

        self.assertEqual(len(raw_moves), 14)
        self.assertEqual(set(raw_moves), expected_moves)

    def test_cannon_capture_with_one_screen(self):
        """
        Test Case 3: Cannon at (4, 4) with friendly piece at (4, 2) and opponent piece at (4, 0).
        Cannon should be able to move to (4, 3) left, (4, 0) left (capture), 9 vertical, and 4 right.
        Total expected moves: 15.
        """
        board = Board(setup=False)
        cannon = Piece("C", "red", (4, 4), "炮")
        board.matrix[4][4] = cannon

        # Friendly screen at (4, 2)
        friendly = Piece("A", "red", (4, 2), "仕")
        board.matrix[4][2] = friendly

        # Opponent target at (4, 0)
        opponent = Piece("A", "black", (4, 0), "士")
        board.matrix[4][0] = opponent

        raw_moves = cannon.get_raw_moves(board.matrix)

        expected_vertical = [(r, 4) for r in range(10) if r != 4]
        expected_horizontal_right = [(4, c) for c in range(5, 9)]
        expected_horizontal_left = [(4, 3), (4, 0)]
        expected_moves = set(
            expected_vertical + expected_horizontal_right + expected_horizontal_left
        )

        self.assertEqual(len(raw_moves), 15)
        self.assertEqual(set(raw_moves), expected_moves)

    def test_cannon_invalid_captures(self):
        """
        Test Case 4: Cannot capture without a screen, or with multiple screens.
        - Part A: Cannon at (4, 4) with opponent at (4, 2) and no screen.
          Cannon should be blocked by opponent at (4, 2) and cannot capture it.
          Expected left moves: [(4, 3)].
        - Part B: Cannon at (4, 4) with friendly at (4, 3), friendly at (4, 2), and opponent at (4, 0).
          Cannon has 2 screens, so it cannot capture (4, 0).
          Expected left moves: [].
        """
        # Part A
        board = Board(setup=False)
        cannon = Piece("C", "red", (4, 4), "炮")
        board.matrix[4][4] = cannon

        opponent = Piece("A", "black", (4, 2), "士")
        board.matrix[4][2] = opponent

        raw_moves_a = cannon.get_raw_moves(board.matrix)
        left_moves_a = [m for m in raw_moves_a if m[0] == 4 and m[1] < 4]
        self.assertEqual(left_moves_a, [(4, 3)])

        # Part B
        board_b = Board(setup=False)
        cannon_b = Piece("C", "red", (4, 4), "炮")
        board_b.matrix[4][4] = cannon_b

        friendly1 = Piece("A", "red", (4, 3), "仕")
        board_b.matrix[4][3] = friendly1
        friendly2 = Piece("A", "red", (4, 2), "仕")
        board_b.matrix[4][2] = friendly2
        opponent_b = Piece("A", "black", (4, 0), "士")
        board_b.matrix[4][0] = opponent_b

        raw_moves_b = cannon_b.get_raw_moves(board_b.matrix)
        left_moves_b = [m for m in raw_moves_b if m[0] == 4 and m[1] < 4]
        self.assertEqual(left_moves_b, [])


if __name__ == "__main__":
    unittest.main()
