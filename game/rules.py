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
