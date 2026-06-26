import unittest
import sys
import os

# Adjust path to find modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.board import Board
from game.pieces import Piece
from main import calculate_remaining_piece_score, calculate_win_exp

class TestEXPSystem(unittest.TestCase):
    def test_calculate_remaining_piece_score(self):
        board = Board(setup=False)
        # Place pieces for Red
        board.matrix[9][4] = Piece('G', 'red', (9, 4), '帥') # 0 pts
        board.matrix[9][0] = Piece('R', 'red', (9, 0), '俥') # 90 pts
        board.matrix[9][1] = Piece('H', 'red', (9, 1), '傌') # 45 pts
        board.matrix[7][1] = Piece('C', 'red', (7, 1), '炮') # 45 pts
        board.matrix[9][2] = Piece('E', 'red', (9, 2), '相') # 20 pts
        board.matrix[9][3] = Piece('A', 'red', (9, 3), '仕') # 20 pts
        board.matrix[6][0] = Piece('P', 'red', (6, 0), '兵') # 10 pts
        board.matrix[6][2] = Piece('P', 'red', (6, 2), '兵') # 10 pts

        # Total Red score = 90 + 45 + 45 + 20 + 20 + 10 + 10 = 240
        score_red = calculate_remaining_piece_score(board, 'red')
        self.assertEqual(score_red, 240)

        # Black has no pieces
        score_black = calculate_remaining_piece_score(board, 'black')
        self.assertEqual(score_black, 0)

    def test_calculate_win_exp(self):
        board = Board(setup=False)
        # Place pieces for Black
        board.matrix[0][4] = Piece('G', 'black', (0, 4), '將') # 0 pts
        board.matrix[0][0] = Piece('R', 'black', (0, 0), '車') # 90 pts
        board.matrix[0][1] = Piece('H', 'black', (0, 1), '馬') # 45 pts
        board.matrix[2][1] = Piece('C', 'black', (2, 1), '砲') # 45 pts
        board.matrix[3][0] = Piece('P', 'black', (3, 0), '卒') # 10 pts
        board.matrix[3][2] = Piece('P', 'black', (3, 2), '卒') # 10 pts

        # Total Black score = 90 + 45 + 45 + 10 + 10 = 200
        # Win EXP = 100 + 200 // 2 = 200
        exp_black = calculate_win_exp(board, 'black')
        self.assertEqual(exp_black, 200)

if __name__ == '__main__':
    unittest.main()
