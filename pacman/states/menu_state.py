from typing import Optional

from pacman.render.Container import Container
from pacman.render.RenderConfig import RenderConfig
from pacman.render.Screen import Screen
from pacman.states.base_state import ScreenState, StateManager


class MenuState(ScreenState):
    def __init__(
        self,
        screen: Screen,
        state_manager: Optional[StateManager] = None
    ) -> None:
        super().__init__(screen, state_manager)
        self.__menu_ctn = self.__load_menu()

    def update(self) -> None:
        pass

    def render(self) -> None:
        self._screen.clear()
        self.__menu_ctn.render()
        self._screen.flip()

    def __load_menu(self) -> Container:
        from pacman.render.Divider import Divider
        from pacman.render.RenderText import RenderText
        from pacman.render.interactives import Button

        container = Container(
            self._screen,
            'VERTICAL',
            size=RenderConfig.screen_size,
            pos=(0, 0),
            padding=130
        )

        menu_ctn = Container(
            self._screen,
            'VERTICAL',
            padding=50,
            bg_color=(0, 0, 0, RenderConfig.menu_opacity)
        )

        title_ctn = Container(self._screen, 'VERTICAL')
        title_ctn.add_content([
            {
                RenderText(
                    self._screen,
                    'PACMAN',
                    font_color=(255, 255, 0),
                    font_size=60
                ): '0%'
            },
            {Divider(self._screen, (255, 255, 0)): '1%'}
        ])

        def on_play() -> None:
            if self._state_manager:
                self._state_manager.set_state(StateManager.PLAYING)

        def on_settings() -> None:
            if self._state_manager:
                self._state_manager.set_state(StateManager.SETTINGS)

        def on_quit() -> None:
            raise SystemExit

        btns_ctn = Container(self._screen, 'VERTICAL', gap=30)
        btns_ctn.add_content([
            {Button(self._screen, 'PLAY', callback=on_play): '0%'},
            {Button(self._screen, 'SETTINGS', callback=on_settings): '0%'},
            {Button(self._screen, 'QUIT', callback=on_quit): '0%'},
        ])

        footer_ctn = Container(self._screen, 'VERTICAL', gap=20)
        footer_info = Container(self._screen, 'HORIZONTAL')
        footer_info.add_content([
            {
                RenderText(
                    self._screen,
                    'Game made by ngaubil and hgeorges',
                    font_size=20
                ): '0%'
            },
            {
                RenderText(
                    self._screen,
                    'Max score: TODO',
                    font_size=20
                ): '0%'
            }
        ])

        footer_ctn.add_content([
            {Divider(self._screen): '2%'},
            {footer_info: '0%'}
        ])

        menu_ctn.add_content([
            {title_ctn: '20%'},
            {btns_ctn: '70%'},
            {footer_ctn: '10%'}
        ])
        container.add_content({menu_ctn: '90%'})
        return container
