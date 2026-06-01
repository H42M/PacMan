from abc import abstractmethod, ABC


class ChaseAI(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_next_pos(self) -> tuple[int, int]:
        pass
