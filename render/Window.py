from render.Container import Container
from render.Screen import Screen
from typing import Optional
import pygame


class Window(Container):
    def __init__(self, screen: Screen,
                 way: str,
                 pos: Optional[tuple[int, int]] = None,
                 size: Optional[tuple[int, int]] = None,
                 gap: Optional[int] = None,
                 bg_color: Optional[tuple[int, int, int]] = None
                 ) -> None:
        super().__init__(screen, way, pos, size, gap)
        self.__bg_color = bg_color

    def render(self) -> None:
        if self._pos and self._size:
            # window = pygame.Surface(self._size)
            # window.set_colorkey(self.__bg_color
            #                     if self.__bg_color else (0, 0, 0))
            pygame.draw.rect(
                # window,
                self._screen.screen,
                self.__bg_color if self.__bg_color else (0, 0, 0),
                (*self._pos, *self._size),
                border_radius=10
            )
            pygame.draw.rect(
                self._screen.screen,
                (255, 255, 255),
                (*self._pos, *self._size),
                width=2,
                border_radius=10
            )
        super().render()
