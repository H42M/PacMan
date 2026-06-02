from __future__ import annotations
from dataclasses import dataclass

from pacman.level import Level
from pacman.player import PlayerState, Direction
from pacman.maze_adapter import Wall, CellPosition


@dataclass(slots=True)
class GameState:
    level: Level
    player: PlayerState
    score: int
    pacgums: set[CellPosition]
    super_pacgums: set[CellPosition]

    @classmethod
    def from_level(cls, level: Level) -> GameState:
        reserved_cells = {level.player_spawn, *level.super_pacgum_positions}
        pacgums = set(level.maze.cells) - reserved_cells
        return cls(level=level, player=PlayerState(level.player_spawn),
                   score=0, pacgums= pacgums,
                   super_pacgums=set(level.super_pacgum_positions))

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
            return True
        else:
            return False
