from pacman.entities.Character import Character


class Player(Character):
    def __init__(self, pos: tuple[int, int] = (0, 0)) -> None:
        super().__init__(pos)
        self.__prev_pos = self.pos
        self.__move_progress: float = 1.0
        self.__move_speed = 0.05
        self.__dir_str = 'e'

    def start_moving(self, new_pos: tuple[int, int]):
        self.__prev_pos = self.pos
        self.pos = new_pos
        self.__move_progress = 0.0

    def tick(self):
        if self.__move_progress < 1.0:
            self.__move_progress = min(
                1.0, self.__move_progress + self.__move_speed)

    @property
    def is_moving(self) -> bool:
        if self.__move_progress < 1.0:
            return True
        return False

    @property
    def progress(self) -> float:
        return self.__move_progress

    @property
    def prev_pos(self) -> tuple[int, int]:
        return self.__prev_pos

    @property
    def dir_str(self) -> str:
        return self.__dir_str

    @dir_str.setter
    def dir_str(self, value: str) -> None:
        self.__dir_str = value
