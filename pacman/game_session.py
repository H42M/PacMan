from __future__ import annotations

from dataclasses import dataclass

from pacman.game_config import GameConfig
from pacman.game_state import GameState
from pacman.level import build_level


@dataclass(slots=True)
class GameSession:
    config: GameConfig
    current_level_index: int
    score: int
    lives: int

    @classmethod
    def from_config(cls, config: GameConfig) -> GameSession:
        return cls(
            config=config,
            current_level_index=0,
            score=0,
            lives=config.lives,
        )

    @property
    def total_levels(self) -> int:
        return len(self.config.levels)

    @property
    def is_final_level(self) -> bool:
        return self.current_level_index >= self.total_levels - 1

    def create_game_state(self) -> GameState:
        level = build_level(self.config, self.current_level_index)
        game_state = GameState.from_level(self.config, level)
        game_state.score = self.score
        game_state.lives = self.lives
        return game_state

    def sync_from_game(self, game: GameState) -> None:
        self.score = game.score
        self.lives = game.lives

    def advance_level(self) -> None:
        if self.is_final_level:
            raise ValueError("Cannot advance past the final level.")
        self.current_level_index += 1
