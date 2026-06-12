from pacman.render.animation.AnimEntity import AnimEntity, AnimSet
from pacman.render.Screen import Screen
from pacman.render.animation.Animator import Animator


class AnimGhost(AnimEntity):
    def __init__(self, screen: Screen, ghost_color: int = 0) -> None:
        super().__init__(screen)
        self.__ghost_color = ghost_color
        self.__set_render_ghost()

    def __set_render_ghost(self) -> None:
        animators = {}
        for dir_i, dir in enumerate('EWNS'):
            frames = []
            # Frame loop
            for frame_i in range(2):
                w = self._SHEET_SPRITE_W
                h = self._SHEET_SPRITE_H
                x = (frame_i * w) + (dir_i * w * 2)
                y = h * (4 + self.__ghost_color)
                frames.append(self._sheet.crop_rect((x, y, w, h)))
            animators[dir] = Animator(frames, tick_rate=8)

        self._render_entity.set_dir_animators(animators)

    def __set_frightened_ghost(self) -> None:
        self._render_entity.fix_rotation = True
        frames = []
        for i in range(2):
            w = self._SHEET_SPRITE_W
            h = self._SHEET_SPRITE_H
            x = (i + 8) * w
            y = 4 * h
            frames.append(self._sheet.crop_rect((x, y, w, h)))

        self._render_entity.set_animator(Animator(frames,
                                                  tick_rate=self._tick_rate))

    def __set_frightened_flashing_ghost(self) -> None:
        self._render_entity.fix_rotation = True
        frames = []
        for i in range(4):
            w = self._SHEET_SPRITE_W
            h = self._SHEET_SPRITE_H
            x = (i + 8) * w
            y = 4 * h
            frames.append(self._sheet.crop_rect((x, y, w, h)))

        self._render_entity.set_animator(Animator(frames,
                                                  tick_rate=self._tick_rate))

    def tick(self) -> None:
        super().tick()

    @property
    def anim_set(self) -> str:
        return self._anim_set

    @anim_set.setter
    def anim_set(self, anim_set: AnimSet) -> None:
        if self._anim_set == anim_set:
            return
        self._anim_set = anim_set
        if anim_set is AnimSet.FRIGHTENED:
            self.__set_frightened_ghost()
        elif anim_set is AnimSet.FRIGHTENED_FLASHING:
            self.__set_frightened_flashing_ghost()
        elif anim_set is AnimSet.NORMAL:
            self.__set_render_ghost()
