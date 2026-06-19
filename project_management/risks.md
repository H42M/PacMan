# Risk analysis

This file records the main project risks, mitigations, and final status.

| Risk | Impact | Mitigation | Final status |
| --- | --- | --- | --- |
| External maze generator API/performance issues. | Could block level generation or make the game slow. | Isolated the generator behind `maze_adapter.py`, handled failures cleanly, used nearby entry/exit cells, and kept generated sizes reasonable. | Mitigated. |
| Invalid or missing config values. | Could crash the game during evaluation. | Added typed config parsing, warnings, defaults, clamping, unknown-key ignoring, and clean CLI handling. | Mitigated. |
| Divergent teammate architectures. | Could cause merge conflicts or duplicated gameplay models. | Promoted one clean gameplay architecture as source of truth and selectively integrated UI/render pieces. | Resolved. |
| Ghost AI oscillation. | Ghosts could look broken even if technically autonomous. | Added shared navigation helpers, path-aware movement, and basic distinct ghost personalities. | Fixed. |
| Excessive maze dead ends. | Smarter ghosts could make the game unfair. | Added internal dead-end cleanup after generation without modifying the external package. | Mitigated. |
| Active ghost overlap. | Visual/gameplay clarity issue. | Added per-tick active ghost position reservation; dead ghosts do not block. | Fixed. |
| Highscore file corruption. | Could crash score display/save flow. | Highscore loader filters invalid data and safely recovers from missing/corrupt files. | Mitigated. |
| Render/gameplay interpolation desync. | Collisions can sometimes feel slightly ahead of visuals. | Assessed as a known limitation; deeper fix would require risky movement/render architecture changes late in the project. | Accepted limitation. |
| Non-functional UI entry. | Reviewer could click a fake Settings feature and see unfinished behavior. | Hid Settings from the main menu while keeping the code reversible. | Fixed. |
| Missing docstrings. | Formal compliance risk. | Added concise PEP 257-style docstrings to all classes/functions/methods and verified through AST audit. | Fixed. |
| Packaging path/data issues. | Release build could miss assets/config. | Added PyInstaller spec including `assets/` and `config/`, Makefile package targets, and packaged-build smoke testing. | Mitigated. |
| Scope creep near defense. | Could destabilize a working game. | Parked non-blocking architecture work and focused on compliance, packaging, and QA. | Controlled. |

## Residual limitations

| Limitation | Reason accepted |
| --- | --- |
| Render interpolation can visually lag behind logical tile movement. | Current behavior is logically consistent. A deeper fix would require larger architecture changes than were justified at final stage. |
| Ghost AI is not arcade-perfect. | The subject requires autonomous chase/flee behavior, not exact original Pac-Man AI. The implementation is path-aware and distinct enough for project scope. |
| Linux build only. | The release package was built on Linux, and PyInstaller builds are platform-specific. This matches the available development/review environment. |
