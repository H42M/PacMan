import json
from pacman.game_config import GameConfig


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


def build_game_config(config_data: dict[str, object]) -> GameConfig:
    """Build a validated game config from raw config data."""
    default_config = GameConfig()
    lives = read_int(config_data, key="lives", default=default_config.lives,
                     min_value=1, max_value=9)

    return GameConfig(lives=lives)


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
