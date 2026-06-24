# Pygame Renderer for Xiangqi Board and Pieces (Anti-Slop Redesign)
import pygame
import math
import random
from gui.assets import get_asset

# Color palettes for themes
THEMES = {
    "classic_wood": {
        "bg_base": (200, 150, 95),         # Rosewood light
        "line_color": (82, 45, 12),        # Dark Walnut lines
        "palace_color": (120, 80, 50),     # Palace lines
        "check_color": (231, 76, 60),      # Red check glow
        "hint_color": (218, 165, 32),      # Gold hint
    },
    "white_marble": {
        "bg_base": (240, 240, 242),        # White marble
        "line_color": (160, 125, 45),      # Gold lines
        "palace_color": (180, 150, 80),    # Palace lines
        "check_color": (231, 76, 60),      # Red check glow
        "hint_color": (41, 128, 185),      # Blue hint
    },
    "dark_glass": {
        "bg_base": (15, 20, 32),           # Smoked glass dark
        "line_color": (0, 165, 230),       # Neon Cyan lines
        "palace_color": (0, 110, 180),     # Darker Neon blue
        "check_color": (255, 60, 60),      # Bright neon check glow
        "hint_color": (89, 222, 155),      # Green hint
    }
}

PIECE_SKINS = {
    "classic_wood_piece": {
        "edge": (205, 190, 160),
        "highlight": (255, 252, 242),
        "border": (110, 75, 40),
        "red_text": (185, 30, 30),
        "black_text": (28, 28, 28)
    },
    "royal_jade": {
        "edge": (0, 95, 60),
        "highlight": (60, 220, 160),
        "border": (0, 60, 40),
        "red_text": (242, 202, 80),        # Gold on Jade for red side
        "black_text": (230, 255, 240)      # White on Jade for black side
    },
    "cyber_steel": {
        "edge": (45, 45, 48),
        "highlight": (210, 215, 225),
        "border": (80, 80, 85),
        "red_text": (255, 65, 65),         # Glowing neon red
        "black_text": (0, 225, 255)        # Glowing neon cyan
    }
}

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
    def __init__(self, cell_size=60, offset_x=40, offset_y=50):
        self.cell_size = cell_size
        self.offset_x = offset_x
        self.offset_y = offset_y
        
        self.font_name = self.detect_chinese_font()
        self.chinese_supported = self.font_name is not None
        
        # Load fonts
        if self.chinese_supported:
            self.piece_font = pygame.font.SysFont(self.font_name, int(cell_size * 0.48), bold=True)
            self.label_font = pygame.font.SysFont(self.font_name, int(cell_size * 0.38))
        else:
            self.piece_font = pygame.font.SysFont(["Segoe UI", "Tahoma", "Arial"], int(cell_size * 0.5), bold=True)
            self.label_font = pygame.font.SysFont(["Segoe UI", "Tahoma", "Arial"], int(cell_size * 0.3))
            
        self.tooltip_header_font = pygame.font.SysFont(["Segoe UI", "Tahoma", "Arial"], int(cell_size * 0.28), bold=True)
        self.tooltip_body_font = pygame.font.SysFont(["Segoe UI", "Tahoma", "Arial"], int(cell_size * 0.24))

        self.tooltip_cache = {}
        self.cache_tooltips()
        
        # Capture burst particles
        self.particles = []
        
        # Cache procedural board textures to save performance (620x820 left-hand area)
        self.board_width = 620
        self.board_height = 820
        self.board_textures = {}
        self.generate_and_cache_board_textures()

    def update_layout(self, cell_size, offset_x, offset_y, board_width, board_height):
        self.cell_size = cell_size
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.board_width = board_width
        self.board_height = board_height
        
        # Reload fonts with new cell_size
        if self.chinese_supported:
            self.piece_font = pygame.font.SysFont(self.font_name, int(cell_size * 0.48), bold=True)
            self.label_font = pygame.font.SysFont(self.font_name, int(cell_size * 0.38))
        else:
            self.piece_font = pygame.font.SysFont(["Segoe UI", "Tahoma", "Arial"], int(cell_size * 0.5), bold=True)
            self.label_font = pygame.font.SysFont(["Segoe UI", "Tahoma", "Arial"], int(cell_size * 0.38))
            
        self.tooltip_header_font = pygame.font.SysFont(["Segoe UI", "Tahoma", "Arial"], int(cell_size * 0.28), bold=True)
        self.tooltip_body_font = pygame.font.SysFont(["Segoe UI", "Tahoma", "Arial"], int(cell_size * 0.24))

        self.tooltip_cache = {}
        self.cache_tooltips()
        
        # Regenerate cached procedural textures for new dimensions
        self.board_textures = {}
        self.generate_and_cache_board_textures()

    def detect_chinese_font(self):
        chinese_fonts = ['microsoftyahei', 'simhei', 'simsun', 'msgothic', 'dengxian', 'arialunicode']
        for f in chinese_fonts:
            if pygame.font.match_font(f):
                return f
        return None

    def get_xy(self, r, c):
        x = self.offset_x + c * self.cell_size
        y = self.offset_y + r * self.cell_size
        return x, y

    def generate_and_cache_board_textures(self):
        for theme_name, theme_data in THEMES.items():
            surf = pygame.Surface((self.board_width, self.board_height))
            bg_base = theme_data["bg_base"]
            surf.fill(bg_base)
            
            # Procedural effects
            if theme_name == "classic_wood":
                # Draw warm rosewood grain
                for y in range(0, self.board_height, 2):
                    # Base color modulation using sine waves
                    wave = math.sin(y * 0.03) * 6 + math.cos(y * 0.005) * 3
                    r = max(0, min(255, bg_base[0] + int(wave)))
                    g = max(0, min(255, bg_base[1] + int(wave * 0.8)))
                    b = max(0, min(255, bg_base[2] + int(wave * 0.5)))
                    pygame.draw.line(surf, (r, g, b), (0, y), (self.board_width, y))
                    pygame.draw.line(surf, (r, g, b), (0, y + 1), (self.board_width, y + 1))
                # Add light noise dots
                for _ in range(3000):
                    nx = random.randint(0, self.board_width - 1)
                    ny = random.randint(0, self.board_height - 1)
                    val = random.randint(-8, 8)
                    r = max(0, min(255, bg_base[0] + val))
                    g = max(0, min(255, bg_base[1] + val))
                    b = max(0, min(255, bg_base[2] + val))
                    surf.set_at((nx, ny), (r, g, b))
                    
            elif theme_name == "white_marble":
                # Light marble veins
                random.seed(123) # Seeded to look consistent
                for _ in range(8):
                    # Draw a jagged marble vein path
                    sx = random.randint(0, self.board_width)
                    sy = random.randint(0, self.board_height)
                    for _ in range(12):
                        ex = sx + random.randint(-40, 40)
                        ey = sy + random.randint(10, 60)
                        ex = max(0, min(self.board_width, ex))
                        ey = max(0, min(self.board_height, ey))
                        # Grey vein
                        pygame.draw.line(surf, (200, 200, 202), (sx, sy), (ex, ey), random.randint(2, 4))
                        pygame.draw.line(surf, (220, 220, 222), (sx, sy), (ex, ey), 1)
                        sx, sy = ex, ey
                random.seed()
                
            elif theme_name == "dark_glass":
                # Dark sleek grid/ambient backdrop
                for y in range(self.board_height):
                    # Vertical gradient
                    ratio = y / self.board_height
                    r = int(bg_base[0] + (30 - bg_base[0]) * ratio)
                    g = int(bg_base[1] + (35 - bg_base[1]) * ratio)
                    b = int(bg_base[2] + (45 - bg_base[2]) * ratio)
                    pygame.draw.line(surf, (r, g, b), (0, y), (self.board_width, y))
                    
                # Glowing blue ambient overlay edges
                glow = pygame.Surface((self.board_width, self.board_height), pygame.SRCALPHA)
                pygame.draw.rect(glow, (0, 165, 230, 25), (0, 0, self.board_width, self.board_height), 12)
                surf.blit(glow, (0, 0))
                
            self.board_textures[theme_name] = surf

    def draw_board(self, surface, theme="classic_wood"):
        theme_data = THEMES.get(theme, THEMES["classic_wood"])
        line_color = theme_data["line_color"]
        palace_color = theme_data["palace_color"]
        
        # For non-classic themes with image assets, draw the image and return
        if theme != "classic_wood":
            asset_map = {
                "white_marble": "board_marble",
                "dark_glass": "board_glass"
            }
            asset_name = asset_map.get(theme)
            img = get_asset(asset_name) if asset_name else None
            if img:
                scaled = pygame.transform.smoothscale(img, (self.board_width, self.board_height))
                surface.blit(scaled, (0, 0))
            elif theme in self.board_textures:
                surface.blit(self.board_textures[theme], (0, 0))
            else:
                surface.fill(theme_data["bg_base"])
            return
            
        # --- Classic wood: use procedural texture + grid lines ---
        if theme in self.board_textures:
            surface.blit(self.board_textures[theme], (0, 0))
        else:
            surface.fill(theme_data["bg_base"])
            
        # Draw Outer Double Border
        border_rect = pygame.Rect(
            self.offset_x - 10, self.offset_y - 10,
            8 * self.cell_size + 20, 9 * self.cell_size + 20
        )
        pygame.draw.rect(surface, line_color, border_rect, 2)
        inner_border_rect = border_rect.inflate(-4, -4)
        pygame.draw.rect(surface, line_color, inner_border_rect, 1)
        
        # Draw horizontal lines (10 lines)
        for r in range(10):
            x1, y1 = self.get_xy(r, 0)
            x2, y2 = self.get_xy(r, 8)
            pygame.draw.line(surface, line_color, (x1, y1), (x2, y2), 1)
            
        # Draw vertical lines (9 lines, broken at the River)
        for c in range(9):
            if c == 0 or c == 8:
                x1, y1 = self.get_xy(0, c)
                x2, y2 = self.get_xy(9, c)
                pygame.draw.line(surface, line_color, (x1, y1), (x2, y2), 1)
            else:
                # Top half (rows 0-4)
                x1, y1 = self.get_xy(0, c)
                x2, y2 = self.get_xy(4, c)
                pygame.draw.line(surface, line_color, (x1, y1), (x2, y2), 1)
                # Bottom half (rows 5-9)
                x1, y1 = self.get_xy(5, c)
                x2, y2 = self.get_xy(9, c)
                pygame.draw.line(surface, line_color, (x1, y1), (x2, y2), 1)

        # Draw Dashed Palace diagonals
        palace_segments = [
            ((0, 3), (2, 5)), ((0, 5), (2, 3)), # Top
            ((7, 3), (9, 5)), ((7, 5), (9, 3))  # Bottom
        ]
        for p1, p2 in palace_segments:
            start_xy = self.get_xy(p1[0], p1[1])
            end_xy = self.get_xy(p2[0], p2[1])
            self.draw_dashed_line(surface, palace_color, start_xy, end_xy, width=1, dash_length=6, space_length=4)
            
        # River text
        if self.chinese_supported:
            river_lbl1 = self.label_font.render("楚 河", True, line_color)
            river_lbl2 = self.label_font.render("漢 界", True, line_color)
        else:
            river_lbl1 = self.label_font.render("楚 河 (SO RIVER)", True, line_color)
            river_lbl2 = self.label_font.render("漢 界 (HAN BORDER)", True, line_color)
            
        rx1 = self.offset_x + 2 * self.cell_size - river_lbl1.get_width() // 2
        rx2 = self.offset_x + 6 * self.cell_size - river_lbl2.get_width() // 2
        ry = self.offset_y + 4 * self.cell_size + self.cell_size // 2 - river_lbl1.get_height() // 2
        surface.blit(river_lbl1, (rx1, ry))
        surface.blit(river_lbl2, (rx2, ry))
        
        # Draw cross markers
        cross_positions = [
            (2, 1), (2, 7), (7, 1), (7, 7),
            (3, 0), (3, 2), (3, 4), (3, 6), (3, 8),
            (6, 0), (6, 2), (6, 4), (6, 6), (6, 8)
        ]
        for r, c in cross_positions:
            self.draw_cross(surface, r, c, line_color)

    def draw_dashed_line(self, surface, color, start_pos, end_pos, width=1, dash_length=4, space_length=4):
        x1, y1 = start_pos
        x2, y2 = end_pos
        dl = math.hypot(x2 - x1, y2 - y1)
        if dl == 0: return
        dx = (x2 - x1) / dl
        dy = (y2 - y1) / dl
        accum = 0.0
        while accum < dl:
            seg_end = min(accum + dash_length, dl)
            sx = int(x1 + dx * accum)
            sy = int(y1 + dy * accum)
            ex = int(x1 + dx * seg_end)
            ey = int(y1 + dy * seg_end)
            pygame.draw.line(surface, color, (sx, sy), (ex, ey), width)
            accum += dash_length + space_length

    def draw_cross(self, surface, r, c, line_color):
        cx, cy = self.get_xy(r, c)
        size = 8
        gap = 3
        
        # Small filled diamond at center intersection
        pygame.draw.polygon(surface, line_color, [
            (cx - 3, cy),
            (cx, cy - 3),
            (cx + 3, cy),
            (cx, cy + 3)
        ])
        
        if c > 0:
            pygame.draw.line(surface, line_color, (cx - gap, cy - gap), (cx - gap - size, cy - gap), 1)
            pygame.draw.line(surface, line_color, (cx - gap, cy - gap), (cx - gap, cy - gap - size), 1)
            pygame.draw.line(surface, line_color, (cx - gap, cy + gap), (cx - gap - size, cy + gap), 1)
            pygame.draw.line(surface, line_color, (cx - gap, cy + gap), (cx - gap, cy + gap + size), 1)
        if c < 8:
            pygame.draw.line(surface, line_color, (cx + gap, cy - gap), (cx + gap + size, cy - gap), 1)
            pygame.draw.line(surface, line_color, (cx + gap, cy - gap), (cx + gap, cy - gap - size), 1)
            pygame.draw.line(surface, line_color, (cx + gap, cy + gap), (cx + gap + size, cy + gap), 1)
            pygame.draw.line(surface, line_color, (cx + gap, cy + gap), (cx + gap, cy + gap + size), 1)

    def draw_piece(self, surface, piece, is_selected=False, skin="classic_wood_piece", cx=None, cy=None):
        if cx is None or cy is None:
            r, c = piece.pos
            cx, cy = self.get_xy(r, c)
        
        # Piece radius base
        radius = int(self.cell_size * 0.44)
        if is_selected:
            radius += 2 # Scale up visual effect
            
        skin_data = PIECE_SKINS.get(skin, PIECE_SKINS["classic_wood_piece"])
        
        # 1. Draw Drop Shadow (Realistic ambient occlusion)
        shadow_surf = pygame.Surface((radius * 2 + 10, radius * 2 + 10), pygame.SRCALPHA)
        shadow_offset = 3 if is_selected else 2
        shadow_alpha = 90 if is_selected else 60
        pygame.draw.circle(shadow_surf, (0, 0, 0, shadow_alpha), (radius + shadow_offset, radius + shadow_offset), radius)
        surface.blit(shadow_surf, (cx - radius - shadow_offset, cy - radius - shadow_offset))
        
        # 2. Draw Outer Bevel Outline
        pygame.draw.circle(surface, skin_data["border"], (cx, cy), radius)
        
        # 3. Concentric Shading for 3D Bevel (Radial Gradient Illusion)
        edge_col = skin_data["edge"]
        high_col = skin_data["highlight"]
        shading_radius = radius - 2
        
        # Draw nested circles offset towards top-left to simulate light reflection
        for i in range(shading_radius):
            ratio = i / max(1, shading_radius)
            # Offset center slightly up-left
            ox = int(cx - (1.0 - ratio) * (3.5 if is_selected else 2.5))
            oy = int(cy - (1.0 - ratio) * (3.5 if is_selected else 2.5))
            
            # Linearly interpolate color
            cr = int(edge_col[0] + (high_col[0] - edge_col[0]) * ratio)
            cg = int(edge_col[1] + (high_col[1] - edge_col[1]) * ratio)
            cb = int(edge_col[2] + (high_col[2] - edge_col[2]) * ratio)
            
            pygame.draw.circle(surface, (cr, cg, cb), (ox, oy), shading_radius - i)

        # 4. Text Character Render with Outline
        text_color = skin_data["red_text"] if piece.color == 'red' else skin_data["black_text"]
        outline_color = (0, 0, 0)
        
        if skin == "royal_jade":
            outline_color = (0, 45, 30)
        elif skin == "cyber_steel":
            outline_color = (20, 20, 25)
            
        if self.chinese_supported:
            char = piece.char
        else:
            char_map = {'G': 'G', 'A': 'A', 'E': 'E', 'R': 'R', 'C': 'C', 'H': 'H', 'P': 'P'}
            char = char_map.get(piece.name, '?')
            
        # Draw 1px character outline
        txt_outline = self.piece_font.render(char, True, outline_color)
        ox = cx - txt_outline.get_width() // 2
        oy = cy - txt_outline.get_height() // 2
        
        surface.blit(txt_outline, (ox - 1, oy))
        surface.blit(txt_outline, (ox + 1, oy))
        surface.blit(txt_outline, (ox, oy - 1))
        surface.blit(txt_outline, (ox, oy + 1))
        
        # Main text
        txt_main = self.piece_font.render(char, True, text_color)
        surface.blit(txt_main, (ox, oy))
        
        # Selected highlight glow ring
        if is_selected:
            # Gold glowing ring
            pygame.draw.circle(surface, (242, 202, 80), (cx, cy), radius + 2, 2)

    def draw_move_hints(self, surface, board, valid_destinations):
        for r, c in valid_destinations:
            cx, cy = self.get_xy(r, c)
            target = board.get_piece((r, c))
            if target:
                radius = int(self.cell_size * 0.44)
                pygame.draw.circle(surface, (231, 76, 60), (cx, cy), radius + 3, 3)
            else:
                # Premium double indicator dot
                pygame.draw.circle(surface, (30, 180, 80), (cx, cy), 6)
                pygame.draw.circle(surface, (30, 180, 80), (cx, cy), 12, 1)

    def draw_check_effect(self, surface, board):
        for color in ['red', 'black']:
            if board.is_in_check(color):
                g_pos = board.get_general_pos(color)
                if g_pos:
                    gx, gy = self.get_xy(g_pos[0], g_pos[1])
                    radius = int(self.cell_size * 0.44)
                    
                    # Pulsing neon red check circle
                    pulse = (math.sin(pygame.time.get_ticks() * 0.015) + 1) / 2
                    glow_color = (255, 50, 50)
                    glow_radius = radius + int(3 + 7 * pulse)
                    pygame.draw.circle(surface, glow_color, (gx, gy), glow_radius, 3)
                    
                    # Check warning banner at top
                    board_center_x = self.offset_x + 4 * self.cell_size
                    text_y = self.offset_y - 42
                    
                    check_text = "⚠️ CHIẾU TƯỚNG! ⚠️"
                    check_font = pygame.font.SysFont(["Segoe UI", "Tahoma", "Arial"], 20, bold=True)
                    txt = check_font.render(check_text, True, (255, 60, 60))
                    
                    # Draw a solid wood-tinted dark border panel
                    bg_rect = pygame.Rect(
                        board_center_x - txt.get_width() // 2 - 12,
                        text_y - 3,
                        txt.get_width() + 24,
                        txt.get_height() + 6
                    )
                    pygame.draw.rect(surface, (35, 20, 15), bg_rect, 0, 6)
                    pygame.draw.rect(surface, (255, 50, 50), bg_rect, 1, 6)
                    surface.blit(txt, (board_center_x - txt.get_width() // 2, text_y))

    def spawn_capture_particles(self, x, y, theme_name="classic_wood"):
        """Spawns 12 small particles flying away on capture"""
        # Determine particle colors based on theme
        colors = [(231, 76, 60), (218, 165, 32), (240, 240, 240)] # Default wood colors
        if theme_name == "white_marble":
            colors = [(160, 125, 45), (180, 150, 80), (240, 240, 240)]
        elif theme_name == "dark_glass":
            colors = [(0, 180, 255), (89, 222, 155), (255, 60, 60)]
            
        for _ in range(12):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2.0, 5.0)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 1.5 # slight initial upwards lift
            color = random.choice(colors)
            size = random.uniform(3.0, 6.0)
            life = 1.0 # decays to 0.0
            self.particles.append({
                "x": float(x),
                "y": float(y),
                "vx": vx,
                "vy": vy,
                "color": color,
                "size": size,
                "life": life,
                "alpha": 255
            })

    def update_particles(self):
        """Updates physics and lifetime of active particles"""
        alive_particles = []
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.15 # Gravity force downward
            p["life"] -= 0.035 # Decays speed
            if p["life"] > 0:
                p["alpha"] = max(0, int(p["life"] * 255))
                alive_particles.append(p)
        self.particles = alive_particles

    def draw_particles(self, surface):
        """Draws active particles with transparency onto screen"""
        for p in self.particles:
            size = int(p["size"])
            if size < 1: size = 1
            # Create a small alpha surface for soft particle draw
            psurf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(psurf, (p["color"][0], p["color"][1], p["color"][2], p["alpha"]), (size, size), size)
            surface.blit(psurf, (int(p["x"]) - size, int(p["y"]) - size))

    def get_board_pos_from_screen(self, mouse_pos):
        mx, my = mouse_pos
        for r in range(10):
            for c in range(9):
                cx, cy = self.get_xy(r, c)
                dist = math.sqrt((mx - cx)**2 + (my - cy)**2)
                if dist < self.cell_size * 0.45:
                    return r, c
        return None

    def cache_tooltips(self):
        for name, desc in PIECE_DESCRIPTIONS.items():
            header_surface = self.tooltip_header_font.render(desc['name'], True, (242, 202, 80))
            max_w = header_surface.get_width()
            
            rule_surfaces = []
            for rule in desc['rules']:
                surf = self.tooltip_body_font.render(rule, True, (230, 230, 230))
                rule_surfaces.append(surf)
                max_w = max(max_w, surf.get_width())
                
            padding = 12
            box_w = max_w + padding * 2
            box_h = header_surface.get_height() + len(rule_surfaces) * 16 + padding * 2 + 8
            
            tooltip_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
            tooltip_surf.fill((20, 12, 10, 220))
            pygame.draw.rect(tooltip_surf, (242, 202, 80), (0, 0, box_w, box_h), 2, 4)
            
            tooltip_surf.blit(header_surface, (padding, padding))
            sep_y = padding + header_surface.get_height() + 4
            pygame.draw.line(tooltip_surf, (100, 100, 100, 150), (padding, sep_y), (box_w - padding, sep_y), 1)
            
            curr_y = sep_y + 6
            for surf in rule_surfaces:
                tooltip_surf.blit(surf, (padding, curr_y))
                curr_y += 16
                
            self.tooltip_cache[name] = {
                "surface": tooltip_surf,
                "width": box_w,
                "height": box_h
            }

    def draw_tooltip(self, surface, piece, mouse_pos):
        cached = self.tooltip_cache.get(piece.name)
        if not cached: return
        box_w = cached["width"]
        box_h = cached["height"]
        tooltip_surf = cached["surface"]
        
        tx = mouse_pos[0] + 15
        ty = mouse_pos[1] + 15
        
        if tx + box_w > 1100: # Total width is 1100
            tx = mouse_pos[0] - box_w - 15
        if ty + box_h > 820: # Total height is 820
            ty = mouse_pos[1] - box_h - 15
            
        if tx < 0: tx = 10
        if ty < 0: ty = 10
        surface.blit(tooltip_surf, (tx, ty))
