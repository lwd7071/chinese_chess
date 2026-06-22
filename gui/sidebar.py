# Pygame Sidebar control panel for game info and actions
import pygame
import time

COLOR_SIDEBAR_BG = (45, 45, 45)      # Dark gray background
COLOR_CARD_BG = (60, 60, 60)         # Lighter gray for info cards
COLOR_ACCENT = (0, 173, 181)         # Cyan accent
COLOR_TEXT = (240, 240, 240)         # Light text
COLOR_TEXT_MUTED = (160, 160, 160)   # Muted gray text
COLOR_BTN_RED = (192, 57, 43)        # Red button
COLOR_BTN_GREEN = (39, 174, 96)      # Green button
COLOR_BTN_BLUE = (41, 128, 185)      # Blue button
COLOR_HISTORY_RED = (231, 76, 60)
COLOR_HISTORY_BLACK = (241, 196, 15)
COLOR_HISTORY_CAPTURE = (46, 204, 113)
COLOR_HISTORY_ROW = (50, 50, 50)
COLOR_HISTORY_FRAME = (90, 90, 90)

PIECE_NAME_VI = {
    'G': 'Tướng',
    'A': 'Sĩ',
    'E': 'Tượng',
    'H': 'Mã',
    'R': 'Xe',
    'C': 'Pháo',
    'P': 'Tốt',
}

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
        self.small_font = pygame.font.SysFont(["Segoe UI", "Tahoma", "Arial"], 13)
        self.history_font = pygame.font.SysFont(["Segoe UI", "Tahoma", "Arial"], 14)
        self.count_font = pygame.font.SysFont(["Segoe UI", "Tahoma", "Arial"], 12, bold=True)
        
        # Define button Rects for click detection
        self.btn_new_game = pygame.Rect(x + 20, 650, width - 40, 30)
        self.btn_undo = pygame.Rect(x + 20, 688, width - 40, 30)
        self.btn_hint = pygame.Rect(x + 20, 726, width - 40, 30)
        self.btn_menu = pygame.Rect(x + 20, 764, width - 40, 28)
        
        # Speed slider rect (for Bot vs Bot)
        # Slider is from X = x + 30 to x + width - 60
        self.slider_track = pygame.Rect(x + 30, 630, width - 60, 6)
        self.slider_knob_x = x + 30 + (width - 60) // 2 # Initial center
        self.slider_knob_radius = 8
        self.slider_dragging = False

        # Move history view state
        self.history_visible_rows = 5
        self.history_scroll = 0
        self.history_view_rect = pygame.Rect(x + 15, 385, width - 30, 215)

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
                    630 - self.slider_knob_radius - 5,
                    self.slider_knob_radius * 2 + 10,
                    self.slider_knob_radius * 2 + 10
                )
                if knob_rect.collidepoint(event.pos) or self.slider_track.inflate(0, 10).collidepoint(event.pos):
                    self.slider_dragging = True
                    self.update_slider_pos(event.pos[0])

        elif event.type == pygame.MOUSEWHEEL:
            if self.history_view_rect.collidepoint(pygame.mouse.get_pos()):
                max_scroll = max(0, self._history_total - self.history_visible_rows)
                self.history_scroll = max(0, min(max_scroll, self.history_scroll - event.y))
                    
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

    def format_square(self, pos):
        return f"{chr(65 + pos[1])}{pos[0]}"

    def get_piece_name(self, piece_name):
        return PIECE_NAME_VI.get(piece_name, piece_name or "Quân")

    def format_move_record(self, record):
        side_label = "Đỏ" if record.get("side") == "red" else "Đen"
        piece_name = self.get_piece_name(record.get("piece_name"))
        from_pos = record.get("from_pos")
        to_pos = record.get("to_pos")
        move_text = f"{side_label} {piece_name} {self.format_square(from_pos)}->{self.format_square(to_pos)}"
        captured_name = record.get("captured_name")
        if captured_name:
            move_text += f" (ăn {self.get_piece_name(captured_name)})"
        return move_text

    def get_history_window(self, moves):
        self._history_total = len(moves)
        if not moves:
            return 0, []
        max_scroll = max(0, len(moves) - self.history_visible_rows)
        start = max(0, min(self.history_scroll, max_scroll))
        end = start + self.history_visible_rows
        return start, moves[start:end]

    def get_hint_summary(self, board, hint_move):
        if not hint_move:
            return None

        from_pos, to_pos = hint_move
        mover = board.get_piece(from_pos)
        target = board.get_piece(to_pos)
        summary = {
            "piece_name": self.get_piece_name(mover.name if mover else None),
            "side_label": "Đỏ" if mover and mover.color == "red" else "Đen",
            "from_square": self.format_square(from_pos),
            "to_square": self.format_square(to_pos),
            "capture_text": "Không ăn quân",
            "effect_text": "Nước đi thường",
        }

        if target:
            summary["capture_text"] = f"Ăn: {self.get_piece_name(target.name)}"

        simulated_board = board.copy()
        simulated_board.make_move(from_pos, to_pos, log_move=False)
        if simulated_board.is_in_check(simulated_board.turn):
            summary["effect_text"] = "Sau nước này sẽ chiếu tướng"
        elif target:
            summary["effect_text"] = "Nước ăn quân an toàn"

        return summary

    def draw(self, surface, board, game_mode, red_bot_name, black_bot_name, hint_move=None, move_history=None, pending_move=None, latest_move_index=None, latest_move_flash_until=0.0):
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
        hint_card_rect = pygame.Rect(self.x + 15, 240, self.width - 30, 132)
        pygame.draw.rect(surface, COLOR_CARD_BG, hint_card_rect, 0, 8)
        
        hint_header = self.body_font.render("GỢI Ý NƯỚC ĐI", True, COLOR_ACCENT)
        surface.blit(hint_header, (self.x + 30, 255))
        
        if hint_move:
            hint_info = self.get_hint_summary(board, hint_move)

            if hint_info:
                hint_title = self.body_font.render(f"Nên đi: {hint_info['piece_name']}", True, COLOR_TEXT)
                surface.blit(hint_title, (self.x + 30, 280))

                side_lbl = self.small_font.render(f"Bên: {hint_info['side_label']}", True, COLOR_TEXT_MUTED)
                surface.blit(side_lbl, (self.x + 30, 298))

                hint_str = f"{hint_info['from_square']} -> {hint_info['to_square']}"
                hint_txt = self.mono_font.render(hint_str, True, COLOR_TEXT)
                surface.blit(hint_txt, (self.x + 30, 315))

                capture_txt = self.body_font.render(hint_info["capture_text"], True, COLOR_TEXT_MUTED)
                surface.blit(capture_txt, (self.x + 30, 332))

                effect_txt = self.small_font.render(hint_info["effect_text"], True, COLOR_HISTORY_CAPTURE)
                surface.blit(effect_txt, (self.x + 30, 350))
        else:
            no_hint = self.body_font.render("Nhấn [HINT] để xem...", True, COLOR_TEXT_MUTED)
            surface.blit(no_hint, (self.x + 30, 300))

        recent_moves = move_history or []
        red_moves = [move for move in recent_moves if move.get("side") == "red"]
        black_moves = [move for move in recent_moves if move.get("side") == "black"]
        total_moves = len(recent_moves)

        # 5. Move history card
        history_card_rect = pygame.Rect(self.x + 15, 385, self.width - 30, 215)
        pygame.draw.rect(surface, COLOR_CARD_BG, history_card_rect, 0, 8)
        pygame.draw.rect(surface, COLOR_HISTORY_FRAME, history_card_rect, 1, 8)

        history_title = self.body_font.render("LỊCH SỬ BƯỚC ĐI CỦA CẢ 2", True, COLOR_ACCENT)
        surface.blit(history_title, (self.x + 30, 395))

        total_red = len(red_moves)
        total_black = len(black_moves)
        total_lbl = self.count_font.render(f"Tổng: {total_moves} nước", True, COLOR_TEXT)
        red_lbl = self.count_font.render(f"Đỏ: {total_red}", True, COLOR_HISTORY_RED)
        black_lbl = self.count_font.render(f"Đen: {total_black}", True, COLOR_HISTORY_BLACK)
        surface.blit(total_lbl, (self.x + 30, 423))
        surface.blit(red_lbl, (self.x + 135, 423))
        surface.blit(black_lbl, (self.x + 220, 423))

        max_scroll = max(0, total_moves - self.history_visible_rows)
        self.history_scroll = min(self.history_scroll, max_scroll)

        if max_scroll > 0:
            scroll_lbl = self.small_font.render(f"Cuộn {self.history_scroll}/{max_scroll}", True, COLOR_TEXT_MUTED)
            surface.blit(scroll_lbl, (self.x + self.width - 120, 395))

        start_y = 451

        start_index, history_window = self.get_history_window(recent_moves)
        for idx, move in enumerate(history_window):
            y = start_y + idx * 23
            row_rect = pygame.Rect(self.x + 25, y - 1, self.width - 56, 18)
            is_latest = latest_move_index is not None and move_history is not None and (start_index + idx) == latest_move_index
            if is_latest and time.time() < latest_move_flash_until:
                row_color = COLOR_HISTORY_CAPTURE
            elif move.get("pending"):
                row_color = COLOR_HISTORY_CAPTURE
            else:
                row_color = COLOR_HISTORY_ROW
            pygame.draw.rect(surface, row_color, row_rect, 0, 4)

            move_num = start_index + idx + 1
            move_text = self.format_move_record(move)
            if is_latest and time.time() < latest_move_flash_until:
                move_color = COLOR_ACCENT
            elif move.get("pending"):
                move_color = COLOR_ACCENT
            elif "(ăn " in move_text:
                move_color = COLOR_HISTORY_CAPTURE
            else:
                move_color = COLOR_TEXT

            num_color = COLOR_HISTORY_RED if move.get("side") == "red" else COLOR_HISTORY_BLACK
            if is_latest and time.time() < latest_move_flash_until:
                num_color = COLOR_ACCENT
            elif move.get("pending"):
                num_color = COLOR_ACCENT
            num_lbl = self.count_font.render(f"{move_num}.", True, num_color)
            txt = self.history_font.render(move_text, True, move_color)
            surface.blit(num_lbl, (self.x + 30, y))
            surface.blit(txt, (self.x + 52, y))

        if max_scroll > 0:
            track_x = self.x + self.width - 18
            track_y = 451
            track_h = 110
            pygame.draw.rect(surface, (70, 70, 70), (track_x, track_y, 5, track_h), 0, 3)

            visible_ratio = min(1.0, self.history_visible_rows / max(1, total_moves))
            thumb_h = max(16, int(track_h * visible_ratio))
            thumb_range = max(1, track_h - thumb_h)
            thumb_y = track_y + int((thumb_range * self.history_scroll) / max_scroll)
            pygame.draw.rect(surface, COLOR_ACCENT, (track_x - 1, thumb_y, 7, thumb_h), 0, 3)

        hint_scroll = self.small_font.render("Cuộn trên khung lịch sử để xem thêm", True, COLOR_TEXT_MUTED)
        surface.blit(hint_scroll, (self.x + 30, 575))

        # 5. Bot speed control (Only for Bot vs Bot)
        if game_mode == "bot_vs_bot":
            speed_title = self.body_font.render("Tốc độ Bot (Độ trễ đi quân):", True, COLOR_TEXT_MUTED)
            surface.blit(speed_title, (self.x + 20, 608))
            
            # Draw slider track
            pygame.draw.rect(surface, (80, 80, 80), pygame.Rect(self.x + 30, 630, self.width - 60, 6))
            
            # Draw slider knob
            pygame.draw.circle(surface, COLOR_ACCENT, (self.slider_knob_x, 630), self.slider_knob_radius)
            
            # Display current delay speed
            delay = self.get_bot_speed_delay()
            delay_lbl = self.mono_font.render(f"{delay:.2f} giây", True, COLOR_TEXT)
            surface.blit(delay_lbl, (self.x + self.width - 90, 607))

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
