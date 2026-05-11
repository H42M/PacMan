from render.RenderObj import RenderOBJ
from render.Screen import Screen

from typing import Optional
import pygame


class Entity(RenderOBJ):
    def __init__(self, screen: Screen,
                 pos: Optional[tuple[int, int]] = None,
                 size: Optional[tuple[int, int]] = None
                 ) -> None:
        self.__texture: Optional[pygame.Surface] = None
        super().__init__(screen, pos, size)

    def set_skin(self, skin_texture: Optional[pygame.Surface]
                 ) -> None:
        if skin_texture:
            self.__texture = skin_texture

    def render(self) -> None:
        if self.__texture and self._pos and self._size:
            pos_tuple = (int(self._pos[0]), int(self._pos[1]))
            self.__texture = pygame.transform.scale(self.__texture, self._size)
            self._screen.screen.blit(self.__texture, pos_tuple)
