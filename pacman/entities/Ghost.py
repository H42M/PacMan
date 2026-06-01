from pacman.entities.Character import Character
from pacman.game.ai import ChaseAI, VectorChase, AmbushChase, DirectChase, \
    ShyChase


class Ghost(Character):
    DIRECT_CHASE = DirectChase
    AMBUSH_CHASE = AmbushChase
    VECTOR_CHASE = VectorChase
    SHY_CHASE = ShyChase

    def __init__(
        self,
        pos: tuple[int, int] = (0, 0),
        chase_algo_cls: type["ChaseAI"] = DirectChase
    ) -> None:
        super().__init__(pos)
        self.__chase_algo = chase_algo_cls()

    def move(self) -> None:
        self.pos = self.__chase_algo.get_next_pos()
