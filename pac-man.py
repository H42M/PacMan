from sys import argv

USAGE = "Usage: python3 pac-man.py config/config.json"
PROJECT_MODULE_NAMES = ("Errors", "pacman")


def is_project_module(module_name: str | None) -> bool:
    """Return True when a missing module belongs to this project."""
    if module_name is None:
        return False
    return (
        module_name in PROJECT_MODULE_NAMES
        or module_name.startswith("pacman.")
    )


def main() -> int:
    """Validate command-line arguments and start the application."""
    if len(argv) != 2:
        print(USAGE)
        return 1

    # Late imports avoid dependency tracebacks before validation/handling.
    try:
        from pacman.config_loader import load_config
        from pacman.app import run
    except ModuleNotFoundError as error:
        if is_project_module(error.name):
            raise
        dependency_name = (
            error.name.split(".")[0]
            if error.name is not None
            else "a required package"
        )
        print(
            f"Missing dependency: {dependency_name}. "
            "Please run 'make install' before starting the game."
        )
        return 1

    config = load_config(argv[1])
    return run(config)


if __name__ == "__main__":
    raise SystemExit(main())
