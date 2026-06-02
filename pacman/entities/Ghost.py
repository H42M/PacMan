from pacman.entities.Character import Character
from pacman.game.Maze import Maze
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
        self.__move_speed = 20
        self.__move_count = 0

    def move(self, player_pos: tuple[int, int], maze: Maze) -> None:
        self.__move_count += 1
        if self.__move_count >= self.__move_speed:
            self.pos = self.__chase_algo.get_next_pos(self.pos, player_pos,
                                                      maze)
            self.__move_count = 0
