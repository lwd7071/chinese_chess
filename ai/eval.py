# Positional evaluation using Piece-Square Tables (PST)

PIECE_VALUES = {
    'G': 10000, # General (Tướng)
    'R': 900,   # Rook (Xe)
    'C': 450,   # Cannon (Pháo)
    'H': 300,   # Horse (Mã)
    'E': 200,   # Elephant (Tượng)
    'A': 200,   # Advisor (Sĩ)
    'P': 100    # Pawn (Tốt)
}

# Piece-Square Tables (PST) from RED perspective (bottom of board, moving up)
# High values encourage placement. Black PST is vertically mirrored.

# Red Pawn (兵): gains value crossing river (row <= 4) and moving to center
PST_PAWN_RED = [
    [0,  3,  6,  9,  9,  9,  6,  3,  0],  # row 0 (deep in enemy territory)
    [0, 12, 18, 24, 30, 24, 18, 12,  0],
    [0, 10, 15, 20, 25, 20, 15, 10,  0],
    [0,  8, 12, 16, 20, 16, 12,  8,  0],
    [0,  6,  9, 12, 15, 12,  9,  6,  0],  # row 4 (river crossed)
    # -------------------- RIVER --------------------
    [0,  0,  0,  0,  5,  0,  0,  0,  0],  # row 5 (just crossed / river)
    [0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0,  0,  0,  0,  0,  0,  0,  0,  0]   # row 9
]

# Knight (馬): prefers center, hates edges
PST_KNIGHT_RED = [
    [ 0, -5, -5, -5, -5, -5, -5, -5,  0],
    [ 0,  5, 10, 10, 10, 10, 10,  5,  0],
    [ 0, 10, 15, 15, 20, 15, 15, 10,  0],
    [ 0,  5, 10, 15, 20, 15, 10,  5,  0],
    [ 0,  5, 10, 10, 15, 10, 10,  5,  0],
    [ 0,  0,  5, 10, 10, 10,  5,  0,  0],
    [ 0,  0,  5,  5, 10,  5,  5,  0,  0],
    [ 0,  0,  0,  0,  5,  0,  0,  0,  0],
    [ 0, -5,  0,  0,  0,  0,  0, -5,  0],
    [ 0, -5, -5, -5, -5, -5, -5, -5,  0]
]

# Cannon (Pháo): prefers 2nd/3rd rank for defense, center files
PST_CANNON_RED = [
    [0,  0,  0,  0,  5,  0,  0,  0,  0],
    [0,  2,  2,  5, 10,  5,  2,  2,  0],
    [0,  0,  0,  2,  5,  2,  0,  0,  0],
    [0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0,  0,  0,  2,  2,  2,  0,  0,  0],
    [0,  2,  5,  5,  5,  5,  5,  2,  0],
    [0,  5, 10, 15, 15, 15, 10,  5,  0], # Defensive base
    [0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0,  0,  0,  0,  0,  0,  0,  0,  0]
]

# Rook (Xe): prefers open lanes and ranks 0, 1, 9
PST_ROOK_RED = [
    [10, 15, 10, 10, 10, 10, 10, 15, 10],
    [10, 20, 15, 20, 20, 20, 15, 20, 10],
    [ 5, 10, 10, 10, 10, 10, 10, 10,  5],
    [ 5, 10, 10, 10, 10, 10, 10, 10,  5],
    [ 5, 10, 10, 10, 10, 10, 10, 10,  5],
    [ 5, 10, 10, 10, 10, 10, 10, 10,  5],
    [ 0,  5,  5,  5,  5,  5,  5,  5,  0],
    [ 0,  5,  5,  5, 10,  5,  5,  5,  0],
    [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
    [ 0,  5,  5, 10, 10, 10,  5,  5,  0]
]

# Elephant and Advisor: prefer staying near the palace center for protection
PST_DEFENSIVE = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 0, 5, 0, 2, 0, 0], # Red palace top
    [0, 0, 0, 5, 0, 5, 0, 0, 0], # Red palace mid
    [0, 0, 2, 5, 10, 5, 2, 0, 0] # Red palace bottom
]

def evaluate_board(board):
    """
    Evaluation function from RED perspective.
    Score = (Red Material + Red Positional) - (Black Material + Black Positional)
    """
    score = 0
    for r in range(10):
        for c in range(9):
            p = board.matrix[r][c]
            if p is None:
                continue
                
            val = PIECE_VALUES.get(p.name, 0)
            bonus = 0
            
            # Apply PST bonuses
            if p.color == 'red':
                if p.name == 'P':
                    bonus = PST_PAWN_RED[r][c]
                elif p.name == 'H':
                    bonus = PST_KNIGHT_RED[r][c]
                elif p.name == 'C':
                    bonus = PST_CANNON_RED[r][c]
                elif p.name == 'R':
                    bonus = PST_ROOK_RED[r][c]
                elif p.name in ['E', 'A']:
                    bonus = PST_DEFENSIVE[r][c]
                score += val + bonus
            else: # Black
                # Vertically mirror row for black PST lookup
                mr = 9 - r
                # Horizontally mirror col to keep symmetry
                mc = 8 - c
                if p.name == 'P':
                    bonus = PST_PAWN_RED[mr][mc]
                elif p.name == 'H':
                    bonus = PST_KNIGHT_RED[mr][mc]
                elif p.name == 'C':
                    bonus = PST_CANNON_RED[mr][mc]
                elif p.name == 'R':
                    bonus = PST_ROOK_RED[mr][mc]
                elif p.name in ['E', 'A']:
                    bonus = PST_DEFENSIVE[mr][mc]
                score -= val + bonus
                
    return score
