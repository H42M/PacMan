"""Main pygame application loop for Pac-Man."""

import os
import pygame

from pacman.constants import WINDOW_HEIGHT, WINDOW_WIDTH
from pacman.game_config import GameConfig
from pacman.maze_adapter import MazeGenerationError
from pacman.level import build_level
from pacman.game_state import GameState


from pacman.render.RenderConfig import RenderConfig
from pacman.render.Screen import Screen

from pacman.states.base_state import StateManager
from pacman.states.menu_state import MenuState
from pacman.states.play_state import PlayState
from pacman.states.game_over_state import GameOverState
from pacman.states.setting_state import SettingsState


def run(config: GameConfig) -> int:
    """Run the Pac-Man application."""
    print()
    print(f"Starting Pac-Man with config: {config}")
    try:
        # level building and maze generation
        def create_play_state(screen: Screen,
                              manager: StateManager) -> PlayState:
            level = build_level(config, 0)
            game = GameState.from_level(config, level)
            return PlayState(screen, manager, game)

        # pygame initialization
        os.environ["SDL_VIDEO_WINDOW_POS"] = "100,100"
        RenderConfig.init(
            (WINDOW_WIDTH, WINDOW_HEIGHT),
            (config.levels[0].width, config.levels[0].height),
        )  # TODO: revisit when levels can use different maze dimensions.

        screen = Screen()
        state_manager = StateManager(
            screen,
            StateManager.MENU,
            {
                StateManager.MENU: (
                    lambda screen, manager: MenuState(screen, manager)
                ),
                StateManager.SETTINGS: (
                    lambda screen, manager: SettingsState(screen, manager)
                ),
                StateManager.PLAYING: (
                    lambda screen, manager: create_play_state(screen, manager)
                ),
                StateManager.GAMEOVER: (
                    lambda screen, manager: GameOverState(screen, manager)
                ),
                StateManager.VICTORY: (
                    lambda screen, manager: GameOverState(
                        screen, manager, GameOverState.WIN_SCREEN)
                )
            }
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
