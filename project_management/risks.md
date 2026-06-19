# Risk analysis

## Risk register

| Risk | Probability | Impact | Mitigation | Final outcome |
| --- | --- | --- | --- | --- |
| External maze generator is slow or fails. | Medium | High | Isolate generator behind adapter, catch generator errors, use nearby entry/exit cells, keep maze sizes reasonable. | Mitigated; generator remains external/unmodified and the performance workaround is in place. |
| Config file is missing, malformed, or contains bad values. | High | High | Implement JSON-with-comments loader, defaults, clamping, warnings, and no-traceback behavior. | Mitigated; config errors are handled safely. |
| Two gameplay architectures diverge between teammates. | High | High | Reconcile around one source of truth: clean `Level` / `GameState` / `GameSession`; integrate UI/render selectively. | Mitigated through integration/reconciliation work. |
| UI/render work breaks gameplay state ownership. | Medium | High | Keep render as observer of gameplay state, not owner of separate gameplay logic. | Mitigated; render consumes the current gameplay objects. |
| Ghost AI is compliant but feels broken. | Medium | Medium | Start with simple autonomous movement, then improve with navigation helpers and path-aware AI. | Mitigated; ghost oscillation fixed by path-aware behavior. |
| Generated mazes contain too many unfair dead ends. | Medium | Medium | Post-process internal maze to reduce excessive dead ends without modifying external package. | Mitigated; cleanup pass added. |
| Ghosts overlap visually/logically. | Medium | Low/Medium | Reserve occupied cells during ghost movement; ignore dead ghosts for blocking. | Mitigated; active ghosts no longer stack at movement end. |
| Highscore file is missing or corrupt. | Medium | Medium | Validate JSON structure, ignore invalid entries, recover with empty list/defaults. | Mitigated; highscore system is robust. |
| Cheat mode introduces gameplay bugs. | Medium | Medium | Keep cheat state small and explicit; test god mode, ghost freeze, extra lives, and skip behavior. | Mitigated through manual testing. |
| Packaging misses assets or config files. | Medium | High | Add root packaging script/spec and smoke-test packaged build. | Pending final packaging pass. |
| README/documentation becomes outdated. | Medium | Medium | Keep project evidence current; write root README after packaging is stable. | Project evidence updated; root README pending final pass. |
| Render interpolation feels behind logical movement. | Medium | Low/Medium | Track as known limitation; avoid risky movement/collision rewrite late. | Parked unless final QA finds it game-breaking. |
| Scope creep near the end. | High | Medium | Avoid new gameplay branches; prioritize packaging, docs, tests, and compliance. | Controlled during final stretch. |

## Highest-risk areas during development

1. **External generator integration**: required by the subject and outside our control.
2. **Architecture reconciliation**: teammate UI/render work and gameplay architecture needed one shared source of truth.
3. **Gameflow correctness**: collisions, lives, game over, victory, highscores, and level transitions all interact.
4. **Final release compliance**: packaging, README, project evidence, and final QA are easy to underestimate.

## Current residual risks

| Residual risk | Status | Plan |
| --- | --- | --- |
| Packaging is not yet smoke-tested as a final build. | Open | Complete packaging branch and run packaged build test. |
| Root README must match final packaging and project-management state. | Open | Write README after packaging is stable. |
| Render interpolation can visually lag behind logic. | Accepted limitation | Mention if needed during defense; do not refactor unless it blocks gameplay. |
