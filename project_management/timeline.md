# Timeline

This timeline summarizes the planned progression and the actual implementation order used for the PacMan project.

## Planned phases

| Phase | Goal | Planned owner(s) |
| --- | --- | --- |
| M0 - Repository and tooling | Project skeleton, Makefile workflow, entrypoint, linting setup. | Hugo |
| M1 - Config and maze adapter | JSON configuration, robust error handling, A-Maze-ing adapter. | Hugo |
| M2 - Minimal playable game | Runtime level model, player state, visible movement, pellets and scoring. | Hugo |
| M3 - Ghosts and game outcomes | Ghost state, autonomous movement, collisions, lives, game over, frightened mode. | Hugo / Both |
| M4 - UI and game flow | Menus, HUD, pause, instructions, game over/victory, visual integration. | Nico / Both |
| M5 - Progression and review tools | Highscores, multiple levels, timer, score/life carryover, cheat mode. | Both |
| M6 - Finalization | Ghost AI quality pass, cleanup, docs, packaging, defense QA. | Both |

## Actual progression

| Order | Delivered work | Branch / area | Outcome |
| --- | --- | --- | --- |
| 1 | Project skeleton and Makefile workflow. | `feature/project-skeleton` | Basic project entry and developer commands established. |
| 2 | Config loader with defaults, clamping, comments, and no-traceback handling. | `feature/config-loader` | Config-driven game setup completed. |
| 3 | External A-Maze-ing integration behind an adapter. | `feature/maze-adapter` | Generator isolated from the rest of the codebase. |
| 4 | Runtime `Level` model. | `feature/level-bootstrap` | Generated maze data became usable by gameplay systems. |
| 5 | Mutable gameplay state and player movement. | `feature/core-gameplay` | First playable logical movement slice. |
| 6 | Rendering bridge. | `feature/gameplay-render-bridge` | Maze and player became visible from the clean gameplay model. |
| 7 | Pacgums, super-pacgums, and scoring. | `feature/player-pellets-score` | Collection and score rules implemented. |
| 8 | UI/gameflow reconciliation. | integration branch | UI/render work was aligned with the clean gameplay architecture. |
| 9 | Ghost state and autonomous movement. | `feature/ghost-state`, `feature/ghost-ai` | Four ghosts spawned, rendered, and moved autonomously. |
| 10 | Timed Pac-Man movement and queued turns. | `feature/player-movement-flow` | Movement became closer to expected Pac-Man behavior. |
| 11 | Collisions, lives, timer, game over, level clear. | `feature/game-outcomes-flow` | Core win/loss loop completed. |
| 12 | Frightened mode and edible ghost respawn. | `feature/ghosts-frightened-mode` | Power-pellet loop completed. |
| 13 | Persistent highscores. | `feature/highscores` | Top-10 JSON highscore system integrated into end screens and menu. |
| 14 | Multi-level progression. | `feature/level-progression` | Ten-level campaign with score/life carryover. |
| 15 | Cheat mode. | `feature/cheat-mode` | Review tools added for peer evaluation. |
| 16 | Ghost AI quality pass and maze dead-end cleanup. | `feature/ghost-ai` | Path-aware ghost behavior and playability improvements. |
| 17 | Final compliance cleanup. | docs/final branches | Ghost AI merge, config/CLI cleanup, dependency handling, ghost overlap prevention, `Errors.py` cleanup, docstrings, settings hiding, layout audit, and project evidence completed; packaging, root README, and final QA remain. |

## Visual timeline

```mermaid
gantt
    title PacMan project timeline
    dateFormat  YYYY-MM-DD
    axisFormat  %d %b

    section Foundation
    Repo and tooling              :done, m0, 2026-05-08, 3d
    Config loader                 :done, m1a, after m0, 4d
    Maze adapter                  :done, m1b, after m1a, 4d
    Level bootstrap               :done, m2a, after m1b, 3d

    section Gameplay
    Core gameplay                 :done, m2b, 2026-05-28, 4d
    Render bridge                 :done, m2c, after m2b, 3d
    Pellets and score             :done, m2d, after m2c, 3d
    Ghosts and outcomes           :done, m3, 2026-06-04, 6d
    Frightened mode               :done, m3b, after m3, 3d

    section Progression and UI
    Highscores                    :done, m5a, 2026-06-10, 3d
    Level progression             :done, m5b, after m5a, 3d
    Cheat mode                    :done, m5c, after m5b, 3d
    UI/gameflow integration       :done, m4, 2026-06-03, 10d

    section Finalization
    Ghost AI quality pass         :done, m6a, 2026-06-17, 2d
    Cleanup and docs              :done, m6b, 2026-06-18, 4d
    Packaging and final QA        :active, m6c, after m6b, 3d
```

## Changes compared with the original plan

- The first architecture plan was intentionally adjusted after teammate work diverged: the team created a clean foundation and selectively integrated UI/render work instead of keeping two incompatible gameplay models.
- Level progression and cheat mode were split into separate branches to reduce risk.
- Ghost AI improvements were added late because the first autonomous movement version was functional but visually too oscillatory.
- Project evidence and docstrings were finalized after gameplay and UI flow stabilized.
- Packaging and root README work remain deliberately last so they can describe the actual release build.
