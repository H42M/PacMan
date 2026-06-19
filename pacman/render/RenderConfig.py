import os.path
import pygame
from typing import Optional
from pacman.utils.path import asset_path


class LoadingError(Exception):
    """Raised when a render asset cannot be loaded."""


class RenderConfig:
    """Class Game Loader.
    Load textures and keep usefull info like cell width, wall thicknes, ..."""

    screen_size: tuple[int, int]
    maze_size: tuple[int, int]
    cell_size: tuple[int, int]
    wall_thickness: int
    assets: dict[str, pygame.Surface]
    menu_opacity: int
    RED = (200, 50, 50)
    GREEN = (100, 205, 100)
    GREY = (100, 100, 100)
    BLUE = (30, 60, 220)
    BLACK = (30, 30, 30)
    YELLOW = (220, 220, 0)
    FONT = asset_path("fonts/Emulogic.ttf")

    @classmethod
    def init(cls, screen_size: tuple[int, int],
             maze_size: tuple[int, int]) -> None:
        """Initialize shared render configuration."""

        cls.screen_size = screen_size

        cls.maze_size = maze_size
        cls.cell_size = (screen_size[0] // maze_size[0],
                         screen_size[1] // maze_size[1])
        cls.wall_thickness = 3
        cls.assets = {}
        cls.menu_opacity = 200

    @classmethod
    def load_asset(cls, key: str, path: str) -> None:
        """Load an image asset into the render cache."""
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
        """Return a cached image asset by key."""
        if key and key in cls.assets:
            return cls.assets[key]
        return None
