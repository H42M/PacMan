from pacman.render.animation.AnimEntity import AnimEntity
from pacman.render.Screen import Screen
from pacman.render.animation.Animator import Animator
from enum import Enum


class AnimSet(str, Enum):
    NORMAL = "NORMAL"
    DEATH = "DEATH"


class AnimPacman(AnimEntity):
    def __init__(self, screen: Screen) -> None:
        super().__init__(screen)
        self.__set_death_anim()
        self.__anim_set = AnimSet.DEATH

    def __set_pacman_anim(self) -> None:
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
        frames = []
        for i in range(12):
            w = self._SHEET_SPRITE_W
            h = self._SHEET_SPRITE_H
            x = (i + 2) * w
            y = 0
            frames.append(self._sheet.crop_rect((x, y, w, h)))
        self._render_entity.set_animator(Animator(frames,
                                                  tick_rate=self._tick_rate))

    def tick(self) -> None:
        super().tick()
        # TEMP TICK:
        if (self.__anim_set is AnimSet.DEATH and
                self.is_anim_over(nb_frames=12)):
            self.__anim_set = AnimSet.NORMAL
            self.__set_pacman_anim()
