from pacman.render.RenderObj import RenderOBJ
from pacman.render.Screen import Screen

from typing import Optional
import pygame
import os


class RenderIMGError(Exception):
    """Raised when an image cannot be rendered."""

    pass


class RenderImg(RenderOBJ):
    """Render an image surface."""

    def __init__(self, screen: Screen,
                 img_path: str,
                 is_square: bool = False,
                 pos: Optional[tuple[int, int]] = None,
                 size: Optional[tuple[int, int]] = None) -> None:
        """Initialize an image renderer."""
        super().__init__(screen, pos, size)
        self.__image = self.__load_img(img_path)
        self.__is_rect = is_square

    def __load_img(self, path: str) -> pygame.Surface:
        """Load an image surface from disk."""
        if not os.path.isfile(path):
            raise RenderIMGError("IMG path doesn't exist")
        return pygame.image.load(path).convert_alpha()

    def render(self) -> None:
        """Render the image to the screen."""
        if self.pos and self.size:
            if self.__is_rect:
                min_size = min(*self.size)
                new_size = (min_size, min_size)
            else:
                new_size = self.size

            image = self.__image
            image = pygame.transform.scale(image, new_size)

            self._screen.screen.blit(image, self.pos)
