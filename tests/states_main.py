from pacman.states.base_state import StateManager
from pacman.render.Screen import Screen
from pacman.render.RenderLoader import RenderLoader

import pygame


if __name__ == '__main__':
    # TODO: init gameloader with user's provided data
    RenderLoader.init(screen_size=(800, 800), maze_size=(20, 20))
    RenderLoader.load_asset('background', 'assets/sprites/pacman_maze_bg.jpg')

    screen = Screen()
    screen.background = RenderLoader.assets['background']
    manager = StateManager(screen, 'MENU')

    while manager.handle_events(pygame.event.get()):
        manager.update()
        manager.render(screen)
