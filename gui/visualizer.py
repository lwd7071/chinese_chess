"""
Visualizer Panel - Step-by-Step Algorithm Visualization

Hiển thị từng bước thực thi thuật toán AI cho mục đích demo và báo cáo.
Thay thế Sidebar khi report_mode=True.

Author: Nhóm 1 - Cờ tướng 6 level
Date: 2026-06-25
"""

import time

import pygame

from ai.step_recorder import (
    AC3Step,
    AlphaBetaStep,
    AndOrStep,
    AStarStep,
    BacktrackStep,
    BaseStep,
    BeamStep,
    BeliefStep,
    BFSStep,
    DFSStep,
    ExpectimaxStep,
    GreedyStep,
    HillClimbStep,
    IDAStarStep,
    MinConflictStep,
    MinimaxStep,
    OnlineStep,
    SAStep,
    UCSStep,
)

# Colors matching sidebar theme
COLOR_BG = (28, 16, 12)  # Dark rosewood
COLOR_CARD = (44, 28, 24)  # Card background
COLOR_ACCENT = (242, 202, 80)  # Gold
COLOR_TEXT = (250, 220, 213)  # Light text
COLOR_TEXT_MUTED = (180, 165, 150)
COLOR_OUTLINE = (77, 70, 53)
COLOR_JADE = (89, 222, 155)
COLOR_RED = (231, 76, 60)
COLOR_BLUE = (52, 152, 219)

# Piece name mapping for display
PIECE_NAME_VI = {
    "general": "Tướng",
    "advisor": "Sĩ",
    "elephant": "Tượng",
    "horse": "Mã",
    "rook": "Xe",
    "cannon": "Pháo",
    "pawn": "Tốt",
    "Tướng": "Tướng",
    "Sĩ": "Sĩ",
    "Tượng": "Tượng",
    "Mã": "Mã",
    "Xe": "Xe",
    "Pháo": "Pháo",
    "Tốt": "Tốt",
}


class StepController:
    """Controller for step navigation (prev/next/auto)"""

    def __init__(self):
        self.mode = "manual"  # "manual" or "auto"
        self.auto_delay = 1.5  # Seconds between auto steps
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


class EmojiSafeFont:
    """Wrapper for pygame.font.Font that dynamically renders custom vector badges/icons
    instead of displaying text-based emojis or bracket characters (like [OK], [X])."""

    CURRENT_BOARD = None
    CURRENT_TURN = None

    TAG_MAP = {
        "✅": "check",
        "[OK]": "check",
        "❌": "cross",
        "[X]": "cross",
        "⚠️": "warn",
        "[!]": "warn",
        "✂️": "cut",
        "[CUT]": "cut",
        "🔙": "back",
        "[BACK]": "back",
        "⭐": "star",
        "★": "star",
        "[*]": "star",
    }

    def __init__(self, font_obj):
        self._font = font_obj

    def tokenize(self, text):
        if not isinstance(text, str):
            return [("text", text)]

        tokens = []
        current_pos = 0
        while current_pos < len(text):
            found_tag = None
            found_idx = -1
            # Find the earliest tag occurrence
            for tag in self.TAG_MAP:
                idx = text.find(tag, current_pos)
                if idx != -1:
                    if found_idx == -1 or idx < found_idx:
                        found_idx = idx
                        found_tag = tag

            if found_idx == -1:
                # No more tags
                tokens.append(("text", text[current_pos:]))
                break
            else:
                # Add preceding text token
                if found_idx > current_pos:
                    tokens.append(("text", text[current_pos:found_idx]))
                # Add tag token
                tokens.append((self.TAG_MAP[found_tag], ""))
                current_pos = found_idx + len(found_tag)
        return tokens

    @staticmethod
    def clean_coordinates(text):
        if not isinstance(text, str):
            return text
        import re

        # Track the color of the first resolved piece in this text line/move
        detected_color = [None]

        def repl(match):
            try:
                row = int(match.group(1))
                col = int(match.group(2))
                if 0 <= row <= 9 and 0 <= col <= 8:
                    col_labels = "ABCDEFGHI"
                    col_char = col_labels[8 - col]
                    row_char = str(row)
                    return f"{col_char}{row_char}"
            except Exception:
                pass
            return match.group(0)

        return re.sub(r'\((\d),\s*(\d)\)', repl, text)

    def size(self, text):
        if isinstance(text, str):
            text = self.clean_coordinates(text)

        if not isinstance(text, str) or not text:
            return self._font.size(text)

        tokens = self.tokenize(text)
        if len(tokens) == 1 and tokens[0][0] == "text":
            return self._font.size(text)

        total_w = 0
        max_h = self._font.get_height()

        for t_type, content in tokens:
            if t_type == "text":
                w, h = self._font.size(content)
                total_w += w
                max_h = max(max_h, h)
            else:
                # Icon size is 12x12, with 4px right spacing
                total_w += 12 + 4
                max_h = max(max_h, 12)

        # Remove trailing spacing
        if total_w > 0:
            total_w -= 4

        return total_w, max_h

    def get_height(self):
        return self._font.get_height()

    def render(self, text, antialias, color, background=None):
        if isinstance(text, str):
            text = self.clean_coordinates(text)

        if not isinstance(text, str) or not text:
            return self._font.render(text, antialias, color, background)

        tokens = self.tokenize(text)
        # If no icons found, render normally
        if len(tokens) == 1 and tokens[0][0] == "text":
            return self._font.render(text, antialias, color, background)

        # Compute combined surface size
        width, height = self.size(text)

        # Create transparent surface
        surf = pygame.Surface((width, height), pygame.SRCALPHA)

        x_offset = 0
        icon_h = 12
        icon_y = (height - icon_h) // 2

        for t_type, content in tokens:
            if t_type == "text":
                text_surf = self._font.render(content, antialias, color, background)
                text_y = (height - text_surf.get_height()) // 2
                surf.blit(text_surf, (x_offset, text_y))
                x_offset += text_surf.get_width()
            else:
                # Draw the custom vector icon at x_offset
                if t_type == "check":
                    # Green circular checkmark badge
                    pygame.draw.circle(surf, (46, 204, 113), (x_offset + 6, icon_y + 6), 5)
                    pygame.draw.line(surf, (255, 255, 255), (x_offset + 3, icon_y + 6), (x_offset + 5, icon_y + 8), 2)
                    pygame.draw.line(surf, (255, 255, 255), (x_offset + 5, icon_y + 8), (x_offset + 9, icon_y + 4), 2)
                elif t_type == "cross":
                    # Red circular cross badge
                    pygame.draw.circle(surf, (231, 76, 60), (x_offset + 6, icon_y + 6), 5)
                    pygame.draw.line(surf, (255, 255, 255), (x_offset + 4, icon_y + 4), (x_offset + 8, icon_y + 8), 2)
                    pygame.draw.line(surf, (255, 255, 255), (x_offset + 4, icon_y + 8), (x_offset + 8, icon_y + 4), 2)
                elif t_type == "warn":
                    # Orange warning triangle badge
                    pygame.draw.polygon(
                        surf,
                        (241, 196, 15),
                        [
                            (x_offset + 6, icon_y + 1),
                            (x_offset + 1, icon_y + 11),
                            (x_offset + 11, icon_y + 11),
                        ],
                    )
                    # Exclamation dot and line (black for contrast)
                    pygame.draw.line(surf, (0, 0, 0), (x_offset + 6, icon_y + 4), (x_offset + 6, icon_y + 7), 2)
                    pygame.draw.rect(surf, (0, 0, 0), (x_offset + 5, icon_y + 9, 2, 2))
                elif t_type == "cut":
                    # Scissor symbol in gray/silver
                    pygame.draw.line(surf, (149, 165, 166), (x_offset + 2, icon_y + 2), (x_offset + 10, icon_y + 10), 2)
                    pygame.draw.line(surf, (149, 165, 166), (x_offset + 2, icon_y + 10), (x_offset + 10, icon_y + 2), 2)
                    pygame.draw.circle(surf, (149, 165, 166), (x_offset + 2, icon_y + 2), 2)
                    pygame.draw.circle(surf, (149, 165, 166), (x_offset + 2, icon_y + 10), 2)
                elif t_type == "back":
                    # Red back arrow
                    pygame.draw.line(surf, (231, 76, 60), (x_offset + 2, icon_y + 6), (x_offset + 10, icon_y + 6), 2)
                    pygame.draw.line(surf, (231, 76, 60), (x_offset + 2, icon_y + 6), (x_offset + 5, icon_y + 3), 2)
                    pygame.draw.line(surf, (231, 76, 60), (x_offset + 2, icon_y + 6), (x_offset + 5, icon_y + 9), 2)
                elif t_type == "star":
                    # Gold star symbol
                    pygame.draw.polygon(
                        surf,
                        (242, 202, 80),
                        [
                            (x_offset + 6, icon_y + 1),
                            (x_offset + 8, icon_y + 4),
                            (x_offset + 11, icon_y + 4),
                            (x_offset + 8, icon_y + 6),
                            (x_offset + 9, icon_y + 10),
                            (x_offset + 6, icon_y + 8),
                            (x_offset + 3, icon_y + 10),
                            (x_offset + 4, icon_y + 6),
                            (x_offset + 1, icon_y + 4),
                            (x_offset + 4, icon_y + 4),
                        ],
                    )
                x_offset += 12 + 4

        return surf

    def __getattr__(self, name):
        return getattr(self._font, name)


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

        # Load fonts with Vietnamese support fallback chain
        import os

        def _load_font(size, bold=False):
            """Thử load font theo thứ tự ưu tiên, hỗ trợ tiếng Việt."""
            # 1. Thử file TTF bundled
            ttf_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "assets", "fonts", "Roboto-Regular.ttf",
            )
            if os.path.exists(ttf_path):
                try:
                    f = pygame.font.Font(ttf_path, size)
                    if bold:
                        f.set_bold(True)
                    return f
                except Exception:
                    pass
            # 2. Thử custom font_name nếu là file .ttf
            if font_name and font_name.endswith(".ttf") and os.path.exists(font_name):
                try:
                    f = pygame.font.Font(font_name, size)
                    if bold:
                        f.set_bold(True)
                    return f
                except Exception:
                    pass
            # 3. SysFont fallback — Arial và Segoe UI hỗ trợ tiếng Việt trên Windows
            for sys_name in ["Arial", "segoeui", "Tahoma"]:
                try:
                    f = pygame.font.SysFont(sys_name, size, bold=bold)
                    return f
                except Exception:
                    pass
            # 4. Default pygame font (cuối cùng)
            return pygame.font.Font(None, size)

        self.title_font = EmojiSafeFont(_load_font(20, bold=True))
        self.header_font = EmojiSafeFont(_load_font(16, bold=True))
        self.body_font = EmojiSafeFont(_load_font(14))
        self.small_font = EmojiSafeFont(_load_font(12))
        self.tiny_font = EmojiSafeFont(_load_font(10))

        # Mono font riêng — ưu tiên Consolas (luôn có trên Windows)
        try:
            self.mono_font = EmojiSafeFont(pygame.font.SysFont("Consolas", 13))
        except Exception:
            self.mono_font = EmojiSafeFont(_load_font(13))

        # Navigation buttons
        btn_y = y + height - 60
        btn_w = 80
        center_x = x + width // 2
        start_x = center_x - 172

        self.btn_prev = pygame.Rect(start_x, btn_y, btn_w, 36)
        self.btn_next = pygame.Rect(start_x + 88, btn_y, btn_w, 36)
        self.btn_auto = pygame.Rect(start_x + 176, btn_y, btn_w, 36)
        self.btn_skip = pygame.Rect(start_x + 264, btn_y, btn_w, 36)

        # Speed slider
        self.slider_rect = pygame.Rect(start_x, btn_y - 45, 344, 8)
        self.is_dragging_slider = False

        # Scroll state for long lists
        self.scroll_offset = 0
        self.max_scroll = 0
        self.current_board = None

    def update_layout(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        btn_y = self.y + self.height - 60
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

        self.slider_rect.x = start_x
        self.slider_rect.y = btn_y - 45

    def handle_event(self, event, controller, recorder):
        """Handle mouse clicks, dragging, and scroll events"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check slider click
            slider_click_area = self.slider_rect.inflate(10, 20)
            if slider_click_area.collidepoint(event.pos):
                self.is_dragging_slider = True
                mx = event.pos[0]
                pct = (mx - self.slider_rect.x) / self.slider_rect.width
                pct = max(0.0, min(1.0, pct))
                controller.auto_delay = 3.0 - pct * (3.0 - 0.1)
                return "slider"

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

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_dragging_slider = False

        elif event.type == pygame.MOUSEMOTION:
            if getattr(self, "is_dragging_slider", False):
                if not pygame.mouse.get_pressed()[0]:
                    self.is_dragging_slider = False
                else:
                    mx = event.pos[0]
                    pct = (mx - self.slider_rect.x) / self.slider_rect.width
                    pct = max(0.0, min(1.0, pct))
                    controller.auto_delay = 3.0 - pct * (3.0 - 0.1)
                    return "slider"

        elif event.type == pygame.MOUSEWHEEL:
            # Scroll content if needed
            self.scroll_offset = max(
                0, min(self.max_scroll, self.scroll_offset - event.y * 20)
            )

        return None

    # ========================================================================
    # FORMAT HELPERS
    # ========================================================================

    def _format_move(self, move_data):
        """Alias for compatibility"""
        return self._format_move_full(move_data)

    # Column labels for coordinate display
    COL_LABELS = "ABCDEFGHI"

    def _pos_to_label(self, pos):
        """Convert (row, col) → 'A0'..'I9' using current board context"""
        color = "red"
        if self.current_board:
            piece = self.current_board.get_piece(pos)
            if piece:
                color = piece.color
            else:
                color = self.current_board.turn
        return self._pos_to_label_with_color(pos, color)

    def _pos_to_label_with_color(self, pos, color):
        row, col = pos
        if 0 <= col < len(self.COL_LABELS) and 0 <= row <= 9:
            col_char = self.COL_LABELS[8 - col]   # A ở phải, I ở trái
            row_char = str(row)                   # 0 ở trên, 9 ở dưới
            return f"{col_char}{row_char}"
        return f"({row},{col})"

    def _format_move_full(self, move_data):
        """
        Format move data thành chuỗi dễ đọc với label tọa độ.
        Input: tuple ((r1,c1),(r2,c2)) hoặc dict {"move":..., "score":..., "piece":...}
        Output: "Mã B2→C4 [280]"
        """
        if move_data is None:
            return "—"

        piece_name = ""
        score_str = ""
        move_tuple = None

        if isinstance(move_data, dict):
            move_tuple = move_data.get("move")
            piece = (
                move_data.get("piece")
                or move_data.get("piece_name")
                or move_data.get("piece_captured")
            )
            if piece and piece != "—":
                vi_name = PIECE_NAME_VI.get(piece, piece)
                piece_name = vi_name + " "
            score = move_data.get("score")
            if score is not None:
                try:
                    score_str = f" [{score:.0f}]"
                except (TypeError, ValueError):
                    score_str = f" [{score}]"
        elif isinstance(move_data, tuple) and len(move_data) == 2:
            if isinstance(move_data[0], tuple):
                move_tuple = move_data

        if move_tuple and isinstance(move_tuple, tuple) and len(move_tuple) == 2:
            if isinstance(move_tuple[0], tuple):
                # Determine piece color contextually
                color = "red"
                if self.current_board:
                    piece = self.current_board.get_piece(move_tuple[0])
                    if piece:
                        color = piece.color
                    else:
                        color = self.current_board.turn

                from_label = self._pos_to_label_with_color(move_tuple[0], color)
                to_label = self._pos_to_label_with_color(move_tuple[1], color)
                return f"{piece_name}{from_label}→{to_label}{score_str}"
            else:
                return f"{piece_name}{move_tuple}{score_str}"

        return str(move_data)[:30]

    def _get_step_subtitle(self, step, total):
        """Trả về subtitle giải thích ý nghĩa tổng số bước."""
        if isinstance(step, (BFSStep, DFSStep)):
            return f"({total} nodes đã mở rộng)"
        elif isinstance(step, (UCSStep, AStarStep)):
            return f"({total} nước đi đang xét)"
        elif isinstance(step, IDAStarStep):
            return f"({total} nodes đã duyệt)"
        elif isinstance(step, (GreedyStep, HillClimbStep)):
            return f"({total} neighbors đã đánh giá)"
        elif isinstance(step, SAStep):
            return f"({total} vòng lặp nhiệt độ)"
        elif isinstance(step, BeamStep):
            return "(2 giai đoạn: chọn beam + worst-case)"
        elif isinstance(step, (OnlineStep, AndOrStep, BeliefStep)):
            return f"({total} bước phân tích)"
        elif isinstance(step, (BacktrackStep, MinConflictStep, AC3Step)):
            return f"({total} bước phân tích CSP)"
        elif isinstance(step, (MinimaxStep, AlphaBetaStep)):
            return f"({total} nodes cây game đã duyệt)"
        elif isinstance(step, ExpectimaxStep):
            return f"({total} nodes đã duyệt)"
        return ""

    # ========================================================================
    # MAIN DRAW
    # ========================================================================

    def draw(self, surface, step: BaseStep, controller, recorder, is_computing=False, board=None):
        """Main render method"""
        self.current_board = board
        EmojiSafeFont.CURRENT_BOARD = board
        EmojiSafeFont.CURRENT_TURN = board.turn if board else None

        # Background
        bg_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, COLOR_BG, bg_rect)
        pygame.draw.line(
            surface, COLOR_OUTLINE, (self.x, self.y), (self.x, self.y + self.height), 2
        )

        if step is None:
            self._render_empty(surface)
            if is_computing:
                text = self.title_font.render(
                    "AI Đang Tính Toán...", True, (255, 50, 50)
                )
                surface.blit(
                    text,
                    (
                        self.x + self.width // 2 - text.get_width() // 2,
                        self.y + self.height // 2 + 50,
                    ),
                )
            return

        # Header with step counter
        self._render_header(surface, step, recorder)

        # Body - delegate to specific renderer
        content_y = self.y + 80
        content_rect = pygame.Rect(
            self.x + 15, content_y, self.width - 30, self.height - 210
        )

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
            self._render_online_andor_belief(surface, step, content_rect)
        elif isinstance(step, (BacktrackStep, MinConflictStep, AC3Step)):
            self._render_csp(surface, step, content_rect)
        elif isinstance(step, AlphaBetaStep):
            self._render_alpha_beta(surface, step, content_rect)
        elif isinstance(step, (MinimaxStep, ExpectimaxStep)):
            self._render_minimax_expectimax(surface, step, content_rect)
        else:
            self._render_text_only(surface, step, content_rect)

        # Draw speed slider
        pygame.draw.rect(surface, COLOR_OUTLINE, self.slider_rect, 0, 4)

        # Calculate handle position: Delay 3.0s (slow) -> 0.1s (fast)
        delay_range = 3.0 - 0.1
        pct = (3.0 - controller.auto_delay) / delay_range
        pct = max(0.0, min(1.0, pct))

        handle_x = self.slider_rect.x + int(pct * self.slider_rect.width)
        handle_y = self.slider_rect.centery

        # Draw active track
        active_rect = pygame.Rect(self.slider_rect.x, self.slider_rect.y, handle_x - self.slider_rect.x, self.slider_rect.height)
        pygame.draw.rect(surface, COLOR_ACCENT, active_rect, 0, 4)

        # Draw handle circle
        pygame.draw.circle(surface, (255, 255, 255), (handle_x, handle_y), 8)
        pygame.draw.circle(surface, COLOR_ACCENT, (handle_x, handle_y), 8, 2)

        # Draw label
        label_txt = self.tiny_font.render(f"Tốc độ chạy tự động: {controller.auto_delay:.1f}s/bước", True, COLOR_TEXT)
        surface.blit(label_txt, (self.slider_rect.x, self.slider_rect.y - 18))

        # Navigation footer
        self._render_footer(surface, controller, recorder)

        if is_computing:
            text = self.title_font.render("AI ĐANG TÍNH TOÁN...", True, (255, 50, 50))
            overlay = pygame.Surface((self.width, 40))
            overlay.set_alpha(200)
            overlay.fill((30, 30, 40))
            surface.blit(overlay, (self.x, self.y + 40))
            surface.blit(
                text, (self.x + self.width // 2 - text.get_width() // 2, self.y + 48)
            )

    def _render_empty(self, surface):
        """Shown when no steps available"""
        msg = self.body_font.render(
            "Chưa có dữ liệu visualization", True, COLOR_TEXT_MUTED
        )
        surface.blit(
            msg,
            (
                self.x + self.width // 2 - msg.get_width() // 2,
                self.y + self.height // 2,
            ),
        )

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
            True,
            COLOR_TEXT,
        )
        surface.blit(
            step_txt,
            (header_rect.right - step_txt.get_width() - 15, header_rect.y + 12),
        )

        # Subtitle giải thích
        total = recorder.total_steps()
        subtitle = self._get_step_subtitle(step, total)
        if subtitle:
            sub_txt = self.tiny_font.render(subtitle, True, COLOR_TEXT_MUTED)
            surface.blit(
                sub_txt,
                (header_rect.right - sub_txt.get_width() - 15, header_rect.y + 32),
            )

    def _render_footer(self, surface, controller, recorder):
        """Render navigation buttons with premium styling and vector icons"""
        mouse_pos = pygame.mouse.get_pos()

        # Draw buttons
        buttons = [
            # (rect, label, icon_type, color, enabled, icon_left)
            (
                self.btn_prev,
                "PREV",
                "prev",
                COLOR_BLUE,
                recorder.current_index > 0,
                True,
            ),
            (
                self.btn_next,
                "NEXT" if recorder.current_index < recorder.total_steps() - 1 else "FINISH",
                "next",
                COLOR_BLUE,
                True,
                False,
            ),
            (
                self.btn_auto,
                "AUTO" if controller.mode == "manual" else "PAUSE",
                "auto" if controller.mode == "manual" else "pause",
                COLOR_JADE if controller.mode == "auto" else COLOR_ACCENT,
                True,
                True,
            ),
            (
                self.btn_skip,
                "SKIP",
                "skip",
                COLOR_RED,
                True,
                False,
            ),
        ]

        for rect, label, icon_type, color, enabled, icon_left in buttons:
            is_hover = rect.collidepoint(mouse_pos) and enabled
            is_pressed = is_hover and pygame.mouse.get_pressed()[0]

            # Draw shadow/glow first
            if enabled:
                if is_hover:
                    # Glowing aura effect on hover
                    glow_rect = rect.inflate(4, 4)
                    glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                    glow_color = (*color, 35) if not is_pressed else (*color, 20)
                    pygame.draw.rect(glow_surf, glow_color, (0, 0, glow_rect.width, glow_rect.height), 0, 8)
                    surface.blit(glow_surf, glow_rect.topleft)
                else:
                    # Soft drop shadow for 3D depth
                    shadow_rect = rect.move(0, 2)
                    shadow_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                    pygame.draw.rect(shadow_surf, (0, 0, 0, 50), (0, 0, rect.width, rect.height), 0, 6)
                    surface.blit(shadow_surf, shadow_rect.topleft)

            # Button active state offset
            draw_rect = rect.move(0, 1) if is_pressed else rect

            # Button background
            btn_bg_color = color if enabled else (44, 32, 28)
            if enabled and is_hover:
                btn_bg_color = self._brighten(color) if not is_pressed else tuple(max(0, c - 20) for c in color)

            pygame.draw.rect(
                surface,
                btn_bg_color,
                draw_rect,
                0,
                6,
            )

            # Glassmorphic top reflection overlay
            if enabled:
                highlight_rect = pygame.Rect(draw_rect.x + 1, draw_rect.y + 1, draw_rect.width - 2, draw_rect.height // 2)
                highlight_surf = pygame.Surface((highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)
                for y_offset in range(highlight_rect.height):
                    alpha = int(45 * (1.0 - y_offset / highlight_rect.height))
                    highlight_surf.fill((255, 255, 255, alpha), (0, y_offset, highlight_rect.width, 1))
                surface.blit(highlight_surf, (highlight_rect.x, highlight_rect.y))

            # Border drawing
            border_color = COLOR_OUTLINE
            border_width = 1
            if enabled:
                if is_hover:
                    border_color = (255, 255, 255)  # White border highlight on hover
                    border_width = 2
                else:
                    border_color = tuple(min(255, c + 40) for c in color)  # Harmonious color border

            pygame.draw.rect(
                surface,
                border_color,
                draw_rect,
                border_width,
                6,
            )

            # Button text and vector icon layout
            txt_color = COLOR_TEXT if enabled else COLOR_TEXT_MUTED
            txt = self.small_font.render(label, True, txt_color)

            icon_w = 8
            if icon_type == "auto":
                icon_w = 12
            elif icon_type == "skip":
                icon_w = 10

            icon_h = 10
            spacing = 5
            total_w = icon_w + spacing + txt.get_width()

            start_x = draw_rect.centerx - total_w // 2

            if icon_left:
                icon_x = start_x
                text_x = start_x + icon_w + spacing
            else:
                text_x = start_x
                icon_x = start_x + txt.get_width() + spacing

            text_y = draw_rect.centery - txt.get_height() // 2
            icon_y = draw_rect.centery - icon_h // 2

            if is_pressed:
                text_y += 1
                icon_y += 1

            # Draw text
            surface.blit(txt, (text_x, text_y))

            # Draw vector icon
            icon_color = txt_color
            if icon_type == "prev":
                pygame.draw.polygon(
                    surface,
                    icon_color,
                    [
                        (icon_x + icon_w, icon_y),
                        (icon_x, icon_y + icon_h // 2),
                        (icon_x + icon_w, icon_y + icon_h),
                    ],
                )
            elif icon_type == "next":
                pygame.draw.polygon(
                    surface,
                    icon_color,
                    [
                        (icon_x, icon_y),
                        (icon_x + icon_w, icon_y + icon_h // 2),
                        (icon_x, icon_y + icon_h),
                    ],
                )
            elif icon_type == "auto":
                pygame.draw.polygon(
                    surface,
                    icon_color,
                    [
                        (icon_x, icon_y),
                        (icon_x + 6, icon_y + icon_h // 2),
                        (icon_x, icon_y + icon_h),
                    ],
                )
                pygame.draw.polygon(
                    surface,
                    icon_color,
                    [
                        (icon_x + 6, icon_y),
                        (icon_x + 12, icon_y + icon_h // 2),
                        (icon_x + 6, icon_y + icon_h),
                    ],
                )
            elif icon_type == "pause":
                pygame.draw.rect(surface, icon_color, (icon_x, icon_y, 2, icon_h))
                pygame.draw.rect(surface, icon_color, (icon_x + 5, icon_y, 2, icon_h))
            elif icon_type == "skip":
                pygame.draw.polygon(
                    surface,
                    icon_color,
                    [
                        (icon_x, icon_y),
                        (icon_x + 6, icon_y + icon_h // 2),
                        (icon_x, icon_y + icon_h),
                    ],
                )
                pygame.draw.rect(surface, icon_color, (icon_x + 8, icon_y, 2, icon_h))

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

    def _draw_item_list(
        self, surface, items, x, y, max_items, formatter=None, best_item=None
    ):
        """Draw a vertical list of items with optional best marker. Returns bottom y."""
        for i, item in enumerate(items[:max_items]):
            if y + i * 18 > self.y + self.height - 100:
                break
            item_y = y + i * 18

            label = formatter(item) if formatter else self._format_move_full(item)
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

        if isinstance(step, BFSStep):
            columns = [
                ("CURRENT NODE", [step.current_node] if step.current_node else [], COLOR_ACCENT),
                ("QUEUE (FIFO)", step.queue[:8], COLOR_JADE),
                ("EVALUATED", (getattr(step, "evaluated", None) or step.explored)[-8:], COLOR_TEXT_MUTED),
            ]
        else:
            columns = [
                ("CURRENT PATH", [step.current_node] if step.current_node else [], COLOR_ACCENT),
                ("STACK", step.stack[:8], COLOR_JADE),
                ("BACKTRACK LOG", (getattr(step, "backtrack_log", None) or step.explored)[-8:], COLOR_TEXT_MUTED),
            ]

        for i, (title, items, color) in enumerate(columns):
            col_x = rect.x + i * (col_w + 10)
            col_rect = self._draw_card(surface, col_x, col_y, col_w - 10, col_h)

            hdr = self.small_font.render(title, True, color)
            surface.blit(hdr, (col_rect.centerx - hdr.get_width() // 2, col_rect.y + 8))
            pygame.draw.line(
                surface,
                COLOR_OUTLINE,
                (col_rect.x + 5, col_rect.y + 28),
                (col_rect.right - 5, col_rect.y + 28),
            )

            for idx, item in enumerate(items):
                if idx > 8:
                    break
                iy = col_rect.y + 35 + idx * 20
                if isinstance(item, dict):
                    node_id = item.get("id", "")
                    depth = item.get("depth", "")
                    move = item.get("move")

                    # Extract moving piece name and map it to friendly Vietnamese name
                    piece = item.get("piece", "")
                    piece_prefix = ""
                    if piece:
                        vi_name = PIECE_NAME_VI.get(piece, piece)
                        piece_prefix = vi_name + " "

                    move_str = self._format_move_full(move) if move else ""
                    if move_str and move_str != "—":
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
                    label = str(item)

                # Prevent text from overflowing the column
                max_text_w = col_w - 12
                if self.tiny_font.size(label)[0] > max_text_w:
                    for i in range(len(label) - 1, 0, -1):
                        truncated = label[:i] + ".."
                        if self.tiny_font.size(truncated)[0] <= max_text_w:
                            label = truncated
                            break
                    else:
                        label = ".."
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
            ("CURRENT MOVE", [step.current_node] if step.current_node else [], COLOR_ACCENT),
            ("FRONTIER (PQ)", getattr(step, "frontier", [])[:8], COLOR_JADE),
            ("EVALUATED", (getattr(step, "evaluated", None) or getattr(step, "explored", []))[-8:], COLOR_TEXT_MUTED),
        ]

        for i, (title, items, color) in enumerate(columns):
            col_x = rect.x + i * (col_w + 10)
            col_rect = self._draw_card(surface, col_x, col_y, col_w - 10, col_h)

            hdr = self.small_font.render(title, True, color)
            surface.blit(hdr, (col_rect.centerx - hdr.get_width() // 2, col_rect.y + 8))
            pygame.draw.line(
                surface,
                COLOR_OUTLINE,
                (col_rect.x + 5, col_rect.y + 28),
                (col_rect.right - 5, col_rect.y + 28),
            )

            for idx, item in enumerate(items):
                if idx > 8:
                    break
                iy = col_rect.y + 35 + idx * 20

                if isinstance(step, UCSStep):
                    move_str = self._format_move_full(item)
                    cost = item.get("g_cost", 0) if isinstance(item, dict) else 0
                    label = f"{move_str} cost:{cost}"
                elif isinstance(step, AStarStep):
                    move_str = self._format_move_full(item)
                    f_val = item.get("f", 0) if isinstance(item, dict) else 0
                    try:
                        label = f"{move_str} f:{f_val:.0f}"
                    except (TypeError, ValueError):
                        label = f"{move_str} f:{f_val}"
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
        iter_txt = self.header_font.render(
            f"Iteration: {step.iteration}", True, COLOR_ACCENT
        )
        thresh_txt = self.header_font.render(
            f"Threshold: {step.threshold:.0f}", True, COLOR_JADE
        )
        surface.blit(iter_txt, (info_rect.x + 15, info_rect.y + 15))
        surface.blit(thresh_txt, (info_rect.centerx + 15, info_rect.y + 15))

        # Current node info
        if step.current_node:
            node_rect = self._draw_card(
                surface, rect.x, info_rect.bottom + 10, rect.width, 60
            )
            move_str = self._format_move_full(step.current_node)
            g = step.current_node.get("g", 0)
            h = step.current_node.get("h", 0)
            f = step.current_node.get("f", 0)

            node_txt = self.body_font.render(f"Node: {move_str}", True, COLOR_TEXT)
            surface.blit(node_txt, (node_rect.x + 15, node_rect.y + 10))

            try:
                vals_txt = self.body_font.render(
                    f"g={g:.0f}  h={h:.0f}  f={f:.0f}", True, COLOR_TEXT_MUTED
                )
            except (TypeError, ValueError):
                vals_txt = self.body_font.render(
                    f"g={g}  h={h}  f={f}", True, COLOR_TEXT_MUTED
                )
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
                    True,
                    COLOR_RED,
                )
            except (TypeError, ValueError):
                cut_txt = self.body_font.render("✂️ CUTOFF", True, COLOR_RED)
            surface.blit(cut_txt, (cutoff_rect.x + 15, cutoff_rect.y + 10))
        elif not step.is_cutoff and step.current_node:
            pass_rect = self._draw_card(surface, rect.x, cutoff_y, rect.width, 40)
            pass_txt = self.body_font.render(
                "✅ f ≤ threshold → tiếp tục", True, COLOR_JADE
            )
            surface.blit(pass_txt, (pass_rect.x + 15, pass_rect.y + 10))

    # ========================================================================
    # RENDERER: Greedy / Hill Climbing (Nhóm B)
    # ========================================================================

    def _render_candidates_list(self, surface, step, rect):
        """Render candidate/neighbor list in 3 columns for Greedy and Hill Climbing"""
        bottom = self._draw_explanation_box(surface, step, rect)

        col_y = bottom + 10
        col_h = rect.bottom - col_y - (40 if (isinstance(step, HillClimbStep) and step.is_plateau) else 10)
        col_w = (rect.width - 20) // 3

        if isinstance(step, HillClimbStep):
            c1_title = "CURRENT STATE"
            c2_title = "NEIGHBORS"
            c3_title = "EVALUATED"
            c1_items = [step.current_move] if step.current_move else []
            c2_items = step.neighbors[:8]
            c3_items = getattr(step, "evaluated", [])[-8:]
        else:  # GreedyStep
            c1_title = "CURRENT MOVE"
            c2_title = "CANDIDATES"
            c3_title = "EVALUATED"
            c1_items = [step.current_node] if step.current_node else []
            c2_items = step.candidates[:8]
            c3_items = getattr(step, "evaluated", [])[-8:]

        columns = [
            (c1_title, c1_items, COLOR_ACCENT),
            (c2_title, c2_items, COLOR_JADE),
            (c3_title, c3_items, COLOR_TEXT_MUTED),
        ]

        for i, (title, items, color) in enumerate(columns):
            col_x = rect.x + i * (col_w + 10)
            col_rect = self._draw_card(surface, col_x, col_y, col_w - 10, col_h)

            hdr = self.small_font.render(title, True, color)
            surface.blit(hdr, (col_rect.centerx - hdr.get_width() // 2, col_rect.y + 8))
            pygame.draw.line(
                surface,
                COLOR_OUTLINE,
                (col_rect.x + 5, col_rect.y + 28),
                (col_rect.right - 5, col_rect.y + 28),
            )

            for idx, item in enumerate(items):
                if idx > 8:
                    break
                iy = col_rect.y + 35 + idx * 20

                if isinstance(step, HillClimbStep):
                    move_str = self._format_move_full(item)
                    score = item.get("score", 0) if isinstance(item, dict) else 0
                    label = f"{move_str} s={score:.0f}"
                else:  # GreedyStep
                    move_str = self._format_move_full(item)
                    h_val = item.get("h", 0) if isinstance(item, dict) else 0
                    label = f"{move_str} h={h_val}"

                txt = self.tiny_font.render(label, True, COLOR_TEXT)
                surface.blit(txt, (col_rect.x + 6, iy))

        # Plateau warning for Hill Climbing
        if isinstance(step, HillClimbStep) and step.is_plateau:
            plat_y = rect.bottom - 30
            plat_txt = self.small_font.render(
                "⚠️ PLATEAU: best ≤ current", True, COLOR_RED
            )
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

        temp_val = self.title_font.render(
            f"T = {step.temperature:.1f}", True, COLOR_ACCENT
        )
        surface.blit(
            temp_val, (temp_rect.centerx - temp_val.get_width() // 2, temp_rect.y + 32)
        )

        # Current vs Candidate comparison — now with move info
        comp_y = rect.y + 80
        comp_rect = self._draw_card(surface, rect.x, comp_y, rect.width, 80)

        curr_str = self._format_move_full(step.current_move)
        cand_str = self._format_move_full(step.candidate_move)

        curr_txt = self.body_font.render(f"Current: {curr_str}", True, COLOR_JADE)
        cand_txt = self.body_font.render(
            f"Candidate: {cand_str}",
            True,
            COLOR_RED if step.delta_e < 0 else COLOR_JADE,
        )

        surface.blit(curr_txt, (comp_rect.x + 15, comp_rect.y + 15))
        surface.blit(cand_txt, (comp_rect.x + 15, comp_rect.y + 45))

        # Delta E and acceptance probability
        formula_y = comp_y + 90
        formula_rect = self._draw_card(surface, rect.x, formula_y, rect.width, 110)

        delta_txt = self.body_font.render(
            f"ΔE = {step.delta_e:.0f}",
            True,
            COLOR_RED if step.delta_e < 0 else COLOR_JADE,
        )
        surface.blit(delta_txt, (formula_rect.x + 15, formula_rect.y + 12))

        prob_txt = self.body_font.render(
            f"P(accept) = e^(ΔE/T) = {step.accept_prob:.3f}", True, COLOR_TEXT
        )
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
        pygame.draw.line(
            surface,
            COLOR_OUTLINE,
            (kept_rect.x + 5, kept_rect.y + 28),
            (kept_rect.right - 5, kept_rect.y + 28),
        )
        for i, item in enumerate(step.kept_beams[:6]):
            iy = kept_rect.y + 35 + i * 18
            if iy > kept_rect.bottom - 15:
                break
            txt = self.tiny_font.render(
                f"✅ {self._format_move_full(item)}", True, COLOR_JADE
            )
            surface.blit(txt, (kept_rect.x + 6, iy))

        # Eliminated column
        elim_rect = self._draw_card(
            surface, rect.x + col_w + 5, col_y, col_w - 5, col_h
        )
        elim_lbl = self.small_font.render("ELIMINATED", True, COLOR_RED)
        surface.blit(elim_lbl, (elim_rect.x + 8, elim_rect.y + 8))
        pygame.draw.line(
            surface,
            COLOR_OUTLINE,
            (elim_rect.x + 5, elim_rect.y + 28),
            (elim_rect.right - 5, elim_rect.y + 28),
        )
        for i, item in enumerate(step.eliminated[:6]):
            iy = elim_rect.y + 35 + i * 18
            if iy > elim_rect.bottom - 15:
                break
            txt = self.tiny_font.render(
                f"❌ {self._format_move_full(item)}", True, COLOR_RED
            )
            surface.blit(txt, (elim_rect.x + 6, iy))

        # Worst-case scores
        if has_worst:
            wc_rect = self._draw_card(
                surface, rect.x, col_y + col_h + 5, rect.width, 50
            )
            wc_lbl = self.small_font.render(
                "Worst-case analysis:", True, COLOR_TEXT_MUTED
            )
            surface.blit(wc_lbl, (wc_rect.x + 10, wc_rect.y + 8))

            wc_parts = []
            for wc in step.worst_case_scores[:3]:
                ms = self._format_move_full(wc)
                ws = wc.get("worst_score", wc.get("score", "?"))
                wc_parts.append(f"{ms}: {ws}")
            wc_txt = self.tiny_font.render("  |  ".join(wc_parts), True, COLOR_TEXT)
            surface.blit(wc_txt, (wc_rect.x + 10, wc_rect.y + 30))

    # ========================================================================
    # RENDERER: Level 4 — Online / AND-OR / Belief (Nhóm E)
    # ========================================================================

    def _render_online_andor_belief(self, surface, step, rect):
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
        after_rect = self._draw_card(
            surface, rect.x + col_w + 5, weight_y, col_w - 5, weight_h
        )
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
            cand_rect = self._draw_card(
                surface, rect.x, cand_y, rect.width, rect.bottom - cand_y - 5
            )
            c_lbl = self.small_font.render("TOP CANDIDATES:", True, COLOR_TEXT_MUTED)
            surface.blit(c_lbl, (cand_rect.x + 10, cand_rect.y + 8))
            for i, item in enumerate(step.candidates[:5]):
                iy = cand_rect.y + 28 + i * 18
                if iy > cand_rect.bottom - 12:
                    break
                is_best = i == 0
                prefix = "✅ " if is_best else "   "
                txt = self.tiny_font.render(
                    f"{prefix}{self._format_move_full(item)}",
                    True,
                    COLOR_JADE if is_best else COLOR_TEXT,
                )
                surface.blit(txt, (cand_rect.x + 8, iy))

    def _render_andor(self, surface, step, rect):
        """AND-OR Search: OR node + AND responses + worst case"""
        bottom = self._draw_explanation_box(surface, step, rect)

        # OR node (our move)
        or_rect = self._draw_card(surface, rect.x, bottom + 10, rect.width, 35)
        or_move = self._format_move_full(step.or_node)
        or_txt = self.body_font.render(f"OR NODE (ta): {or_move}", True, COLOR_ACCENT)
        surface.blit(or_txt, (or_rect.x + 15, or_rect.y + 8))

        # AND responses (opponent)
        and_y = or_rect.bottom + 10
        and_h = rect.bottom - and_y - 50
        and_rect = self._draw_card(surface, rect.x, and_y, rect.width, and_h)
        and_lbl = self.small_font.render(
            "AND RESPONSES (đối thủ):", True, COLOR_TEXT_MUTED
        )
        surface.blit(and_lbl, (and_rect.x + 10, and_rect.y + 8))
        pygame.draw.line(
            surface,
            COLOR_OUTLINE,
            (and_rect.x + 5, and_rect.y + 28),
            (and_rect.right - 5, and_rect.y + 28),
        )

        for i, resp in enumerate(step.and_responses[:6]):
            iy = and_rect.y + 35 + i * 18
            if iy > and_rect.bottom - 12:
                break
            resp_str = self._format_move_full(resp)
            is_worst = (resp == step.and_responses[-1]) if step.and_responses else False
            suffix = " ← WORST" if is_worst else ""
            color = COLOR_RED if is_worst else COLOR_TEXT
            txt = self.tiny_font.render(f"  {resp_str}{suffix}", True, color)
            surface.blit(txt, (and_rect.x + 8, iy))

        # Guaranteed score
        gs_rect = self._draw_card(surface, rect.x, and_rect.bottom + 5, rect.width, 35)
        gs_txt = self.body_font.render(
            f"Guaranteed score: {step.guaranteed_score:.0f}", True, COLOR_ACCENT
        )
        surface.blit(gs_txt, (gs_rect.x + 15, gs_rect.y + 8))

    def _render_belief(self, surface, step, rect):
        """Belief State: style detection + probability + expected utility"""
        bottom = self._draw_explanation_box(surface, step, rect)

        # Detected style
        style_rect = self._draw_card(surface, rect.x, bottom + 10, rect.width, 55)
        style_txt = self.header_font.render(
            f"Phong cách: {step.opponent_style.upper()}", True, COLOR_ACCENT
        )
        surface.blit(style_txt, (style_rect.x + 15, style_rect.y + 8))

        # Probability distribution
        probs = step.belief_probs
        prob_parts = [f"P({k[:3]})={v:.1f}" for k, v in probs.items()]
        prob_txt = self.small_font.render("  ".join(prob_parts), True, COLOR_TEXT_MUTED)
        surface.blit(prob_txt, (style_rect.x + 15, style_rect.y + 32))

        # Utility per style
        if step.utility_per_style:
            util_rect = self._draw_card(
                surface, rect.x, style_rect.bottom + 10, rect.width, 80
            )
            util_lbl = self.small_font.render(
                "Utility per style:", True, COLOR_TEXT_MUTED
            )
            surface.blit(util_lbl, (util_rect.x + 10, util_rect.y + 8))

            for i, (style, val) in enumerate(step.utility_per_style.items()):
                iy = util_rect.y + 28 + i * 16
                try:
                    txt = self.tiny_font.render(
                        f"  {style}: {val:.0f}", True, COLOR_TEXT
                    )
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
                    f"E[U] = {step.expected_utility:.0f}", True, COLOR_JADE
                )
            except (TypeError, ValueError):
                eu_txt = self.body_font.render(
                    f"E[U] = {step.expected_utility}", True, COLOR_JADE
                )
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
        vars_lbl = self.small_font.render(
            "VARIABLES (domain size):", True, COLOR_TEXT_MUTED
        )
        surface.blit(vars_lbl, (vars_rect.x + 10, vars_rect.y + 8))

        chosen = step.chosen_variable
        for i, (pos, size) in enumerate(list(step.variables.items())[:6]):
            iy = vars_rect.y + 28 + i * 18
            if iy > vars_rect.bottom - 12:
                break
            is_chosen = str(pos) == str(chosen)
            prefix = "✅ " if is_chosen else "   "
            suffix = " ← MRV" if is_chosen else ""
            color = COLOR_JADE if is_chosen else COLOR_TEXT
            txt = self.tiny_font.render(
                f"{prefix}{pos}: domain={size}{suffix}", True, color
            )
            surface.blit(txt, (vars_rect.x + 8, iy))

        # Domain for chosen variable
        if step.domain:
            dom_y = vars_rect.bottom + 10
            dom_h = rect.bottom - dom_y - 10
            dom_rect = self._draw_card(surface, rect.x, dom_y, rect.width, dom_h)
            dom_lbl = self.small_font.render(
                f"DOMAIN cho {chosen}:", True, COLOR_TEXT_MUTED
            )
            surface.blit(dom_lbl, (dom_rect.x + 10, dom_rect.y + 8))

            for i, item in enumerate(step.domain[:8]):
                iy = dom_rect.y + 28 + i * 18
                if iy > dom_rect.bottom - 12:
                    break
                is_best = i == 0
                prefix = "✅ " if is_best else "   "
                suffix = " ← BEST" if is_best else ""
                color = COLOR_JADE if is_best else COLOR_TEXT
                txt = self.tiny_font.render(
                    f"{prefix}{self._format_move_full(item)}{suffix}", True, color
                )
                surface.blit(txt, (dom_rect.x + 8, iy))

    def _render_min_conflicts(self, surface, step, rect):
        """Min-Conflicts: conflict counts + candidates"""
        bottom = self._draw_explanation_box(surface, step, rect)

        # Conflict summary
        best_cand = step.best_candidate
        after = (
            best_cand.get("conflicts_after", 0) if isinstance(best_cand, dict) else 0
        )
        diff = step.current_conflicts - after

        conf_rect = self._draw_card(surface, rect.x, bottom + 10, rect.width, 40)
        conf_txt = self.body_font.render(
            f"Conflicts: {step.current_conflicts} → {after} (giảm {diff})",
            True,
            COLOR_JADE if diff > 0 else COLOR_TEXT,
        )
        surface.blit(conf_txt, (conf_rect.x + 15, conf_rect.y + 10))

        # Candidates list
        cand_y = conf_rect.bottom + 10
        cand_rect = self._draw_card(
            surface, rect.x, cand_y, rect.width, rect.bottom - cand_y - 10
        )
        cand_lbl = self.small_font.render(
            "TOP CANDIDATES (by conflicts):", True, COLOR_TEXT_MUTED
        )
        surface.blit(cand_lbl, (cand_rect.x + 10, cand_rect.y + 8))
        pygame.draw.line(
            surface,
            COLOR_OUTLINE,
            (cand_rect.x + 5, cand_rect.y + 28),
            (cand_rect.right - 5, cand_rect.y + 28),
        )

        for i, item in enumerate(step.candidates[:8]):
            iy = cand_rect.y + 35 + i * 18
            if iy > cand_rect.bottom - 12:
                break
            move_str = self._format_move_full(item)
            conflicts = (
                item.get("conflicts_after", "?") if isinstance(item, dict) else "?"
            )
            is_best = i == 0
            prefix = "✅ " if is_best else "   "
            suffix = " ← BEST" if is_best else ""
            color = COLOR_JADE if is_best else COLOR_TEXT
            txt = self.tiny_font.render(
                f"{prefix}{move_str} conflicts={conflicts}{suffix}", True, color
            )
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
        pygame.draw.line(
            surface,
            COLOR_OUTLINE,
            (safe_rect.x + 5, safe_rect.y + 28),
            (safe_rect.right - 5, safe_rect.y + 28),
        )
        for i, item in enumerate(step.safe_moves[:6]):
            iy = safe_rect.y + 35 + i * 18
            if iy > safe_rect.bottom - 12:
                break
            txt = self.tiny_font.render(
                f"  {self._format_move_full(item)}", True, COLOR_TEXT
            )
            surface.blit(txt, (safe_rect.x + 6, iy))

        # Pruned column
        pruned_rect = self._draw_card(
            surface, rect.x + col_w + 5, col_y, col_w - 5, col_h
        )
        pruned_cnt = len(step.pruned_moves)
        pruned_lbl = self.small_font.render(
            f"PRUNED ❌ ({pruned_cnt})", True, COLOR_RED
        )
        surface.blit(pruned_lbl, (pruned_rect.x + 8, pruned_rect.y + 8))
        pygame.draw.line(
            surface,
            COLOR_OUTLINE,
            (pruned_rect.x + 5, pruned_rect.y + 28),
            (pruned_rect.right - 5, pruned_rect.y + 28),
        )
        for i, item in enumerate(step.pruned_moves[:6]):
            iy = pruned_rect.y + 35 + i * 18
            if iy > pruned_rect.bottom - 12:
                break
            reason = item.get("reason", "") if isinstance(item, dict) else ""
            move_str = self._format_move_full(item)
            label = f"{move_str}: {reason}" if reason else move_str
            txt = self.tiny_font.render(f"  {label[:30]}", True, COLOR_RED)
            surface.blit(txt, (pruned_rect.x + 6, iy))

        # Chosen move
        chosen_rect = self._draw_card(
            surface, rect.x, col_y + col_h + 5, rect.width, 35
        )
        chosen_str = self._format_move_full(step.chosen_from_safe)
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

            pygame.draw.circle(
                surface,
                COLOR_JADE if i == len(path) - 1 else COLOR_TEXT_MUTED,
                (x, y),
                12,
            )
            pygame.draw.circle(surface, COLOR_OUTLINE, (x, y), 12, 1)

            depth = node.get("depth", i)
            d_txt = self.tiny_font.render(f"d{depth}", True, COLOR_BG)
            surface.blit(
                d_txt, (x - d_txt.get_width() // 2, y - d_txt.get_height() // 2)
            )

            if i < len(path) - 1:
                pygame.draw.line(surface, COLOR_OUTLINE, (x + 12, y), (x + 48, y), 2)
                pygame.draw.polygon(
                    surface,
                    COLOR_OUTLINE,
                    [(x + 48, y), (x + 43, y - 3), (x + 43, y + 3)],
                )

        # Alpha/Beta display
        ab_y = path_y + 80
        ab_rect = self._draw_card(surface, rect.x, ab_y, rect.width, 50)

        def format_inf(val):
            if val == float("inf"):
                return "∞"
            elif val == float("-inf"):
                return "-∞"
            try:
                return f"{val:.0f}"
            except Exception:
                return str(val)

        alpha_str = format_inf(step.alpha)
        beta_str = format_inf(step.beta)
        alpha_txt = self.header_font.render(f"α = {alpha_str}", True, COLOR_JADE)
        beta_txt = self.header_font.render(f"β = {beta_str}", True, COLOR_RED)

        surface.blit(
            alpha_txt, (ab_rect.x + 30, ab_rect.centery - alpha_txt.get_height() // 2)
        )
        surface.blit(
            beta_txt,
            (ab_rect.centerx + 30, ab_rect.centery - beta_txt.get_height() // 2),
        )

        # Pruning indicator
        if step.is_pruned:
            prune_txt = self.body_font.render(f"✂️ {step.prune_reason}", True, COLOR_RED)
            surface.blit(prune_txt, (rect.x + 10, ab_rect.bottom + 10))

        # Siblings display — now with move info
        sib_y = ab_y + 70 if not step.is_pruned else ab_y + 90
        sib_rect = pygame.Rect(rect.x, sib_y, rect.width, rect.bottom - sib_y - 10)

        if sib_rect.height > 50:
            self._draw_card(
                surface, sib_rect.x, sib_rect.y, sib_rect.width, sib_rect.height
            )

            sib_lbl = self.small_font.render("Siblings:", True, COLOR_TEXT_MUTED)
            surface.blit(sib_lbl, (sib_rect.x + 10, sib_rect.y + 8))

            for i, sib in enumerate(step.siblings_evaluated[:6]):
                y = sib_rect.y + 30 + i * 18
                if y > sib_rect.bottom - 12:
                    break
                val = sib.get("value", 0)
                move_str = self._format_move_full(sib)
                try:
                    txt = self.tiny_font.render(
                        f"  {move_str} val:{val:.0f}", True, COLOR_TEXT
                    )
                except (TypeError, ValueError):
                    txt = self.tiny_font.render(
                        f"  {move_str} val:{val}", True, COLOR_TEXT
                    )
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
            is_max = node.get("is_max", True) if isinstance(node, dict) else True
            color = COLOR_JADE if i == len(path) - 1 else COLOR_TEXT_MUTED

            pygame.draw.circle(surface, color, (x, y), 12)
            pygame.draw.circle(surface, COLOR_OUTLINE, (x, y), 12, 1)

            label = "▲" if is_max else "▼"
            d_txt = self.tiny_font.render(label, True, COLOR_BG)
            surface.blit(
                d_txt, (x - d_txt.get_width() // 2, y - d_txt.get_height() // 2)
            )

            if i < len(path) - 1:
                pygame.draw.line(surface, COLOR_OUTLINE, (x + 12, y), (x + 48, y), 2)

        # Node type + value
        node = step.current_node
        is_max = node.get("is_max", True) if isinstance(node, dict) else True
        value = node.get("value", 0) if isinstance(node, dict) else 0

        type_rect = self._draw_card(
            surface, rect.x, path_rect.bottom + 10, rect.width, 40
        )
        type_label = "MAX" if is_max else "MIN"
        try:
            type_txt = self.header_font.render(
                f"{type_label} node  VALUE: {value:.0f}", True, COLOR_ACCENT
            )
        except (TypeError, ValueError):
            type_txt = self.header_font.render(
                f"{type_label} node  VALUE: {value}", True, COLOR_ACCENT
            )
        surface.blit(type_txt, (type_rect.x + 15, type_rect.y + 10))

        # Siblings
        sib_y = type_rect.bottom + 10
        sib_rect = self._draw_card(
            surface, rect.x, sib_y, rect.width, rect.bottom - sib_y - 10
        )

        sib_lbl = self.small_font.render("Siblings:", True, COLOR_TEXT_MUTED)
        surface.blit(sib_lbl, (sib_rect.x + 10, sib_rect.y + 8))

        for i, sib in enumerate(step.siblings_evaluated[:6]):
            iy = sib_rect.y + 28 + i * 18
            if iy > sib_rect.bottom - 12:
                break
            val = sib.get("value", 0)
            move_str = self._format_move_full(sib)
            try:
                txt = self.tiny_font.render(
                    f"  {move_str} val:{val:.0f}", True, COLOR_TEXT
                )
            except (TypeError, ValueError):
                txt = self.tiny_font.render(f"  {move_str} val:{val}", True, COLOR_TEXT)
            surface.blit(txt, (sib_rect.x + 10, iy))

        # Best so far
        if step.best_so_far:
            best_str = self._format_move_full(step.best_so_far)
            best_txt = self.small_font.render(
                f"Best so far: {best_str}", True, COLOR_JADE
            )
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
        depth = (
            step.current_node.get("depth", "?")
            if isinstance(step.current_node, dict)
            else "?"
        )
        surface.blit(node_txt, (node_rect.x + 15, node_rect.y + 10))
        depth_txt = self.small_font.render(f"depth={depth}", True, COLOR_TEXT_MUTED)
        surface.blit(
            depth_txt, (node_rect.right - depth_txt.get_width() - 15, node_rect.y + 13)
        )

        # Child values
        if step.child_values:
            children_rect = self._draw_card(
                surface, rect.x, node_rect.bottom + 10, rect.width, 80
            )
            c_lbl = self.small_font.render("Child values:", True, COLOR_TEXT_MUTED)
            surface.blit(c_lbl, (children_rect.x + 10, children_rect.y + 8))

            vals = [
                cv.get("value", 0) if isinstance(cv, dict) else cv
                for cv in step.child_values[:8]
            ]
            try:
                vals_str = ", ".join(f"{v:.0f}" for v in vals)
            except (TypeError, ValueError):
                vals_str = ", ".join(str(v) for v in vals)
            vals_txt = self.body_font.render(vals_str, True, COLOR_TEXT)
            surface.blit(vals_txt, (children_rect.x + 15, children_rect.y + 30))

            try:
                best_txt = self.small_font.render(
                    f"Best = {step.best_value:.0f}", True, COLOR_JADE
                )
            except (TypeError, ValueError):
                best_txt = self.small_font.render(
                    f"Best = {step.best_value}", True, COLOR_JADE
                )
            surface.blit(best_txt, (children_rect.x + 15, children_rect.y + 55))

            formula_y = children_rect.bottom + 10
        else:
            formula_y = node_rect.bottom + 100

        # Expected value formula
        if step.expected_value is not None:
            formula_rect = self._draw_card(surface, rect.x, formula_y, rect.width, 60)
            try:
                e_txt = self.body_font.render(
                    f"E[V] = 0.7 × {step.best_value:.0f} + 0.3 × avg", True, COLOR_TEXT
                )
                result_txt = self.header_font.render(
                    f"= {step.expected_value:.0f}", True, COLOR_JADE
                )
            except (TypeError, ValueError):
                e_txt = self.body_font.render(
                    f"E[V] = {step.expected_value}", True, COLOR_TEXT
                )
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

        pygame.draw.line(
            surface,
            COLOR_OUTLINE,
            (expl_rect.x + 15, expl_rect.y + 45),
            (expl_rect.right - 15, expl_rect.y + 45),
        )

        expl_lines = self._wrap_text(step.explanation, rect.width - 30, self.body_font)
        for i, line in enumerate(expl_lines[:15]):
            txt = self.body_font.render(line, True, COLOR_TEXT)
            surface.blit(txt, (expl_rect.x + 15, expl_rect.y + 60 + i * 20))

        info_y = expl_rect.y + 60 + min(len(expl_lines), 15) * 20 + 20
        self._render_generic_fields(
            surface, step, expl_rect.x + 15, info_y, rect.width - 30
        )

    def _render_generic_fields(self, surface, step, x, y, max_width):
        """Render common fields from step dataclass"""
        fields_to_show = []

        for key, val in step.__dict__.items():
            if key in ["step_num", "algorithm", "explanation", "chosen_move"]:
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
        g = node.get("g", 0)
        h = node.get("h", 0)
        f = node.get("f", 0)

        break_y = rect.bottom - 60
        break_rect = self._draw_card(surface, rect.x, break_y, rect.width, 50)

        try:
            formula = self.body_font.render(
                f"f(n) = g(n) + h(n) = {g:.0f} + {h:.0f} = {f:.0f}", True, COLOR_ACCENT
            )
        except (TypeError, ValueError):
            formula = self.body_font.render(
                f"f(n) = g + h = {g} + {h} = {f}", True, COLOR_ACCENT
            )
        surface.blit(
            formula,
            (
                break_rect.centerx - formula.get_width() // 2,
                break_rect.centery - formula.get_height() // 2,
            ),
        )

    def _wrap_text(self, text, max_width, font):
        """Wrap text to fit within max_width"""
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = " ".join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]

        if current_line:
            lines.append(" ".join(current_line))

        return lines
