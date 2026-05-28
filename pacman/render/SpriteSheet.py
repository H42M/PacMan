import os
import pygame


class SpriteSheet:
    def __init__(self, path: str) -> None:
        if os.path.isfile(path):
            self.__sheet = pygame.image.load(path).convert_alpha()
        else:
            raise ValueError('Sprite sheet path doesnt exist')

    def crop(self, x: int, y: int, w: int, h: int) -> pygame.Surface:
        surface = pygame.Surface((w, h), pygame.SRCALPHA)
        surface.blit(self.__sheet, (0, 0), (x, y, w, h))
        return surface

    def crop_rect(self, rect: tuple[int, int, int, int]) -> pygame.Surface:
        x, y, w, h = rect
        return self.crop(x, y, w, h)
