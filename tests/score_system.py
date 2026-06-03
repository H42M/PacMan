from pacman.game.ScoreSystem import ScoreSystem


if __name__ == '__main__':
    score = ScoreSystem()
    score.add_dot()
    score.add_ghost()
    score.write_score('Joueur 2')
