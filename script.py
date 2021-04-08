from grid import Hashi

game = Hashi(10, 10)
game.easy_game()
print(game.grid_str())
print(game.grid_str("debug"))
print(game.grid_str("solved"))