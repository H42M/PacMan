import os
import json


class ScoreSystem:
    DOT = 10
    PELLET = 50
    GHOST = 200

    def __init__(self) -> None:
        self.__score = 0
        self.__ghost_streak = 0

    def add_dot(self) -> None:
        self.__score += self.DOT

    def add_pellet(self) -> None:
        self.__score += self.PELLET

    def add_ghost(self) -> None:
        self.__score += self.GHOST * (2 ** self.__ghost_streak)
        self.__ghost_streak += 1

    def write_score(self, player_name: str) -> None:
        json_path = 'data/scores.json'
        if os.path.isfile(json_path):
            with open(json_path, 'r') as f:
                data = json.load(f)
        else:
            data = {player_name: {}}

        data[player_name]['score'] = self.__score
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=2)
