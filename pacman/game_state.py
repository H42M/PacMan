from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum

from pacman.level import Level
from pacman.player import PlayerState, Direction
from pacman.maze_adapter import Wall, CellPosition
from pacman.game_config import GameConfig
from pacman.ghost import GhostState


class GameOutcome(str, Enum):
    PLAYING = "PLAYING"
    LEVEL_CLEARED = "LEVEL_CLEARED"
    GAME_OVER = "GAME_OVER"


@dataclass(slots=True)
class GameState:
    level: Level
    lives: int
    outcome: GameOutcome
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
        return cls(level=level,
                   lives=config.lives,
                   outcome=GameOutcome.PLAYING,
                   player=PlayerState(level.player_spawn),
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

    def queue_player_direction(self, direction: Direction) -> None:
        self.player.queued_direction = direction

    def advance_player(self) -> None:
        if self.player.queued_direction is not None:
            target = self._get_target_position(self.player.position,
                                               self.player.queued_direction)
            if target is not None:
                self.player.current_direction = self.player.queued_direction
                self.player.queued_direction = None
                self.player.position = target
                self.collect_at(target)
                return
        if self.player.current_direction is not None:
            target = self._get_target_position(
                self.player.position,
                self.player.current_direction)
            if target is not None:
                self.player.position = target
                self.collect_at(target)

    def collect_at(self, position: CellPosition) -> None:
        if not self.level.is_inside(position):
            return
        if position in self.pacgums:
            self.pacgums.remove(position)
            self.score += self.points_per_pacgum
        elif position in self.super_pacgums:
            self.super_pacgums.remove(position)
            self.score += self.points_per_super_pacgum

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

    def respawn_entities(self) -> None:
        self.player.position = self.level.player_spawn
        self.player.current_direction = None
        self.player.queued_direction = None

        for ghost in self.ghosts:
            ghost.position = ghost.spawn_position
            ghost.direction = None

    def handle_player_ghost_collision(self) -> None:
        if self.outcome is not GameOutcome.PLAYING:
            return
        if any(self.player.position == ghost.position
               for ghost in self.ghosts):
            self.lives -= 1
            if self.lives <= 0:
                self.outcome = GameOutcome.GAME_OVER
            else:
                self.respawn_entities()

    def has_collected_all_pacgums(self) -> bool:
        return not self.pacgums and not self.super_pacgums

    def debug_collect_all_pacgums(self) -> None:
        self.pacgums.clear()
        self.super_pacgums.clear()
