from render.Screen import Screen
from render.GameLoader import GameLoader

from render.RenderObj import RenderOBJ
from mazegenerator.mazegenerator import MazeGenerator

# from pygame import Surface


class RenderMaze(RenderOBJ):
    def __init__(self, screen: Screen) -> None:
        self.__maze = MazeGenerator(size=GameLoader.maze_size)
        self.__maze.generate()
        print(self.__maze.maze)

        super().__init__(screen)

    # def get_cells(self) -> list[Surface]:
    #     for y, row in enumerate(self.__maze.maze):
    #         for x, cell in enumerate(row):
    #             cell_pos = (x * GameLoader.cell_size[0],
    #                         y * GameLoader.cell_size[1])
    #             cell_decoded = self.__decode_cell(cell)
    #             cell_surfaces = []
    #             if 'N' in cell_decoded:
    #                 cell_surfaces.append(Surface(GameLoader.cell_size,
    #                                              ))

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
