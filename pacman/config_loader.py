import json
from pacman.game_config import GameConfig, LevelConfig

# Parsing helpers


def strip_comment_lines(raw_text: str) -> str:
    """Remove full-line comments from JSON-like config text."""
    raw_lines: list[str] = raw_text.splitlines()
    clean_lines: list[str] = []
    for line in raw_lines:
        if line.strip().startswith("#"):
            clean_lines.append("")
        else:
            clean_lines.append(line)
    return "\n".join(clean_lines)


def check_config_object(parsed_config: object) -> dict[str, object] | None:
    """Return config if it is a JSON object, otherwise None."""
    if not isinstance(parsed_config, dict):
        print(
            "Warning: config root must be a JSON object "
            f"but got {type(parsed_config).__name__}."
        )
        return None
    return parsed_config


# Value readers


def read_str(
        config_data: dict[str, object],
        key: str,
        default: str,
        ) -> str:
    """Read a string config value with defaulting."""

    if key not in config_data:
        print(f"Warning: config key '{key}' not found.")
        print(f"Using default value: {default}.")
        return default
    value = config_data[key]
    if not isinstance(value, str):
        print(f"Warning: config key '{key}' must be a string, "
              f"got {type(value).__name__}.")
        print(f"Using default value: {default}.")
        return default
    if not value.strip():
        print(f"Warning: config key '{key}' cannot be empty.")
        print(f"Using default value: {default}.")
        return default

    return value.strip()


def read_int(
    config_data: dict[str, object],
    key: str,
    default: int,
    min_value: int,
    max_value: int,
) -> int:
    """Read an integer config value with defaulting and clamping."""
    if key not in config_data:
        print(f"Warning: config key '{key}' not found.")
        print(f"Using default value: {default}.")
        return default

    value = config_data[key]

    if isinstance(value, bool) or not isinstance(value, int):
        print(
            f"Warning: config key '{key}' must be an int, "
            f"got {type(value).__name__}."
        )
        print(f"Using default value: {default}.")
        return default

    if value < min_value:
        print(
            f"Warning: config key '{key}' is under minimum {min_value}."
        )
        print(f"Using minimum value: {min_value}.")
        return min_value

    if value > max_value:
        print(
            f"Warning: config key '{key}' is above maximum {max_value}."
        )
        print(f"Using maximum value: {max_value}.")
        return max_value

    return value


def read_optional_int(config_data: dict[str, object],
                      key: str,
                      default: int | None,
                      ) -> int | None:
    """Read an optional integer config value with defaulting."""
    if key not in config_data:
        print(f"Warning: config key '{key}' not found.")
        print(f"Using default value: {default}.")
        return default
    value = config_data[key]
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int):
        print(f"Warning: config key '{key}' must be an integer or null, "
              f"got {type(value).__name__}.")
        print(f"Using default value: {default}.")
        return default
    return value


# Config builders


def build_level_config(level_data: dict[str, object],
                       default_level: LevelConfig,) -> LevelConfig:
    """Build a validated level config from raw level data."""
    width = read_int(config_data=level_data,
                     key="width",
                     default=default_level.width,
                     min_value=7,
                     max_value=100,)
    height = read_int(config_data=level_data,
                      key="height",
                      default=default_level.height,
                      min_value=7,
                      max_value=100,)
    seed = read_optional_int(config_data=level_data,
                             key="seed",
                             default=default_level.seed)
    level_max_time = read_int(config_data=level_data,
                              key="level_max_time",
                              default=default_level.level_max_time,
                              min_value=1,
                              max_value=999,)

    return LevelConfig(
        width=width,
        height=height,
        seed=seed,
        level_max_time=level_max_time,
    )


def read_levels(
    config_data: dict[str, object],
    default: tuple[LevelConfig, ...],
) -> tuple[LevelConfig, ...]:
    """Read level configs with defaulting."""
    if "levels" not in config_data:
        print("Warning: no levels found in config.")
        print("Using default levels.")
        return default

    value = config_data["levels"]

    if not isinstance(value, list):
        print("Warning: config key 'levels' must be a list.")
        print("Using default levels.")
        return default
    if not value:
        print("Warning: config key 'levels' is an empty list.")
        print("Using default levels.")
        return default

    levels_list: list[LevelConfig] = []
    for i, level in enumerate(value):
        default_level = default[i % len(default)]
        if not isinstance(level, dict):
            print(
                f"Warning: level {i} must be a JSON object, "
                f"got {type(level).__name__}."
            )
            levels_list.append(default_level)
        else:
            levels_list.append(build_level_config(
                level_data=level,
                default_level=default_level
                ))
    return tuple(levels_list)


def build_game_config(config_data: dict[str, object]) -> GameConfig:
    """Build a validated game config from raw config data."""
    default_config = GameConfig()

    highscore_filename = read_str(config_data,
                                  key="highscore_filename",
                                  default=default_config.highscore_filename)
    lives = read_int(config_data, key="lives", default=default_config.lives,
                     min_value=1, max_value=9)
    points_per_pacgum = read_int(config_data,
                                 key="points_per_pacgum",
                                 default=default_config.points_per_pacgum,
                                 min_value=1, max_value=100,
                                 )
    points_per_super_pacgum = read_int(
        config_data,
        key="points_per_super_pacgum",
        default=default_config.points_per_super_pacgum,
        min_value=5,
        max_value=500,
    )
    points_per_ghost = read_int(config_data,
                                key="points_per_ghost",
                                default=default_config.points_per_ghost,
                                min_value=20,
                                max_value=2000,
                                )
    levels = read_levels(
        config_data=config_data,
        default=default_config.levels
    )

    return GameConfig(highscore_filename=highscore_filename,
                      lives=lives,
                      points_per_pacgum=points_per_pacgum,
                      points_per_super_pacgum=points_per_super_pacgum,
                      points_per_ghost=points_per_ghost,
                      levels=levels,
                      )


def load_config(config_path: str) -> GameConfig:
    """Load a game configuration from a JSON file."""
    try:
        with open(config_path) as config_file:
            raw_text = config_file.read()
            parsed_config: object = json.loads(strip_comment_lines(raw_text))
            config_data = check_config_object(parsed_config)
            if config_data is None:
                print("Using default configuration.")
                return GameConfig()

    except OSError as error:
        print(f"Warning: could not read config file '{config_path}': {error}")
        print("Using default configuration.")
        return GameConfig()

    except json.JSONDecodeError as error:
        print(f"Warning: invalid JSON config: {error}")
        print("Using default configuration.")
        return GameConfig()

    return build_game_config(config_data)


if __name__ == "__main__":
    print(load_config("config/config.json"))
