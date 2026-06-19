from enum import Enum
from dataclasses import dataclass

from pacman.maze_adapter import CellPosition


class Direction(str, Enum):
    """Represent a grid movement direction."""

    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


@dataclass(slots=True)
class PlayerState:
    """Store runtime state for the player."""

    position: CellPosition
    current_direction: Direction | None = None
    queued_direction: Direction | None = None
