from pacman.states.base_state import StateManager
from pacman.states.menu_state import MenuState
from pacman.render.Screen import Screen

import pygame


if __name__ == '__main__':
    menu = MenuState()
    manager = StateManager(menu)

    screen = Screen()

    while True:
        manager.handle_event(pygame.event.get())
        manager.update()
        manager.render(screen)
