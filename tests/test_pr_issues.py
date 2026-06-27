import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_clean_controller_class():
    import sys

    if "main" in sys.modules:
        del sys.modules["main"]
    with (
        patch("pygame.init"),
        patch("pygame.mixer.init"),
        patch("pygame.display.set_mode"),
        patch("pygame.display.set_caption"),
        patch("pygame.time.Clock"),
        patch("gui.renderer.Renderer"),
        patch("gui.sidebar.Sidebar"),
        patch("gui.menu.StartMenu"),
        patch("gui.shop.ShopScreen"),
        patch("gui.settings.SettingsScreen"),
        patch("gui.visualizer.VisualizerPanel"),
    ):
        from main import GameController

        return GameController


class TestPRIssuesReproduction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.GameController = get_clean_controller_class()

    @patch("pygame.init")
    @patch("pygame.mixer.init")
    @patch("pygame.display.set_mode")
    @patch("pygame.display.set_caption")
    @patch("pygame.time.Clock")
    @patch("gui.renderer.Renderer")
    @patch("gui.sidebar.Sidebar")
    @patch("gui.menu.StartMenu")
    @patch("gui.shop.ShopScreen")
    @patch("gui.settings.SettingsScreen")
    @patch("gui.visualizer.VisualizerPanel")
    @patch("main.GameController.draw_top_bar")
    def test_none_bot_level_no_crash_h2(self, mock_draw_top_bar, *mocks):
        """Verify that GameController.draw_game_screen does not crash when bot level is None (Fix H2)."""
        controller = self.GameController()
        controller.menu.red_bot_level = None
        controller.menu.red_bot_algo = "UCS"
        controller.menu.black_bot_level = 0
        controller.menu.black_bot_algo = "Human"

        # Mock board and components to allow drawing phase to run without invoking pygame graphics
        controller.board = MagicMock()
        controller.board.move_log = []
        controller.board.turn = "red"
        controller.renderer = MagicMock()
        controller.sidebar = MagicMock()
        controller.visualizer = MagicMock()

        # Running draw_game_screen should not raise TypeError
        try:
            controller.draw_game_screen()
        except TypeError as e:
            self.fail(f"GameController.draw_game_screen crashed with TypeError: {e}")

    @patch("pygame.init")
    @patch("pygame.mixer.init")
    @patch("pygame.display.set_mode")
    @patch("pygame.display.set_caption")
    @patch("pygame.time.Clock")
    @patch("gui.renderer.Renderer")
    @patch("gui.sidebar.Sidebar")
    @patch("gui.menu.StartMenu")
    @patch("gui.shop.ShopScreen")
    @patch("gui.settings.SettingsScreen")
    @patch("gui.visualizer.VisualizerPanel")
    @patch("main.GameController.draw_top_bar")
    def test_single_sidebar_draw_h1(self, mock_draw_top_bar, *mocks):
        """Verify that GameController.draw_game_screen draws the sidebar exactly once when report_mode is False (Fix H1)."""
        controller = self.GameController()
        controller.report_mode = False
        controller.board = MagicMock()
        controller.board.move_log = []

        # Mock components
        controller.renderer = MagicMock()
        controller.sidebar = MagicMock()
        controller.visualizer = MagicMock()

        controller.draw_game_screen()

        # Check call count - should be exactly 1
        draw_count = controller.sidebar.draw.call_count
        print(f"[VERIFY-H1] Sidebar draw called {draw_count} times")
        self.assertEqual(
            draw_count,
            1,
            f"Sidebar draw should be called exactly once, got {draw_count}",
        )

    @patch("pygame.init")
    @patch("pygame.mixer.init")
    @patch("pygame.display.set_mode")
    @patch("pygame.display.set_caption")
    @patch("pygame.time.Clock")
    @patch("gui.renderer.Renderer")
    @patch("gui.sidebar.Sidebar")
    @patch("gui.menu.StartMenu")
    @patch("gui.shop.ShopScreen")
    @patch("gui.settings.SettingsScreen")
    @patch("gui.visualizer.VisualizerPanel")
    def test_single_event_handling_h3(self, *mocks):
        """Verify that a single sidebar click event triggers handle_event exactly once when report_mode is False (Fix H3)."""
        controller = self.GameController()
        controller.state = "game"
        controller.report_mode = False
        controller.animation = None

        # Mock board and pygame screen / drawing
        controller.board = MagicMock()
        controller.board.history = []
        controller.board.turn = "red"
        controller.draw_game_screen = MagicMock()

        # Mock pygame event
        mock_event = MagicMock()
        mock_event.type = (
            5  # Arbitrary event type that is NOT pygame.QUIT or pygame.VIDEORESIZE
        )

        # Mock handle_event
        controller.sidebar.handle_event = MagicMock(return_value=None)

        # We need to mock pygame.event.get() to yield our event
        with (
            patch("pygame.event.get", return_value=[mock_event]),
            patch("pygame.display.flip", side_effect=KeyboardInterrupt),
            patch("pygame.mouse.get_pos", return_value=(0, 0)),
            patch("main.play_synth_sound"),
        ):
            try:
                controller.run()
            except KeyboardInterrupt:
                pass

        handle_count = controller.sidebar.handle_event.call_count
        print(f"[VERIFY-H3] sidebar.handle_event called {handle_count} times")
        self.assertEqual(
            handle_count,
            1,
            f"sidebar.handle_event should be called exactly once, got {handle_count}",
        )


if __name__ == "__main__":
    unittest.main()
