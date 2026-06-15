import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import threading

# Adjust path to find modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock pygame before importing GameController
with patch('pygame.init'), \
     patch('pygame.mixer.init'), \
     patch('pygame.display.set_mode'), \
     patch('pygame.display.set_caption'), \
     patch('pygame.time.Clock'), \
     patch('gui.renderer.Renderer'), \
     patch('gui.sidebar.Sidebar'), \
     patch('gui.menu.StartMenu'):
    from main import GameController

class TestThreadSafety(unittest.TestCase):
    @patch('pygame.init')
    @patch('pygame.mixer.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('gui.renderer.Renderer')
    @patch('gui.sidebar.Sidebar')
    @patch('gui.menu.StartMenu')
    def test_controller_has_ai_lock(self, *mocks):
        """Verify that GameController has an ai_lock initialized."""
        controller = GameController()
        self.assertTrue(hasattr(controller, 'ai_lock'), "GameController should have an ai_lock attribute")
        self.assertIsInstance(controller.ai_lock, type(threading.Lock()))

    @patch('pygame.init')
    @patch('pygame.mixer.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('gui.renderer.Renderer')
    @patch('gui.sidebar.Sidebar')
    @patch('gui.menu.StartMenu')
    def test_calculate_uses_lock(self, *mocks):
        """Verify that the background calculation thread acquires the lock when writing ai_result."""
        controller = GameController()
        
        # Initialize lock attribute if it exists
        mock_lock = MagicMock()
        controller.ai_lock = mock_lock
        
        controller.menu.game_mode = "human_vs_bot"
        controller.board = MagicMock()
        controller.board.turn = 'black'
        controller.sidebar.get_bot_speed_delay.return_value = 0.0
        controller.renderer.get_xy.return_value = (0, 0)
        
        with patch('main.has_lost', return_value=False), \
             patch('main.AI_REGISTRY', {'test_bot': lambda b: ((9, 0), (9, 1))}):
            controller.menu.black_bot_algo = 'test_bot'
            
            # Capture the thread when it's started by patching thread creation/start
            started_thread = None
            original_start = threading.Thread.start
            def mock_start(self_thread):
                nonlocal started_thread
                started_thread = self_thread
                original_start(self_thread)
                
            with patch.object(threading.Thread, 'start', mock_start):
                controller.handle_bot_turns()
            
            self.assertIsNotNone(started_thread, "AI calculation thread should have been started")
            started_thread.join()
            
            # The calculation should have entered/exited the lock to set self.ai_result
            self.assertTrue(mock_lock.__enter__.called, "Lock should be acquired during calculation result assignment")

    @patch('pygame.init')
    @patch('pygame.mixer.init')
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    @patch('gui.renderer.Renderer')
    @patch('gui.sidebar.Sidebar')
    @patch('gui.menu.StartMenu')
    def test_get_result_uses_lock(self, *mocks):
        """Verify that the main thread acquires the lock when reading and clearing ai_result."""
        controller = GameController()
        
        controller.board = MagicMock()
        controller.board.turn = 'black'
        controller.menu.game_mode = "human_vs_bot"
        controller.menu.black_bot_algo = 'test_bot'
        controller.sidebar.get_bot_speed_delay.return_value = 0.0
        controller.renderer.get_xy.return_value = (0, 0)
        
        controller.ai_thread = MagicMock()
        controller.ai_thread.is_alive.return_value = False
        controller.ai_result = ((9, 0), (9, 1))
        
        mock_lock = MagicMock()
        controller.ai_lock = mock_lock
        
        controller.handle_bot_turns()
        
        # Verify lock was acquired when reading/clearing ai_result
        self.assertTrue(mock_lock.__enter__.called, "Lock should be acquired when accessing and clearing ai_result")
        self.assertIsNone(controller.ai_result)

if __name__ == '__main__':
    unittest.main()
