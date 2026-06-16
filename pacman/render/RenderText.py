from pacman.render.RenderObj import RenderOBJ

import pygame
from typing import Optional
from pacman.render.Screen import Screen


class RenderText(RenderOBJ):
    """Render text inside a rectangle."""

    def __init__(self,
                 screen: Screen,
                 text: str,
                 pos: Optional[tuple[int, int]] = None,
                 size: Optional[tuple[int, int]] = None,
                 bg_color: Optional[tuple[int, int, int]] = None,
                 font_color: Optional[tuple[int, int, int]] = None,
                 font_size: Optional[int] = None,
                 font_family: Optional[str] = None,
                 ) -> None:
        """Initialize the text object."""
        super().__init__(screen, pos, size)
        if not font_size:
            self.__font_size = 28
        else:
            self.__font_size = font_size
        self.__font = pygame.font.Font(font_family, self.__font_size)
        self.__text = text

        self.__bg_color = bg_color
        self.__font_color = font_color if font_color else (255, 255, 255)

    def render(self) -> None:
        """Render the text to the screen."""
        if self._pos and self._size:
            text_surf = self.__font.render(self.__text, True,
                                           self.__font_color, self.__bg_color)
            text_rect = text_surf.get_rect(center=(self._pos[0] + self._size[0]
                                                   // 2,
                                                   self._pos[1] + self._size[1]
                                                   // 2))
            self._screen.screen.blit(text_surf, text_rect)

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, value: str) -> None:
        self.__text = value
