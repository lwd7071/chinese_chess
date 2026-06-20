import unittest
from game.board import Board
from game.pieces import Piece

class TestHorse(unittest.TestCase):
    def test_horse_empty_board(self):
        """
        Test Case 1: Horse at (4, 4) on an empty board.
        Should have exactly 8 valid L-shaped moves.
        """
        board = Board(setup=False)
        horse = Piece('H', 'red', (4, 4), '傌')
        board.matrix[4][4] = horse
        
        raw_moves = horse.get_raw_moves(board.matrix)
        
        expected_moves = {
            (2, 3), (2, 5),  # vertical up
            (6, 3), (6, 5),  # vertical down
            (3, 2), (5, 2),  # horizontal left
            (3, 6), (5, 6)   # horizontal right
        }
        
        self.assertEqual(len(raw_moves), 8)
        self.assertEqual(set(raw_moves), expected_moves)

    def test_horse_blocked_by_friendly_piece(self):
        """
        Test Case 2: Horse at (4, 4) blocked by friendly piece at (3, 4) (leg for up directions).
        Should have exactly 6 valid moves (up moves (2, 3) and (2, 5) blocked).
        """
        board = Board(setup=False)
        horse = Piece('H', 'red', (4, 4), '傌')
        board.matrix[4][4] = horse
        
        # Friendly piece at the leg (3, 4)
        friendly = Piece('A', 'red', (3, 4), '仕')
        board.matrix[3][4] = friendly
        
        raw_moves = horse.get_raw_moves(board.matrix)
        
        expected_moves = {
            (6, 3), (6, 5),  # vertical down
            (3, 2), (5, 2),  # horizontal left
            (3, 6), (5, 6)   # horizontal right
        }
        
        self.assertEqual(len(raw_moves), 6)
        self.assertEqual(set(raw_moves), expected_moves)

    def test_horse_capture_opponent_piece(self):
        """
        Test Case 3: Horse at (4, 4) with opponent piece at (2, 3) (target position).
        All 8 moves should be valid, including (2, 3) for capture.
        """
        board = Board(setup=False)
        horse = Piece('H', 'red', (4, 4), '傌')
        board.matrix[4][4] = horse
        
        # Opponent piece at the target position (2, 3)
        opponent = Piece('A', 'black', (2, 3), '仕')
        board.matrix[2][3] = opponent
        
        raw_moves = horse.get_raw_moves(board.matrix)
        
        expected_moves = {
            (2, 3), (2, 5),  # vertical up
            (6, 3), (6, 5),  # vertical down
            (3, 2), (5, 2),  # horizontal left
            (3, 6), (5, 6)   # horizontal right
        }
        
        self.assertEqual(len(raw_moves), 8)
        self.assertEqual(set(raw_moves), expected_moves)

    def test_horse_edge_cases_and_blocking(self):
        """
        Test Case 4: Horse at starting position (9, 1) near the corner.
        On empty board, only 3 moves are within board boundaries: (7, 0), (7, 2), (8, 3).
        If we place a friendly piece at (8, 1) (leg for up-moves), only (8, 3) should be valid.
        """
        board = Board(setup=False)
        horse = Piece('H', 'red', (9, 1), '傌')
        board.matrix[9][1] = horse
        
        # 1. Test empty board first
        raw_moves = horse.get_raw_moves(board.matrix)
        expected_empty = {(7, 0), (7, 2), (8, 3)}
        self.assertEqual(len(raw_moves), 3)
        self.assertEqual(set(raw_moves), expected_empty)
        
        # 2. Block the vertical-up leg (8, 1)
        friendly = Piece('A', 'red', (8, 1), '仕')
        board.matrix[8][1] = friendly
        
        raw_moves_blocked = horse.get_raw_moves(board.matrix)
        expected_blocked = {(8, 3)}
        self.assertEqual(len(raw_moves_blocked), 1)
        self.assertEqual(set(raw_moves_blocked), expected_blocked)

if __name__ == '__main__':
    unittest.main()



