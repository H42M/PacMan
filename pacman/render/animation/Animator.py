import pygame


class Animator:
    def __init__(self, frames: list[pygame.Surface], tick_rate: int = 1
                 ) -> None:
        self.__frames = frames + frames[-2:0:-1]  # [0,1,2,3,2,1] puis boucle
        self.__index: int = 0
        self.__tick_rate = tick_rate
        self.__tick_count = 0

    def set_frame_by_progress(self, progress: float) -> None:
        n = len(self.__frames)
        t = 1.0 - abs(progress * 2 - 1.0)
        self.__index = int(t * (n - 1))

    def tick(self, step: int = 1) -> None:
        if self.__tick_count >= self.__tick_rate:
            self.__index = (self.__index + step) % len(self.__frames)
        self.__tick_count = (self.__tick_count + 1) % self.__tick_rate + 1

    @property
    def current_frame(self) -> pygame.Surface:
        return self.__frames[self.__index]

    @property
    def frame_index(self) -> int:
        return self.__index

    @property
    def frames(self) -> list[pygame.Surface]:
        return self.__frames

    @property
    def tick_rate(self) -> int:
        return self.__tick_rate

    @tick_rate.setter
    def tick_rate(self, value: int) -> None:
        self.__tick_rate = value
        self.__tick_count = 0
