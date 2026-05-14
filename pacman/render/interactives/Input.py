from pacman.render.interactives.Button import Button
from pacman.render.Screen import Screen

from typing import Optional
import pygame


class Input(Button):
    def __init__(self, screen: Screen,
                 pos: Optional[tuple[int, int]] = None,
                 size: Optional[tuple[int, int]] = None,
                 placeholder: str = "Text example"
                 ) -> None:
        super().__init__(screen, placeholder, pos, size)
        self.__focus = False
        self.__placeholder = placeholder
        self.__value = ""
        self._color = None

    def handle_key(self, event: pygame.event.Event) -> None:
        if not self.__focus:
            return

        if event.key == pygame.K_BACKSPACE:
            self.__value = self.__value[:-1]
        elif event.key == pygame.K_RETURN:
            self.__focus = False
        else:
            special = "!@#$%^&*()-_+= "
            char: str = event.unicode
            self.__value += char if char.isalnum() or char in special else ''

    def execute(self) -> None:
        self.__focus = True

    def render(self) -> None:
        if self.__focus:
            self._text = self.__value + '_'
        elif self.__value:
            self._text = self.__value
        else:
            self._text = self.__placeholder

        self._color = (255, 100, 0) if self.__focus else None

        super().render()

    @property
    def focus(self) -> bool:
        return self.__focus

    @focus.setter
    def focus(self, value: bool) -> None:
        self.__focus = value
