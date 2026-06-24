# Easing functions for smooth motion design (Pygame animations)
import math

def ease_out_cubic(t):
    """GSAP Power3.easeOut equivalent"""
    t = max(0.0, min(1.0, t))
    return 1.0 - pow(1.0 - t, 3)

def ease_out_back(t):
    """GSAP Back.easeOut — has a small overshoot for a weight/physics feel"""
    t = max(0.0, min(1.0, t))
    c1 = 1.70158
    c3 = c1 + 1.0
    return 1.0 + c3 * pow(t - 1.0, 3) + c1 * pow(t - 1.0, 2)

def ease_out_quad(t):
    t = max(0.0, min(1.0, t))
    return 1.0 - (1.0 - t) * (1.0 - t)

def ease_in_out_quad(t):
    t = max(0.0, min(1.0, t))
    if t < 0.5:
        return 2.0 * t * t
    else:
        return 1.0 - pow(-2.0 * t + 2.0, 2) / 2.0
