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
        from pacman.render.interactives import Input
        from pacman.render.interactives import Button

        input_name_ctn = Container(self._screen, 'HORIZONTAL')
        input_name_ctn.add_content([
            {RenderText(self._screen, 'Submit player name: '): '20%'},
            {Input(self._screen, 'ex: player_2', base_color=(100, 100, 100),
                   focus_color=(255, 0, 0)): '50%'},
            {Button(self._screen, 'Save', color=(100, 205, 100)): '20%'}

        ])
        score = 1201
        game_over_header = Container(self._screen, 'VERTICAL', gap=5)
        game_over_header.add_content([
            {RenderText(self._screen,
                        'You Win' if self.__win_or_loose == self.WIN_SCREEN
                        else 'Game Over',
                        font_size=70): '40%'},
            {RenderText(self._screen, f'Your Score: {score}'): '0%'}
        ])
        game_over_ctn = Container(self._screen, 'VERTICAL',
                                  padding=30,
                                  gap=30)

        def on_menu():
            if self._state_manager:
                self._state_manager.set_state(StateManager.MENU)

        game_over_ctn.add_content([
            {game_over_header: '25%'},
            {input_name_ctn: '25%'},
            {Button(self._screen, 'Back to Menu', callback=on_menu): '25%'},
        ])
        window_ctn = Container(self._screen, 'VERTICAL',
                               size=RenderConfig.screen_size,
                               pos=(0, 0),)
        window_ctn.add_content({game_over_ctn: '60%'})
        return window_ctn

    def render(self) -> None:
        self._screen.clear()
        self.__game_over_ctn.render()
        self._screen.flip()

    def update(self) -> None:
        return super().update()

    def handle_events(self, events: list[Event]) -> bool:
        return super().handle_events(events)
