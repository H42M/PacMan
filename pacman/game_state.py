from __future__ import annotations
from dataclasses import dataclass, field

from pacman.level import Level
from pacman.player import PlayerState, Direction
from pacman.maze_adapter import Wall, CellPosition
from pacman.game_config import GameConfig


@dataclass(slots=True)
class GameState:
    level: Level
    player: PlayerState
    score: int
    pacgums: set[CellPosition] = field(repr=False)
    super_pacgums: set[CellPosition] = field(repr=False)
    points_per_pacgum: int
    points_per_super_pacgum: int

    @classmethod
    def from_level(cls, config: GameConfig, level: Level) -> GameState:
        reserved_cells: set[CellPosition] = {
            level.player_spawn,
            *level.ghost_spawns,
            *level.super_pacgum_positions,
            *level.maze.solid_positions,
        }
        pacgums: set[CellPosition] = {
            (x, y)
            for y, row in enumerate(level.maze.cells)
            for x in range(len(row))
            if (x, y) not in reserved_cells
        }
        return cls(level=level, player=PlayerState(level.player_spawn),
                   score=0, pacgums=pacgums,
                   super_pacgums=set(level.super_pacgum_positions),
                   points_per_pacgum=config.points_per_pacgum,
                   points_per_super_pacgum=config.points_per_super_pacgum,)

    def try_move(self, direction: Direction) -> bool:
        if direction == Direction.UP:
            movement = (0, -1)
            blocking_wall = Wall.NORTH
        elif direction == Direction.DOWN:
            movement = (0, 1)
            blocking_wall = Wall.SOUTH
        elif direction == Direction.LEFT:
            movement = (-1, 0)
            blocking_wall = Wall.WEST
        elif direction == Direction.RIGHT:
            movement = (1, 0)
            blocking_wall = Wall.EAST
        else:
            raise ValueError("Direction is incorrect.")

        x, y = self.player.position
        dx, dy = movement
        new_position = (x + dx, y + dy)

        blocked = self.level.walls_at(self.player.position) & blocking_wall
        if (self.level.is_inside(new_position) and not blocked):
            self.player.position = new_position
            self.collect_at(new_position)
            return True
        else:
            return False

    def collect_at(self, position: CellPosition) -> None:
        if not self.level.is_inside(position):
            return
        if position in self.pacgums:
            self.pacgums.remove(position)
            self.score += self.points_per_pacgum
        elif position in self.super_pacgums:
            self.super_pacgums.remove(position)
            self.score += self.points_per_super_pacgum

    def has_collected_all_pacgums(self) -> bool:
        return not self.pacgums and not self.super_pacgums
