class Character:
    UP = 1
    DOWN = -1
    LEFT = -2
    RIGHT = -1

    def __init__(self, pos: tuple[int, int] = (0, 0)) -> None:
        self.__pos = pos
        self.__dir = self.UP
