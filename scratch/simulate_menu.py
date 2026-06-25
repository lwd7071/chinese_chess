import sys
import os
import pygame

# Append current working directory (project root) to sys.path
sys.path.append(os.getcwd())

# Set SDL to run headlessly so it doesn't open a window during test
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from main import GameController

def test_menu_click_bot_vs_bot():
    controller = GameController()
    print("GameController initialized successfully.")
    
    # Simulate clicking on "Bot dau Bot"
    btn = controller.menu.btn_mode_bot
    click_pos = (btn.centerx, btn.centery)
    print(f"Simulating click on 'Bot dau Bot' at {click_pos}")
    
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=click_pos)
    res = controller.menu.handle_event(event)
    print(f"menu.handle_event returned: {res}, menu state: {controller.menu.state}")
    
    # Draw the menu
    surface = pygame.Surface((controller.width, controller.height))
    controller.menu.draw(surface)
    print("menu.draw completed successfully.")
    
    # Choose level 1 (index 0) for Red bot
    level_rect = controller.menu.level_rects[0]
    click_pos = (level_rect.centerx, level_rect.centery)
    print(f"Simulating click on Red Level 1 at {click_pos}")
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=click_pos)
    controller.menu.handle_event(event)
    print(f"menu state: {controller.menu.state}, selected red level: {controller.menu.red_bot_level}")
    
    # Click the seal button to go to algo selection for Red
    seal_pos = (controller.menu.seal_cx, controller.menu.seal_cy)
    print(f"Simulating click on Seal at {seal_pos}")
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=seal_pos)
    controller.menu.handle_event(event)
    print(f"menu state: {controller.menu.state}")
    
    # Choose first algorithm for Red
    algo_rect = controller.menu.algo_btn_rects[0]
    click_pos = (algo_rect.centerx, algo_rect.centery)
    print(f"Simulating click on Red Algorithm 1 at {click_pos}")
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=click_pos)
    controller.menu.handle_event(event)
    print(f"menu state: {controller.menu.state}")
    
    # Choose level 1 (index 0) for Black bot
    level_rect = controller.menu.level_rects[0]
    click_pos = (level_rect.centerx, level_rect.centery)
    print(f"Simulating click on Black Level 1 at {click_pos}")
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=click_pos)
    controller.menu.handle_event(event)
    print(f"menu state: {controller.menu.state}, selected black level: {controller.menu.black_bot_level}")
    
    # Click the seal button to go to algo selection for Black
    print(f"Simulating click on Seal at {seal_pos}")
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=seal_pos)
    controller.menu.handle_event(event)
    print(f"menu state: {controller.menu.state}")
    
    # Choose first algorithm for Black
    click_pos = (algo_rect.centerx, algo_rect.centery)
    print(f"Simulating click on Black Algorithm 1 at {click_pos}")
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=click_pos)
    res = controller.menu.handle_event(event)
    print(f"menu.handle_event returned: {res}")
    
    if res == "game":
        print("Starting game...")
        controller.start_new_game()
        controller.state = "game"
        print("Game started. Drawing game screen...")
        controller.draw_game_screen()
        print("Game screen drawn successfully.")

if __name__ == '__main__':
    try:
        test_menu_click_bot_vs_bot()
        print("All simulation steps PASSED with no exceptions.")
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(1)
