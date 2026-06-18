_This activity has been created as part of the 42 curriculum by hgeorges, ngaubil._

# PacMan

## Description

PacMan is a Python/Pygame implementation of a Pac-Man-style game for the 42 curriculum.
The goal is to provide a playable game with generated mazes, pellets, ghosts, scoring,
level progression, highscores, configuration, and a clear project architecture.

## Features

- Main menu, instructions screen, highscores screen, HUD, pause menu, game over screen, victory screen, and name entry for highscores.
- Pac-Man movement with walls, queued direction changes, pacgums, super-pacgums, score, lives, death/respawn, level timer, game over, and victory.
- Four ghosts with autonomous movement, path-aware normal behavior, frightened mode, eaten ghost scoring, dead/inactive state, and respawn.
- Ten configured levels with score and life carryover.
- JSON highscore persistence.
- Cheat mode for review and testing.
- Safe config loading with defaults, clamping, warnings, and full-line `#` comments.
- Graceful missing dependency handling before `make install`.

## Requirements

- Python 3.
- `make`.
- Pygame and project dependencies installed through `requirements.txt`.
- The assigned A-Maze-ing wheel located at `external/mazegenerator-00001-py3-none-any.whl`.

## Installation

Install dependencies with:

```bash
make install
```

This creates the local virtual environment and installs:

- `pygame`
- `flake8`
- `mypy`
- the external A-Maze-ing maze generator wheel from `external/`

## Usage

Run the game with:

```bash
python3 pac-man.py config/config.json
```

The Makefile shortcut is:

```bash
make run
```

Useful Makefile commands:

```bash
make install
make run
make debug
make clean
make lint
```

If the command-line arguments are wrong, the program prints:

```text
Usage: python3 pac-man.py config/config.json
```

If dependencies are missing, the program prints a clear message asking the user to run `make install`.

## Controls

- `W` or Up arrow: move up.
- `A` or Left arrow: move left.
- `S` or Down arrow: move down.
- `D` or Right arrow: move right.
- `Esc`: pause or resume.
- Mouse: interact with menus and buttons.

Cheat/review shortcuts:

- `F1`: skip current level.
- `F2`: trigger game over.
- `F3`: toggle god mode.
- `F4`: toggle ghost freeze.
- `F5`: add one life, up to the HUD-safe cap.

## Configuration

The default config file is `config/config.json`.

The config loader supports JSON with full-line `#` comments. Missing or invalid values are handled safely with warnings, defaults, and clamping where appropriate.

Top-level keys:

- `highscore_filename`: JSON file used for highscore persistence.
- `lives`: starting lives. The default project config starts the player with `3` lives.
- `points_per_pacgum`: score for a normal pacgum.
- `points_per_super_pacgum`: score for a super-pacgum.
- `points_per_ghost`: score for eating a frightened ghost.
- `levels`: list of level configurations.

Per-level keys:

- `width`: generated maze width.
- `height`: generated maze height.
- `seed`: maze seed, or `null` for random generation.
- `level_max_time`: level timer in seconds.

The default project config contains 10 levels. The first level uses the fixed seed `42` for reproducible startup behavior, and later levels use `null` seeds for random generation.

## Highscore system

Highscores are stored in a JSON file, configured by `highscore_filename`.

The highscore system:

- keeps the top 10 scores;
- validates player names;
- limits names to 10 characters;
- accepts only alphanumeric characters and spaces in names;
- validates scores as non-negative integers;
- recovers safely from missing, corrupt, or invalid highscore files.

This simple JSON approach was chosen because it is inspectable, easy to reset during evaluation, and robust enough for the project scope.

## Maze generation

The project uses the assigned A-Maze-ing generator as-is from:

```text
external/mazegenerator-00001-py3-none-any.whl
```

The rest of the project does not depend directly on the external package. Maze generation is isolated behind:

```text
pacman/maze_adapter.py
```

The adapter:

- imports and calls the external generator;
- requests `perfect=False` for Pac-Man-compatible corridors;
- converts generator output into the internal `GeneratedMaze` and `Wall` model;
- catches generator errors and reports them through a project exception;
- applies internal dead-end cleanup without modifying the external package.

## Cheat mode

Cheat mode exists to help peers and evaluators test game paths quickly.

Available cheat actions:

- skip the current level;
- trigger game over;
- toggle god mode;
- freeze ghosts;
- add a life.

Cheats are available from keyboard shortcuts and from the pause menu.

## General software architecture

High-level module responsibilities:

- `pac-man.py`: entry point, CLI validation, missing dependency handling, and app startup.
- `pacman/config_loader.py` and `pacman/game_config.py`: config loading, defaults, validation, and typed config objects.
- `pacman/maze_adapter.py`: adapter around the external A-Maze-ing generator.
- `pacman/level.py`: runtime level model built from config and generated maze data.
- `pacman/game_session.py`: cross-level session state, including current level, score, and lives.
- `pacman/game_state.py`: per-level gameplay state, rules, collisions, pellets, ghosts, lives, and outcomes.
- `pacman/navigation.py`: movement legality and direction helpers.
- `pacman/ghost_ai.py`: ghost AI, target selection, and path-aware movement helpers.
- `pacman/highscores.py`: highscore validation, sorting, loading, and saving.
- `pacman/states/`: UI and gameflow states.
- `pacman/render/`: rendering layer, containers, text, maze rendering, sprites, animation, buttons, and inputs.

The main architecture separates gameplay data from rendering. Gameplay state owns rules and outcomes, while render classes observe that state and draw it.

## Implementation summary

The game starts by loading validated configuration, generating the current level through the maze adapter, and creating a `GameSession` and `GameState`.

During gameplay:

- player input queues movement directions;
- the level timer advances while not paused;
- Pac-Man collects pacgums and super-pacgums;
- ghosts move on their own timers;
- frightened mode changes ghost behavior temporarily;
- eaten ghosts become inactive and respawn later;
- score and lives persist across levels through `GameSession`;
- game over and victory screens can save highscores.

The UI/gameflow layer manages menu screens, pause behavior, instructions, highscores, game over, and victory. The render layer handles Pygame drawing and sprite animation.

## Project management

Project-management evidence is stored in:

```text
project_management/
```

It contains the timeline, progress tracking, decision log, risk analysis, team organization notes, acceptance test plan, bug log, and final report.

## Packaging / Release

TODO: final packaging/release instructions will be added after the packaging build is implemented and tested.

The final package is expected to target a public/private platform flow such as Itch.io, but this README does not claim that a package has already been built, tested, or uploaded.

## AI usage and resources

AI tools were used to support planning, documentation drafting, debugging help, code review, and checklist generation.

Generated suggestions were reviewed, tested, and adapted by the team before being kept in the project.

Useful resources:

- Python documentation: https://docs.python.org/3/
- Pygame documentation: https://www.pygame.org/docs/
- JSON documentation: https://docs.python.org/3/library/json.html
- GNU Make documentation: https://www.gnu.org/software/make/manual/
- 42 subject materials for this activity.

## TODO before final defense

- Implement and test the final packaging/release build.
- Add final packaging/release instructions to this README.
- Run final QA from a clean install.
- Rehearse the defense flow with the project-management evidence and final build.
