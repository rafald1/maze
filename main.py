from game import Game


if __name__ == "__main__":
    game = Game()

    while game.run:
        game.game_loop()
