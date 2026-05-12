from render.GameLoader import GameLoader

from render.Screen import Screen
from render.RenderMaze import RenderMaze
from render.buttons.Button import Button
from render.Entity import Entity
from render.Container import Container


if __name__ == "__main__":

    GameLoader.init((800, 800), (15, 15))
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
        {Button(screen, 'Un Bouton'): '0%'},
        {Button(screen, 'Un Bouton'): '0%'},
        {Button(screen, 'Un Bouton'): "0%"},
    ])
    # MAZE CONTAINER
    maze = RenderMaze(screen, (GameLoader.screen_size))
    ctn_maze = Container(screen, 'HORIZONTAL', size=(GameLoader.screen_size),
                         gap=0)
    ctn_maze.add_content({maze: '80%'})

    # TOTAL CONTAINER
    ctn_v = Container(screen, 'VERTICAL', (0, 0), GameLoader.screen_size, 0)
    ctn_v.add_content([
        {ctn_h: '5%'},
        {ctn_maze: '90%'}
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
        pacman.set_rotation('W')
        # pacman.render()
        # ghost.render()
        # maze.render()
        # ctn_h.render()
        ctn_v.render()

        screen.flip()
