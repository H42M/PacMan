from game_state import GameState
from maze_adapter import CellPosition, Wall
from player import Direction


def get_target_position(
        self,
        position: CellPosition,
        direction: Direction,
) -> CellPosition | None:
    if direction == Direction.UP:
        movement = (0, -1)
        blocking_wall = Wall.NORTH
    elif direction == Direction.DOWN:
        movement = (0, 1)
        blocking_wall = Wall.SOUTH
    elif direction == Direction.LEFT:
        movement = (-1, 0)
        blocking_wall = Wall.WEST
    elif direction == Direction.RIGHT:
        movement = (1, 0)
        blocking_wall = Wall.EAST
    else:
        raise ValueError("Direction is incorrect.")

    x, y = position
    dx, dy = movement
    target = (x + dx, y + dy)

    if target in self.level.maze.solid_positions:
        return None
    blocked = self.level.walls_at(position) & blocking_wall
    if self.level.is_inside(target) and not blocked:
        return target
    else:
        return None

def get_valid_neighbor_positions(level, position) -> None:
    

def get_direction_between(start, target) -> None:
    ...
