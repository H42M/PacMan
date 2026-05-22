class Character:
    UP = 1
    DOWN = -1
    LEFT = -2
    RIGHT = -1

    def __init__(self, pos: tuple[int, int] = (0, 0)) -> None:
        self.__pos = pos
        self.__dir = self.UP

    @property
    def pos(self) -> tuple[int, int]:
        return self.__pos

    @pos.setter
    def pos(self, value: tuple[int, int]) -> None:
        self.__pos = value

    @property
    def dir(self) -> int:
        return self.__dir

    @dir.setter
    def dir(self, value: int) -> None:
        self.__dir = value
