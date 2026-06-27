# BÁO CÁO TRẢ LỜI CÂU HỎI HỆ THỐNG AI & VISUALIZER

---

## === PHẦN 1: DỮ LIỆU GHI VÀO STEP ===

### 1. Trong mỗi hàm AI:
#### Các trường move/current_move/candidate_move đang lưu kiểu dữ liệu gì?
Trong các hàm AI, các trường `move`, `current_move`, `candidate_move` chủ yếu lưu dưới dạng **`dict`** (để truyền vào `current_node`, `current_move`, `candidate_move`) hoặc **`tuple`** (để truyền vào `chosen_move`, `move`):

*   **`chosen_move`** (trong tất cả các Step): Lưu kiểu **`tuple`** tọa độ dạng `((from_r, from_c), (to_r, to_c))` hoặc `None`.
*   **`current_node`** (trong BFS, DFS, UCS, Greedy, A*, IDA*, Minimax, Alpha-Beta, Expectimax): Lưu kiểu **`dict`**. Ví dụ trong A*: `{'move': (from_pos, to_pos), 'g': g, 'h': h, 'f': f, 'piece_captured': piece_name, 'cap_val': cap_val}`.
*   **`current_move` / `candidate_move`** (trong Hill Climbing, Simulated Annealing): Lưu kiểu **`dict`**. Ví dụ trong SA: `{'move': current_move, 'score': current_score}` (trong đó giá trị bên trong key `'move'` là một `tuple`).
*   **Các danh sách (`frontier`, `explored`, `candidates`, `neighbors`, `domain`, `and_responses`, `safe_moves`, `pruned_moves`)**: Lưu kiểu **`list` các `dict`**.

---

#### Paste đoạn `recorder.add_step(...)` của từng hàm:

**1. `bfs_move` (Level 1):**
```python
            recorder.add_step(BFSStep(
                step_num=step_counter + 1,
                algorithm="BFS",
                explanation=f"Duyệt node n{curr.id} ở depth={curr.depth}, mở rộng các nước đi tiếp theo",
                current_node={'id': f'n{curr.id}', 'move': curr.move, 'depth': curr.depth, 'score': curr.score},
                queue=queue_info,
                explored=explored_nodes.copy()
            ))
```

**2. `dfs_move` (Level 1):**
```python
            recorder.add_step(DFSStep(
                step_num=step_counter[0] + 1,
                algorithm="DFS",
                explanation=f"DFS ở depth={depth - remaining_depth}, duyệt {len(moves)} nước đi",
                current_node={'depth': depth - remaining_depth, 'score': None},
                stack=current_stack.copy(),
                explored=explored_nodes.copy(),
                is_backtracking=False
            ))
```

**3. `ucs_move` (Level 1):**
```python
            recorder.add_step(UCSStep(
                step_num=i + 1,
                algorithm="UCS",
                explanation=f"Xét nước {from_pos}→{to_pos}: cost = 1000 - {cap_val}({piece_name}) = {cost}",
                chosen_move=best_move,
                current_node=node_info,
                frontier=sorted_frontier.copy(),
                explored=explored_list.copy()
            ))
```

**4. `greedy_move` (Level 2):**
```python
            recorder.add_step(GreedyStep(
                step_num=i + 1,
                algorithm="Greedy",
                explanation=f"Xét nước {from_pos}→{to_pos}: h={val} ({piece_name}), chọn h LỚN NHẤT",
                chosen_move=best_move,
                current_node=candidate_info,
                candidates=sorted_candidates.copy()
            ))
```

**5. `a_star_move` (Level 2):**
```python
            recorder.add_step(AStarStep(
                step_num=i + 1,
                algorithm="A*",
                explanation=f"Xét nước {from_pos}→{to_pos}: g={g} (1000-{cap_val}), h={h} (vật chất đối thủ), f={f}",
                chosen_move=best_move,
                current_node=node_info,
                frontier=sorted_frontier.copy(),
                explored=explored_list.copy()
            ))
```

**6. `ida_star_move` (Level 2):**
```python
            # Trong hàm search():
            recorder.add_step(IDAStarStep(
                step_num=step_counter[0] + 1,
                algorithm="IDA*",
                explanation=f"IDA* node {from_pos}→{to_pos}: f={f}, threshold={threshold}, depth={depth}",
                current_node={'move': (from_pos, to_pos), 'g': g, 'h': h, 'f': f},
                threshold=threshold,
                iteration=0,  # Will be updated in outer loop
                exceeded_f=f if f > threshold else None,
                is_cutoff=(f > threshold)
            ))
            
            # Trong vòng lặp iterative deepening:
            recorder.add_step(IDAStarStep(
                step_num=step_counter[0] + 1,
                algorithm="IDA*",
                explanation=f"IDA* Iteration {iteration + 1}: threshold={threshold}",
                iteration=iteration + 1,
                threshold=threshold
            ))
```

**7. `hill_climbing_move` (Level 3):**
```python
            recorder.add_step(HillClimbStep(
                step_num=i + 1,
                algorithm="Hill Climbing",
                explanation=f"Xét nước {from_pos}→{to_pos}: score={score}, tìm neighbor tốt nhất",
                chosen_move=best_move,
                current_score=best_score,
                current_move={'move': best_move, 'score': best_score},
                neighbors=sorted_neighbors.copy(),
                best_neighbor={'move': best_move, 'score': best_score},
                is_plateau=(score <= best_score and i > 0)
            ))
```

**8. `simulated_annealing_move` (Level 3):**
```python
            recorder.add_step(SAStep(
                step_num=step_counter + 1,
                algorithm="Simulated Annealing",
                explanation=f"T={temp:.1f}, ΔE={delta:.0f}, P(accept)={accept_prob:.3f} → {'✅ Chấp nhận' if accepted else '❌ Từ chối'}",
                chosen_move=best_move,
                current_move={'move': current_move, 'score': current_score},
                candidate_move={'move': candidate, 'score': score},
                temperature=temp,
                delta_e=delta,
                accept_prob=accept_prob,
                accepted=accepted
            ))
```

**9. `beam_search_move` (Level 3):**
```python
        # Bước 1:
        recorder.add_step(BeamStep(
            step_num=1,
            algorithm="Beam Search",
            explanation=f"Chọn top {k} beams từ {len(candidates)} candidates, loại bỏ {len(eliminated)}",
            beam_k=k,
            all_candidates=[{'move': m, 'score': s} for s, m in candidates],
            kept_beams=[{'move': m, 'score': s} for s, m in beam],
            eliminated=[{'move': m, 'score': s} for s, m in eliminated],
            worst_case_scores=[]
        ))
        
        # Bước 2:
        recorder.add_step(BeamStep(
            step_num=2,
            algorithm="Beam Search",
            explanation=f"Đánh giá worst-case response, chọn beam có worst-case score cao nhất: {best_beam_score:.0f}",
            chosen_move=best_beam_move,
            beam_k=k,
            all_candidates=[{'move': m, 'score': s} for s, m in candidates],
            kept_beams=[{'move': m, 'score': s} for s, m in beam],
            eliminated=[{'move': m, 'score': s} for s, m in eliminated],
            worst_case_scores=worst_case_scores
        ))
```

**10. `online_search_move` (Level 4):**
```python
        # Bước 1:
        recorder.add_step(OnlineStep(
            step_num=1,
            algorithm="Online Search",
            explanation=f"{'⚠️ Đang bị chiếu' if in_check else '✅ An toàn'} → Điều chỉnh trọng số động",
            in_check=in_check,
            weights_before=weights_before,
            weights_after=weights_after,
            candidates=[]
        ))
        
        # Bước 2:
        recorder.add_step(OnlineStep(
            step_num=2,
            algorithm="Online Search",
            explanation=f"Chọn nước tốt nhất với trọng số mới: score={best_score:.0f}",
            chosen_move=best_move,
            in_check=in_check,
            weights_before=weights_before,
            weights_after=weights_after,
            candidates=sorted_candidates
        ))
```

**11. `and_or_search_move` (Level 4):**
```python
            recorder.add_step(AndOrStep(
                step_num=i + 1,
                algorithm="AND-OR Search",
                explanation=f"OR node: {from_pos}→{to_pos}, worst-case score={worst_case_score:.0f}",
                chosen_move=best_move if worst_case_score > best_guaranteed_score else None,
                or_node={'move': (from_pos, to_pos), 'responses_count': len(and_responses)},
                and_responses=and_responses[:5],  # Limit to 5 for display
                worst_case={'move': worst_case_move, 'score': worst_case_score} if worst_case_move else {},
                guaranteed_score=worst_case_score
            ))
```

**12. `belief_state_search_move` (Level 4):**
```python
        # Bước 1:
        recorder.add_step(BeliefStep(
            step_num=1,
            algorithm="Belief State",
            explanation=f"Phát hiện phong cách đối thủ: {opp_style.upper()}",
            opponent_style=opp_style,
            belief_probs={'aggressive': p_agg, 'defensive': p_def, 'positional': p_pos},
            utility_per_style={},
            expected_utility=0.0
        ))
        
        # Bước 2:
        recorder.add_step(BeliefStep(
            step_num=2,
            algorithm="Belief State",
            explanation=f"E[U]={best_expected_utility:.0f} = {p_agg:.1f}*{u_agg:.0f} + {p_def:.1f}*{u_def:.0f} + {p_pos:.1f}*{u_pos:.0f}",
            chosen_move=best_move,
            opponent_style=opp_style,
            belief_probs={'aggressive': p_agg, 'defensive': p_def, 'positional': p_pos},
            utility_per_style={'aggressive': u_agg, 'defensive': u_def, 'positional': u_pos},
            expected_utility=best_expected_utility
        ))
```

**13. `backtracking_mrv_move` (Level 5):**
```python
        # Bước 1:
        recorder.add_step(BacktrackStep(
            step_num=1,
            algorithm="Backtracking MRV",
            explanation=f"Tính domain size cho {len(var_domains)} biến (quân cờ)",
            variables=variables_info
        ))
        
        # Bước 2:
        recorder.add_step(BacktrackStep(
            step_num=2,
            algorithm="Backtracking MRV",
            explanation=f"MRV chọn biến {chosen_var} (domain={len(var_domains[chosen_var])} - nhỏ nhất), score={best_score:.0f}",
            chosen_move=(chosen_var, best_to),
            variables={str(pos): len(domain) for pos, domain in var_domains.items()},
            chosen_variable=str(chosen_var),
            domain=domain_list,
            best_assignment={'move': (chosen_var, best_to), 'score': best_score}
        ))
```

**14. `min_conflicts_move` (Level 5):**
```python
        recorder.add_step(MinConflictStep(
            step_num=1,
            algorithm="Min-Conflicts",
            explanation=f"Conflicts trước={current_conflicts}, sau={min_conflicts} (giảm {current_conflicts - min_conflicts})",
            chosen_move=best_move,
            current_conflicts=current_conflicts,
            candidates=sorted_candidates,
            best_candidate={'move': best_move, 'conflicts_after': min_conflicts, 'score': best_score}
        ))
```

**15. `ac3_move` (Level 5):**
```python
        recorder.add_step(AC3Step(
            step_num=1,
            algorithm="AC-3",
            explanation=f"Lọc {len(pruned_moves)}/{len(legal_moves)} nước không an toàn, còn {len(safe_moves)} nước an toàn",
            chosen_move=best_move,
            all_moves=len(legal_moves),
            safe_moves=[{'move': m, 'score': best_score if m == best_move else 0} for m in safe_moves[:10]],
            pruned_moves=pruned_moves[:10],
            chosen_from_safe={'move': best_move, 'score': best_score}
        ))
```

**16. `minimax_move` (Level 6):**
```python
                # MAX node:
                if recorder and step_counter[0] < 20:
                    from ai.step_recorder import MinimaxStep
                    recorder.add_step(MinimaxStep(
                        step_num=step_counter[0] + 1,
                        algorithm="Minimax",
                        explanation=f"MAX node depth={d}, value={val:.0f}",
                        current_node={'move': m, 'depth': d, 'is_max': True, 'value': val},
                        current_path=[{'move': p, 'depth': depth - len(path) + i} for i, p in enumerate(path + [m])],
                        siblings_evaluated=siblings.copy(),
                        best_so_far={'move': m, 'value': max_val}
                    ))
                    step_counter[0] += 1
                    
                # MIN node:
                if recorder and step_counter[0] < 20:
                    from ai.step_recorder import MinimaxStep
                    recorder.add_step(MinimaxStep(
                        step_num=step_counter[0] + 1,
                        algorithm="Minimax",
                        explanation=f"MIN node depth={d}, value={val:.0f}",
                        current_node={'move': m, 'depth': d, 'is_max': False, 'value': val},
                        current_path=[{'move': p, 'depth': depth - len(path) + i} for i, p in enumerate(path + [m])],
                        siblings_evaluated=siblings.copy(),
                        best_so_far={'move': m, 'value': min_val}
                    ))
                    step_counter[0] += 1
```

**17. `alpha_beta_move` (Level 6):**
```python
                # MAX node:
                if recorder and step_counter[0] < 30:
                    from ai.step_recorder import AlphaBetaStep
                    is_pruned = (beta <= alpha)
                    recorder.add_step(AlphaBetaStep(
                        step_num=step_counter[0] + 1,
                        algorithm="Alpha-Beta",
                        explanation=f"MAX node depth={d}, α={old_alpha:.0f}→{alpha:.0f}, β={beta:.0f}" + 
                                  (f" → Cắt tỉa!" if is_pruned else ""),
                        current_node={'move': m, 'depth': d, 'is_max': True, 'value': val},
                        current_path=[{'move': p, 'depth': depth - len(path) + i} for i, p in enumerate(path + [m])],
                        alpha=alpha,
                        beta=beta,
                        is_pruned=is_pruned,
                        prune_reason=f"β({beta:.0f}) ≤ α({alpha:.0f}) → cắt nhánh" if is_pruned else "",
                        siblings_evaluated=siblings.copy()
                    ))
                    step_counter[0] += 1

                # MIN node:
                if recorder and step_counter[0] < 30:
                    from ai.step_recorder import AlphaBetaStep
                    is_pruned = (beta <= alpha)
                    recorder.add_step(AlphaBetaStep(
                        step_num=step_counter[0] + 1,
                        algorithm="Alpha-Beta",
                        explanation=f"MIN node depth={d}, α={alpha:.0f}, β={old_beta:.0f}→{beta:.0f}" +
                                  (f" → Cắt tỉa!" if is_pruned else ""),
                        current_node={'move': m, 'depth': d, 'is_max': False, 'value': val},
                        current_path=[{'move': p, 'depth': depth - len(path) + i} for i, p in enumerate(path + [m])],
                        alpha=alpha,
                        beta=beta,
                        is_pruned=is_pruned,
                        prune_reason=f"β({beta:.0f}) ≤ α({alpha:.0f}) → cắt nhánh" if is_pruned else "",
                        siblings_evaluated=siblings.copy()
                    ))
                    step_counter[0] += 1
```

**18. `expectimax_move` (Level 6):**
```python
            if recorder and step_counter[0] < 20:
                from ai.step_recorder import ExpectimaxStep
                recorder.add_step(ExpectimaxStep(
                    step_num=step_counter[0] + 1,
                    algorithm="Expectimax",
                    explanation=f"CHANCE node depth={d}, E[V]={expected_val:.0f} (70% best + 30% avg)",
                    current_node={'depth': d, 'is_ai_turn': is_ai_turn},
                    is_chance_node=True,
                    child_values=[{'value': v} for v in results],
                    best_value=best_res,
                    expected_value=expected_val
                ))
                step_counter[0] += 1
```

---

### 2. Khi hiển thị tên quân cờ và tọa độ, code đang làm như thế nào?
#### Có dùng PIECE_NAME_VI không?
Có. Trong các hàm `ucs_move`, `greedy_move`, `a_star_move`, code định nghĩa từ điển `PIECE_NAME_VI` để dịch tên quân cờ sang tiếng Việt nhằm đưa vào chuỗi giải thích `explanation` và thông tin node:
```python
    # Mapping piece names to Vietnamese
    PIECE_NAME_VI = {
        'general': 'Tướng', 'advisor': 'Sĩ', 'elephant': 'Tượng',
        'horse': 'Mã', 'rook': 'Xe', 'cannon': 'Pháo', 'pawn': 'Tốt'
    }
```

#### get_piece(pos) trả về object gì, có thuộc tính gì?
`board.get_piece(pos)` trả về đối tượng con của lớp **`Piece`** (như `General`, `Rook`, `Cannon`, `Pawn`...).
Các thuộc tính quan trọng của object này bao gồm:
*   `name`: Tên định danh (ví dụ: `'general'`, `'rook'`, `'cannon'`, `'pawn'`, hoặc `'P'`, `'R'` tùy theo ngữ cảnh khởi tạo).
*   `color`: Màu sắc quân cờ (`'red'` hoặc `'black'`).
*   `pos`: Tọa độ hiện tại trên bàn cờ, lưu dạng tuple `(row, col)`.
*   `char`: Ký tự chữ Hán hiển thị trên bàn cờ (ví dụ: `'帥'`, `'車'`, `'炮'`).

---

## === PHẦN 2: VISUALIZER ===

### 3. Trong gui/visualizer.py:
#### Có bao nhiêu hàm _render_xxx?
Có tổng cộng **9 hàm** bắt đầu bằng `_render_`:
1. `_render_empty(self, surface)`
2. `_render_header(self, surface, step, recorder)`
3. `_render_footer(self, surface, controller, recorder)`
4. `_render_search_3col(self, surface, step, rect)`
5. `_render_alpha_beta(self, surface, step, rect)`
6. `_render_sa(self, surface, step, rect)`
7. `_render_text_only(self, surface, step, rect)`
8. `_render_generic_fields(self, surface, step, x, y, max_width)`
9. `_render_score_breakdown_astar(self, surface, step, rect)`

---

#### Mỗi hàm đang đọc dữ liệu từ Step như thế nào? (Paste code từng hàm):

**1. `_render_empty`:** (Không đọc từ step, chỉ hiển thị thông báo trống)
```python
    def _render_empty(self, surface):
        """Shown when no steps available"""
        msg = self.body_font.render("Chưa có dữ liệu visualization", True, COLOR_TEXT_MUTED)
        surface.blit(msg, (self.x + self.width // 2 - msg.get_width() // 2, self.y + self.height // 2))
```

**2. `_render_header`:** Đọc `step.algorithm` và thông số index từ `recorder`.
```python
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
```

**3. `_render_footer`:** (Đọc trạng thái index từ `recorder` và `controller.mode`)
```python
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
```

**4. `_render_search_3col`:** Đọc `step.explanation`, `step.current_node`, `step.frontier`, `step.explored`.
```python
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
```

**5. `_render_alpha_beta`:** Đọc `step.explanation`, `step.current_path`, `step.alpha`, `step.beta`, `step.is_pruned`, `step.prune_reason`, `step.siblings_evaluated`.
```python
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
```

**6. `_render_sa`:** Đọc `step.temperature`, `step.current_move`, `step.candidate_move`, `step.delta_e`, `step.accept_prob`, `step.accepted`, `step.explanation`.
```python
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
```

**7. `_render_text_only`:** Fallback hiển thị text `step.algorithm`, `step.explanation` và gọi `_render_generic_fields`.
```python
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
```

**8. `_render_generic_fields`:** Lặp qua `step.__dict__`, bỏ qua các key mặc định, hiển thị các key có kiểu dữ liệu đơn giản.
```python
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
```

**9. `_render_score_breakdown_astar`:** Đọc `step.current_node` để lấy `g`, `h`, `f`.
```python
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
```

---

#### Phần hiển thị move (tọa độ, tên quân) đang format như thế nào?
Hiện tại, trong code của `visualizer.py`, phần hiển thị move (tọa độ, tên quân) **chưa được bóc tách và format riêng biệt**.
*   Trong `_render_search_3col` (cho UCS/A*): Code lặp qua `items`. Nếu là UCS, nó trích xuất mỗi `item.get('g_cost')` và in ra `cost: {cost}`. Nếu là A*, nó trích xuất mỗi `item.get('f')` và in ra `f: {f_val:.0f}`. Với các danh sách khác, nó dùng chuỗi thô `str(item)[:20]`.
*   Trong `_render_alpha_beta`: Nó chỉ trích xuất `sib.get('value', 0)` và in `value: {val:.0f}`.
*   Trong `_render_sa`: Nó chỉ trích xuất `step.current_move.get('score', 0)` và in `Current: {curr_score:.0f}`.
=> **Kết luận:** Code visualizer hiện tại hoàn toàn bỏ qua việc truy xuất key `'move'` (tọa độ `((r1,c1),(r2,c2))`) và key `'piece_captured'` (tên quân cờ) trong các ô dữ liệu!

---

### 4. Phần Score Breakdown đang hiển thị gì? (Paste code):
Phần Score Breakdown (`_render_score_breakdown_astar`) đang hiển thị dòng công thức tổng quát phân tích chi tiết điểm số của A*: `f(n) = g(n) + h(n) = [g] + [h] = [f]`
```python
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
```

---

## === PHẦN 3: FLOW TRONG MAIN.PY ===

### 5. Khi report_mode=True:
#### AI được gọi synchronous hay vẫn dùng thread?
AI được gọi **synchronous (đồng bộ)**, chạy thẳng trên luồng chính (main thread) của game, hoàn toàn không tạo `threading.Thread`.

#### Sau khi recorder có đủ steps, game có PAUSE không apply move ngay không?
**Có.** Game lập tức dừng lại (pause). Nước đi tìm được không đưa vào `trigger_move_animation` ngay mà được cất giữ vào biến `self.pending_ai_move` để chờ người dùng bấm theo dõi từng bước visualization.

#### Khi bấm NEXT đến step cuối cùng, move được apply lên bàn cờ như thế nào?
Khi người chơi bấm NEXT ở bước cuối cùng (hoặc chế độ AUTO chạy hết danh sách step), hàm `visualizer.handle_event` (hoặc `step_controller.update`) sẽ trả về chuỗi `"finish"`. Khi nhận được tín hiệu `"finish"`, `main.py` kiểm tra biến `self.pending_ai_move`. Nếu có dữ liệu, nó sẽ gọi `self.trigger_move_animation(self.pending_ai_move[0], self.pending_ai_move[1])` để thực thi hiệu ứng di chuyển trên bàn cờ, sau đó xóa sạch recorder (`self.step_recorder.clear()`) và đặt `self.pending_ai_move = None`.

---

#### Paste toàn bộ đoạn code xử lý report_mode trong handle_bot_turns và draw:

**Trong `handle_bot_turns`:**
```python
            # Report mode: synchronous AI call with recorder
            if self.report_mode:
                # Clear recorder for new turn
                self.step_recorder.clear()
                
                # Call AI synchronously (no threading to avoid race condition)
                bot_func = AI_REGISTRY[bot_algo]
                move = bot_func(self.board, recorder=self.step_recorder)
                
                # Don't execute move yet - wait for user to step through visualization
                # Store pending move
                if move and self.step_recorder.total_steps() > 0:
                    self.pending_ai_move = move
                elif move:
                    self.trigger_move_animation(move[0], move[1])
                return
```

**Trong vòng lặp chính `run()` (phần xử lý sự kiện click & auto update):**
```python
                    # Sidebar / Visualizer click actions
                    if self.report_mode and self.step_recorder.total_steps() > 0:
                        vis_action = self.visualizer.handle_event(event, self.step_controller, self.step_recorder)
                        if vis_action == "finish" and getattr(self, 'pending_ai_move', None):
                            self.trigger_move_animation(self.pending_ai_move[0], self.pending_ai_move[1])
                            self.step_recorder.clear()
                            self.pending_ai_move = None
                            continue
```
```python
            # 2. Game Logic / Bot turns
            if self.state == "game" and not self.animation:
                if self.report_mode and self.step_recorder.total_steps() > 0:
                    if self.step_controller.update(self.step_recorder) == "finish" and getattr(self, 'pending_ai_move', None):
                        self.trigger_move_animation(self.pending_ai_move[0], self.pending_ai_move[1])
                        self.step_recorder.clear()
                        self.pending_ai_move = None
                else:
                    self.handle_bot_turns()
```

**Trong `draw_game_screen`:**
```python
        # 5. Draw Sidebar Panel or Visualizer Panel (depending on report_mode)
        red_bot = f"L{self.menu.red_bot_level + 1}: {self.menu.red_bot_algo}" if self.menu.red_bot_algo and self.menu.red_bot_algo != "Human" else "Human"
        black_bot = f"L{self.menu.black_bot_level + 1}: {self.menu.black_bot_algo}" if self.menu.black_bot_algo else ""
        
        if self.report_mode and self.step_recorder.total_steps() > 0:
            # Show Visualizer Panel
            current_step = self.step_recorder.get_current_step()
            self.visualizer.draw(self.screen, current_step, self.step_controller, self.step_recorder)
        else:
            # Show normal Sidebar
            self.sidebar.draw(
                self.screen, self.board, self.menu.game_mode,
                red_bot, black_bot, hint_move=self.hint_move, move_history=self.board.move_log, pending_move=self.pending_move,
                latest_move_index=self.latest_move_index, latest_move_flash_until=self.latest_move_flash_until
            )
```

---

## === PHẦN 4: VẤN ĐỀ HIỆN TẠI ===

### 6. Nhìn vào screenshot SA đang hiển thị:
#### Current: 5, Candidate: 5 — con số 5 này từ đâu ra trong code?
Con số `5` này chính là điểm số đánh giá bàn cờ (`score`) được trả về từ hàm `get_perspective_score(board, color)` trong `simulated_annealing_move`. 
*   Khi AI ghi bước chạy, nó lưu dữ liệu dạng: `current_move={'move': current_move, 'score': current_score}` và `candidate_move={'move': candidate, 'score': score}`.
*   Trong hàm `_render_sa`, visualizer trích xuất: `curr_score = step.current_move.get('score', 0)` và `cand_score = step.candidate_move.get('score', 0)` rồi in thẳng ra màn hình chuỗi `f"Current: {curr_score:.0f}"` và `f"Candidate: {cand_score:.0f}"`. Vì điểm số lúc đó bằng 5, màn hình hiển thị con số 5!

#### Tại sao không hiển thị tên quân và tọa độ?
Bởi vì trong hàm `_render_sa(self, surface, step, rect)` của `gui/visualizer.py`, code **hoàn toàn không truy xuất** key `'move'` (tọa độ) trong từ điển `step.current_move` hay `step.candidate_move`. Nó chỉ lấy duy nhất key `'score'`. Hơn nữa, trong `simulated_annealing_move`, thuật toán cũng chưa hề truyền tên quân cờ (như `piece_name`) vào từ điển `current_move`. Do đó giao diện hoàn toàn thiếu thông tin tọa độ và tên quân.

---

### 7. Có bất kỳ TODO, placeholder, hoặc đoạn code chưa implement nào trong visualizer không? (Paste ra nếu có):
**Có.** Trong `gui/visualizer.py`, phần lớn các thuật toán AI (tới 14/18 thuật toán) chưa có giao diện render trực quan riêng biệt mà đang bị dồn vào nhánh `fallback` text thô (gọi hàm `_render_text_only`):

**Đoạn phân nhánh chưa đầy đủ trong `draw`:**
```python
        if isinstance(step, (UCSStep, AStarStep)):
            self._render_search_3col(surface, step, content_rect)
        elif isinstance(step, AlphaBetaStep):
            self._render_alpha_beta(surface, step, content_rect)
        elif isinstance(step, SAStep):
            self._render_sa(surface, step, content_rect)
        else:
            # Fallback: text-only explanation
            self._render_text_only(surface, step, content_rect)
```

**Hạn chế nghiêm trọng trong `_render_generic_fields` (thuộc fallback):**
```python
        # Collect interesting fields
        for key, val in step.__dict__.items():
            if key in ['step_num', 'algorithm', 'explanation', 'chosen_move']:
                continue
            if isinstance(val, (int, float, str, bool)):
                fields_to_show.append((key, val))
```
**Nhận xét:** Đoạn code `if isinstance(val, (int, float, str, bool)):` đã **loại bỏ hoàn toàn** các trường dữ liệu mang tính cấu trúc `list` hoặc `dict` (như `candidates` của Greedy/Online, `neighbors` của Hill Climbing, `and_responses` của And-Or, `safe_moves` của AC3...). Kết quả là khi chạy các thuật toán này, màn hình chỉ hiện thị được mỗi dòng `explanation` mà mất sạch toàn bộ danh sách các nước đi ứng viên!
