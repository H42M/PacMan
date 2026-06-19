"""Main pygame application loop for Pac-Man."""

import os
import pygame

from pacman.constants import WINDOW_HEIGHT, WINDOW_WIDTH
from pacman.game_config import GameConfig
from pacman.maze_adapter import MazeGenerationError
from pacman.game_session import GameSession

from pacman.render.RenderConfig import RenderConfig
from pacman.render.Screen import Screen

from pacman.states.base_state import StateManager
from pacman.states.menu_state import MenuState
from pacman.states.play_state import PlayState
from pacman.states.game_over_state import GameOverState
from pacman.states.setting_state import SettingsState
from pacman.states.highscore_state import HighScoreState
from pacman.states.instruction_state import InstructionState


def run(config: GameConfig) -> int:
    """Run the Pac-Man application."""
    try:
        # level building and maze generation
        def create_play_state(screen: Screen,
                              manager: StateManager) -> PlayState:
            """Create a fresh play state for the current session."""
            session = GameSession.from_config(config)
            game = session.create_game_state()
            return PlayState(screen, manager, game, session=session)

        # pygame initialization
        def final_score_from_payload(payload: dict[str, object]) -> int:
            """Return the final score stored in a state payload."""
            final_score = payload.get("final_score", 0)
            if isinstance(final_score, int):
                return final_score
            return 0
        os.environ["SDL_VIDEO_WINDOW_POS"] = "100,100"
        RenderConfig.init(
            (WINDOW_WIDTH, WINDOW_HEIGHT),
            (config.levels[0].width, config.levels[0].height),
        )

        screen = Screen()
        state_manager = StateManager(
            screen,
            StateManager.MENU,
            {
                StateManager.MENU: (
                    lambda screen, manager, _payload: MenuState(
                        screen, manager, config.highscore_filename)
                ),
                StateManager.SETTINGS: (
                    lambda screen, manager, _payload: SettingsState(
                        screen, manager)
                ),
                StateManager.HIGHSCORE: (
                    lambda screen, manager, _payload: HighScoreState(
                        screen, manager,
                        highscore_path=config.highscore_filename)
                ),
                StateManager.INSTRUCTIONS: (
                    lambda screen, manager, _payload: InstructionState(
                        screen, manager)
                ),
                StateManager.PLAYING: (
                    lambda screen, manager, _payload: create_play_state(
                        screen, manager)
                ),
                StateManager.GAMEOVER: (
                    lambda screen, manager, payload: GameOverState(
                        screen,
                        manager,
                        final_score=final_score_from_payload(payload),
                        highscore_path=config.highscore_filename,
                    )
                ),
                StateManager.VICTORY: (
                    lambda screen, manager, payload: GameOverState(
                        screen,
                        manager,
                        GameOverState.WIN_SCREEN,
                        final_score=final_score_from_payload(payload),
                        highscore_path=config.highscore_filename,
                    )
                ),
            },
        )

        # game loop
        is_running = True
        while is_running:
            events = pygame.event.get()

            try:
                is_running = state_manager.handle_events(events)
            except SystemExit:
                is_running = False

            if not is_running:
                break

            state_manager.update()
            state_manager.render()

    # error handling
    except pygame.error as error:
        print()
        print("Error:")
        print(error)
        print()
        return 1
    except MazeGenerationError as error:
        print()
        print("Error:")
        print(error)
        print()
        return 1
    except ValueError as error:
        print()
        print("Error:")
        print(error)
        print()
        return 1
    finally:
        pygame.quit()
    return 0
