from render.RenderObj import RenderOBJ
from render.Screen import Screen

from typing import Optional, Union


class Container(RenderOBJ):

    def __init__(self,
                 screen: Screen,
                 way: str,
                 pos: Optional[tuple[int, int]] = None,
                 size: Optional[tuple[int, int]] = None,
                 ) -> None:
        super().__init__(screen, pos, size)
        self.__way = way

    def add_content(self, objs: Union[RenderOBJ, list[RenderOBJ]]):
        pass
