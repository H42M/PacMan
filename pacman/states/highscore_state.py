from pacman.render.Screen import Screen
from pacman.states.base_state import ScreenState, StateManager
from pacman.render.Container import Container
from pacman.render.RenderConfig import RenderConfig

from typing import Optional


class HighScoreState(ScreenState):
    """Render the highscore screen."""

    def __init__(self, screen: Screen,
                 state_manager: Optional[StateManager] = None,
                 highscore_path: Optional[str] = None
                 ) -> None:
        """Initialize the highscore state."""
        super().__init__(screen, state_manager)
        self.__highscore_path = highscore_path
        self.__container = self.__load_renderer()

    def render(self) -> None:
        """Render the highscore screen."""
        if self.__container:
            self._screen.clear()
            self.__container.render()
            self._screen.flip()

    def update(self) -> None:
        """Update the highscore screen."""
        return

    def __load_renderer(self) -> Container:
        """Build the highscore screen container."""
        from pacman.render.RenderText import RenderText
        from pacman.render.interactives.Button import Button
        from pacman.render.Divider import Divider
        from pacman.highscores import load_highscores

        header_ctn = Container(self._screen, 'VERTICAL')
        header_ctn.add_content([
            {RenderText(self._screen, 'PACMAN',
                        font_family=RenderConfig.FONT,
                        font_size=42,
                        font_color=RenderConfig.YELLOW): '90%'},
            {Divider(self._screen, color=RenderConfig.YELLOW): '2%'}
        ])

        highscores = (load_highscores(self.__highscore_path)
                      if self.__highscore_path else None)

        highscores_ctn = Container(self._screen, 'VERTICAL', gap=5)
        highscores_ctn.add_content([
            {RenderText(self._screen, 'HIGHSCORES', font_size=18,
                        font_family=RenderConfig.FONT): '0%'}
        ])

        if highscores:
            highscores_ctn.add_content([
                {
                    RenderText(
                        self._screen,
                        f'{index + 1}. {entry.name}: {entry.score}',
                        font_size=18,
                        font_family=RenderConfig.FONT
                    ): '0%'
                }
                for index, entry in enumerate(highscores)
            ])
        else:
            highscores_ctn.add_content([
                {RenderText(self._screen,
                            'No highscores yet', font_size=12,
                            font_family=RenderConfig.FONT): '0%'}
            ])

        def on_quit() -> None:
            """Return to the main menu."""
            if self._state_manager:
                self._state_manager.set_state(StateManager.MENU)

        back_btn = Button(self._screen, 'Back to menu',
                          font_family=RenderConfig.FONT,
                          callback=on_quit,
                          color=RenderConfig.RED)

        main_ctn = Container(self._screen, 'VERTICAL', pos=(0, 0),
                             size=RenderConfig.screen_size,
                             padding=50,
                             gap=20,
                             bg_color=RenderConfig.BLACK)
        main_ctn.add_content([
            {header_ctn: '11%'},
            {highscores_ctn: '70%'},
            {back_btn: '8%'}
        ])
        return main_ctn
