# Positional evaluation using Piece-Square Tables (PST)

PIECE_VALUES = {
    "G": 10000,  # General (Tướng)
    "R": 900,  # Rook (Xe)
    "C": 450,  # Cannon (Pháo)
    "H": 300,  # Horse (Mã)
    "E": 200,  # Elephant (Tượng)
    "A": 200,  # Advisor (Sĩ)
    "P": 100,  # Pawn (Tốt)
}

# Piece-Square Tables (PST) from RED perspective (bottom of board, moving up)
# High values encourage placement. Black PST is vertically mirrored.

# Red Pawn (兵): gains value crossing river (row <= 4) and moving to center
PST_PAWN_RED = [
    [0, 3, 6, 9, 9, 9, 6, 3, 0],  # row 0 (deep in enemy territory)
    [0, 12, 18, 24, 30, 24, 18, 12, 0],
    [0, 10, 15, 20, 25, 20, 15, 10, 0],
    [0, 8, 12, 16, 20, 16, 12, 8, 0],
    [0, 6, 9, 12, 15, 12, 9, 6, 0],  # row 4 (river crossed)
    # -------------------- RIVER --------------------
    [0, 0, 0, 0, 5, 0, 0, 0, 0],  # row 5 (just crossed / river)
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  # row 9
]

# Knight (馬): prefers center, hates edges
PST_KNIGHT_RED = [
    [0, -5, -5, -5, -5, -5, -5, -5, 0],
    [0, 5, 10, 10, 10, 10, 10, 5, 0],
    [0, 10, 15, 15, 20, 15, 15, 10, 0],
    [0, 5, 10, 15, 20, 15, 10, 5, 0],
    [0, 5, 10, 10, 15, 10, 10, 5, 0],
    [0, 0, 5, 10, 10, 10, 5, 0, 0],
    [0, 0, 5, 5, 10, 5, 5, 0, 0],
    [0, 0, 0, 0, 5, 0, 0, 0, 0],
    [0, -5, 0, 0, 0, 0, 0, -5, 0],
    [0, -5, -5, -5, -5, -5, -5, -5, 0],
]

# Cannon (Pháo): prefers 2nd/3rd rank for defense, center files
PST_CANNON_RED = [
    [0, 0, 0, 0, 5, 0, 0, 0, 0],
    [0, 2, 2, 5, 10, 5, 2, 2, 0],
    [0, 0, 0, 2, 5, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 2, 0, 0, 0],
    [0, 2, 5, 5, 5, 5, 5, 2, 0],
    [0, 5, 10, 15, 15, 15, 10, 5, 0],  # Defensive base
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

# Rook (Xe): prefers open lanes and ranks 0, 1, 9
PST_ROOK_RED = [
    [10, 15, 10, 10, 10, 10, 10, 15, 10],
    [10, 20, 15, 20, 20, 20, 15, 20, 10],
    [5, 10, 10, 10, 10, 10, 10, 10, 5],
    [5, 10, 10, 10, 10, 10, 10, 10, 5],
    [5, 10, 10, 10, 10, 10, 10, 10, 5],
    [5, 10, 10, 10, 10, 10, 10, 10, 5],
    [0, 5, 5, 5, 5, 5, 5, 5, 0],
    [0, 5, 5, 5, 10, 5, 5, 5, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 5, 5, 10, 10, 10, 5, 5, 0],
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
    [0, 0, 2, 0, 5, 0, 2, 0, 0],  # Red palace top
    [0, 0, 0, 5, 0, 5, 0, 0, 0],  # Red palace mid
    [0, 0, 2, 5, 10, 5, 2, 0, 0],  # Red palace bottom
]


def evaluate_board(board):
    """
    Hàm đánh giá giá trị bàn cờ (Evaluation function) từ góc nhìn của quân ĐỎ (RED).
    Điểm số (Score) = (Tổng giá trị quân Đỏ + Điểm vị trí quân Đỏ) - (Tổng giá trị quân Đen + Điểm vị trí quân Đen).
    - Điểm dương (> 0): Đỏ đang chiếm ưu thế.
    - Điểm âm (< 0): Đen đang chiếm ưu thế.
    - Điểm bằng 0: Thế trận cân bằng.
    """
    score = 0
    # Duyệt qua toàn bộ 10 hàng và 9 cột trên bàn cờ cờ tướng
    for r in range(10):
        for c in range(9):
            p = board.matrix[r][c]
            if p is None:
                continue

            # Lấy giá trị cơ bản của quân cờ (ví dụ: Tướng=10000, Xe=900, Pháo=450,...)
            val = PIECE_VALUES.get(p.name, 0)
            bonus = 0

            # Tính toán điểm thưởng vị trí (PST - Piece-Square Table) tùy thuộc vào màu quân cờ
            if p.color == "red":
                if p.name == "P":
                    bonus = PST_PAWN_RED[r][c] # Tốt đỏ: thưởng khi sang sông và tiến vào trung tâm
                elif p.name == "H":
                    bonus = PST_KNIGHT_RED[r][c] # Mã đỏ: ưa thích vị trí trung tâm, tránh rìa bàn cờ
                elif p.name == "C":
                    bonus = PST_CANNON_RED[r][c] # Pháo đỏ: thích kiểm soát các hàng phòng thủ và cột trung tâm
                elif p.name == "R":
                    bonus = PST_ROOK_RED[r][c] # Xe đỏ: ưa thích các cột mở và vị trí thông thoáng
                elif p.name in ["E", "A"]:
                    bonus = PST_DEFENSIVE[r][c] # Sĩ/Tượng đỏ: thích ở vị trí trung tâm của cung tướng để phòng thủ
                # Cộng điểm cho quân Đỏ
                score += val + bonus
            else:  # Quân Đen (Black)
                # Lật ngược tọa độ hàng (vertically mirror) để đối chiếu đúng với bảng điểm PST của Đỏ
                mr = 9 - r
                # Lật ngược tọa độ cột (horizontally mirror) để duy trì tính đối xứng
                mc = 8 - c
                if p.name == "P":
                    bonus = PST_PAWN_RED[mr][mc]
                elif p.name == "H":
                    bonus = PST_KNIGHT_RED[mr][mc]
                elif p.name == "C":
                    bonus = PST_CANNON_RED[mr][mc]
                elif p.name == "R":
                    bonus = PST_ROOK_RED[mr][mc]
                elif p.name in ["E", "A"]:
                    bonus = PST_DEFENSIVE[mr][mc]
                # Trừ điểm đối với quân Đen (do đang tính theo góc nhìn của Đỏ)
                score -= val + bonus

    return score
