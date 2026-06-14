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

ALGORITHMS = {
    0: [
        {"name": "BFS", "desc": "Duyệt theo chiều rộng (Tìm kiếm mù)", "reg_key": "BFS"},
        {"name": "DFS", "desc": "Duyệt theo chiều sâu (Tìm kiếm mù)", "reg_key": "DFS"},
        {"name": "UCS", "desc": "Tìm kiếm chi phí đồng nhất (Tối ưu ăn quân)", "reg_key": "UCS"}
    ],
    1: [
        {"name": "Greedy", "desc": "Ăn quân giá trị cao nhất lập tức", "reg_key": "Greedy"},
        {"name": "A*", "desc": "Kết hợp chi phí thực + ước lượng heuristic", "reg_key": "A*"},
        {"name": "IDA*", "desc": "Thuật toán A* giới hạn độ sâu tiết kiệm bộ nhớ", "reg_key": "IDA*"}
    ],
    2: [
        {"name": "Hill Climbing", "desc": "Leo đồi tìm kiếm nước đi cục bộ tốt nhất", "reg_key": "Hill Climbing"},
        {"name": "Simulated Annealing", "desc": "Chấp nhận nước đi tệ ngẫu nhiên để thoát cực trị", "reg_key": "Simulated Annealing"},
        {"name": "Beam Search", "desc": "Duy trì chùm k trạng thái tốt nhất", "reg_key": "Beam Search"}
    ],
    3: [
        {"name": "Online Search", "desc": "Tính toán và cập nhật hành vi real-time", "reg_key": "Online Search"},
        {"name": "AND-OR Search", "desc": "Lập kế hoạch dự phòng cho mọi phản ứng đối thủ", "reg_key": "AND-OR Search"},
        {"name": "Belief State", "desc": "Dự đoán tập trạng thái ý định của đối thủ", "reg_key": "Belief State"}
    ],
    4: [
        {"name": "Backtracking", "desc": "Quay lui thỏa mãn ràng buộc thông minh (CSP)", "reg_key": "Backtracking"},
        {"name": "Min-Conflicts", "desc": "Giải quyết xung đột để bảo vệ quân tướng", "reg_key": "Min-Conflicts"},
        {"name": "AC-3", "desc": "Lọc sớm các nước đi không hợp lệ trước khi tìm kiếm", "reg_key": "AC-3"}
    ],
    5: [
        {"name": "Minimax", "desc": "Tối đa hóa điểm số bản thân, tối thiểu hóa đối thủ", "reg_key": "Minimax"},
        {"name": "Alpha-Beta", "desc": "Minimax tối ưu cắt tỉa nhánh thừa (4-6 nước)", "reg_key": "Alpha-Beta"},
        {"name": "Expectimax", "desc": "Đối kháng khi đối thủ có thể đi nước không hoàn hảo", "reg_key": "Expectimax"}
    ]
}

class StartMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.title_font = pygame.font.SysFont("segoe ui, tahoma, arial", 36, bold=True)
        self.header_font = pygame.font.SysFont("segoe ui, tahoma, arial", 20, bold=True)
        self.body_font = pygame.font.SysFont("segoe ui, tahoma, arial", 15, bold=True)
        self.detail_font = pygame.font.SysFont("segoe ui, tahoma, arial", 13)
        self.label_font = pygame.font.SysFont("segoe ui, tahoma, arial", 16, bold=True)
        
        # Menu Flow State
        # States: "mode_select", "level_red", "algo_red", "level_black", "algo_black"
        self.state = "mode_select"
        self.game_mode = "human_vs_bot" # human_vs_bot, bot_vs_bot
        
        self.red_bot_level = 0
        self.red_bot_algo = ""
        self.black_bot_level = 0
        self.black_bot_algo = ""
        
        # Transition alpha for fade effect
        self.transition_alpha = 255
        
        # Buttons definitions
        # Screen 1: Game Mode Select Buttons
        self.btn_mode_human = pygame.Rect(width // 2 - 200, 240, 400, 55)
        self.btn_mode_bot = pygame.Rect(width // 2 - 200, 320, 400, 55)
        
        # Screen 2: Level Select Buttons (Center vertically)
        self.level_rects = []
        for i in range(6):
            self.level_rects.append(pygame.Rect(width // 2 - 200, 180 + i * 55, 400, 46))
            
        # Screen 3: Algorithm Select Buttons (Center vertically)
        self.algo_rects = []
        for i in range(3):
            self.algo_rects.append(pygame.Rect(width // 2 - 250, 220 + i * 85, 500, 68))
            
        # Shared Navigation Back Button
        self.btn_back = pygame.Rect(width // 2 - 100, 540, 200, 40)
        self.btn_level_back = pygame.Rect(width // 2 - 100, 580, 200, 40)

    def trigger_transition(self):
        self.transition_alpha = 255

    def handle_event(self, event):
        """Returns True if configuration is complete and starts the game loop"""
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return False
            
        pos = event.pos
        
        # --- STATE: mode_select ---
        if self.state == "mode_select":
            if self.btn_mode_human.collidepoint(pos):
                self.game_mode = "human_vs_bot"
                self.red_bot_level = None
                self.red_bot_algo = None
                self.state = "level_black"
                self.trigger_transition()
            elif self.btn_mode_bot.collidepoint(pos):
                self.game_mode = "bot_vs_bot"
                self.state = "level_red"
                self.trigger_transition()
                
        # --- STATE: level_red ---
        elif self.state == "level_red":
            for i, rect in enumerate(self.level_rects):
                if rect.collidepoint(pos):
                    self.red_bot_level = i
                    self.state = "algo_red"
                    self.trigger_transition()
                    return False
            if self.btn_level_back.collidepoint(pos):
                self.state = "mode_select"
                self.trigger_transition()
                
        # --- STATE: algo_red ---
        elif self.state == "algo_red":
            for i, rect in enumerate(self.algo_rects):
                if rect.collidepoint(pos):
                    self.red_bot_algo = ALGORITHMS[self.red_bot_level][i]["reg_key"]
                    self.state = "level_black"
                    self.trigger_transition()
                    return False
            if self.btn_back.collidepoint(pos):
                self.state = "level_red"
                self.trigger_transition()
                
        # --- STATE: level_black ---
        elif self.state == "level_black":
            for i, rect in enumerate(self.level_rects):
                if rect.collidepoint(pos):
                    self.black_bot_level = i
                    self.state = "algo_black"
                    self.trigger_transition()
                    return False
            if self.btn_level_back.collidepoint(pos):
                if self.game_mode == "human_vs_bot":
                    self.state = "mode_select"
                else:
                    self.state = "algo_red"
                self.trigger_transition()
                
        # --- STATE: algo_black ---
        elif self.state == "algo_black":
            for i, rect in enumerate(self.algo_rects):
                if rect.collidepoint(pos):
                    self.black_bot_algo = ALGORITHMS[self.black_bot_level][i]["reg_key"]
                    # Configuration complete, launch game!
                    self.state = "mode_select" # reset menu state for next launch
                    return True
            if self.btn_back.collidepoint(pos):
                self.state = "level_black"
                self.trigger_transition()
                
        return False

    def draw(self, surface):
        # 1. Fill wooden background
        surface.fill(COLOR_WOOD_BG)
        
        # Transparent overlay panel
        panel = pygame.Surface((self.width - 100, self.height - 80), pygame.SRCALPHA)
        panel.fill((20, 20, 20, 230)) # Black translucent overlay
        surface.blit(panel, (50, 40))
        
        # Main Title Header
        title_txt = self.title_font.render("CỜ TƯỚNG AI - XIANGQI BOT", True, COLOR_ACCENT)
        surface.blit(title_txt, (self.width // 2 - title_txt.get_width() // 2, 65))
        
        # 2. Render content based on current State
        # --- STATE: mode_select ---
        if self.state == "mode_select":
            # Subtitle
            sub_lbl = self.header_font.render("CHỌN CHẾ ĐỘ CHƠI", True, COLOR_TEXT)
            surface.blit(sub_lbl, (self.width // 2 - sub_lbl.get_width() // 2, 160))
            
            # Button 1: Human vs Bot
            pygame.draw.rect(surface, COLOR_ACCENT, self.btn_mode_human, 0, 6)
            lbl1 = self.header_font.render("NGƯỜI ĐẤU BOT", True, (20, 20, 20))
            surface.blit(lbl1, (self.btn_mode_human.centerx - lbl1.get_width() // 2, self.btn_mode_human.centery - lbl1.get_height() // 2))
            
            # Button 2: Bot vs Bot
            pygame.draw.rect(surface, (60, 60, 60), self.btn_mode_bot, 0, 6)
            pygame.draw.rect(surface, COLOR_ACCENT, self.btn_mode_bot, 1, 6)
            lbl2 = self.header_font.render("BOT ĐẤU BOT", True, COLOR_TEXT)
            surface.blit(lbl2, (self.btn_mode_bot.centerx - lbl2.get_width() // 2, self.btn_mode_bot.centery - lbl2.get_height() // 2))
            
        # --- STATE: level_red / level_black ---
        elif self.state in ["level_red", "level_black"]:
            # Custom title based on active side
            if self.state == "level_red":
                sub_title = "BÊN ĐỎ (RED) - CHỌN CẤP ĐỘ BOT"
                title_color = (231, 76, 60)
            else:
                if self.game_mode == "human_vs_bot":
                    sub_title = "CHỌN CẤP ĐỘ BOT ĐỐI THỦ"
                    title_color = COLOR_ACCENT
                else:
                    sub_title = "BÊN ĐEN (BLACK) - CHỌN CẤP ĐỘ BOT"
                    title_color = (241, 196, 15)
                    
            sub_lbl = self.header_font.render(sub_title, True, title_color)
            surface.blit(sub_lbl, (self.width // 2 - sub_lbl.get_width() // 2, 130))
            
            # Draw 6 levels list
            for i, rect in enumerate(self.level_rects):
                bg_color = (35, 35, 35)
                border_color = (80, 80, 80)
                
                # Highlight on hover (optional, but keep design simple)
                pygame.draw.rect(surface, bg_color, rect, 0, 5)
                pygame.draw.rect(surface, border_color, rect, 1, 5)
                
                lvl_title, lvl_desc = LEVEL_DETAILS[i]
                t_lbl = self.body_font.render(lvl_title, True, COLOR_TEXT)
                surface.blit(t_lbl, (rect.x + 15, rect.y + 4))
                
                d_lbl = self.detail_font.render(lvl_desc, True, COLOR_TEXT_MUTED)
                surface.blit(d_lbl, (rect.x + 15, rect.y + 24))
                
            # Draw Back Button
            pygame.draw.rect(surface, (192, 57, 43), self.btn_level_back, 0, 5)
            back_lbl = self.body_font.render("QUAY LẠI", True, COLOR_TEXT)
            surface.blit(back_lbl, (self.btn_level_back.centerx - back_lbl.get_width() // 2, self.btn_level_back.centery - back_lbl.get_height() // 2))

        # --- STATE: algo_red / algo_black ---
        elif self.state in ["algo_red", "algo_black"]:
            # Custom title based on active side
            if self.state == "algo_red":
                sub_title = "BÊN ĐỎ (RED) - CHỌN THUẬT TOÁN BOT"
                title_color = (231, 76, 60)
                active_level = self.red_bot_level
            else:
                if self.game_mode == "human_vs_bot":
                    sub_title = "CHỌN THUẬT TOÁN CHO BOT"
                    title_color = COLOR_ACCENT
                else:
                    sub_title = "BÊN ĐEN (BLACK) - CHỌN THUẬT TOÁN BOT"
                    title_color = (241, 196, 15)
                active_level = self.black_bot_level
                
            sub_lbl = self.header_font.render(sub_title, True, title_color)
            surface.blit(sub_lbl, (self.width // 2 - sub_lbl.get_width() // 2, 130))
            
            # Sub-desc showing chosen level
            level_info = f"(Đang cấu hình thuật toán cho {LEVEL_DETAILS[active_level][0].split(':')[0]})"
            info_lbl = self.detail_font.render(level_info, True, COLOR_TEXT_MUTED)
            surface.blit(info_lbl, (self.width // 2 - info_lbl.get_width() // 2, 165))
            
            # Draw 3 algorithms buttons
            algos_list = ALGORITHMS[active_level]
            for i, rect in enumerate(self.algo_rects):
                bg_color = (40, 40, 40)
                border_color = COLOR_ACCENT
                
                pygame.draw.rect(surface, bg_color, rect, 0, 6)
                pygame.draw.rect(surface, border_color, rect, 1, 6)
                
                # Algorithm Name
                algo_name = algos_list[i]["name"]
                name_lbl = self.header_font.render(algo_name, True, COLOR_TEXT)
                surface.blit(name_lbl, (rect.x + 20, rect.y + 10))
                
                # Algorithm Description
                algo_desc = algos_list[i]["desc"]
                desc_lbl = self.detail_font.render(algo_desc, True, COLOR_TEXT_MUTED)
                surface.blit(desc_lbl, (rect.x + 20, rect.y + 38))
                
            # Draw Back Button
            pygame.draw.rect(surface, (192, 57, 43), self.btn_back, 0, 5)
            back_lbl = self.body_font.render("QUAY LẠI", True, COLOR_TEXT)
            surface.blit(back_lbl, (self.btn_back.centerx - back_lbl.get_width() // 2, self.btn_back.centery - back_lbl.get_height() // 2))

        # 3. Draw smooth screen transition overlay
        if self.transition_alpha > 0:
            trans_surface = pygame.Surface((self.width, self.height))
            trans_surface.fill((20, 20, 20))
            trans_surface.set_alpha(self.transition_alpha)
            surface.blit(trans_surface, (0, 0))
            self.transition_alpha = max(0, self.transition_alpha - 25) # Smoothly fade out overlay
