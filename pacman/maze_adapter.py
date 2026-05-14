from dataclasses import dataclass
from enum import IntFlag


class MazeGenerationError(Exception):
    """Raised when maze generation fails."""


class Wall(IntFlag):
    """Wall bit flags used by the assigned maze generator."""

    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    ALL = NORTH | EAST | SOUTH | WEST


@dataclass(frozen=True, slots=True)
class GeneratedMaze:
    """Immutable maze data generated for one PacMan level."""

    width: int
    height: int
    cells: tuple[tuple[Wall, ...], ...]
    entry: tuple[int, int]
    exit: tuple[int, int]