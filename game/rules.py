# Rules validation logic (checkmate, stalemate)

def is_in_check(board, color):
    return board.is_in_check(color)

def has_lost(board, color):
    """
    In Chinese Chess, a player loses if:
    1. They are in check and have no legal moves left (Checkmate).
    2. They have no legal moves left even if not in check (Stalemate / Vô tử).
    """
    legal_moves = board.get_all_legal_moves(color)
    return len(legal_moves) == 0

def is_checkmate(board, color):
    """Specific check for Checkmate (in check and no moves)"""
    return board.is_in_check(color) and len(board.get_all_legal_moves(color)) == 0

def is_stalemate(board, color):
    """Specific check for Stalemate (not in check but no moves)"""
    return not board.is_in_check(color) and len(board.get_all_legal_moves(color)) == 0

def is_no_cross_river_pieces(board):
    """
    Checks if both sides have no pieces left that can cross the river.
    Cross-river capable pieces are: 'R' (Rook), 'C' (Cannon), 'H' (Horse), 'P' (Pawn).
    If neither side has any of these, then the game is a draw.
    """
    if not hasattr(board, "matrix") or not isinstance(board.matrix, list):
        return False
    cross_river_types = {'R', 'C', 'H', 'P'}
    for r in range(10):
        for c in range(9):
            piece = board.matrix[r][c]
            if piece and hasattr(piece, "name") and piece.name in cross_river_types:
                return False
    return True

