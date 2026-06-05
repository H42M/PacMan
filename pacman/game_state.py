from __future__ import annotations
from dataclasses import dataclass, field

from pacman.level import Level
from pacman.player import PlayerState, Direction
from pacman.maze_adapter import Wall, CellPosition
from pacman.game_config import GameConfig
from pacman.ghost import GhostState


@dataclass(slots=True)
class GameState:
    level: Level
    player: PlayerState
    score: int
    pacgums: set[CellPosition] = field(repr=False)
    super_pacgums: set[CellPosition] = field(repr=False)
    points_per_pacgum: int
    points_per_super_pacgum: int

    ghosts: list[GhostState]

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

        ghost_names: list[str] = ["Blinky", "Pinky", "Inky", "Clyde"]
        ghost_positions = level.ghost_spawns
        ghost_colors = [
            (255, 0, 0),      # Blinky - red
            (255, 184, 255),  # Pinky - pink
            (0, 255, 255),    # Inky - cyan
            (255, 184, 82),   # Clyde - orange
        ]
        ghosts = [
            GhostState(name, position, position, color)
            for name, position, color
            in zip(ghost_names, ghost_positions, ghost_colors, strict=True)
        ]
        return cls(level=level, player=PlayerState(level.player_spawn),
                   score=0, pacgums=pacgums,
                   super_pacgums=set(level.super_pacgum_positions),
                   points_per_pacgum=config.points_per_pacgum,
                   points_per_super_pacgum=config.points_per_super_pacgum,
                   ghosts=ghosts)

    def _get_target_position(
        self,
        position: CellPosition,
        direction: Direction,
    ) -> CellPosition | None:
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

        x, y = position
        dx, dy = movement
        target = (x + dx, y + dy)

        if target in self.level.maze.solid_positions:
            return None
        blocked = self.level.walls_at(position) & blocking_wall
        if self.level.is_inside(target) and not blocked:
            return target
        else:
            return None

    def try_move(self, direction: Direction) -> bool:
        target = self._get_target_position(self.player.position, direction)
        if target is None:
            return False
        self.player.position = target
        self.collect_at(target)
        return True

    def move_ghosts(self) -> None:
        for ghost in self.ghosts:
            best_target: CellPosition | None = None
            best_direction: Direction | None = None
            best_distance: int | None = None
            for direction in Direction:
                target = self._get_target_position(ghost.position, direction)
                if target is not None:
                    dx = target[0] - self.player.position[0]
                    dy = target[1] - self.player.position[1]
                    distance = dx * dx + dy * dy
                    if best_distance is None or distance < best_distance:
                        best_distance = distance
                        best_direction = direction
                        best_target = target
            if best_target is not None:
                ghost.direction = best_direction
                ghost.position = best_target

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
