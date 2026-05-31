from __future__ import annotations
from dataclasses import dataclass

from pacman.level import Level
from pacman.player import PlayerState


@dataclass(slots=True)
class GameState:
    level: Level
    player: PlayerState

    @classmethod
    def from_level(cls, level: Level) -> GameState:
        return cls(level=level, player=PlayerState(level.player_spawn))
