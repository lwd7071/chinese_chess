# Pieces model for Chinese Chess


class Piece:
    def __init__(self, name, color, pos, char):
        """
        name: 'G' (General), 'A' (Advisor), 'E' (Elephant), 'R' (Rook), 'C' (Cannon), 'H' (Horse), 'P' (Pawn)
        color: 'red' or 'black'
        pos: Tuple (row, col)
        char: Chinese character representation
        """
        self.name = name
        self.color = color
        self.pos = pos
        self.char = char

    def get_raw_moves(self, board_matrix):
        """
        Returns a list of all pseudo-legal target positions (row, col)
        without considering if the move puts the own general in check.
        """
        r, c = self.pos
        moves = []

        if self.name == "G":  # General (Tướng)
            # 1 step orthogonal, within Palace
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            palace_rows = range(7, 10) if self.color == "red" else range(0, 3)
            palace_cols = range(3, 6)

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if nr in palace_rows and nc in palace_cols:
                    dest = board_matrix[nr][nc]
                    if dest is None or dest.color != self.color:
                        moves.append((nr, nc))

        elif self.name == "A":  # Advisor (Sĩ)
            # 1 step diagonal, within Palace
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            palace_rows = range(7, 10) if self.color == "red" else range(0, 3)
            palace_cols = range(3, 6)

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if nr in palace_rows and nc in palace_cols:
                    dest = board_matrix[nr][nc]
                    if dest is None or dest.color != self.color:
                        moves.append((nr, nc))

        elif self.name == "E":  # Elephant (Tượng)
            # 2 steps diagonal, cannot cross river, blocked at center eye
            directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
            valid_rows = range(5, 10) if self.color == "red" else range(0, 5)

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if nr in valid_rows and 0 <= nc < 9:
                    # Check blocking eye
                    eye_r, eye_c = r + dr // 2, c + dc // 2
                    if board_matrix[eye_r][eye_c] is None:
                        dest = board_matrix[nr][nc]
                        if dest is None or dest.color != self.color:
                            moves.append((nr, nc))

        elif self.name == "R":  # Rook (Xe)
            # Slide orthogonally
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                while 0 <= nr < 10 and 0 <= nc < 9:
                    dest = board_matrix[nr][nc]
                    if dest is None:
                        moves.append((nr, nc))
                    elif dest.color != self.color:
                        moves.append((nr, nc))
                        break  # Stop after capturing opponent
                    else:
                        break  # Blocked by own piece
                    nr += dr
                    nc += dc

        elif self.name == "C":  # Cannon (Pháo)
            # Slide orthogonally. Eat by jumping over exactly 1 piece.
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                jumped = False
                while 0 <= nr < 10 and 0 <= nc < 9:
                    dest = board_matrix[nr][nc]
                    if not jumped:
                        if dest is None:
                            moves.append((nr, nc))
                        else:
                            jumped = True  # Hit first piece (screen/ngòi)
                    else:
                        if dest is not None:
                            if dest.color != self.color:
                                moves.append((nr, nc))  # Capture
                            break  # Blocked after first jump
                    nr += dr
                    nc += dc

        elif self.name == "H":  # Horse (Mã)
            # L-shape: 2 steps in 1 dir + 1 step in perp dir.
            # Blocked at leg (1 step in 2-step dir)
            potential_moves = [
                # vertical moves (dr=2, leg is dr=1)
                (-2, -1, -1, 0),
                (-2, 1, -1, 0),
                (2, -1, 1, 0),
                (2, 1, 1, 0),
                # horizontal moves (dc=2, leg is dc=1)
                (-1, -2, 0, -1),
                (1, -2, 0, -1),
                (-1, 2, 0, 1),
                (1, 2, 0, 1),
            ]

            for dr, dc, leg_r, leg_c in potential_moves:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 10 and 0 <= nc < 9:
                    # Check blocking leg
                    if board_matrix[r + leg_r][c + leg_c] is None:
                        dest = board_matrix[nr][nc]
                        if dest is None or dest.color != self.color:
                            moves.append((nr, nc))

        elif self.name == "P":  # Pawn (Tốt)
            # 1 step forward. After river, also 1 step sideways.
            if self.color == "red":
                # Move up
                if r - 1 >= 0:
                    dest = board_matrix[r - 1][c]
                    if dest is None or dest.color != self.color:
                        moves.append((r - 1, c))
                # Sideways after river (Red river boundary is row 5, so river is row <= 4)
                if r <= 4:
                    for dc in [-1, 1]:
                        nc = c + dc
                        if 0 <= nc < 9:
                            dest = board_matrix[r][nc]
                            if dest is None or dest.color != self.color:
                                moves.append((r, nc))
            else:  # Black
                # Move down
                if r + 1 < 10:
                    dest = board_matrix[r + 1][c]
                    if dest is None or dest.color != self.color:
                        moves.append((r + 1, c))
                # Sideways after river (Black river boundary is row 4, so river is row >= 5)
                if r >= 5:
                    for dc in [-1, 1]:
                        nc = c + dc
                        if 0 <= nc < 9:
                            dest = board_matrix[r][nc]
                            if dest is None or dest.color != self.color:
                                moves.append((r, nc))

        return moves

    def copy(self):
        p = Piece(self.name, self.color, self.pos, self.char)
        return p

    def __repr__(self):
        return f"{self.color[0].upper()}_{self.name}{self.pos}"
