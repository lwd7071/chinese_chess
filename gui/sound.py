# Synthesized audio effects generator for Chess moves

import threading

import pygame

# Fallback for winsound on Windows if numpy is missing
try:
    import numpy as np

    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import winsound

    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False


def play_synth_sound(sound_type):
    """
    Plays a synthesized sound effect programmatically.
    Runs asynchronously in a thread to avoid blocking Pygame game loop.
    """
    thread = threading.Thread(target=_play_sound_task, args=(sound_type,))
    thread.daemon = True
    thread.start()


def _play_sound_task(sound_type):
    # Try using pygame.sndarray with numpy first
    if HAS_NUMPY:
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=2)

            sample_rate = 22050

            if sound_type == "move":
                # Short wood block knock
                duration = 0.08
                t = np.linspace(0, duration, int(sample_rate * duration), False)
                wave = np.sin(2 * np.pi * 320 * t) * np.exp(-40 * t)
                audio = np.repeat(
                    (wave * 16384).astype(np.int16)[:, np.newaxis], 2, axis=1
                )
                sound = pygame.sndarray.make_sound(audio)
                sound.play()
                return

            elif sound_type == "capture":
                # Metal scratch capture sound
                duration = 0.15
                t = np.linspace(0, duration, int(sample_rate * duration), False)
                freqs = 700 - 450 * (t / duration)
                wave = np.sin(2 * np.pi * freqs * t) * np.exp(-18 * t)
                audio = np.repeat(
                    (wave * 16384).astype(np.int16)[:, np.newaxis], 2, axis=1
                )
                sound = pygame.sndarray.make_sound(audio)
                sound.play()
                return

            elif sound_type == "check":
                # Double high pitched beep
                duration = 0.22
                t = np.linspace(0, duration, int(sample_rate * duration), False)
                # Beep at 0-0.08s and 0.12-0.20s
                gate = (t < 0.08) | ((t > 0.12) & (t < 0.20))
                wave = np.sin(2 * np.pi * 880 * t) * gate * np.exp(-5 * t)
                audio = np.repeat(
                    (wave * 12000).astype(np.int16)[:, np.newaxis], 2, axis=1
                )
                sound = pygame.sndarray.make_sound(audio)
                sound.play()
                return
        except Exception:
            pass  # Fall back to winsound Beep if pygame mixer fails

    # Windows fallback
    if HAS_WINSOUND:
        try:
            if sound_type == "move":
                winsound.Beep(280, 80)
            elif sound_type == "capture":
                winsound.Beep(450, 150)
            elif sound_type == "check":
                winsound.Beep(880, 100)
                winsound.Beep(880, 100)
        except Exception:
            pass
