# Final report

## Project summary

This project recreates a Pac-Man-style game in Python with Pygame. The final game is built around a modular architecture: configuration loading, external maze generation, runtime level data, gameplay state, session progression, rendering, UI states, highscores, and cheat tools are separated into dedicated modules.

The project reached a playable MVP-plus state: Pac-Man can move through generated mazes, collect pacgums and super-pacgums, score points, avoid or eat ghosts, lose lives, progress through multiple levels, save highscores, pause the game, and use cheat tools for peer review.

## Completed subject requirements

| Requirement area | Status | Notes |
| --- | --- | --- |
| Python project and Makefile workflow | Done | `make install`, `make run`, `make debug`, `make clean`, and `make lint` are part of the workflow. |
| CLI config argument | Done | Launch format is `python3 pac-man.py config/config.json`; wrong arg count handled cleanly. |
| JSON config with comments/defaults | Done | Config supports comment handling, compliant defaults, validation, and clamping. |
| Faulty config/dependency handling | Done | Missing/invalid config values and missing dependencies before `make install` are handled without raw tracebacks where applicable. |
| Assigned A-Maze-ing package | Done | Used as-is behind the maze adapter with `perfect=False`. |
| Generated maze gameplay | Done | Maze, walls, corridors, pacgums, super-pacgums, player, and ghosts are generated/initialized from level data. |
| Player rules | Done | 4-direction movement, walls, lives, respawn, game over, level clear. |
| Ghost rules | Done | Autonomous movement, normal chase, frightened flee, edible ghost scoring, dead/respawn behavior, and active ghost overlap prevention. |
| Pacgums and scoring | Done | Normal pacgums, super-pacgums, and edible ghost scoring implemented. |
| Multiple levels | Done | Ten configured levels with score/life carryover. |
| Timer and pause | Done | Level timer, timeout behavior, pause/resume. |
| Highscores | Done | Persistent JSON top-10 highscores with name and score validation. |
| UI screens | Done | Main menu, highscores, instructions, HUD, pause, game over, victory, name entry; inactive settings entry hidden. |
| Cheat mode | Done | God mode, level skip, game over trigger, ghost freeze, extra lives. |
| Project-management evidence | Done | This directory contains the repo evidence files and current final-status tracking. |
| Docstring compliance | Done | All classes/functions/methods have concise one-line docstrings; AST audit and behavior-neutral AST comparison passed. |
| README | Pending final pass | Should be finalized after packaging instructions are stable. |
| Packaging/public platform build | Pending final pass | Dedicated packaging branch/build evidence still required. |

## Architecture summary

The final architecture keeps gameplay data and rendering separated:

- `pac-man.py` validates CLI usage and starts the app.
- `pacman/config_loader.py` and `pacman/game_config.py` own config parsing and validated settings.
- `pacman/maze_adapter.py` owns all contact with the external A-Maze-ing package.
- `pacman/level.py` represents one generated playable level.
- `pacman/game_session.py` stores cross-level campaign state.
- `pacman/game_state.py` stores mutable per-level gameplay state.
- `pacman/navigation.py` centralizes movement legality helpers.
- `pacman/ghost_ai.py` owns normal ghost target/path behavior.
- `pacman/highscores.py` owns highscore persistence.
- `pacman/states/` owns UI/gameflow states.
- `pacman/render/` owns drawing, sprites, and animation presentation.

This split made the project easier to test, explain, and adapt after UI/render and gameplay work diverged.

## Final validation status

Manual validation confirmed the main gameplay loop, ghost behavior, frightened mode, highscores, level progression, cheat mode, pause behavior, and several cleanup fixes. `make lint`, docstring coverage audit, behavior-neutral docstring audit, and a headless layout audit for MenuState, HighScoreState, InstructionState, SettingsState, GameOverState, and PlayState have passed.

The final remaining validation items are:

- test final packaged build,
- smoke-test the release package with assets/config,
- finalize README to match the packaged delivery.

## Known limitations

| Limitation | Impact | Decision |
| --- | --- | --- |
| Render interpolation can appear slightly behind logical movement. | Collisions may sometimes feel slightly early visually. | Accepted for final unless QA finds it game-breaking. |
| Ghost AI is improved but not arcade-perfect. | Ghosts are distinct and path-aware but not exact Namco behavior. | Accepted; exact arcade AI is outside mandatory scope. |
| Settings state remains registered but hidden from the menu. | No player-facing fake options; code path remains easy to restore. | Accepted for final unless a real settings feature is added. |

## Lessons learned

- Isolating the external maze generator early reduced later risk.
- A clear `Level` / `GameState` / `GameSession` split made level progression and resets much easier.
- UI/render and gameplay architecture need a shared source of truth to avoid conflicts.
- Small branches with clear scope were easier to merge and defend.
- Final compliance work should not be underestimated: README, project evidence, packaging, and QA are real deliverables, not afterthoughts.
