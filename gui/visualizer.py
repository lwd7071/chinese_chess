"""
Visualizer Panel - Step-by-Step Algorithm Visualization

Hiển thị từng bước thực thi thuật toán AI cho mục đích demo và báo cáo.
Thay thế Sidebar khi report_mode=True.

Author: Nhóm 1 - Cờ tướng 6 level
Date: 2026-06-25
"""

import pygame
import time
import math
from ai.step_recorder import (
    BaseStep, UCSStep, AStarStep, AlphaBetaStep, SAStep,
    GreedyStep, IDAStarStep, BFSStep, DFSStep, HillClimbStep,
    BeamStep, MinimaxStep, ExpectimaxStep,
    OnlineStep, AndOrStep, BeliefStep,
    BacktrackStep, MinConflictStep, AC3Step
)

# Colors matching sidebar theme
COLOR_BG = (28, 16, 12)           # Dark rosewood
COLOR_CARD = (44, 28, 24)         # Card background
COLOR_ACCENT = (242, 202, 80)     # Gold
COLOR_TEXT = (250, 220, 213)      # Light text
COLOR_TEXT_MUTED = (180, 165, 150)
COLOR_OUTLINE = (77, 70, 53)
COLOR_JADE = (89, 222, 155)
COLOR_RED = (231, 76, 60)
COLOR_BLUE = (52, 152, 219)

# Piece name mapping for display
PIECE_NAME_VI = {
    'general': 'Tướng', 'advisor': 'Sĩ', 'elephant': 'Tượng',
    'horse': 'Mã', 'rook': 'Xe', 'cannon': 'Pháo', 'pawn': 'Tốt',
    'Tướng': 'Tướng', 'Sĩ': 'Sĩ', 'Tượng': 'Tượng',
    'Mã': 'Mã', 'Xe': 'Xe', 'Pháo': 'Pháo', 'Tốt': 'Tốt',
}


class StepController:
    """Controller for step navigation (prev/next/auto)"""
    
    def __init__(self):
        self.mode = "manual"          # "manual" or "auto"
        self.auto_delay = 1.5         # Seconds between auto steps
        self.last_auto_time = 0
        self.is_paused = False
        
    def next_step(self, recorder) -> bool:
        """Move to next step"""
        return recorder.next()
    
    def prev_step(self, recorder) -> bool:
        """Move to previous step"""
        return recorder.prev()
    
    def toggle_auto(self):
        """Toggle between manual and auto mode"""
        self.mode = "auto" if self.mode == "manual" else "manual"
        self.last_auto_time = time.time()
    
    def toggle_pause(self):
        """Pause/resume auto mode"""
        self.is_paused = not self.is_paused
        if not self.is_paused:
            self.last_auto_time = time.time()
    
    def update(self, recorder):
        """Called every frame to handle auto stepping"""
        if self.mode == "auto" and not self.is_paused:
            if time.time() - self.last_auto_time >= self.auto_delay:
                if not recorder.next():
                    # Reached end, pause
                    self.is_paused = True
                    self.mode = "manual"
                    return "finish"
                self.last_auto_time = time.time()
        return None


class VisualizerPanel:
    """
    Main visualization panel for step-by-step algorithm display.
    Replaces Sidebar when report_mode=True.
    """
    
    def __init__(self, x, y, width, height, chinese_supported=False, font_name=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # Load fonts. If custom font_name is provided, use it (assumed to be a file path for pygame.font.Font if it ends with .ttf)
        # However, for UI we mainly use SysFont unless we really need chinese
        font_list = ["Segoe UI", "Arial"]
        if font_name and not font_name.endswith('.ttf'):
            font_list.insert(0, font_name)
            
        try:
            if font_name and font_name.endswith('.ttf'):
                self.title_font = pygame.font.Font(font_name, 20)
                self.header_font = pygame.font.Font(font_name, 16)
                self.body_font = pygame.font.Font(font_name, 14)
                self.mono_font = pygame.font.SysFont(["Consolas", "Courier New"], 13)
                self.small_font = pygame.font.Font(font_name, 12)
                self.tiny_font = pygame.font.Font(font_name, 10)
            else:
                self.title_font = pygame.font.SysFont(font_list, 20, bold=True)
                self.header_font = pygame.font.SysFont(font_list, 16, bold=True)
                self.body_font = pygame.font.SysFont(font_list, 14)
                self.mono_font = pygame.font.SysFont(["Consolas", "Courier New"] + font_list, 13)
                self.small_font = pygame.font.SysFont(font_list, 12)
                self.tiny_font = pygame.font.SysFont(font_list, 10)
        except Exception:
            # Fallback
            self.title_font = pygame.font.SysFont(["Segoe UI", "Arial"], 20, bold=True)
            self.header_font = pygame.font.SysFont(["Segoe UI", "Arial"], 16, bold=True)
            self.body_font = pygame.font.SysFont(["Segoe UI", "Arial"], 14)
            self.mono_font = pygame.font.SysFont(["Consolas", "Courier New"], 13)
            self.small_font = pygame.font.SysFont(["Segoe UI", "Arial"], 12)
            self.tiny_font = pygame.font.SysFont(["Segoe UI", "Arial"], 10)
        
        # Navigation buttons
        btn_y = y + height - 60
        btn_w = 80
        center_x = x + width // 2
        start_x = center_x - 172
        
        self.btn_prev = pygame.Rect(start_x, btn_y, btn_w, 36)
        self.btn_next = pygame.Rect(start_x + 88, btn_y, btn_w, 36)
        self.btn_auto = pygame.Rect(start_x + 176, btn_y, btn_w, 36)
        self.btn_skip = pygame.Rect(start_x + 264, btn_y, btn_w, 36)
        
        # Scroll state for long lists
        self.scroll_offset = 0
        self.max_scroll = 0
        
    def update_layout(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        btn_y = self.y + self.height - 60
        btn_w = 80
        center_x = self.x + self.width // 2
        start_x = center_x - 172
        
        self.btn_prev.x = start_x
        self.btn_prev.y = btn_y
        self.btn_next.x = start_x + 88
        self.btn_next.y = btn_y
        self.btn_auto.x = start_x + 176
        self.btn_auto.y = btn_y
        self.btn_skip.x = start_x + 264
        self.btn_skip.y = btn_y
        
    def handle_event(self, event, controller, recorder):
        """Handle mouse clicks and scroll events"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_prev.collidepoint(event.pos):
                controller.prev_step(recorder)
                controller.mode = "manual"  # Switch to manual on click
                return "prev"
            elif self.btn_next.collidepoint(event.pos):
                if recorder.current_index == recorder.total_steps() - 1:
                    controller.mode = "manual"
                    return "finish"
                controller.next_step(recorder)
                controller.mode = "manual"
                return "next"
            elif self.btn_auto.collidepoint(event.pos):
                controller.toggle_auto()
                return "auto"
            elif self.btn_skip.collidepoint(event.pos):
                recorder.reset_to_end()
                controller.mode = "manual"
                return "finish"
        
        elif event.type == pygame.MOUSEWHEEL:
            # Scroll content if needed
            self.scroll_offset = max(0, min(self.max_scroll, self.scroll_offset - event.y * 20))
            
        return None
    
    # ========================================================================
    # FORMAT HELPERS
    # ========================================================================
    
    def _format_move(self, move_data):
        """Format move tuple/dict thành chuỗi dễ đọc cho hiển thị."""
        if move_data is None:
            return "—"
        
        if isinstance(move_data, tuple) and len(move_data) == 2:
            if isinstance(move_data[0], tuple):
                return f"{move_data[0]}→{move_data[1]}"
            return str(move_data)
        
        if isinstance(move_data, dict):
            parts = []
            # Tên quân nếu có
            piece = move_data.get('piece_captured') or move_data.get('piece')
            if piece and piece != '—':
                vi_name = PIECE_NAME_VI.get(piece, piece)
                parts.append(vi_name)
            
            # Tọa độ nước đi
            move = move_data.get('move')
            if move and isinstance(move, tuple) and len(move) == 2:
                if isinstance(move[0], tuple):
                    parts.append(f"{move[0]}→{move[1]}")
                else:
                    parts.append(str(move))
            
            # Score nếu có
            score = move_data.get('score')
            if score is not None:
                try:
                    parts.append(f"[{score:.0f}]")
                except (TypeError, ValueError):
                    parts.append(f"[{score}]")
            
            return ' '.join(parts) if parts else str(move_data)[:25]
        
        return str(move_data)[:25]
    
    def _format_move_short(self, move_data):
        """Format ngắn gọn — chỉ tọa độ, không score."""
        if move_data is None:
            return "—"
        if isinstance(move_data, tuple) and len(move_data) == 2:
            if isinstance(move_data[0], tuple):
                return f"{move_data[0]}→{move_data[1]}"
            return str(move_data)
        if isinstance(move_data, dict):
            move = move_data.get('move')
            if move:
                return self._format_move_short(move)
        return str(move_data)[:20]
    
    # ========================================================================
    # MAIN DRAW
    # ========================================================================
    
    def draw(self, surface, step: BaseStep, controller, recorder, is_computing=False):
        """Main render method"""
        # Background
        bg_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, COLOR_BG, bg_rect)
        pygame.draw.line(surface, COLOR_OUTLINE, (self.x, self.y), (self.x, self.y + self.height), 2)
        
        if step is None:
            self._render_empty(surface)
            if is_computing:
                text = self.title_font.render("AI Đang Tính Toán...", True, (255, 50, 50))
                surface.blit(text, (self.x + self.width // 2 - text.get_width() // 2, self.y + self.height // 2 + 50))
            return
        
        # Header with step counter
        self._render_header(surface, step, recorder)
        
        # Body - delegate to specific renderer
        content_y = self.y + 80
        content_rect = pygame.Rect(self.x + 15, content_y, self.width - 30, self.height - 160)
        
        if isinstance(step, (BFSStep, DFSStep)):
            self._render_bfs_dfs(surface, step, content_rect)
        elif isinstance(step, (UCSStep, AStarStep)):
            self._render_search_3col(surface, step, content_rect)
        elif isinstance(step, IDAStarStep):
            self._render_ida_star(surface, step, content_rect)
        elif isinstance(step, (GreedyStep, HillClimbStep)):
            self._render_candidates_list(surface, step, content_rect)
        elif isinstance(step, SAStep):
            self._render_sa(surface, step, content_rect)
        elif isinstance(step, BeamStep):
            self._render_beam(surface, step, content_rect)
        elif isinstance(step, (OnlineStep, AndOrStep, BeliefStep)):
            self._render_level4(surface, step, content_rect)
        elif isinstance(step, (BacktrackStep, MinConflictStep, AC3Step)):
            self._render_csp(surface, step, content_rect)
        elif isinstance(step, AlphaBetaStep):
            self._render_alpha_beta(surface, step, content_rect)
        elif isinstance(step, (MinimaxStep, ExpectimaxStep)):
            self._render_minimax_expectimax(surface, step, content_rect)
        else:
            self._render_text_only(surface, step, content_rect)
        
        # Navigation footer
        self._render_footer(surface, controller, recorder)
        
        if is_computing:
            text = self.title_font.render("AI ĐANG TÍNH TOÁN...", True, (255, 50, 50))
            overlay = pygame.Surface((self.width, 40))
            overlay.set_alpha(200)
            overlay.fill((30, 30, 40))
            surface.blit(overlay, (self.x, self.y + 40))
            surface.blit(text, (self.x + self.width // 2 - text.get_width() // 2, self.y + 48))
    
    def _render_empty(self, surface):
        """Shown when no steps available"""
        msg = self.body_font.render("Chưa có dữ liệu visualization", True, COLOR_TEXT_MUTED)
        surface.blit(msg, (self.x + self.width // 2 - msg.get_width() // 2, self.y + self.height // 2))
    
    def _render_header(self, surface, step, recorder):
        """Render header with step counter and algorithm name"""
        # Title bar
        header_rect = pygame.Rect(self.x + 15, self.y + 15, self.width - 30, 50)
        pygame.draw.rect(surface, COLOR_CARD, header_rect, 0, 8)
        pygame.draw.rect(surface, COLOR_OUTLINE, header_rect, 1, 8)
        
        # Algorithm name
        algo_txt = self.title_font.render(step.algorithm, True, COLOR_ACCENT)
        surface.blit(algo_txt, (header_rect.x + 15, header_rect.y + 8))
        
        # Step counter
        step_txt = self.header_font.render(
            f"Bước {recorder.current_index + 1}/{recorder.total_steps()}",
            True, COLOR_TEXT
        )
        surface.blit(step_txt, (header_rect.right - step_txt.get_width() - 15, header_rect.y + 12))
    
    def _render_footer(self, surface, controller, recorder):
        """Render navigation buttons"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw buttons
        buttons = [
            (self.btn_prev, "◀ PREV", COLOR_BLUE, recorder.current_index > 0),
            (self.btn_next, "NEXT ▶" if recorder.current_index < recorder.total_steps() - 1 else "FINISH ▶", COLOR_BLUE, True),
            (self.btn_auto, "▶▶ AUTO" if controller.mode == "manual" else "⏸ PAUSE", 
             COLOR_JADE if controller.mode == "auto" else COLOR_ACCENT, True),
            (self.btn_skip, "SKIP >|", COLOR_RED, True)
        ]
        
        for rect, label, color, enabled in buttons:
            is_hover = rect.collidepoint(mouse_pos) and enabled
            btn_color = color if enabled else COLOR_OUTLINE
            
            # Button background
            pygame.draw.rect(surface, btn_color if not is_hover else self._brighten(btn_color), rect, 0, 6)
            pygame.draw.rect(surface, COLOR_ACCENT if enabled else COLOR_OUTLINE, rect, 1, 6)
            
            # Button text
            txt_color = COLOR_TEXT if enabled else COLOR_TEXT_MUTED
            txt = self.small_font.render(label, True, txt_color)
            surface.blit(txt, (rect.centerx - txt.get_width() // 2, rect.centery - txt.get_height() // 2))
    
    def _brighten(self, color):
        """Brighten color for hover effect"""
        return tuple(min(255, c + 30) for c in color)
    
    # ========================================================================
    # SHARED RENDERING HELPERS
    # ========================================================================
    
    def _draw_explanation_box(self, surface, step, rect, max_lines=3, height=60):
        """Draw explanation text box at top of content area. Returns bottom y."""
        expl_rect = pygame.Rect(rect.x, rect.y, rect.width, height)
        pygame.draw.rect(surface, COLOR_CARD, expl_rect, 0, 6)
        pygame.draw.rect(surface, COLOR_OUTLINE, expl_rect, 1, 6)
        
        expl_lines = self._wrap_text(step.explanation, rect.width - 20, self.body_font)
        for i, line in enumerate(expl_lines[:max_lines]):
            txt = self.body_font.render(line, True, COLOR_TEXT)
            surface.blit(txt, (expl_rect.x + 10, expl_rect.y + 8 + i * 18))
        return expl_rect.bottom
    
    def _draw_card(self, surface, x, y, w, h):
        """Draw a standard card background. Returns the rect."""
        r = pygame.Rect(x, y, w, h)
        pygame.draw.rect(surface, COLOR_CARD, r, 0, 6)
        pygame.draw.rect(surface, COLOR_OUTLINE, r, 1, 6)
        return r
    
    def _draw_item_list(self, surface, items, x, y, max_items, formatter=None, best_item=None):
        """Draw a vertical list of items with optional best marker. Returns bottom y."""
        for i, item in enumerate(items[:max_items]):
            if y + i * 18 > self.y + self.height - 100:
                break
            item_y = y + i * 18
            
            label = formatter(item) if formatter else self._format_move(item)
            is_best = (item == best_item) if best_item is not None else (i == 0)
            prefix = "✅ " if is_best else "   "
            color = COLOR_JADE if is_best else COLOR_TEXT
            
            txt = self.tiny_font.render(f"{prefix}{label}", True, color)
            surface.blit(txt, (x, item_y))
        
        return y + min(len(items), max_items) * 18
    
    # ========================================================================
    # RENDERER: BFS / DFS (Nhóm A)
    # ========================================================================
    
    def _render_bfs_dfs(self, surface, step, rect):
        """Render BFS/DFS with Queue/Stack + Current + Explored columns"""
        bottom = self._draw_explanation_box(surface, step, rect)
        
        # 3 columns
        col_y = bottom + 10
        col_h = rect.bottom - col_y - 10
        col_w = (rect.width - 20) // 3
        
        ds_name = "QUEUE" if isinstance(step, BFSStep) else "STACK"
        ds_items = step.queue if isinstance(step, BFSStep) else step.stack
        
        columns = [
            ("CURRENT", [step.current_node] if step.current_node else [], COLOR_ACCENT),
            (ds_name, ds_items[:8], COLOR_JADE),
            ("EXPLORED", step.explored[:8], COLOR_TEXT_MUTED)
        ]
        
        for i, (title, items, color) in enumerate(columns):
            col_x = rect.x + i * (col_w + 10)
            col_rect = self._draw_card(surface, col_x, col_y, col_w - 10, col_h)
            
            hdr = self.small_font.render(title, True, color)
            surface.blit(hdr, (col_rect.centerx - hdr.get_width() // 2, col_rect.y + 8))
            pygame.draw.line(surface, COLOR_OUTLINE,
                           (col_rect.x + 5, col_rect.y + 28),
                           (col_rect.right - 5, col_rect.y + 28))
            
            for idx, item in enumerate(items):
                if idx > 8:
                    break
                iy = col_rect.y + 35 + idx * 20
                if isinstance(item, dict):
                    node_id = item.get('id', '')
                    depth = item.get('depth', '')
                    move = item.get('move')
                    
                    # Extract moving piece name and map it to friendly Vietnamese name
                    piece = item.get('piece', '')
                    piece_prefix = ""
                    if piece:
                        vi_name = PIECE_NAME_VI.get(piece, piece)
                        piece_prefix = vi_name + " "
                        
                    move_str = self._format_move_short(move) if move else ''
                    if move_str and move_str != '—':
                        if node_id:
                            label = f"{node_id}: {piece_prefix}{move_str} (d={depth})"
                        else:
                            label = f"{piece_prefix}{move_str} (d={depth})"
                    else:
                        if node_id:
                            label = f"{node_id} d={depth}"
                        else:
                            label = f"d={depth}"
                else:
                    label = str(item)[:18]
                txt = self.tiny_font.render(label, True, COLOR_TEXT)
                surface.blit(txt, (col_rect.x + 6, iy))
        
        # DFS backtracking badge
        if isinstance(step, DFSStep) and step.is_backtracking:
            badge_y = rect.bottom - 30
            badge = self.small_font.render("🔙 BACKTRACKING", True, COLOR_RED)
            surface.blit(badge, (rect.x + 10, badge_y))
    
    # ========================================================================
    # RENDERER: UCS / A* (Nhóm — existing, fixed)
    # ========================================================================
    
    def _render_search_3col(self, surface, step, rect):
        """Render 3-column layout for UCS/A*"""
        bottom = self._draw_explanation_box(surface, step, rect)
        
        col_y = bottom + 10
        col_h = rect.bottom - col_y - (70 if isinstance(step, AStarStep) else 10)
        col_w = (rect.width - 20) // 3
        
        columns = [
            ("CURRENT", [step.current_node], COLOR_ACCENT),
            ("FRONTIER", getattr(step, 'frontier', [])[:8], COLOR_JADE),
            ("EXPLORED", getattr(step, 'explored', [])[:8], COLOR_TEXT_MUTED)
        ]
        
        for i, (title, items, color) in enumerate(columns):
            col_x = rect.x + i * (col_w + 10)
            col_rect = self._draw_card(surface, col_x, col_y, col_w - 10, col_h)
            
            hdr = self.small_font.render(title, True, color)
            surface.blit(hdr, (col_rect.centerx - hdr.get_width() // 2, col_rect.y + 8))
            pygame.draw.line(surface, COLOR_OUTLINE,
                           (col_rect.x + 5, col_rect.y + 28),
                           (col_rect.right - 5, col_rect.y + 28))
            
            for idx, item in enumerate(items):
                if idx > 8:
                    break
                iy = col_rect.y + 35 + idx * 20
                
                if isinstance(step, UCSStep):
                    move_str = self._format_move_short(item)
                    cost = item.get('g_cost', 0) if isinstance(item, dict) else 0
                    label = f"{move_str} c={cost}"
                elif isinstance(step, AStarStep):
                    move_str = self._format_move_short(item)
                    f_val = item.get('f', 0) if isinstance(item, dict) else 0
                    try:
                        label = f"{move_str} f={f_val:.0f}"
                    except (TypeError, ValueError):
                        label = f"{move_str} f={f_val}"
                else:
                    label = str(item)[:20]
                
                txt = self.tiny_font.render(label, True, COLOR_TEXT)
                surface.blit(txt, (col_rect.x + 6, iy))
        
        # A* score breakdown
        if isinstance(step, AStarStep):
            self._render_score_breakdown_astar(surface, step, rect)
    
    # ========================================================================
    # RENDERER: IDA* (Nhóm C)
    # ========================================================================
    
    def _render_ida_star(self, surface, step, rect):
        """Render IDA* with threshold/iteration info"""
        bottom = self._draw_explanation_box(surface, step, rect)
        
        # Iteration + Threshold card
        info_rect = self._draw_card(surface, rect.x, bottom + 10, rect.width, 50)
        iter_txt = self.header_font.render(f"Iteration: {step.iteration}", True, COLOR_ACCENT)
        thresh_txt = self.header_font.render(f"Threshold: {step.threshold:.0f}", True, COLOR_JADE)
        surface.blit(iter_txt, (info_rect.x + 15, info_rect.y + 15))
        surface.blit(thresh_txt, (info_rect.centerx + 15, info_rect.y + 15))
        
        # Current node info
        if step.current_node:
            node_rect = self._draw_card(surface, rect.x, info_rect.bottom + 10, rect.width, 60)
            move_str = self._format_move_short(step.current_node)
            g = step.current_node.get('g', 0)
            h = step.current_node.get('h', 0)
            f = step.current_node.get('f', 0)
            
            node_txt = self.body_font.render(f"Node: {move_str}", True, COLOR_TEXT)
            surface.blit(node_txt, (node_rect.x + 15, node_rect.y + 10))
            
            try:
                vals_txt = self.body_font.render(f"g={g:.0f}  h={h:.0f}  f={f:.0f}", True, COLOR_TEXT_MUTED)
            except (TypeError, ValueError):
                vals_txt = self.body_font.render(f"g={g}  h={h}  f={f}", True, COLOR_TEXT_MUTED)
            surface.blit(vals_txt, (node_rect.x + 15, node_rect.y + 35))
            
            # Cutoff indicator
            cutoff_y = node_rect.bottom + 10
        else:
            cutoff_y = info_rect.bottom + 80
        
        if step.is_cutoff and step.exceeded_f is not None:
            cutoff_rect = self._draw_card(surface, rect.x, cutoff_y, rect.width, 40)
            try:
                cut_txt = self.body_font.render(
                    f"✂️ f({step.exceeded_f:.0f}) > threshold({step.threshold:.0f}) → CUTOFF",
                    True, COLOR_RED)
            except (TypeError, ValueError):
                cut_txt = self.body_font.render(f"✂️ CUTOFF", True, COLOR_RED)
            surface.blit(cut_txt, (cutoff_rect.x + 15, cutoff_rect.y + 10))
        elif not step.is_cutoff and step.current_node:
            pass_rect = self._draw_card(surface, rect.x, cutoff_y, rect.width, 40)
            pass_txt = self.body_font.render("✅ f ≤ threshold → tiếp tục", True, COLOR_JADE)
            surface.blit(pass_txt, (pass_rect.x + 15, pass_rect.y + 10))
    
    # ========================================================================
    # RENDERER: Greedy / Hill Climbing (Nhóm B)
    # ========================================================================
    
    def _render_candidates_list(self, surface, step, rect):
        """Render candidate/neighbor list for Greedy and Hill Climbing"""
        bottom = self._draw_explanation_box(surface, step, rect)
        
        # Current state card
        if isinstance(step, HillClimbStep):
            curr_str = self._format_move(step.current_move)
            items = step.neighbors
            label = "NEIGHBORS"
        else:  # GreedyStep
            curr_str = self._format_move(step.current_node)
            items = step.candidates
            label = "CANDIDATES"
        
        curr_rect = self._draw_card(surface, rect.x, bottom + 10, rect.width, 35)
        curr_txt = self.body_font.render(f"Hiện tại: {curr_str}", True, COLOR_JADE)
        surface.blit(curr_txt, (curr_rect.x + 15, curr_rect.y + 8))
        
        # Candidates/neighbors list
        list_y = curr_rect.bottom + 10
        list_h = rect.bottom - list_y - 10
        if isinstance(step, HillClimbStep) and step.is_plateau:
            list_h -= 30  # Room for plateau badge
        
        list_rect = self._draw_card(surface, rect.x, list_y, rect.width, list_h)
        
        lbl_txt = self.small_font.render(f"{label} (sorted by score):", True, COLOR_TEXT_MUTED)
        surface.blit(lbl_txt, (list_rect.x + 10, list_rect.y + 8))
        pygame.draw.line(surface, COLOR_OUTLINE,
                        (list_rect.x + 5, list_rect.y + 28),
                        (list_rect.right - 5, list_rect.y + 28))
        
        for i, item in enumerate(items[:10]):
            iy = list_rect.y + 35 + i * 18
            if iy > list_rect.bottom - 15:
                break
            item_str = self._format_move(item)
            is_first = (i == 0)
            prefix = "✅ " if is_first else "   "
            suffix = " ← BEST" if is_first else ""
            color = COLOR_JADE if is_first else COLOR_TEXT
            txt = self.tiny_font.render(f"{prefix}{item_str}{suffix}", True, color)
            surface.blit(txt, (list_rect.x + 8, iy))
        
        # Plateau warning for Hill Climbing
        if isinstance(step, HillClimbStep) and step.is_plateau:
            plat_y = list_rect.bottom + 5
            plat_txt = self.small_font.render("⚠️ PLATEAU: best ≤ current", True, COLOR_RED)
            surface.blit(plat_txt, (rect.x + 10, plat_y))
    
    # ========================================================================
    # RENDERER: SA (existing, fixed)
    # ========================================================================
    
    def _render_sa(self, surface, step, rect):
        """Render Simulated Annealing with temperature"""
        # Temperature display
        temp_rect = self._draw_card(surface, rect.x, rect.y, rect.width, 70)
        
        temp_lbl = self.small_font.render("NHIỆT ĐỘ", True, COLOR_TEXT_MUTED)
        surface.blit(temp_lbl, (temp_rect.x + 15, temp_rect.y + 8))
        
        temp_val = self.title_font.render(f"T = {step.temperature:.1f}", True, COLOR_ACCENT)
        surface.blit(temp_val, (temp_rect.centerx - temp_val.get_width() // 2, temp_rect.y + 32))
        
        # Current vs Candidate comparison — now with move info
        comp_y = rect.y + 80
        comp_rect = self._draw_card(surface, rect.x, comp_y, rect.width, 80)
        
        curr_str = self._format_move(step.current_move)
        cand_str = self._format_move(step.candidate_move)
        
        curr_txt = self.body_font.render(f"Current: {curr_str}", True, COLOR_JADE)
        cand_txt = self.body_font.render(f"Candidate: {cand_str}", True,
                                        COLOR_RED if step.delta_e < 0 else COLOR_JADE)
        
        surface.blit(curr_txt, (comp_rect.x + 15, comp_rect.y + 15))
        surface.blit(cand_txt, (comp_rect.x + 15, comp_rect.y + 45))
        
        # Delta E and acceptance probability
        formula_y = comp_y + 90
        formula_rect = self._draw_card(surface, rect.x, formula_y, rect.width, 110)
        
        delta_txt = self.body_font.render(f"ΔE = {step.delta_e:.0f}", True,
                                         COLOR_RED if step.delta_e < 0 else COLOR_JADE)
        surface.blit(delta_txt, (formula_rect.x + 15, formula_rect.y + 12))
        
        prob_txt = self.body_font.render(f"P(accept) = e^(ΔE/T) = {step.accept_prob:.3f}",
                                        True, COLOR_TEXT)
        surface.blit(prob_txt, (formula_rect.x + 15, formula_rect.y + 40))
        
        # Decision
        decision_icon = "✅ CHẤP NHẬN" if step.accepted else "❌ TỪ CHỐI"
        decision_color = COLOR_JADE if step.accepted else COLOR_RED
        decision = self.header_font.render(decision_icon, True, decision_color)
        surface.blit(decision, (formula_rect.x + 15, formula_rect.y + 72))
        
        # Explanation at bottom
        expl_lines = self._wrap_text(step.explanation, rect.width - 20, self.small_font)
        for i, line in enumerate(expl_lines[:2]):
            txt = self.small_font.render(line, True, COLOR_TEXT_MUTED)
            surface.blit(txt, (rect.x + 10, formula_rect.bottom + 8 + i * 16))
    
    # ========================================================================
    # RENDERER: Beam Search (Nhóm D)
    # ========================================================================
    
    def _render_beam(self, surface, step, rect):
        """Render Beam Search with kept/eliminated columns"""
        bottom = self._draw_explanation_box(surface, step, rect)
        
        # Two columns: Kept | Eliminated
        col_y = bottom + 10
        col_w = (rect.width - 10) // 2
        
        # Worst case scores area
        has_worst = len(step.worst_case_scores) > 0
        col_h = rect.bottom - col_y - (60 if has_worst else 10)
        
        # Kept column
        kept_rect = self._draw_card(surface, rect.x, col_y, col_w - 5, col_h)
        kept_lbl = self.small_font.render(f"KEPT (top {step.beam_k})", True, COLOR_JADE)
        surface.blit(kept_lbl, (kept_rect.x + 8, kept_rect.y + 8))
        pygame.draw.line(surface, COLOR_OUTLINE,
                        (kept_rect.x + 5, kept_rect.y + 28),
                        (kept_rect.right - 5, kept_rect.y + 28))
        for i, item in enumerate(step.kept_beams[:6]):
            iy = kept_rect.y + 35 + i * 18
            if iy > kept_rect.bottom - 15:
                break
            txt = self.tiny_font.render(f"✅ {self._format_move(item)}", True, COLOR_JADE)
            surface.blit(txt, (kept_rect.x + 6, iy))
        
        # Eliminated column
        elim_rect = self._draw_card(surface, rect.x + col_w + 5, col_y, col_w - 5, col_h)
        elim_lbl = self.small_font.render("ELIMINATED", True, COLOR_RED)
        surface.blit(elim_lbl, (elim_rect.x + 8, elim_rect.y + 8))
        pygame.draw.line(surface, COLOR_OUTLINE,
                        (elim_rect.x + 5, elim_rect.y + 28),
                        (elim_rect.right - 5, elim_rect.y + 28))
        for i, item in enumerate(step.eliminated[:6]):
            iy = elim_rect.y + 35 + i * 18
            if iy > elim_rect.bottom - 15:
                break
            txt = self.tiny_font.render(f"❌ {self._format_move(item)}", True, COLOR_RED)
            surface.blit(txt, (elim_rect.x + 6, iy))
        
        # Worst-case scores
        if has_worst:
            wc_rect = self._draw_card(surface, rect.x, col_y + col_h + 5, rect.width, 50)
            wc_lbl = self.small_font.render("Worst-case analysis:", True, COLOR_TEXT_MUTED)
            surface.blit(wc_lbl, (wc_rect.x + 10, wc_rect.y + 8))
            
            wc_parts = []
            for wc in step.worst_case_scores[:3]:
                ms = self._format_move_short(wc)
                ws = wc.get('worst_score', wc.get('score', '?'))
                wc_parts.append(f"{ms}: {ws}")
            wc_txt = self.tiny_font.render("  |  ".join(wc_parts), True, COLOR_TEXT)
            surface.blit(wc_txt, (wc_rect.x + 10, wc_rect.y + 30))
    
    # ========================================================================
    # RENDERER: Level 4 — Online / AND-OR / Belief (Nhóm E)
    # ========================================================================
    
    def _render_level4(self, surface, step, rect):
        """Dispatch to specific Level 4 renderer"""
        if isinstance(step, OnlineStep):
            self._render_online(surface, step, rect)
        elif isinstance(step, AndOrStep):
            self._render_andor(surface, step, rect)
        elif isinstance(step, BeliefStep):
            self._render_belief(surface, step, rect)
    
    def _render_online(self, surface, step, rect):
        """Online Search: check status + weight changes + candidates"""
        bottom = self._draw_explanation_box(surface, step, rect)
        
        # Check status badge
        status_rect = self._draw_card(surface, rect.x, bottom + 10, rect.width, 35)
        if step.in_check:
            badge = self.header_font.render("⚠️ ĐANG BỊ CHIẾU", True, COLOR_RED)
        else:
            badge = self.header_font.render("✅ AN TOÀN", True, COLOR_JADE)
        surface.blit(badge, (status_rect.x + 15, status_rect.y + 8))
        
        # Weight comparison — 2 columns
        weight_y = status_rect.bottom + 10
        col_w = (rect.width - 10) // 2
        avail_h = rect.bottom - weight_y - 10
        
        if step.candidates:
            weight_h = min(avail_h // 2, 120)
        else:
            weight_h = avail_h
        
        # Before column
        before_rect = self._draw_card(surface, rect.x, weight_y, col_w - 5, weight_h)
        b_lbl = self.small_font.render("TRƯỚC", True, COLOR_TEXT_MUTED)
        surface.blit(b_lbl, (before_rect.x + 8, before_rect.y + 8))
        for i, (k, v) in enumerate(list(step.weights_before.items())[:6]):
            iy = before_rect.y + 28 + i * 16
            if iy > before_rect.bottom - 12:
                break
            vi_name = PIECE_NAME_VI.get(k, k)
            txt = self.tiny_font.render(f"{vi_name}: {v}", True, COLOR_TEXT)
            surface.blit(txt, (before_rect.x + 8, iy))
        
        # After column
        after_rect = self._draw_card(surface, rect.x + col_w + 5, weight_y, col_w - 5, weight_h)
        a_lbl = self.small_font.render("SAU", True, COLOR_ACCENT)
        surface.blit(a_lbl, (after_rect.x + 8, after_rect.y + 8))
        for i, (k, v) in enumerate(list(step.weights_after.items())[:6]):
            iy = after_rect.y + 28 + i * 16
            if iy > after_rect.bottom - 12:
                break
            vi_name = PIECE_NAME_VI.get(k, k)
            changed = step.weights_before.get(k) != v
            color = COLOR_JADE if changed else COLOR_TEXT
            txt = self.tiny_font.render(f"{vi_name}: {v}", True, color)
            surface.blit(txt, (after_rect.x + 8, iy))
        
        # Candidates list
        if step.candidates:
            cand_y = weight_y + weight_h + 10
            cand_rect = self._draw_card(surface, rect.x, cand_y, rect.width, rect.bottom - cand_y - 5)
            c_lbl = self.small_font.render("TOP CANDIDATES:", True, COLOR_TEXT_MUTED)
            surface.blit(c_lbl, (cand_rect.x + 10, cand_rect.y + 8))
            for i, item in enumerate(step.candidates[:5]):
                iy = cand_rect.y + 28 + i * 18
                if iy > cand_rect.bottom - 12:
                    break
                is_best = (i == 0)
                prefix = "✅ " if is_best else "   "
                txt = self.tiny_font.render(f"{prefix}{self._format_move(item)}", True,
                                          COLOR_JADE if is_best else COLOR_TEXT)
                surface.blit(txt, (cand_rect.x + 8, iy))
    
    def _render_andor(self, surface, step, rect):
        """AND-OR Search: OR node + AND responses + worst case"""
        bottom = self._draw_explanation_box(surface, step, rect)
        
        # OR node (our move)
        or_rect = self._draw_card(surface, rect.x, bottom + 10, rect.width, 35)
        or_move = self._format_move(step.or_node)
        or_txt = self.body_font.render(f"OR NODE (ta): {or_move}", True, COLOR_ACCENT)
        surface.blit(or_txt, (or_rect.x + 15, or_rect.y + 8))
        
        # AND responses (opponent)
        and_y = or_rect.bottom + 10
        and_h = rect.bottom - and_y - 50
        and_rect = self._draw_card(surface, rect.x, and_y, rect.width, and_h)
        and_lbl = self.small_font.render("AND RESPONSES (đối thủ):", True, COLOR_TEXT_MUTED)
        surface.blit(and_lbl, (and_rect.x + 10, and_rect.y + 8))
        pygame.draw.line(surface, COLOR_OUTLINE,
                        (and_rect.x + 5, and_rect.y + 28),
                        (and_rect.right - 5, and_rect.y + 28))
        
        for i, resp in enumerate(step.and_responses[:6]):
            iy = and_rect.y + 35 + i * 18
            if iy > and_rect.bottom - 12:
                break
            resp_str = self._format_move(resp)
            is_worst = (resp == step.and_responses[-1]) if step.and_responses else False
            suffix = " ← WORST" if is_worst else ""
            color = COLOR_RED if is_worst else COLOR_TEXT
            txt = self.tiny_font.render(f"  {resp_str}{suffix}", True, color)
            surface.blit(txt, (and_rect.x + 8, iy))
        
        # Guaranteed score
        gs_rect = self._draw_card(surface, rect.x, and_rect.bottom + 5, rect.width, 35)
        gs_txt = self.body_font.render(f"Guaranteed score: {step.guaranteed_score:.0f}", True, COLOR_ACCENT)
        surface.blit(gs_txt, (gs_rect.x + 15, gs_rect.y + 8))
    
    def _render_belief(self, surface, step, rect):
        """Belief State: style detection + probability + expected utility"""
        bottom = self._draw_explanation_box(surface, step, rect)
        
        # Detected style
        style_rect = self._draw_card(surface, rect.x, bottom + 10, rect.width, 55)
        style_txt = self.header_font.render(
            f"Phong cách: {step.opponent_style.upper()}", True, COLOR_ACCENT)
        surface.blit(style_txt, (style_rect.x + 15, style_rect.y + 8))
        
        # Probability distribution
        probs = step.belief_probs
        prob_parts = [f"P({k[:3]})={v:.1f}" for k, v in probs.items()]
        prob_txt = self.small_font.render("  ".join(prob_parts), True, COLOR_TEXT_MUTED)
        surface.blit(prob_txt, (style_rect.x + 15, style_rect.y + 32))
        
        # Utility per style
        if step.utility_per_style:
            util_rect = self._draw_card(surface, rect.x, style_rect.bottom + 10, rect.width, 80)
            util_lbl = self.small_font.render("Utility per style:", True, COLOR_TEXT_MUTED)
            surface.blit(util_lbl, (util_rect.x + 10, util_rect.y + 8))
            
            for i, (style, val) in enumerate(step.utility_per_style.items()):
                iy = util_rect.y + 28 + i * 16
                try:
                    txt = self.tiny_font.render(f"  {style}: {val:.0f}", True, COLOR_TEXT)
                except (TypeError, ValueError):
                    txt = self.tiny_font.render(f"  {style}: {val}", True, COLOR_TEXT)
                surface.blit(txt, (util_rect.x + 10, iy))
            
            # Expected utility formula
            eu_y = util_rect.bottom + 10
        else:
            eu_y = style_rect.bottom + 100
        
        if step.expected_utility:
            eu_rect = self._draw_card(surface, rect.x, eu_y, rect.width, 35)
            try:
                eu_txt = self.body_font.render(
                    f"E[U] = {step.expected_utility:.0f}", True, COLOR_JADE)
            except (TypeError, ValueError):
                eu_txt = self.body_font.render(f"E[U] = {step.expected_utility}", True, COLOR_JADE)
            surface.blit(eu_txt, (eu_rect.x + 15, eu_rect.y + 8))
    
    # ========================================================================
    # RENDERER: CSP — Backtracking / Min-Conflicts / AC-3 (Nhóm F)
    # ========================================================================
    
    def _render_csp(self, surface, step, rect):
        """Dispatch to specific CSP renderer"""
        if isinstance(step, BacktrackStep):
            self._render_backtrack(surface, step, rect)
        elif isinstance(step, MinConflictStep):
            self._render_min_conflicts(surface, step, rect)
        elif isinstance(step, AC3Step):
            self._render_ac3(surface, step, rect)
    
    def _render_backtrack(self, surface, step, rect):
        """Backtracking MRV: variables + domain + best assignment"""
        bottom = self._draw_explanation_box(surface, step, rect)
        
        # Variables with domain sizes
        vars_h = min(150, len(step.variables) * 18 + 35)
        vars_rect = self._draw_card(surface, rect.x, bottom + 10, rect.width, vars_h)
        vars_lbl = self.small_font.render("VARIABLES (domain size):", True, COLOR_TEXT_MUTED)
        surface.blit(vars_lbl, (vars_rect.x + 10, vars_rect.y + 8))
        
        chosen = step.chosen_variable
        for i, (pos, size) in enumerate(list(step.variables.items())[:6]):
            iy = vars_rect.y + 28 + i * 18
            if iy > vars_rect.bottom - 12:
                break
            is_chosen = (str(pos) == str(chosen))
            prefix = "✅ " if is_chosen else "   "
            suffix = " ← MRV" if is_chosen else ""
            color = COLOR_JADE if is_chosen else COLOR_TEXT
            txt = self.tiny_font.render(f"{prefix}{pos}: domain={size}{suffix}", True, color)
            surface.blit(txt, (vars_rect.x + 8, iy))
        
        # Domain for chosen variable
        if step.domain:
            dom_y = vars_rect.bottom + 10
            dom_h = rect.bottom - dom_y - 10
            dom_rect = self._draw_card(surface, rect.x, dom_y, rect.width, dom_h)
            dom_lbl = self.small_font.render(f"DOMAIN cho {chosen}:", True, COLOR_TEXT_MUTED)
            surface.blit(dom_lbl, (dom_rect.x + 10, dom_rect.y + 8))
            
            for i, item in enumerate(step.domain[:8]):
                iy = dom_rect.y + 28 + i * 18
                if iy > dom_rect.bottom - 12:
                    break
                is_best = (i == 0)
                prefix = "✅ " if is_best else "   "
                suffix = " ← BEST" if is_best else ""
                color = COLOR_JADE if is_best else COLOR_TEXT
                txt = self.tiny_font.render(f"{prefix}{self._format_move(item)}{suffix}", True, color)
                surface.blit(txt, (dom_rect.x + 8, iy))
    
    def _render_min_conflicts(self, surface, step, rect):
        """Min-Conflicts: conflict counts + candidates"""
        bottom = self._draw_explanation_box(surface, step, rect)
        
        # Conflict summary
        best_cand = step.best_candidate
        after = best_cand.get('conflicts_after', 0) if isinstance(best_cand, dict) else 0
        diff = step.current_conflicts - after
        
        conf_rect = self._draw_card(surface, rect.x, bottom + 10, rect.width, 40)
        conf_txt = self.body_font.render(
            f"Conflicts: {step.current_conflicts} → {after} (giảm {diff})",
            True, COLOR_JADE if diff > 0 else COLOR_TEXT)
        surface.blit(conf_txt, (conf_rect.x + 15, conf_rect.y + 10))
        
        # Candidates list
        cand_y = conf_rect.bottom + 10
        cand_rect = self._draw_card(surface, rect.x, cand_y, rect.width, rect.bottom - cand_y - 10)
        cand_lbl = self.small_font.render("TOP CANDIDATES (by conflicts):", True, COLOR_TEXT_MUTED)
        surface.blit(cand_lbl, (cand_rect.x + 10, cand_rect.y + 8))
        pygame.draw.line(surface, COLOR_OUTLINE,
                        (cand_rect.x + 5, cand_rect.y + 28),
                        (cand_rect.right - 5, cand_rect.y + 28))
        
        for i, item in enumerate(step.candidates[:8]):
            iy = cand_rect.y + 35 + i * 18
            if iy > cand_rect.bottom - 12:
                break
            move_str = self._format_move_short(item)
            conflicts = item.get('conflicts_after', '?') if isinstance(item, dict) else '?'
            is_best = (i == 0)
            prefix = "✅ " if is_best else "   "
            suffix = " ← BEST" if is_best else ""
            color = COLOR_JADE if is_best else COLOR_TEXT
            txt = self.tiny_font.render(
                f"{prefix}{move_str} conflicts={conflicts}{suffix}", True, color)
            surface.blit(txt, (cand_rect.x + 8, iy))
    
    def _render_ac3(self, surface, step, rect):
        """AC-3: safe/pruned columns + chosen move"""
        bottom = self._draw_explanation_box(surface, step, rect)
        
        # Two columns: Safe | Pruned
        col_y = bottom + 10
        col_w = (rect.width - 10) // 2
        col_h = rect.bottom - col_y - 50
        
        # Safe column
        safe_rect = self._draw_card(surface, rect.x, col_y, col_w - 5, col_h)
        safe_cnt = len(step.safe_moves)
        safe_lbl = self.small_font.render(f"SAFE ✅ ({safe_cnt})", True, COLOR_JADE)
        surface.blit(safe_lbl, (safe_rect.x + 8, safe_rect.y + 8))
        pygame.draw.line(surface, COLOR_OUTLINE,
                        (safe_rect.x + 5, safe_rect.y + 28),
                        (safe_rect.right - 5, safe_rect.y + 28))
        for i, item in enumerate(step.safe_moves[:6]):
            iy = safe_rect.y + 35 + i * 18
            if iy > safe_rect.bottom - 12:
                break
            txt = self.tiny_font.render(f"  {self._format_move(item)}", True, COLOR_TEXT)
            surface.blit(txt, (safe_rect.x + 6, iy))
        
        # Pruned column
        pruned_rect = self._draw_card(surface, rect.x + col_w + 5, col_y, col_w - 5, col_h)
        pruned_cnt = len(step.pruned_moves)
        pruned_lbl = self.small_font.render(f"PRUNED ❌ ({pruned_cnt})", True, COLOR_RED)
        surface.blit(pruned_lbl, (pruned_rect.x + 8, pruned_rect.y + 8))
        pygame.draw.line(surface, COLOR_OUTLINE,
                        (pruned_rect.x + 5, pruned_rect.y + 28),
                        (pruned_rect.right - 5, pruned_rect.y + 28))
        for i, item in enumerate(step.pruned_moves[:6]):
            iy = pruned_rect.y + 35 + i * 18
            if iy > pruned_rect.bottom - 12:
                break
            reason = item.get('reason', '') if isinstance(item, dict) else ''
            move_str = self._format_move_short(item)
            label = f"{move_str}: {reason}" if reason else move_str
            txt = self.tiny_font.render(f"  {label[:30]}", True, COLOR_RED)
            surface.blit(txt, (pruned_rect.x + 6, iy))
        
        # Chosen move
        chosen_rect = self._draw_card(surface, rect.x, col_y + col_h + 5, rect.width, 35)
        chosen_str = self._format_move(step.chosen_from_safe)
        chosen_txt = self.body_font.render(f"✅ CHOSEN: {chosen_str}", True, COLOR_JADE)
        surface.blit(chosen_txt, (chosen_rect.x + 15, chosen_rect.y + 8))
    
    # ========================================================================
    # RENDERER: Alpha-Beta (existing, fixed)
    # ========================================================================
    
    def _render_alpha_beta(self, surface, step, rect):
        """Render Alpha-Beta tree visualization"""
        # Explanation
        bottom = self._draw_explanation_box(surface, step, rect, max_lines=2, height=50)
        
        # Path display
        path_y = bottom + 10
        path_rect = self._draw_card(surface, rect.x, path_y, rect.width, 70)
        
        path_lbl = self.small_font.render("PATH:", True, COLOR_ACCENT)
        surface.blit(path_lbl, (path_rect.x + 10, path_rect.y + 8))
        
        path = step.current_path[:5]
        for i, node in enumerate(path):
            x = path_rect.x + 60 + i * 60
            y = path_rect.y + 25
            
            pygame.draw.circle(surface, COLOR_JADE if i == len(path) - 1 else COLOR_TEXT_MUTED,
                             (x, y), 12)
            pygame.draw.circle(surface, COLOR_OUTLINE, (x, y), 12, 1)
            
            depth = node.get('depth', i)
            d_txt = self.tiny_font.render(f"d{depth}", True, COLOR_BG)
            surface.blit(d_txt, (x - d_txt.get_width() // 2, y - d_txt.get_height() // 2))
            
            if i < len(path) - 1:
                pygame.draw.line(surface, COLOR_OUTLINE, (x + 12, y), (x + 48, y), 2)
                pygame.draw.polygon(surface, COLOR_OUTLINE, [
                    (x + 48, y), (x + 43, y - 3), (x + 43, y + 3)
                ])
        
        # Alpha/Beta display
        ab_y = path_y + 80
        ab_rect = self._draw_card(surface, rect.x, ab_y, rect.width, 50)
        
        alpha_txt = self.header_font.render(f"α = {step.alpha:.0f}", True, COLOR_JADE)
        beta_txt = self.header_font.render(f"β = {step.beta:.0f}", True, COLOR_RED)
        
        surface.blit(alpha_txt, (ab_rect.x + 30, ab_rect.centery - alpha_txt.get_height() // 2))
        surface.blit(beta_txt, (ab_rect.centerx + 30, ab_rect.centery - beta_txt.get_height() // 2))
        
        # Pruning indicator
        if step.is_pruned:
            prune_txt = self.body_font.render(f"✂️ {step.prune_reason}", True, COLOR_RED)
            surface.blit(prune_txt, (rect.x + 10, ab_rect.bottom + 10))
        
        # Siblings display — now with move info
        sib_y = ab_y + 70 if not step.is_pruned else ab_y + 90
        sib_rect = pygame.Rect(rect.x, sib_y, rect.width, rect.bottom - sib_y - 10)
        
        if sib_rect.height > 50:
            self._draw_card(surface, sib_rect.x, sib_rect.y, sib_rect.width, sib_rect.height)
            
            sib_lbl = self.small_font.render("Siblings:", True, COLOR_TEXT_MUTED)
            surface.blit(sib_lbl, (sib_rect.x + 10, sib_rect.y + 8))
            
            for i, sib in enumerate(step.siblings_evaluated[:6]):
                y = sib_rect.y + 30 + i * 18
                if y > sib_rect.bottom - 12:
                    break
                val = sib.get('value', 0)
                move_str = self._format_move_short(sib.get('move'))
                try:
                    txt = self.tiny_font.render(f"  {move_str} val:{val:.0f}", True, COLOR_TEXT)
                except (TypeError, ValueError):
                    txt = self.tiny_font.render(f"  {move_str} val:{val}", True, COLOR_TEXT)
                surface.blit(txt, (sib_rect.x + 10, y))
    
    # ========================================================================
    # RENDERER: Minimax / Expectimax (Nhóm G)
    # ========================================================================
    
    def _render_minimax_expectimax(self, surface, step, rect):
        """Render Minimax or Expectimax"""
        if isinstance(step, ExpectimaxStep):
            self._render_expectimax(surface, step, rect)
        else:
            self._render_minimax(surface, step, rect)
    
    def _render_minimax(self, surface, step, rect):
        """Minimax: path + node type + siblings + best so far"""
        bottom = self._draw_explanation_box(surface, step, rect, max_lines=2, height=50)
        
        # Path display (reuse alpha-beta style)
        path_y = bottom + 10
        path_rect = self._draw_card(surface, rect.x, path_y, rect.width, 65)
        
        path_lbl = self.small_font.render("PATH:", True, COLOR_ACCENT)
        surface.blit(path_lbl, (path_rect.x + 10, path_rect.y + 8))
        
        path = step.current_path[:5]
        for i, node in enumerate(path):
            x = path_rect.x + 60 + i * 60
            y = path_rect.y + 25
            is_max = node.get('is_max', True) if isinstance(node, dict) else True
            color = COLOR_JADE if i == len(path) - 1 else COLOR_TEXT_MUTED
            
            pygame.draw.circle(surface, color, (x, y), 12)
            pygame.draw.circle(surface, COLOR_OUTLINE, (x, y), 12, 1)
            
            label = "▲" if is_max else "▼"
            d_txt = self.tiny_font.render(label, True, COLOR_BG)
            surface.blit(d_txt, (x - d_txt.get_width() // 2, y - d_txt.get_height() // 2))
            
            if i < len(path) - 1:
                pygame.draw.line(surface, COLOR_OUTLINE, (x + 12, y), (x + 48, y), 2)
        
        # Node type + value
        node = step.current_node
        is_max = node.get('is_max', True) if isinstance(node, dict) else True
        value = node.get('value', 0) if isinstance(node, dict) else 0
        
        type_rect = self._draw_card(surface, rect.x, path_rect.bottom + 10, rect.width, 40)
        type_label = "MAX" if is_max else "MIN"
        try:
            type_txt = self.header_font.render(f"{type_label} node  VALUE: {value:.0f}", True, COLOR_ACCENT)
        except (TypeError, ValueError):
            type_txt = self.header_font.render(f"{type_label} node  VALUE: {value}", True, COLOR_ACCENT)
        surface.blit(type_txt, (type_rect.x + 15, type_rect.y + 10))
        
        # Siblings
        sib_y = type_rect.bottom + 10
        sib_rect = self._draw_card(surface, rect.x, sib_y, rect.width, rect.bottom - sib_y - 10)
        
        sib_lbl = self.small_font.render("Siblings:", True, COLOR_TEXT_MUTED)
        surface.blit(sib_lbl, (sib_rect.x + 10, sib_rect.y + 8))
        
        for i, sib in enumerate(step.siblings_evaluated[:6]):
            iy = sib_rect.y + 28 + i * 18
            if iy > sib_rect.bottom - 12:
                break
            val = sib.get('value', 0)
            move_str = self._format_move_short(sib.get('move'))
            try:
                txt = self.tiny_font.render(f"  {move_str} val:{val:.0f}", True, COLOR_TEXT)
            except (TypeError, ValueError):
                txt = self.tiny_font.render(f"  {move_str} val:{val}", True, COLOR_TEXT)
            surface.blit(txt, (sib_rect.x + 10, iy))
        
        # Best so far
        if step.best_so_far:
            best_str = self._format_move(step.best_so_far)
            best_txt = self.small_font.render(f"Best so far: {best_str}", True, COLOR_JADE)
            surface.blit(best_txt, (sib_rect.x + 10, sib_rect.bottom - 22))
    
    def _render_expectimax(self, surface, step, rect):
        """Expectimax: chance node + child values + expected value formula"""
        bottom = self._draw_explanation_box(surface, step, rect)
        
        # Node type badge
        node_rect = self._draw_card(surface, rect.x, bottom + 10, rect.width, 40)
        if step.is_chance_node:
            node_txt = self.header_font.render("🎲 CHANCE NODE", True, COLOR_ACCENT)
        else:
            node_txt = self.header_font.render("▲ MAX NODE", True, COLOR_JADE)
        depth = step.current_node.get('depth', '?') if isinstance(step.current_node, dict) else '?'
        surface.blit(node_txt, (node_rect.x + 15, node_rect.y + 10))
        depth_txt = self.small_font.render(f"depth={depth}", True, COLOR_TEXT_MUTED)
        surface.blit(depth_txt, (node_rect.right - depth_txt.get_width() - 15, node_rect.y + 13))
        
        # Child values
        if step.child_values:
            children_rect = self._draw_card(surface, rect.x, node_rect.bottom + 10, rect.width, 80)
            c_lbl = self.small_font.render("Child values:", True, COLOR_TEXT_MUTED)
            surface.blit(c_lbl, (children_rect.x + 10, children_rect.y + 8))
            
            vals = [cv.get('value', 0) if isinstance(cv, dict) else cv for cv in step.child_values[:8]]
            try:
                vals_str = ", ".join(f"{v:.0f}" for v in vals)
            except (TypeError, ValueError):
                vals_str = ", ".join(str(v) for v in vals)
            vals_txt = self.body_font.render(vals_str, True, COLOR_TEXT)
            surface.blit(vals_txt, (children_rect.x + 15, children_rect.y + 30))
            
            try:
                best_txt = self.small_font.render(f"Best = {step.best_value:.0f}", True, COLOR_JADE)
            except (TypeError, ValueError):
                best_txt = self.small_font.render(f"Best = {step.best_value}", True, COLOR_JADE)
            surface.blit(best_txt, (children_rect.x + 15, children_rect.y + 55))
            
            formula_y = children_rect.bottom + 10
        else:
            formula_y = node_rect.bottom + 100
        
        # Expected value formula
        if step.expected_value is not None:
            formula_rect = self._draw_card(surface, rect.x, formula_y, rect.width, 60)
            try:
                e_txt = self.body_font.render(
                    f"E[V] = 0.7 × {step.best_value:.0f} + 0.3 × avg",
                    True, COLOR_TEXT)
                result_txt = self.header_font.render(
                    f"= {step.expected_value:.0f}", True, COLOR_JADE)
            except (TypeError, ValueError):
                e_txt = self.body_font.render(f"E[V] = {step.expected_value}", True, COLOR_TEXT)
                result_txt = self.header_font.render("", True, COLOR_JADE)
            surface.blit(e_txt, (formula_rect.x + 15, formula_rect.y + 10))
            surface.blit(result_txt, (formula_rect.x + 15, formula_rect.y + 35))
    
    # ========================================================================
    # FALLBACK RENDERER
    # ========================================================================
    
    def _render_text_only(self, surface, step, rect):
        """Fallback text-only renderer for unknown step types"""
        expl_rect = pygame.Rect(rect.x, rect.y, rect.width, rect.height)
        pygame.draw.rect(surface, COLOR_CARD, expl_rect, 0, 8)
        pygame.draw.rect(surface, COLOR_OUTLINE, expl_rect, 1, 8)
        
        algo_lbl = self.header_font.render(step.algorithm, True, COLOR_ACCENT)
        surface.blit(algo_lbl, (expl_rect.x + 15, expl_rect.y + 15))
        
        pygame.draw.line(surface, COLOR_OUTLINE,
                        (expl_rect.x + 15, expl_rect.y + 45),
                        (expl_rect.right - 15, expl_rect.y + 45))
        
        expl_lines = self._wrap_text(step.explanation, rect.width - 30, self.body_font)
        for i, line in enumerate(expl_lines[:15]):
            txt = self.body_font.render(line, True, COLOR_TEXT)
            surface.blit(txt, (expl_rect.x + 15, expl_rect.y + 60 + i * 20))
        
        info_y = expl_rect.y + 60 + min(len(expl_lines), 15) * 20 + 20
        self._render_generic_fields(surface, step, expl_rect.x + 15, info_y, rect.width - 30)
    
    def _render_generic_fields(self, surface, step, x, y, max_width):
        """Render common fields from step dataclass"""
        fields_to_show = []
        
        for key, val in step.__dict__.items():
            if key in ['step_num', 'algorithm', 'explanation', 'chosen_move']:
                continue
            if isinstance(val, (int, float, str, bool)):
                fields_to_show.append((key, val))
        
        for i, (key, val) in enumerate(fields_to_show[:8]):
            if y + i * 18 > self.y + self.height - 100:
                break
            
            txt = self.small_font.render(f"{key}: {val}", True, COLOR_TEXT_MUTED)
            surface.blit(txt, (x, y + i * 18))
    
    def _render_score_breakdown_astar(self, surface, step, rect):
        """Render score breakdown for A* at bottom"""
        if not isinstance(step, AStarStep):
            return
        
        node = step.current_node
        g = node.get('g', 0)
        h = node.get('h', 0)
        f = node.get('f', 0)
        
        break_y = rect.bottom - 60
        break_rect = self._draw_card(surface, rect.x, break_y, rect.width, 50)
        
        try:
            formula = self.body_font.render(f"f(n) = g(n) + h(n) = {g:.0f} + {h:.0f} = {f:.0f}",
                                           True, COLOR_ACCENT)
        except (TypeError, ValueError):
            formula = self.body_font.render(f"f(n) = g + h = {g} + {h} = {f}", True, COLOR_ACCENT)
        surface.blit(formula, (break_rect.centerx - formula.get_width() // 2,
                              break_rect.centery - formula.get_height() // 2))
    
    def _wrap_text(self, text, max_width, font):
        """Wrap text to fit within max_width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
