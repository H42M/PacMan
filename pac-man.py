from sys import argv
from pacman.app import run
from pacman.game_config import GameConfig


def main() -> int:
    """Validate command-line arguments and start the application."""
    if len(argv) != 2:
        print("Usage: make run")
        return 1

    config = GameConfig()
    return run(config)


if __name__ == "__main__":
    raise SystemExit(main())
