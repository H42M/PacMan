from pacman.render.animation.AnimEntity import AnimEntity, AnimSet
from pacman.render.Screen import Screen
from pacman.render.animation.Animator import Animator
from typing import Optional


class AnimPacman(AnimEntity):
    """Render an animated Pac-Man sprite."""

    def __init__(self, screen: Screen) -> None:
        """Initialize a Pac-Man animation renderer."""
        super().__init__(screen)
        self.__set_pacman_anim()

    def __set_pacman_anim(self) -> None:
        """Configure the normal Pac-Man animation."""
        frames = []
        for i in range(3):
            w = self._SHEET_SPRITE_W
            h = self._SHEET_SPRITE_H
            x = i * w
            y = 0
            frames.append(self._sheet.crop_rect((x, y, w, h)))

        self._render_entity.set_animator(Animator(frames,
                                                  tick_rate=self._tick_rate))

    def __set_death_anim(self) -> None:
        """Configure the Pac-Man death animation."""
        frames = []
        for i in range(12):
            w = self._SHEET_SPRITE_W
            h = self._SHEET_SPRITE_H
            x = (i + 2) * w
            y = 0
            frames.append(self._sheet.crop_rect((x, y, w, h)))
        self._render_entity.set_animator(Animator(frames,
                                                  tick_rate=self._tick_rate,
                                                  loop=False))

    def tick(self) -> None:
        """Advance the Pac-Man animation."""
        if (self._anim_set is AnimSet.DEATH and
                self.is_anim_over(nb_frames=12)):
            self._anim_set = AnimSet.NORMAL
            self.__set_pacman_anim()
        super().tick()

    @property
    def anim_set(self) -> str:
        """Return the current Pac-Man animation set."""
        return self._anim_set

    @anim_set.setter
    def anim_set(self, anim_set: AnimSet) -> None:
        """Set the current Pac-Man animation set."""
        if self._anim_set == anim_set:
            return
        self._anim_set = anim_set
        animator = self._render_entity.animator
        if not animator:
            return
        if self._anim_set is AnimSet.BOOSTED:
            self.__set_pacman_anim()
            animator.tick_rate = 8
        elif self._anim_set is AnimSet.NORMAL:
            self.__set_pacman_anim()
            animator.tick_rate = 18
        elif self._anim_set is AnimSet.DEATH:
            self.__set_death_anim()

    @property
    def animator(self) -> Optional[Animator]:
        """Return the active Pac-Man animator."""
        return self._render_entity.animator
