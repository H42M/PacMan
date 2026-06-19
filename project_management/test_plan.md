# Acceptance test plan

This plan lists the manual tests used or planned for final validation. The project relies mainly on manual acceptance testing because it is a graphical Pygame game with interactive behavior.

## Defense-critical checklist

| Area | Test | Steps | Expected result | Status |
| --- | --- | --- | --- | --- |
| CLI | Wrong number of arguments. | Run `python3 pac-man.py` and `python3 pac-man.py a b`. | Usage message printed; exits cleanly; no traceback. | Passed / retest final. |
| Dependencies | Missing dependencies before install. | Run game before `make install` in a clean environment. | Clear message asks user to run `make install`; no traceback. | Passed. |
| Config | Valid config launches game. | Run `python3 pac-man.py config/config.json`. | Game starts and reaches menu/gameplay. | Passed / retest final. |
| Config | Missing config file. | Run with a nonexistent config path. | Friendly error/fallback behavior; no Python traceback. | Retest final. |
| Config | Invalid JSON. | Create invalid JSON and launch. | Error handled cleanly; no crash. | Retest final. |
| Config | `#` comments. | Add full-line comments in config. | Comments ignored and config loads. | Passed / retest final. |
| Config | Invalid numeric values. | Use invalid widths/heights/timers/scores/lives. | Values clamped/defaulted safely. | Passed / retest final. |
| Maze adapter | External package used as-is. | Inspect adapter/imports and reinstall package. | Generator is called through adapter; external package unmodified. | Passed. |
| Maze adapter | `perfect=False`. | Inspect adapter call. | Generator receives `perfect=False`. | Passed. |
| Maze adapter | Generation failure handling. | Simulate or trigger invalid generation path where practical. | Friendly handling through adapter error path. | Retest final if practical. |
| Rendering | Maze visible from `Level`/`GeneratedMaze`. | Start game and inspect first level. | Maze renders from internal representation. | Passed. |
| Player | Movement with arrows/WASD. | Move in all directions. | Pac-Man moves through corridors. | Passed. |
| Player | Wall collision. | Try to move through walls. | Movement is blocked. | Passed. |
| Player | Timed movement and queued turns. | Hold direction and queue turns. | Pac-Man continues moving and turns when legal. | Passed. |
| Collectibles | Pacgums. | Move over normal pacgums. | Pacgums disappear and score increases. | Passed. |
| Collectibles | Super-pacgums. | Eat a super-pacgum. | Score increases and ghosts become frightened. | Passed. |
| Ghosts | Normal chase. | Start game and observe ghosts. | Ghosts move autonomously and pursue Pac-Man. | Passed. |
| Ghosts | Frightened behavior. | Eat super-pacgum. | Ghosts flee/run away while frightened. | Passed. |
| Ghosts | Eat frightened ghost. | Touch frightened ghost. | Ghost becomes dead/inactive; score increases. | Passed. |
| Ghosts | Respawn. | Wait after eating a ghost. | Ghost respawns after delay. | Passed. |
| Ghosts | No active ghost overlap. | Observe several ghost ticks. | Active ghosts do not end a tick on the same cell. | Passed. |
| Lives | Normal ghost collision. | Touch normal ghost. | Life is lost; player death animation and respawn flow occur. | Passed. |
| Game over | Lose all lives or use cheat shortcut. | Trigger game over. | Game over screen appears with final score/name entry. | Passed. |
| Victory | Clear final level or use level-skip path. | Complete all levels. | Victory screen appears with final score/name entry. | Passed. |
| Level progression | Clear non-final level. | Clear level 1. | Next level starts; score/lives carry over. | Passed. |
| Timer | Level timeout. | Let timer expire. | Timeout triggers configured loss/game-over behavior. | Passed / retest final. |
| Pause | Pause and resume. | Pause during gameplay. | Movement and timers stop; resume continues game. | Passed. |
| Highscores | Save score. | Enter valid name after win/loss. | Score saved to JSON and displayed in highscores. | Passed. |
| Highscores | Invalid name. | Try invalid/too-long name. | Name rejected or handled safely. | Passed / retest final. |
| Highscores | Corrupt file. | Corrupt highscore JSON and launch. | Game recovers safely; no traceback. | Retest final. |
| Cheat mode | God mode. | Enable god mode and touch normal ghost. | No life lost; frightened ghost eating still works. | Passed. |
| Cheat mode | Ghost freeze. | Enable ghost freeze. | Ghosts stop moving while game continues. | Passed. |
| Cheat mode | Extra life. | Add life. | Lives increase up to HUD-safe cap. | Passed. |
| Cheat mode | Level skip. | Trigger skip. | Existing level-clear/progression flow is reused. | Passed. |
| UI | Main menu. | Launch game. | Start, highscores, instructions, and exit paths work; inactive settings entry is hidden. | Passed. |
| UI | Instructions. | Open instructions screen. | Controls/rules visible; back to menu works. | Passed. |
| UI | HUD. | Play a level. | Score, lives, level, and time visible. | Passed. |
| Tooling | `make lint`. | Run `make lint`. | flake8 and mypy pass. | Passed. |
| Tooling | Docstring coverage. | Run AST audit for classes/functions/methods. | No missing class/function/method docstrings; behavior-neutral AST comparison passes after stripping docstrings. | Passed. |
| UI layout | Headless state layout audit. | Build MenuState, HighScoreState, InstructionState, SettingsState, GameOverState, and PlayState with dummy video driver. | Concrete render object bounds fit within the screen. | Passed. |
| Packaging | Packaged build. | Build package and launch packaged game. | Packaged game launches with assets/config; no traceback. | Pending final packaging. |

## Final manual test route

1. `make fclean && make install && make lint`.
2. `python3 pac-man.py` to verify usage message.
3. `make run` to verify standard launch.
4. Start game, move, collect pacgums, eat a super-pacgum, eat a ghost, lose a life, pause/resume.
5. Use cheats to skip levels and trigger game over/victory paths.
6. Save a highscore and confirm it appears in the menu.
7. Run the headless layout audit if UI structure changes.
8. Build the package and smoke-test the packaged executable.
