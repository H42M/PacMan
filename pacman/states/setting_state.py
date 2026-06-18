from typing import Optional

from pacman.constants import WINDOW_HEIGHT, WINDOW_WIDTH
from pacman.render.Container import Container
from pacman.render.RenderConfig import RenderConfig
from pacman.render.Screen import Screen
from pacman.states.base_state import ScreenState, StateManager


class SettingsState(ScreenState):
    """Render the settings screen."""

    def __init__(
        self,
        screen: Screen,
        state_manager: Optional[StateManager] = None,
        infos: Optional[dict[str, str]] = None
    ) -> None:
        """Initialize the settings state."""
        super().__init__(screen, state_manager)
        self.__infos = infos or {
            'godmode': 'Disabled',
            'difficulty': 'Normal',
            'screen_size': f'{WINDOW_WIDTH} x {WINDOW_HEIGHT}',
        }
        self.__menu_ctn = self.__load_settings()

    def update(self) -> None:
        """Update the settings screen."""
        pass

    def render(self) -> None:
        """Render the settings screen."""
        self._screen.clear()
        self.__menu_ctn.render()
        self._screen.flip()

    def load_infos(self, infos: dict[str, str]) -> None:
        """Load settings labels into the screen state."""
        for required in ['godmode', 'difficulty', 'screen_size']:
            if required not in infos:
                raise SettingsError(f'Missing {required} in settings')
        self.__infos = infos

    def __load_settings(self) -> Container:
        """Build the settings screen container."""
        from pacman.render.Divider import Divider
        from pacman.render.RenderText import RenderText
        from pacman.render.interactives import Button, SelectButton

        godmode_btn = SelectButton(self._screen, ['Disabled', 'Enabled'])
        godmode_btn.set_index(self.__infos['godmode'])

        difficulty_btn = SelectButton(self._screen, ['Easy', 'Normal', 'Hard'])
        difficulty_btn.set_index(self.__infos['difficulty'])

        sizes = [(i + 5) * 100 for i in range(5)]
        sizes_str = [f'{size} x {size}' for size in sizes]
        current_size = self.__infos['screen_size']
        if current_size not in sizes_str:
            sizes_str.append(current_size)

        screen_size_btn = SelectButton(self._screen, sizes_str)
        screen_size_btn.set_index(current_size)

        def on_quit() -> None:
            """Return to the main menu without saving."""
            if self._state_manager:
                self._state_manager.set_state(StateManager.MENU)

        def on_save() -> None:
            """Store selected settings labels and return to the menu."""
            self.__infos = {
                'godmode': godmode_btn.text,
                'difficulty': difficulty_btn.text,
                'screen_size': screen_size_btn.text,
            }
            if self._state_manager:
                self._state_manager.set_state(StateManager.MENU)

        container = Container(
            self._screen,
            'VERTICAL',
            size=RenderConfig.screen_size,
            pos=(0, 0),
            padding=90
        )

        settings_ctn = Container(
            self._screen,
            'VERTICAL',
            bg_color=(0, 0, 0, RenderConfig.menu_opacity)
        )

        title_ctn = Container(self._screen, 'VERTICAL')
        title_ctn.add_content([
            {RenderText(self._screen, 'SETTINGS', font_size=40): '0%'},
            {Divider(self._screen): '1%'}
        ])

        btns_ctn = Container(self._screen, 'VERTICAL')

        cheats_ctn = Container(self._screen, 'HORIZONTAL')
        cheats_ctn.add_content([
            {RenderText(self._screen, 'Cheat Menu: '): '50%'},
            {godmode_btn: '50%'},
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
            {cheats_ctn: '20%'},
            {difficulty_ctn: '20%'},
            {win_size_ctn: '20%'},
        ])

        footer_ctn = Container(self._screen, 'HORIZONTAL')
        footer_ctn.add_content([
            {Button(self._screen, 'SAVE CHANGES', callback=on_save): '45%'},
            {Button(self._screen, 'CANCEL', callback=on_quit): '45%'},
        ])

        settings_ctn.add_content([
            {title_ctn: '20%'},
            {btns_ctn: '60%'},
            {footer_ctn: '10%'},
        ])

        container.add_content({settings_ctn: '90%'})
        return container


class SettingsError(Exception):
    """Raised when settings data is incomplete."""

    pass
