_This activity has been created as part of the 42 curriculum by hgeorges, ngaubil._

# PacMan

## Description

PacMan is a Python/Pygame implementation of a Pac-Man-style arcade game created for the 42 curriculum. The project focuses on object-oriented design, robust configuration, generated mazes, persistent highscores, playable game flow, project management evidence, and a packaged release build.

The release build is available on Itch.io:

```text
https://h42m.itch.io/pacman-42-nh
```

## Features

- Main menu with Start Game, Highscores, Instructions, and Exit.
- In-game HUD displaying score, lives, current level, and remaining time.
- Pause menu with resume, menu return, and review cheat controls.
- Game over and victory screens with final score and highscore name entry.
- Ten-level progression with score and remaining lives carried between levels.
- Pac-Man movement with timed motion, queued turns, wall collision, and pellet collection.
- Pacgums, super-pacgums, scoring, frightened mode, edible ghosts, and ghost respawn.
- Four autonomous ghosts with path-aware movement and distinct basic personalities.
- Persistent top-10 JSON highscore system.
- Cheat mode for peer review and feature testing.
- Robust JSON configuration with defaults, clamping, warnings, and full-line `#` comments.
- Graceful handling for missing dependencies before `make install`.
- PyInstaller packaging workflow and Linux release archive.

## Requirements

Development requirements:

- Python 3.10 or later.
- `make`.
- A Unix-like shell environment for the provided Makefile commands.

Runtime dependencies are installed through `requirements.txt`:

- `pygame`
- `flake8`
- `mypy`
- `pyinstaller`
- the assigned A-Maze-ing wheel from `external/mazegenerator-00001-py3-none-any.whl`

The packaged Linux build does not require the user to create a Python virtual environment.

## Installation

Install project dependencies with:

```bash
make install
```

This creates `.venv/`, upgrades `pip`, and installs the dependencies listed in `requirements.txt`.

## Usage

Run the source version with:

```bash
python3 pac-man.py config/config.json
```

The development shortcut is:

```bash
make run
```

Useful Makefile commands:

```bash
make install
make run
make debug
make clean
make fclean
make re
make lint
make lint-strict
make package
make package-zip
```

If the command-line arguments are wrong, the program prints:

```text
Usage: python3 pac-man.py config/config.json
```

If a dependency such as `pygame` is missing, the program exits cleanly and asks the user to run `make install`.

## Controls

Movement:

- `W` or Up arrow: move up.
- `A` or Left arrow: move left.
- `S` or Down arrow: move down.
- `D` or Right arrow: move right.

Gameflow:

- `Esc`: pause or resume.
- Mouse: interact with menus and buttons.

Cheat/review shortcuts:

- `F1`: skip current level.
- `F2`: trigger game over.
- `F3`: toggle god mode.
- `F4`: toggle ghost freeze.
- `F5`: add one life up to the HUD-safe cap.

## Configuration

The default configuration file is:

```text
config/config.json
```

The config loader supports JSON with full-line `#` comments. Missing, invalid, or out-of-range values are handled safely with warnings, defaults, and clamping where appropriate.

Top-level keys:

- `highscore_filename`: JSON file used for highscore persistence.
- `lives`: starting lives. The final default is `3`.
- `points_per_pacgum`: score for a normal pacgum.
- `points_per_super_pacgum`: score for a super-pacgum.
- `points_per_ghost`: score for eating a frightened ghost.
- `levels`: list of level configurations.

Per-level keys:

- `width`: generated maze width.
- `height`: generated maze height.
- `seed`: maze seed, or `null` for random generation.
- `level_max_time`: level timer in seconds.

The final config contains 10 levels. The first level uses the fixed seed `42` for reproducible startup behavior, and later levels use `null` seeds for random generation.

## Highscore system

Highscores are stored in a JSON file configured by `highscore_filename`.

The highscore system:

- keeps the top 10 scores;
- validates player names;
- limits names to 10 characters;
- accepts only alphanumeric characters and spaces in names;
- validates scores as non-negative integers;
- recovers safely from missing, corrupt, or invalid highscore files;
- displays saved highscores from the main menu.

This JSON approach was chosen because it is inspectable, easy to reset during evaluation, and robust enough for the project scope.

## Maze generation

The project uses the assigned external A-Maze-ing generator as-is from:

```text
external/mazegenerator-00001-py3-none-any.whl
```

Maze generation is isolated behind:

```text
pacman/maze_adapter.py
```

The adapter:

- imports and calls the assigned generator;
- requests `perfect=False` for Pac-Man-compatible corridors;
- converts generator output into the internal `GeneratedMaze` and `Wall` model;
- translates project seed values into the package seed behavior;
- handles generator failures cleanly;
- applies internal dead-end cleanup without modifying the external package.

The rest of the game consumes the internal maze representation rather than depending directly on the external package output.

## Cheat mode

Cheat mode exists to help peers and evaluators test important game paths quickly.

Available cheat actions:

- skip the current level;
- trigger game over;
- toggle god mode;
- freeze ghosts;
- add a life.

Cheats are available from keyboard shortcuts and from the pause menu.

## General software architecture

High-level module responsibilities:

- `pac-man.py`: entry point, CLI validation, dependency handling, and app startup.
- `pacman/config_loader.py` and `pacman/game_config.py`: config loading, defaults, validation, and typed config objects.
- `pacman/maze_adapter.py`: adapter around the external A-Maze-ing generator.
- `pacman/level.py`: runtime level model built from config and generated maze data.
- `pacman/game_session.py`: cross-level session state, including current level, score, and lives.
- `pacman/game_state.py`: per-level gameplay rules, collisions, pellets, ghosts, lives, and outcomes.
- `pacman/navigation.py`: shared movement legality and direction helpers.
- `pacman/ghost_ai.py`: path-aware ghost targeting and movement helpers.
- `pacman/highscores.py`: highscore validation, sorting, loading, and saving.
- `pacman/states/`: UI and gameflow states.
- `pacman/render/`: Pygame rendering layer, UI components, sprites, animation, and layout.

The architecture separates gameplay rules from rendering. Gameplay state owns rules and outcomes, while render classes observe the current state and draw it.

## Implementation summary

The game starts by loading the configuration, generating the current level through the maze adapter, and creating a `GameSession` plus a per-level `GameState`.

During gameplay:

- player input queues movement directions;
- movement legality is checked through shared navigation helpers;
- Pac-Man collects pacgums and super-pacgums;
- the level timer advances while the game is not paused;
- ghosts move on their own timer;
- frightened mode temporarily changes ghost behavior;
- eaten ghosts become inactive and respawn later;
- active ghost overlap is prevented during movement ticks;
- score and remaining lives persist across levels through `GameSession`;
- game over and victory screens can save highscores.

The UI/gameflow layer manages menus, pause behavior, instructions, highscores, game over, and victory. The render layer handles drawing and animation.

## Packaging / Release

The project includes a PyInstaller packaging workflow.

Build the package locally with:

```bash
make package
```

Create the Linux release archive with:

```bash
make package-zip
```

The generated archive is:

```text
dist/PacMan-linux.zip
```

Run the packaged Linux build from inside the extracted `PacMan` directory:

```bash
./PacMan config/config.json
```

The Linux build was uploaded for evaluation/demo purposes on Itch.io:

```text
https://h42m.itch.io/pacman-42-nh
```

The committed packaging workflow is defined by `pacman.spec`, `requirements.txt`, and the Makefile package targets. Build outputs such as `build/`, `dist/`, and release ZIP files are generated artifacts and are not committed to the repository.

## Project management

Project-management evidence is stored in:

```text
project_management/
```

It includes:

- project timeline;
- progress tracking;
- decision log;
- risk analysis;
- team organization;
- acceptance test plan;
- bug log;
- final report.

## AI usage and resources

AI tools were used as support for planning, documentation drafting, debugging help, code review, prompt/checklist preparation, and final compliance review. Suggestions were reviewed, tested, and adapted by the team before being kept in the project.

Useful resources:

- Python documentation: https://docs.python.org/3/
- Pygame documentation: https://www.pygame.org/docs/
- PyInstaller documentation: https://pyinstaller.org/en/stable/
- Itch.io documentation: https://itch.io/docs/creators/
- JSON documentation: https://docs.python.org/3/library/json.html
- GNU Make documentation: https://www.gnu.org/software/make/manual/
- 42 subject materials for this activity.
