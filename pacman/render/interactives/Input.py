from pacman.render.RenderObj import RenderOBJ
from pacman.render.Screen import Screen

from typing import Optional
import pygame


class Input(RenderOBJ):
    def __init__(self, screen: Screen,
                 pos: Optional[tuple[int, int]] = None,
                 size: Optional[tuple[int, int]] = None,
                 placeholder: str = "Text example"
                 ) -> None:
        super().__init__(screen, pos, size)
        self.__focus = False
        self.__placeholder = placeholder


