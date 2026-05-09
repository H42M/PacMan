import pygame
from typing import Optional
from render.Screen import Screen


class RenderOBJ:

    def __init__(self, screen: Screen,
                 pos: Optional[tuple[int, int]] = None,
                 size: Optional[tuple[int, int]] = None) -> None:
        self._screen = screen

        self._surface: Optional[pygame.Surface] = None
        self._pos: Optional[tuple[int, int]] = pos
        self._size: Optional[tuple[int, int]] = size

    def render(self):
        pass
