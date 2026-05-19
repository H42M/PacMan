"""Main pygame application loop for Pac-Man."""

import pygame
from pacman.constants import WINDOW_HEIGHT, WINDOW_WIDTH
from pacman.game_config import GameConfig

from pacman.states.base_state import StateManager
from pacman.render.Screen import Screen
from pacman.render.RenderLoader import RenderLoader


def run(config: GameConfig):
    # TODO: init gameloader with Gameconfig data
    print(f"Starting Pac-Man with config: {config}")
    try:
        RenderLoader.init(screen_size=(WINDOW_WIDTH, WINDOW_HEIGHT),
                          maze_size=(20, 20))
        RenderLoader.load_asset('background',
                                'assets/sprites/pacman_maze_bg.jpg')

        screen = Screen()
        screen.background = RenderLoader.assets['background']
        manager = StateManager(screen, 'MENU')

        while manager.handle_events(pygame.event.get()):
            manager.update()
            manager.render()
    except pygame.error as e:
        print(e)
        return 1
    finally:
        pygame.quit()
    return 0
