from sys import argv

from pacman.config_loader import load_config


def main() -> int:
    """Validate command-line arguments and start the application."""
    if len(argv) != 2:
        print("Usage: make run")
        return 1

    # late import to avoid pygame message when error happens
    from pacman.app import run

    config = load_config(argv[1])
    return run(config)


if __name__ == "__main__":
    raise SystemExit(main())
