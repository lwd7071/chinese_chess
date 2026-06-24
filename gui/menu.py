# Pygame Start Menu screen for Xiangqi AI Game (Royal Theme Redesign)
import pygame
import math
import random
import time
from gui.assets import get_asset

# Color Palette constants
COLOR_WOOD_BG = (30, 16, 12)         # Rosewood base
COLOR_TEXT = (250, 220, 213)        # On-surface
COLOR_TEXT_MUTED = (180, 165, 150)  # Muted gold-grey
COLOR_GOLD = (242, 202, 80)         # Antique Gold
COLOR_OUTLINE = (77, 70, 53)        # Outline border
COLOR_CARD_BG = (42, 26, 22)        # Translucent container
COLOR_RED_TEXT = (231, 76, 60)      # Red side accent
COLOR_BLACK_TEXT = (241, 196, 15)   # Black side accent

LEVEL_DETAILS = {
    0: ("Level 1: BFS / DFS / UCS", "Tìm kiếm mù (Uninformed Search)."),
    1: ("Level 2: Greedy / A* / IDA*", "Tìm kiếm Heuristic (Informed Search)."),
    2: ("Level 3: Hill Climbing / SA / Beam", "Tìm kiếm cục bộ (Local Search)."),
    3: ("Level 4: Online / AND-OR / Belief", "Lập kế hoạch AND-OR & Belief State."),
    4: ("Level 5: CSP (MRV / Min-Conflicts)", "Bài toán thỏa mãn ràng buộc (CSP)."),
    5: ("Level 6: Minimax / Alpha-Beta", "Đối kháng Minimax & Alpha-Beta (Deep Search).")
}

LEVEL_DEFAULT_ALGOS = {
    0: "BFS",
    1: "A*",
    2: "Hill Climbing",
    3: "Online Search",
    4: "Min-Conflicts",
    5: "Alpha-Beta"
}

class StartMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Load fonts
        self.brand_font = pygame.font.SysFont(["Playfair Display", "Segoe UI", "Tahoma"], 46, bold=True)
        self.brand_sub_font = pygame.font.SysFont(["Source Serif 4", "Segoe UI", "Tahoma"], 18)
        self.title_font = pygame.font.SysFont(["Segoe UI", "Tahoma", "Arial"], 24, bold=True)
        self.header_font = pygame.font.SysFont(["Segoe UI", "Tahoma", "Arial"], 18, bold=True)
        self.body_font = pygame.font.SysFont(["Segoe UI", "Tahoma", "Arial"], 15, bold=True)
        self.detail_font = pygame.font.SysFont(["Segoe UI", "Tahoma", "Arial"], 13)
        self.footer_font = pygame.font.SysFont(["JetBrains Mono", "Consolas"], 12)
        
        # State Machine
        # States: "mode_select", "level_red", "level_black"
        self.state = "mode_select"
        self.game_mode = "human_vs_bot"
        
        self.red_bot_level = None
        self.red_bot_algo = ""
        self.black_bot_level = None
        self.black_bot_algo = ""
        
        self.transition_alpha = 255
        
        # Mode Select screen buttons (aligned right, 5 buttons vertical layout)
        btn_x = 620
        btn_w = 380
        btn_h = 52
        self.btn_mode_human = pygame.Rect(btn_x, 210, btn_w, btn_h)
        self.btn_mode_bot = pygame.Rect(btn_x, 275, btn_w, btn_h)
        self.btn_mode_online = pygame.Rect(btn_x, 340, btn_w, btn_h)
        self.btn_mode_shop = pygame.Rect(btn_x, 405, btn_w, btn_h)
        self.btn_mode_settings = pygame.Rect(btn_x, 470, btn_w, btn_h)
        
        # Temporary "Coming Soon" popup state
        self.popup_message = ""
        self.popup_timer = 0.0
        
        # Back button on level selection screens
        self.btn_level_back = pygame.Rect(40, 40, 110, 36)
        
        # 6 Level Cards Coordinates (arranged in 2 columns of 3 rows)
        self.level_rects = []
        card_w, card_h = 400, 90
        start_x1 = 130
        start_x2 = 570
        start_ys = [200, 305, 410]
        
        # Card 0: level 1, Card 1: level 2, etc.
        self.level_rects.append(pygame.Rect(start_x1, start_ys[0], card_w, card_h))
        self.level_rects.append(pygame.Rect(start_x2, start_ys[0], card_w, card_h))
        self.level_rects.append(pygame.Rect(start_x1, start_ys[1], card_w, card_h))
        self.level_rects.append(pygame.Rect(start_x2, start_ys[1], card_w, card_h))
        self.level_rects.append(pygame.Rect(start_x1, start_ys[2], card_w, card_h))
        self.level_rects.append(pygame.Rect(start_x2, start_ys[2], card_w, card_h))
        
        # Royal Seal button collision Rect (centered at bottom)
        self.seal_cx = width // 2
        self.seal_cy = 615
        self.seal_r = 55
        self.btn_seal = pygame.Rect(self.seal_cx - self.seal_r, self.seal_cy - self.seal_r, self.seal_r * 2, self.seal_r * 2)
        
        # Cache local wood grain procedural texture
        self.wood_texture = self.generate_wood_texture(width, height)

    def generate_wood_texture(self, width, height):
        surf = pygame.Surface((width, height))
        surf.fill(COLOR_WOOD_BG)
        for y in range(0, height, 2):
            wave = math.sin(y * 0.02) * 5 + math.sin(y * 0.1) * 2
            r = max(0, min(255, COLOR_WOOD_BG[0] + int(wave)))
            g = max(0, min(255, COLOR_WOOD_BG[1] + int(wave * 0.8)))
            b = max(0, min(255, COLOR_WOOD_BG[2] + int(wave * 0.5)))
            pygame.draw.line(surf, (r, g, b), (0, y), (width, y))
            pygame.draw.line(surf, (r, g, b), (0, y + 1), (width, y + 1))
            
        noise = pygame.Surface((width, height), pygame.SRCALPHA)
        for _ in range(int(width * height * 0.01)):
            nx = random.randint(0, width - 1)
            ny = random.randint(0, height - 1)
            alpha = random.randint(4, 9)
            val = random.randint(-12, 12)
            nr = max(0, min(255, COLOR_WOOD_BG[0] + val))
            ng = max(0, min(255, COLOR_WOOD_BG[1] + val))
            nb = max(0, min(255, COLOR_WOOD_BG[2] + val))
            noise.set_at((nx, ny), (nr, ng, nb, alpha))
            
        surf.blit(noise, (0, 0))
        return surf

    def update_layout(self, width, height):
        self.width = width
        self.height = height
        
        # Recalculate background texture
        self.wood_texture = self.generate_wood_texture(width, height)
        
        # Recalculate Mode Select screen buttons (aligned right)
        btn_x = self.width - 480
        btn_w = 380
        btn_h = 52
        self.btn_mode_human = pygame.Rect(btn_x, 210, btn_w, btn_h)
        self.btn_mode_bot = pygame.Rect(btn_x, 275, btn_w, btn_h)
        self.btn_mode_online = pygame.Rect(btn_x, 340, btn_w, btn_h)
        self.btn_mode_shop = pygame.Rect(btn_x, 405, btn_w, btn_h)
        self.btn_mode_settings = pygame.Rect(btn_x, 470, btn_w, btn_h)
        
        # Recalculate 6 Level Cards Coordinates (arranged in 2 columns of 3 rows, centered)
        self.level_rects = []
        card_w, card_h = 400, 90
        start_x1 = self.width // 2 - 420
        start_x2 = self.width // 2 + 20
        start_ys = [200, 305, 410]
        
        self.level_rects.append(pygame.Rect(start_x1, start_ys[0], card_w, card_h))
        self.level_rects.append(pygame.Rect(start_x2, start_ys[0], card_w, card_h))
        self.level_rects.append(pygame.Rect(start_x1, start_ys[1], card_w, card_h))
        self.level_rects.append(pygame.Rect(start_x2, start_ys[1], card_w, card_h))
        self.level_rects.append(pygame.Rect(start_x1, start_ys[2], card_w, card_h))
        self.level_rects.append(pygame.Rect(start_x2, start_ys[2], card_w, card_h))
        
        # Recalculate Royal Seal button collision Rect (centered at bottom)
        self.seal_cx = width // 2
        self.seal_cy = height - 205
        self.btn_seal = pygame.Rect(self.seal_cx - self.seal_r, self.seal_cy - self.seal_r, self.seal_r * 2, self.seal_r * 2)

    def trigger_transition(self):
        self.transition_alpha = 255

    def show_popup(self, message):
        self.popup_message = message
        self.popup_timer = time.time() + 2.0

    def handle_event(self, event):
        """Returns \"game\" to start, \"shop\" to redirect, or False/None"""
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return False
            
        pos = event.pos
        mouse_pos = pygame.mouse.get_pos()
        
        # --- STATE: mode_select ---
        if self.state == "mode_select":
            # Apply 8px hover translation shift for clicks too
            btn_human = self.btn_mode_human.copy()
            if btn_human.collidepoint(mouse_pos): btn_human.x += 8
            
            btn_bot = self.btn_mode_bot.copy()
            if btn_bot.collidepoint(mouse_pos): btn_bot.x += 8
            
            btn_online = self.btn_mode_online.copy()
            if btn_online.collidepoint(mouse_pos): btn_online.x += 8
            
            btn_shop = self.btn_mode_shop.copy()
            if btn_shop.collidepoint(mouse_pos): btn_shop.x += 8
            
            btn_settings = self.btn_mode_settings.copy()
            if btn_settings.collidepoint(mouse_pos): btn_settings.x += 8
            
            if btn_human.collidepoint(pos):
                self.game_mode = "human_vs_bot"
                self.red_bot_level = None
                self.red_bot_algo = "Human"
                self.state = "level_black"
                self.trigger_transition()
                return False
            elif btn_bot.collidepoint(pos):
                self.game_mode = "bot_vs_bot"
                self.red_bot_level = None
                self.red_bot_algo = ""
                self.state = "level_red"
                self.trigger_transition()
                return False
            elif btn_online.collidepoint(pos):
                self.show_popup("Thách Đấu Trực Tuyến sẽ sớm ra mắt!")
                from gui.sound import play_synth_sound
                play_synth_sound('move')
                return False
            elif btn_shop.collidepoint(pos):
                return "shop"
            elif btn_settings.collidepoint(pos):
                self.show_popup("Cài đặt hệ thống đang phát triển!")
                from gui.sound import play_synth_sound
                play_synth_sound('move')
                return False
                
        # --- STATE: level_red (RED selection grid) ---
        elif self.state == "level_red":
            # Check Level Card click
            for i, rect in enumerate(self.level_rects):
                if rect.collidepoint(pos):
                    # Toggle selection
                    if self.red_bot_level == i:
                        self.red_bot_level = None
                    else:
                        self.red_bot_level = i
                    from gui.sound import play_synth_sound
                    play_synth_sound('move')
                    return False
                    
            # Check Back Button
            if self.btn_level_back.collidepoint(pos):
                self.state = "mode_select"
                self.trigger_transition()
                return False
                
            # Check Royal Seal Button (Khai chiến - direct to level_black, no more intermediate popups!)
            if self.red_bot_level is not None and self.btn_seal.collidepoint(pos):
                # Set default algorithm for chosen red bot level
                self.red_bot_algo = LEVEL_DEFAULT_ALGOS[self.red_bot_level]
                self.state = "level_black"
                self.trigger_transition()
                from gui.sound import play_synth_sound
                play_synth_sound('check')
                return False
                
        # --- STATE: level_black (BLACK selection grid) ---
        elif self.state == "level_black":
            # Check Level Card click
            for i, rect in enumerate(self.level_rects):
                if rect.collidepoint(pos):
                    if self.black_bot_level == i:
                        self.black_bot_level = None
                    else:
                        self.black_bot_level = i
                    from gui.sound import play_synth_sound
                    play_synth_sound('move')
                    return False
                    
            # Check Back Button
            if self.btn_level_back.collidepoint(pos):
                if self.game_mode == "human_vs_bot":
                    self.state = "mode_select"
                else:
                    self.state = "level_red"
                self.trigger_transition()
                return False
                
            # Check Royal Seal Button (Khai chiến - starts game directly!)
            if self.black_bot_level is not None and self.btn_seal.collidepoint(pos):
                # Set default algorithm for chosen black bot level
                self.black_bot_algo = LEVEL_DEFAULT_ALGOS[self.black_bot_level]
                
                # Reset menu state for next menu launch
                self.state = "mode_select"
                from gui.sound import play_synth_sound
                play_synth_sound('check')
                return "game"
                    
        return False

    def draw(self, surface):
        # 1. Background image or wood texture
        bg_img = get_asset("mahogany_table")
        if bg_img:
            scaled = pygame.transform.smoothscale(bg_img, (self.width, self.height))
            surface.blit(scaled, (0, 0))
        else:
            surface.blit(self.wood_texture, (0, 0))
            
        # Dark ambient vignette overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for x in range(self.width):
            ratio = x / self.width
            alpha = int(180 + (65 * ratio))
            pygame.draw.line(overlay, (12, 6, 4, alpha), (x, 0), (x, self.height))
        surface.blit(overlay, (0, 0))
        
        mouse_pos = pygame.mouse.get_pos()
        
        # 2. Rendering based on State
        # --- STATE: mode_select ---
        if self.state == "mode_select":
            # LEFT SIDE: Brand Anchor
            title_x = 80
            # Shadow
            t_shadow = self.brand_font.render("Hoàng Gia Tượng Kỳ", True, (15, 8, 6))
            surface.blit(t_shadow, (title_x + 3, 273))
            
            t_main = self.brand_font.render("Hoàng Gia Tượng Kỳ", True, COLOR_GOLD)
            surface.blit(t_main, (title_x, 270))
            
            sub_lbl = self.brand_sub_font.render("Đỉnh Cao Trí Tuệ • Khí Chất Hoàng Gia", True, COLOR_TEXT_MUTED)
            surface.blit(sub_lbl, (title_x + 4, 335))
            
            # Divider decoration
            dec_y = 375
            pygame.draw.line(surface, COLOR_OUTLINE, (title_x, dec_y), (title_x + 320, dec_y), 1)
            pygame.draw.polygon(surface, COLOR_GOLD, [
                (title_x + 160 - 6, dec_y),
                (title_x + 160, dec_y - 3),
                (title_x + 160 + 6, dec_y),
                (title_x + 160, dec_y + 3)
            ])
            
            footer_txt = self.footer_font.render("Nhóm 1 - HCMUTE", True, (120, 110, 100))
            surface.blit(footer_txt, (title_x + 4, self.height - 60))
            
            # RIGHT SIDE: Buttons List (5 Buttons matching Stitch HTML mockup)
            buttons = [
                (self.btn_mode_human, "Người đấu Bot", "🤖"),
                (self.btn_mode_bot, "Bot đấu Bot", "💻"),
                (self.btn_mode_online, "Thách đấu Trực tuyến", "⚔️"),
                (self.btn_mode_shop, "Cửa tiệm", "🛒"),
                (self.btn_mode_settings, "Cài đặt", "⚙️")
            ]
            
            for rect, text, icon in buttons:
                is_hover = rect.collidepoint(mouse_pos)
                draw_rect = rect.copy()
                if is_hover:
                    draw_rect.x += 8
                    
                pygame.draw.rect(surface, COLOR_CARD_BG if is_hover else (35, 20, 16), draw_rect, 0, 8)
                pygame.draw.rect(surface, COLOR_GOLD if is_hover else COLOR_OUTLINE, draw_rect, 2 if is_hover else 1, 8)
                
                b_color = COLOR_GOLD if is_hover else COLOR_TEXT
                b_txt = self.header_font.render(text, True, b_color)
                surface.blit(b_txt, (draw_rect.x + 20, draw_rect.centery - b_txt.get_height() // 2))
                
                icon_font = pygame.font.SysFont("Segoe UI Symbol", 18)
                i_txt = icon_font.render(icon, True, b_color)
                surface.blit(i_txt, (draw_rect.right - 38, draw_rect.centery - i_txt.get_height() // 2))
                
        # --- STATE: level_red / level_black (Cấu Hình Trí Tuệ) ---
        elif self.state in ["level_red", "level_black"]:
            # Back Button (Aligned top left)
            is_hover_back = self.btn_level_back.collidepoint(mouse_pos)
            pygame.draw.rect(surface, (60, 40, 30) if is_hover_back else (35, 20, 16), self.btn_level_back, 0, 6)
            pygame.draw.rect(surface, COLOR_GOLD, self.btn_level_back, 1, 6)
            back_txt = self.body_font.render("QUAY LẠI", True, COLOR_GOLD)
            surface.blit(back_txt, (self.btn_level_back.centerx - back_txt.get_width() // 2, self.btn_level_back.centery - back_txt.get_height() // 2))
            
            # Draw Header Title (Centered)
            active_side_text = "BÊN ĐỎ (RED)" if self.state == "level_red" else "BÊN ĐEN (BLACK)"
            active_side_color = COLOR_RED_TEXT if self.state == "level_red" else COLOR_BLACK_TEXT
            
            # Gold shadow and title
            hdr_shadow = self.brand_font.render("Cấu Hình Trí Tuệ", True, (15, 8, 6))
            surface.blit(hdr_shadow, (self.width // 2 - hdr_shadow.get_width() // 2 + 2, 62))
            hdr_txt = self.brand_font.render("Cấu Hình Trí Tuệ", True, COLOR_GOLD)
            surface.blit(hdr_txt, (self.width // 2 - hdr_txt.get_width() // 2, 60))
            
            sub_lbl = self.brand_sub_font.render(f"Lựa chọn cấp độ thuật toán đối kháng cho {active_side_text}", True, COLOR_TEXT_MUTED)
            surface.blit(sub_lbl, (self.width // 2 - sub_lbl.get_width() // 2, 125))
            
            # Divider decoration
            dec_y = 155
            pygame.draw.line(surface, COLOR_OUTLINE, (self.width // 2 - 200, dec_y), (self.width // 2 + 200, dec_y), 1)
            pygame.draw.polygon(surface, active_side_color, [
                (self.width // 2 - 8, dec_y),
                (self.width // 2, dec_y - 4),
                (self.width // 2 + 8, dec_y),
                (self.width // 2, dec_y + 4)
            ])
            
            # Draw 6 Level cards
            selected_level = self.red_bot_level if self.state == "level_red" else self.black_bot_level
            
            for i, rect in enumerate(self.level_rects):
                is_hover = rect.collidepoint(mouse_pos)
                is_selected = selected_level == i
                is_dimmed = selected_level is not None and not is_selected
                
                # Card Background opacity card
                card_alpha = 100 if is_dimmed else (235 if is_selected else (190 if is_hover else 150))
                card_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                
                # Fill card body
                card_surface.fill((44, 28, 24, card_alpha))
                surface.blit(card_surface, (rect.x, rect.y))
                
                # Draw border
                border_color = COLOR_GOLD if is_selected else (COLOR_GOLD if is_hover else COLOR_OUTLINE)
                border_w = 2 if is_selected else 1
                pygame.draw.rect(surface, border_color, rect, border_w, 8)
                
                # Draw details text
                lvl_lbl_txt = f"CẤP ĐỘ {i + 1}"
                title_col = COLOR_GOLD if is_selected else (COLOR_TEXT if not is_dimmed else COLOR_TEXT_MUTED)
                desc_col = COLOR_TEXT_MUTED if not is_dimmed else (100, 90, 80)
                
                l_lbl = self.detail_font.render(lvl_lbl_txt, True, title_col)
                surface.blit(l_lbl, (rect.x + 20, rect.y + 12))
                
                algo_title, algo_desc = LEVEL_DETAILS[i]
                t_lbl = self.body_font.render(algo_title.split(":")[-1].strip(), True, title_col)
                surface.blit(t_lbl, (rect.x + 20, rect.y + 28))
                
                d_lbl = self.detail_font.render(algo_desc, True, desc_col)
                surface.blit(d_lbl, (rect.x + 20, rect.y + 54))
                
            # Draw Royal Seal Button (Khai Chiến / Bắt Đầu)
            is_hover_seal = self.btn_seal.collidepoint(mouse_pos) and selected_level is not None
            seal_active = selected_level is not None
            
            # Circle base shadow
            pygame.draw.circle(surface, (10, 5, 4, 150), (self.seal_cx + 3, self.seal_cy + 3), self.seal_r)
            
            # Inner circle base gradient
            r_outer = self.seal_r + (4 if is_hover_seal else 0)
            seal_color_outer = (139, 0, 0) if seal_active else (80, 80, 80)
            seal_color_inner = (180, 0, 0) if seal_active else (110, 110, 110)
            
            for r_val in range(r_outer, 0, -2):
                ratio = r_val / r_outer
                cr = int(seal_color_inner[0] + (seal_color_outer[0] - seal_color_inner[0]) * ratio)
                cg = int(seal_color_inner[1] + (seal_color_outer[1] - seal_color_inner[1]) * ratio)
                cb = int(seal_color_inner[2] + (seal_color_outer[2] - seal_color_inner[2]) * ratio)
                pygame.draw.circle(surface, (cr, cg, cb), (self.seal_cx, self.seal_cy), r_val)
                
            # Seal border
            seal_border_color = COLOR_GOLD if seal_active else (150, 150, 150)
            pygame.draw.circle(surface, seal_border_color, (self.seal_cx, self.seal_cy), r_outer, 2)
            
            # Text inside seal
            txt_start = self.body_font.render("BẮT ĐẦU", True, COLOR_GOLD if seal_active else (180, 180, 180))
            txt_khai = self.detail_font.render("Khai Chiến", True, (255, 193, 7) if seal_active else (160, 160, 160))
            
            surface.blit(txt_start, (self.seal_cx - txt_start.get_width() // 2, self.seal_cy - 12))
            surface.blit(txt_khai, (self.seal_cx - txt_khai.get_width() // 2, self.seal_cy + 10))

        # 3. Draw temporary popup notifications (Coming Soon banner)
        if time.time() < self.popup_timer:
            p_width = 360
            p_height = 80
            px = self.width // 2 - p_width // 2
            py = self.height // 2 - p_height // 2
            
            # Draw semi-transparent dark panel
            pygame.draw.rect(surface, (44, 28, 24), (px, py, p_width, p_height), 0, 10)
            pygame.draw.rect(surface, COLOR_GOLD, (px, py, p_width, p_height), 2, 10)
            
            # Text info
            p_txt = self.body_font.render(self.popup_message, True, COLOR_GOLD)
            surface.blit(p_txt, (self.width // 2 - p_txt.get_width() // 2, self.height // 2 - p_txt.get_height() // 2))

        # 4. Draw smooth transition overlay
        if self.transition_alpha > 0:
            trans = pygame.Surface((self.width, self.height))
            trans.fill((12, 6, 4))
            trans.set_alpha(self.transition_alpha)
            surface.blit(trans, (0, 0))
            self.transition_alpha = max(0, self.transition_alpha - 20)
