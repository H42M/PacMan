"""Main pygame application loop for Pac-Man."""

import os
import pygame

from pacman.constants import WINDOW_HEIGHT, WINDOW_WIDTH

from pacman.level import build_level
from pacman.game_state import GameState


from pacman.render.RenderConfig import RenderConfig
from pacman.render.Screen import Screen

from pacman.states.base_state import StateManager
from pacman.states import MenuState, PlayState, SettingsState, GameOverState

from pacman.config_loader import load_config
from sys import argv

if __name__ == '__main__':
    config = load_config(argv[1])
    # def run(config: GameConfig) -> int:
    """Run the Pac-Man application."""
    print()
    print(f"Starting Pac-Man with config: {config}")
    try:
        # level building and maze generation
        level = build_level(config, 0)
        game = GameState.from_level(config, level)
        print()
        print(game)
        print()

        # pygame initialization
        os.environ["SDL_VIDEO_WINDOW_POS"] = "100,100"
        RenderConfig.init(
            (WINDOW_WIDTH, WINDOW_HEIGHT),
            (game.level.maze.width, game.level.maze.height),
        )
        screen = Screen()
        state_manager = StateManager(
            screen,
            StateManager.GAMEOVER,
            {
                StateManager.MENU: (
                    lambda screen, manager: MenuState(screen, manager)
                ),
                StateManager.SETTINGS: (
                    lambda screen, manager: SettingsState(screen, manager)
                ),
                StateManager.PLAYING: (
                    lambda screen, manager: PlayState(screen, manager, game)
                ),
                StateManager.GAMEOVER: (
                    lambda screen, manager: GameOverState(screen, manager)
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
    except Exception as e:
        print(f'Error: {e}')
