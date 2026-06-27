# Pygame Shop Screen for Cờ Tướng AI (Xiangqi Shop - Royal Redesign)
import math
import random

import pygame

from gui.assets import get_asset

COLOR_BG = (30, 16, 12)  # Warm deep mahogany background (#1e100c)
COLOR_CARD_BG = (39, 24, 20)  # Surface-container-low (#271814)
COLOR_TEXT = (250, 220, 213)  # On-surface (#fadcd5)
COLOR_GOLD = (242, 202, 80)  # Antique Gold (#f2ca50)
COLOR_MUTED = (208, 197, 175)  # On-surface-variant (#d0c5af)
COLOR_OUTLINE = (77, 70, 53)  # Outline-variant (#4d4635)
COLOR_ACCENT = (89, 222, 155)  # Secondary green jade (#59de9b)
COLOR_BTN_BUY = (212, 175, 55)  # Purchase button gold
COLOR_BTN_EQUIPPED = (60, 50, 45)  # Equipped state dark


class ShopScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Load premium fonts (falling back to Segoe UI/Tahoma)
        self.title_font = pygame.font.SysFont(
            "Playfair Display, Segoe UI, Tahoma", 38, bold=True
        )
        self.section_font = pygame.font.SysFont(
            "Playfair Display, Segoe UI, Tahoma", 20, bold=True
        )
        self.item_name_font = pygame.font.SysFont(
            "Source Serif 4, Segoe UI, Tahoma", 18, bold=True
        )
        self.body_font = pygame.font.SysFont("Source Serif 4, Segoe UI, Tahoma", 13)
        self.btn_font = pygame.font.SysFont("Segoe UI, Tahoma, Arial", 12, bold=True)
        self.gold_font = pygame.font.SysFont("Consolas, Segoe UI", 16, bold=True)

        # Background wood noise texture cached
        self.wood_texture = self.generate_wood_texture(width, height)

        # Definitions of Shop items
        self.boards = [
            {
                "id": "classic_wood",
                "name": "Gỗ Mộc Cổ Điển",
                "desc": "Phong cách truyền thống với vân gỗ tự nhiên, mang lại cảm giác tĩnh tại và sâu lắng.",
                "price": 0,
                "type": "board",
            },
            {
                "id": "white_marble",
                "name": "Cẩm Thạch Trắng",
                "desc": "Đá cẩm thạch nguyên khối khảm chỉ vàng. Lạnh lùng, sang trọng và đầy uy quyền.",
                "price": 500,
                "type": "board",
            },
            {
                "id": "dark_glass",
                "name": "Hắc Kính Dạ Quang",
                "desc": "Kính cường lực tối màu kết hợp vạch kẻ dạ quang. Khẳng định cá tính khác biệt.",
                "price": 800,
                "type": "board",
            },
        ]

        self.pieces = [
            {
                "id": "classic_wood_piece",
                "name": "Mộc Ngà Cổ Điển",
                "desc": "Quân gỗ mộc mạc viền ngà, chạm khắc tinh xảo truyền thống.",
                "price": 0,
                "type": "piece",
            },
            {
                "id": "royal_jade",
                "name": "Ngọc Bích Đế Vương",
                "desc": "Ngọc lục bảo quý hiếm khắc chữ vàng ròng. Tuyệt tác dành cho bậc trượng phu.",
                "price": 1000,
                "type": "piece",
            },
            {
                "id": "cyber_steel",
                "name": "Thép Lạnh Cyberpunk",
                "desc": "Thép nguyên khối tiện CNC chính xác, rãnh chữ khắc ánh sáng neon âm bản.",
                "price": 1200,
                "type": "piece",
            },
        ]

        # Layout metrics
        self.padding = 40
        self.card_width = 300
        self.card_height = 236

        # Rect of Back Button
        self.btn_back = pygame.Rect(40, 32, 110, 34)

        # Define Rects for cards dynamically in draw
        self.card_rects = {}  # key: item_id -> Rect

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

        # Regenerate wood texture
        self.wood_texture = self.generate_wood_texture(width, height)

        # Recalculate Back button
        self.btn_back = pygame.Rect(40, 32, 110, 34)

        # Clear card rects to be re-populated dynamically in draw
        self.card_rects = {}

    def handle_event(self, event, controller):
        """Processes clicks on buy/equip/back buttons. Returns state if changed."""
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return None

        pos = event.pos

        # Check Back Button
        if self.btn_back.collidepoint(pos):
            from gui.sound import play_synth_sound

            play_synth_sound("move")
            return "menu"

        # Check Item Card clicks
        from gui.sound import play_synth_sound

        for item_id, rect in self.card_rects.items():
            if rect.collidepoint(pos):
                # Find the item
                item = None
                for b in self.boards:
                    if b["id"] == item_id:
                        item = b
                for p in self.pieces:
                    if p["id"] == item_id:
                        item = p

                if not item:
                    continue

                is_owned = False
                is_equipped = False

                if item["type"] == "board":
                    is_owned = item["id"] in controller.owned_boards
                    is_equipped = controller.equipped_board == item["id"]
                else:
                    is_owned = item["id"] in controller.owned_pieces
                    is_equipped = controller.equipped_piece == item["id"]

                # Action: Buy or Equip
                if is_owned:
                    if not is_equipped:
                        if item["type"] == "board":
                            controller.equipped_board = item["id"]
                        else:
                            controller.equipped_piece = item["id"]
                        play_synth_sound("move")
                else:
                    # Try to buy
                    if controller.gold >= item["price"]:
                        controller.gold -= item["price"]
                        if item["type"] == "board":
                            controller.owned_boards.append(item["id"])
                            controller.equipped_board = item["id"]
                        else:
                            controller.owned_pieces.append(item["id"])
                            controller.equipped_piece = item["id"]
                        play_synth_sound("check")
                    else:
                        play_synth_sound("capture")  # Insufficient funds beep

        return None

    def draw(self, surface, controller):
        # 1. Draw wood background
        bg_img = get_asset("mahogany_table")
        if bg_img:
            scaled = pygame.transform.smoothscale(bg_img, (self.width, self.height))
            surface.blit(scaled, (0, 0))
        else:
            surface.blit(self.wood_texture, (0, 0))

        # 2. Draw Top Bar
        top_bar = pygame.Surface((self.width, 80), pygame.SRCALPHA)
        top_bar.fill((15, 8, 6, 180))
        surface.blit(top_bar, (0, 0))
        pygame.draw.line(surface, COLOR_OUTLINE, (0, 80), (self.width, 80), 1)

        # Back Button
        pygame.draw.rect(surface, (60, 40, 30), self.btn_back, 0, 6)
        pygame.draw.rect(surface, COLOR_GOLD, self.btn_back, 1, 6)
        back_txt = self.btn_font.render("QUAY LẠI", True, COLOR_GOLD)
        surface.blit(
            back_txt,
            (
                self.btn_back.centerx - back_txt.get_width() // 2,
                self.btn_back.centery - back_txt.get_height() // 2,
            ),
        )

        # Gold counter box (Right side)
        gold_box = pygame.Rect(self.width - 200, 20, 160, 40)
        pygame.draw.rect(surface, (30, 20, 15), gold_box, 0, 20)
        pygame.draw.rect(surface, COLOR_GOLD, gold_box, 1, 20)

        # Draw Gold Coin Icon
        pygame.draw.circle(surface, COLOR_GOLD, (gold_box.x + 20, gold_box.centery), 9)
        pygame.draw.circle(
            surface, (200, 150, 30), (gold_box.x + 20, gold_box.centery), 6
        )
        c_font = pygame.font.SysFont("Segoe UI, Tahoma", 10, bold=True)
        c_txt = c_font.render("V", True, COLOR_GOLD)
        surface.blit(
            c_txt,
            (
                gold_box.x + 20 - c_txt.get_width() // 2,
                gold_box.centery - c_txt.get_height() // 2 + 1,
            ),
        )

        gold_val_txt = self.gold_font.render(f"{controller.gold:,}", True, COLOR_GOLD)
        surface.blit(
            gold_val_txt,
            (gold_box.x + 38, gold_box.centery - gold_val_txt.get_height() // 2),
        )

        # Title "CỬA TIỆM HOÀNG GIA"
        brand_font = pygame.font.SysFont("Playfair Display, Segoe UI", 18, bold=True)
        brand_txt = brand_font.render("Hoàng Gia Tượng Kỳ", True, COLOR_GOLD)
        surface.blit(brand_txt, (self.width // 2 - brand_txt.get_width() // 2, 30))

        # 3. Main Header (Under top bar)
        title_txt = self.title_font.render("Cửa Tiệm Hoàng Gia", True, COLOR_GOLD)
        surface.blit(title_txt, (self.width // 2 - title_txt.get_width() // 2, 105))

        sub_txt = self.body_font.render(
            "Trang hoàng kỳ đài, khẳng định đẳng cấp. Khám phá những tuyệt tác thủ công dành riêng cho Kỳ Vương.",
            True,
            COLOR_MUTED,
        )
        surface.blit(sub_txt, (self.width // 2 - sub_txt.get_width() // 2, 152))

        # Horizontal divider decoration
        div_w = 400
        div_x = self.width // 2 - div_w // 2
        div_y = 185
        pygame.draw.line(
            surface, COLOR_OUTLINE, (div_x, div_y), (div_x + div_w, div_y), 1
        )
        pygame.draw.polygon(
            surface,
            COLOR_GOLD,
            [
                (self.width // 2 - 8, div_y),
                (self.width // 2, div_y - 4),
                (self.width // 2 + 8, div_y),
                (self.width // 2, div_y + 4),
            ],
        )

        # 4. Draw Section: BÀN CỜ (BOARDS)
        sec1_y = 210
        sec1_lbl = self.section_font.render("BÀN CỜ", True, COLOR_GOLD)
        surface.blit(sec1_lbl, (80, sec1_y))
        pygame.draw.line(
            surface,
            COLOR_OUTLINE,
            (170, sec1_y + 14),
            (self.width - 80, sec1_y + 14),
            1,
        )

        board_start_x = max(40, (self.width - 960) // 2)
        board_spacing = 30
        for i, item in enumerate(self.boards):
            x = board_start_x + i * (self.card_width + board_spacing)
            y = sec1_y + 42
            self.draw_item_card(surface, x, y, item, controller)

        # 5. Draw Section: QUÂN CỜ (PIECES)
        sec2_y = 515
        sec2_lbl = self.section_font.render("QUÂN CỜ", True, COLOR_GOLD)
        surface.blit(sec2_lbl, (80, sec2_y))
        pygame.draw.line(
            surface,
            COLOR_OUTLINE,
            (185, sec2_y + 14),
            (self.width - 80, sec2_y + 14),
            1,
        )

        piece_start_x = max(40, (self.width - 960) // 2)
        piece_spacing = 30
        for i, item in enumerate(self.pieces):
            x = piece_start_x + i * (self.card_width + piece_spacing)
            y = sec2_y + 42
            self.draw_item_card(surface, x, y, item, controller)

    def draw_item_card(self, surface, x, y, item, controller):
        card_rect = pygame.Rect(x, y, self.card_width, self.card_height)
        self.card_rects[item["id"]] = card_rect

        # Determine status
        is_owned = False
        is_equipped = False
        if item["type"] == "board":
            is_owned = item["id"] in controller.owned_boards
            is_equipped = controller.equipped_board == item["id"]
        else:
            is_owned = item["id"] in controller.owned_pieces
            is_equipped = controller.equipped_piece == item["id"]

        # Card Background
        pygame.draw.rect(surface, COLOR_CARD_BG, card_rect, 0, 10)
        # Specular/light highlight border
        border_color = (
            COLOR_GOLD if is_equipped else (COLOR_OUTLINE if is_owned else (50, 35, 30))
        )
        border_width = 2 if is_equipped else 1
        pygame.draw.rect(surface, border_color, card_rect, border_width, 10)

        # 1. Preview Box (top part of card)
        preview_h = 96
        preview_rect = pygame.Rect(x + 10, y + 10, self.card_width - 20, preview_h)
        pygame.draw.rect(surface, (20, 12, 10), preview_rect, 0, 6)

        asset_map = {
            "classic_wood": "board_parchment",
            "white_marble": "board_marble",
            "dark_glass": "board_glass",
            "royal_jade": "piece_jade",
            "cyber_steel": "piece_steel",
        }
        asset_name = asset_map.get(item["id"])
        img = get_asset(asset_name) if asset_name else None

        if img:
            if item["type"] == "board":
                scaled = pygame.transform.smoothscale(
                    img, (preview_rect.width, preview_rect.height)
                )
                surface.blit(scaled, (preview_rect.x, preview_rect.y))
                pygame.draw.rect(surface, COLOR_OUTLINE, preview_rect, 1, 6)
            else:
                px, py = preview_rect.centerx, preview_rect.centery
                r = 32
                scaled = pygame.transform.smoothscale(img, (r * 2, r * 2))
                surface.blit(scaled, (px - r, py - r))
        else:
            # Fallback to stylized vector previews
            if item["type"] == "board":
                if item["id"] == "classic_wood":
                    # Draw small wood planks
                    for py in range(preview_rect.y + 4, preview_rect.bottom - 4, 10):
                        pygame.draw.line(
                            surface,
                            (120, 75, 35),
                            (preview_rect.x + 10, py),
                            (preview_rect.right - 10, py),
                            1,
                        )
                    pygame.draw.rect(
                        surface,
                        (90, 50, 15),
                        (preview_rect.centerx - 30, preview_rect.centery - 30, 60, 60),
                        1,
                    )
                    pygame.draw.line(
                        surface,
                        (90, 50, 15),
                        (preview_rect.centerx, preview_rect.centery - 30),
                        (preview_rect.centerx, preview_rect.centery + 30),
                        1,
                    )
                    pygame.draw.line(
                        surface,
                        (90, 50, 15),
                        (preview_rect.centerx - 30, preview_rect.centery),
                        (preview_rect.centerx + 30, preview_rect.centery),
                        1,
                    )
                elif item["id"] == "white_marble":
                    pygame.draw.rect(surface, (230, 230, 230), preview_rect, 0, 6)
                    random.seed(42)
                    for _ in range(5):
                        x1 = random.randint(preview_rect.x, preview_rect.right)
                        y1 = random.randint(preview_rect.y, preview_rect.bottom)
                        x2 = x1 + random.randint(-30, 30)
                        y2 = y1 + random.randint(-30, 30)
                        pygame.draw.line(
                            surface, (190, 190, 190), (x1, y1), (x2, y2), 2
                        )
                    random.seed()
                    pygame.draw.rect(
                        surface,
                        COLOR_GOLD,
                        (preview_rect.centerx - 30, preview_rect.centery - 30, 60, 60),
                        1,
                    )
                elif item["id"] == "dark_glass":
                    pygame.draw.rect(surface, (10, 15, 25), preview_rect, 0, 6)
                    pygame.draw.rect(
                        surface,
                        (0, 180, 255),
                        (preview_rect.centerx - 30, preview_rect.centery - 30, 60, 60),
                        1,
                    )
                    pygame.draw.line(
                        surface,
                        (0, 180, 255),
                        (preview_rect.centerx - 30, preview_rect.centery - 30),
                        (preview_rect.centerx + 30, preview_rect.centery + 30),
                        1,
                    )
                    pygame.draw.line(
                        surface,
                        (0, 180, 255),
                        (preview_rect.centerx + 30, preview_rect.centery - 30),
                        (preview_rect.centerx - 30, preview_rect.centery + 30),
                        1,
                    )
            else:  # piece
                px, py = preview_rect.centerx, preview_rect.centery
                r = 28
                if item["id"] == "classic_wood_piece":
                    pygame.draw.circle(surface, (160, 110, 60), (px, py), r)
                    pygame.draw.circle(surface, (250, 240, 215), (px, py), r - 2)
                    p_font = pygame.font.SysFont("Segoe UI, Tahoma", 18, bold=True)
                    p_txt = p_font.render("將", True, (20, 20, 20))
                    surface.blit(
                        p_txt,
                        (px - p_txt.get_width() // 2, py - p_txt.get_height() // 2),
                    )
                elif item["id"] == "royal_jade":
                    pygame.draw.circle(surface, (0, 90, 60), (px, py), r)
                    pygame.draw.circle(surface, (0, 140, 100), (px, py), r - 2)
                    p_font = pygame.font.SysFont("Segoe UI, Tahoma", 18, bold=True)
                    p_txt = p_font.render("將", True, COLOR_GOLD)
                    surface.blit(
                        p_txt,
                        (px - p_txt.get_width() // 2, py - p_txt.get_height() // 2),
                    )
                elif item["id"] == "cyber_steel":
                    pygame.draw.circle(surface, (50, 50, 55), (px, py), r)
                    pygame.draw.circle(surface, (90, 90, 95), (px, py), r - 2)
                    p_font = pygame.font.SysFont("Segoe UI, Tahoma", 18, bold=True)
                    p_txt = p_font.render("將", True, (0, 220, 255))
                    surface.blit(
                        p_txt,
                        (px - p_txt.get_width() // 2, py - p_txt.get_height() // 2),
                    )

        # Status Label on Preview
        if is_equipped:
            lbl_bg = pygame.Rect(x + 15, y + 15, 84, 20)
            pygame.draw.rect(surface, (40, 80, 50), lbl_bg, 0, 4)
            lbl_txt = self.btn_font.render("ĐANG DÙNG", True, COLOR_ACCENT)
            surface.blit(
                lbl_txt,
                (
                    lbl_bg.centerx - lbl_txt.get_width() // 2,
                    lbl_bg.centery - lbl_txt.get_height() // 2,
                ),
            )
        elif is_owned:
            lbl_bg = pygame.Rect(x + 15, y + 15, 78, 20)
            pygame.draw.rect(surface, (50, 50, 50), lbl_bg, 0, 4)
            lbl_txt = self.btn_font.render("ĐÃ SỞ HỮU", True, COLOR_TEXT)
            surface.blit(
                lbl_txt,
                (
                    lbl_bg.centerx - lbl_txt.get_width() // 2,
                    lbl_bg.centery - lbl_txt.get_height() // 2,
                ),
            )

        # 2. Text Info
        name_txt = self.item_name_font.render(
            item["name"], True, COLOR_GOLD if is_equipped else COLOR_TEXT
        )
        surface.blit(name_txt, (x + 15, y + 115))

        # Desc - multi-line split manually for small box
        desc_words = item["desc"].split()
        lines = []
        curr_line = ""
        for word in desc_words:
            test_line = curr_line + (" " if curr_line else "") + word
            if self.body_font.size(test_line)[0] < self.card_width - 30:
                curr_line = test_line
            else:
                lines.append(curr_line)
                curr_line = word
        if curr_line:
            lines.append(curr_line)

        dy = y + 138
        for line in lines[:2]:  # Show up to 2 lines
            l_txt = self.body_font.render(line, True, COLOR_MUTED)
            surface.blit(l_txt, (x + 15, dy))
            dy += 16

        # 3. Action Button (Bottom)
        btn_rect = pygame.Rect(x + 15, y + 190, self.card_width - 30, 32)
        if is_equipped:
            pygame.draw.rect(surface, COLOR_BTN_EQUIPPED, btn_rect, 0, 5)
            pygame.draw.rect(surface, COLOR_OUTLINE, btn_rect, 1, 5)
            b_txt = self.btn_font.render("ĐANG TRANG BỊ", True, COLOR_MUTED)
            surface.blit(
                b_txt,
                (
                    btn_rect.centerx - b_txt.get_width() // 2,
                    btn_rect.centery - b_txt.get_height() // 2,
                ),
            )
        elif is_owned:
            pygame.draw.rect(surface, (80, 60, 50), btn_rect, 0, 5)
            pygame.draw.rect(surface, COLOR_GOLD, btn_rect, 1, 5)
            b_txt = self.btn_font.render("SỬ DỤNG", True, COLOR_GOLD)
            surface.blit(
                b_txt,
                (
                    btn_rect.centerx - b_txt.get_width() // 2,
                    btn_rect.centery - b_txt.get_height() // 2,
                ),
            )
        else:
            pygame.draw.rect(surface, COLOR_GOLD, btn_rect, 0, 5)
            btn_str = f"MUA - {item['price']} VÀNG"
            b_txt = self.btn_font.render(btn_str, True, (20, 10, 5))
            surface.blit(
                b_txt,
                (
                    btn_rect.centerx - b_txt.get_width() // 2,
                    btn_rect.centery - b_txt.get_height() // 2,
                ),
            )
