from sys import argv

from pacman.app import run
from pacman.config_loader import load_config


def main() -> int:
    """Validate command-line arguments and start the application."""
    if len(argv) != 2:
        print("Usage: make run")
        return 1

    config = load_config(argv[1])
    return run(config)


if __name__ == "__main__":
    raise SystemExit(main())
