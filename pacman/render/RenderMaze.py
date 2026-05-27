from pacman.render.Screen import Screen
from pacman.render.RenderObj import RenderOBJ
from pacman.game.Maze import Maze
import pygame


class RenderMaze(RenderOBJ):
    """Convert maze from MazeGenerator to something displayable."""
    def __init__(self, screen: Screen, maze: Maze) -> None:
        """Initialize RenderMaze"""
        self.__maze = maze
        self.__color = (255, 255, 255)
        self.__wall_thickness = 3
        self.__cell_size: tuple[int, int] = (0, 0)
        super().__init__(screen)

    def render(self) -> None:
        """Display render on screen."""
        if self.pos and self.size:
            # print(f'Maze rendered: {self.size}, {self.pos}')
            screen = self._screen.screen
            cell_size = (self.size[0] // self.__maze.w,
                         self.size[1] // self.__maze.h)
            self.__cell_size = cell_size
            w = cell_size[0]
            h = cell_size[1]
            # print(f'cell size: {cell_size}')

            for y, row in enumerate(self.__maze.maze):
                for x, cell in enumerate(row):
                    cell_x = self.pos[0] + (x * cell_size[0])
                    cell_y = self.pos[1] + (y * cell_size[1])

                    t = self.__wall_thickness
                    color = self.__color
                    if cell.n:
                        pygame.draw.rect(
                            screen,
                            color,
                            (cell_x, cell_y, w, t)
                        )
                    if cell.s:
                        pygame.draw.rect(
                            screen,
                            color,
                            (cell_x, cell_y + h - t, w, t)
                        )
                    if cell.e:
                        pygame.draw.rect(
                            screen,
                            color,
                            (cell_x + w - t, cell_y, t, h)
                        )
                    if cell.w:
                        pygame.draw.rect(
                            screen,
                            color,
                            (cell_x, cell_y, t, h)
                        )

    def grid_to_screen(self, grid_pos: tuple[int, int],
                       obj_size: tuple[int, int]) -> tuple[int, int]:

        if self.pos:
            cell_w, cell_h = self.cell_size
            x = (
                self.pos[0]
                + (grid_pos[0] * cell_w)
                + ((cell_w - obj_size[0]) // 2)
            )
            y = (
                self.pos[1]
                + (grid_pos[1] * cell_h)
                + ((cell_h - obj_size[1]) // 2)
            )
            return (x, y)
        return (0, 0)

    @property
    def cell_size(self) -> tuple[int, int]:
        return self.__cell_size
