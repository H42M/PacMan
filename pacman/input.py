from pygame import K_w, K_a, K_s, K_d
from pygame import K_UP, K_LEFT, K_DOWN, K_RIGHT

from pacman.player import Direction


def direction_from_key(key_pressed: int) -> Direction | None:
    """Return the movement direction for a keyboard key."""
    if key_pressed == K_UP or key_pressed == K_w:
        return Direction.UP
    elif key_pressed == K_a or key_pressed == K_LEFT:
        return Direction.LEFT
    elif key_pressed == K_DOWN or key_pressed == K_s:
        return Direction.DOWN
    elif key_pressed == K_RIGHT or key_pressed == K_d:
        return Direction.RIGHT
    else:
        return None
