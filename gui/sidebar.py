# Pygame Sidebar control panel for game info and actions
import pygame

COLOR_SIDEBAR_BG = (45, 45, 45)      # Dark gray background
COLOR_CARD_BG = (60, 60, 60)         # Lighter gray for info cards
COLOR_ACCENT = (0, 173, 181)         # Cyan accent
COLOR_TEXT = (240, 240, 240)         # Light text
COLOR_TEXT_MUTED = (160, 160, 160)   # Muted gray text
COLOR_BTN_RED = (192, 57, 43)        # Red button
COLOR_BTN_GREEN = (39, 174, 96)      # Green button
COLOR_BTN_BLUE = (41, 128, 185)      # Blue button

class Sidebar:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # Load fonts
        self.title_font = pygame.font.SysFont(["Segoe UI", "Tahoma", "Arial"], 22, bold=True)
        self.body_font = pygame.font.SysFont(["Segoe UI", "Tahoma", "Arial"], 16)
        self.mono_font = pygame.font.SysFont(["Consolas", "Courier New"], 14)
        
        # Define button Rects for click detection
        self.btn_new_game = pygame.Rect(x + 20, 480, width - 40, 35)
        self.btn_undo = pygame.Rect(x + 20, 530, width - 40, 35)
        self.btn_hint = pygame.Rect(x + 20, 580, width - 40, 35)
        self.btn_menu = pygame.Rect(x + 20, 630, width - 40, 35)
        
        # Speed slider rect (for Bot vs Bot)
        # Slider is from X = x + 30 to x + width - 60
        self.slider_track = pygame.Rect(x + 30, 400, width - 60, 6)
        self.slider_knob_x = x + 30 + (width - 60) // 2 # Initial center
        self.slider_knob_radius = 8
        self.slider_dragging = False

    def get_bot_speed_delay(self):
        """Converts slider position to delay in seconds (0.2s to 2.2s)"""
        # Slider length
        length = self.width - 60
        ratio = (self.slider_knob_x - (self.x + 30)) / length
        # Map 0..1 to 0.2..2.2
        return 0.2 + ratio * 2.0

    def handle_event(self, event, current_speed_delay=None):
        """Returns action string if a button is clicked, or handles slider dragging"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Check button clicks
                if self.btn_new_game.collidepoint(event.pos):
                    return "new_game"
                elif self.btn_undo.collidepoint(event.pos):
                    return "undo"
                elif self.btn_hint.collidepoint(event.pos):
                    return "hint"
                elif self.btn_menu.collidepoint(event.pos):
                    return "menu"
                    
                # Check slider click/drag start
                knob_rect = pygame.Rect(
                    self.slider_knob_x - self.slider_knob_radius - 5,
                    400 - self.slider_knob_radius - 5,
                    self.slider_knob_radius * 2 + 10,
                    self.slider_knob_radius * 2 + 10
                )
                if knob_rect.collidepoint(event.pos) or self.slider_track.inflate(0, 10).collidepoint(event.pos):
                    self.slider_dragging = True
                    self.update_slider_pos(event.pos[0])
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.slider_dragging = False
                
        elif event.type == pygame.MOUSEMOTION:
            if self.slider_dragging:
                self.update_slider_pos(event.pos[0])
                
        return None

    def update_slider_pos(self, mx):
        # Clamp knob X between slider track boundaries
        start_x = self.x + 30
        end_x = self.x + self.width - 30
        self.slider_knob_x = max(start_x, min(mx, end_x))

    def draw(self, surface, board, game_mode, red_bot_name, black_bot_name, hint_move=None):
        # 1. Fill sidebar background
        sidebar_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, COLOR_SIDEBAR_BG, sidebar_rect)
        
        # Draw left border separator line
        pygame.draw.line(surface, (80, 80, 80), (self.x, self.y), (self.x, self.y + self.height), 2)
        
        # 2. Draw Header
        header_txt = self.title_font.render("BẢNG ĐIỀU KHIỂN", True, COLOR_ACCENT)
        surface.blit(header_txt, (self.x + 20, self.y + 20))
        
        # Divider
        pygame.draw.line(surface, (60, 60, 60), (self.x + 15, self.y + 55), (self.x + self.width - 15, self.y + 55), 1)
        
        # 3. Draw Game Info Card
        card_rect = pygame.Rect(self.x + 15, 75, self.width - 30, 150)
        pygame.draw.rect(surface, COLOR_CARD_BG, card_rect, 0, 8) # Rounded corners
        
        # Turn label
        turn_lbl = self.body_font.render("Lượt đi:", True, COLOR_TEXT_MUTED)
        surface.blit(turn_lbl, (self.x + 30, 95))
        
        turn_val_str = "Đỏ (RED)" if board.turn == 'red' else "Đen (BLACK)"
        turn_val_color = (231, 76, 60) if board.turn == 'red' else (241, 196, 15)
        turn_val = self.body_font.render(turn_val_str, True, turn_val_color)
        surface.blit(turn_val, (self.x + 105, 95))

        # Check warning
        if board.is_in_check(board.turn):
            import math
            pulse = (math.sin(pygame.time.get_ticks() * 0.015) + 1) / 2
            warn_color = (231, 76, 60) if pulse > 0.5 else (241, 196, 15)
            warn_font = pygame.font.SysFont(["Segoe UI", "Tahoma", "Arial"], 14, bold=True)
            warn_val = warn_font.render("⚠️ ĐANG BỊ CHIẾU!", True, warn_color)
            surface.blit(warn_val, (self.x + 200, 96))
        
        # Mode label
        mode_lbl = self.body_font.render("Chế độ:", True, COLOR_TEXT_MUTED)
        surface.blit(mode_lbl, (self.x + 30, 130))
        
        mode_val_str = "Human vs Bot" if game_mode == "human_vs_bot" else "Bot vs Bot"
        mode_val = self.body_font.render(mode_val_str, True, COLOR_TEXT)
        surface.blit(mode_val, (self.x + 105, 130))
        
        # Bot profiles
        if game_mode == "human_vs_bot":
            bot_lbl = self.body_font.render("Cấp độ Bot:", True, COLOR_TEXT_MUTED)
            surface.blit(bot_lbl, (self.x + 30, 165))
            # Black is Bot in Human vs Bot
            bot_val = self.body_font.render(black_bot_name, True, COLOR_ACCENT)
            surface.blit(bot_val, (self.x + 120, 165))
        else:
            # Bot vs Bot showing both levels
            bot_lbl = self.body_font.render("Bot Đỏ:", True, COLOR_TEXT_MUTED)
            surface.blit(bot_lbl, (self.x + 30, 165))
            bot_val = self.body_font.render(red_bot_name.split(":")[-1].strip(), True, (231, 76, 60))
            surface.blit(bot_val, (self.x + 95, 165))
            
            bot2_lbl = self.body_font.render("Bot Đen:", True, COLOR_TEXT_MUTED)
            surface.blit(bot2_lbl, (self.x + 30, 190))
            bot2_val = self.body_font.render(black_bot_name.split(":")[-1].strip(), True, (241, 196, 15))
            surface.blit(bot2_val, (self.x + 95, 190))

        # 4. Draw Hint Info / Move stats Card
        hint_card_rect = pygame.Rect(self.x + 15, 240, self.width - 30, 110)
        pygame.draw.rect(surface, COLOR_CARD_BG, hint_card_rect, 0, 8)
        
        hint_header = self.body_font.render("GỢI Ý NƯỚC ĐI", True, COLOR_ACCENT)
        surface.blit(hint_header, (self.x + 30, 255))
        
        if hint_move:
            from_pos, to_pos = hint_move
            # Convert row/col to human format, e.g. (9,0) to A0
            c_char1 = chr(65 + from_pos[1])
            c_char2 = chr(65 + to_pos[1])
            hint_str = f"Nên đi: {c_char1}{from_pos[0]} -> {c_char2}{to_pos[0]}"
            hint_txt = self.mono_font.render(hint_str, True, COLOR_TEXT)
            surface.blit(hint_txt, (self.x + 30, 290))
        else:
            no_hint = self.body_font.render("Nhấn [HINT] để xem...", True, COLOR_TEXT_MUTED)
            surface.blit(no_hint, (self.x + 30, 290))

        # 5. Bot speed control (Only for Bot vs Bot)
        if game_mode == "bot_vs_bot":
            speed_title = self.body_font.render("Tốc độ Bot (Độ trễ đi quân):", True, COLOR_TEXT_MUTED)
            surface.blit(speed_title, (self.x + 20, 370))
            
            # Draw slider track
            pygame.draw.rect(surface, (80, 80, 80), self.slider_track)
            
            # Draw slider knob
            pygame.draw.circle(surface, COLOR_ACCENT, (self.slider_knob_x, 403), self.slider_knob_radius)
            
            # Display current delay speed
            delay = self.get_bot_speed_delay()
            delay_lbl = self.mono_font.render(f"{delay:.2f} giây", True, COLOR_TEXT)
            surface.blit(delay_lbl, (self.x + self.width - 90, 368))

        # 6. Render action buttons
        # Button: New game
        pygame.draw.rect(surface, COLOR_BTN_BLUE, self.btn_new_game, 0, 5)
        bt1 = self.body_font.render("VÁN MỚI", True, COLOR_TEXT)
        surface.blit(bt1, (self.btn_new_game.centerx - bt1.get_width() // 2, self.btn_new_game.centery - bt1.get_height() // 2))
        
        # Button: Undo
        pygame.draw.rect(surface, COLOR_BTN_GREEN, self.btn_undo, 0, 5)
        bt2 = self.body_font.render("HOÀN NƯỚC (UNDO)", True, COLOR_TEXT)
        surface.blit(bt2, (self.btn_undo.centerx - bt2.get_width() // 2, self.btn_undo.centery - bt2.get_height() // 2))
        
        # Button: Hint
        pygame.draw.rect(surface, (155, 89, 182), self.btn_hint, 0, 5)
        bt3 = self.body_font.render("GỢI Ý NƯỚC ĐI (HINT)", True, COLOR_TEXT)
        surface.blit(bt3, (self.btn_hint.centerx - bt3.get_width() // 2, self.btn_hint.centery - bt3.get_height() // 2))
        
        # Button: Main menu
        pygame.draw.rect(surface, COLOR_BTN_RED, self.btn_menu, 0, 5)
        bt4 = self.body_font.render("VỀ MENU CHÍNH", True, COLOR_TEXT)
        surface.blit(bt4, (self.btn_menu.centerx - bt4.get_width() // 2, self.btn_menu.centery - bt4.get_height() // 2))
