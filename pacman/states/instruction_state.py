from pacman.render.Screen import Screen
from pacman.states.base_state import ScreenState, StateManager
from pacman.render.Container import Container

from typing import Optional


class InstructionState(ScreenState):

    def __init__(self, screen: Screen,
                 state_manager: Optional[StateManager] = None) -> None:
        super().__init__(screen, state_manager)
        self.__container = self.__load_page()

    def update(self) -> None:
        return

    def render(self) -> None:
        self._screen.clear()
        self.__container.render()
        self._screen.flip()

    def __load_page(self) -> Container:
        from pacman.render.RenderConfig import RenderConfig
        from pacman.render.RenderText import RenderText
        from pacman.render.Divider import Divider
        from pacman.render.interactives.Button import Button

        title_color = RenderConfig.RED
        text_size = 12
        title_size = 20

        # --- HEADER -----
        header_ctn = Container(self._screen, 'VERTICAL')
        header_ctn.add_content([
            {RenderText(self._screen, 'INSTRUCTIONS',
                        font_color=RenderConfig.YELLOW): '95%'},
            {Divider(self._screen, color=RenderConfig.YELLOW): '2%'}
        ])

        # --- GAME RULES -----
        #   --- HOW TO PLAY ---
        htp_ctn = Container(self._screen, 'VERTICAL')
        htp_ctn.add_content([
            {RenderText(self._screen, 'HOW TO PLAY',
                        font_color=title_color,
                        font_size=title_size): '0%'},
            {RenderText(self._screen, 'Eat all pacgums in the maze to '
                        'complete the level.',
                        font_size=text_size): '0%'},
            {RenderText(self._screen, 'Avoid ghosts unless they are '
                        'vulnerable after eating a Super Pacgum.',
                        font_size=text_size): '0%'},
            {RenderText(self._screen, 'Complete all levels before losing all '
                        'your lives within the allotted time.',
                        font_size=text_size): '0%'},
        ])

        #   --- CONTROLS ---
        controls_ctn = Container(self._screen, 'VERTICAL')
        controls_ctn.add_content([
            {RenderText(self._screen, 'CONTROLS',
                        font_color=title_color,
                        font_size=title_size): '0%'},
            {RenderText(self._screen, 'W: Move UP',
                        font_size=text_size): '0%'},
            {RenderText(self._screen, 'A: Move LEFT',
                        font_size=text_size): '0%'},
            {RenderText(self._screen, 'S: Move DOWN',
                        font_size=text_size): '0%'},
            {RenderText(self._screen, 'D: Move RIGHT',
                        font_size=text_size): '0%'},
            {RenderText(self._screen, 'ESC: Pause/Resume',
                        font_size=text_size): '0%'},
        ])

        #   --- SCORING ---
        scoring_ctn = Container(self._screen, 'VERTICAL')
        scoring_ctn.add_content([
            {RenderText(self._screen, 'SCORING',
                        font_color=title_color,
                        font_size=title_size): '0%'},
            {RenderText(self._screen, 'PACGUM: 10 points',
                        font_size=text_size): '0%'},
            {RenderText(self._screen, 'SUPER PACGUM: 50 points',
                        font_size=text_size): '0%'},
            {RenderText(self._screen, 'GHOSTS: 200 points',
                        font_size=text_size): '0%'},
        ])

        #   --- CHEATS ---
        cheats_ctn = Container(self._screen, 'VERTICAL')
        cheats_ctn.add_content([
            {RenderText(self._screen, 'CHEATS',
                        font_color=title_color,
                        font_size=title_size): '0%'},
            {RenderText(self._screen, 'F1: Skip Current Level',
                        font_size=text_size): '0%'},
            {RenderText(self._screen, 'F2: Trigger Game over',
                        font_size=text_size): '0%'},
            {RenderText(self._screen, 'F3: Enable/Disable God mode',
                        font_size=text_size): '0%'},
            {RenderText(self._screen, 'F4: Freeze ghosts',
                        font_size=text_size): '0%'},
            {RenderText(self._screen, 'F5: Add life',
                        font_size=text_size): '0%'},
        ])

        # --- SECTIONS -----
        section1 = Container(self._screen, 'HORIZONTAL')
        section1.add_content([
            {controls_ctn: '45%'},
            {scoring_ctn: '45%'}
        ])
        main_section = Container(self._screen, 'VERTICAL')
        main_section.add_content([
            {htp_ctn: '20%'},
            {section1: '30%'},
            {cheats_ctn: '30%'}
        ])

        # --- FOOTER -----
        def on_quit() -> None:
            if self._state_manager:
                self._state_manager.set_state(StateManager.MENU)

        footer_ctn = Container(self._screen, 'VERTICAL')
        footer_ctn.add_content(
            {Button(self._screen, 'Back to menu',
                    callback=on_quit,
                    color=RenderConfig.RED): '0%'}
            )

        main_container = Container(self._screen, 'VERTICAL',
                                   pos=(0, 0),
                                   size=(RenderConfig.screen_size),
                                   padding=50,
                                   bg_color=RenderConfig.BLACK)
        main_container.add_content([
            {header_ctn: '10%'},
            {main_section: '70%'},
            {footer_ctn: '10%'}
        ])
        return main_container
