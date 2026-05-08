class GameLoader:

    screen_size: tuple[int, int]
    maze_size: tuple[int, int]
    cell_size: tuple[int, int]
    wall_thickness: int

    @classmethod
    def init(cls, screen_size: tuple[int, int],
             maze_size: tuple[int, int]):

        cls.screen_size = screen_size

        cls.maze_size = maze_size
        cls.cell_size = (screen_size[0] // maze_size[0],
                         screen_size[1] // maze_size[1])
        cls.wall_thickness = 5
