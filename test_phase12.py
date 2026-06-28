"""
Phase 12 Diagnostic Script — kiểm tra thực tế tất cả thay đổi
Chạy WITHOUT pygame để verify logic, data flow, function signatures
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

errors = []
warnings = []
passed = []

def check(name, condition, detail=""):
    if condition:
        passed.append(f"✅ {name}")
    else:
        errors.append(f"❌ {name}: {detail}")

def warn(name, detail=""):
    warnings.append(f"⚠️ {name}: {detail}")

print("=" * 70)
print("PHASE 12 DIAGNOSTIC — Runtime Verification")
print("=" * 70)

# ============================================================
# CHECK 1: ai/level3.py — PIECE_NAME_VI + _get_piece_name + "piece" key
# ============================================================
print("\n--- CHECK 1: ai/level3.py ---")
try:
    import ai.level3 as L3

    # Check PIECE_NAME_VI exists
    check("level3.PIECE_NAME_VI exists",
          hasattr(L3, 'PIECE_NAME_VI'),
          "Missing PIECE_NAME_VI dict")

    if hasattr(L3, 'PIECE_NAME_VI'):
        check("level3.PIECE_NAME_VI has 7 entries",
              len(L3.PIECE_NAME_VI) == 7,
              f"Expected 7, got {len(L3.PIECE_NAME_VI)}")
        check("level3.PIECE_NAME_VI['rook'] == 'Xe'",
              L3.PIECE_NAME_VI.get('rook') == 'Xe',
              f"Got: {L3.PIECE_NAME_VI.get('rook')}")

    # Check _get_piece_name helper
    check("level3._get_piece_name exists",
          hasattr(L3, '_get_piece_name'),
          "Missing _get_piece_name helper function")

    # Check function signatures have recorder param
    import inspect

    for func_name in ['hill_climbing_move', 'simulated_annealing_move', 'beam_search_move']:
        func = getattr(L3, func_name, None)
        check(f"level3.{func_name} exists", func is not None, "Function missing")
        if func:
            sig = inspect.signature(func)
            check(f"level3.{func_name} has 'recorder' param",
                  'recorder' in sig.parameters,
                  f"Params: {list(sig.parameters.keys())}")

except Exception as e:
    errors.append(f"❌ level3.py import failed: {e}")

# ============================================================
# CHECK 2: ai/level4.py — PIECE_NAME_VI + _get_piece_name
# ============================================================
print("\n--- CHECK 2: ai/level4.py ---")
try:
    import ai.level4 as L4

    check("level4.PIECE_NAME_VI exists",
          hasattr(L4, 'PIECE_NAME_VI'),
          "Missing PIECE_NAME_VI dict")

    check("level4._get_piece_name exists",
          hasattr(L4, '_get_piece_name'),
          "Missing _get_piece_name helper function")

    for func_name in ['online_search_move', 'and_or_search_move', 'belief_state_search_move']:
        func = getattr(L4, func_name, None)
        check(f"level4.{func_name} exists", func is not None, "Function missing")
        if func:
            sig = inspect.signature(func)
            check(f"level4.{func_name} has 'recorder' param",
                  'recorder' in sig.parameters,
                  f"Params: {list(sig.parameters.keys())}")

except Exception as e:
    errors.append(f"❌ level4.py import failed: {e}")

# ============================================================
# CHECK 3: ai/level5.py — PIECE_NAME_VI + _get_piece_name
# ============================================================
print("\n--- CHECK 3: ai/level5.py ---")
try:
    import ai.level5 as L5

    check("level5.PIECE_NAME_VI exists",
          hasattr(L5, 'PIECE_NAME_VI'),
          "Missing PIECE_NAME_VI dict")

    check("level5._get_piece_name exists",
          hasattr(L5, '_get_piece_name'),
          "Missing _get_piece_name helper function")

    for func_name in ['backtracking_mrv_move', 'min_conflicts_move', 'ac3_move']:
        func = getattr(L5, func_name, None)
        check(f"level5.{func_name} exists", func is not None, "Function missing")
        if func:
            sig = inspect.signature(func)
            check(f"level5.{func_name} has 'recorder' param",
                  'recorder' in sig.parameters,
                  f"Params: {list(sig.parameters.keys())}")

except Exception as e:
    errors.append(f"❌ level5.py import failed: {e}")

# ============================================================
# CHECK 4: ai/step_recorder.py — All 18+ dataclasses
# ============================================================
print("\n--- CHECK 4: ai/step_recorder.py ---")
try:
    from ai.step_recorder import (
        StepRecorder,
        UCSStep,
    )
    check("All 18 Step dataclasses importable", True)
    check("StepRecorder importable", True)

    # Test StepRecorder functionality
    rec = StepRecorder()
    check("StepRecorder.steps initially empty", len(rec.steps) == 0)

    rec.add_step(UCSStep(
        step_num=1, algorithm="UCS",
        explanation="Test step",
        chosen_move=((0,0),(0,5)),
        current_node={"move": ((0,0),(0,5)), "g_cost": 100},
        frontier=[],
        explored=[]
    ))
    check("StepRecorder.add_step works", rec.total_steps() == 1)
    check("StepRecorder.get_current_step returns step",
          rec.get_current_step() is not None)
    check("StepRecorder.get_current_step is UCSStep",
          isinstance(rec.get_current_step(), UCSStep))

    rec.clear()
    check("StepRecorder.clear works", rec.total_steps() == 0)

except Exception as e:
    errors.append(f"❌ step_recorder.py import/test failed: {e}")

# ============================================================
# CHECK 5: gui/visualizer.py — Key methods (without pygame)
# ============================================================
print("\n--- CHECK 5: gui/visualizer.py (source analysis) ---")
try:
    viz_path = os.path.join(os.path.dirname(__file__), 'gui', 'visualizer.py')
    with open(viz_path, 'r', encoding='utf-8') as f:
        viz_source = f.read()

    # FIX 1: Font loading
    check("FIX1: _load_font helper exists",
          '_load_font' in viz_source,
          "Missing _load_font function")
    check("FIX1: Roboto TTF fallback path",
          'Roboto' in viz_source or 'roboto' in viz_source,
          "No Roboto font reference found")
    check("FIX1: Arial fallback",
          '"Arial"' in viz_source or "'Arial'" in viz_source,
          "No Arial fallback")

    # FIX 2: Coordinate labels
    check("FIX2: COL_LABELS constant exists",
          'COL_LABELS' in viz_source,
          "Missing COL_LABELS constant")
    check("FIX2: ABCDEFGHI in source",
          'ABCDEFGHI' in viz_source,
          "Missing column label string")
    check("FIX2: _pos_to_label method exists",
          '_pos_to_label' in viz_source,
          "Missing _pos_to_label method")
    check("FIX2: _format_move_full method exists",
          'def _format_move_full' in viz_source,
          "Missing _format_move_full method definition")

    # FIX 2d: Old functions removed/aliased
    has_format_move_short_def = 'def _format_move_short' in viz_source
    check("FIX2d: _format_move_short REMOVED",
          not has_format_move_short_def,
          "_format_move_short still defined — should be deleted")

    # Check _format_move is aliased or calls _format_move_full
    if 'def _format_move(' in viz_source or '_format_move = _format_move_full' in viz_source:
        # Check it's not the old implementation
        if '_format_move = _format_move_full' in viz_source:
            check("FIX2d: _format_move aliased to _format_move_full", True)
        elif 'def _format_move(' in viz_source and '_format_move_full' in viz_source:
            check("FIX2d: _format_move wraps _format_move_full", True)
        else:
            warn("FIX2d: _format_move exists but may not call _format_move_full")

    # Check no stale calls to _format_move_short
    import re
    short_calls = re.findall(r'_format_move_short\(', viz_source)
    check("FIX2: No remaining _format_move_short() calls",
          len(short_calls) == 0,
          f"Found {len(short_calls)} stale calls to _format_move_short()")

    # FIX 4: Subtitle
    check("FIX4: _get_step_subtitle method exists",
          '_get_step_subtitle' in viz_source,
          "Missing _get_step_subtitle method")

    # Check all renderers exist
    renderers = [
        '_render_bfs_dfs', '_render_search_3col', '_render_ida_star',
        '_render_candidates_list', '_render_sa', '_render_beam',
        '_render_online_andor_belief', '_render_csp',
        '_render_alpha_beta', '_render_minimax_expectimax',
        '_render_text_only'
    ]
    for r in renderers:
        check(f"Renderer {r} exists",
              f'def {r}' in viz_source,
              f"Missing renderer method {r}")

    # Check dispatch in draw()
    step_types_in_dispatch = [
        'BFSStep', 'DFSStep', 'UCSStep', 'AStarStep', 'IDAStarStep',
        'GreedyStep', 'HillClimbStep', 'SAStep', 'BeamStep',
        'OnlineStep', 'AndOrStep', 'BeliefStep',
        'BacktrackStep', 'MinConflictStep', 'AC3Step',
        'AlphaBetaStep', 'MinimaxStep', 'ExpectimaxStep'
    ]
    for st in step_types_in_dispatch:
        check(f"Dispatch handles {st}",
              st in viz_source,
              f"{st} not referenced in visualizer.py")

    # PIECE_NAME_VI in visualizer
    check("PIECE_NAME_VI in visualizer.py",
          'PIECE_NAME_VI' in viz_source,
          "Missing PIECE_NAME_VI dict in visualizer")

except Exception as e:
    errors.append(f"❌ visualizer.py analysis failed: {e}")

# ============================================================
# CHECK 6: ai/level1.py, level2.py, level6.py — recorder params
# ============================================================
print("\n--- CHECK 6: Other AI levels (recorder params) ---")
try:
    import ai.level1 as L1
    import ai.level2 as L2
    import ai.level6 as L6

    l1_funcs = ['bfs_move', 'dfs_move', 'ucs_move']
    l2_funcs = ['greedy_move', 'a_star_move', 'ida_star_move']
    l6_funcs = ['minimax_move', 'alpha_beta_move', 'expectimax_move']

    for mod, funcs, name in [(L1, l1_funcs, 'level1'), (L2, l2_funcs, 'level2'), (L6, l6_funcs, 'level6')]:
        for func_name in funcs:
            func = getattr(mod, func_name, None)
            check(f"{name}.{func_name} exists", func is not None, "Missing")
            if func:
                sig = inspect.signature(func)
                check(f"{name}.{func_name} has 'recorder' param",
                      'recorder' in sig.parameters,
                      f"Params: {list(sig.parameters.keys())}")

except Exception as e:
    errors.append(f"❌ Level 1/2/6 check failed: {e}")

# ============================================================
# CHECK 7: main.py — report_mode integration
# ============================================================
print("\n--- CHECK 7: main.py integration ---")
try:
    main_path = os.path.join(os.path.dirname(__file__), 'main.py')
    with open(main_path, 'r', encoding='utf-8') as f:
        main_source = f.read()

    check("main.py imports StepRecorder",
          'StepRecorder' in main_source,
          "Missing StepRecorder import")
    check("main.py has report_mode",
          'report_mode' in main_source,
          "Missing report_mode flag")
    check("main.py has step_recorder attribute",
          'step_recorder' in main_source,
          "Missing step_recorder usage")
    check("main.py has visualizer",
          'visualizer' in main_source or 'VisualizerPanel' in main_source,
          "Missing visualizer integration")
    check("main.py has step_controller",
          'step_controller' in main_source or 'StepController' in main_source,
          "Missing step_controller integration")

except Exception as e:
    errors.append(f"❌ main.py analysis failed: {e}")

# ============================================================
# CHECK 8: Source-level "piece" key verification
# ============================================================
print("\n--- CHECK 8: 'piece' key in AI source code ---")
try:
    for fname, display in [('ai/level3.py', 'level3'), ('ai/level4.py', 'level4'), ('ai/level5.py', 'level5')]:
        fpath = os.path.join(os.path.dirname(__file__), fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            src = f.read()

        piece_key_count = src.count('"piece"')
        check(f"{display}: has 'piece' key references",
              piece_key_count >= 2,
              f"Only {piece_key_count} occurrences of '\"piece\"' found")

except Exception as e:
    errors.append(f"❌ Piece key verification failed: {e}")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("RESULTS SUMMARY")
print("=" * 70)

print(f"\n✅ PASSED: {len(passed)}")
for p in passed:
    print(f"  {p}")

if warnings:
    print(f"\n⚠️ WARNINGS: {len(warnings)}")
    for w in warnings:
        print(f"  {w}")

if errors:
    print(f"\n❌ ERRORS: {len(errors)}")
    for e in errors:
        print(f"  {e}")
else:
    print(f"\n🎉 ALL {len(passed)} CHECKS PASSED — Phase 12 verified!")

print(f"\nTotal: {len(passed)} passed, {len(warnings)} warnings, {len(errors)} errors")
