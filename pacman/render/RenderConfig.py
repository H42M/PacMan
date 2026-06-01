import os.path
import pygame
from typing import Optional

from Errors import LoadingError


class RenderConfig:
    """Class Game Loader.
    Load textures and keep usefull info like cell width, wall thicknes, ..."""

    screen_size: tuple[int, int]
    maze_size: tuple[int, int]
    cell_size: tuple[int, int]
    wall_thickness: int
    assets: dict[str, pygame.Surface]
    menu_opacity: int

    @classmethod
    def load_pacman_frames(cls) -> None:
        sheet_row = 14
        sheet_col = 15
        sheet_path = 'assets/sprites/pacman-spritesheet.png'

        if os.path.isfile(sheet_path):
            try:
                sheet = pygame.image.load(sheet_path).convert_alpha()
                w = sheet.get_width() // sheet_row
                h = sheet.get_height() // sheet_col

                pacman_sheets = {}
                for i, dir in enumerate('ewns'):
                    frames = [
                        sheet.subsurface(pygame.Rect(0, i * h, w, h)),
                        sheet.subsurface(pygame.Rect(w, i * h, w, h)),
                    ]
                    pacman_sheets[dir] = {
                            'nb_frames': 2,
                            'frames': frames
                    }

            except Exception as e:
                raise LoadingError(f'Impossible to load {sheet_path}: {e}')
        else:
            raise LoadingError(f'File : {sheet_path} doesnt exist')

    @classmethod
    def init(cls, screen_size: tuple[int, int],
             maze_size: tuple[int, int]) -> None:

        cls.screen_size = screen_size

        cls.maze_size = maze_size
        cls.cell_size = (screen_size[0] // maze_size[0],
                         screen_size[1] // maze_size[1])
        cls.wall_thickness = 3
        cls.assets = {}
        cls.menu_opacity = 200

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
