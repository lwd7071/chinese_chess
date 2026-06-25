# Pygame Settings Screen for Chinese Chess (Xiangqi Settings - Profile & History)
import pygame
import json
import os
import datetime
import math
import random

COLOR_BG = (30, 16, 12)             # Warm deep mahogany background (#1e100c)
COLOR_CARD_BG = (39, 24, 20)        # Surface-container-low (#271814)
COLOR_TEXT = (250, 220, 213)        # On-surface (#fadcd5)
COLOR_GOLD = (242, 202, 80)         # Antique Gold (#f2ca50)
COLOR_MUTED = (208, 197, 175)       # On-surface-variant (#d0c5af)
COLOR_OUTLINE = (77, 70, 53)        # Outline-variant (#4d4635)
COLOR_ACCENT = (89, 222, 155)       # Secondary green jade (#59de9b)
COLOR_RED = (231, 76, 60)           # Highlight red

class SettingsScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Fonts
        self.title_font = pygame.font.SysFont(["Playfair Display", "Segoe UI", "Tahoma"], 32, bold=True)
        self.tab_font = pygame.font.SysFont(["Segoe UI", "Tahoma"], 14, bold=True)
        self.label_font = pygame.font.SysFont(["Source Serif 4", "Segoe UI", "Tahoma"], 16, bold=True)
        self.value_font = pygame.font.SysFont(["Segoe UI", "Tahoma"], 15)
        self.stats_font = pygame.font.SysFont(["Consolas", "Segoe UI"], 16, bold=True)
        self.tiny_font = pygame.font.SysFont(["Segoe UI", "Tahoma"], 11)
        self.header_font = pygame.font.SysFont(["Segoe UI", "Tahoma"], 13, bold=True)
        
        # File Path for Persistence
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "profile.json")
        self.load_profile()
        
        # Layout metrics
        self.btn_back = pygame.Rect(40, 32, 110, 34)
        self.btn_tab_profile = pygame.Rect(180, 32, 120, 34)
        self.btn_tab_history = pygame.Rect(310, 32, 120, 34)
        
        self.active_tab = "profile" # "profile", "history"
        self.focused_field = None # "name", "country", "birthday", None
        
        # Procedural background texture
        self.wood_texture = self.generate_wood_texture(width, height)
        
        # Scroll state for history
        self.history_scroll = 0
        self.history_visible_rows = 12
        self.row_height = 38
        
        # Input boxes (calculated dynamically in update_layout)
        self.input_name = pygame.Rect(0, 0, 0, 0)
        self.input_country = pygame.Rect(0, 0, 0, 0)
        self.input_birthday = pygame.Rect(0, 0, 0, 0)
        
        self.recalculate_rects()
        
        # Cursor blink state
        self.cursor_visible = True
        self.last_cursor_toggle = pygame.time.get_ticks()

    def load_profile(self):
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception:
                self.data = self.get_default_profile()
        else:
            self.data = self.get_default_profile()
            self.save_profile()
            
        # Guarantee historical fields exist
        if "name" not in self.data: self.data["name"] = "Kỳ Vương"
        if "country" not in self.data: self.data["country"] = "Việt Nam"
        if "birthday" not in self.data: self.data["birthday"] = "01/01/2000"
        if "level" not in self.data: self.data["level"] = 1
        if "exp" not in self.data: self.data["exp"] = 120
        if "history" not in self.data: self.data["history"] = []

    def get_default_profile(self):
        return {
            "name": "Kỳ Vương",
            "country": "Việt Nam",
            "birthday": "01/01/2000",
            "level": 1,
            "exp": 120,
            "history": []
        }

    def save_profile(self):
        try:
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving profile: {e}")

    def add_match_record(self, mode, algo, result, exp_gained=None):
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # Localize strings
        display_mode = "Người vs Bot" if mode == "human_vs_bot" else "Bot vs Bot"
        display_algo = algo.replace("Level ", "L") if algo else "Tự động"
        
        record = {
            "mode": display_mode,
            "algo": display_algo,
            "result": result, # "Thắng", "Thua", "Hòa"
            "time": now
        }
        
        self.data["history"].insert(0, record) # Prepend to history
        
        # Award EXP based on result
        if mode == "human_vs_bot":
            if exp_gained is None:
                exp_gained = 100 if result == "Thắng" else (40 if result == "Hòa" else 20)
            self.data["exp"] += exp_gained
            
            # Level up check (500 exp per level scaling)
            while self.data["exp"] >= self.data["level"] * 500:
                self.data["exp"] -= self.data["level"] * 500
                self.data["level"] += 1
                
        self.save_profile()

    def generate_wood_texture(self, width, height):
        surf = pygame.Surface((width, height))
        surf.fill(COLOR_BG)
        for y in range(0, height, 2):
            wave = math.sin(y * 0.02) * 5 + math.sin(y * 0.1) * 2
            r = max(0, min(255, COLOR_BG[0] + int(wave)))
            g = max(0, min(255, COLOR_BG[1] + int(wave * 0.8)))
            b = max(0, min(255, COLOR_BG[2] + int(wave * 0.5)))
            pygame.draw.line(surf, (r, g, b), (0, y), (width, y))
            pygame.draw.line(surf, (r, g, b), (0, y + 1), (width, y + 1))
            
        noise = pygame.Surface((width, height), pygame.SRCALPHA)
        for _ in range(int(width * height * 0.015)):
            nx = random.randint(0, width - 1)
            ny = random.randint(0, height - 1)
            alpha = random.randint(3, 8)
            val = random.randint(-15, 15)
            nr = max(0, min(255, COLOR_BG[0] + val))
            ng = max(0, min(255, COLOR_BG[1] + val))
            nb = max(0, min(255, COLOR_BG[2] + val))
            noise.set_at((nx, ny), (nr, ng, nb, alpha))
            
        surf.blit(noise, (0, 0))
        return surf

    def update_layout(self, width, height):
        self.width = width
        self.height = height
        self.wood_texture = self.generate_wood_texture(width, height)
        self.recalculate_rects()
        
    def recalculate_rects(self):
        self.btn_back = pygame.Rect(40, 32, 110, 34)
        self.btn_tab_profile = pygame.Rect(180, 32, 120, 34)
        self.btn_tab_history = pygame.Rect(310, 32, 120, 34)
        
        # Text input box positions centered horizontally
        center_x = self.width // 2
        box_w = 275
        box_h = 36
        
        self.input_name = pygame.Rect(center_x - 60, 240, box_w, box_h)
        self.input_country = pygame.Rect(center_x - 60, 300, box_w, box_h)
        self.input_birthday = pygame.Rect(center_x - 60, 360, box_w, box_h)
        
        # Calculate visible rows for history table based on height
        self.history_visible_rows = max(4, (self.height - 220) // self.row_height)

    def handle_event(self, event, controller=None):
        pos = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check Back Button
            if self.btn_back.collidepoint(event.pos):
                from gui.sound import play_synth_sound
                play_synth_sound('move')
                self.focused_field = None
                self.save_profile()
                return "menu"
                
            # Check Tab buttons
            if self.btn_tab_profile.collidepoint(event.pos):
                from gui.sound import play_synth_sound
                play_synth_sound('move')
                self.active_tab = "profile"
                self.focused_field = None
                return None
            elif self.btn_tab_history.collidepoint(event.pos):
                from gui.sound import play_synth_sound
                play_synth_sound('move')
                self.active_tab = "history"
                self.focused_field = None
                return None
                
            # Check input field focus in profile tab
            if self.active_tab == "profile":
                if self.input_name.collidepoint(event.pos):
                    self.focused_field = "name"
                elif self.input_country.collidepoint(event.pos):
                    self.focused_field = "country"
                elif self.input_birthday.collidepoint(event.pos):
                    self.focused_field = "birthday"
                else:
                    if self.focused_field:
                        self.save_profile() # Save changes when clicking outside
                    self.focused_field = None
                    
        elif event.type == pygame.MOUSEWHEEL and self.active_tab == "history":
            # Scroll match history list
            max_scroll = max(0, len(self.data["history"]) - self.history_visible_rows)
            self.history_scroll = max(0, min(max_scroll, self.history_scroll - event.y))
            
        elif event.type == pygame.KEYDOWN and self.focused_field:
            if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                self.save_profile()
                self.focused_field = None
            elif event.key == pygame.K_BACKSPACE:
                val = self.data[self.focused_field]
                if len(val) > 0:
                    self.data[self.focused_field] = val[:-1]
            else:
                char = event.unicode
                if char and char.isprintable():
                    val = self.data[self.focused_field]
                    max_len = 10 if self.focused_field == "birthday" else 20
                    if len(val) < max_len:
                        self.data[self.focused_field] = val + char
                        
        return None

    def draw(self, surface):
        # 1. Draw wood background
        surface.blit(self.wood_texture, (0, 0))
        
        # 2. Draw Header Tab Bar Area
        pygame.draw.line(surface, COLOR_OUTLINE, (0, 80), (self.width, 80), 1)
        
        # --- Back button ---
        mouse_pos = pygame.mouse.get_pos()
        is_hover_back = self.btn_back.collidepoint(mouse_pos)
        pygame.draw.rect(surface, (55, 35, 30) if is_hover_back else COLOR_CARD_BG, self.btn_back, 0, 6)
        pygame.draw.rect(surface, COLOR_GOLD, self.btn_back, 1, 6)
        lbl_back = self.tab_font.render("QUAY LẠI", True, COLOR_TEXT)
        surface.blit(lbl_back, (self.btn_back.centerx - lbl_back.get_width() // 2, self.btn_back.centery - lbl_back.get_height() // 2))
        
        # --- Profile Tab Button ---
        is_hover_p = self.btn_tab_profile.collidepoint(mouse_pos)
        is_active_p = self.active_tab == "profile"
        bg_p = (60, 45, 35) if is_active_p else ((55, 35, 30) if is_hover_p else COLOR_CARD_BG)
        border_p = COLOR_GOLD if (is_active_p or is_hover_p) else COLOR_OUTLINE
        pygame.draw.rect(surface, bg_p, self.btn_tab_profile, 0, 6)
        pygame.draw.rect(surface, border_p, self.btn_tab_profile, 1, 6)
        lbl_p = self.tab_font.render("HỒ SƠ", True, COLOR_GOLD if is_active_p else COLOR_TEXT)
        surface.blit(lbl_p, (self.btn_tab_profile.centerx - lbl_p.get_width() // 2, self.btn_tab_profile.centery - lbl_p.get_height() // 2))
        
        # --- History Tab Button ---
        is_hover_h = self.btn_tab_history.collidepoint(mouse_pos)
        is_active_h = self.active_tab == "history"
        bg_h = (60, 45, 35) if is_active_h else ((55, 35, 30) if is_hover_h else COLOR_CARD_BG)
        border_h = COLOR_GOLD if (is_active_h or is_hover_h) else COLOR_OUTLINE
        pygame.draw.rect(surface, bg_h, self.btn_tab_history, 0, 6)
        pygame.draw.rect(surface, border_h, self.btn_tab_history, 1, 6)
        lbl_h = self.tab_font.render("LỊCH SỬ ĐẤU", True, COLOR_GOLD if is_active_h else COLOR_TEXT)
        surface.blit(lbl_h, (self.btn_tab_history.centerx - lbl_h.get_width() // 2, self.btn_tab_history.centery - lbl_h.get_height() // 2))
        
        # 3. Draw tab content
        if self.active_tab == "profile":
            self.draw_profile_tab(surface)
        else:
            self.draw_history_tab(surface)

    def draw_profile_tab(self, surface):
        center_x = self.width // 2
        
        # Render Title Card
        card_rect = pygame.Rect(center_x - 240, 115, 480, 85)
        pygame.draw.rect(surface, COLOR_CARD_BG, card_rect, 0, 8)
        pygame.draw.rect(surface, COLOR_OUTLINE, card_rect, 1, 8)
        
        # Level circle representation
        lvl_center_x = card_rect.x + 52
        lvl_center_y = card_rect.centery
        pygame.draw.circle(surface, COLOR_GOLD, (lvl_center_x, lvl_center_y), 26)
        pygame.draw.circle(surface, (55, 35, 30), (lvl_center_x, lvl_center_y), 24)
        
        lvl_num = self.stats_font.render(str(self.data["level"]), True, COLOR_GOLD)
        surface.blit(lvl_num, (lvl_center_x - lvl_num.get_width() // 2, lvl_center_y - lvl_num.get_height() // 2))
        
        # Text details
        lbl_name = self.title_font.render(self.data["name"], True, COLOR_GOLD)
        surface.blit(lbl_name, (card_rect.x + 95, card_rect.y + 12))
        
        # EXP bar parameters
        current_exp = self.data["exp"]
        required_exp = self.data["level"] * 500
        progress_ratio = min(1.0, current_exp / max(1, required_exp))
        
        # Draw EXP progress bar
        bar_x = card_rect.x + 95
        bar_y = card_rect.y + 54
        bar_w = 320
        bar_h = 10
        pygame.draw.rect(surface, (20, 12, 10), (bar_x, bar_y, bar_w, bar_h), 0, 5)
        pygame.draw.rect(surface, COLOR_GOLD, (bar_x, bar_y, int(bar_w * progress_ratio), bar_h), 0, 5)
        pygame.draw.rect(surface, COLOR_OUTLINE, (bar_x, bar_y, bar_w, bar_h), 1, 5)
        
        exp_txt = self.tiny_font.render(f"EXP: {current_exp}/{required_exp} ({(progress_ratio * 100):.1f}%)", True, COLOR_MUTED)
        surface.blit(exp_txt, (bar_x + bar_w - exp_txt.get_width(), bar_y - 14))
        
        # Render input form background card
        form_rect = pygame.Rect(center_x - 240, 215, 480, 200)
        pygame.draw.rect(surface, COLOR_CARD_BG, form_rect, 0, 8)
        pygame.draw.rect(surface, COLOR_OUTLINE, form_rect, 1, 8)
        
        # Fields configuration
        fields = [
            ("Họ và Tên:", self.data["name"], self.input_name, "name"),
            ("Quốc gia:", self.data["country"], self.input_country, "country"),
            ("Ngày sinh:", self.data["birthday"], self.input_birthday, "birthday")
        ]
        
        # Cursor blink check
        now = pygame.time.get_ticks()
        if now - self.last_cursor_toggle >= 500:
            self.cursor_visible = not self.cursor_visible
            self.last_cursor_toggle = now
            
        for label_text, val, rect, key in fields:
            # Draw Label
            lbl = self.label_font.render(label_text, True, COLOR_MUTED)
            surface.blit(lbl, (form_rect.x + 25, rect.centery - lbl.get_height() // 2))
            
            # Draw Input Box
            is_focused = self.focused_field == key
            bg_box = (20, 12, 10) if is_focused else (30, 20, 16)
            border_box = COLOR_GOLD if is_focused else COLOR_OUTLINE
            
            pygame.draw.rect(surface, bg_box, rect, 0, 4)
            pygame.draw.rect(surface, border_box, rect, 1, 4)
            
            # Draw Value Text
            txt_val = self.value_font.render(val, True, COLOR_TEXT)
            surface.blit(txt_val, (rect.x + 12, rect.centery - txt_val.get_height() // 2))
            
            # Draw blinking cursor if focused
            if is_focused and self.cursor_visible:
                cursor_x = rect.x + 12 + txt_val.get_width() + 2
                pygame.draw.line(surface, COLOR_GOLD, (cursor_x, rect.y + 8), (cursor_x, rect.bottom - 8), 2)
                
        # Footer Help tips
        help_lbl = self.tiny_font.render("Nhấp chuột vào các ô trên để nhập và nhấn Enter để lưu lại thay đổi", True, COLOR_MUTED)
        surface.blit(help_lbl, (center_x - help_lbl.get_width() // 2, form_rect.bottom + 12))

    def draw_history_tab(self, surface):
        center_x = self.width // 2
        table_y = 115
        table_w = self.width - 80
        table_h = self.height - 180
        
        # Background card for history list
        card_rect = pygame.Rect(40, table_y, table_w, table_h)
        pygame.draw.rect(surface, COLOR_CARD_BG, card_rect, 0, 8)
        pygame.draw.rect(surface, COLOR_OUTLINE, card_rect, 1, 8)
        
        # Table Header Columns Layout
        col_w1 = 180 # Chế độ
        col_w2 = 250 # Thuật toán/Đối thủ
        col_w3 = 140 # Kết quả
        col_w4 = table_w - col_w1 - col_w2 - col_w3 - 20 # Ngày giờ (remaining width)
        
        hdr_rect = pygame.Rect(42, table_y + 2, table_w - 4, 38)
        pygame.draw.rect(surface, (20, 12, 10), hdr_rect, 0, 6)
        pygame.draw.line(surface, COLOR_OUTLINE, (40, table_y + 40), (40 + table_w, table_y + 40), 1)
        
        # Render Column Header Texts
        lbl_h1 = self.header_font.render("CHẾ ĐỘ ĐẤU", True, COLOR_GOLD)
        lbl_h2 = self.header_font.render("THUẬT TOÁN / ĐỐI THỦ", True, COLOR_GOLD)
        lbl_h3 = self.header_font.render("KẾT QUẢ", True, COLOR_GOLD)
        lbl_h4 = self.header_font.render("THỜI GIAN", True, COLOR_GOLD)
        
        surface.blit(lbl_h1, (60, table_y + 20 - lbl_h1.get_height() // 2))
        surface.blit(lbl_h2, (60 + col_w1, table_y + 20 - lbl_h2.get_height() // 2))
        surface.blit(lbl_h3, (60 + col_w1 + col_w2, table_y + 20 - lbl_h3.get_height() // 2))
        surface.blit(lbl_h4, (60 + col_w1 + col_w2 + col_w3, table_y + 20 - lbl_h4.get_height() // 2))
        
        # Match History data rendering
        history = self.data.get("history", [])
        if not history:
            no_txt = self.value_font.render("Chưa có lịch sử đấu nào được ghi nhận", True, COLOR_MUTED)
            surface.blit(no_txt, (center_x - no_txt.get_width() // 2, table_y + 120))
            return
            
        start_y = table_y + 41
        visible_count = min(len(history) - self.history_scroll, self.history_visible_rows)
        
        for idx in range(visible_count):
            item_idx = self.history_scroll + idx
            record = history[item_idx]
            
            y = start_y + idx * self.row_height
            row_rect = pygame.Rect(42, y, table_w - 4, self.row_height)
            
            # Alternate row background colors
            if idx % 2 == 1:
                pygame.draw.rect(surface, (33, 20, 16), row_rect)
            pygame.draw.line(surface, (50, 42, 32), (40, y + self.row_height), (40 + table_w, y + self.row_height), 1)
            
            # Values render
            mode_txt = self.value_font.render(record.get("mode", "Tự động"), True, COLOR_TEXT)
            algo_txt = self.value_font.render(record.get("algo", "Tự động"), True, COLOR_TEXT)
            time_txt = self.value_font.render(record.get("time", ""), True, COLOR_MUTED)
            
            # Colorful result text
            result = record.get("result", "Hòa")
            res_color = COLOR_ACCENT if result == "Thắng" else (COLOR_RED if result == "Thua" else COLOR_GOLD)
            res_txt = self.label_font.render(result, True, res_color)
            
            # Blit columns
            surface.blit(mode_txt, (60, y + self.row_height // 2 - mode_txt.get_height() // 2))
            surface.blit(algo_txt, (60 + col_w1, y + self.row_height // 2 - algo_txt.get_height() // 2))
            surface.blit(res_txt, (60 + col_w1 + col_w2, y + self.row_height // 2 - res_txt.get_height() // 2))
            surface.blit(time_txt, (60 + col_w1 + col_w2 + col_w3, y + self.row_height // 2 - time_txt.get_height() // 2))
            
        # Draw scrollbar track & thumb if list overflows visible rows
        max_rows_scroll = max(0, len(history) - self.history_visible_rows)
        if max_rows_scroll > 0:
            track_x = 40 + table_w - 10
            track_y = start_y + 5
            track_h = table_h - 55
            pygame.draw.rect(surface, (50, 30, 25), (track_x, track_y, 4, track_h), 0, 2)
            
            visible_ratio = min(1.0, self.history_visible_rows / len(history))
            thumb_h = max(20, int(track_h * visible_ratio))
            thumb_range = max(1, track_h - thumb_h)
            thumb_y = track_y + int((thumb_range * self.history_scroll) / max_rows_scroll)
            pygame.draw.rect(surface, COLOR_GOLD, (track_x - 1, thumb_y, 6, thumb_h), 0, 2)
            
            # Bottom help tip
            scroll_tip = self.tiny_font.render("Cuộn chuột trong bảng lịch sử để xem thêm", True, COLOR_MUTED)
            surface.blit(scroll_tip, (40 + table_w - scroll_tip.get_width() - 15, table_y + table_h - 18))
