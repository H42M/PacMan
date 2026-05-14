from pacman.render.RenderLoader import GameLoader

from pacman.render.Screen import Screen
from pacman.render.RenderMaze import RenderMaze
from pacman.render.interactives import Button, ToggleButton
from pacman.render.Entity import Entity
from pacman.render.Container import Container
from pacman.render.RenderText import RenderText


def reset_ghost_pos() -> None:
    ghost.x = 1
    ghost.y = GameLoader.screen_size[1] // 2


def ghost_pos_half() -> bool:
    return True if ghost.x and ghost.x > 100 else False


if __name__ == "__main__":

    GameLoader.init((1000, 1000), (15, 15))
    GameLoader.load_asset('pacman', 'assets/sprites/pacman.png')
    GameLoader.load_asset('ghost-blue',
                          'assets/sprites/ghost-blue.png')

    screen = Screen()

    # BUTTONS CONTAINER
    ctn_h = Container(screen, 'HORIZONTAL',
                      pos=(0, 0),
                      size=(GameLoader.screen_size[0], 0),
                      gap=20)
    ctn_h.add_content([
        {Button(screen, 'Rest ghost pos', callback=reset_ghost_pos): '0%'},
        {ToggleButton(screen, 'Un Bouton', state_callback=ghost_pos_half
                      ): '0%'},
        {Button(screen, 'Un Bouton'): "0%"},
    ])
    # MAZE CONTAINER
    maze = RenderMaze(screen, (GameLoader.screen_size))
    ctn_maze = Container(screen, 'HORIZONTAL', size=(GameLoader.screen_size),
                         gap=0)
    ctn_maze.add_content({maze: '80%'})

    # Info CONTAINER
    info_container = Container(screen, 'HORIZONTAL',
                               size=GameLoader.screen_size)
    ghost_x = RenderText(screen, '', (0, 0), (100, 100))
    ghost_y = RenderText(screen, '', (0, 0), (100, 100))
    info_container.add_content([
        {ghost_x: '50%'},
        {ghost_y: '50%'}])

    # TOTAL CONTAINER
    ctn_v = Container(screen, 'VERTICAL', (0, 0), GameLoader.screen_size, 0)
    ctn_v.add_content([
        {ctn_h: '5%'},
        {ctn_maze: '85%'},
        {info_container: '5%'}
    ])

    print(f'maze Y : {maze.y}, MAZE.H: {maze.h},'
          f' ctn_h y: {ctn_h.y}, ctn_h h: {ctn_h.h}')

    pacman = Entity(screen, (100, 100), GameLoader.cell_size)
    pacman.set_skin(GameLoader.get_asset('pacman'))
    ghost = Entity(screen, (300, 300), GameLoader.cell_size)
    ghost.set_skin(GameLoader.get_asset('ghost-blue'))

    while screen.handle_events():
        screen.clear()
        ghost.x = (ghost.x + 1 if ghost.x is not None and
                   ghost.x <= GameLoader.screen_size[0] else 1)
        ghost_x.text = f'GHOST X: {ghost.x}'
        ghost_y.text = f'GHOST Y: {ghost.y}'

        pacman.set_rotation('W')
        pacman.render()
        ghost.render()
        # maze.render()
        # ctn_h.render()
        ctn_v.render()
        screen.flip()
