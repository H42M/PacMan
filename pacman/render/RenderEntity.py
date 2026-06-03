from typing import Optional

import pygame

from pacman.render.Animator import Animator
from pacman.render.RenderObj import RenderOBJ
from pacman.render.Screen import Screen


class RenderEntityError(Exception):
    pass


class RenderEntity(RenderOBJ):
    """Render a static or animated sprite.

    This class is intentionally gameplay-agnostic. It does not own or import
    player, ghost, world, or maze logic.
    """

    def __init__(self, screen: Screen) -> None:
        super().__init__(screen)
        self.__static: Optional[pygame.Surface] = None
        self.__animator: Optional[Animator] = None
        self.__dir_animators: Optional[dict[str, Animator]] = None
        self.__rotation: str = 'E'

    def set_skin(self, texture: Optional[pygame.Surface]) -> None:
        if texture:
            self.__static = texture
        else:
            raise RenderEntityError('No skin provided')

    def set_animator(self, animator: Animator) -> None:
        self.__animator = animator

    def set_dir_animators(self, animators: dict[str, Animator]) -> None:
        self.__dir_animators = animators

    def set_rotation(self, direction: str) -> None:
        d = direction.upper()
        if d not in ('N', 'S', 'E', 'W'):
            raise ValueError(f'Invalid rotation: {direction!r}')
        self.__rotation = d

    def set_progress(self, progress: float) -> None:
        if self.__animator:
            self.__animator.set_frame_by_progress(progress)

    def tick_animator(self) -> None:
        if self.__dir_animators:
            anim = self.__dir_animators.get(self.__rotation)
            if anim:
                anim.tick()
        elif self.__animator:
            self.__animator.tick()

    def render(self) -> None:
        if not (self._pos and self._size):
            return

        texture = self.__resolve_texture()
        if texture is None:
            return

        if self.__dir_animators:
            scaled = pygame.transform.scale(texture, self._size)
        else:
            angles = {'E': 0, 'W': 180, 'N': 90, 'S': 270}
            angle = angles.get(self.__rotation, 0)
            rotated = pygame.transform.rotate(texture, angle)
            scaled = pygame.transform.scale(rotated, self._size)

        self._screen.screen.blit(scaled, self._pos)

    def __resolve_texture(self) -> Optional[pygame.Surface]:
        if self.__dir_animators:
            anim = self.__dir_animators.get(self.__rotation)
            return anim.current_frame if anim else None
        if self.__animator:
            return self.__animator.current_frame
        return self.__static
