# Main launcher of Xiangqi AI Game in Python + Pygame (Royal Theme Redesign)
import os
import sys
import threading
import time

import pygame

# Adjust path to find submodules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai import AI_REGISTRY
from ai.step_recorder import StepRecorder
from game.board import Board
from game.rules import has_lost, is_in_check, is_no_cross_river_pieces
from gui.easing import ease_out_back
from gui.menu import StartMenu
from gui.renderer import Renderer
from gui.settings import SettingsScreen
from gui.shop import ShopScreen
from gui.sidebar import Sidebar
from gui.sound import play_synth_sound
from gui.visualizer import StepController, VisualizerPanel

# Screen Dimensions
WIDTH = 1100
HEIGHT = 820

# Color Palette constants (Matching sidebar theme)
COLOR_ACCENT = (242, 202, 80)  # Antique Gold
COLOR_OUTLINE = (77, 70, 53)  # Outline border
COLOR_TEXT = (250, 220, 213)  # On-surface text
COLOR_TEXT_MUTED = (180, 165, 150)  # Muted beige
COLOR_RED = (231, 76, 60)  # Red turn/side
COLOR_BLACK = (241, 196, 15)  # Black turn/side


def calculate_remaining_piece_score(board, winner_color):
    piece_values = {"P": 10, "A": 20, "E": 20, "H": 45, "C": 45, "R": 90, "G": 0}
    score = 0
    for row in board.matrix:
        for piece in row:
            if piece and piece.color == winner_color:
                score += piece_values.get(piece.name, 0)
    return score


def calculate_win_exp(board, winner_color):
    score = calculate_remaining_piece_score(board, winner_color)
    return 100 + score // 2


class GameController:
    def __init__(self):
        pygame.init()
        try:
            pygame.mixer.init()
        except Exception:
            print("Warning: pygame.mixer.init() failed. Running without sound.")

        self.width = WIDTH
        self.height = HEIGHT
        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.RESIZABLE
        )
        pygame.display.set_caption("Hoàng Gia Tượng Kỳ - Board Game Dashboard")
        self.clock = pygame.time.Clock()

        # Init GUI modules
        self.renderer = Renderer(cell_size=60, offset_x=40, offset_y=80)
        self.sidebar = Sidebar(
            x=620,
            y=0,
            width=480,
            height=self.height,
            chinese_supported=self.renderer.chinese_supported,
            font_name=self.renderer.font_name,
        )
        self.menu = StartMenu(width=self.width, height=self.height)
        self.shop = ShopScreen(width=self.width, height=self.height)
        self.settings = SettingsScreen(width=self.width, height=self.height)

        self.red_exp = self.settings.data.get("exp", 0)
        self.black_exp = 0
        self.exp_awarded = False

        self.state = "menu"  # menu, game, shop, settings, game_over
        # Step-by-step visualization (for report mode)
        self.report_mode = False
        self.step_recorder = StepRecorder()
        self.visualizer = VisualizerPanel(
            x=620,
            y=0,
            width=480,
            height=self.height,
            chinese_supported=self.renderer.chinese_supported,
            font_name=self.renderer.font_name,
        )
        self.step_controller = StepController()

        self.state = "menu"  # menu, game, shop, game_over

        # In-game wealth/skin storage (kept in-memory)
        self.gold = 1250
        self.owned_boards = ["classic_wood"]
        self.owned_pieces = ["classic_wood_piece"]
        self.equipped_board = "classic_wood"
        self.equipped_piece = "classic_wood_piece"
        self.shop_return_state = "menu"

        # Game State Variables
        self.board = None
        self.selected_pos = None
        self.valid_moves = []
        self.hint_move = None
        self.game_start_time = None
        self.game_end_time = None
        self.pending_move = None
        self.pending_ai_move = None
        self.latest_move_index = None
        self.latest_move_flash_until = 0.0

        # Top Nav Menu Tabs (Rect coordinates) - calculated dynamically
        self.btn_top_match = pygame.Rect(0, 0, 0, 0)
        self.btn_top_shop = pygame.Rect(0, 0, 0, 0)
        self.btn_top_settings = pygame.Rect(0, 0, 0, 0)

        # Temporary popup state
        self.popup_message = ""
        self.popup_timer = 0.0

        # AI threading state
        self.ai_thread = None
        self.ai_result = None
        self.ai_lock = threading.Lock()
        self.last_bot_move_time = 0
        self.bot_paused = False

        # Animation state
        self.animation = None

        # Game Over state variables - calculated dynamically
        self.game_over_result = ""
        self.btn_game_over_retry = pygame.Rect(0, 0, 0, 0)
        self.btn_game_over_menu = pygame.Rect(0, 0, 0, 0)

        # Hover tooltip state
        self.hover_pos = None
        self.hover_piece = None
        self.hover_start_time = 0.0
        self.hover_triggered = False

        # Perform initial layout calculation
        self.recalculate_layout()

    def recalculate_layout(self):
        # 1. Update widths and heights
        self.sidebar_width = max(400, min(480, int(self.width * 0.4)))
        self.board_width = self.width - self.sidebar_width
        self.board_height = self.height

        # 2. Update top navigation tabs
        nav_start_x = self.board_width // 2 - 130
        self.btn_top_match = pygame.Rect(nav_start_x, 20, 80, 32)
        self.btn_top_shop = pygame.Rect(nav_start_x + 90, 20, 80, 32)
        self.btn_top_settings = pygame.Rect(nav_start_x + 180, 20, 80, 32)

        # 3. Update game over buttons
        self.btn_game_over_retry = pygame.Rect(
            self.width // 2 - 160, self.height // 2 + 30, 140, 40
        )
        self.btn_game_over_menu = pygame.Rect(
            self.width // 2 + 20, self.height // 2 + 30, 140, 40
        )

        # 4. Update board grid coordinates (cell_size, offset_x, offset_y)
        max_grid_w = self.board_width - 110
        max_grid_h = self.height - 72 - 100
        cell_size_w = max_grid_w / 8
        cell_size_h = max_grid_h / 9
        cell_size = int(min(cell_size_w, cell_size_h))
        cell_size = max(40, min(80, cell_size))  # Limit between 40 and 80

        grid_w = 8 * cell_size
        grid_h = 9 * cell_size
        offset_x = int((self.board_width - grid_w) / 2)
        offset_y = int(72 + ((self.height - 72) - grid_h) / 2)

        # Update renderer layout
        self.renderer.update_layout(
            cell_size, offset_x, offset_y, self.board_width, self.board_height
        )

        # Update sidebar layout
        self.sidebar.update_layout(self.board_width, 0, self.sidebar_width, self.height)

        # Update visualizer layout
        if hasattr(self, "visualizer") and self.visualizer:
            self.visualizer.update_layout(
                self.board_width, 0, self.sidebar_width, self.height
            )

        # Update menu layout
        self.menu.update_layout(self.width, self.height)

        # Update shop layout
        self.shop.update_layout(self.width, self.height)

        # Update settings layout
        self.settings.update_layout(self.width, self.height)

    def start_new_game(self):
        self.board = Board()
        self.selected_pos = None
        self.valid_moves = []
        self.hint_move = None
        self.pending_move = None
        self.pending_ai_move = None
        self.latest_move_index = None
        self.latest_move_flash_until = 0.0
        self.ai_thread = None
        self.ai_result = None
        self.animation = None
        self.last_bot_move_time = time.time()
        self.game_over_result = ""
        self.bot_paused = False
        self.exp_awarded = False
        self.red_exp = self.settings.data.get("exp", 0)
        self.step_recorder.clear()
        self.step_controller = StepController()
        self.game_start_time = time.time()
        self.game_end_time = None

    def show_popup(self, message):
        self.popup_message = message
        self.popup_timer = time.time() + 2.0

    def trigger_move_animation(self, from_pos, to_pos):
        piece = self.board.get_piece(from_pos)
        captured = self.board.get_piece(to_pos)

        self.pending_move = {
            "side": self.board.turn,
            "from_pos": from_pos,
            "to_pos": to_pos,
            "piece_name": piece.name if piece else None,
            "piece_char": piece.char if piece else None,
            "captured_name": captured.name if captured else None,
            "captured_char": captured.char if captured else None,
            "pending": True,
        }

        self.board.move_log.append(self.pending_move)
        visible_rows = getattr(self.sidebar, "history_visible_rows", 6)
        if not isinstance(visible_rows, int):
            visible_rows = 6

        # Group historical pair rows length calculation
        pair_rows_count = len(self.board.move_log) // 2 + (len(self.board.move_log) % 2)
        self.sidebar.history_scroll = max(0, pair_rows_count - visible_rows)
        self.latest_move_index = len(self.board.move_log) - 1
        self.latest_move_flash_until = time.time() + 2.0

        x1, y1 = self.renderer.get_xy(from_pos[0], from_pos[1])
        x2, y2 = self.renderer.get_xy(to_pos[0], to_pos[1])

        self.animation = {
            "piece": piece,
            "from_pos": from_pos,
            "to_pos": to_pos,
            "from_xy": (x1, y1),
            "to_xy": (x2, y2),
            "start_time": time.time(),
            "duration": 0.3,
            "captured": captured,
        }

    def run(self):
        running = True
        while running:
            self.clock.tick(60)  # 60 FPS

            # 1. Handle Events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    w = max(1000, event.w)
                    h = max(750, event.h)
                    self.width, self.height = w, h
                    self.screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
                    self.recalculate_layout()

                if self.state == "menu":
                    res = self.menu.handle_event(event)
                    if res == "game":
                        self.start_new_game()
                        self.state = "game"
                    elif res == "shop":
                        self.state = "shop"
                        self.shop_return_state = "menu"
                    elif res == "settings":
                        self.state = "settings"
                        self.shop_return_state = "menu"

                elif self.state == "shop":
                    res = self.shop.handle_event(event, self)
                    if res == "menu":
                        self.state = self.shop_return_state

                elif self.state == "settings":
                    res = self.settings.handle_event(event, self)
                    if res == "menu":
                        self.state = self.shop_return_state

                elif self.state == "game" and not self.animation:
                    # Check Top Bar click first
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mx, my = event.pos
                        if self.btn_top_shop.collidepoint(event.pos):
                            self.state = "shop"
                            self.shop_return_state = "game"
                            play_synth_sound("move")
                            continue
                        elif self.btn_top_settings.collidepoint(event.pos):
                            self.state = "settings"
                            self.shop_return_state = "game"
                            play_synth_sound("move")
                            continue

                    # Hotkey to toggle report mode
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        self.report_mode = not self.report_mode
                        self.show_popup(
                            f"Report Mode: {'ON' if self.report_mode else 'OFF'}"
                        )
                        if not self.report_mode:
                            self.step_recorder.clear()
                            self.pending_ai_move = None
                        play_synth_sound("move")
                        continue

                    # Sidebar / Visualizer / Board click actions
                    if (
                        self.report_mode
                        and self.step_recorder.total_steps() > 0
                        and self.ai_thread is None
                    ):
                        vis_action = self.visualizer.handle_event(
                            event, self.step_controller, self.step_recorder
                        )
                        if vis_action == "finish" and getattr(
                            self, "pending_ai_move", None
                        ):
                            self.trigger_move_animation(
                                self.pending_ai_move[0], self.pending_ai_move[1]
                            )
                            self.step_recorder.clear()
                            self.pending_ai_move = None
                            continue
                    else:
                        # Sidebar click actions
                        action = self.sidebar.handle_event(event, self.menu.game_mode)
                        if action:
                            if (
                                action.startswith("select_algo:")
                                or action.startswith("select_algo_red:")
                                or action.startswith("select_algo_black:")
                            ):
                                new_algo = action.split(":")[-1]
                                # Find the level category of the new algorithm
                                level_cat = 0
                                from gui.sidebar import ALGO_OPTIONS

                                for opt_key, _, lvl in ALGO_OPTIONS:
                                    if opt_key == new_algo:
                                        level_cat = lvl
                                        break

                                if action.startswith("select_algo_red:"):
                                    self.menu.red_bot_algo = new_algo
                                    self.menu.red_bot_level = level_cat
                                elif action.startswith("select_algo_black:"):
                                    self.menu.black_bot_algo = new_algo
                                    self.menu.black_bot_level = level_cat
                                else:  # select_algo:
                                    if self.menu.game_mode == "human_vs_bot":
                                        self.menu.black_bot_algo = new_algo
                                        self.menu.black_bot_level = level_cat
                                    else:
                                        if self.board.turn == "red":
                                            self.menu.red_bot_algo = new_algo
                                            self.menu.red_bot_level = level_cat
                                        else:
                                            self.menu.black_bot_algo = new_algo
                                            self.menu.black_bot_level = level_cat
                            elif action == "new_game":
                                self.start_new_game()
                            elif action == "surrender":
                                win_exp = calculate_win_exp(self.board, "black")
                                self.game_over_result = f"Black wins! +{win_exp} EXP"
                                self.state = "game_over"
                                self.game_end_time = time.time()
                                play_synth_sound("check")
                                self.award_game_over_exp("black", win_exp)
                            elif action == "return":
                                if self.menu.game_mode == "bot_vs_bot":
                                    self.state = "menu"
                                    self.menu.state = "mode_select"
                                    self.menu.trigger_transition()
                                else:
                                    if self.state == "game":
                                        self.show_popup(
                                            "Bạn phải đầu hàng trước khi quay lại!"
                                        )
                                    else:
                                        self.state = "menu"
                                        self.menu.state = "mode_select"
                                        self.menu.trigger_transition()
                            elif action == "toggle_pause":
                                self.bot_paused = not self.bot_paused
                                play_synth_sound("move")
                            elif action == "undo":
                                if self.menu.game_mode == "human_vs_bot":
                                    if len(self.board.history) >= 2:
                                        self.board.undo_move()
                                        self.board.undo_move()
                                else:
                                    if len(self.board.history) >= 1:
                                        self.board.undo_move()
                                self.selected_pos = None
                                self.valid_moves = []
                                self.hint_move = None
                            elif action == "hint":
                                self.hint_move = AI_REGISTRY["Alpha-Beta"](self.board)
                                play_synth_sound("move")

                        # Board piece click — select or move pieces
                        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            board_pos = self.renderer.get_board_pos_from_screen(
                                event.pos
                            )
                            if board_pos:
                                self.handle_human_click(board_pos)

                elif self.state == "game_over":
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.btn_game_over_retry.collidepoint(event.pos):
                            self.start_new_game()
                            self.state = "game"
                        elif self.btn_game_over_menu.collidepoint(event.pos):
                            self.state = "menu"
                            self.menu.state = "mode_select"
                            self.menu.trigger_transition()

            # 2. Game Logic / Bot turns
            if self.state == "game" and not self.animation:
                if (
                    self.report_mode
                    and self.step_recorder.total_steps() > 0
                    and self.ai_thread is None
                ):
                    if self.step_controller.update(
                        self.step_recorder
                    ) == "finish" and getattr(self, "pending_ai_move", None):
                        self.trigger_move_animation(
                            self.pending_ai_move[0], self.pending_ai_move[1]
                        )
                        self.step_recorder.clear()
                        self.pending_ai_move = None
                else:
                    self.handle_bot_turns()

            # Update hover state for tooltip delay (1s)
            if self.state == "game" and not self.animation:
                curr_mouse_pos = pygame.mouse.get_pos()
                board_pos = self.renderer.get_board_pos_from_screen(curr_mouse_pos)
                if board_pos:
                    piece = self.board.get_piece(board_pos)
                    if piece:
                        if self.hover_pos == board_pos:
                            if not self.hover_triggered and (
                                time.time() - self.hover_start_time >= 1.0
                            ):
                                self.hover_triggered = True
                                self.hover_piece = piece
                        else:
                            self.hover_pos = board_pos
                            self.hover_piece = None
                            self.hover_start_time = time.time()
                            self.hover_triggered = False
                    else:
                        self.hover_pos = None
                        self.hover_piece = None
                        self.hover_start_time = 0.0
                        self.hover_triggered = False
                else:
                    self.hover_pos = None
                    self.hover_piece = None
                    self.hover_start_time = 0.0
                    self.hover_triggered = False
            else:
                self.hover_pos = None
                self.hover_piece = None
                self.hover_start_time = 0.0
                self.hover_triggered = False

            # 3. Update Animations & Particles
            self.update_animation()
            if self.state in ["game", "game_over"]:
                self.renderer.update_particles()

            # 4. Drawing Phase
            if self.state == "menu":
                self.menu.draw(self.screen)
            elif self.state == "shop":
                self.shop.draw(self.screen, self)
            elif self.state == "settings":
                self.settings.draw(self.screen)
            elif self.state in ["game", "game_over"]:
                self.draw_game_screen()
                if self.state == "game_over":
                    self.draw_game_over_overlay()

            pygame.display.flip()

        pygame.quit()

    def handle_human_click(self, pos):
        # Prevent moves when it's not the human's turn or when the visualizer is active
        if self.menu.game_mode != "human_vs_bot":
            return

        is_visualizer_active = self.report_mode and (
            self.step_recorder.total_steps() > 0 or self.ai_thread is not None
        )

        if self.board.turn != "red" or self.pending_ai_move or is_visualizer_active:
            self.show_popup("Chưa đến lượt bạn!")
            return

        piece = self.board.get_piece(pos)

        # If we click on our own piece, select it
        if piece and piece.color == "red":
            self.selected_pos = pos
            all_legal = self.board.get_all_legal_moves("red")
            self.valid_moves = [
                to_pos for from_pos, to_pos in all_legal if from_pos == pos
            ]
            self.hint_move = None

        # If we clicked on a valid move cell, execute it
        elif self.selected_pos and pos in self.valid_moves:
            self.trigger_move_animation(self.selected_pos, pos)
            self.selected_pos = None
            self.valid_moves = []

    def handle_bot_turns(self):
        if self.menu.game_mode == "bot_vs_bot" and self.bot_paused:
            return

        is_bot = False
        bot_algo = ""

        if self.menu.game_mode == "human_vs_bot" and self.board.turn == "black":
            is_bot = True
            bot_algo = self.menu.black_bot_algo
        elif self.menu.game_mode == "bot_vs_bot":
            is_bot = True
            if self.board.turn == "red":
                bot_algo = self.menu.red_bot_algo
            else:
                bot_algo = self.menu.black_bot_algo

        if is_bot and bot_algo and bot_algo != "Human":
            if has_lost(self.board, self.board.turn) or is_no_cross_river_pieces(
                self.board
            ):
                return

            # Report mode: asynchronous AI call with recorder
            if self.report_mode:
                if self.ai_thread is None and not self.pending_ai_move:
                    self.step_recorder.clear()
                    bot_func = AI_REGISTRY[bot_algo]
                    board_copy = self.board.copy()

                    def calculate():
                        result = bot_func(board_copy, recorder=self.step_recorder)
                        with self.ai_lock:
                            self.ai_result = result

                    self.ai_thread = threading.Thread(target=calculate)
                    self.ai_thread.daemon = True
                    self.ai_thread.start()

                if self.ai_thread and not self.ai_thread.is_alive():
                    self.ai_thread = None
                    with self.ai_lock:
                        move = self.ai_result
                        self.ai_result = None

                    # Don't execute move yet - wait for user to step through visualization
                    # Store pending move
                    if move and self.step_recorder.total_steps() > 0:
                        self.pending_ai_move = move
                        self.step_controller = StepController()
                    elif move:
                        self.trigger_move_animation(move[0], move[1])
                return

            # Normal mode: async AI call (original behavior)
            delay = self.sidebar.get_bot_speed_delay()
            if time.time() - self.last_bot_move_time < delay:
                return

            if self.ai_thread is None:
                bot_func = AI_REGISTRY[bot_algo]
                board_copy = self.board.copy()

                def calculate():
                    result = bot_func(board_copy)
                    with self.ai_lock:
                        self.ai_result = result

                self.ai_thread = threading.Thread(target=calculate)
                self.ai_thread.daemon = True
                self.ai_thread.start()

            if self.ai_thread and not self.ai_thread.is_alive():
                self.ai_thread = None
                with self.ai_lock:
                    move = self.ai_result
                    self.ai_result = None

                if move:
                    self.trigger_move_animation(move[0], move[1])
                self.last_bot_move_time = time.time()

    def update_animation(self):
        if not self.animation:
            return

        anim = self.animation
        elapsed = time.time() - anim["start_time"]
        progress = elapsed / anim["duration"]

        if progress >= 1.0:
            # Execute actual move on model board
            self.board.make_move(anim["from_pos"], anim["to_pos"], log_move=False)

            is_captured = anim["captured"] is not None
            is_check = is_in_check(self.board, self.board.turn)

            # Spawn capture particles on piece capture
            if is_captured:
                cx, cy = self.renderer.get_xy(anim["to_pos"][0], anim["to_pos"][1])
                self.renderer.spawn_capture_particles(cx, cy, self.equipped_board)

            if is_check:
                play_synth_sound("check")
            elif is_captured:
                play_synth_sound("capture")
            else:
                play_synth_sound("move")

            # Reward gold on game won
            if has_lost(self.board, self.board.turn):
                winner = "red" if self.board.turn == "black" else "black"
                if self.menu.game_mode == "human_vs_bot" and winner == "red":
                    self.gold += 100
                else:
                    self.gold += 50

            self.animation = None
            self.hint_move = None
            if self.pending_move:
                self.pending_move["pending"] = False
            self.pending_move = None

            # Check win/draw conditions
            if is_no_cross_river_pieces(self.board):
                self.game_over_result = "HÒA CỜ - Không còn quân qua sông!"
                self.state = "game_over"
                self.game_end_time = time.time()
                if self.menu.game_mode == "human_vs_bot":
                    self.record_match_history("Hòa", exp_gained=40)
                    self.red_exp = self.settings.data.get("exp", 0)
                else:
                    self.record_match_history("Hòa")
            elif has_lost(self.board, self.board.turn):
                winner_color = "red" if self.board.turn == "black" else "black"
                win_exp = calculate_win_exp(self.board, winner_color)

                if winner_color == "red":
                    self.game_over_result = f"Red wins! +{win_exp} EXP"
                else:
                    self.game_over_result = f"Black wins! +{win_exp} EXP"

                self.state = "game_over"
                self.game_end_time = time.time()
                self.award_game_over_exp(winner_color, win_exp)

    def record_match_history(self, result, exp_gained=None):
        mode = self.menu.game_mode
        if mode == "human_vs_bot":
            algo = self.menu.black_bot_algo
        else:
            algo = f"{self.menu.red_bot_algo} vs {self.menu.black_bot_algo}"
        self.settings.add_match_record(mode, algo, result, exp_gained=exp_gained)

    def award_game_over_exp(self, winner_color, win_exp):
        if self.exp_awarded:
            return

        if winner_color == "red":
            if self.menu.game_mode == "human_vs_bot":
                self.record_match_history("Thắng", exp_gained=win_exp)
                self.red_exp = self.settings.data.get("exp", 0)
            else:
                self.red_exp += win_exp
                self.record_match_history("Đỏ thắng")
        else:
            self.black_exp += win_exp
            if self.menu.game_mode == "human_vs_bot":
                self.record_match_history("Thua", exp_gained=20)
                self.red_exp = self.settings.data.get("exp", 0)
            else:
                self.record_match_history("Đen thắng")

        self.exp_awarded = True

    def draw_game_screen(self):
        # 1. Draw Board theme background & grid lines
        self.renderer.draw_board(self.screen, theme=self.equipped_board)

        # Draw check effects
        self.renderer.draw_check_effect(self.screen, self.board)

        # Highlight selected piece & hint destinations
        if self.selected_pos:
            cx, cy = self.renderer.get_xy(self.selected_pos[0], self.selected_pos[1])
            pygame.draw.circle(
                self.screen,
                (242, 202, 80),
                (cx, cy),
                self.renderer.cell_size * 0.44 + 2,
                2,
            )
            self.renderer.draw_move_hints(self.screen, self.board, self.valid_moves)

        # Draw AI suggestion hints
        if self.hint_move:
            from_pos, to_pos = self.hint_move
            fx, fy = self.renderer.get_xy(from_pos[0], from_pos[1])
            tx, ty = self.renderer.get_xy(to_pos[0], to_pos[1])
            pygame.draw.circle(
                self.screen,
                (52, 152, 219),
                (fx, fy),
                self.renderer.cell_size * 0.44 + 2,
                3,
            )
            pygame.draw.circle(
                self.screen,
                (52, 152, 219),
                (tx, ty),
                self.renderer.cell_size * 0.44 + 2,
                3,
            )

        # 2. Draw static pieces (not currently animating)
        animating_piece = self.animation["piece"] if self.animation else None
        for r in range(10):
            for c in range(9):
                p = self.board.matrix[r][c]
                if p and p != animating_piece:
                    self.renderer.draw_piece(
                        self.screen,
                        p,
                        is_selected=(p.pos == self.selected_pos),
                        skin=self.equipped_piece,
                    )

        # 3. Draw sliding piece with overshoot easing
        if self.animation:
            anim = self.animation
            p = anim["piece"]

            elapsed = time.time() - anim["start_time"]
            t = min(1.0, elapsed / anim["duration"])
            prog = ease_out_back(t)

            x1, y1 = anim["from_xy"]
            x2, y2 = anim["to_xy"]

            curr_x = int(x1 + prog * (x2 - x1))
            curr_y = int(y1 + prog * (y2 - y1))

            self.renderer.draw_piece(
                self.screen,
                p,
                is_selected=False,
                skin=self.equipped_piece,
                cx=curr_x,
                cy=curr_y,
            )

        # 4. Draw Top Navigation Bar (Gold balance, Shop, Profile)
        self.draw_top_bar()

        # 5. Draw Sidebar Panel or Visualizer Panel (depending on report_mode)
        red_bot_lvl = (
            self.menu.red_bot_level if self.menu.red_bot_level is not None else 0
        )
        black_bot_lvl = (
            self.menu.black_bot_level if self.menu.black_bot_level is not None else 0
        )
        red_bot = (
            f"L{red_bot_lvl + 1}: {self.menu.red_bot_algo}"
            if self.menu.red_bot_algo and self.menu.red_bot_algo != "Human"
            else "Human"
        )
        black_bot = (
            f"L{black_bot_lvl + 1}: {self.menu.black_bot_algo}"
            if self.menu.black_bot_algo
            else ""
        )

        if self.report_mode and (
            self.step_recorder.total_steps() > 0 or self.ai_thread is not None
        ):
            # Show Visualizer Panel
            current_step = self.step_recorder.get_current_step()
            self.visualizer.draw(
                self.screen,
                current_step,
                self.step_controller,
                self.step_recorder,
                is_computing=(self.ai_thread is not None),
            )
        else:
            # Show normal Sidebar
            elapsed = 0.0
            if self.game_start_time is not None:
                if self.game_end_time is not None:
                    elapsed = self.game_end_time - self.game_start_time
                else:
                    elapsed = time.time() - self.game_start_time

            self.sidebar.draw(
                self.screen,
                self.board,
                self.menu.game_mode,
                red_bot,
                black_bot,
                hint_move=self.hint_move,
                move_history=self.board.move_log,
                pending_move=self.pending_move,
                latest_move_index=self.latest_move_index,
                latest_move_flash_until=self.latest_move_flash_until,
                bot_paused=self.bot_paused,
                red_exp=self.red_exp,
                black_exp=self.black_exp,
                is_game_over=(self.state == "game_over"),
                elapsed_time=elapsed,
            )

        # 6. Draw capture burst particles
        self.renderer.draw_particles(self.screen)

        # 7. Draw hover tooltip if triggered
        if self.hover_triggered and self.hover_piece:
            self.renderer.draw_tooltip(
                self.screen, self.hover_piece, pygame.mouse.get_pos()
            )

        # 8. Draw temporary popup notification banner if active
        if time.time() < self.popup_timer:
            p_width = 320
            p_height = 68
            px = self.board_width // 2 - p_width // 2  # Center on board canvas
            py = self.height // 2 - p_height // 2

            p_surf = pygame.Surface((p_width, p_height), pygame.SRCALPHA)
            p_surf.fill((44, 28, 24, 240))
            pygame.draw.rect(p_surf, COLOR_ACCENT, (0, 0, p_width, p_height), 2, 8)

            p_font = pygame.font.SysFont("Segoe UI, Tahoma", 14, bold=True)
            p_txt = p_font.render(self.popup_message, True, COLOR_ACCENT)
            p_surf.blit(
                p_txt,
                (
                    p_width // 2 - p_txt.get_width() // 2,
                    p_height // 2 - p_txt.get_height() // 2,
                ),
            )
            self.screen.blit(p_surf, (px, py))

    def draw_top_bar(self):
        # Semi-transparent dark overlay for top bar
        top_bar_surf = pygame.Surface((self.board_width, 72), pygame.SRCALPHA)
        top_bar_surf.fill((15, 8, 6, 200))
        self.screen.blit(top_bar_surf, (0, 0))
        pygame.draw.line(self.screen, COLOR_OUTLINE, (0, 72), (self.board_width, 72), 1)

        # Title "Hoàng Gia Tượng Kỳ"
        brand_font = pygame.font.SysFont("Playfair Display, Segoe UI", 18, bold=True)
        brand_txt = brand_font.render("Hoàng Gia Tượng Kỳ", True, COLOR_ACCENT)
        self.screen.blit(brand_txt, (15, 36 - brand_txt.get_height() // 2))

        # Navigation Tabs: Trận Đấu (Active) / Cửa Tiệm / Cài Đặt
        mouse_pos = pygame.mouse.get_pos()
        tab_font = pygame.font.SysFont("Segoe UI, Tahoma", 13, bold=True)

        # Tab "Trận Đấu" - Active
        active_color = COLOR_ACCENT
        match_txt = tab_font.render("TRẬN ĐẤU", True, active_color)
        self.screen.blit(
            match_txt,
            (
                self.btn_top_match.centerx - match_txt.get_width() // 2,
                self.btn_top_match.centery - match_txt.get_height() // 2,
            ),
        )
        # Draw Gold underline for active tab
        pygame.draw.line(
            self.screen,
            COLOR_ACCENT,
            (self.btn_top_match.x + 8, 52),
            (self.btn_top_match.right - 8, 52),
            2,
        )

        # Tab "Cửa Tiệm" - Navigates to shop
        is_hover_shop = self.btn_top_shop.collidepoint(mouse_pos)
        shop_color = COLOR_ACCENT if is_hover_shop else COLOR_TEXT_MUTED
        shop_txt = tab_font.render("CỬA TIỆM", True, shop_color)
        self.screen.blit(
            shop_txt,
            (
                self.btn_top_shop.centerx - shop_txt.get_width() // 2,
                self.btn_top_shop.centery - shop_txt.get_height() // 2,
            ),
        )

        # Tab "Cài Đặt" - Show coming soon popup
        is_hover_settings = self.btn_top_settings.collidepoint(mouse_pos)
        settings_color = COLOR_ACCENT if is_hover_settings else COLOR_TEXT_MUTED
        settings_txt = tab_font.render("CÀI ĐẶT", True, settings_color)
        self.screen.blit(
            settings_txt,
            (
                self.btn_top_settings.centerx - settings_txt.get_width() // 2,
                self.btn_top_settings.centery - settings_txt.get_height() // 2,
            ),
        )

        # Gold counter box
        gold_box = pygame.Rect(self.board_width - 148, 20, 92, 32)
        pygame.draw.rect(self.screen, (30, 20, 15), gold_box, 0, 16)
        pygame.draw.rect(self.screen, COLOR_ACCENT, gold_box, 1, 16)

        # Coin icon
        pygame.draw.circle(
            self.screen, COLOR_ACCENT, (gold_box.x + 14, gold_box.centery), 6
        )
        c_font = pygame.font.SysFont("Segoe UI", 8, bold=True)
        c_txt = c_font.render("V", True, (40, 25, 10))
        self.screen.blit(
            c_txt,
            (
                gold_box.x + 14 - c_txt.get_width() // 2,
                gold_box.centery - c_txt.get_height() // 2 + 1,
            ),
        )

        gold_font = pygame.font.SysFont("Consolas, Segoe UI", 12, bold=True)
        gold_val_txt = gold_font.render(f"{self.gold:,}", True, COLOR_ACCENT)
        self.screen.blit(
            gold_val_txt,
            (gold_box.x + 25, gold_box.centery - gold_val_txt.get_height() // 2),
        )

        # Profile Avatar Circle
        avatar_center = (self.board_width - 25, 36)
        pygame.draw.circle(self.screen, COLOR_ACCENT, avatar_center, 15)
        pygame.draw.circle(self.screen, (55, 35, 30), avatar_center, 13)
        av_font = pygame.font.SysFont("Segoe UI", 10, bold=True)
        av_txt = av_font.render("KV", True, COLOR_ACCENT)
        self.screen.blit(
            av_txt,
            (
                avatar_center[0] - av_txt.get_width() // 2,
                avatar_center[1] - av_txt.get_height() // 2,
            ),
        )

    def draw_game_over_overlay(self):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((15, 8, 6, 180))
        self.screen.blit(overlay, (0, 0))

        panel_width = 440
        panel_height = 240
        panel_x = self.width // 2 - panel_width // 2
        panel_y = self.height // 2 - panel_height // 2

        pygame.draw.rect(
            self.screen,
            (44, 28, 24),
            (panel_x, panel_y, panel_width, panel_height),
            0,
            12,
        )
        pygame.draw.rect(
            self.screen,
            COLOR_ACCENT,
            (panel_x, panel_y, panel_width, panel_height),
            2,
            12,
        )

        hdr_font = pygame.font.SysFont("Segoe UI, Tahoma, Arial", 26, bold=True)
        hdr_txt = hdr_font.render("TRẬN ĐẤU KẾT THÚC", True, COLOR_ACCENT)
        self.screen.blit(
            hdr_txt, (self.width // 2 - hdr_txt.get_width() // 2, panel_y + 30)
        )

        res_font = pygame.font.SysFont("Segoe UI, Tahoma, Arial", 18, bold=True)
        res_color = (
            COLOR_RED
            if "Đỏ" in self.game_over_result
            else (COLOR_BLACK if "Đen" in self.game_over_result else COLOR_TEXT)
        )
        res_txt = res_font.render(self.game_over_result, True, res_color)
        self.screen.blit(
            res_txt, (self.width // 2 - res_txt.get_width() // 2, panel_y + 85)
        )

        btn_font = pygame.font.SysFont("Segoe UI, Tahoma, Arial", 16, bold=True)

        # Draw Retry button
        pygame.draw.rect(self.screen, (39, 174, 96), self.btn_game_over_retry, 0, 6)
        pygame.draw.rect(self.screen, COLOR_ACCENT, self.btn_game_over_retry, 1, 6)
        retry_lbl = btn_font.render("CHƠI LẠI", True, COLOR_TEXT)
        self.screen.blit(
            retry_lbl,
            (
                self.btn_game_over_retry.centerx - retry_lbl.get_width() // 2,
                self.btn_game_over_retry.centery - retry_lbl.get_height() // 2,
            ),
        )

        # Draw Menu button
        pygame.draw.rect(self.screen, (192, 57, 43), self.btn_game_over_menu, 0, 6)
        pygame.draw.rect(self.screen, COLOR_ACCENT, self.btn_game_over_menu, 1, 6)
        menu_lbl = btn_font.render("MENU CHÍNH", True, COLOR_TEXT)
        self.screen.blit(
            menu_lbl,
            (
                self.btn_game_over_menu.centerx - menu_lbl.get_width() // 2,
                self.btn_game_over_menu.centery - menu_lbl.get_height() // 2,
            ),
        )


if __name__ == "__main__":
    controller = GameController()
    controller.run()
