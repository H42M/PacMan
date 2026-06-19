from typing import Optional

import pygame

from pacman.render.animation.Animator import Animator
from pacman.render.RenderObj import RenderOBJ
from pacman.render.Screen import Screen


class RenderEntityError(Exception):
    """Raised when a render entity is missing required data."""

    pass


class RenderEntity(RenderOBJ):
    """Render a static or animated sprite."""

    def __init__(self, screen: Screen) -> None:
        """Initialize a render entity."""
        super().__init__(screen)
        self.__static: Optional[pygame.Surface] = None
        self.__animator: Optional[Animator] = None
        self.__dir_animators: Optional[dict[str, Animator]] = None
        self.__rotation: str = 'E'
        self.__fix_rotation = False

    def set_skin(self, texture: Optional[pygame.Surface]) -> None:
        """Set a static sprite texture."""
        if texture:
            self.__static = texture
        else:
            raise RenderEntityError('No skin provided')

    def set_animator(self, animator: Animator) -> None:
        """Set a single animator for the entity."""
        self.__animator = animator
        self.__dir_animators = None

    def set_dir_animators(self, animators: dict[str, Animator]) -> None:
        """Set direction-specific animators for the entity."""
        self.__dir_animators = animators
        self.__animator = None

    def set_rotation(self, direction: str) -> None:
        """Set the entity rotation direction."""
        d = direction.upper()
        if d not in ('N', 'S', 'E', 'W'):
            raise ValueError(f'Invalid rotation: {direction!r}')
        self.__rotation = d

    def set_progress(self, progress: float) -> None:
        """Set the active animator progress."""
        if self.__animator:
            self.__animator.set_frame_by_progress(progress)

    def tick_animator(self) -> None:
        """Advance the active animator."""
        if self.__dir_animators:
            anim = self.__dir_animators.get(self.__rotation)
            if anim:
                anim.tick()
        elif self.__animator:
            self.__animator.tick()

    def render(self) -> None:
        """Render the current entity texture."""
        if not (self._pos and self._size):
            return

        texture = self.__resolve_texture()
        if texture is None:
            return

        if self.__dir_animators:
            scaled = pygame.transform.scale(texture, self._size)
            self._screen.screen.blit(scaled, self._pos)
        else:
            angles = {'E': 0, 'W': 180, 'N': 90, 'S': 270}
            angle = angles.get(self.__rotation, 0)
            scaled = pygame.transform.scale(texture, self._size)
            if self.__fix_rotation:
                rotated = scaled
            else:
                rotated = pygame.transform.rotate(scaled, angle)

            self._screen.screen.blit(rotated, self._pos)

    def __resolve_texture(self) -> Optional[pygame.Surface]:
        """Return the texture for the current animation state."""
        if self.__dir_animators:
            anim = self.__dir_animators.get(self.__rotation)
            return anim.current_frame if anim else None
        if self.__animator:
            return self.__animator.current_frame
        return self.__static

    @property
    def animator(self) -> Optional[Animator]:
        """Return the active animator."""
        return self.__animator

    @property
    def fix_rotation(self) -> bool:
        """Return whether rotation should be skipped."""
        return self.__fix_rotation

    @fix_rotation.setter
    def fix_rotation(self, value: bool) -> None:
        """Set whether rotation should be skipped."""
        self.__fix_rotation = value

    @property
    def direction(self) -> str:
        """Return the current render direction."""
        return self.__rotation
