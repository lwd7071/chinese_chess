# Board model representing the 9x10 grid and game state
from game.pieces import Piece

class Board:
    def __init__(self, setup=True):
        self.matrix = [[None for _ in range(9)] for _ in range(10)]
        self.turn = 'red' # Red goes first
        self.history = [] # Stack of (from_pos, to_pos, captured_piece, old_turn)
        
        if setup:
            self.setup_pieces()

    def setup_pieces(self):
        # 1. Setup Black pieces (top rows: 0, 2, 3)
        self.matrix[0][0] = Piece('R', 'black', (0, 0), '車')
        self.matrix[0][1] = Piece('H', 'black', (0, 1), '馬')
        self.matrix[0][2] = Piece('E', 'black', (0, 2), '象')
        self.matrix[0][3] = Piece('A', 'black', (0, 3), '士')
        self.matrix[0][4] = Piece('G', 'black', (0, 4), '將')
        self.matrix[0][5] = Piece('A', 'black', (0, 5), '士')
        self.matrix[0][6] = Piece('E', 'black', (0, 6), '象')
        self.matrix[0][7] = Piece('H', 'black', (0, 7), '馬')
        self.matrix[0][8] = Piece('R', 'black', (0, 8), '車')
        
        self.matrix[2][1] = Piece('C', 'black', (2, 1), '砲')
        self.matrix[2][7] = Piece('C', 'black', (2, 7), '砲')
        
        for c in [0, 2, 4, 6, 8]:
            self.matrix[3][c] = Piece('P', 'black', (3, c), '卒')

        # 2. Setup Red pieces (bottom rows: 9, 7, 6)
        self.matrix[9][0] = Piece('R', 'red', (9, 0), '俥')
        self.matrix[9][1] = Piece('H', 'red', (9, 1), '傌')
        self.matrix[9][2] = Piece('E', 'red', (9, 2), '相')
        self.matrix[9][3] = Piece('A', 'red', (9, 3), '仕')
        self.matrix[9][4] = Piece('G', 'red', (9, 4), '帥')
        self.matrix[9][5] = Piece('A', 'red', (9, 5), '仕')
        self.matrix[9][6] = Piece('E', 'red', (9, 6), '相')
        self.matrix[9][7] = Piece('H', 'red', (9, 7), '傌')
        self.matrix[9][8] = Piece('R', 'red', (9, 8), '俥')
        
        self.matrix[7][1] = Piece('C', 'red', (7, 1), '炮')
        self.matrix[7][7] = Piece('C', 'red', (7, 7), '炮')
        
        for c in [0, 2, 4, 6, 8]:
            self.matrix[6][c] = Piece('P', 'red', (6, c), '兵')

    def get_piece(self, pos):
        r, c = pos
        if 0 <= r < 10 and 0 <= c < 9:
            return self.matrix[r][c]
        return None

    def get_general_pos(self, color):
        for r in range(10):
            for c in range(9):
                p = self.matrix[r][c]
                if p and p.name == 'G' and p.color == color:
                    return (r, c)
        return None

    def is_in_check(self, color):
        """Checks if the general of the given color is under threat"""
        g_pos = self.get_general_pos(color)
        if g_pos is None:
            return False
            
        opp_color = 'black' if color == 'red' else 'red'
        
        # Check if any opponent piece can capture the general
        for r in range(10):
            for c in range(9):
                p = self.matrix[r][c]
                if p and p.color == opp_color:
                    if g_pos in p.get_raw_moves(self.matrix):
                        return True
                        
        # Check General Face-Off Rule ("Lộ mặt tướng")
        # If both generals are on the same column with no pieces in between, it is invalid
        # This counts as check / threat
        red_g = self.get_general_pos('red')
        black_g = self.get_general_pos('black')
        if red_g and black_g and red_g[1] == black_g[1]:
            col = red_g[1]
            blocked = False
            # Check cells between them
            start_r = min(red_g[0], black_g[0]) + 1
            end_r = max(red_g[0], black_g[0])
            for row in range(start_r, end_r):
                if self.matrix[row][col] is not None:
                    blocked = True
                    break
            if not blocked:
                # If they face off, the side whose turn it is cannot make a move that keeps them facing off
                # To enforce this: facing off counts as a threat/check!
                return True
                
        return False

    def get_all_legal_moves(self, color):
        """
        Calculates all legal moves for a given color.
        Returns list of ((from_row, from_col), (to_row, to_col))
        """
        legal_moves = []
        for r in range(10):
            for c in range(9):
                p = self.matrix[r][c]
                if p and p.color == color:
                    raw_moves = p.get_raw_moves(self.matrix)
                    for tr, tc in raw_moves:
                        # Test move
                        from_pos = (r, c)
                        to_pos = (tr, tc)
                        
                        captured = self.make_move(from_pos, to_pos, test_only=True)
                        if not self.is_in_check(color):
                            legal_moves.append((from_pos, to_pos))
                        self.undo_move(test_only=True)
        return legal_moves

    def make_move(self, from_pos, to_pos, test_only=False):
        """
        Executes a move. Switches turn.
        test_only: if True, skips visual checks or history logs that are GUI-specific
        """
        fr, fc = from_pos
        tr, tc = to_pos
        
        piece = self.matrix[fr][fc]
        captured = self.matrix[tr][tc]
        
        # Record history
        self.history.append((from_pos, to_pos, captured, self.turn))
        
        # Move piece in matrix
        self.matrix[tr][tc] = piece
        self.matrix[fr][fc] = None
        piece.pos = to_pos
        
        # Switch turn
        self.turn = 'black' if self.turn == 'red' else 'red'
        return captured

    def undo_move(self, test_only=False):
        if not self.history:
            return
            
        from_pos, to_pos, captured, old_turn = self.history.pop()
        fr, fc = from_pos
        tr, tc = to_pos
        
        piece = self.matrix[tr][tc]
        self.matrix[fr][fc] = piece
        self.matrix[tr][tc] = captured
        
        piece.pos = from_pos
        if captured:
            captured.pos = to_pos
            
        self.turn = old_turn

    def copy(self):
        """Returns a deep copy of the board state"""
        b = Board(setup=False)
        b.turn = self.turn
        # Copy pieces
        for r in range(10):
            for c in range(9):
                p = self.matrix[r][c]
                if p:
                    b.matrix[r][c] = p.copy()
        # History is copied as ref or new list
        b.history = list(self.history)
        return b
