from __future__ import annotations
from dataclasses import dataclass, field

from pacman.config_loader import GameConfig
from pacman.maze_adapter import generate_maze, GeneratedMaze
from pacman.maze_adapter import CellPosition


@dataclass(frozen=True, slots=True)
class Level:
    """Runtime data for one generated Pac-Man level."""

    number: int
    maze: GeneratedMaze = field(repr=False)
    max_time: int
    player_spawn: CellPosition
    ghost_spawns: tuple[CellPosition, ...]
    super_pacgum_positions: tuple[CellPosition, ...]


def get_center_position(maze: GeneratedMaze) -> CellPosition:
    return (maze.width // 2, maze.height // 2)


def get_corner_positions(
                            maze: GeneratedMaze) -> tuple[CellPosition, ...]:
    return (
        (maze.width - maze.width + 1, maze.height - maze.height + 1),
        (maze.width - maze.width + 1, maze.height - 1),
        (maze.width - 1, maze.height - maze.height + 1),
        (maze.width - 1, maze.height - 1)
    )


def build_level(config: GameConfig, level_index: int) -> Level:
    try:
        level_config = config.levels[level_index]
        maze = generate_maze(level_config)
        center_pos = get_center_position(maze)
        corner_pos = get_corner_positions(maze)
    except (ValueError, IndexError) as error:
        raise ValueError from error

    return Level(
        number=level_index + 1,
        maze=maze,
        max_time=level_config.level_max_time,
        player_spawn=center_pos,
        ghost_spawns=corner_pos,
        super_pacgum_positions=corner_pos,
    )
