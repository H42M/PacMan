# Acceptance test plan

This checklist covers the main validation areas for the final PacMan project.

## Final validation checklist

| Area | Test | Expected result | Final status |
| --- | --- | --- | --- |
| Install | Run `make install`. | Dependencies install in `.venv/`. | Passed. |
| Lint/type checks | Run `make lint`. | flake8 and mypy pass. | Passed. |
| CLI usage | Run `python3 pac-man.py`. | Usage message is printed without traceback. | Passed. |
| Missing dependencies | Run before dependencies are installed or simulate missing dependency. | Clear message asks user to run `make install`. | Passed. |
| Standard launch | Run `make run`. | Game starts from `config/config.json`. | Passed. |
| Config comments | Add full-line `#` comment to config. | Config still loads. | Passed. |
| Config errors | Use missing/invalid values. | Defaults/clamping/warnings; no Python traceback. | Passed. |
| Maze generator | Start a level. | External generator is called through adapter; package unmodified. | Passed. |
| Maze adapter | `perfect=False`. | Adapter calls generator with non-perfect maze mode. | Passed. |
| Rendering | Start gameplay. | Maze, player, ghosts, collectibles, and HUD are visible. | Passed. |
| Player movement | Move with arrows/WASD. | Pac-Man moves through corridors only. | Passed. |
| Wall collision | Try to move through walls. | Movement is blocked. | Passed. |
| Queued turns | Hold direction and queue turns. | Pac-Man turns when legal and stops when blocked. | Passed. |
| Pacgums | Collect normal pacgums. | Pacgums disappear and score increases. | Passed. |
| Super-pacgums | Eat a super-pacgum. | Score increases and ghosts become frightened. | Passed. |
| Normal ghosts | Observe ghost movement. | Ghosts move autonomously and chase/path toward targets. | Passed. |
| Frightened ghosts | Eat super-pacgum. | Ghosts run away while frightened. | Passed. |
| Eat ghost | Touch frightened ghost. | Ghost becomes dead/inactive; score increases. | Passed. |
| Ghost respawn | Wait after eating ghost. | Ghost respawns after delay. | Passed. |
| Ghost overlap | Observe several ghost ticks. | Active ghosts do not end a tick on the same cell. | Passed. |
| Lives/death | Touch normal ghost. | Life is lost; death/respawn flow occurs. | Passed. |
| Game over | Lose all lives or use cheat. | Game over screen appears with final score/name entry. | Passed. |
| Victory | Clear all levels or use level-skip path. | Victory screen appears with final score/name entry. | Passed. |
| Level progression | Clear non-final level. | Next level starts; score/lives carry over. | Passed. |
| Timer | Let timer expire. | Timeout triggers game-over behavior. | Passed. |
| Pause | Pause during gameplay. | Movement and timers stop; resume continues. | Passed. |
| Highscore save | Enter valid name after win/loss. | Score saves and displays in highscores. | Passed. |
| Invalid highscore names | Enter invalid/too-long name. | Name is rejected or handled safely. | Passed. |
| Corrupt highscore file | Corrupt JSON and launch/display. | Loader recovers safely. | Passed. |
| Cheat god mode | Enable god mode and touch normal ghost. | No life lost; frightened ghost eating still works. | Passed. |
| Cheat ghost freeze | Enable ghost freeze. | Ghosts stop while the game continues. | Passed. |
| Cheat extra life | Add life. | Lives increase up to HUD-safe cap. | Passed. |
| Cheat level skip | Trigger skip. | Existing level-clear/progression flow is reused. | Passed. |
| Main menu | Launch game. | Start, highscores, instructions, and exit are available. | Passed. |
| Instructions | Open instructions. | Controls/rules visible; back to menu works. | Passed. |
| HUD | Play a level. | Score, lives, level, and time are visible. | Passed. |
| Docstrings | Run AST audit. | No class/function/method definitions without docstrings. | Passed. |
| Behavior-neutral docs | Compare AST after stripping docstrings. | Docstring pass did not alter behavior. | Passed. |
| UI layout | Run headless layout audit. | Concrete render object bounds fit within 1000x1000. | Passed. |
| Packaging | Run `make package`. | `dist/PacMan/` build is generated. | Passed. |
| Release ZIP | Run `make package-zip`. | `dist/PacMan-linux.zip` is generated. | Passed. |
| Packaged run | Run `./PacMan config/config.json` inside extracted package. | Packaged game starts with assets/config. | Passed. |
| Itch.io upload | Upload Linux ZIP to Itch.io. | Build available at release page. | Passed. |

## Final manual route

1. `make fclean && make install && make lint`.
2. `python3 pac-man.py` to verify the usage message.
3. `make run` to verify standard launch.
4. Start game, move, collect pacgums, eat a super-pacgum, eat a ghost, lose a life, pause/resume.
5. Use cheats to skip levels and trigger game over/victory paths.
6. Save a highscore and confirm it appears in the highscore screen.
7. Run `make package` and `make package-zip`.
8. Test the packaged executable from inside `dist/PacMan`.
