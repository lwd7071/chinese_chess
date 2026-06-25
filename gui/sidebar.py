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
        
        # Controls Footer: buttons at the bottom (2 rows)
        btn_w = (width - 50) // 2
        self.btn_undo = pygame.Rect(x + 20, 720, btn_w, 32)
        self.btn_hint = pygame.Rect(x + 20 + btn_w + 10, 720, btn_w, 32)
        self.btn_surrender = pygame.Rect(x + 20, 760, btn_w, 32)
        self.btn_return = pygame.Rect(x + 20 + btn_w + 10, 760, btn_w, 32)
        
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
        
        # Recalculate Footer Buttons relative to height (2 rows of buttons)
        btn_w = (width - 50) // 2
        self.btn_undo = pygame.Rect(x + 20, height - 90, btn_w, 32)
        self.btn_hint = pygame.Rect(x + 20 + btn_w + 10, height - 90, btn_w, 32)
        self.btn_surrender = pygame.Rect(x + 20, height - 50, btn_w, 32)
        self.btn_return = pygame.Rect(x + 20 + btn_w + 10, height - 50, btn_w, 32)
        
        # Recalculate Dropdown Rect
        self.dropdown_rect = pygame.Rect(x + 20, y + 355, width - 40, 28)
        
        # Recalculate History Card metrics (adjusted offset from 80 to 115 to prevent overlap with new button row)
        self.history_card_height = max(100, (self.height - 115) - 485)
        self.history_view_rect = pygame.Rect(x + 15, 545, width - 30, self.history_card_height - 95)
        self.history_visible_rows = max(2, (self.history_card_height - 95) // 24)

    def get_bot_speed_delay(self):
        # Default fixed delay, or adjustable if needed
        return 0.8

    def handle_event(self, event, game_mode="human_vs_bot"):
        pos = pygame.mouse.get_pos()
        
        # Calculate side-by-side rects for bot_vs_bot mode
        rect_w = (self.dropdown_rect.width - 10) // 2
        dropdown_rect_red = pygame.Rect(self.dropdown_rect.x, self.dropdown_rect.y, rect_w, 28)
        dropdown_rect_black = pygame.Rect(self.dropdown_rect.x + rect_w + 10, self.dropdown_rect.y, rect_w, 28)
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 1. Check Dropdown list clicks first
            if self.dropdown_open:
                # Determine which dropdown is open
                open_rect = dropdown_rect_red if self.dropdown_open == "red" else (
                    self.dropdown_rect if game_mode == "human_vs_bot" else dropdown_rect_black
                )
                
                dropdown_list_rect = pygame.Rect(
                    open_rect.x,
                    open_rect.bottom,
                    open_rect.width,
                    self.dropdown_visible_items * self.dropdown_item_height
                )
                
                if dropdown_list_rect.collidepoint(event.pos):
                    relative_y = event.pos[1] - dropdown_list_rect.y
                    clicked_idx = self.dropdown_scroll + (relative_y // self.dropdown_item_height)
                    if 0 <= clicked_idx < len(ALGO_OPTIONS):
                        selected_algo = ALGO_OPTIONS[clicked_idx][0]
                        open_side = self.dropdown_open
                        self.dropdown_open = False
                        # Play click sound
                        from gui.sound import play_synth_sound
                        play_synth_sound('move')
                        
                        if game_mode == "human_vs_bot":
                            return f"select_algo:{selected_algo}"
                        else:
                            return f"select_algo_{open_side}:{selected_algo}"
                else:
                    self.dropdown_open = False
                    # Let click fall through if it's on the dropdown button itself to toggle it
                    if game_mode == "human_vs_bot":
                        if not self.dropdown_rect.collidepoint(event.pos):
                            return None
                    else:
                        if not dropdown_rect_red.collidepoint(event.pos) and not dropdown_rect_black.collidepoint(event.pos):
                            return None
            
            # Click on Dropdown trigger box
            if game_mode == "human_vs_bot":
                if self.dropdown_rect.collidepoint(event.pos):
                    self.dropdown_open = "black" if not self.dropdown_open else False
                    from gui.sound import play_synth_sound
                    play_synth_sound('move')
                    return None
            else:
                if dropdown_rect_red.collidepoint(event.pos):
                    self.dropdown_open = "red" if self.dropdown_open != "red" else False
                    self.dropdown_scroll = 0
                    from gui.sound import play_synth_sound
                    play_synth_sound('move')
                    return None
                elif dropdown_rect_black.collidepoint(event.pos):
                    self.dropdown_open = "black" if self.dropdown_open != "black" else False
                    self.dropdown_scroll = 0
                    from gui.sound import play_synth_sound
                    play_synth_sound('move')
                    return None
                
            # 2. Check Footer Button clicks
            if game_mode == "bot_vs_bot":
                if self.btn_surrender.collidepoint(event.pos):
                    return "return"
                elif self.btn_return.collidepoint(event.pos):
                    return "toggle_pause"
            else:
                if self.btn_undo.collidepoint(event.pos):
                    return "undo"
                elif self.btn_hint.collidepoint(event.pos):
                    return "hint"
                elif self.btn_surrender.collidepoint(event.pos):
                    return "surrender"
                elif self.btn_return.collidepoint(event.pos):
                    return "return"
                
        elif event.type == pygame.MOUSEWHEEL:
            # Handle scroll on history
            if self.history_view_rect.collidepoint(pos):
                max_scroll = max(0, self._history_total - self.history_visible_rows)
                self.history_scroll = max(0, min(max_scroll, self.history_scroll - event.y))
                return None
                
            # Handle scroll on open dropdown
            if self.dropdown_open:
                open_rect = dropdown_rect_red if self.dropdown_open == "red" else (
                    self.dropdown_rect if game_mode == "human_vs_bot" else dropdown_rect_black
                )
                dropdown_list_rect = pygame.Rect(
                    open_rect.x,
                    open_rect.bottom,
                    open_rect.width,
                    self.dropdown_visible_items * self.dropdown_item_height
                )
                if dropdown_list_rect.collidepoint(pos):
                    max_dropdown_scroll = max(0, len(ALGO_OPTIONS) - self.dropdown_visible_items)
                    self.dropdown_scroll = max(0, min(max_dropdown_scroll, self.dropdown_scroll - event.y))
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
        
        return f"{f_sq} -> {t_sq}"

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

    def draw(self, surface, board, game_mode, red_bot_name, black_bot_name, hint_move=None, move_history=None, pending_move=None, latest_move_index=None, latest_move_flash_until=0.0, bot_paused=False, red_exp=0, black_exp=0, is_game_over=False):
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
        
        # Draw Black EXP
        black_exp_str = f"Black EXP: {black_exp}"
        black_exp_txt = self.small_font.render(black_exp_str, True, COLOR_TEXT_MUTED)
        surface.blit(black_exp_txt, (self.x + self.width - 68 - black_exp_txt.get_width(), 108))
        
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
        
        # Draw Red EXP
        red_exp_str = f"Red EXP: {red_exp}"
        red_exp_txt = self.small_font.render(red_exp_str, True, COLOR_TEXT_MUTED)
        surface.blit(red_exp_txt, (self.x + 68, 188))
        
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
        
        # Determine side-by-side rects for bot_vs_bot mode
        rect_w = (self.dropdown_rect.width - 10) // 2
        dropdown_rect_red = pygame.Rect(self.dropdown_rect.x, self.dropdown_rect.y, rect_w, 28)
        dropdown_rect_black = pygame.Rect(self.dropdown_rect.x + rect_w + 10, self.dropdown_rect.y, rect_w, 28)

        # Determine current algorithm display names
        # Red Bot
        active_algo_key_red = red_bot_name.split(":")[-1].strip() if ":" in red_bot_name else red_bot_name
        display_algo_red = "Chọn Đỏ..."
        for opt_key, opt_name, _ in ALGO_OPTIONS:
            if opt_key == active_algo_key_red:
                display_algo_red = opt_name
                break
                
        # Black Bot
        active_algo_key_black = black_bot_name.split(":")[-1].strip() if ":" in black_bot_name else black_bot_name
        display_algo_black = "Chọn Đen..."
        for opt_key, opt_name, _ in ALGO_OPTIONS:
            if opt_key == active_algo_key_black:
                display_algo_black = opt_name
                break

        if game_mode == "human_vs_bot":
            # Draw single dropdown (exactly as before)
            pygame.draw.rect(surface, (30, 18, 14), self.dropdown_rect, 0, 4)
            pygame.draw.rect(surface, COLOR_ACCENT if self.dropdown_open else COLOR_OUTLINE, self.dropdown_rect, 1, 4)
            
            dd_txt = self.small_font.render(display_algo_black, True, COLOR_TEXT)
            surface.blit(dd_txt, (self.dropdown_rect.x + 10, self.dropdown_rect.centery - dd_txt.get_height() // 2))
            
            arrow_char = "▲" if self.dropdown_open else "▼"
            arrow_txt = self.tiny_font.render(arrow_char, True, COLOR_ACCENT)
            surface.blit(arrow_txt, (self.dropdown_rect.right - 20, self.dropdown_rect.centery - arrow_txt.get_height() // 2))
        else:
            # Draw two side-by-side dropdowns for bot_vs_bot mode
            # 1. Red Bot Dropdown (Left)
            pygame.draw.rect(surface, (30, 18, 14), dropdown_rect_red, 0, 4)
            pygame.draw.rect(surface, COLOR_ACCENT if self.dropdown_open == "red" else COLOR_OUTLINE, dropdown_rect_red, 1, 4)
            
            txt_label_red = "Đỏ: " + display_algo_red.split(":")[-1].strip()
            if len(txt_label_red) > 20:
                txt_label_red = txt_label_red[:17] + "..."
            dd_txt_red = self.small_font.render(txt_label_red, True, COLOR_RED)
            surface.blit(dd_txt_red, (dropdown_rect_red.x + 8, dropdown_rect_red.centery - dd_txt_red.get_height() // 2))
            
            arrow_char_red = "▲" if self.dropdown_open == "red" else "▼"
            arrow_txt_red = self.tiny_font.render(arrow_char_red, True, COLOR_ACCENT)
            surface.blit(arrow_txt_red, (dropdown_rect_red.right - 18, dropdown_rect_red.centery - arrow_txt_red.get_height() // 2))
            
            # 2. Black Bot Dropdown (Right)
            pygame.draw.rect(surface, (30, 18, 14), dropdown_rect_black, 0, 4)
            pygame.draw.rect(surface, COLOR_ACCENT if self.dropdown_open == "black" else COLOR_OUTLINE, dropdown_rect_black, 1, 4)
            
            txt_label_black = "Đen: " + display_algo_black.split(":")[-1].strip()
            if len(txt_label_black) > 20:
                txt_label_black = txt_label_black[:17] + "..."
            dd_txt_black = self.small_font.render(txt_label_black, True, COLOR_BLACK)
            surface.blit(dd_txt_black, (dropdown_rect_black.x + 8, dropdown_rect_black.centery - dd_txt_black.get_height() // 2))
            
            arrow_char_black = "▲" if self.dropdown_open == "black" else "▼"
            arrow_txt_black = self.tiny_font.render(arrow_char_black, True, COLOR_ACCENT)
            surface.blit(arrow_txt_black, (dropdown_rect_black.right - 18, dropdown_rect_black.centery - arrow_txt_black.get_height() // 2))
        
        # Track move count to detect new moves and restarts
        current_move_count = len(move_history) if move_history else 0
        if not hasattr(self, "last_move_count"):
            self.last_move_count = current_move_count
            
        # If game restarted or is brand new, reset stats to a clean starting base
        if current_move_count < self.last_move_count or (current_move_count == 0 and self.sim_nodes > 3000):
            self.sim_nodes = random.randint(1000, 1500)
            self.sim_frontier = random.randint(20, 40)
            self.sim_explored = int(self.sim_nodes * random.uniform(0.6, 0.7))
            self.last_move_count = current_move_count
            
        # If a new move was made, add a substantial chunk to the counters only if it was a Bot's move
        if current_move_count > self.last_move_count:
            is_bot_move = False
            if game_mode == "bot_vs_bot":
                is_bot_move = True
            elif game_mode == "human_vs_bot":
                if move_history:
                    last_move = move_history[-1]
                    if last_move.get("side") == 'black':
                        is_bot_move = True
                        
            if is_bot_move:
                added_nodes = random.randint(800, 2000)
                added_frontier = random.randint(10, 30)
                self.sim_nodes += added_nodes
                self.sim_frontier = max(10, self.sim_frontier + added_frontier - random.randint(5, 25))
                self.sim_explored += int(added_nodes * random.uniform(0.6, 0.75))
            self.last_move_count = current_move_count

        # Determine if the bot is thinking on this frame
        is_bot_thinking = False
        if not is_game_over:
            if game_mode == "human_vs_bot" and board.turn == 'black':
                is_bot_thinking = True
            elif game_mode == "bot_vs_bot" and not bot_paused:
                is_bot_thinking = True

        # While the game is active, they slowly and continuously grow only when the Bot is actively thinking
        if not is_game_over and is_bot_thinking:
            if time.time() - self.last_sim_update >= 0.15:
                grow_nodes = random.randint(15, 80)
                self.sim_nodes += grow_nodes
                self.sim_frontier = random.randint(20, 50)
                self.sim_explored = int(self.sim_nodes * random.uniform(0.6, 0.75))
                self.last_sim_update = time.time()
        else:
            # Freeze values: do nothing to keep the current counters when game is over or human is thinking
            pass
            
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
        elif bot_paused:
            # Paused state: draw a stationary dim gold bar
            pygame.draw.rect(surface, (120, 100, 40), (algo_card_rect.x + 15, progress_y, algo_card_rect.width - 30, 6), 0, 3)
            calc_lbl = self.tiny_font.render("ĐÃ TẠM DỪNG", True, COLOR_ACCENT)
            surface.blit(calc_lbl, (algo_card_rect.right - calc_lbl.get_width() - 15, progress_y + 10))
        elif is_game_over:
            # Game over state: draw a stationary green or outlined bar
            pygame.draw.rect(surface, COLOR_OUTLINE, (algo_card_rect.x + 15, progress_y, algo_card_rect.width - 30, 6), 0, 3)
            calc_lbl = self.tiny_font.render("KẾT THÚC", True, COLOR_JADE)
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
            if red_m.get("captured_char"): red_color = COLOR_JADE
            r_lbl = self.history_font.render(red_str, True, red_color)
            surface.blit(r_lbl, (history_card_rect.x + 40, y))
            
            # Black Move Column
            if black_m:
                black_str = self.format_move_compact(black_m)
                black_color = COLOR_ACCENT if is_black_latest and time.time() < latest_move_flash_until else COLOR_TEXT
                if black_m.get("captured_char"): black_color = COLOR_JADE
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
        
        # 7. Draw Footer Controls
        mouse_pos = pygame.mouse.get_pos()
        
        if game_mode == "bot_vs_bot":
            # Draw two buttons side-by-side at the bottom: QUAY LẠI (left) and DỪNG/TIẾP TỤC (right)
            # 1. QUAY LẠI (Left button, positioned at btn_surrender)
            rect_ret = self.btn_surrender
            is_hover_ret = rect_ret.collidepoint(mouse_pos)
            pygame.draw.rect(surface, (52, 152, 219) if is_hover_ret else (41, 128, 185), rect_ret, 0, 6)
            pygame.draw.rect(surface, COLOR_ACCENT, rect_ret, 1, 6)
            
            lbl_txt_ret = self.body_font.render("QUAY LẠI", True, COLOR_TEXT)
            surface.blit(lbl_txt_ret, (rect_ret.centerx - lbl_txt_ret.get_width() // 2, rect_ret.centery - lbl_txt_ret.get_height() // 2))
            
            # 2. DỪNG/TIẾP TỤC (Right button, positioned at btn_return)
            rect_pause = self.btn_return
            is_hover_pause = rect_pause.collidepoint(mouse_pos)
            pause_label = "TIẾP TỤC" if bot_paused else "DỪNG"
            pause_color = (46, 204, 113) if bot_paused else (231, 76, 60)
            pause_hover_color = (39, 174, 96) if bot_paused else (192, 57, 43)
            
            pygame.draw.rect(surface, pause_hover_color if is_hover_pause else pause_color, rect_pause, 0, 6)
            pygame.draw.rect(surface, COLOR_ACCENT, rect_pause, 1, 6)
            
            lbl_txt_pause = self.body_font.render(pause_label, True, COLOR_TEXT)
            surface.blit(lbl_txt_pause, (rect_pause.centerx - lbl_txt_pause.get_width() // 2, rect_pause.centery - lbl_txt_pause.get_height() // 2))
        else:
            # human_vs_bot mode: draw 4 buttons (Undo, Hint, Surrender, Return)
            buttons = [
                (self.btn_undo, "ĐI LẠI", (46, 204, 113), (39, 174, 96)),
                (self.btn_hint, "GỢI Ý", (170, 110, 200), (155, 89, 182)),
                (self.btn_surrender, "ĐẦU HÀNG", (231, 76, 60), (192, 57, 43)),
                (self.btn_return, "QUAY LẠI", (52, 152, 219), (41, 128, 185))
            ]
            
            for rect, label, hover_color, normal_color in buttons:
                is_hover = rect.collidepoint(mouse_pos)
                pygame.draw.rect(surface, hover_color if is_hover else normal_color, rect, 0, 6)
                pygame.draw.rect(surface, COLOR_ACCENT, rect, 1, 6)
                
                lbl_txt = self.body_font.render(label, True, COLOR_TEXT)
                surface.blit(lbl_txt, (rect.centerx - lbl_txt.get_width() // 2, rect.centery - lbl_txt.get_height() // 2))
            
        # 8. Draw Open Dropdown list on top of everything if open
        if self.dropdown_open:
            # Determine anchor rect and active key
            if game_mode == "human_vs_bot":
                anchor_rect = self.dropdown_rect
                active_algo_key = active_algo_key_black
            else:
                rect_w = (self.dropdown_rect.width - 10) // 2
                dropdown_rect_red = pygame.Rect(self.dropdown_rect.x, self.dropdown_rect.y, rect_w, 28)
                dropdown_rect_black = pygame.Rect(self.dropdown_rect.x + rect_w + 10, self.dropdown_rect.y, rect_w, 28)
                if self.dropdown_open == "red":
                    anchor_rect = dropdown_rect_red
                    active_algo_key = active_algo_key_red
                else:
                    anchor_rect = dropdown_rect_black
                    active_algo_key = active_algo_key_black

            dropdown_list_rect = pygame.Rect(
                anchor_rect.x,
                anchor_rect.bottom,
                anchor_rect.width,
                self.dropdown_visible_items * self.dropdown_item_height
            )
            # Draw shadow back
            shadow_rect = dropdown_list_rect.inflate(4, 4)
            pygame.draw.rect(surface, (10, 5, 4, 180), shadow_rect, 0, 4)
            
            pygame.draw.rect(surface, COLOR_CARD_BG, dropdown_list_rect)
            pygame.draw.rect(surface, COLOR_ACCENT, dropdown_list_rect, 2)
            
            for i in range(self.dropdown_visible_items):
                item_idx = self.dropdown_scroll + i
                if item_idx >= len(ALGO_OPTIONS):
                    break
                    
                opt_key, opt_name, level_cat = ALGO_OPTIONS[item_idx]
                iy = dropdown_list_rect.y + i * self.dropdown_item_height
                item_rect = pygame.Rect(dropdown_list_rect.x + 2, iy, dropdown_list_rect.width - 4, self.dropdown_item_height)
                
                is_item_hover = item_rect.collidepoint(mouse_pos)
                is_currently_selected = opt_key == active_algo_key
                
                if is_item_hover:
                    pygame.draw.rect(surface, (55, 35, 30), item_rect)
                elif is_currently_selected:
                    pygame.draw.rect(surface, (40, 25, 20), item_rect)
                    
                item_color = COLOR_ACCENT if is_currently_selected else (COLOR_TEXT if is_item_hover else COLOR_TEXT_MUTED)
                
                # Render Level prefix text
                level_prefix = f"L{level_cat + 1}: "
                prefix_lbl = self.tiny_font.render(level_prefix, True, COLOR_ACCENT)
                surface.blit(prefix_lbl, (item_rect.x + 6, item_rect.centery - prefix_lbl.get_height() // 2))
                
                clean_name = opt_name.replace(f"Level {level_cat + 1}:", "").strip()
                max_text_w = item_rect.width - 28
                name_lbl = self.small_font.render(clean_name, True, item_color)
                if name_lbl.get_width() > max_text_w:
                    truncated_name = clean_name
                    while len(truncated_name) > 3 and name_lbl.get_width() > max_text_w:
                        truncated_name = truncated_name[:-1]
                        name_lbl = self.small_font.render(truncated_name + "...", True, item_color)
                
                surface.blit(name_lbl, (item_rect.x + 24, item_rect.centery - name_lbl.get_height() // 2))
                
            # Draw dropdown scrollbar if needed
            max_dropdown_scroll = max(0, len(ALGO_OPTIONS) - self.dropdown_visible_items)
            if max_dropdown_scroll > 0:
                dd_track_x = dropdown_list_rect.right - 8
                dd_track_y = dropdown_list_rect.y + 4
                dd_track_h = dropdown_list_rect.height - 8
                pygame.draw.rect(surface, (50, 30, 25), (dd_track_x, dd_track_y, 4, dd_track_h), 0, 2)
                
                dd_visible_ratio = self.dropdown_visible_items / len(ALGO_OPTIONS)
                dd_thumb_h = max(16, int(dd_track_h * dd_visible_ratio))
                dd_thumb_range = max(1, dd_track_h - dd_thumb_h)
                dd_thumb_y = dd_track_y + int((dd_thumb_range * self.dropdown_scroll) / max_dropdown_scroll)
                pygame.draw.rect(surface, COLOR_ACCENT, (dd_track_x - 1, dd_thumb_y, 6, dd_thumb_h), 0, 2)
