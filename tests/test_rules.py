import unittest
import sys
import os

# Adjust path to find modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.board import Board
from game.pieces import Piece
from game.rules import is_in_check, is_checkmate, is_stalemate, has_lost

class TestXiangqiRules(unittest.TestCase):
    def test_initial_no_check(self):
        """Verify that neither side is in check or has lost in the initial setup."""
        board = Board()
        self.assertFalse(is_in_check(board, 'red'))
        self.assertFalse(is_in_check(board, 'black'))
        self.assertFalse(has_lost(board, 'red'))
        self.assertFalse(has_lost(board, 'black'))

    def test_flying_king_rule(self):
        """Verify that two generals directly facing each other on the same column causes check/threat."""
        board = Board(setup=False)
        board.matrix[0][4] = Piece('G', 'black', (0, 4), '將')
        board.matrix[9][4] = Piece('G', 'red', (9, 4), '帥')
        
        # Facing each other with no intervening pieces -> should count as check/threat
        self.assertTrue(is_in_check(board, 'red'))
        self.assertTrue(is_in_check(board, 'black'))

        # Place a blocking piece in between
        board.matrix[5][4] = Piece('P', 'red', (5, 4), '兵')
        self.assertFalse(is_in_check(board, 'red'))
        self.assertFalse(is_in_check(board, 'black'))

    def test_checkmate_scenario(self):
        """Verify checkmate detection (in check and has no legal moves left)."""
        board = Board(setup=False)
        board.turn = 'black'
        # Setup board: Generals placed with a blocking Pawn at (6, 4) to prevent face-off
        board.matrix[0][4] = Piece('G', 'black', (0, 4), '將')
        board.matrix[9][4] = Piece('G', 'red', (9, 4), '帥')
        board.matrix[6][4] = Piece('P', 'red', (6, 4), '兵')
        
        # Red Rook at (1, 4) directly checks Black General
        board.matrix[1][4] = Piece('R', 'red', (1, 4), '俥')
        # Red Rooks at (1, 3) and (1, 5) cover palace columns
        board.matrix[1][3] = Piece('R', 'red', (1, 3), '俥')
        board.matrix[1][5] = Piece('R', 'red', (1, 5), '俥')
        
        self.assertTrue(is_in_check(board, 'black'))
        self.assertTrue(is_checkmate(board, 'black'))
        self.assertFalse(is_stalemate(board, 'black'))
        self.assertTrue(has_lost(board, 'black'))

    def test_stalemate_scenario(self):
        """Verify stalemate detection (not in check but has no legal moves left)."""
        board = Board(setup=False)
        board.turn = 'black'
        board.matrix[0][4] = Piece('G', 'black', (0, 4), '將')
        board.matrix[9][4] = Piece('G', 'red', (9, 4), '帥')
        board.matrix[6][4] = Piece('P', 'red', (6, 4), '兵')
        
        # Surround Black General but without placing it in check directly.
        # Red Rooks control palace exits columns 3 and 5, and row 1.
        board.matrix[9][3] = Piece('R', 'red', (9, 3), '俥')
        board.matrix[9][5] = Piece('R', 'red', (9, 5), '俥')
        board.matrix[1][0] = Piece('R', 'red', (1, 0), '俥')
        
        self.assertFalse(is_in_check(board, 'black'))
        self.assertTrue(is_stalemate(board, 'black'))
        self.assertFalse(is_checkmate(board, 'black'))
        self.assertTrue(has_lost(board, 'black'))

    def test_self_check_prevention(self):
        """Verify that a player cannot make a move that leaves their own General in check (pinned piece)."""
        board = Board(setup=False)
        board.turn = 'red'
        board.matrix[9][4] = Piece('G', 'red', (9, 4), '帥')
        board.matrix[0][4] = Piece('G', 'black', (0, 4), '將')
        board.matrix[6][4] = Piece('P', 'red', (6, 4), '兵') # Block face-off
        
        # Black Rook at (7, 4) pins the Red Pawn at (6, 4) against the General at (9, 4)
        board.matrix[7][4] = Piece('R', 'black', (7, 4), '車')
        
        # The Red Pawn at (6, 4) cannot move sideways or forward because that reveals check
        legal_moves = board.get_all_legal_moves('red')
        pawn_moves = [m for m in legal_moves if m[0] == (6, 4)]
        self.assertEqual(len(pawn_moves), 0)

    def test_piece_movement_rules(self):
        """Verify movement constraints and boundaries for all individual pieces."""
        # --- General limits (Palace boundaries, 1 step orthogonal) ---
        board = Board(setup=False)
        g = Piece('G', 'red', (9, 4), '帥')
        board.matrix[9][4] = g
        # Orthogonal moves allowed
        self.assertIn((8, 4), g.get_raw_moves(board.matrix))
        self.assertIn((9, 3), g.get_raw_moves(board.matrix))
        # Diagonal moves not allowed
        self.assertNotIn((8, 3), g.get_raw_moves(board.matrix))
        # Exiting palace not allowed
        g.pos = (7, 4)
        board.matrix[7][4] = g
        board.matrix[9][4] = None
        self.assertNotIn((6, 4), g.get_raw_moves(board.matrix))

        # --- Advisor limits (Palace boundaries, 1 step diagonal) ---
        board = Board(setup=False)
        a = Piece('A', 'red', (9, 3), '仕')
        board.matrix[9][3] = a
        self.assertIn((8, 4), a.get_raw_moves(board.matrix))
        self.assertNotIn((9, 4), a.get_raw_moves(board.matrix)) # No orthogonal
        a.pos = (8, 4)
        board.matrix[8][4] = a
        board.matrix[9][3] = None
        self.assertIn((7, 3), a.get_raw_moves(board.matrix))
        self.assertNotIn((6, 3), a.get_raw_moves(board.matrix)) # Exits palace

        # --- Elephant limits (2 steps diagonal, eye-blocking, no river crossing) ---
        board = Board(setup=False)
        e = Piece('E', 'red', (9, 2), '相')
        board.matrix[9][2] = e
        self.assertIn((7, 4), e.get_raw_moves(board.matrix))
        # Eye-blocking
        board.matrix[8][3] = Piece('P', 'red', (8, 3), '兵')
        self.assertNotIn((7, 4), e.get_raw_moves(board.matrix))
        # Crossing river boundary (Red Elephant stays at row >= 5)
        board.matrix[8][3] = None
        e.pos = (5, 2)
        board.matrix[5][2] = e
        board.matrix[9][2] = None
        self.assertNotIn((3, 0), e.get_raw_moves(board.matrix))

        # --- Horse leg blocking (leg/hobble rule) ---
        board = Board(setup=False)
        h = Piece('H', 'red', (9, 1), '傌')
        board.matrix[9][1] = h
        self.assertIn((7, 0), h.get_raw_moves(board.matrix))
        self.assertIn((7, 2), h.get_raw_moves(board.matrix))
        # leg is at (8, 1)
        board.matrix[8][1] = Piece('P', 'red', (8, 1), '兵')
        self.assertNotIn((7, 0), h.get_raw_moves(board.matrix))
        self.assertNotIn((7, 2), h.get_raw_moves(board.matrix))

        # --- Cannon capture mechanics (needs exactly 1 screen) ---
        board = Board(setup=False)
        c = Piece('C', 'red', (7, 1), '炮')
        board.matrix[7][1] = c
        board.matrix[2][1] = Piece('R', 'black', (2, 1), '車')
        # No screen -> cannot capture
        self.assertNotIn((2, 1), c.get_raw_moves(board.matrix))
        # 1 screen -> can capture
        board.matrix[5][1] = Piece('P', 'red', (5, 1), '兵')
        self.assertIn((2, 1), c.get_raw_moves(board.matrix))
        # 2 screens -> cannot capture
        board.matrix[4][1] = Piece('P', 'red', (4, 1), '兵')
        self.assertNotIn((2, 1), c.get_raw_moves(board.matrix))

        # --- Pawn movement before and after crossing river ---
        board = Board(setup=False)
        p = Piece('P', 'red', (6, 2), '兵')
        board.matrix[6][2] = p
        # Before river: only forward allowed
        self.assertIn((5, 2), p.get_raw_moves(board.matrix))
        self.assertNotIn((6, 1), p.get_raw_moves(board.matrix))
        # After river: forward and sideways allowed
        p.pos = (4, 2)
        board.matrix[4][2] = p
        board.matrix[6][2] = None
        self.assertIn((3, 2), p.get_raw_moves(board.matrix))
        self.assertIn((4, 1), p.get_raw_moves(board.matrix))
        self.assertIn((4, 3), p.get_raw_moves(board.matrix))

if __name__ == '__main__':
    unittest.main()
