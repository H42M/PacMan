from dataclasses import dataclass
from enum import IntFlag
from typing import TypeAlias

from pacman.game_config import LevelConfig

CellPosition: TypeAlias = tuple[int, int]


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
    entry: CellPosition
    exit: CellPosition


def translate_seed(seed: int | None) -> int:
    """Convert PacMan seed values to the assigned package seed convention."""
    if seed is None:
        return 0
    return seed


def generate_maze(level: LevelConfig) -> GeneratedMaze:
    try:
        from mazegenerator.mazegenerator import MazeGenerator
    except ImportError as error:
        raise MazeGenerationError(
            "Maze generator package is not installed\nPlease run make install."
        ) from error

    try:
        maze = MazeGenerator(size=(level.width, level.height),
                             perfect=False,
                             seed=translate_seed(level.seed))
    except Exception as error:
        raise MazeGenerationError("Maze generation failed.") from error

    cells = tuple(tuple(Wall(cell) for cell in row) for row in maze.maze)
    if not cells or not cells[0]:
        raise MazeGenerationError("Maze is empty")
    first_width = len(cells[0])
    if any(len(row) != first_width for row in cells):
        raise MazeGenerationError("Maze has inconsistent widths")

    return GeneratedMaze(width=first_width,
                         height=len(cells),
                         cells=cells,
                         entry=maze.maze_entry,
                         exit=maze.maze_exit)
