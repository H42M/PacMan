from render.RenderObj import RenderOBJ
from render.Screen import Screen

from typing import Optional
import pygame


class Entity(RenderOBJ):
    def __init__(self, screen: Screen,
                 pos: Optional[tuple[int, int]] = None,
                 size: Optional[tuple[int, int]] = None
                 ) -> None:
        self.__saved_texture: Optional[pygame.Surface] = None
        self.__current_rotation: str = 'E'
        super().__init__(screen, pos, size)

    def set_skin(self, skin_texture: Optional[pygame.Surface]
                 ) -> None:
        if skin_texture:
            self.__saved_texture = skin_texture

    def set_rotation(self, rotation: str):
        if rotation not in ['N', 'S', 'E', 'W']:
            raise ValueError(f'Invalid rotation provided: {rotation}')
        self.__current_rotation = rotation

    def render(self) -> None:
        if self.__saved_texture and self._pos and self._size:
            angle_registry = {
                'S': 270,
                'E': 0,
                'N': 90,
                'W': 180
            }
            rotated = pygame.transform.rotate(
                self.__saved_texture, angle_registry[self.__current_rotation])
            scaled = pygame.transform.scale(rotated, self._size)
            pos_tuple = (int(self._pos[0]), int(self._pos[1]))
            self._screen.screen.blit(scaled, pos_tuple)
