import pygame
from typing import Optional


class RenderOBJ:

    def __init__(self, screen: pygame.Surface) -> None:
        self.__screen = screen

        self.__surface: Optional[pygame.Surface] = None
        self.__pos: Optional[tuple[int, int]] = None

    def render(self):
        pass
