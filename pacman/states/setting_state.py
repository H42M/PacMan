from typing import Optional

from pacman.constants import WINDOW_HEIGHT, WINDOW_WIDTH
from pacman.render.Container import Container
from pacman.render.RenderConfig import RenderConfig
from pacman.render.Screen import Screen
from pacman.states.base_state import ScreenState, StateManager


class SettingsState(ScreenState):
    def __init__(
        self,
        screen: Screen,
        state_manager: Optional[StateManager] = None,
        infos: Optional[dict[str, str]] = None
    ) -> None:
        super().__init__(screen, state_manager)
        self.__infos = infos or {
            'godmode': 'Disabled',
            'difficulty': 'Normal',
            'screen_size': f'{WINDOW_WIDTH} x {WINDOW_HEIGHT}',
        }
        self.__menu_ctn = self.__load_settings()

    def update(self) -> None:
        pass

    def render(self) -> None:
        self._screen.clear()
        self.__menu_ctn.render()
        self._screen.flip()

    def load_infos(self, infos: dict[str, str]) -> None:
        for required in ['godmode', 'difficulty', 'screen_size']:
            if required not in infos:
                raise SettingsError(f'Missing {required} in settings')
        self.__infos = infos

    def __load_settings(self) -> Container:
        from pacman.render.Divider import Divider
        from pacman.render.RenderText import RenderText
        from pacman.render.interactives import Button, SelectButton

        cheat_btn = SelectButton(self._screen,
                                 ['Disabled', 'Enabled'],
                                 color=RenderConfig.RED)
        cheat_btn.set_index(self.__infos['godmode'])

        difficulty_btn = SelectButton(self._screen,
                                      ['Easy', 'Normal', 'Hard'],
                                      color=RenderConfig.RED)
        difficulty_btn.set_index(self.__infos['difficulty'])

        sizes = [(i + 5) * 100 for i in range(5)]
        sizes_str = [f'{size} x {size}' for size in sizes]
        current_size = self.__infos['screen_size']
        if current_size not in sizes_str:
            sizes_str.append(current_size)

        screen_size_btn = SelectButton(self._screen,
                                       sizes_str,
                                       color=RenderConfig.RED)
        screen_size_btn.set_index(current_size)

        def on_quit() -> None:
            if self._state_manager:
                self._state_manager.set_state(StateManager.MENU)

        def on_save() -> None:
            self.__infos = {
                'godmode': cheat_btn.text,
                'difficulty': difficulty_btn.text,
                'screen_size': screen_size_btn.text,
            }
            if self._state_manager:
                self._state_manager.set_state(StateManager.MENU)

        title_ctn = Container(self._screen, 'VERTICAL')
        title_ctn.add_content([
            {RenderText(self._screen, 'SETTINGS',
                        font_size=40,
                        font_color=RenderConfig.YELLOW): '0%'},
            {Divider(self._screen, color=RenderConfig.YELLOW): '1%'}
        ])

        label_font = 18

        cheats_ctn = Container(self._screen, 'HORIZONTAL')
        cheats_ctn.add_content([
            {RenderText(self._screen, 'Cheat Menu: ',
                        font_size=label_font): '50%'},
            {cheat_btn: '50%'},
        ])

        difficulty_ctn = Container(self._screen, 'HORIZONTAL')
        difficulty_ctn.add_content([
            {RenderText(self._screen, 'Difficulty: ',
                        font_size=label_font): '50%'},
            {difficulty_btn: '50%'},
        ])

        win_size_ctn = Container(self._screen, 'HORIZONTAL')
        win_size_ctn.add_content([
            {RenderText(self._screen, 'Window Size: ',
                        font_size=label_font): '50%'},
            {screen_size_btn: '50%'},
        ])

        btns_ctn = Container(self._screen, 'VERTICAL',
                             gap=20)
        btns_ctn.add_content([
            {cheats_ctn: '15%'},
            {difficulty_ctn: '15%'},
            {win_size_ctn: '15%'},
        ])

        footer_ctn = Container(self._screen, 'HORIZONTAL')
        footer_ctn.add_content([
            {Button(self._screen, 'SAVE CHANGES',
                    callback=on_save,
                    color=RenderConfig.RED): '45%'},
            {Button(self._screen, 'CANCEL',
                    callback=on_quit,
                    color=RenderConfig.RED): '45%'},
        ])

        settings_ctn = Container(
            self._screen,
            'VERTICAL',)

        settings_ctn.add_content([
            {title_ctn: '20%'},
            {btns_ctn: '30%'},
            {footer_ctn: '10%'},
        ])

        container = Container(
            self._screen,
            'VERTICAL',
            size=RenderConfig.screen_size,
            pos=(0, 0),
            padding=90,
            bg_color=RenderConfig.BLACK
        )

        container.add_content({settings_ctn: '90%'})
        return container


class SettingsError(Exception):
    pass
