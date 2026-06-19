import os
import pygame


class SpriteSheet:
    """Load and crop sprites from a sprite sheet."""

    def __init__(self, path: str) -> None:
        """Initialize a sprite sheet from an image path."""
        if os.path.isfile(path):
            self.__sheet = pygame.image.load(path).convert_alpha()
        else:
            raise ValueError('Sprite sheet path doesnt exist')

    def crop(self, x: int, y: int, w: int, h: int) -> pygame.Surface:
        """Return a cropped sprite surface."""
        surface = pygame.Surface((w, h), pygame.SRCALPHA)
        surface.blit(self.__sheet, (0, 0), (x, y, w, h))
        return surface

    def crop_rect(self, rect: tuple[int, int, int, int]) -> pygame.Surface:
        """Return a cropped sprite surface from a rectangle."""
        x, y, w, h = rect
        return self.crop(x, y, w, h)

    @property
    def size(self) -> tuple[int, int]:
        """Return the sprite sheet size."""
        return self.__sheet.get_size()
