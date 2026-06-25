# Pull Request Review Report (Local Review)

**Date**: 2026-06-25  
**Review Type**: Local-only review (inspected branch diffs against merge base `635cb9c` due to host system lacking the `gh` CLI)  
**Branch**: `tri/exp-system` → `dev` / `main`  
**Decision**: **APPROVE** ✅ (0 Critical, 0 High, 0 Medium, 3 Low issues remaining)

---

## ⚠️ Warning: Local-Only Review
This review was conducted locally by analyzing git diffs against the merge base commit `635cb9c` and verifying the local environment, as the GitHub CLI (`gh`) is not installed on this host machine. Remote PR retrieval and automated comment posting were skipped.

---

## Summary of Changes
This branch implements the EXP system, match history logging, profile customization, and visual UI refinements:
1. **EXP System & Formula**: Implements a standard Xiangqi piece value representation to award EXP to the winner based on remaining pieces ($100 + \text{score}/2$) where:
   - Rook (`R`) = 90, Cannon (`C`) = 45, Horse (`H`) = 45, Elephant (`E`) = 20, Advisor (`A`) = 20, Pawn (`P`) = 10, General (`G`) = 0.
2. **Profile & History Screen**: Implements `gui/settings.py` for user details modification (Name, Country, Birthday) and displays match history records loaded/saved from `profile.json`.
3. **AI Search Metrics Controls**: Modifies search parameters (`sim_nodes`, `sim_frontier`, `sim_explored`) to slowly grow while the Bot is thinking and freeze immediately when the human is thinking or when the game is over.
4. **Dual Dropdown Controls**: Renders red and black bot level dropdowns side-by-side in Bot vs Bot mode with elegant text truncation (`...`) to prevent overflow.
5. **Defensive UI & Rendering**: Includes outline font positioning centering using `get_bounding_rect` to prevent square glyph alignment issues, and safeguards against `None` bot level references.
6. **Test Isolation Fix**: Fixes a test isolation failure in `tests/test_main_thread_safety.py` by clearing `sys.modules['main']` before importing the patched class, preventing font library initialization conflicts.

---

## Findings & Resolutions

### CRITICAL
*None.*

---

### HIGH
*None.*

---

### MEDIUM
*None.*

---

### LOW / ADVISORY

#### L1 — Profile Birthday Format Validation
* **Status**: **Advisory**
* **Finding**: `gui/settings.py` allows editing the birthday field without executing strict date format checks. A user can type invalid date formats (e.g. `99/99/9999`) or random printable characters.
* **Recommendation**: While this is low risk (simple profile display), adding a basic date format validator or using regex checks on saving would enhance profile data integrity.

#### L2 — Sound Mixer Warmup / Fallback Warnings
* **Status**: **Advisory**
* **Finding**: `main.py` has a try-except fallback when initializing `pygame.mixer` which correctly prints a warning if audio initialization fails. This is good defensive design for headless test runs.

#### L3 — Level-Up EXP Overflow
* **Status**: **Advisory**
* **Finding**: In `SettingsScreen.add_match_record()`, the level-up loop uses a while loop `while self.data["exp"] >= self.data["level"] * 500: ...` to handle multiple levels if a huge amount of EXP is earned at once. This works correctly but can scale infinitely. Make sure to watch out for potential integer overflows if extremely large EXP values are injected.

---

## Verification Plan

### Automated Tests
All 49 unit and thread safety tests pass successfully:
```powershell
venv\Scripts\python -m unittest discover tests
```
* **Result**: `OK (49 tests in 0.110s)`

### Manual Verification
1. Open settings panel, modify fields (Name, Country, Birthday) and hit `Enter` to verify it persists to `profile.json`.
2. Check that the level progress bar scales correctly with EXP.
3. Start a Human vs Bot or Bot vs Bot game, and verify that simulated metrics (Node, Frontier, Explored) freeze when the Human is thinking.
4. Verify the side-by-side dropdown lists in Bot vs Bot match setups.
