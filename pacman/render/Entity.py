from pacman.render.RenderObj import RenderOBJ
from pacman.render.Screen import Screen

from typing import Optional
import pygame


class RenderEntity(RenderOBJ):
    """Entity class.
    Used to display entities like pacman or ghosts.
    Can be rotated if needed.
    Initial direction must be east"""
    def __init__(self, screen: Screen,
                 pos: Optional[tuple[int, int]] = None,
                 size: Optional[tuple[int, int]] = None
                 ) -> None:
        """Initialize Entity class."""
        self.__saved_texture: Optional[pygame.Surface] = None
        self.__current_rotation: str = 'E'
        super().__init__(screen, pos, size)

    def set_skin(self, skin_texture: Optional[pygame.Surface]
                 ) -> None:
        """Set creature skin."""
        if skin_texture:
            self.__saved_texture = skin_texture

    def set_rotation(self, rotation: str) -> None:
        """Set creature rotation"""
        if rotation not in ['N', 'S', 'E', 'W']:
            raise ValueError(f'Invalid rotation provided: {rotation}')
        self.__current_rotation = rotation

    def render(self) -> None:
        """Display the creature on screen based on his direction"""
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
