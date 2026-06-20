import unittest
from game.board import Board
from game.pieces import Piece

class TestElephant(unittest.TestCase):
    def test_elephant_empty_board(self):
        """
        Test Case 1: Elephant at (7, 4) on an empty board.
        Should have exactly 4 valid diagonal moves.
        """
        board = Board(setup=False)
        elephant = Piece('E', 'red', (7, 4), '相')
        board.matrix[7][4] = elephant
        
        raw_moves = elephant.get_raw_moves(board.matrix)
        
        expected_moves = {
            (9, 2), (9, 6),  # bottom-left, bottom-right
            (5, 2), (5, 6)   # top-left, top-right (at river edge)
        }
        
        self.assertEqual(len(raw_moves), 4)
        self.assertEqual(set(raw_moves), expected_moves)

    def test_elephant_blocked_at_eye(self):
        """
        Test Case 2: Elephant at (7, 4) blocked by friendly piece at (8, 3) (eye for bottom-left move).
        Should only be able to move to (9, 6), (5, 2), (5, 6).
        """
        board = Board(setup=False)
        elephant = Piece('E', 'red', (7, 4), '相')
        board.matrix[7][4] = elephant
        
        # Friendly piece blocking the bottom-left eye at (8, 3)
        friendly = Piece('A', 'red', (8, 3), '仕')
        board.matrix[8][3] = friendly
        
        raw_moves = elephant.get_raw_moves(board.matrix)
        
        expected_moves = {
            (9, 6),  # bottom-right
            (5, 2), (5, 6)   # top-left, top-right (at river edge)
        }
        
        self.assertEqual(len(raw_moves), 3)
        self.assertEqual(set(raw_moves), expected_moves)

    def test_elephant_cannot_cross_river(self):
        """
        Test Case 3: Elephant at (5, 2) (at the river edge).
        Should not be able to cross the river (rows <= 4 are Black territory).
        Only diagonal moves back to Red territory (7, 0) and (7, 4) should be valid.
        """
        board = Board(setup=False)
        elephant = Piece('E', 'red', (5, 2), '相')
        board.matrix[5][2] = elephant
        
        raw_moves = elephant.get_raw_moves(board.matrix)
        
        expected_moves = {
            (7, 0), (7, 4)  # back to own territory
        }
        
        # Moves (3, 0) and (3, 4) cross the river (row 4 and 3) so they must be blocked
        self.assertEqual(len(raw_moves), 2)
        self.assertEqual(set(raw_moves), expected_moves)

    def test_elephant_capture_opponent_piece(self):
        """
        Test Case 4: Elephant at (7, 4) with opponent piece at (9, 2) (target position).
        All 4 diagonal moves should be valid, including (9, 2) for capture.
        """
        board = Board(setup=False)
        elephant = Piece('E', 'red', (7, 4), '相')
        board.matrix[7][4] = elephant
        
        # Opponent piece at target position (9, 2)
        opponent = Piece('A', 'black', (9, 2), '士')
        board.matrix[9][2] = opponent
        
        raw_moves = elephant.get_raw_moves(board.matrix)
        
        expected_moves = {
            (9, 2), (9, 6),  # bottom-left (capture), bottom-right
            (5, 2), (5, 6)   # top-left, top-right
        }
        
        self.assertEqual(len(raw_moves), 4)
        self.assertEqual(set(raw_moves), expected_moves)

if __name__ == '__main__':
    unittest.main()



