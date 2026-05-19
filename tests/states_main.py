from pacman.states.base_state import StateManager
from pacman.render.Screen import Screen
from pacman.render.RenderConfig import RenderConfig

import pygame


if __name__ == '__main__':
    # TODO: init gameloader with user's provided data
    RenderConfig.init(screen_size=(800, 800), maze_size=(20, 20))
    RenderConfig.load_asset('background', 'assets/sprites/pacman_maze_bg.jpg')

    screen = Screen()
    screen.background = RenderConfig.assets['background']
    manager = StateManager(screen, 'MENU')

    while manager.handle_events(pygame.event.get()):
        manager.update()
        manager.render()
