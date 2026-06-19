import pygame


class Animator:
    """Advance through animation frames over time."""

    def __init__(self, frames: list[pygame.Surface], tick_rate: int = 1,
                 loop: bool = True
                 ) -> None:
        """Initialize an animator with frames and timing."""
        if loop:
            self.__frames = frames + frames[-2:0:-1]  # [0,1,2,3,2,1]
        else:
            self.__frames = frames
        self.__index: int = 0
        self.__tick_rate = tick_rate
        self.__tick_count = 0
        self.__loop = loop

    def set_frame_by_progress(self, progress: float) -> None:
        """Set the frame index from normalized progress."""
        n = len(self.__frames)
        t = 1.0 - abs(progress * 2 - 1.0)
        self.__index = int(t * (n - 1))

    def tick(self, step: int = 1) -> None:
        """Advance the animator by one tick."""
        if self.__tick_count >= self.__tick_rate:
            if self.__loop:
                self.__index = (self.__index + step) % len(self.__frames)
            else:
                self.__index = min(
                    self.__index + step,
                    len(self.__frames) - 1
                )

        self.__tick_count = (self.__tick_count + 1) % self.__tick_rate + 1

    @property
    def current_frame(self) -> pygame.Surface:
        """Return the current animation frame."""
        return self.__frames[self.__index]

    @property
    def frame_index(self) -> int:
        """Return the current frame index."""
        return self.__index

    @property
    def frames(self) -> list[pygame.Surface]:
        """Return all animation frames."""
        return self.__frames

    @property
    def tick_rate(self) -> int:
        """Return the animation tick rate."""
        return self.__tick_rate

    @tick_rate.setter
    def tick_rate(self, value: int) -> None:
        """Set the animation tick rate."""
        self.__tick_rate = value
        self.__tick_count = 0

    @property
    def finished(self) -> bool:
        """Return whether a non-looping animation is finished."""
        return (
            not self.__loop and
            self.__index == len(self.__frames) - 1
        )
