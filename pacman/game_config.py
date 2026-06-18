from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LevelConfig:
    """Configuration for one generated level."""

    width: int = 15
    height: int = 15
    seed: int | None = None
    level_max_time: int = 90


DEFAULT_LEVELS: tuple[LevelConfig, ...] = (
    LevelConfig(width=7, height=7, seed=42, level_max_time=55),
    LevelConfig(width=9, height=9, seed=None, level_max_time=65),
    LevelConfig(width=11, height=11, seed=None, level_max_time=75),
    LevelConfig(width=13, height=13, seed=None, level_max_time=85),
    LevelConfig(width=15, height=15, seed=None, level_max_time=95),
    LevelConfig(width=15, height=15, seed=None, level_max_time=95),
    LevelConfig(width=17, height=17, seed=None, level_max_time=105),
    LevelConfig(width=17, height=17, seed=None, level_max_time=105),
    LevelConfig(width=19, height=19, seed=None, level_max_time=115),
    LevelConfig(width=19, height=19, seed=None, level_max_time=115),
)


@dataclass(frozen=True, slots=True)
class GameConfig:
    """Validated game configuration used by the application."""

    highscore_filename: str = "highscores.json"
    lives: int = 3
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    levels: tuple[LevelConfig, ...] = DEFAULT_LEVELS
