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
        self.__player_name = ""

    def save_and_quit(self):
        if self._state_manager:
            # TODO: RECORD SCORE:
            self._state_manager.set_state(StateManager.MENU)

    def __load_game_over_ctn(self) -> Container:
        from pacman.render.RenderConfig import RenderConfig
        from pacman.render.Container import Container
        from pacman.render.RenderText import RenderText
        from pacman.render.interactives import Input, ToggleButton

        def save():
            self.__player_name = input_name.value

        input_name_ctn = Container(self._screen, 'HORIZONTAL')
        input_name = Input(self._screen, 'ex: player_2',
                           base_color=RenderConfig.RED,
                           focus_color=(255, 50, 50))
        input_name_ctn.add_content([
            {RenderText(self._screen, 'Submit player name: '): '20%'},
            {input_name: '50%'},
            {ToggleButton(self._screen, 'Save', color_on=RenderConfig.GREEN,
                          color_off=RenderConfig.GREY,
                          state_callback=input_name.get_value,
                          callback=save): '20%'}
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

        def get_player_name():
            return self.__player_name

        game_over_ctn.add_content([
            {game_over_header: '25%'},
            {input_name_ctn: '25%'},
            {ToggleButton(self._screen, 'Back to Menu',
                          color_off=RenderConfig.GREY,
                          color_on=RenderConfig.GREEN,
                          callback=self.save_and_quit,
                          state_callback=get_player_name
                          ): '25%'},
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
