import unittest
import sys
import os

# Adjust path to find modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.board import Board
from game.pieces import Piece
from ai.level6 import expectimax_move

class TestExpectimaxBlack(unittest.TestCase):
    def test_expectimax_as_black_turn(self):
        """
        Verify that expectimax_move runs when it is Black's turn
        and returns a valid move.
        """
        board = Board()
        board.turn = 'black' # Force Black's turn
        
        move = expectimax_move(board, depth=1)
        self.assertIsNotNone(move, "Should find a valid move for Black")
        
        # Verify that the move is indeed legal for Black
        legal_moves = board.get_all_legal_moves('black')
        self.assertIn(move, legal_moves, "The selected move must be a legal move for Black")

    def test_expectimax_minimax_logic_black(self):
        """
        Test that Black AI minimizes the board score (from Red's perspective)
        rather than treating its own turn as a chance node.
        We set up a simple board where Black (MIN) has two moves:
        Move A: leads to a lower score (better for Black)
        Move B: leads to a higher score (worse for Black)
        And we verify that it chooses Move A.
        """
        # Create an empty board
        board = Board(setup=False)
        board.turn = 'black'
        
        # Place Black General at (0, 4)
        board.matrix[0][4] = Piece('G', 'black', (0, 4), '將')
        # Place Red General at (9, 4)
        board.matrix[9][4] = Piece('G', 'red', (9, 4), '帥')
        # Place a blocking piece on column 4 to prevent general face-off
        board.matrix[5][4] = Piece('P', 'red', (5, 4), '兵')
        
        # Place a Black Rook at (0, 0)
        board.matrix[0][0] = Piece('R', 'black', (0, 0), '車')
        
        # Place two Red targets for the Black Rook:
        # Target 1 (cheaper): Red Pawn at (3, 0) - value 100
        # Target 2 (expensive): Red Rook at (0, 3) - value 900
        board.matrix[3][0] = Piece('P', 'red', (3, 0), '兵')
        board.matrix[0][3] = Piece('R', 'red', (0, 3), '俥')
        
        # Note: Black Rook at (0, 0) can move to (1, 0), (2, 0), (3, 0) [capturing Pawn],
        # or (0, 1), (0, 2), (0, 3) [capturing Rook].
        # Capturing the Red Rook is the best move for Black because it decreases Red's material score by 900.
        # Capturing the Red Pawn decreases Red's material score by only 100.
        # Let's run expectimax with depth=1
        best_move = expectimax_move(board, depth=1)
        
        # Best move should be capturing the Red Rook at (0, 3)
        self.assertEqual(best_move[0], (0, 0), "Should move from (0, 0)")
        self.assertEqual(best_move[1], (0, 3), "Should capture the Red Rook at (0, 3) to minimize Red's score")

if __name__ == '__main__':
    unittest.main()
