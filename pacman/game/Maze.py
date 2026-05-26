from pacman.mazegenerator import MazeGenerator


class MazeError(Exception):

    pass


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
        print(f'Generating Maze: \n{self.__gen_maze.maze}')
        if not self.__gen_maze or not self.__gen_maze.maze:
            print('NO MAZE')
            raise MazeError('No generated maze provided')

        maze: list[list[Cell]] = []
        for y, row in enumerate(self.__gen_maze.maze):
            maze_row: list[Cell] = []
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
                maze_row.append(cell_obj)
            maze.append(maze_row)
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

    def get_cell_wall(self, pos: tuple[int, int], wall: str):
        cell = self.__maze[pos[1]][pos[0]]
        if wall.upper() == 'N':
            return cell.n
        if wall.upper() == 'S':
            return cell.s
        if wall.upper() == 'E':
            return cell.e
        if wall.upper() == 'W':
            return cell.w
