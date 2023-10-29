# Author: Christopher Zhang
# GitHub username: czhanger
# Date: 11/22/2022
# Description: CS162 Mancala Portfolio Project. A text-based version of the board game Mancala.


class Mancala:
    """
    A class to represent the Mancala game. The main class of the program. Interactions with the game will be
    initiated through this class. Human players will only interact with this class.
    """
    def __init__(self):
        """
        Constructor for Mancala. Takes no parameters. Initializes game board and empty variables to be filled by
        Player 1 and 2 Objects
        """
        self._player1 = None
        self._player2 = None

    def create_player(self, name: str):
        """
        Initializes player object using Player class. Takes the name of the player as a parameter.
        If no player1 has been created, player is saved as player1. Return player
        If player1 exists but no player 2 exists, player is saved as player2. Return player
        If player1 and player 2 exist, Let user know that the game can only be played with 2 players. Return None
        """
        player = Player(name)
        if self._player1 is None:
            self._player1 = player
        elif self._player2 is None:
            self._player2 = player
        else:
            print("Game can only be played with two players!")
        return player

    def print_board(self):
        """
        Takes no parameters.
        Prints current state of the game board in the following order:
        player 1: number of seeds in store, seeds number from pit 1 to 6 in a list
        player 2: number of seeds in store, seeds number from pit 1 to 6 in a list
        """
        print("player1:")
        print(f"store: {self._player1.get_store()}")
        print(f"{self._player1.get_board()}")
        print("player2:")
        print(f"store: {self._player2.get_store()}")
        print(f"{self._player2.get_board()}")

    def print_board_list(self):
        """Prints board as a list. Returns player 1 board, player 1 store,
        player 2 board, and player 2 store in a single list."""
        board = []
        for pit in self._player1.get_board():
            board.append(pit)
        board.append(self._player1.get_store())
        for pit in self._player2.get_board():
            board.append(pit)
        board.append(self._player2.get_store())

        return board

    def play_game(self, player, move):
        """
        2 parameters:
        player - player making the move
        move_pit - the pit from which the player will grab seeds to sow from

        Purpose: The purpose of this method is to allow players to make moves in the game. Allows the user to
        sow seeds from move_pit. Method will also check if the game is over or not. Play_game will make use of
        return_winner to check game state, Player.make_move and Player.sow_left_overs to make moves on the board.
        """

        if player != 1 and player != 2:
            return "Invalid player number"
        else:
            if player == 1:
                mover = self._player1
                opponent = self._player2
            else:
                mover = self._player2
                opponent = self._player1

        if move <= 0 or move > 6:
            return "Invalid number for pit index"
        else:
            if self.return_winner() != "Game has not ended":      # check game state
                return "Game is ended"
            else:
                leftovers = mover.make_move('start', move_pit=move)
                self.special_rule_2(mover, opponent, leftovers)
                while leftovers > 0:
                    mover.add_store(1)         # add a seed to mover's store everytime we pass by
                    self.special_rule_2(mover, opponent, leftovers)
                    leftovers -= 1
                    if leftovers == 0:         # SPECIAL RULE 1: last seed lands in mover's store
                        print(f"player {player} take another turn")
                    if leftovers > 0:          # if there are leftovers, sow them in opponent's pits
                        leftovers = opponent.make_move('leftovers', leftovers=leftovers)
                    if leftovers > 0:          # if there are still leftovers, sow them in mover's pits
                        leftovers = mover.make_move('leftovers', leftovers=leftovers)
                        self.special_rule_2(mover, opponent, leftovers)

                if self._player1.seeds_left_in_pits() == 0 or self._player2.seeds_left_in_pits() == 0:
                    if self._player1.seeds_left_in_pits() == 0:
                        self._player2.move_pits_to_store()
                    else:
                        self._player1.move_pits_to_store()

                return self.print_board_list()

    def special_rule_2(self, mover, opponent, leftovers):
        """Checks for and executes rule 2 if necessary."""
        if leftovers == 0:
            last_pit_index = mover.get_last_pit_sowed()
            seeds = mover.get_seeds_in_pit(last_pit_index)
            if seeds == 1:
                opposite_pit_index = 5 - last_pit_index
                stolen_seeds = opponent.give_seeds(opposite_pit_index)
                mover.add_store(stolen_seeds)
                mover.add_store(mover.give_seeds(last_pit_index))

    def return_winner(self):
        """
        Takes no parameters.

        Purpose:
        Checks if the game is ended, tied, or not ended yet.
        If the game is over, return the winner: 'Winner is player 1(or 2): player's name'
        If the game is tied, return 'It's a tie'
        If the game is not over, return 'Game has not ended'
        """
        if self._player1.seeds_left_in_pits() == 0 or self._player2.seeds_left_in_pits() == 0:
            if self._player1.seeds_left_in_pits() == 0:
                self._player2.move_pits_to_store()
            else:
                self._player1.move_pits_to_store()

            p1_store = self._player1.get_store()
            p2_store = self._player2.get_store()

            if p1_store > p2_store:
                return f'Winner is player 1: {self._player1.get_name()}'
            elif p2_store > p1_store:
                return f'Winner is player 2: {self._player2.get_name()}'
            else:
                return "It's a tie"

        else:
            return "Game has not ended"


class Player:
    """
    A class to represent a player in the mancala game. Class will keep track of player's name and board including
    # of seeds in each pit and # of seeds in store. Class will handle movements/changes to player's side of the board.
    """
    def __init__(self, name: str):
        """
        Constructor for Player class. Takes name of player as parameter. Initializes store to 0 seeds and sets
        player board to the starting state of the game. Also has _last_pit_sowed to keep track of when the last seed
        lands in player's own pit
        """
        self._STARTING_SEEDS = 4  # number of seeds per pit at the start of the game
        self._name = name
        self._store = 0
        self._board = [self._STARTING_SEEDS, self._STARTING_SEEDS, self._STARTING_SEEDS,  # initializes starting board
                       self._STARTING_SEEDS, self._STARTING_SEEDS, self._STARTING_SEEDS]  # based on constant
        self._last_pit_sowed = None

    def get_name(self):
        """returns name of player"""
        return self._name

    def get_store(self):
        """returns store of player"""
        return self._store

    def get_board(self):
        """returns board of player"""
        return self._board

    def get_last_pit_sowed(self):
        """returns the last pit a seed landed in, used for special rule 2"""
        return self._last_pit_sowed

    def add_store(self, seeds):
        """Takes number of seeds in store as the parameter. Set the store of player."""
        self._store += seeds

    def give_seeds(self, pit):
        """
        1 parameter:
        pit - the pit from which seeds will be stolen

        purpose: The purpose of this method is to steal seeds when the second special rule is detected.

        return:
        seeds - number of seeds in the pit we want to steal from.
        """
        seeds = self._board[pit]
        self._board[pit] = 0
        return seeds

    def make_move(self, start_or_leftovers, leftovers=None, move_pit=None):
        """
        3 parameter:
        start_or_leftovers - determines whether method is working with a starting pit or leftovers
        move_pit - IF start of move, pit that seeds will be moved from as parameter(1,7).
        leftovers - IF moving leftover seeds, # of leftover seeds to distribute

        purpose: The purpose of this method is to initiate player moves.
        Sow seeds in players pits. hand = seeds in mov_pit , For seed in hand sow a seed in the next pit then
        move to next pit. If there are still seeds left in hand, return them as leftover seeds

        return:
        leftover_seeds - seeds to be sowed in opponents pits
        """
        if start_or_leftovers == "start":
            move_pit -= 1
            seeds_in_hand = self._board[move_pit]           # seeds to be sown
            self._board[move_pit] = 0
            current_pit = move_pit                          # to track which pit we are in
        else:
            seeds_in_hand = leftovers
            current_pit = -1

        current_pit += 1                                    # move to first pit we sow a seed in
        while current_pit <= 5:
            if seeds_in_hand > 0:
                self._board[current_pit] += 1
                seeds_in_hand -= 1
                self._last_pit_sowed = current_pit
                current_pit += 1
            else:
                return seeds_in_hand
        return seeds_in_hand

    def seeds_left_in_pits(self):
        """Purpose: Returns the total number of seeds left in all pits(1-6)"""
        total_seeds = 0
        for seeds in self._board:
            total_seeds += seeds
        return total_seeds

    def move_pits_to_store(self):
        """Purpose: Clears all pits(1-6) by setting them all to 0. This will be used during win condition when
        opposite side has 0 seeds left in their pits. Player will move all seeds left in their pits to their store."""
        self._store += self.seeds_left_in_pits()
        self._board = [0, 0, 0, 0, 0, 0]

    def get_seeds_in_pit(self, pit):
        """
        1 parameter:
        pit - the pit index from the pit we want the seed count from

        purpose: Used to check if a move meets conditions of special rule 2.
        If the last pit sowed only has 1 seed in it, then that pit had been empty.

        returns:
        seeds - number of seeds in that pit
        """
        seeds = self._board[pit]
        return seeds

    def __repr__(self):
        """representation of data in Player Object"""
        return f"Player Object(Name: {repr(self.get_name())}," \
               f" Board: {repr(self.get_board())}," \
               f" Store: {repr(self.get_store())})"

game = Mancala()
player1 = game.create_player("Lily")
player2 = game.create_player("Lucy")
game.play_game(1,3)
game.play_game(1,4)
game.play_game(2,2)
game.play_game(2,3)
game.play_game(1,5)
game.play_game(2,2)
game.play_game(1,6)
game.play_game(2,4)
game.play_game(1,5)
game.play_game(2,2)
game.play_game(1,2)
game.play_game(1,1)
game.play_game(1,5)
game.play_game(1,4)
game.play_game(1,6)
game.play_game(2,1)
game.play_game(1,3)
game.play_game(2,2)
game.play_game(1,5)
game.play_game(1,6)
game.play_game(1,4)
game.play_game(2,3)
game.play_game(1,2)
game.play_game(2,5)
game.play_game(1,5)
game.play_game(2,4)
game.play_game(1,4)
game.play_game(2,6)
game.play_game(1,6)
game.play_game(1,5)
game.play_game(2,2)
game.print_board()
