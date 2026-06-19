from enum import Enum
from typing import TypeAlias
from dataclasses import dataclass

from pacman.maze_adapter import CellPosition
from pacman.player import Direction


class GhostMode(str, Enum):
    """Represent a ghost's gameplay mode."""

    NORMAL = "NORMAL"
    FRIGHTENED = "FRIGHTENED"
    DEAD = "DEAD"


GhostColor: TypeAlias = tuple[int, int, int]


@dataclass(slots=True)
class GhostState:
    """Store runtime state for one ghost."""

    name: str
    position: CellPosition
    spawn_position: CellPosition
    color: GhostColor
    mode: GhostMode = GhostMode.NORMAL
    direction: Direction | None = None
    respawn_timer_ms: int = 0
