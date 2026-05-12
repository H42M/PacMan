from render.RenderObj import RenderOBJ
from render.Screen import Screen

from typing import Optional, Union


class Container(RenderOBJ):

    def __init__(self,
                 screen: Screen,
                 way: str,
                 pos: Optional[tuple[int, int]] = None,
                 size: Optional[tuple[int, int]] = None,
                 gap: Optional[int] = None
                 ) -> None:
        super().__init__(screen, pos, size)
        self.__way = way
        self.__gap = gap if gap else 0
        self.__content: dict[RenderOBJ, int] = {}

    def __is_valid_percentage(self, value: str) -> bool:
        if not isinstance(value, str) or not value.endswith('%'):
            return False
        try:
            new_value = int(value[:-1])
        except ValueError:
            return False
        if not (0 <= new_value <= 100):
            return False
        return True

    def __are_all_elm_0(self) -> bool:
        for elm, size in self.__content.items():
            if size != 0:
                return False
        return True

    def add_content(self, objs: Union[dict[RenderOBJ, str],
                                      list[dict[RenderOBJ, str]]]
                    ) -> None:
        if isinstance(objs, dict):
            for key, value in objs.items():
                if not self.__is_valid_percentage(value):
                    raise ValueError(f"La valeur '{value}' n'est pas un "
                                     "pourcentage valide (format: '10%')")
                self.__content[key] = int(value[:-1])
        else:
            for item in objs:
                for key, value in item.items():
                    if not self.__is_valid_percentage(value):
                        raise ValueError(f"La valeur '{value}' n'est pas un "
                                         "pourcentage valide (format: '10%')")
                    self.__content[key] = int(value[:-1])
        self.__resize()

    def __resize(self) -> None:
        if self._size and self._pos:
            nb_gap = len(self.__content) + 1
            total_gap = nb_gap * self.__gap

            if self.__way == "HORIZONTAL":
                end_x = self.__gap

                if self.__are_all_elm_0():
                    elm_size = ((self._size[0] - total_gap) //
                                len(self.__content))
                    for i, (elm, size) in enumerate(self.__content.items()):
                        elm.y = self.y
                        elm.w = elm_size
                        elm.x = (self.__gap * (i + 1)) + (elm_size * i)
                        elm.h = self.h
                        if isinstance(elm, Container):
                            elm.__resize()
                else:
                    for i, (elm, size) in enumerate(self.__content.items()):
                        elm.y = self.y
                        elm.w = int(self._size[0] * (size / 100))

                    if self.__gap == 0 and not self.__are_all_elm_0():
                        gap = self.__process_gap()
                    else:
                        gap = self.__gap

                    for i, (elm, size) in enumerate(self.__content.items()):
                        elm.x = end_x + gap
                        end_x = elm.x if elm.x else 0 + elm.w if elm.w else 0
                        if isinstance(elm, Container):
                            elm.__resize()

                        elm.h = self.h
            if self.__way == 'VERTICAL':
                end_y = 0

                if self.__are_all_elm_0():
                    elm_size = ((self._size[1] - total_gap) //
                                len(self.__content))
                    for i, (elm, size) in enumerate(self.__content.items()):
                        elm.h = elm_size
                        print(f'elm.h: {elm.h}')
                        elm.y = (self.__gap * (i + 1)) + (elm_size * i)
                        if isinstance(elm, Container):
                            elm.__resize()
                else:
                    # Set all new size first
                    for i, (elm, size) in enumerate(self.__content.items()):
                        elm.h = int(self._size[1] * (size / 100))

                    if self.__gap == 0 and not self.__are_all_elm_0():
                        gap = self.__process_gap()
                    else:
                        gap = self.__gap

                    # Set all new pos then
                    for i, (elm, size) in enumerate(self.__content.items()):
                        elm.y = end_y + gap
                        end_y = ((elm.y if elm.y else 0) +
                                 (elm.h if elm.h else 0))
                        print(f'* elm : ({elm.x, elm.y}), ({elm.w, elm.h})')
                        print(f'** GAP: {gap}')
                        if isinstance(elm, Container):
                            elm.__resize()

    def __process_gap(self) -> int:
        if self._size and self._pos:
            if self.__way == 'VERTICAL':
                total_height = sum(elm.h if elm.h else 0
                                   for elm, _ in self.__content.items())
                return ((self._size[1] - total_height) //
                        (len(self.__content) + 1))
            else:
                total_width = sum(elm.w if elm.w else 0
                                  for elm, _ in self.__content.items())
                return ((self._size[0] - total_width) //
                        (len(self.__content) + 1))
        raise ValueError('size or pos not defined: cant process gap')

    def render(self) -> None:
        for elm in self.__content:
            elm.render()

    @property
    def size(self) -> Optional[tuple[int, int]]:
        return self._size

    @size.setter
    def size(self, value: Optional[tuple[int, int]]) -> None:
        if value:
            self._size = value
            self.__resize()

    @property
    def w(self) -> Optional[int]:
        if self._size:
            return self._size[0]
        return None

    @w.setter
    def w(self, value: Optional[int]) -> None:
        if value:
            if self._size:
                self._size = (value, self._size[1])
            else:
                self._size = (value, 0)
            self.__resize()

    @property
    def h(self) -> Optional[int]:
        if self._size:
            return self._size[1]
        return None

    @h.setter
    def h(self, value: Optional[int]) -> None:
        if value:
            if self._size:
                self._size = (self._size[0], value)
            else:
                self._size = (0, value)
            self.__resize()
