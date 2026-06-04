from enum import Enum
from typing import TypeAlias
from dataclasses import dataclass

from pacman.maze_adapter import CellPosition
from pacman.player import Direction


class GhostMode(str, Enum):
    NORMAL = "NORMAL"


GhostColor: TypeAlias = tuple[int, int, int]


@dataclass(slots=True)
class GhostState:
    name: str
    position: CellPosition
    spawn_position: CellPosition
    color: GhostColor
    mode: GhostMode = GhostMode.NORMAL
    direction: Direction | None = None
