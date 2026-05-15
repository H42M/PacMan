from dataclasses import dataclass
from enum import IntFlag
from pacman.game_config import LevelConfig


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


def translate_seed(seed: int | None) -> int:
    """Convert PacMan seed values to the assigned package seed convention."""
    if seed is None:
        return 0
    return seed


def generate_maze(level: LevelConfig) -> GeneratedMaze:
    from mazegenerator.mazegenerator import MazeGenerator

    maze = MazeGenerator(size=(level.width, level.height),
                         perfect=False,
                         seed=translate_seed(level.seed))
    cells = tuple(tuple(Wall(cell) for cell in row) for row in maze.maze)

    return GeneratedMaze(width=len(cells[0]),
                         height=len(cells),
                         cells=cells,
                         entry=maze.maze_entry,
                         exit=maze.maze_exit)
