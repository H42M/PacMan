from sys import argv
from pacman.app import run


def main() -> int:
    """Validate command-line arguments and start the application."""
    if len(argv) != 2:
        print("Usage: make run")
        return 1

    config_path = argv[1]
    return run(config_path)


if __name__ == "__main__":
    raise SystemExit(main())
