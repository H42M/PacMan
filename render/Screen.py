
from __future__ import annotations
from typing import TYPE_CHECKING

import pygame
from render.GameLoader import GameLoader

if TYPE_CHECKING:
    from render.buttons.Button import Button


class Screen:
    def __init__(self) -> None:
        pygame.init()
        self.__screen_size = GameLoader.screen_size
        self.__screen_name = 'PACMAN'
        self.__screen = pygame.display.set_mode(
            self.__screen_size
        )
        self.__clock = pygame.time.Clock()
        pygame.display.set_caption(self.__screen_name)
        self.__background = None
        self.__clickables: list[Button] = []

    def clear(self) -> None:
        if self.__background:
            self.__screen.blit(self.__background, (0, 0))
        else:
            self.__screen.fill((0, 0, 0))

    def flip(self) -> None:
        self.__clock.tick(360)
        pygame.display.flip()

    def handle_events(self) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.__clickables:
                    if button.is_clicked(mouse_pos):
                        button.execute()

        for button in self.__clickables:
            button.update_hover(mouse_pos)
        return True

    def record_clickable(self, obj: Button):
        self.__clickables.append(obj)

    # GETTERS / SETTERS

    @property
    def screen(self) -> pygame.Surface:
        return self.__screen

    @screen.setter
    def screen(self, value: pygame.Surface) -> None:
        self.__screen = value
