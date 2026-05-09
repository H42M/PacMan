from render.GameLoader import GameLoader

from render.Screen import Screen
from render.RenderMaze import RenderMaze
from render.buttons.Button import Button

if __name__ == "__main__":
    GameLoader.init((800, 800), (15, 15))
    screen = Screen()
    maze = RenderMaze(screen)
    button = Button(screen, 'Un Bouton', (0, 0), (100, 100))

    while screen.handle_events():
        maze.render()
        screen.flip()
        # button.render()
