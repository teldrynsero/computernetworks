# Game: Rock-paper-scissors. Keeps track of
# player moves, winner of each game, and 
# checks whether players have made their
# moves and if the game is ready to proceed.

class Game:
    def __init__(self, id):
        self.p1Went = False # Has player 1 made a move?
        self.p2Went = False # Has player 2 made a move?
        self.ready = False # Both players ready to play
        self.id = id # Game ID
        self.moves = [None, None] # Stores both players' moves
        self.wins = [0,0] # Tracks each player's wins
        self.ties = 0 # Tracks tied games

    # Returns move made by player
    def get_player_move(self, p):
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    # Updates when player makes a move
    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    # Checks if both players are connected (and ready to play)
    def connected(self):
        return self.ready

    # Have both players made their moves?
    def bothWent(self):
        return self.p1Went and self.p2Went

    # Who won this game?
    def winner(self):

        # Convert moves to uppercase
        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        # TIE GAME
        winner = -1
        # p1 ROCK beats p2 SCISSORS
        if p1 == "R" and p2 == "S":
            winner = 0
        # p1 SCISSORS loses to p2 ROCK
        elif p1 == "S" and p2 == "R":
            winner = 1
        # p1 PAPER beats p2 ROCK
        elif p1 == "P" and p2 == "R":
            winner = 0
        # p1 ROCK loses to p2 PAPER
        elif p1 == "R" and p2 == "P":
            winner = 1
        # p1 SCISSORS beats p2 PAPER
        elif p1 == "S" and p2 == "P":
            winner = 0
        # p1 PAPER loses to p2 SCISSORS
        elif p1 == "P" and p2 == "S":
            winner = 1

        return winner

    # Start new game
    def resetWent(self):
        self.p1Went = False
        self.p2Went = False