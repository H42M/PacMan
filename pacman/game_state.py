from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum

from pacman.level import Level
from pacman.player import PlayerState, Direction
from pacman.maze_adapter import CellPosition
from pacman.game_config import GameConfig
from pacman.ghost import GhostState, GhostMode
from pacman.ghost_ai import choose_normal_ghost_step
from pacman.navigation import get_direction_between, get_target_position


class GameOutcome(str, Enum):
    PLAYING = "PLAYING"
    LEVEL_CLEARED = "LEVEL_CLEARED"
    GAME_OVER = "GAME_OVER"


class GameplayPhase(str, Enum):
    PLAYING = "PLAYING"
    PLAYER_DYING = "PLAYER_DYING"


@dataclass(slots=True)
class GameState:
    level: Level
    lives: int
    remaining_time: int
    outcome: GameOutcome
    phase: GameplayPhase
    player: PlayerState
    score: int
    pacgums: set[CellPosition] = field(repr=False)
    super_pacgums: set[CellPosition] = field(repr=False)
    points_per_pacgum: int
    points_per_super_pacgum: int
    ghosts: list[GhostState]
    frightened_timer_ms: int
    ghost_respawn_timer_ms: int
    points_per_ghost: int

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
                   remaining_time=level.max_time,
                   outcome=GameOutcome.PLAYING,
                   phase=GameplayPhase.PLAYING,
                   player=PlayerState(level.player_spawn),
                   score=0, pacgums=pacgums,
                   super_pacgums=set(level.super_pacgum_positions),
                   points_per_pacgum=config.points_per_pacgum,
                   points_per_super_pacgum=config.points_per_super_pacgum,
                   ghosts=ghosts,
                   frightened_timer_ms=0,
                   ghost_respawn_timer_ms=10000,
                   points_per_ghost=config.points_per_ghost)

    def timer_tick(self) -> None:
        if (self.outcome is GameOutcome.PLAYING and
                self.phase is GameplayPhase.PLAYING):
            self.remaining_time -= 1
            if self.remaining_time <= 0:
                self.remaining_time = 0
                self.outcome = GameOutcome.GAME_OVER

    def tick_ghost_timers(self, elapsed_ms: int) -> None:
        if self.phase is not GameplayPhase.PLAYING:
            return
        if self.frightened_timer_ms > 0:
            self.frightened_timer_ms -= elapsed_ms
            if self.frightened_timer_ms <= 0:
                self.frightened_timer_ms = 0
                for ghost in self.ghosts:
                    if ghost.mode is GhostMode.FRIGHTENED:
                        ghost.mode = GhostMode.NORMAL
        for ghost in self.ghosts:
            if ghost.mode is GhostMode.DEAD:
                ghost.respawn_timer_ms -= elapsed_ms
                if ghost.respawn_timer_ms <= 0:
                    ghost.respawn_timer_ms = 0
                    ghost.position = ghost.spawn_position
                    ghost.direction = None
                    ghost.mode = (GhostMode.FRIGHTENED
                                  if self.frightened_timer_ms > 0
                                  else GhostMode.NORMAL)

    def _get_target_position(
        self,
        position: CellPosition,
        direction: Direction,
    ) -> CellPosition | None:
        return get_target_position(self.level, position, direction)

    def queue_player_direction(self, direction: Direction) -> None:
        if self.phase is not GameplayPhase.PLAYING:
            return
        self.player.queued_direction = direction

    def advance_player(self) -> None:
        if self.phase is not GameplayPhase.PLAYING:
            return
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

    def activate_frightened_mode(self) -> None:
        self.frightened_timer_ms = 10000
        for ghost in self.ghosts:
            if ghost.mode is not GhostMode.DEAD:
                ghost.mode = GhostMode.FRIGHTENED

    def collect_at(self, position: CellPosition) -> None:
        if not self.level.is_inside(position):
            return
        if position in self.pacgums:
            self.pacgums.remove(position)
            self.score += self.points_per_pacgum
        elif position in self.super_pacgums:
            self.super_pacgums.remove(position)
            self.score += self.points_per_super_pacgum
            self.activate_frightened_mode()

    def _choose_frightened_ghost_step(
            self, ghost: GhostState,
    ) -> CellPosition | None:
        best_target: CellPosition | None = None
        best_distance: int | None = None

        for direction in Direction:
            target = self._get_target_position(ghost.position, direction)
            if target is None:
                continue

            dx = target[0] - self.player.position[0]
            dy = target[1] - self.player.position[1]
            distance = dx * dx + dy * dy

            if best_distance is None or distance > best_distance:
                best_distance = distance
                best_target = target

        return best_target

    def move_ghosts(self) -> None:
        if self.phase is not GameplayPhase.PLAYING:
            return

        for ghost in self.ghosts:
            if ghost.mode is GhostMode.DEAD:
                continue

            if ghost.mode is GhostMode.NORMAL:
                next_position = choose_normal_ghost_step(
                    ghost,
                    self.ghosts,
                    self.player,
                    self.level,
                )
            else:
                next_position = self._choose_frightened_ghost_step(ghost)

            if next_position is None:
                continue

            ghost.direction = get_direction_between(
                ghost.position,
                next_position,
            )
            ghost.position = next_position

    def respawn_entities(self) -> None:
        self.player.position = self.level.player_spawn
        self.player.current_direction = None
        self.player.queued_direction = None
        self.frightened_timer_ms = 0

        for ghost in self.ghosts:
            ghost.position = ghost.spawn_position
            ghost.direction = None
            ghost.mode = GhostMode.NORMAL
            ghost.respawn_timer_ms = 0

    def begin_player_death(self) -> None:
        if self.phase is GameplayPhase.PLAYER_DYING:
            return
        self.lives -= 1
        self.phase = GameplayPhase.PLAYER_DYING
        self.player.current_direction = None
        self.player.queued_direction = None

    def finish_player_death(self) -> None:
        if self.phase is not GameplayPhase.PLAYER_DYING:
            return
        if self.lives <= 0:
            self.outcome = GameOutcome.GAME_OVER
        else:
            self.respawn_entities()
        self.phase = GameplayPhase.PLAYING

    def handle_player_ghost_collision(self, *, god_mode: bool = False) -> None:
        if (self.outcome is not GameOutcome.PLAYING or
                self.phase is not GameplayPhase.PLAYING):
            return
        for ghost in self.ghosts:
            if (ghost.mode is GhostMode.NORMAL and
                    self.player.position == ghost.position):
                if god_mode:
                    continue
                self.begin_player_death()
                return
            if (ghost.mode is GhostMode.FRIGHTENED and
                    self.player.position == ghost.position):
                self.score += self.points_per_ghost
                ghost.mode = GhostMode.DEAD
                ghost.respawn_timer_ms = self.ghost_respawn_timer_ms
                ghost.direction = None

    def has_collected_all_pacgums(self) -> bool:
        return not self.pacgums and not self.super_pacgums

    def debug_trigger_level_clear(self) -> None:
        self.outcome = GameOutcome.LEVEL_CLEARED

    def debug_trigger_game_over(self) -> None:
        self.outcome = GameOutcome.GAME_OVER
