import pygame


class Animator:
    def __init__(self, frames: list[pygame.Surface]) -> None:
        self.__frames = frames
        self.__index: int = 0

    def set_frame_by_progress(self, progress: float) -> None:
        n = len(self.__frames)
        t = 1.0 - abs(progress * 2 - 1.0)
        self.__index = int(t * (n - 1))

    def tick(self, step: int = 1) -> None:
        self.__index = (self.__index + step) % len(self.__frames)

    @property
    def current_frame(self) -> pygame.Surface:
        return self.__frames[self.__index]
