from pacman.states.base_state import GameState
from typing import Optional
from pacman.states.base_state import StateManager
from pacman.render.Screen import Screen
from pacman.render.Container import Container
import pygame


class SettingsState(GameState):
    def __init__(self, screen: Screen,
                 state_manager: Optional[StateManager] = None,
                 infos: Optional[dict[str, str]] = None
                 ) -> None:
        super().__init__(screen, state_manager)
        if infos:
            self.__infos: dict[str, str] = infos
        else:
            from pacman.constants import WINDOW_HEIGHT, WINDOW_WIDTH
            self.__infos = {
                'godmode': 'Disabled',
                'difficulty': 'Normal',
                'screen_size': f'{WINDOW_WIDTH} x {WINDOW_HEIGHT}'
            }
        self.__menu_ctn = self.__load_settings()

    def handle_events(self, events: list[pygame.event.Event]) -> bool:
        return super().handle_events(events)

    def update(self) -> None:
        # return super().update()
        pass

    def render(self) -> None:
        self._screen.clear()
        self.__menu_ctn.render()
        self._screen.flip()

    def load_infos(self, infos: dict[str, str]) -> None:
        for required in ['godmode', 'difficulty', 'screen_size']:
            if required not in infos:
                raise (SettingsError(f'Missing {required} in '
                                     'provided settings'))
        self.__infos = infos

    def __load_settings(self) -> Container:
        from pacman.render import RenderConfig
        from pacman.render.RenderText import RenderText
        from pacman.render.Divider import Divider
        from pacman.render.interactives import SelectButton
        from pacman.render.interactives import Button

        # Create and set needed buttons
        godmod_btn = SelectButton(self._screen, ['Disabled', 'Enabled'])
        godmod_btn.set_index(self.__infos['godmode'])
        difficulty_btn = SelectButton(self._screen,
                                      ['Easy', 'Normal', 'Hard'])
        difficulty_btn.set_index(self.__infos['difficulty'])
        sizes = [(i + 5) * 100 for i in range(5)]
        sizes_str = [(f'{size} x {size}') for size in sizes]
        screen_size_btn = SelectButton(self._screen, sizes_str)
        screen_size_btn.set_index(self.__infos['screen_size'])

        # Create save / quit buttons
        def on_quit() -> None:
            if self._state_manager:
                self._state_manager.set_state('MENU')

        def on_save() -> None:
            self.__infos = {
                'godmode': godmod_btn.text,
                'difficulty': difficulty_btn.text,
                'screen_size': screen_size_btn.text,
            }
            print(self.__infos)
            if self._state_manager:
                self._state_manager.set_state('MENU')

        # Create settings UI
        container = Container(self._screen, 'VERTICAL',
                              size=RenderConfig.screen_size,
                              pos=(0, 0),
                              padding=90)
        settings_ctn = Container(self._screen, 'VERTICAL',
                                 bg_color=(0, 0, 0, RenderConfig.menu_opacity))

        # -- TITLE:
        title_ctn = Container(self._screen, 'VERTICAL')
        title_ctn.add_content([
            {RenderText(self._screen, 'SETTINGS', font_size=40): '0%'},
            {Divider(self._screen): '1%'}])

        # -- BUTTONS:
        btns_ctn = Container(self._screen, 'VERTICAL')

        godmod_ctn = Container(self._screen, 'HORIZONTAL')
        godmod_ctn.add_content([
            {RenderText(self._screen, 'God mode: '): '50%'},
            {godmod_btn: '50%'},
        ])

        difficulty_ctn = Container(self._screen, 'HORIZONTAL')
        difficulty_ctn.add_content([
            {RenderText(self._screen, 'Difficulty: '): '50%'},
            {difficulty_btn: '50%'},
        ])

        win_size_ctn = Container(self._screen, 'HORIZONTAL')
        win_size_ctn.add_content([
            {RenderText(self._screen, 'Window Size: '): '50%'},
            {screen_size_btn: '50%'},
        ])
        btns_ctn.add_content([
                {godmod_ctn: '20%'},
                {difficulty_ctn: '20%'},
                {win_size_ctn: '20%'}
            ])

        # -- FOOTER
        footer_ctn = Container(self._screen, 'HORIZONTAL')
        footer_ctn.add_content([
            {Button(self._screen, 'SAVE CHANGES', callback=on_save): '45%'},
            {Button(self._screen, 'CANCEL', callback=on_quit): '45%'}
        ])

        settings_ctn.add_content([{title_ctn: '20%'}, {btns_ctn: '60%'},
                                  {footer_ctn: '10%'}])
        container.add_content({settings_ctn: '90%'})
        return container


class SettingsError(Exception):

    pass
