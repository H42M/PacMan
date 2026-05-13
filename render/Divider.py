from render.RenderObj import RenderOBJ
from render.Screen import Screen

import pygame
from typing import Optional


class Divider(RenderOBJ):
    def __init__(self, screen: Screen,
                 color: Optional[tuple[int, int, int]] = None,
                 pos: Optional[tuple[int, int]] = None,
                 size: Optional[tuple[int, int]] = None) -> None:
        super().__init__(screen, pos, size)
        self.__color = color if color else (255, 255, 255)

    def render(self) -> None:
        if self.pos and self.size:
            pygame.draw.rect(
                self._screen.screen,
                self.__color,
                (*self.pos, *self.size)
            )
