from render.GameLoader import GameLoader

from render.Screen import Screen
from render.RenderMaze import RenderMaze

if __name__ == "__main__":
    GameLoader.init((800, 800), (15, 15))
    screen = Screen()
    maze = RenderMaze(screen)

    while screen.handle_events():
        screen.flip()
