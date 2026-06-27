import unittest

from game.board import Board
from game.pieces import Piece


class TestPawn(unittest.TestCase):
    def test_pawn_red_before_river(self):
        """
        Test Case 1: Red Pawn at (6, 4) (before crossing river).
        Should only have exactly 1 valid forward move to (5, 4).
        """
        board = Board(setup=False)
        pawn = Piece("P", "red", (6, 4), "兵")
        board.matrix[6][4] = pawn

        raw_moves = pawn.get_raw_moves(board.matrix)
        expected_moves = {(5, 4)}

        self.assertEqual(len(raw_moves), 1)
        self.assertEqual(set(raw_moves), expected_moves)

    def test_pawn_red_after_river(self):
        """
        Test Case 2: Red Pawn at (4, 4) (after crossing river).
        Should have exactly 3 valid moves: forward to (3, 4), sideways to (4, 3) and (4, 5).
        """
        board = Board(setup=False)
        pawn = Piece("P", "red", (4, 4), "兵")
        board.matrix[4][4] = pawn

        raw_moves = pawn.get_raw_moves(board.matrix)
        expected_moves = {(3, 4), (4, 3), (4, 5)}

        self.assertEqual(len(raw_moves), 3)
        self.assertEqual(set(raw_moves), expected_moves)

    def test_pawn_blocking_and_capture(self):
        """
        Test Case 3: Red Pawn at (4, 4) after crossing river.
        - Blocked by friendly piece at (3, 4).
        - Opponent piece at (4, 3).
        Should have exactly 2 valid moves: (4, 3) (capture) and (4, 5) (move sideways).
        """
        board = Board(setup=False)
        pawn = Piece("P", "red", (4, 4), "兵")
        board.matrix[4][4] = pawn

        # Friendly piece blocking forward at (3, 4)
        friendly = Piece("R", "red", (3, 4), "俥")
        board.matrix[3][4] = friendly

        # Opponent piece at (4, 3)
        opponent = Piece("R", "black", (4, 3), "俥")
        board.matrix[4][3] = opponent

        raw_moves = pawn.get_raw_moves(board.matrix)
        expected_moves = {(4, 3), (4, 5)}

        self.assertEqual(len(raw_moves), 2)
        self.assertEqual(set(raw_moves), expected_moves)

    def test_pawn_black_before_and_after_river(self):
        """
        Test Case 4: Black Pawn before and after crossing river.
        - Before river at (3, 4): Should only move forward down to (4, 4).
        - After river at (5, 4): Should move forward down to (6, 4) and sideways to (5, 3) and (5, 5).
        """
        # Before river
        board1 = Board(setup=False)
        pawn1 = Piece("P", "black", (3, 4), "卒")
        board1.matrix[3][4] = pawn1

        raw_moves1 = pawn1.get_raw_moves(board1.matrix)
        self.assertEqual(set(raw_moves1), {(4, 4)})

        # After river
        board2 = Board(setup=False)
        pawn2 = Piece("P", "black", (5, 4), "卒")
        board2.matrix[5][4] = pawn2

        raw_moves2 = pawn2.get_raw_moves(board2.matrix)
        self.assertEqual(set(raw_moves2), {(6, 4), (5, 3), (5, 5)})


if __name__ == "__main__":
    unittest.main()
