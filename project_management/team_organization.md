# Team organization

This project was developed by two teammates: Hugo and Nico.

## Responsibilities

| Area | Main contributor(s) | Notes |
| --- | --- | --- |
| Repository/tooling | Hugo | Makefile workflow, dependency setup, linting, entry point. |
| Configuration | Hugo | JSON config loading, defaults, validation, clamping, comments. |
| Maze adapter | Hugo | Assigned A-Maze-ing package integration and internal maze representation. |
| Gameplay architecture | Hugo | `Level`, `GameState`, `GameSession`, player movement, score, lives, outcomes. |
| Ghost/gameplay systems | Hugo | Ghost state, movement, frightened mode, AI quality pass, overlap prevention. |
| UI/render/menu work | Nico / Both | Rendering, menus, HUD, gameflow screens, visual integration. |
| Integration | Both | Aligning gameplay source of truth with render/UI work. |
| Highscores/progression/cheats | Hugo / Both | Persistent scores, campaign flow, review helpers. |
| Documentation/evidence | Both | README, project-management evidence, testing records, final report. |
| Packaging/release | Hugo / Both | PyInstaller workflow, Linux archive, Itch.io upload, final smoke test. |

## Workflow

- Work was organized around feature branches and merged through `develop`.
- Branches were scoped around one technical goal when possible.
- Risky integration work was handled separately from feature implementation.
- UI/render work was integrated while preserving the gameplay state model as the source of truth.
- Late-stage work prioritized compliance, stability, and defense readiness over new features.

## Review process

- Important gameplay changes were manually tested after implementation.
- `make lint` was used to check flake8 and mypy compliance.
- Compile checks were used for syntax-level validation.
- Final UI layout was checked through a headless Pygame audit.
- The packaged Linux build was tested after generation.

## Communication notes

The project involved several scope and architecture adjustments. The final approach kept the collaboration constructive by separating ownership: gameplay rules and state stayed centralized, while UI/render work was integrated as presentation and gameflow layers around that model.
