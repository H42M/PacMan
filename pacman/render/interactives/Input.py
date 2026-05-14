from pacman.render.interactives.Button import Button
from pacman.render.Screen import Screen

from typing import Optional
import pygame


class Input(Button):
    """Input text objetc."""
    def __init__(self, screen: Screen,
                 placeholder: str = "Text example",
                 base_color: Optional[tuple[int, int, int]] = None,
                 focus_color: Optional[tuple[int, int, int]] = None,
                 pos: Optional[tuple[int, int]] = None,
                 size: Optional[tuple[int, int]] = None,
                 ) -> None:
        """Initialize Input."""
        super().__init__(screen, placeholder, pos, size)
        self.__focus = False
        self.__placeholder = placeholder
        self.__value = ""
        self.__base_color = base_color if base_color else (255, 0, 0)
        self.__focus_color = focus_color if focus_color else (255, 100, 10)
        self._color = base_color

    def handle_key(self, event: pygame.event.Event) -> None:
        """Handle key interaction."""
        if not self.__focus:
            return

        if event.key == pygame.K_BACKSPACE:
            self.__value = self.__value[:-1]
        elif event.key == pygame.K_RETURN:
            self.__focus = False
        else:
            if event.unicode.isprintable():
                self.__value += event.unicode
            else:
                self.__focus = False

    def execute(self) -> None:
        """Set focus on input text element."""
        self.__focus = True

    def render(self) -> None:
        """Display input text element on screen"""
        if self.__focus:
            self._text = self.__value + '_'
        elif self.__value:
            self._text = self.__value
        else:
            self._text = self.__placeholder

        self._color = self.__focus_color if self.__focus else self.__base_color

        super().render()

    @property
    def focus(self) -> bool:
        return self.__focus

    @focus.setter
    def focus(self, value: bool) -> None:
        self.__focus = value

    @property
    def base_color(self) -> tuple[int, int, int]:
        return self.__base_color

    @base_color.setter
    def _base_color(self, value: tuple[int, int, int]) -> None:
        self.__base_color = value

    @property
    def focus_color(self) -> tuple[int, int, int]:
        return self.__focus_color

    @focus_color.setter
    def _focus_color(self, value: tuple[int, int, int]) -> None:
        self.__focus_color = value
