from __future__ import annotations
from dataclasses import dataclass, field

from pacman.game_config import GameConfig
from pacman.maze_adapter import generate_maze, GeneratedMaze
from pacman.maze_adapter import CellPosition
from pacman.maze_adapter import Wall


@dataclass(frozen=True, slots=True)
class Level:
    """Runtime data for one generated Pac-Man level."""

    number: int
    maze: GeneratedMaze = field(repr=False)
    max_time: int
    player_spawn: CellPosition
    ghost_spawns: tuple[CellPosition, ...]
    super_pacgum_positions: tuple[CellPosition, ...]

    def is_inside(self, position: CellPosition) -> bool:
        x, y = position
        return 0 <= x < self.maze.width and 0 <= y < self.maze.height

    def walls_at(self, position: CellPosition) -> Wall:
        x, y = position
        if not self.is_inside(position):
            raise ValueError("Cell position is not inside maze.")
        return self.maze.cells[y][x]


def get_center_position(maze: GeneratedMaze) -> CellPosition:
    return (maze.width // 2, maze.height // 2)


def get_corner_positions(maze: GeneratedMaze) -> tuple[CellPosition, ...]:
    return (
        (maze.width - maze.width + 1, maze.height - maze.height + 1),
        (maze.width - maze.width + 1, maze.height - 1),
        (maze.width - 1, maze.height - maze.height + 1),
        (maze.width - 1, maze.height - 1)
    )


def build_level(config: GameConfig, level_index: int) -> Level:
    if level_index < 0 or level_index >= len(config.levels):
        raise ValueError(f"Level {level_index} not in config.")
    level_config = config.levels[level_index]
    maze = generate_maze(level_config)
    center_pos = get_center_position(maze)
    corner_pos = get_corner_positions(maze)

    return Level(
        number=level_index + 1,
        maze=maze,
        max_time=level_config.level_max_time,
        player_spawn=center_pos,
        ghost_spawns=corner_pos,
        super_pacgum_positions=corner_pos,
    )
