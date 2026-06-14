# Pygame Start Menu screen for Xiangqi AI Game
# pyrefly: ignore [missing-import]
import pygame

COLOR_WOOD_BG = (235, 195, 135)
COLOR_PANEL_BG = (30, 30, 30)
COLOR_ACCENT = (0, 173, 181)
COLOR_TEXT = (240, 240, 240)
COLOR_TEXT_MUTED = (150, 150, 150)
COLOR_BTN = (46, 204, 113)

# 18 AI algorithms lists grouped into 6 levels
LEVEL_DETAILS = {
    0: ("Level 1: BFS/DFS/UCS", "Tìm kiếm mù. UCS tối ưu hóa ăn quân lớn."),
    1: ("Level 2: Greedy/A*/IDA*", "Heuristic đánh giá tổng lực đối thủ còn lại."),
    2: ("Level 3: Hill Climbing/SA/Beam", "Tìm kiếm cục bộ. SA chấp nhận nước đi ngẫu nhiên."),
    3: ("Level 4: Online/AND-OR/Belief", "Đối phó sự cố, lập kế hoạch AND-OR."),
    4: ("Level 5: CSP (MRV/Min-Conflicts)", "Thỏa mãn ràng buộc, né ô nguy hiểm, bảo vệ tướng."),
    5: ("Level 6: Minimax/Alpha-Beta", "Đối kháng sâu 4-6 nước, tối ưu hóa cắt tỉa.")
}

class StartMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.title_font = pygame.font.SysFont("segoe ui, tahoma, arial", 36, bold=True)
        self.header_font = pygame.font.SysFont("segoe ui, tahoma, arial", 20, bold=True)
        self.body_font = pygame.font.SysFont("segoe ui, tahoma, arial", 15)
        self.detail_font = pygame.font.SysFont("segoe ui, tahoma, arial", 13)
        
        self.game_mode = "human_vs_bot" # human_vs_bot, bot_vs_bot
        
        # Level selection indices (0 to 5)
        self.red_bot_level = 5 # Default Level 6 (Alpha-Beta)
        self.black_bot_level = 5 # Default Level 6 (Alpha-Beta)
        
        # Define layout boxes for click checks
        self.mode_boxes = {
            "human_vs_bot": pygame.Rect(width // 2 - 220, 160, 200, 45),
            "bot_vs_bot": pygame.Rect(width // 2 + 20, 160, 200, 45)
        }
        
        # Level boxes (represented vertically/horizontally)
        # Red Bot Levels (Bot vs Bot)
        self.red_level_rects = []
        for i in range(6):
            self.red_level_rects.append(pygame.Rect(width // 2 - 260, 270 + i * 50, 240, 40))
            
        # Black Bot Levels
        self.black_level_rects = []
        for i in range(6):
            self.black_level_rects.append(pygame.Rect(width // 2 + 20, 270 + i * 50, 240, 40))
            
        self.btn_start = pygame.Rect(width // 2 - 120, 600, 240, 50)

    def handle_event(self, event):
        """Returns True if 'start_game' button is clicked and starts the game loop"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = event.pos
                
                # Check mode change clicks
                for mode_id, rect in self.mode_boxes.items():
                    if rect.collidepoint(pos):
                        self.game_mode = mode_id
                        
                # Check Level clicks
                if self.game_mode == "bot_vs_bot":
                    for i, rect in enumerate(self.red_level_rects):
                        if rect.collidepoint(pos):
                            self.red_bot_level = i
                            
                for i, rect in enumerate(self.black_level_rects):
                    if rect.collidepoint(pos):
                        self.black_bot_level = i
                        
                # Check Start Game click
                if self.btn_start.collidepoint(pos):
                    return True
        return False

    def draw(self, surface):
        # Fill wooden background
        surface.fill(COLOR_WOOD_BG)
        
        # Transparent overlay panel
        panel = pygame.Surface((self.width - 100, self.height - 80), pygame.SRCALPHA)
        panel.fill((20, 20, 20, 230)) # Black translucent overlay
        surface.blit(panel, (50, 40))
        
        # 1. Main Header Title
        title_txt = self.title_font.render("CỜ TƯỚNG AI - XIANGQI BOT", True, COLOR_ACCENT)
        surface.blit(title_txt, (self.width // 2 - title_txt.get_width() // 2, 65))
        
        # 2. Draw Mode selection
        for mode_id, rect in self.mode_boxes.items():
            is_selected = (self.game_mode == mode_id)
            color = COLOR_ACCENT if is_selected else (60, 60, 60)
            pygame.draw.rect(surface, color, rect, 0, 6)
            
            lbl_str = "Người đấu Bot" if mode_id == "human_vs_bot" else "Bot đấu Bot"
            lbl = self.header_font.render(lbl_str, True, COLOR_TEXT if is_selected else COLOR_TEXT_MUTED)
            surface.blit(lbl, (rect.centerx - lbl.get_width() // 2, rect.centery - lbl.get_height() // 2))

        # 3. Draw Level Selection Headers
        if self.game_mode == "human_vs_bot":
            # Just show one panel for Bot opponent
            bot_hdr = self.header_font.render("CHỌN CẤP ĐỘ BOT ĐỐI THỦ", True, COLOR_TEXT)
            surface.blit(bot_hdr, (self.width // 2 - bot_hdr.get_width() // 2, 230))
            
            # Highlight Black levels panel (center-aligned or expanded)
            for i, rect in enumerate(self.black_level_rects):
                # Reposition black level boxes to center for a better aesthetic in single bot selector
                centered_rect = pygame.Rect(self.width // 2 - 200, 270 + i * 50, 400, 42)
                is_sel = (self.black_bot_level == i)
                bg_color = (40, 40, 40) if is_sel else (25, 25, 25)
                border_color = COLOR_ACCENT if is_sel else (50, 50, 50)
                
                pygame.draw.rect(surface, bg_color, centered_rect, 0, 5)
                pygame.draw.rect(surface, border_color, centered_rect, 1, 5)
                
                # Title
                lvl_title, lvl_desc = LEVEL_DETAILS[i]
                t_lbl = self.body_font.render(lvl_title, True, COLOR_TEXT if is_sel else COLOR_TEXT_MUTED)
                surface.blit(t_lbl, (centered_rect.x + 15, centered_rect.y + 4))
                
                d_lbl = self.detail_font.render(lvl_desc, True, COLOR_ACCENT if is_sel else COLOR_TEXT_MUTED)
                surface.blit(d_lbl, (centered_rect.x + 15, centered_rect.y + 22))
        else:
            # Bot vs Bot showing both selectors
            bot1_hdr = self.header_font.render("CHỌN CẤP BOT ĐỎ (RED)", True, (231, 76, 60))
            surface.blit(bot1_hdr, (self.width // 2 - 260, 230))
            
            bot2_hdr = self.header_font.render("CHỌN CẤP BOT ĐEN (BLACK)", True, (241, 196, 15))
            surface.blit(bot2_hdr, (self.width // 2 + 20, 230))
            
            # Draw Red levels
            for i, rect in enumerate(self.red_level_rects):
                is_sel = (self.red_bot_level == i)
                bg_color = (40, 40, 40) if is_sel else (25, 25, 25)
                border_color = (231, 76, 60) if is_sel else (50, 50, 50)
                
                pygame.draw.rect(surface, bg_color, rect, 0, 5)
                pygame.draw.rect(surface, border_color, rect, 1, 5)
                
                lvl_title, lvl_desc = LEVEL_DETAILS[i]
                t_lbl = self.body_font.render(lvl_title.split(":")[0] + " Bot", True, COLOR_TEXT if is_sel else COLOR_TEXT_MUTED)
                surface.blit(t_lbl, (rect.x + 10, rect.y + 4))
                d_lbl = self.detail_font.render(lvl_title.split(":")[-1].strip(), True, COLOR_TEXT_MUTED)
                surface.blit(d_lbl, (rect.x + 10, rect.y + 22))
                
            # Draw Black levels
            for i, rect in enumerate(self.black_level_rects):
                is_sel = (self.black_bot_level == i)
                bg_color = (40, 40, 40) if is_sel else (25, 25, 25)
                border_color = (241, 196, 15) if is_sel else (50, 50, 50)
                
                pygame.draw.rect(surface, bg_color, rect, 0, 5)
                pygame.draw.rect(surface, border_color, rect, 1, 5)
                
                lvl_title, lvl_desc = LEVEL_DETAILS[i]
                t_lbl = self.body_font.render(lvl_title.split(":")[0] + " Bot", True, COLOR_TEXT if is_sel else COLOR_TEXT_MUTED)
                surface.blit(t_lbl, (rect.x + 10, rect.y + 4))
                d_lbl = self.detail_font.render(lvl_title.split(":")[-1].strip(), True, COLOR_TEXT_MUTED)
                surface.blit(d_lbl, (rect.x + 10, rect.y + 22))

        # 4. Big Start Game Button
        pygame.draw.rect(surface, COLOR_BTN, self.btn_start, 0, 8)
        start_lbl = self.header_font.render("BẮT ĐẦU CHƠI", True, (20, 20, 20))
        surface.blit(start_lbl, (self.btn_start.centerx - start_lbl.get_width() // 2, self.btn_start.centery - start_lbl.get_height() // 2))
