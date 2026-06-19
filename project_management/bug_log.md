# Bug log

This log records notable bugs and fixes. Minor implementation mistakes fixed immediately during development are not all listed here.

| Bug | Severity | Status | Fix summary | Notes |
| --- | --- | --- | --- | --- |
| Ghost AI could oscillate instead of pathfinding to Pac-Man. | Medium | Fixed | Replaced local greedy neighbor choice with path-aware movement using shared navigation helpers. | Fixed during ghost AI quality pass. |
| Generated mazes could contain too many unfair dead ends. | Medium | Fixed | Added internal maze post-processing to reduce excessive dead ends without modifying the external generator. | Improves playability with smarter ghosts. |
| Active ghosts could overlap. | Medium | Fixed | Added active ghost position reservation during ghost movement; dead ghosts do not block cells. | Fixed during final cleanup. |
| Game could crash before `make install` due to missing dependencies. | Low | Fixed | Moved/wrapped imports in `pac-man.py` so missing dependencies print a clear install message. | Prevents traceback before dependency setup. |
| Default config did not match final compliance expectations. | Low | Fixed | Updated default lives/seeds and first level sizing during final compliance cleanup. | Keeps launch defaults aligned with expected gameplay. |
| God mode could resume gameplay unexpectedly. | Medium | Fixed | Cheat and pause flow were stabilized so toggles do not accidentally resume the game. | Fixed during cheat/menu work. |
| Cheat menu Back button returned to main menu instead of pause menu. | Medium | Fixed | Pause/cheat menu navigation was corrected. | Fixed during menu/cheat integration. |
| Opening cheat menu once could cause pause menu to reopen as cheat menu. | Medium | Fixed | Pause menu state is reset/rebuilt correctly. | Fixed during menu/cheat integration. |
| End-screen Back to Menu/highscore save behavior was unclear. | Low | Fixed | End-screen flow was clarified and integrated with highscore behavior. | No longer tracked as open. |
| Legacy root `Errors.py` module remained after architecture cleanup. | Low | Fixed | Moved `LoadingError` locally into render config and deleted unused root error module. | Final cleanup. |
| Non-functional Settings screen was player-facing. | Low | Fixed | Removed the main-menu settings entry/callback; settings state registration remains intact. | Avoids exposing fake options. |
| Docstring coverage was incomplete. | Low | Fixed | Added concise one-line docstrings to every class/function/method and verified with AST audits. | Behavior-neutral AST comparison passed. |
| UI layout could regress during final menu cleanup. | Low | Fixed | Ran headless layout audit for menu, highscores, instructions, settings, game over, and play states. | All concrete bounds fit the screen. |
| Packaging initially had no release workflow. | Medium | Fixed | Added PyInstaller spec, package Makefile targets, Linux ZIP build, and Itch.io upload. | Final release workflow completed. |

## Accepted known limitations

| Limitation | Reason accepted |
| --- | --- |
| Render interpolation can visually lag behind logical tile movement. | Proper fix would require movement/collision/render architecture changes late in the project. Current behavior is logically consistent and not a core subject blocker. |
| Ghost AI is not arcade-perfect. | The subject requires autonomous chase/flee behavior, not exact original Pac-Man AI. Current movement is path-aware and distinct enough for project scope. |
| Release build targets Linux only. | PyInstaller builds are platform-specific, and the final build was produced for the Linux review environment. |
