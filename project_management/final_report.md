# Final report

## Project summary

The final project is a complete Python/Pygame Pac-Man-style game created for the 42 curriculum by hgeorges and ngaubil.

The game includes generated mazes, Pac-Man movement, pacgums, super-pacgums, autonomous ghosts, frightened mode, scoring, lives, death/respawn flow, game over, victory, highscores, multiple levels, timer, pause, instructions, cheat mode, project-management evidence, documentation, and a Linux packaged release.

The final release page is:

```text
https://h42m.itch.io/pacman-42-nh
```

## Completed subject requirements

| Requirement | Final status |
| --- | --- |
| Python project with graphical game loop. | Completed with Python/Pygame. |
| Makefile workflow. | Completed: install, run, debug, clean, fclean, re, lint, lint-strict, package, package-zip. |
| JSON config with comments/defaults/safe handling. | Completed. |
| Assigned A-Maze-ing package used as-is. | Completed through `pacman/maze_adapter.py`. |
| Generated maze with pacgums, super-pacgums, ghosts, and player. | Completed. |
| Player movement, lives, death, respawn, game over. | Completed. |
| Ghost autonomous chase/flee/respawn behavior. | Completed. |
| Scoring system. | Completed. |
| Persistent top-10 highscores with name validation. | Completed. |
| Multiple levels with score/life carryover. | Completed with 10 configured levels. |
| Timer/timeout. | Completed. |
| Cheat mode for peer review. | Completed. |
| Main menu, highscores, instructions, HUD, pause, game over, victory. | Completed. |
| Project packaging/release. | Completed with PyInstaller Linux build and Itch.io upload. |
| Project-management evidence. | Completed in `project_management/`. |
| README. | Completed at repository root. |
| Docstrings/type hints/linting. | Completed and validated. |

## Architecture summary

The project is organized around a clean separation between configuration, maze generation, runtime level data, gameplay rules, session progression, UI states, rendering, and persistence.

- Config loading validates raw JSON and provides safe typed data.
- Maze generation is isolated behind an adapter so the assigned external package is used as-is.
- `Level` stores generated per-level data.
- `GameState` owns gameplay rules for the current level.
- `GameSession` owns score, lives, and level progression across levels.
- Navigation and ghost AI helpers keep movement logic reusable.
- State classes manage menus, pause, play, game over, victory, highscores, and instructions.
- Render classes draw gameplay and UI without owning gameplay rules.

## Validation summary

Final validation included:

- `make lint`;
- compile checks;
- AST docstring coverage audit;
- behavior-neutral AST comparison after stripping docstrings;
- manual gameplay testing;
- cheat mode testing;
- highscore save/load testing;
- headless UI layout audit;
- PyInstaller package build;
- release ZIP generation;
- packaged executable smoke test;
- Itch.io upload.

## Known limitations

The remaining limitations are accepted as polish rather than compliance blockers:

- Render interpolation can feel slightly behind logical tile movement in some collision cases.
- Ghost AI is path-aware and distinct but not an exact arcade-perfect recreation.
- The packaged build targets Linux only.

## Conclusion

The project reached a complete playable, documented, and packaged state. The final result satisfies the mandatory gameplay, configuration, highscore, UI, project-management, README, and packaging expectations while preserving a modular architecture that can still be extended later.
