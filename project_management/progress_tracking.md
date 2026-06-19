# Progress tracking

This file summarizes project progress by milestone and gives a defense-friendly snapshot of the work completed.

## Milestone board

| Milestone | Status | Main deliverables |
| --- | --- | --- |
| M0 - Repository and tooling | Done | Makefile, virtual environment workflow, entrypoint, lint/type-check commands. |
| M1 - Config and maze adapter | Done | JSON-with-comments loader, defaults/clamping, A-Maze-ing adapter, `PERFECT=False`. |
| M2 - Minimal playable game | Done | Runtime level model, player state, movement, render bridge, pellets and scoring. |
| M3 - Ghosts and power mode | Done | Ghost state, autonomous movement, collisions/lives, frightened mode, dead ghost respawn. |
| M4 - UI and game flow | Done | Main menu, highscores view, instructions, HUD, pause, game over/victory, name entry. |
| M5 - Progression and review tools | Done | 10 levels, timer, score/life carryover, persistent highscores, cheat mode. |
| M6 - Finalization | In progress | Ghost AI, compliance cleanup, docstrings, project evidence, and UI cleanup done; packaging, root README, and final QA remain. |

## Kanban snapshot

| Done | In progress | Remaining before defense |
| --- | --- | --- |
| Config loader |  | Packaging/release build |
| Maze adapter |  | Root README finalization |
| Level bootstrap |  | Final QA / defense rehearsal |
| Core gameplay |  |  |
| Render bridge |  |  |
| Pellets and scoring |  |  |
| Ghost state and AI |  |  |
| Frightened mode |  |  |
| Game outcomes |  |  |
| Highscores |  |  |
| Level progression |  |  |
| Cheat mode |  |  |
| Ghost overlap fix |  |  |
| Missing dependency handling |  |  |
| Legacy `Errors.py` cleanup |  |  |
| Default config compliance fix |  |  |
| Docstring compliance pass |  |  |
| Project-management evidence |  |  |
| Non-functional settings menu entry hidden |  |  |
| Headless layout audit |  |  |

## Branch summary

| Branch / area | Purpose | Final state |
| --- | --- | --- |
| `feature/config-loader` | Config models, comments, defaults, safe handling. | Merged. |
| `feature/maze-adapter` | External A-Maze-ing integration behind adapter. | Merged. |
| `feature/level-bootstrap` | Runtime level model from config + generated maze. | Merged. |
| `feature/core-gameplay` | Mutable player/game state and movement legality. | Merged. |
| `feature/gameplay-render-bridge` | Render visible maze and player from gameplay state. | Merged. |
| `feature/player-pellets-score` | Collectibles and score. | Merged. |
| `integration/ui-gameflow-reconciliation` | Align UI/render with clean gameplay model. | Merged/promoted as foundation. |
| `feature/ghost-state` | Ghost dataclass/state/spawns/rendering. | Merged. |
| `feature/ghost-ai` | Autonomous ghost movement, later path-aware AI and dead-end cleanup. | Merged. |
| `feature/player-movement-flow` | Timed movement and queued turns. | Merged. |
| `feature/game-outcomes-flow` | Life loss, game over, level clear, timer. | Merged. |
| `feature/ghosts-frightened-mode` | Super-pacgum frightened mode and edible ghost respawn. | Merged. |
| `feature/highscores` | JSON highscore persistence and end-screen saving. | Merged. |
| `feature/level-progression` | 10-level campaign and session carryover. | Merged. |
| `feature/cheat-mode` | Review tools: god mode, level skip, ghost freeze, extra life. | Merged. |
| Final cleanup branches | Documentation, packaging, docstrings, final QA. | Evidence, docstrings, UI cleanup done; packaging, root README, and final QA remain. |

## Progress notes

- Most defense-critical gameplay requirements are implemented and manually validated.
- Remaining work is release work rather than new gameplay design.
- New gameplay branches should be avoided unless final QA finds a real blocker.
