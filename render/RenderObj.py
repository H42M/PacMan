import pygame
from typing import Optional
from render.Screen import Screen


class RenderOBJ:

    def __init__(self, screen: Screen) -> None:
        self._screen = screen

        self._surface: Optional[pygame.Surface] = None
        self._pos: Optional[tuple[int, int]] = None

    def render(self):
        pass
