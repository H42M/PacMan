from dataclasses import dataclass
from enum import IntFlag
from typing import TypeAlias

from pacman.game_config import LevelConfig

CellPosition: TypeAlias = tuple[int, int]


FT_PATTERN: tuple[tuple[int, ...], ...] = (
    (1, 0, 0, 0, 1, 1, 1),
    (1, 0, 0, 0, 0, 0, 1),
    (1, 1, 1, 0, 1, 1, 1),
    (0, 0, 1, 0, 1, 0, 0),
    (0, 0, 1, 0, 1, 1, 1),
)


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
    solid_positions: tuple[CellPosition, ...]

    def get_cell_wall(self, cell: tuple[int, int], direction: str) -> bool:
        x, y = cell
        wall = self.cells[y][x]

        dir_map = {
            'N': Wall.NORTH,
            'E': Wall.EAST,
            'S': Wall.SOUTH,
            'W': Wall.WEST,
        }

        try:
            return bool(wall & dir_map[direction.upper()])
        except KeyError:
            raise ValueError(
                f"Invalid direction '{direction}'. "
                "Expected N, E, S or W."
            )


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
    width = first_width
    height = len(cells)
    solid_positions = get_generator_solid_positions(width, height)

    return GeneratedMaze(
        width=width,
        height=height,
        cells=cells,
        entry=maze.maze_entry,
        exit=maze.maze_exit,
        solid_positions=solid_positions,
    )


def get_generator_solid_positions(
        width: int, height: int) -> tuple[CellPosition, ...]:
    pattern_height = len(FT_PATTERN)
    pattern_width = len(FT_PATTERN[0])

    if pattern_height * 2 > height or pattern_width * 2 > width:
        return ()

    offset_y = (height - pattern_height) // 2
    offset_x = (width - pattern_width) // 2

    return tuple(
        (offset_x + x, offset_y + y)
        for y, row in enumerate(FT_PATTERN)
        for x, value in enumerate(row)
        if value == 1
    )
