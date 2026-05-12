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


def check_config_object(parsed_config: object) -> dict[str, object]:
    """Return config if it is a JSON object, otherwise empty defaults."""
    if not isinstance(parsed_config, dict):
        print(
            "Warning: config root must be a JSON object "
            f"but got {type(parsed_config).__name__}."
        )
        return {}
    return parsed_config


def build_game_config(config_data: dict[str, object]) -> GameConfig:
    """Build a validated game config from raw config data."""
    return GameConfig()


def load_config(config_path: str) -> GameConfig:
    """Load a game configuration from a JSON file."""
    try:
        with open(config_path) as config_file:
            raw_text = config_file.read()
            parsed_config: object = json.loads(strip_comment_lines(raw_text))
            config_data = check_config_object(parsed_config)

    except FileNotFoundError:
        print(f"Warning: config file not found: {config_path}")
        print("Using default configuration.")
        return GameConfig()

    except json.JSONDecodeError as error:
        print(f"Warning: invalid JSON config: {error}")
        print("Using default configuration.")
        return GameConfig()

    return build_game_config(config_data)


if __name__ == "__main__":
    load_config("config/config.json")
