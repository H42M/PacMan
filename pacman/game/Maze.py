from pacman.mazegenerator import MazeGenerator


class Cell:
    def __init__(self) -> None:
        self.__n = False
        self.__s = False
        self.__e = False
        self.__w = False

    @property
    def n(self):
        return self.__n

    @n.setter
    def n(self, value):
        self.__n = value

    @property
    def s(self):
        return self.__s

    @s.setter
    def s(self, value):
        self.__s = value

    @property
    def e(self):
        return self.__e

    @e.setter
    def e(self, value):
        self.__e = value

    @property
    def w(self):
        return self.__w

    @w.setter
    def w(self, value):
        self.__w = value


class Maze:
    def __init__(self, maze_size: tuple[int, int],
                 perfect: bool = False, seed: int = 0
                 ) -> None:
        self.__size = maze_size
        self.__gen_maze = MazeGenerator(maze_size, perfect, seed=seed)
        self.__gen_maze.generate()
        self.__maze = self.__generate_maze_obj()

    def __generate_maze_obj(self) -> list[list[Cell]]:
        """Display render on screen."""
        if not self.__gen_maze or not self.__gen_maze.maze:
            return []

        maze = []
        for y, row in enumerate(self.__gen_maze.maze):
            row = []
            for x, cell in enumerate(row):
                cell_decoded = self.__decode_cell(cell)
                cell_obj = Cell()
                if 'N' in cell_decoded:
                    cell_obj.n = True
                if 'S' in cell_decoded:
                    cell_obj.s = True
                if 'E' in cell_decoded:
                    cell_obj.e = True
                if 'W' in cell_decoded:
                    cell_obj.w = True
                row.append(cell)
            maze.append(row)
        return maze

    def __decode_cell(self, value: int) -> list[str]:
        """Change a hexa cell to usable data"""
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

    @property
    def maze(self) -> list[list[Cell]]:
        return self.__maze

    @property
    def w(self) -> int:
        return self.__size[0]

    @property
    def h(self) -> int:
        return self.__size[1]
