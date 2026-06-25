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
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # Fonts
        self.title_font = pygame.font.SysFont(["Segoe UI", "Arial"], 20, bold=True)
        self.header_font = pygame.font.SysFont(["Segoe UI", "Arial"], 16, bold=True)
        self.body_font = pygame.font.SysFont(["Segoe UI", "Arial"], 14)
        self.mono_font = pygame.font.SysFont(["Consolas", "Courier New"], 13)
        self.small_font = pygame.font.SysFont(["Segoe UI", "Arial"], 12)
        self.tiny_font = pygame.font.SysFont(["Segoe UI", "Arial"], 10)
        
        # Navigation buttons
        btn_y = y + height - 60
        btn_w = 80
        gap = 10
        center_x = x + width // 2
        
        self.btn_prev = pygame.Rect(center_x - btn_w * 1.5 - gap, btn_y, btn_w, 36)
        self.btn_next = pygame.Rect(center_x - btn_w // 2, btn_y, btn_w, 36)
        self.btn_auto = pygame.Rect(center_x + btn_w // 2 + gap, btn_y, btn_w, 36)
        
        # Scroll state for long lists
        self.scroll_offset = 0
        self.max_scroll = 0
        
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
        
        elif event.type == pygame.MOUSEWHEEL:
            # Scroll content if needed
            self.scroll_offset = max(0, min(self.max_scroll, self.scroll_offset - event.y * 20))
            
        return None
    
    def draw(self, surface, step: BaseStep, controller, recorder):
        """Main render method"""
        # Background
        bg_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, COLOR_BG, bg_rect)
        pygame.draw.line(surface, COLOR_OUTLINE, (self.x, self.y), (self.x, self.y + self.height), 2)
        
        if step is None:
            self._render_empty(surface)
            return
        
        # Header with step counter
        self._render_header(surface, step, recorder)
        
        # Body - delegate to specific renderer
        content_y = self.y + 80
        content_rect = pygame.Rect(self.x + 15, content_y, self.width - 30, self.height - 160)
        
        if isinstance(step, (UCSStep, AStarStep)):
            self._render_search_3col(surface, step, content_rect)
        elif isinstance(step, AlphaBetaStep):
            self._render_alpha_beta(surface, step, content_rect)
        elif isinstance(step, SAStep):
            self._render_sa(surface, step, content_rect)
        else:
            # Fallback: text-only explanation
            self._render_text_only(surface, step, content_rect)
        
        # Navigation footer
        self._render_footer(surface, controller, recorder)
    
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
             COLOR_JADE if controller.mode == "auto" else COLOR_ACCENT, True)
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
    # TIER FULL RENDERERS
    # ========================================================================
    
    def _render_search_3col(self, surface, step, rect):
        """Render 3-column layout for UCS/A* (Tier Full)"""
        # Explanation box at top
        expl_rect = pygame.Rect(rect.x, rect.y, rect.width, 60)
        pygame.draw.rect(surface, COLOR_CARD, expl_rect, 0, 6)
        pygame.draw.rect(surface, COLOR_OUTLINE, expl_rect, 1, 6)
        
        # Wrap explanation text
        expl_lines = self._wrap_text(step.explanation, rect.width - 20, self.body_font)
        for i, line in enumerate(expl_lines[:3]):  # Max 3 lines
            txt = self.body_font.render(line, True, COLOR_TEXT)
            surface.blit(txt, (expl_rect.x + 10, expl_rect.y + 8 + i * 18))
        
        # 3 columns: Current | Frontier | Explored
        col_y = rect.y + 70
        col_h = rect.height - 140
        col_w = (rect.width - 20) // 3
        
        columns = [
            ("CURRENT", [step.current_node], COLOR_ACCENT),
            ("FRONTIER", getattr(step, 'frontier', [])[:8], COLOR_JADE),
            ("EXPLORED", getattr(step, 'explored', [])[:8], COLOR_TEXT_MUTED)
        ]
        
        for i, (title, items, color) in enumerate(columns):
            col_x = rect.x + i * (col_w + 10)
            col_rect = pygame.Rect(col_x, col_y, col_w - 10, col_h)
            
            # Column header
            pygame.draw.rect(surface, COLOR_CARD, col_rect, 0, 6)
            pygame.draw.rect(surface, COLOR_OUTLINE, col_rect, 1, 6)
            
            hdr = self.small_font.render(title, True, color)
            surface.blit(hdr, (col_rect.centerx - hdr.get_width() // 2, col_rect.y + 8))
            
            pygame.draw.line(surface, COLOR_OUTLINE, 
                           (col_rect.x + 5, col_rect.y + 28),
                           (col_rect.right - 5, col_rect.y + 28))
            
            # Column items
            for idx, item in enumerate(items):
                if idx > 10:  # Limit display
                    break
                y = col_rect.y + 35 + idx * 22
                
                # Format item based on type
                if isinstance(step, UCSStep):
                    cost = item.get('g_cost', 0)
                    txt = self.tiny_font.render(f"cost: {cost}", True, COLOR_TEXT)
                elif isinstance(step, AStarStep):
                    f_val = item.get('f', 0)
                    txt = self.tiny_font.render(f"f: {f_val:.0f}", True, COLOR_TEXT)
                else:
                    txt = self.tiny_font.render(str(item)[:20], True, COLOR_TEXT)
                
                surface.blit(txt, (col_rect.x + 8, y))
        
        # Score breakdown box at bottom
        if isinstance(step, AStarStep):
            self._render_score_breakdown_astar(surface, step, rect)
    
    def _render_alpha_beta(self, surface, step, rect):
        """Render Alpha-Beta tree visualization (Tier Full)"""
        # Explanation
        expl_rect = pygame.Rect(rect.x, rect.y, rect.width, 50)
        pygame.draw.rect(surface, COLOR_CARD, expl_rect, 0, 6)
        pygame.draw.rect(surface, COLOR_OUTLINE, expl_rect, 1, 6)
        
        expl_lines = self._wrap_text(step.explanation, rect.width - 20, self.body_font)
        for i, line in enumerate(expl_lines[:2]):
            txt = self.body_font.render(line, True, COLOR_TEXT)
            surface.blit(txt, (expl_rect.x + 10, expl_rect.y + 8 + i * 18))
        
        # Path display
        path_y = rect.y + 60
        path_rect = pygame.Rect(rect.x, path_y, rect.width, 70)
        pygame.draw.rect(surface, COLOR_CARD, path_rect, 0, 6)
        pygame.draw.rect(surface, COLOR_OUTLINE, path_rect, 1, 6)
        
        path_lbl = self.small_font.render("PATH:", True, COLOR_ACCENT)
        surface.blit(path_lbl, (path_rect.x + 10, path_rect.y + 8))
        
        # Draw path nodes
        path = step.current_path[:5]  # Show max 5 nodes
        for i, node in enumerate(path):
            x = path_rect.x + 60 + i * 60
            y = path_rect.y + 25
            
            # Node circle
            pygame.draw.circle(surface, COLOR_JADE if i == len(path) - 1 else COLOR_TEXT_MUTED, 
                             (x, y), 12)
            pygame.draw.circle(surface, COLOR_OUTLINE, (x, y), 12, 1)
            
            # Depth label
            depth = node.get('depth', i)
            d_txt = self.tiny_font.render(f"d{depth}", True, COLOR_BG)
            surface.blit(d_txt, (x - d_txt.get_width() // 2, y - d_txt.get_height() // 2))
            
            # Arrow between nodes
            if i < len(path) - 1:
                pygame.draw.line(surface, COLOR_OUTLINE, (x + 12, y), (x + 48, y), 2)
                # Arrow head
                pygame.draw.polygon(surface, COLOR_OUTLINE, [
                    (x + 48, y),
                    (x + 43, y - 3),
                    (x + 43, y + 3)
                ])
        
        # Alpha/Beta display
        ab_y = path_y + 80
        ab_rect = pygame.Rect(rect.x, ab_y, rect.width, 50)
        pygame.draw.rect(surface, COLOR_CARD, ab_rect, 0, 6)
        pygame.draw.rect(surface, COLOR_OUTLINE, ab_rect, 1, 6)
        
        alpha_txt = self.header_font.render(f"α = {step.alpha:.0f}", True, COLOR_JADE)
        beta_txt = self.header_font.render(f"β = {step.beta:.0f}", True, COLOR_RED)
        
        surface.blit(alpha_txt, (ab_rect.x + 30, ab_rect.centery - alpha_txt.get_height() // 2))
        surface.blit(beta_txt, (ab_rect.centerx + 30, ab_rect.centery - beta_txt.get_height() // 2))
        
        # Pruning indicator
        if step.is_pruned:
            prune_txt = self.body_font.render(f"✂️ {step.prune_reason}", True, COLOR_RED)
            surface.blit(prune_txt, (rect.x + 10, ab_rect.bottom + 10))
        
        # Siblings display
        sib_y = ab_y + 70 if not step.is_pruned else ab_y + 90
        sib_rect = pygame.Rect(rect.x, sib_y, rect.width, rect.bottom - sib_y - 10)
        
        if sib_rect.height > 50:
            pygame.draw.rect(surface, COLOR_CARD, sib_rect, 0, 6)
            pygame.draw.rect(surface, COLOR_OUTLINE, sib_rect, 1, 6)
            
            sib_lbl = self.small_font.render("Siblings:", True, COLOR_TEXT_MUTED)
            surface.blit(sib_lbl, (sib_rect.x + 10, sib_rect.y + 8))
            
            for i, sib in enumerate(step.siblings_evaluated[:6]):
                y = sib_rect.y + 30 + i * 18
                val = sib.get('value', 0)
                txt = self.tiny_font.render(f"value: {val:.0f}", True, COLOR_TEXT)
                surface.blit(txt, (sib_rect.x + 15, y))
    
    def _render_sa(self, surface, step, rect):
        """Render Simulated Annealing with temperature (Tier Full)"""
        # Temperature display (large and prominent)
        temp_rect = pygame.Rect(rect.x, rect.y, rect.width, 80)
        pygame.draw.rect(surface, COLOR_CARD, temp_rect, 0, 8)
        pygame.draw.rect(surface, COLOR_OUTLINE, temp_rect, 1, 8)
        
        temp_lbl = self.small_font.render("🌡️ NHIỆT ĐỘ", True, COLOR_TEXT_MUTED)
        surface.blit(temp_lbl, (temp_rect.x + 15, temp_rect.y + 10))
        
        temp_val = self.title_font.render(f"T = {step.temperature:.1f}", True, COLOR_ACCENT)
        surface.blit(temp_val, (temp_rect.centerx - temp_val.get_width() // 2, temp_rect.y + 35))
        
        # Current vs Candidate comparison
        comp_y = rect.y + 90
        comp_rect = pygame.Rect(rect.x, comp_y, rect.width, 100)
        pygame.draw.rect(surface, COLOR_CARD, comp_rect, 0, 6)
        pygame.draw.rect(surface, COLOR_OUTLINE, comp_rect, 1, 6)
        
        curr_score = step.current_move.get('score', 0)
        cand_score = step.candidate_move.get('score', 0)
        
        curr_txt = self.body_font.render(f"Current: {curr_score:.0f}", True, COLOR_JADE)
        cand_txt = self.body_font.render(f"Candidate: {cand_score:.0f}", True, 
                                        COLOR_RED if step.delta_e < 0 else COLOR_JADE)
        
        surface.blit(curr_txt, (comp_rect.x + 15, comp_rect.y + 20))
        surface.blit(cand_txt, (comp_rect.x + 15, comp_rect.y + 50))
        
        # Delta E and acceptance probability
        formula_y = comp_y + 110
        formula_rect = pygame.Rect(rect.x, formula_y, rect.width, 120)
        pygame.draw.rect(surface, COLOR_CARD, formula_rect, 0, 6)
        pygame.draw.rect(surface, COLOR_OUTLINE, formula_rect, 1, 6)
        
        delta_txt = self.body_font.render(f"ΔE = {step.delta_e:.0f}", True, 
                                         COLOR_RED if step.delta_e < 0 else COLOR_JADE)
        surface.blit(delta_txt, (formula_rect.x + 15, formula_rect.y + 15))
        
        prob_txt = self.body_font.render(f"P(accept) = e^(ΔE/T) = {step.accept_prob:.3f}", 
                                        True, COLOR_TEXT)
        surface.blit(prob_txt, (formula_rect.x + 15, formula_rect.y + 45))
        
        # Decision
        decision_icon = "✅ CHẤP NHẬN" if step.accepted else "❌ TỪ CHỐI"
        decision_color = COLOR_JADE if step.accepted else COLOR_RED
        decision = self.header_font.render(decision_icon, True, decision_color)
        surface.blit(decision, (formula_rect.x + 15, formula_rect.y + 80))
        
        # Explanation at bottom
        expl_lines = self._wrap_text(step.explanation, rect.width - 20, self.small_font)
        for i, line in enumerate(expl_lines[:2]):
            txt = self.small_font.render(line, True, COLOR_TEXT_MUTED)
            surface.blit(txt, (rect.x + 10, formula_rect.bottom + 10 + i * 16))
    
    # ========================================================================
    # FALLBACK RENDERER
    # ========================================================================
    
    def _render_text_only(self, surface, step, rect):
        """Fallback text-only renderer for all other algorithms"""
        # Main explanation card
        expl_rect = pygame.Rect(rect.x, rect.y, rect.width, rect.height)
        pygame.draw.rect(surface, COLOR_CARD, expl_rect, 0, 8)
        pygame.draw.rect(surface, COLOR_OUTLINE, expl_rect, 1, 8)
        
        # Algorithm name
        algo_lbl = self.header_font.render(step.algorithm, True, COLOR_ACCENT)
        surface.blit(algo_lbl, (expl_rect.x + 15, expl_rect.y + 15))
        
        pygame.draw.line(surface, COLOR_OUTLINE, 
                        (expl_rect.x + 15, expl_rect.y + 45),
                        (expl_rect.right - 15, expl_rect.y + 45))
        
        # Explanation text (wrapped)
        expl_lines = self._wrap_text(step.explanation, rect.width - 30, self.body_font)
        for i, line in enumerate(expl_lines[:15]):  # Max 15 lines
            txt = self.body_font.render(line, True, COLOR_TEXT)
            surface.blit(txt, (expl_rect.x + 15, expl_rect.y + 60 + i * 20))
        
        # Additional info if available
        info_y = expl_rect.y + 60 + min(len(expl_lines), 15) * 20 + 20
        
        # Try to display some key fields
        self._render_generic_fields(surface, step, expl_rect.x + 15, info_y, rect.width - 30)
    
    def _render_generic_fields(self, surface, step, x, y, max_width):
        """Render common fields from step dataclass"""
        fields_to_show = []
        
        # Collect interesting fields
        for key, val in step.__dict__.items():
            if key in ['step_num', 'algorithm', 'explanation', 'chosen_move']:
                continue
            if isinstance(val, (int, float, str, bool)):
                fields_to_show.append((key, val))
        
        # Render fields
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
        break_rect = pygame.Rect(rect.x, break_y, rect.width, 50)
        pygame.draw.rect(surface, COLOR_CARD, break_rect, 0, 6)
        pygame.draw.rect(surface, COLOR_OUTLINE, break_rect, 1, 6)
        
        formula = self.body_font.render(f"f(n) = g(n) + h(n) = {g:.0f} + {h:.0f} = {f:.0f}", 
                                       True, COLOR_ACCENT)
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
