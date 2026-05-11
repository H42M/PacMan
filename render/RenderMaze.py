from render.Screen import Screen
from render.GameLoader import GameLoader

from render.RenderObj import RenderOBJ
from mazegenerator.mazegenerator import MazeGenerator

from pygame import Surface


class RenderMaze(RenderOBJ):
    def __init__(self, screen: Screen) -> None:
        self.__maze = MazeGenerator(size=GameLoader.maze_size)
        self.__maze.generate()
        self.__color = (255, 255, 0)
        print(self.__maze.maze)

        super().__init__(screen)

    def render(self) -> None:
        for y, row in enumerate(self.__maze.maze):
            for x, cell in enumerate(row):
                cell_pos = (x * GameLoader.cell_size[0],
                            y * GameLoader.cell_size[1])
                cell_decoded = self.__decode_cell(cell)

                if 'N' in cell_decoded:
                    cell_surface = Surface((GameLoader.cell_size[0],
                                            GameLoader.wall_thickness))
                    cell_surface.fill(self.__color)
                    self._screen.screen.blit(cell_surface, cell_pos)

                if 'S' in cell_decoded:
                    cell_y = (cell_pos[1] + GameLoader.cell_size[1] -
                              GameLoader.wall_thickness)
                    cell_surface = Surface((GameLoader.cell_size[0],
                                            GameLoader.wall_thickness))
                    cell_surface.fill(self.__color)
                    self._screen.screen.blit(
                        cell_surface,
                        (cell_pos[0], cell_y))

                if 'E' in cell_decoded:
                    cell_x = (cell_pos[0] + GameLoader.cell_size[0] -
                              GameLoader.wall_thickness)
                    cell_surface = Surface((GameLoader.wall_thickness,
                                            GameLoader.cell_size[1]))
                    cell_surface.fill(self.__color)
                    self._screen.screen.blit(
                        cell_surface,
                        (cell_x, cell_pos[1]))

                if 'W' in cell_decoded:
                    cell_surface = Surface((GameLoader.wall_thickness,
                                            GameLoader.cell_size[1]))
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
