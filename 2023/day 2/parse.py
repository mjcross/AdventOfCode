from game import Game, Turn

def parse(stream):
    games = []
    for rawLine in stream:
        line = rawLine.strip().lower()

        # parse the game number
        field = line.split(':')
        gameField = field[0].split(' ')
        assert gameField[0] == 'game'
        game = Game(id = int(gameField[1]))

        # parse the turns for the game
        turnFields = field[1].split(';')
        for turnField in turnFields:
            turn = Turn()

            # parse the colour counts for the turn
            colourCounts = turnField.split(',')
            for colourCount in colourCounts:
                countStr, colour = colourCount.strip().split()
                count = int(countStr)
                if colour == 'red':
                    turn.red = count
                elif colour == 'green':
                    turn.green = count
                elif colour == 'blue':
                    turn.blue = count

            # add the turn to the game
            game.turns.append(turn)

        # add the game to the list of games
        games.append(game)
        
    return games