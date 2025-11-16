# This entrypoint file to be used in development. Start by reading README.md
from RPS_game import play, mrugesh, abbey, quincy, kris, human, random_player
from RPS import player


play(human, abbey, 2, verbose=True)

play(human, random_player, 1)

