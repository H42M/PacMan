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
        self.__wall_thickness = 5
        super().__init__(screen)

    def render(self) -> None:
        """Display render on screen."""
        if self.pos and self.size:
            screen = self._screen.screen
            cell_size = (self.size[0] // self.__maze.w,
                         self.size[1] / self.__maze.h)
            w = cell_size[0]
            h = cell_size[1]

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
