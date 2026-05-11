from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LevelConfig:
    """Configuration for one generated level."""

    width: int = 28
    height: int = 31
    seed: int | None = None
    level_max_time: int = 90


@dataclass(frozen=True, slots=True)
class GameConfig:
    """Validated game configuration used by the application."""

    highscore_filename: str = "highscores.json"
    lives: int = 3
    pacgum: int = 42
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    levels: tuple[LevelConfig, ...] = (LevelConfig(seed=42),)
