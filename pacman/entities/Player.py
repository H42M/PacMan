from pacman.entities.Character import Character


class Player(Character):
    def __init__(self, pos: tuple[int, int] = (0, 0)) -> None:
        super().__init__(pos)
