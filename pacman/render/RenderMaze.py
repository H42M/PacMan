"""Maze renderer based on the internal GeneratedMaze model."""

import pygame

from pacman.maze_adapter import GeneratedMaze, Wall
from pacman.render.RenderObj import RenderOBJ
from pacman.render.Screen import Screen


class RenderMaze(RenderOBJ):
    """Render a generated maze on the pygame screen."""

    def __init__(self, screen: Screen, maze: GeneratedMaze) -> None:
        """Initialize the maze renderer."""
        self.__maze = maze
        self.__color = (30, 60, 220)
        self.__wall_thickness = 4
        self.__cell_size: tuple[int, int] = (0, 0)
        super().__init__(screen)

    def render(self) -> None:
        """Draw maze walls."""
        if self.pos is None or self.size is None:
            return

        screen = self._screen.screen
        cell_size = (
            self.size[0] // self.__maze.width,
            self.size[1] // self.__maze.height,
        )
        self.__cell_size = cell_size
        cell_width, cell_height = cell_size
        thickness = self.__wall_thickness

        for y, row in enumerate(self.__maze.cells):
            for x, cell in enumerate(row):
                cell_x = self.pos[0] + (x * cell_width)
                cell_y = self.pos[1] + (y * cell_height)

                if cell & Wall.NORTH:
                    pygame.draw.rect(
                        screen,
                        self.__color,
                        (cell_x, cell_y, cell_width, thickness),
                    )
                if cell & Wall.SOUTH:
                    pygame.draw.rect(
                        screen,
                        self.__color,
                        (
                            cell_x,
                            cell_y + cell_height - thickness,
                            cell_width,
                            thickness,
                        ),
                    )
                if cell & Wall.EAST:
                    pygame.draw.rect(
                        screen,
                        self.__color,
                        (
                            cell_x + cell_width - thickness,
                            cell_y,
                            thickness,
                            cell_height,
                        ),
                    )
                if cell & Wall.WEST:
                    pygame.draw.rect(
                        screen,
                        self.__color,
                        (cell_x, cell_y, thickness, cell_height),
                    )

    def grid_to_screen(
        self,
        grid_pos: tuple[int, int],
        obj_size: tuple[int, int],
    ) -> tuple[int, int]:
        """Convert a maze cell position to a centered screen position."""
        if self.pos is None:
            return (0, 0)

        cell_width, cell_height = self.cell_size
        x = (
            self.pos[0]
            + (grid_pos[0] * cell_width)
            + ((cell_width - obj_size[0]) // 2)
        )
        y = (
            self.pos[1]
            + (grid_pos[1] * cell_height)
            + ((cell_height - obj_size[1]) // 2)
        )
        return (x, y)

    @property
    def cell_size(self) -> tuple[int, int]:
        """Return the last computed cell size."""
        return self.__cell_size
