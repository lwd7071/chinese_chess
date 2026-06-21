# Pygame Renderer for Xiangqi Board and Pieces
import pygame
import math

# Wooden theme colors
COLOR_WOOD_BG = (235, 195, 135)      # Light wood grain base
COLOR_BOARD_LINE = (110, 60, 20)      # Dark wood lines
COLOR_PALACE_LINE = (160, 110, 60)    # Muted Palace diagonals
COLOR_PIECE_BG = (250, 240, 215)      # Ivory piece background
COLOR_RED = (200, 30, 30)             # Red piece text
COLOR_BLACK = (20, 20, 20)            # Black piece text
COLOR_BORDER = (160, 110, 60)         # Circle outline
COLOR_HIGHLIGHT = (240, 200, 40)      # Yellow outline for selected
COLOR_MOVE_DOT = (30, 180, 80)        # Green dot for valid moves

# Piece descriptions for tooltips
PIECE_DESCRIPTIONS = {
    'G': {
        'name': "Tướng (General)",
        'rules': [
            "• Đi từng ô một (ngang hoặc dọc).",
            "• Chỉ di chuyển trong phạm vi cung cấm.",
            "• Hai Tướng không được đối mặt trực tiếp",
            "  trên cùng một cột dọc mà không có cản."
        ]
    },
    'A': {
        'name': "Sĩ (Advisor)",
        'rules': [
            "• Đi chéo đúng 1 ô mỗi nước đi.",
            "• Chỉ di chuyển trong phạm vi cung cấm.",
            "• Chức năng chính là bảo vệ Tướng."
        ]
    },
    'E': {
        'name': "Tượng (Elephant)",
        'rules': [
            "• Đi chéo đúng 2 ô (hình chữ Điền).",
            "• Không được đi qua sông sang lãnh thổ địch.",
            "• Bị cản (chẹn mắt Tượng) nếu có bất kỳ",
            "  quân nào nằm ở ô tâm của nước đi."
        ]
    },
    'H': {
        'name': "Mã (Horse)",
        'rules': [
            "• Đi theo hình chữ L (tiến 2 ô thẳng",
            "  sau đó rẽ ngang 1 ô).",
            "• Bị cản (cản chân Mã) nếu có quân cờ",
            "  nằm ngay cạnh ô xuất phát hướng thẳng."
        ]
    },
    'R': {
        'name': "Xe (Rook)",
        'rules': [
            "• Đi ngang hoặc dọc tùy ý không giới hạn ô.",
            "• Không thể nhảy qua quân cờ khác."
        ]
    },
    'C': {
        'name': "Pháo (Cannon)",
        'rules': [
            "• Đi ngang hoặc dọc giống Xe.",
            "• Khi ăn quân: Bắt buộc phải nhảy qua",
            "  đúng 1 quân cờ khác làm ngòi cản."
        ]
    },
    'P': {
        'name': "Tốt (Pawn)",
        'rules': [
            "• Đi thẳng tiến lên 1 ô mỗi nước.",
            "• Khi chưa qua sông: Chỉ được đi thẳng.",
            "• Khi đã qua sông: Được đi thẳng hoặc",
            "  đi ngang sang hai bên."
        ]
    }
}

class Renderer:
    def __init__(self, cell_size=64, offset_x=50, offset_y=50):
        self.cell_size = cell_size
        self.offset_x = offset_x
        self.offset_y = offset_y
        
        # Detect Chinese font support
        self.font_name = self.detect_chinese_font()
        self.chinese_supported = self.font_name is not None
        
        # Load fonts
        if self.chinese_supported:
            self.piece_font = pygame.font.SysFont(self.font_name, int(cell_size * 0.55), bold=True)
            self.label_font = pygame.font.SysFont(self.font_name, int(cell_size * 0.35))
        else:
            self.piece_font = pygame.font.SysFont(["Segoe UI", "Tahoma", "Arial"], int(cell_size * 0.5), bold=True)
            self.label_font = pygame.font.SysFont(["Segoe UI", "Tahoma", "Arial"], int(cell_size * 0.3))
            
        # Tooltip fonts must always support Vietnamese (independent of Chinese piece font support)
        self.tooltip_header_font = pygame.font.SysFont(["Segoe UI", "Tahoma", "Arial"], int(cell_size * 0.28), bold=True)
        self.tooltip_body_font = pygame.font.SysFont(["Segoe UI", "Tahoma", "Arial"], int(cell_size * 0.24))

    def detect_chinese_font(self):
        chinese_fonts = ['microsoftyahei', 'simhei', 'simsun', 'msgothic', 'dengxian', 'arialunicode']
        for f in chinese_fonts:
            if pygame.font.match_font(f):
                return f
        return None

    def get_xy(self, r, c):
        """Converts board index (row, col) to screen coordinates (x, y)"""
        x = self.offset_x + c * self.cell_size
        y = self.offset_y + r * self.cell_size
        return x, y

    def draw_board(self, surface):
        # 1. Fill wood background
        surface.fill(COLOR_WOOD_BG)
        
        # Draw board border
        border_rect = pygame.Rect(
            self.offset_x - 10, self.offset_y - 10,
            8 * self.cell_size + 20, 9 * self.cell_size + 20
        )
        pygame.draw.rect(surface, COLOR_BOARD_LINE, border_rect, 3)
        
        # 2. Draw horizontal lines (10 lines)
        for r in range(10):
            x1, y1 = self.get_xy(r, 0)
            x2, y2 = self.get_xy(r, 8)
            pygame.draw.line(surface, COLOR_BOARD_LINE, (x1, y1), (x2, y2), 1)
            
        # 3. Draw vertical lines (9 lines, broken at the River rows 4 to 5)
        for c in range(9):
            if c == 0 or c == 8:
                # Outer boundaries are continuous
                x1, y1 = self.get_xy(0, c)
                x2, y2 = self.get_xy(9, c)
                pygame.draw.line(surface, COLOR_BOARD_LINE, (x1, y1), (x2, y2), 1)
            else:
                # Top half (rows 0-4)
                x1, y1 = self.get_xy(0, c)
                x2, y2 = self.get_xy(4, c)
                pygame.draw.line(surface, COLOR_BOARD_LINE, (x1, y1), (x2, y2), 1)
                # Bottom half (rows 5-9)
                x1, y1 = self.get_xy(5, c)
                x2, y2 = self.get_xy(9, c)
                pygame.draw.line(surface, COLOR_BOARD_LINE, (x1, y1), (x2, y2), 1)

        # 4. Draw Palaces (diagonals in rows 0-2 and 7-9, cols 3-5)
        palaces = [
            ((0, 3), (2, 5)), ((0, 5), (2, 3)), # Black palace
            ((7, 3), (9, 5)), ((7, 5), (9, 3))  # Red palace
        ]
        for p1, p2 in palaces:
            x1, y1 = self.get_xy(p1[0], p1[1])
            x2, y2 = self.get_xy(p2[0], p2[1])
            pygame.draw.line(surface, COLOR_PALACE_LINE, (x1, y1), (x2, y2), 1)
            
        # 5. Draw River text labels (Sở Hà - Hán Giới)
        if self.chinese_supported:
            river_lbl1 = self.label_font.render("楚 河", True, COLOR_BOARD_LINE)
            river_lbl2 = self.label_font.render("漢 界", True, COLOR_BOARD_LINE)
        else:
            river_lbl1 = self.label_font.render("CHU RIVER", True, COLOR_BOARD_LINE)
            river_lbl2 = self.label_font.render("HAN BORDER", True, COLOR_BOARD_LINE)
            
        # Draw on row 4.5
        rx1 = self.offset_x + 2 * self.cell_size - river_lbl1.get_width() // 2
        rx2 = self.offset_x + 6 * self.cell_size - river_lbl2.get_width() // 2
        ry = self.offset_y + 4 * self.cell_size + self.cell_size // 2 - river_lbl1.get_height() // 2
        
        surface.blit(river_lbl1, (rx1, ry))
        surface.blit(river_lbl2, (rx2, ry))
        
        # 6. Draw star/cross markers for Cannon and Pawn starting points
        cross_positions = [
            (2, 1), (2, 7), (7, 1), (7, 7), # Cannons
            (3, 0), (3, 2), (3, 4), (3, 6), (3, 8), # Black Pawns
            (6, 0), (6, 2), (6, 4), (6, 6), (6, 8)  # Red Pawns
        ]
        for r, c in cross_positions:
            self.draw_cross(surface, r, c)

    def draw_cross(self, surface, r, c):
        """Draws small chess cross indicators at given intersections"""
        cx, cy = self.get_xy(r, c)
        size = 8
        gap = 3
        # Left boundary check for drawing half crosses
        if c > 0:
            # top-left corner
            pygame.draw.line(surface, COLOR_BOARD_LINE, (cx - gap, cy - gap), (cx - gap - size, cy - gap), 1)
            pygame.draw.line(surface, COLOR_BOARD_LINE, (cx - gap, cy - gap), (cx - gap, cy - gap - size), 1)
            # bottom-left corner
            pygame.draw.line(surface, COLOR_BOARD_LINE, (cx - gap, cy + gap), (cx - gap - size, cy + gap), 1)
            pygame.draw.line(surface, COLOR_BOARD_LINE, (cx - gap, cy + gap), (cx - gap, cy + gap + size), 1)
        if c < 8:
            # top-right corner
            pygame.draw.line(surface, COLOR_BOARD_LINE, (cx + gap, cy - gap), (cx + gap + size, cy - gap), 1)
            pygame.draw.line(surface, COLOR_BOARD_LINE, (cx + gap, cy - gap), (cx + gap, cy - gap - size), 1)
            # bottom-right corner
            pygame.draw.line(surface, COLOR_BOARD_LINE, (cx + gap, cy + gap), (cx + gap + size, cy + gap), 1)
            pygame.draw.line(surface, COLOR_BOARD_LINE, (cx + gap, cy + gap), (cx + gap, cy + gap + size), 1)

    def draw_piece(self, surface, piece, is_selected=False):
        r, c = piece.pos
        cx, cy = self.get_xy(r, c)
        radius = int(self.cell_size * 0.44)
        
        # Outer circle outline
        pygame.draw.circle(surface, COLOR_BORDER, (cx, cy), radius)
        # Inner circle fill
        pygame.draw.circle(surface, COLOR_PIECE_BG, (cx, cy), radius - 2)
        
        # Determine text and color
        text_color = COLOR_RED if piece.color == 'red' else COLOR_BLACK
        
        if self.chinese_supported:
            char = piece.char
        else:
            # Fallback english abbreviation mapping
            char_map = {
                'G': 'G', 'A': 'A', 'E': 'E', 'R': 'R', 'C': 'C', 'H': 'H', 'P': 'P'
            }
            char = char_map.get(piece.name, '?')
            
        # Draw character
        txt = self.piece_font.render(char, True, text_color)
        surface.blit(txt, (cx - txt.get_width() // 2, cy - txt.get_height() // 2))
        
        # Highlights
        if is_selected:
            pygame.draw.circle(surface, COLOR_HIGHLIGHT, (cx, cy), radius + 2, 2)

    def draw_move_hints(self, surface, board, valid_destinations):
        """Draws indicators for all legal destination squares of the selected piece, highlighting captures in red"""
        for r, c in valid_destinations:
            cx, cy = self.get_xy(r, c)
            target = board.get_piece((r, c))
            if target:
                # Capture move: highlight the opponent piece with a thick red circle
                radius = int(self.cell_size * 0.44)
                pygame.draw.circle(surface, (231, 76, 60), (cx, cy), radius + 2, 3)
            else:
                # Normal move: green dot indicator
                pygame.draw.circle(surface, COLOR_MOVE_DOT, (cx, cy), 8)
                pygame.draw.circle(surface, COLOR_MOVE_DOT, (cx, cy), 14, 1)

    def draw_check_effect(self, surface, board):
        """Draws a pulsing red glow around the King in check and displays 'CHIẾU TƯỚNG!'"""
        import math
        for color in ['red', 'black']:
            if board.is_in_check(color):
                g_pos = board.get_general_pos(color)
                if g_pos:
                    gx, gy = self.get_xy(g_pos[0], g_pos[1])
                    radius = int(self.cell_size * 0.44)
                    # Flashing effect based on ticks (period ~1s)
                    pulse = (math.sin(pygame.time.get_ticks() * 0.015) + 1) / 2 # 0.0 to 1.0
                    glow_color = (231, 76, 60)
                    glow_radius = radius + int(3 + 6 * pulse)
                    pygame.draw.circle(surface, glow_color, (gx, gy), glow_radius, 3)
                    
                    # Also draw check banner text at the top of the board
                    board_center_x = self.offset_x + 4 * self.cell_size
                    text_y = self.offset_y - 42
                    
                    check_text = "⚠️ CHIẾU TƯỚNG! ⚠️"
                    check_font = pygame.font.SysFont(["Segoe UI", "Tahoma", "Arial"], 20, bold=True)
                    text_color = (231, 76, 60)
                    
                    txt = check_font.render(check_text, True, text_color)
                    # Draw a solid dark background for readability
                    bg_rect = pygame.Rect(
                        board_center_x - txt.get_width() // 2 - 10,
                        text_y - 2,
                        txt.get_width() + 20,
                        txt.get_height() + 4
                    )
                    pygame.draw.rect(surface, (30, 30, 30), bg_rect, 0, 4)
                    pygame.draw.rect(surface, (231, 76, 60), bg_rect, 1, 4) # Red border
                    surface.blit(txt, (board_center_x - txt.get_width() // 2, text_y))
            
    def get_board_pos_from_screen(self, mouse_pos):
        """Converts mouse click coordinates (x, y) to board indices (row, col) or None"""
        mx, my = mouse_pos
        # Check proximity to all 90 cells
        for r in range(10):
            for c in range(9):
                cx, cy = self.get_xy(r, c)
                dist = math.sqrt((mx - cx)**2 + (my - cy)**2)
                if dist < self.cell_size * 0.45:
                    return r, c
        return None

    def draw_tooltip(self, surface, piece, mouse_pos):
        """Draws an elegant hover tooltip box with piece rules next to the cursor"""
        desc = PIECE_DESCRIPTIONS.get(piece.name)
        if not desc:
            return
            
        header_surface = self.tooltip_header_font.render(desc['name'], True, (240, 200, 40))
        max_w = header_surface.get_width()
        
        rule_surfaces = []
        for rule in desc['rules']:
            surf = self.tooltip_body_font.render(rule, True, (230, 230, 230))
            rule_surfaces.append(surf)
            max_w = max(max_w, surf.get_width())
            
        padding = 12
        box_w = max_w + padding * 2
        box_h = header_surface.get_height() + len(rule_surfaces) * 16 + padding * 2 + 8
        
        tx = mouse_pos[0] + 15
        ty = mouse_pos[1] + 15
        
        # Screen bounds (WIDTH=940, HEIGHT=700)
        if tx + box_w > 940:
            tx = mouse_pos[0] - box_w - 15
        if ty + box_h > 700:
            ty = mouse_pos[1] - box_h - 15
            
        if tx < 0:
            tx = 10
        if ty < 0:
            ty = 10
            
        # Draw translucent tooltip box
        tooltip_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        tooltip_surf.fill((20, 20, 20, 220))
        
        # Border
        pygame.draw.rect(tooltip_surf, (0, 173, 181), (0, 0, box_w, box_h), 2, 4)
        
        # Title
        tooltip_surf.blit(header_surface, (padding, padding))
        
        # Divider line
        sep_y = padding + header_surface.get_height() + 4
        pygame.draw.line(tooltip_surf, (100, 100, 100, 150), (padding, sep_y), (box_w - padding, sep_y), 1)
        
        # Rules list
        curr_y = sep_y + 6
        for surf in rule_surfaces:
            tooltip_surf.blit(surf, (padding, curr_y))
            curr_y += 16
            
        surface.blit(tooltip_surf, (tx, ty))
