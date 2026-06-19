from __future__ import annotations
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


DIRECTIONS = (
    (Wall.NORTH, 0, -1, Wall.SOUTH),
    (Wall.EAST, 1, 0, Wall.WEST),
    (Wall.SOUTH, 0, 1, Wall.NORTH),
    (Wall.WEST, -1, 0, Wall.EAST),
)


DirectionInfo: TypeAlias = tuple[Wall, int, int, Wall]


@dataclass(frozen=True, slots=True)
class GeneratedMaze:
    """Immutable maze data generated for one PacMan level."""

    width: int
    height: int
    cells: tuple[tuple[Wall, ...], ...]
    entry: CellPosition
    exit: CellPosition
    solid_positions: tuple[CellPosition, ...]


def translate_seed(seed: int | None) -> int:
    """Convert PacMan seed values to the assigned package seed convention."""
    if seed is None:
        return 0
    return seed


def generate_maze(level: LevelConfig) -> GeneratedMaze:
    """Generate and normalize a maze for a level."""
    try:
        from mazegenerator.mazegenerator import MazeGenerator
    except ImportError as error:
        raise MazeGenerationError(
            "Maze generator package is not installed\nPlease run make install."
        ) from error

    try:
        maze = MazeGenerator(size=(level.width, level.height),
                             perfect=False,
                             entry_cell=(0, 0),
                             exit_cell=(0, 1),
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

    generated_maze = GeneratedMaze(
        width=width,
        height=height,
        cells=cells,
        entry=maze.maze_entry,
        exit=maze.maze_exit,
        solid_positions=solid_positions,
    )
    return clean_dead_ends(generated_maze)


def is_inside(width: int, height: int, position: CellPosition) -> bool:
    """Return whether a position is inside a rectangle."""
    x, y = position
    return 0 <= x < width and 0 <= y < height


def is_border(position: CellPosition, maze: GeneratedMaze) -> bool:
    """Return whether a position is on the maze border."""
    x, y = position
    return (
        x == 0
        or y == 0
        or x == maze.width - 1
        or y == maze.height - 1
    )


def is_solid(maze: GeneratedMaze, position: CellPosition) -> bool:
    """Return whether a position is marked as solid."""
    return position in maze.solid_positions


def is_playable_internal_cell(
        maze: GeneratedMaze, position: CellPosition) -> bool:
    """Return whether a position is playable and not on the border."""
    return (
        is_inside(maze.width, maze.height, position)
        and not is_border(position, maze)
        and not is_solid(maze, position)
    )


def count_usable_exits(
        cells: list[list[Wall]],
        maze: GeneratedMaze,
        position: CellPosition) -> int:
    """Count usable exits from a maze cell."""
    x, y = position
    walls = cells[y][x]
    usable_exits = 0

    for wall, dx, dy, _opposite_wall in DIRECTIONS:
        if walls & wall:
            continue

        neighbor = (x + dx, y + dy)
        if not is_playable_internal_cell(maze, neighbor):
            continue

        usable_exits += 1

    return usable_exits


def find_wall_to_open(cells: list[list[Wall]],
                      maze: GeneratedMaze,
                      position: CellPosition) -> DirectionInfo | None:
    """Find a neighboring wall that can be opened."""
    x, y = position
    walls = cells[y][x]
    for wall, dx, dy, opposite_wall in DIRECTIONS:
        if not (wall & walls):
            continue
        neighbor = (x + dx, y + dy)
        if not is_playable_internal_cell(maze, neighbor):
            continue
        return (wall, dx, dy, opposite_wall)
    return None


def open_wall_between(
        cells: list[list[Wall]],
        position: CellPosition,
        direction: DirectionInfo) -> None:
    """Open a wall between a cell and its neighbor."""
    x, y = position
    wall, dx, dy, opposite_wall = direction
    cells[y][x] &= ~wall
    cells[y + dy][x + dx] &= ~opposite_wall


def clean_dead_ends(generated_maze: GeneratedMaze) -> GeneratedMaze:
    """Open selected walls to reduce dead ends."""
    maze = generated_maze
    cells = [list(row) for row in maze.cells]
    for y, row in enumerate(cells):
        for x, walls in enumerate(row):
            position = (x, y)
            if not is_playable_internal_cell(maze, position):
                continue
            if count_usable_exits(cells, maze, position) != 1:
                continue
            direction = find_wall_to_open(cells, maze, position)
            if direction is None:
                continue
            open_wall_between(cells, position, direction)

    return GeneratedMaze(
        width=maze.width,
        height=maze.height,
        cells=tuple(tuple(row)for row in cells),
        entry=maze.entry,
        exit=maze.exit,
        solid_positions=maze.solid_positions
    )


def get_generator_solid_positions(
        width: int, height: int) -> tuple[CellPosition, ...]:
    """Return solid positions reserved from the generator pattern."""
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
