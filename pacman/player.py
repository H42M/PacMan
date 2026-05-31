from enum import Enum
from dataclasses import dataclass

from pacman.maze_adapter import CellPosition


class Direction(str, Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


@dataclass(slots=True)
class PlayerState:
    position: CellPosition
