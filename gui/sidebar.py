# Pygame Sidebar control panel for game info and actions (Royal Theme Redesign)
import pygame
import time
import math
import random
from gui.assets import get_asset

COLOR_SIDEBAR_BG = (28, 16, 12)       # Warm deep dark rosewood (#1c100c)
COLOR_CARD_BG = (44, 28, 24)          # Slightly lighter container (#2c1c18)
COLOR_ACCENT = (242, 202, 80)         # Antique Gold (#f2ca50)
COLOR_TEXT = (250, 220, 213)          # On-surface (#fadcd5)
COLOR_TEXT_MUTED = (180, 165, 150)    # Muted beige
COLOR_OUTLINE = (77, 70, 53)          # Outline border (#4d4635)
COLOR_JADE = (89, 222, 155)           # Jade green (#59de9b)
COLOR_RED = (231, 76, 60)             # Red turn/side
COLOR_BLACK = (241, 196, 15)          # Black turn/side

PIECE_NAME_VI = {
    'G': 'Tướng',
    'A': 'Sĩ',
    'E': 'Tượng',
    'H': 'Mã',
    'R': 'Xe',
    'C': 'Pháo',
    'P': 'Tốt',
}

# 18 Algorithms mapped to their display name and search registry keys
ALGO_OPTIONS = [
    # Level 1
    ("BFS", "BFS (Breadth-First)", 0),
    ("DFS", "DFS (Depth-First)", 0),
    ("UCS", "UCS (Uniform Cost)", 0),
    # Level 2
    ("Greedy", "Greedy Search", 1),
    ("A*", "A* Algorithm", 1),
    ("IDA*", "IDA* Search", 1),
    # Level 3
    ("Hill Climbing", "Hill Climbing", 2),
    ("Simulated Annealing", "Simulated Annealing", 2),
    ("Beam Search", "Beam Search", 2),
    # Level 4
    ("Online Search", "Online Search", 3),
    ("AND-OR Search", "AND-OR Search", 3),
    ("Belief State", "Belief State", 3),
    # Level 5
    ("Backtracking", "Backtracking (CSP)", 4),
    ("Min-Conflicts", "Min-Conflicts", 4),
    ("AC-3", "AC-3 Constraint", 4),
    # Level 6
    ("Minimax", "Minimax", 5),
    ("Alpha-Beta", "Alpha-Beta Pruning", 5),
    ("Expectimax", "Expectimax", 5)
]

class Sidebar:
    def __init__(self, x, y, width, height, chinese_supported=False, font_name=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.chinese_supported = chinese_supported
        self.font_name = font_name
        
        # Load fonts
        self.title_font = pygame.font.SysFont("Segoe UI, Tahoma, Arial", 20, bold=True)
        self.body_font = pygame.font.SysFont("Segoe UI, Tahoma, Arial", 15, bold=True)
        self.mono_font = pygame.font.SysFont("Consolas, Courier New", 13, bold=True)
        self.small_font = pygame.font.SysFont("Segoe UI, Tahoma, Arial", 13)
        self.tiny_font = pygame.font.SysFont("Segoe UI, Tahoma, Arial", 11)
        self.count_font = pygame.font.SysFont("Segoe UI, Tahoma, Arial", 12, bold=True)
        
        if self.chinese_supported and self.font_name:
            self.history_font = pygame.font.SysFont(self.font_name, 13)
        else:
            self.history_font = pygame.font.SysFont("Segoe UI, Tahoma, Arial", 13)
        
        # Controls Footer: 3 Buttons horizontal at the bottom
        btn_w = (width - 60) // 3
        self.btn_undo = pygame.Rect(x + 20, 760, btn_w, 36)
        self.btn_hint = pygame.Rect(x + 20 + btn_w + 10, 760, btn_w, 36)
        self.btn_surrender = pygame.Rect(x + 20 + (btn_w + 10) * 2, 760, btn_w, 36)
        
        # Algorithm Dropdown state
        self.dropdown_open = False
        self.dropdown_rect = pygame.Rect(x + 20, 355, width - 40, 28)
        self.dropdown_scroll = 0
        self.dropdown_visible_items = 6
        self.dropdown_item_height = 24
        
        # Simulated AI search stats
        self.sim_nodes = 1284
        self.sim_frontier = 42
        self.sim_explored = 856
        self.last_sim_update = 0.0
        
        # Move history view state
        self.history_card_height = 255
        self.history_visible_rows = 6
        self.history_scroll = 0
        self.history_view_rect = pygame.Rect(x + 15, 545, width - 30, 160)
        self._history_total = 0

    def update_layout(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # Recalculate Footer Buttons relative to height
        btn_w = (width - 60) // 3
        self.btn_undo = pygame.Rect(x + 20, height - 60, btn_w, 36)
        self.btn_hint = pygame.Rect(x + 20 + btn_w + 10, height - 60, btn_w, 36)
        self.btn_surrender = pygame.Rect(x + 20 + (btn_w + 10) * 2, height - 60, btn_w, 36)
        
        # Recalculate Dropdown Rect
        self.dropdown_rect = pygame.Rect(x + 20, y + 355, width - 40, 28)
        
        # Recalculate History Card metrics
        self.history_card_height = max(100, (self.height - 80) - 485)
        self.history_view_rect = pygame.Rect(x + 15, 545, width - 30, self.history_card_height - 95)
        self.history_visible_rows = max(2, (self.history_card_height - 95) // 24)

    def get_bot_speed_delay(self):
        # Default fixed delay, or adjustable if needed
        return 0.8

    def handle_event(self, event, current_speed_delay=None):
        pos = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check Footer Button clicks
            if self.btn_undo.collidepoint(event.pos):
                return "undo"
            elif self.btn_hint.collidepoint(event.pos):
                return "hint"
            elif self.btn_surrender.collidepoint(event.pos):
                return "menu" # Surrender goes back to menu in Controller
                
        elif event.type == pygame.MOUSEWHEEL:
            # Handle scroll on history
            if self.history_view_rect.collidepoint(pos):
                max_scroll = max(0, self._history_total - self.history_visible_rows)
                self.history_scroll = max(0, min(max_scroll, self.history_scroll - event.y))
                return None
                    
        return None

    def format_square(self, pos):
        return f"{chr(65 + pos[1])}{pos[0]}"

    def get_piece_name(self, piece_name):
        return PIECE_NAME_VI.get(piece_name, piece_name or "Quân")

    def format_move_compact(self, record):
        # Translate characters to Chinese pieces abbreviations
        char_map = {
            '帥': '帥', '將': '將',
            '仕': '仕', '士': '士',
            '相': '相', '象': '象',
            '馬': '馬', '傌': '馬',
            '車': '車', '俥': '車',
            '砲': '砲', '炮': '砲',
            '兵': '兵', '卒': '卒'
        }
        
        # Translate to English piece names if Chinese is not supported
        en_map = {
            '帥': 'G', '將': 'G',
            '仕': 'A', '士': 'A',
            '相': 'E', '象': 'E',
            '馬': 'H', '傌': 'H',
            '車': 'R', '俥': 'R',
            '砲': 'C', '炮': 'C',
            '兵': 'P', '卒': 'P'
        }
        
        if not self.chinese_supported:
            char = record.get("piece_name") or "?"
        else:
            char = record.get("piece_char") or "?"
            char = char_map.get(char, char)
            
        from_pos = record.get("from_pos")
        to_pos = record.get("to_pos")
        f_sq = self.format_square(from_pos)
        t_sq = self.format_square(to_pos)
        
        move_str = f"{char}{f_sq}->{t_sq}"
        
        captured = record.get("captured_char")
        if captured:
            if not self.chinese_supported:
                captured = en_map.get(captured, record.get("captured_name") or "?")
            else:
                captured = char_map.get(captured, captured)
            move_str += f"x{captured}"
        return move_str

    def get_history_rows(self, moves):
        """Groups move history list into Red/Black pairs (rows)"""
        rows = []
        for i in range(0, len(moves), 2):
            red_move = moves[i]
            black_move = moves[i+1] if i+1 < len(moves) else None
            rows.append((red_move, black_move))
        
        self._history_total = len(rows)
        max_scroll = max(0, len(rows) - self.history_visible_rows)
        start = max(0, min(self.history_scroll, max_scroll))
        end = start + self.history_visible_rows
        return start, rows[start:end]

    def draw(self, surface, board, game_mode, red_bot_name, black_bot_name, hint_move=None, move_history=None, pending_move=None, latest_move_index=None, latest_move_flash_until=0.0):
        # 1. Fill sidebar background
        sidebar_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, COLOR_SIDEBAR_BG, sidebar_rect)
        pygame.draw.line(surface, COLOR_OUTLINE, (self.x, self.y), (self.x, self.y + self.height), 2)
        
        # 2. Draw Header "BẢNG ĐIỀU KHIỂN"
        header_txt = self.title_font.render("BẢNG ĐIỀU KHIỂN", True, COLOR_ACCENT)
        surface.blit(header_txt, (self.x + 20, self.y + 20))
        pygame.draw.line(surface, COLOR_OUTLINE, (self.x + 15, self.y + 55), (self.x + self.width - 15, self.y + 55), 1)
        
        # 3. Draw Game Info Card (Opponent, Timer, Player)
        card_rect = pygame.Rect(self.x + 15, 70, self.width - 30, 150)
        pygame.draw.rect(surface, COLOR_CARD_BG, card_rect, 0, 8)
        pygame.draw.rect(surface, COLOR_OUTLINE, card_rect, 1, 8)
        
        # --- Opponent profile ---
        opp_av_center = (self.x + 40, 105)
        pygame.draw.circle(surface, COLOR_ACCENT, opp_av_center, 18)
        pygame.draw.circle(surface, (55, 35, 30), opp_av_center, 16)
        opp_img = get_asset("avatar_opponent")
        if opp_img:
            scaled_opp = pygame.transform.smoothscale(opp_img, (32, 32))
            surface.blit(scaled_opp, (opp_av_center[0] - 16, opp_av_center[1] - 16))
        else:
            opp_txt = self.tiny_font.render("BOT", True, COLOR_ACCENT)
            surface.blit(opp_txt, (opp_av_center[0] - opp_txt.get_width() // 2, opp_av_center[1] - opp_txt.get_height() // 2))
            
        opp_lbl = self.tiny_font.render("ĐỐI THỦ", True, COLOR_TEXT_MUTED)
        surface.blit(opp_lbl, (self.x + 68, 90))
        
        opp_name_str = black_bot_name if game_mode == "human_vs_bot" else black_bot_name.split(":")[-1].strip()
        opp_name_str = opp_name_str or "Lão Ngoan Đồng"
        opp_name = self.body_font.render(opp_name_str, True, COLOR_BLACK)
        surface.blit(opp_name, (self.x + 68, 108))
        
        # --- Timer / Turn Indicator Box ---
        turn_box = pygame.Rect(self.x + 30, 133, self.width - 60, 26)
        pygame.draw.rect(surface, (30, 18, 14), turn_box, 0, 13)
        pygame.draw.rect(surface, COLOR_OUTLINE, turn_box, 1, 13)
        
        # Timer icon (represented as vertical lines or small circle)
        timer_center = (turn_box.x + 18, turn_box.centery)
        pygame.draw.circle(surface, COLOR_ACCENT, timer_center, 6, 1)
        pygame.draw.line(surface, COLOR_ACCENT, timer_center, (timer_center[0], timer_center[1] - 3), 1)
        pygame.draw.line(surface, COLOR_ACCENT, timer_center, (timer_center[0] + 2, timer_center[1]), 1)
        
        timer_txt = self.mono_font.render("05:24", True, COLOR_ACCENT)
        surface.blit(timer_txt, (turn_box.x + 28, turn_box.centery - timer_txt.get_height() // 2))
        
        turn_val_str = "LƯỢT CỦA BẠN" if board.turn == 'red' and game_mode == "human_vs_bot" else (
            "LƯỢT CỦA ĐỎ" if board.turn == 'red' else "LƯỢT CỦA ĐEN"
        )
        turn_val_color = COLOR_RED if board.turn == 'red' else COLOR_BLACK
        
        if board.is_in_check(board.turn):
            pulse = (math.sin(pygame.time.get_ticks() * 0.015) + 1) / 2
            if pulse > 0.5:
                turn_val_str = "!!! BỊ CHIẾU !!!"
                turn_val_color = COLOR_RED
                
        turn_val = self.small_font.render(turn_val_str, True, turn_val_color)
        surface.blit(turn_val, (turn_box.right - turn_val.get_width() - 15, turn_box.centery - turn_val.get_height() // 2))
        
        # --- Player profile ---
        play_av_center = (self.x + self.width - 40, 185)
        pygame.draw.circle(surface, COLOR_ACCENT, play_av_center, 18)
        pygame.draw.circle(surface, (55, 35, 30), play_av_center, 16)
        play_img = get_asset("avatar_player")
        if play_img:
            scaled_play = pygame.transform.smoothscale(play_img, (32, 32))
            surface.blit(scaled_play, (play_av_center[0] - 16, play_av_center[1] - 16))
        else:
            play_txt = self.tiny_font.render("KV", True, COLOR_ACCENT)
            surface.blit(play_txt, (play_av_center[0] - play_txt.get_width() // 2, play_av_center[1] - play_txt.get_height() // 2))
            
        play_lbl = self.tiny_font.render("BẠN", True, COLOR_TEXT_MUTED)
        surface.blit(play_lbl, (self.x + self.width - 68 - play_lbl.get_width(), 170))
        
        play_name_str = "Kỳ Vương" if game_mode == "human_vs_bot" else red_bot_name.split(":")[-1].strip()
        play_name_str = play_name_str or "Kỳ Vương"
        play_name = self.body_font.render(play_name_str, True, COLOR_RED if game_mode != "human_vs_bot" else COLOR_ACCENT)
        surface.blit(play_name, (self.x + self.width - 68 - play_name.get_width(), 188))
        
        # 4. Bảng Xếp Hạng & Thống Kê
        stats_rect = pygame.Rect(self.x + 15, 230, self.width - 30, 75)
        pygame.draw.rect(surface, COLOR_CARD_BG, stats_rect, 0, 8)
        pygame.draw.rect(surface, COLOR_OUTLINE, stats_rect, 1, 8)
        
        stats_lbl = self.small_font.render("Bảng Xếp Hạng & Thống Kê", True, COLOR_ACCENT)
        surface.blit(stats_lbl, (stats_rect.x + 15, stats_rect.y + 10))
        
        rec_lbl = self.small_font.render("Kỷ lục thời gian:", True, COLOR_TEXT_MUTED)
        rec_val = self.mono_font.render("02:15", True, COLOR_JADE)
        surface.blit(rec_lbl, (stats_rect.x + 15, stats_rect.y + 32))
        surface.blit(rec_val, (stats_rect.right - rec_val.get_width() - 15, stats_rect.y + 30))
        
        reward_lbl = self.small_font.render("Phần thưởng thắng:", True, COLOR_TEXT_MUTED)
        reward_val = self.mono_font.render("+50 Vàng", True, COLOR_ACCENT)
        surface.blit(reward_lbl, (stats_rect.x + 15, stats_rect.y + 52))
        surface.blit(reward_val, (stats_rect.right - reward_val.get_width() - 15, stats_rect.y + 50))
        
        # 5. Bảng Điều Khiển Thuật Toán
        algo_card_rect = pygame.Rect(self.x + 15, 315, self.width - 30, 160)
        pygame.draw.rect(surface, COLOR_CARD_BG, algo_card_rect, 0, 8)
        pygame.draw.rect(surface, COLOR_OUTLINE, algo_card_rect, 1, 8)
        
        algo_header = self.title_font.render("BẢNG ĐIỀU KHIỂN THUẬT TOÁN", True, COLOR_ACCENT)
        surface.blit(algo_header, (algo_card_rect.x + 15, algo_card_rect.y + 10))
        
        # Dropdown selection container (Combobox)
        # Determine current algorithm display name
        active_bot_name = black_bot_name if game_mode == "human_vs_bot" else (
            red_bot_name if board.turn == 'red' else black_bot_name
        )
        active_algo_key = active_bot_name.split(":")[-1].strip() if ":" in active_bot_name else active_bot_name
        
        display_algo = "Chọn chiến thuật..."
        for opt_key, opt_name, _ in ALGO_OPTIONS:
            if opt_key == active_algo_key:
                display_algo = opt_name
                break
                
        # Draw algorithm display box (static)
        pygame.draw.rect(surface, (30, 18, 14), self.dropdown_rect, 0, 4)
        pygame.draw.rect(surface, COLOR_OUTLINE, self.dropdown_rect, 1, 4)
        
        # Algorithm Label
        dd_txt = self.small_font.render(display_algo, True, COLOR_TEXT)
        surface.blit(dd_txt, (self.dropdown_rect.x + 10, self.dropdown_rect.centery - dd_txt.get_height() // 2))
        
        # Draw AI computation stats Node / Frontier / Explored
        # Update simulation counters if Bot is thinking (active_bot_name is not "Human" and turn is Bot's)
        is_bot_thinking = False
        if game_mode == "human_vs_bot" and board.turn == 'black':
            is_bot_thinking = True
        elif game_mode == "bot_vs_bot":
            is_bot_thinking = True
            
        # If thread calculation is running, increment sim counters
        if is_bot_thinking and time.time() - self.last_sim_update >= 0.15:
            self.sim_nodes = random.randint(self.sim_nodes + 5, self.sim_nodes + 120)
            self.sim_frontier = random.randint(15, 65)
            self.sim_explored = int(self.sim_nodes * random.uniform(0.6, 0.72))
            self.last_sim_update = time.time()
        elif not is_bot_thinking:
            # Idle/Last state values
            self.sim_nodes = 1284
            self.sim_frontier = 42
            self.sim_explored = 856
            
        stats_box_y = algo_card_rect.y + 76
        stats_box_w = (algo_card_rect.width - 40) // 3
        
        # Draw 3 boxes: NODE, FRONTIER, EXPLORED
        box_titles = ["NODE", "FRONTIER", "EXPLORED"]
        box_vals = [f"{self.sim_nodes:,}", f"{self.sim_frontier}", f"{self.sim_explored:,}"]
        box_colors = [COLOR_ACCENT, COLOR_JADE, COLOR_TEXT_MUTED]
        
        for idx in range(3):
            bx = algo_card_rect.x + 15 + idx * (stats_box_w + 5)
            b_rect = pygame.Rect(bx, stats_box_y, stats_box_w, 42)
            pygame.draw.rect(surface, (30, 20, 16), b_rect, 0, 4)
            pygame.draw.rect(surface, COLOR_OUTLINE, b_rect, 1, 4)
            
            # Title
            t_txt = self.tiny_font.render(box_titles[idx], True, COLOR_TEXT_MUTED)
            surface.blit(t_txt, (b_rect.centerx - t_txt.get_width() // 2, b_rect.y + 4))
            
            # Value
            v_txt = self.mono_font.render(box_vals[idx], True, box_colors[idx])
            surface.blit(v_txt, (b_rect.centerx - v_txt.get_width() // 2, b_rect.y + 20))
            
        # Draw Progress Loading bar
        progress_y = algo_card_rect.y + 130
        pygame.draw.rect(surface, (30, 20, 16), (algo_card_rect.x + 15, progress_y, algo_card_rect.width - 30, 6), 0, 3)
        
        if is_bot_thinking:
            # Pulsing/sliding progress bar
            pulse_offset = int((pygame.time.get_ticks() * 0.08) % (algo_card_rect.width - 100))
            pygame.draw.rect(surface, COLOR_ACCENT, (algo_card_rect.x + 15 + pulse_offset, progress_y, 70, 6), 0, 3)
            
            # Pulsing "ĐANG TÍNH..." text
            is_pulse_alpha = (math.sin(pygame.time.get_ticks() * 0.015) + 1) / 2 > 0.5
            calc_lbl = self.tiny_font.render("ĐANG TÍNH..." if is_pulse_alpha else "", True, COLOR_ACCENT)
            surface.blit(calc_lbl, (algo_card_rect.right - calc_lbl.get_width() - 15, progress_y + 10))
        else:
            # Idle full line progress
            pygame.draw.rect(surface, COLOR_OUTLINE, (algo_card_rect.x + 15, progress_y, algo_card_rect.width - 30, 6), 0, 3)
            calc_lbl = self.tiny_font.render("SẴN SÀNG", True, COLOR_JADE)
            surface.blit(calc_lbl, (algo_card_rect.right - calc_lbl.get_width() - 15, progress_y + 10))
            
        # 6. Move History (2 Columns: Red / Black)
        history_card_rect = pygame.Rect(self.x + 15, 485, self.width - 30, self.history_card_height)
        pygame.draw.rect(surface, COLOR_CARD_BG, history_card_rect, 0, 8)
        pygame.draw.rect(surface, COLOR_OUTLINE, history_card_rect, 1, 8)
        
        hist_lbl = self.small_font.render("LỊCH SỬ NƯỚC ĐI", True, COLOR_ACCENT)
        surface.blit(hist_lbl, (history_card_rect.x + 15, history_card_rect.y + 10))
        
        recent_moves = move_history or []
        total_moves = len(recent_moves)
        
        hist_stats = self.tiny_font.render(f"Tổng: {total_moves} nước | Đỏ: {math.ceil(total_moves/2)} | Đen: {total_moves//2}", True, COLOR_TEXT_MUTED)
        surface.blit(hist_stats, (history_card_rect.x + 15, history_card_rect.y + 32))
        
        # Grid Header for history: "ĐỎ (RED)" vs "ĐEN (BLACK)"
        hdr_y = history_card_rect.y + 54
        col_w = (history_card_rect.width - 40) // 2
        red_hdr = self.count_font.render("ĐỎ (RED)", True, COLOR_RED)
        black_hdr = self.count_font.render("ĐEN (BLACK)", True, COLOR_BLACK)
        surface.blit(red_hdr, (history_card_rect.x + 40, hdr_y))
        surface.blit(black_hdr, (history_card_rect.x + 40 + col_w, hdr_y))
        pygame.draw.line(surface, COLOR_OUTLINE, (history_card_rect.x + 15, hdr_y + 16), (history_card_rect.right - 15, hdr_y + 16), 1)
        
        # Group history into rows
        start_row_idx, history_rows = self.get_history_rows(recent_moves)
        
        start_y = history_card_rect.y + 78
        for idx, (red_m, black_m) in enumerate(history_rows):
            y = start_y + idx * 24
            row_rect = pygame.Rect(history_card_rect.x + 10, y - 2, history_card_rect.width - 25, 20)
            
            # Check highlight if it is the absolute latest move
            is_red_latest = (start_row_idx + idx) * 2 == (total_moves - 1)
            is_black_latest = (start_row_idx + idx) * 2 + 1 == (total_moves - 1)
            
            # Row index number label
            row_num_lbl = self.count_font.render(f"{start_row_idx + idx + 1}.", True, COLOR_TEXT_MUTED)
            surface.blit(row_num_lbl, (history_card_rect.x + 15, y))
            
            # Red Move Column
            red_str = self.format_move_compact(red_m)
            red_color = COLOR_ACCENT if is_red_latest and time.time() < latest_move_flash_until else COLOR_TEXT
            if "x" in red_str: red_color = COLOR_JADE
            r_lbl = self.history_font.render(red_str, True, red_color)
            surface.blit(r_lbl, (history_card_rect.x + 40, y))
            
            # Black Move Column
            if black_m:
                black_str = self.format_move_compact(black_m)
                black_color = COLOR_ACCENT if is_black_latest and time.time() < latest_move_flash_until else COLOR_TEXT
                if "x" in black_str: black_color = COLOR_JADE
                b_lbl = self.history_font.render(black_str, True, black_color)
                surface.blit(b_lbl, (history_card_rect.x + 40 + col_w, y))
                
        # Draw scrollbar if necessary
        max_rows_scroll = max(0, self._history_total - self.history_visible_rows)
        if max_rows_scroll > 0:
            track_x = history_card_rect.right - 10
            track_y = start_y
            track_h = self.history_card_height - 120
            pygame.draw.rect(surface, (50, 30, 25), (track_x, track_y, 4, track_h), 0, 2)
            
            visible_ratio = min(1.0, self.history_visible_rows / max(1, self._history_total))
            thumb_h = max(16, int(track_h * visible_ratio))
            thumb_range = max(1, track_h - thumb_h)
            thumb_y = track_y + int((thumb_range * self.history_scroll) / max_rows_scroll)
            pygame.draw.rect(surface, COLOR_ACCENT, (track_x - 1, thumb_y, 6, thumb_h), 0, 2)
            
        # Hint line at history footer
        hist_hint = self.tiny_font.render("Cuộn chuột trong bảng lịch sử để xem thêm", True, COLOR_TEXT_MUTED)
        surface.blit(hist_hint, (history_card_rect.x + 15, history_card_rect.bottom - 18))
        
        # 7. Draw Footer Controls: ĐI LẠI / GỢI Ý / ĐẦU HÀNG
        # Render action buttons (with premium outline styling)
        mouse_pos = pygame.mouse.get_pos()
        
        buttons = [
            (self.btn_undo, "ĐI LẠI", (46, 204, 113), (39, 174, 96)),
            (self.btn_hint, "GỢI Ý", (170, 110, 200), (155, 89, 182)),
            (self.btn_surrender, "ĐẦU HÀNG", (231, 76, 60), (192, 57, 43))
        ]
        
        for rect, label, hover_color, normal_color in buttons:
            is_hover = rect.collidepoint(mouse_pos)
            pygame.draw.rect(surface, hover_color if is_hover else normal_color, rect, 0, 6)
            pygame.draw.rect(surface, COLOR_ACCENT, rect, 1, 6)
            
            lbl_txt = self.body_font.render(label, True, COLOR_TEXT)
            surface.blit(lbl_txt, (rect.centerx - lbl_txt.get_width() // 2, rect.centery - lbl_txt.get_height() // 2))
            

