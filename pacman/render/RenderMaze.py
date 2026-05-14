from pacman.render.Screen import Screen
from pacman.render.GameLoader import GameLoader
from Errors import MazeError
from pacman.render.RenderObj import RenderOBJ
from mazegenerator.mazegenerator import MazeGenerator

from pygame import Surface


class RenderMaze(RenderOBJ):
    def __init__(self, screen: Screen, size: tuple[int, int]) -> None:
        self.__maze = MazeGenerator(size=GameLoader.maze_size,
                                    perfect=False,
                                    seed=0,)
        self.__maze.generate()
        self.__color = (255, 255, 255)
        print(self.__maze.maze)

        super().__init__(screen, size=size)

    def render(self) -> None:
        if not self._size:
            raise MazeError('Cannot render maze (Size not defined)')

        cell_w = ((self._size[0] - GameLoader.wall_thickness) //
                  self.__maze._width)
        cell_h = ((self._size[1] - GameLoader.wall_thickness) //
                  self.__maze._height)

        for y, row in enumerate(self.__maze.maze):
            for x, cell in enumerate(row):
                x_maze = self.x if self.x else 0
                y_maze = self.y if self.y else 0
                cell_pos = (x * cell_w + x_maze,
                            y * cell_h + y_maze)
                # print(f'Maze: {self.x}, {self.y}')
                cell_decoded = self.__decode_cell(cell)

                if 'N' in cell_decoded:
                    cell_surface = Surface((cell_w,
                                            GameLoader.wall_thickness))
                    cell_surface.fill(self.__color)
                    self._screen.screen.blit(cell_surface, cell_pos)

                if 'S' in cell_decoded:
                    cell_y = (cell_pos[1] + cell_h -
                              GameLoader.wall_thickness)
                    cell_surface = Surface((cell_w,
                                            GameLoader.wall_thickness))
                    cell_surface.fill(self.__color)
                    self._screen.screen.blit(
                        cell_surface,
                        (cell_pos[0], cell_y))

                if 'E' in cell_decoded:
                    cell_x = (cell_pos[0] + cell_w -
                              GameLoader.wall_thickness)
                    cell_surface = Surface((GameLoader.wall_thickness,
                                            cell_h))
                    cell_surface.fill(self.__color)
                    self._screen.screen.blit(
                        cell_surface,
                        (cell_x, cell_pos[1]))

                if 'W' in cell_decoded:
                    cell_surface = Surface((GameLoader.wall_thickness,
                                            cell_h))
                    cell_surface.fill(self.__color)
                    self._screen.screen.blit(
                        cell_surface,
                        cell_pos)

    def __decode_cell(self, value: int) -> list[str]:
        NORTH = 1
        EAST = 2
        SOUTH = 4
        WEST = 8
        walls = []

        if value & NORTH:
            walls.append("N")
        if value & EAST:
            walls.append("E")
        if value & SOUTH:
            walls.append("S")
        if value & WEST:
            walls.append("W")

        return walls
