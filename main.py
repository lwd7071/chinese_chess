# Main launcher of Xiangqi AI Game in Python + Pygame
import pygame
import time
import threading
import sys
import os

# Adjust path to find submodules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game.board import Board
from game.rules import has_lost, is_in_check, is_checkmate, is_stalemate
from ai import AI_REGISTRY
from gui.renderer import Renderer
from gui.sidebar import Sidebar
from gui.menu import StartMenu
from gui.sound import play_synth_sound

# Screen Dimensions
WIDTH = 940
HEIGHT = 700

class GameController:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Cờ Tướng AI - Xiangqi AI Game Dashboard")
        self.clock = pygame.time.Clock()
        
        # Init GUI modules
        self.renderer = Renderer(cell_size=60, offset_x=40, offset_y=50)
        self.sidebar = Sidebar(x=580, y=0, width=360, height=700)
        self.menu = StartMenu(width=WIDTH, height=HEIGHT)
        
        self.state = "menu" # menu, game
        
        # Game State Variables
        self.board = None
        self.selected_pos = None
        self.valid_moves = []
        self.hint_move = None
        
        # AI threading state
        self.ai_thread = None
        self.ai_result = None
        self.ai_lock = threading.Lock()
        self.last_bot_move_time = 0
        
        # Animation state: {"piece": Piece, "from_xy": (x,y), "to_xy": (x,y), "progress": 0.0, "to_pos": (r,c), "captured": Piece}
        self.animation = None
        
        # Game Over state variables
        self.game_over_result = ""
        self.btn_game_over_retry = pygame.Rect(WIDTH // 2 - 160, HEIGHT // 2 + 30, 140, 40)
        self.btn_game_over_menu = pygame.Rect(WIDTH // 2 + 20, HEIGHT // 2 + 30, 140, 40)

    def start_new_game(self):
        self.board = Board()
        self.selected_pos = None
        self.valid_moves = []
        self.hint_move = None
        self.ai_thread = None
        self.ai_result = None
        self.animation = None
        self.last_bot_move_time = time.time()
        self.game_over_result = ""
        
    def trigger_move_animation(self, from_pos, to_pos):
        piece = self.board.get_piece(from_pos)
        captured = self.board.get_piece(to_pos)
        
        x1, y1 = self.renderer.get_xy(from_pos[0], from_pos[1])
        x2, y2 = self.renderer.get_xy(to_pos[0], to_pos[1])
        
        self.animation = {
            "piece": piece,
            "from_pos": from_pos,
            "to_pos": to_pos,
            "from_xy": (x1, y1),
            "to_xy": (x2, y2),
            "progress": 0.0,
            "captured": captured
        }
        
    def run(self):
        running = True
        while running:
            self.clock.tick(60) # 60 FPS
            
            # 1. Handle Events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    
                if self.state == "menu":
                    if self.menu.handle_event(event):
                        self.start_new_game()
                        self.state = "game"
                        
                elif self.state == "game" and not self.animation:
                    # Sidebar click actions
                    action = self.sidebar.handle_event(event)
                    if action == "new_game":
                        self.start_new_game()
                    elif action == "menu":
                        self.state = "menu"
                    elif action == "undo":
                        # Undo twice in Human vs Bot, or once in Bot vs Bot
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
                        # Suggest the best move for current turn using Alpha-Beta search (Level 6)
                        self.stats_lbl = "Đang tìm kiếm gợi ý..."
                        self.hint_move = AI_REGISTRY["Level 6: Alpha-Beta Bot"](self.board)
                        
                    # Human Move inputs
                    elif self.menu.game_mode == "human_vs_bot" and self.board.turn == 'red':
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            board_pos = self.renderer.get_board_pos_from_screen(event.pos)
                            if board_pos:
                                self.handle_human_click(board_pos)
                                
                elif self.state == "game_over":
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.btn_game_over_retry.collidepoint(event.pos):
                            self.start_new_game()
                            self.state = "game"
                        elif self.btn_game_over_menu.collidepoint(event.pos):
                            self.state = "menu"
                                
            # 2. Game Logic / Bot calculations
            if self.state == "game" and not self.animation:
                self.handle_bot_turns()
                
            # 3. Update Animations
            self.update_animation()
            
            # 4. Drawing Phase
            if self.state == "menu":
                self.menu.draw(self.screen)
            elif self.state in ["game", "game_over"]:
                self.draw_game_screen()
                if self.state == "game_over":
                    self.draw_game_over_overlay()
                
            pygame.display.flip()
            
        pygame.quit()

    def handle_human_click(self, pos):
        r, c = pos
        piece = self.board.get_piece(pos)
        
        # If we click on our own piece, select it
        if piece and piece.color == 'red':
            self.selected_pos = pos
            # Filter all legal moves starting from this piece position
            all_legal = self.board.get_all_legal_moves('red')
            self.valid_moves = [to_pos for from_pos, to_pos in all_legal if from_pos == pos]
            self.hint_move = None # Clear hint on selection
            
        # If we clicked on a valid move cell, execute it
        elif self.selected_pos and pos in self.valid_moves:
            self.trigger_move_animation(self.selected_pos, pos)
            self.selected_pos = None
            self.valid_moves = []

    def handle_bot_turns(self):
        # Check if it is the Bot's turn
        is_bot = False
        bot_algo = ""
        
        if self.menu.game_mode == "human_vs_bot" and self.board.turn == 'black':
            is_bot = True
            bot_algo = self.menu.black_bot_algo
        elif self.menu.game_mode == "bot_vs_bot":
            is_bot = True
            if self.board.turn == 'red':
                bot_algo = self.menu.red_bot_algo
            else:
                bot_algo = self.menu.black_bot_algo
                
        if is_bot and bot_algo:
            # Check game end
            if has_lost(self.board, self.board.turn):
                return
                
            # In Bot vs Bot, respect speed slider delay
            delay = self.sidebar.get_bot_speed_delay()
            if time.time() - self.last_bot_move_time < delay:
                return
                
            # If no AI thread running, launch one
            if self.ai_thread is None:
                bot_func = AI_REGISTRY[bot_algo]
                
                # Make a thread-safe copy of the board to calculate moves in background
                board_copy = self.board.copy()
                
                def calculate():
                    result = bot_func(board_copy)
                    with self.ai_lock:
                        self.ai_result = result
                    
                self.ai_thread = threading.Thread(target=calculate)
                self.ai_thread.daemon = True
                self.ai_thread.start()
                
            # Check thread completion
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
        anim["progress"] += 0.08 # Animation speed (takes ~12 frames to complete)
        
        if anim["progress"] >= 1.0:
            # Execute actual move on model board
            self.board.make_move(anim["from_pos"], anim["to_pos"])
            
            # Trigger corresponding sound
            is_captured = anim["captured"] is not None
            is_check = is_in_check(self.board, self.board.turn) # opposite turn side checked
            
            if is_check:
                play_synth_sound('check')
            elif is_captured:
                play_synth_sound('capture')
            else:
                play_synth_sound('move')
                
            # Clear animation
            self.animation = None
            self.hint_move = None
            
            # Check for win conditions
            if has_lost(self.board, self.board.turn):
                winner = "Đỏ (RED)" if self.board.turn == 'black' else "Đen (BLACK)"
                loser_color = self.board.turn
                if is_checkmate(self.board, loser_color):
                    self.game_over_result = f"CHIẾU BÍ - Quân {winner} thắng!"
                elif is_stalemate(self.board, loser_color):
                    self.game_over_result = f"VÔ TỬ (HẾT NƯỚC) - Quân {winner} thắng!"
                else:
                    self.game_over_result = f"KẾT THÚC - Quân {winner} thắng!"
                self.state = "game_over"

    def draw_game_screen(self):
        # 1. Draw static elements
        self.renderer.draw_board(self.screen)
        
        # Draw check notification effect (glow around King and top banner text)
        self.renderer.draw_check_effect(self.screen, self.board)
        
        # Highlight selected and hints
        if self.selected_pos:
            cx, cy = self.renderer.get_xy(self.selected_pos[0], self.selected_pos[1])
            pygame.draw.circle(self.screen, (240, 200, 40), (cx, cy), self.renderer.cell_size * 0.44 + 2, 2)
            self.renderer.draw_move_hints(self.screen, self.board, self.valid_moves)
            
        # Draw hint move if requested
        if self.hint_move:
            from_pos, to_pos = self.hint_move
            fx, fy = self.renderer.get_xy(from_pos[0], from_pos[1])
            tx, ty = self.renderer.get_xy(to_pos[0], to_pos[1])
            # Highlight starting cell in blue, destination in blue
            pygame.draw.circle(self.screen, (52, 152, 219), (fx, fy), self.renderer.cell_size * 0.44 + 2, 3)
            pygame.draw.circle(self.screen, (52, 152, 219), (tx, ty), self.renderer.cell_size * 0.44 + 2, 3)

        # 2. Draw static pieces (not currently in animation)
        animating_piece = self.animation["piece"] if self.animation else None
        
        for r in range(10):
            for c in range(9):
                p = self.board.matrix[r][c]
                if p and p != animating_piece:
                    self.renderer.draw_piece(self.screen, p, is_selected=(p.pos == self.selected_pos))
                    
        # 3. Draw sliding piece if animating
        if self.animation:
            anim = self.animation
            p = anim["piece"]
            
            # Linear interpolation of positions
            x1, y1 = anim["from_xy"]
            x2, y2 = anim["to_xy"]
            prog = anim["progress"]
            
            curr_x = int(x1 + prog * (x2 - x1))
            curr_y = int(y1 + prog * (y2 - y1))
            
            # Temporary relocate piece representation for drawing
            old_pos = p.pos
            # Draw piece circle manually at interpolated position
            radius = int(self.renderer.cell_size * 0.44)
            pygame.draw.circle(self.screen, (160, 110, 60), (curr_x, curr_y), radius)
            pygame.draw.circle(self.screen, (250, 240, 215), (curr_x, curr_y), radius - 2)
            
            text_color = (200, 30, 30) if p.color == 'red' else (20, 20, 20)
            if self.renderer.chinese_supported:
                char = p.char
            else:
                char = p.name
                
            txt = self.renderer.piece_font.render(char, True, text_color)
            self.screen.blit(txt, (curr_x - txt.get_width() // 2, curr_y - txt.get_height() // 2))

        # 4. Draw sidebar details
        red_bot = f"L{self.menu.red_bot_level + 1}: {self.menu.red_bot_algo}" if self.menu.red_bot_algo else "Human"
        black_bot = f"L{self.menu.black_bot_level + 1}: {self.menu.black_bot_algo}" if self.menu.black_bot_algo else ""
        self.sidebar.draw(
            self.screen, self.board, self.menu.game_mode,
            red_bot, black_bot, hint_move=self.hint_move
        )

    def draw_game_over_overlay(self):
        # 1. Draw a dark translucent overlay over the board/screen
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((20, 20, 20, 180)) # Black overlay with 180 alpha
        self.screen.blit(overlay, (0, 0))
        
        # 2. Draw panel card in the center
        panel_width = 440
        panel_height = 240
        panel_x = WIDTH // 2 - panel_width // 2
        panel_y = HEIGHT // 2 - panel_height // 2
        
        # Panel background
        pygame.draw.rect(self.screen, (45, 45, 45), (panel_x, panel_y, panel_width, panel_height), 0, 12)
        # Panel border
        pygame.draw.rect(self.screen, (0, 173, 181), (panel_x, panel_y, panel_width, panel_height), 2, 12)
        
        # 3. Draw Header text
        hdr_font = pygame.font.SysFont("segoe ui, tahoma, arial", 26, bold=True)
        hdr_txt = hdr_font.render("TRẬN ĐẤU KẾT THÚC", True, (0, 173, 181))
        self.screen.blit(hdr_txt, (WIDTH // 2 - hdr_txt.get_width() // 2, panel_y + 30))
        
        # 4. Draw result text (e.g. CHIẾU BÍ - Quân Đỏ thắng!)
        res_font = pygame.font.SysFont("segoe ui, tahoma, arial", 18, bold=True)
        res_color = (231, 76, 60) if "Quân Đỏ" in self.game_over_result else ((241, 196, 15) if "Quân Đen" in self.game_over_result else (240, 240, 240))
        res_txt = res_font.render(self.game_over_result, True, res_color)
        self.screen.blit(res_txt, (WIDTH // 2 - res_txt.get_width() // 2, panel_y + 85))
        
        # 5. Draw buttons
        btn_font = pygame.font.SysFont("segoe ui, tahoma, arial", 16, bold=True)
        
        # Draw Retry button
        pygame.draw.rect(self.screen, (39, 174, 96), self.btn_game_over_retry, 0, 6)
        retry_lbl = btn_font.render("CHƠI LẠI", True, (240, 240, 240))
        self.screen.blit(retry_lbl, (self.btn_game_over_retry.centerx - retry_lbl.get_width() // 2, self.btn_game_over_retry.centery - retry_lbl.get_height() // 2))
        
        # Draw Menu button
        pygame.draw.rect(self.screen, (192, 57, 43), self.btn_game_over_menu, 0, 6)
        menu_lbl = btn_font.render("MENU CHÍNH", True, (240, 240, 240))
        self.screen.blit(menu_lbl, (self.btn_game_over_menu.centerx - menu_lbl.get_width() // 2, self.btn_game_over_menu.centery - menu_lbl.get_height() // 2))

if __name__ == "__main__":
    controller = GameController()
    controller.run()
