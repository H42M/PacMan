from pygame.event import Event

from pacman.render.Screen import Screen
from pacman.states.base_state import ScreenState, StateManager
from pacman.render.Container import Container


class GameOverState(ScreenState):
    LOOSE_SCREEN = 'LOOSE_SCEEN'
    WIN_SCREEN = 'WIN_SCREEN'

    def __init__(self, screen: Screen,
                 state_manager: StateManager | None = None,
                 win_or_lose: str = LOOSE_SCREEN
                 ) -> None:
        super().__init__(screen, state_manager)
        self.__win_or_loose = win_or_lose
        self.__game_over_ctn = self.__load_game_over_ctn()

    def __load_game_over_ctn(self) -> Container:
        from pacman.render.RenderConfig import RenderConfig
        from pacman.render.Container import Container
        from pacman.render.RenderText import RenderText

        game_over_ctn = Container(self._screen, 'VERTICAL',
                                  size=RenderConfig.screen_size)
        game_over_ctn.add_content(
            {RenderText(self._screen,
                        'You Win' if self.__win_or_loose == self.LOOSE_SCREEN
                        else 'Game OVer'): '0%'}
        )
        return game_over_ctn

    def render(self) -> None:
        self._screen.clear()
        self.__game_over_ctn.render()
        self._screen.flip()

    def update(self) -> None:
        return super().update()

    def handle_events(self, events: list[Event]) -> bool:
        return super().handle_events(events)
