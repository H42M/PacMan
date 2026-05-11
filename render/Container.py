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
        self.__content: list[RenderOBJ] = []

    def add_content(self, objs: Union[RenderOBJ, list[RenderOBJ]]):
        if isinstance(objs, RenderOBJ):
            self.__content.append(objs)
        else:
            self.__content.extend(objs)
        self.__resize()

    def __resize(self):
        if self._size and self._pos:
            if self.__way == "HORIZONTAL":
                nb_gap = len(self.__content) + 1
                total_gap = nb_gap * self.__gap
                elm_size = ((self._size[0] - total_gap) //
                            len(self.__content))

                for i, elm in enumerate(self.__content):
                    elm.w = elm_size
                    elm.x = (self.__gap * (i + 1)) + (elm_size * i)

    def render(self) -> None:
        for elm in self.__content:
            elm.render()
