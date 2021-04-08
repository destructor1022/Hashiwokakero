from grid import Hashi
def easy(shape, width, height):
    game = Hashi(width, height)
    game.easy_game(shape)
    return game.grid_str("debug")