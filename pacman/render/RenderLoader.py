import os.path
import pygame
from typing import Optional

from Errors import LoadingError


class GameLoader:

    screen_size: tuple[int, int]
    maze_size: tuple[int, int]
    cell_size: tuple[int, int]
    wall_thickness: int
    assets: dict[str, pygame.Surface]

    @classmethod
    def init(cls, screen_size: tuple[int, int],
             maze_size: tuple[int, int]) -> None:

        cls.screen_size = screen_size

        cls.maze_size = maze_size
        cls.cell_size = (screen_size[0] // maze_size[0],
                         screen_size[1] // maze_size[1])
        cls.wall_thickness = 3
        cls.assets = {}

    @classmethod
    def load_asset(cls, key: str, path: str) -> None:
        if os.path.isfile(path):
            try:
                texture = pygame.image.load(path)
                cls.assets[key] = texture
            except Exception as e:
                raise LoadingError(f'Impossible to load {path}: {e}')
        else:
            raise LoadingError(f'File : {path} doesnt exist')

    @classmethod
    def get_asset(cls, key: Optional[str]) -> Optional[pygame.Surface]:
        if key and key in cls.assets:
            return cls.assets[key]
        return None
