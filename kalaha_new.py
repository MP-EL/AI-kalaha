import enum
import os
from time import sleep
import numpy as np
import random
from timeit import default_timer as timer
import matplotlib.pyplot as plt

import sys, signal


def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit()
signal.signal(signal.SIGINT, signal_handler)

def random_move(board):
    move = random.choice(board.allowed_moves())
    return move

class RandomAgent:
    def __init__(self,seed):
        self.random = random.Random(seed)
    
    def get_move(self,board):
        return self.random.choice(board.allowed_moves())

        

class MinimaxAgent:
    def __init__(self, max_depth=8, alpha_beta_pruning=True, seed=1):
        self.max_depth = max_depth
        self.alpha_beta_pruning = alpha_beta_pruning
        self.random = random.Random(seed)

    def get_move(self, board):
        """Gets the best move by performing minimax to retrieve the highest value move.
        Args:
            board (KalahaBoard): KalahaBoard class (Use the class in this script).
        Returns:
            int: the current best move retrieved from the minimax algo.
        """
        moves_and_scores = []
        moves = board.allowed_moves()
        #If there is only 1 legal move pick that move.
        if len(moves) == 1:
            return moves[0]
        #for every legal move run the minimax algo recursively to test all moves down to the desired depth.
        for move in moves:
            moves_and_scores.append([self._minimax(board, True, 0, move, float('-inf'), float('inf')), move])
        #get max value of the minimax outputs. 
        max_score = max([i[0] for i in moves_and_scores])

        best_moves = []
        #choose all moves that are equal to max_score
        for move_and_score in moves_and_scores:
            if move_and_score[0] == max_score:
                best_moves.append(move_and_score[1])
        #Choose a random move from the max_score moves (For some reason this makes it much stronger than when choosing the first move with the highest score).
        rand = self.random.choice([i for i in best_moves])
        return rand

    def _minimax(self, board, is_max_player, current_depth, move, alpha, beta):
        """Minimax algorithm for a kalaha board. Should not be called standalone but instead called through the get_move function

        Args:
            board (KalahaBoard): KalahaBoard class.
            is_max_player (bool): decides whether or not the minimax should run for the maximizing player or not, should always be initiated as True.
            current_depth (int): current depth of the recursion in minimax.
            move (int): the move currently being investigated by minimax. 
            alpha (float): alpha value for minimax algorithm. Should be initiated as float(-'inf')
            beta (float): beta value for minimax algorithm. Should be initiated as float('inf')

        Returns:
            int: the current best move retrieved from the minimax algo.
        """
        #stop condition
        if current_depth == self.max_depth:
            return board.score()[board.current_player()]
        
        #Make a copy of the board to test the moves on.
        new_board = board.copy()
        new_board.move(move)
        moves = new_board.allowed_moves()
        #init -inf og inf values for the minimax algo.
        best_value = float('-inf') if is_max_player else float('inf')
        for move in moves:
            move_score = self._minimax(new_board, not is_max_player, current_depth + 1, move, alpha, beta)
            #find the max value from the minimax output and perform alpha beta pruning.
            if is_max_player:
                best_value = max(move_score, best_value)
                if self.alpha_beta_pruning:
                    alpha = max(alpha, best_value)
                    if beta <= alpha:
                        return best_value
            #The same as above but with the min part of minimax instead of max
            else:
                best_value = min(move_score, best_value)
                if self.alpha_beta_pruning:
                    beta = min(beta, best_value)
                    if beta <= alpha: 
                        return best_value
        return best_value

class KalahaBoard:
    def __init__(self, number_of_cups, number_of_stones):
        self.number_of_cups = number_of_cups
        self.stones = number_of_stones
        #set up board
        self.reset_board()
        self._player_houses = { 0: self.number_of_cups*(1),
                                1: self.number_of_cups*(2) + 1}
        
    def reset_board(self):
        self.BP1 = [self.stones for i in range(self.number_of_cups)] + [0]
        self.BP2 = [self.stones for i in range(self.number_of_cups)] + [0]
        self.board = self.BP1 + self.BP2
        self.player = 0

    def print_board(self):
        # os.system('cls' if os.name == 'nt' else 'clear')
        
        # BP1 = self.board[0:self.number_of_cups + 1]
        # BP2 = self.board[1+self.number_of_cups: self.number_of_cups*2 + 2]
        # # print(BP1)
        # # print(BP2)
        # if self.current_player() == 0:
        #     print("allowed moves", [i + 1 for i in self.allowed_moves()])
        # else:
        #     print("allowed moves", self.allowed_moves())
        # BP2.reverse()
        # print(f"\nPocket # :  {'  '.join([str(i + 1) for i in range(self.number_of_cups)][::-1])}")
        # print('P2 -->', BP2[:1], BP2[1:self.number_of_cups+1])
        # print('P1 --> ', '  ', BP1[0:self.number_of_cups],BP1[self.number_of_cups:])
        # print(f"Pocket # :  {'  '.join([str(i + 1) for i in range(self.number_of_cups)])}")
        # BP2.reverse()
        pass

    def move(self, b):
        if b not in self.allowed_moves():
            print("move not allowed")
            return False

        old_board = list(self.board)

        stones_to_distribute = self.board[b]
        self.board[b] = 0

        other_player = 1 if self.current_player() == 0 else 0

        current_cup = b
        while stones_to_distribute > 0:
            current_cup = current_cup+1

            if current_cup >= len(self.board):
                current_cup -= len(self.board)

            if current_cup == self._get_house(other_player):
                continue

            self.board[current_cup] += 1
            stones_to_distribute -= 1

        # stone in empty cup -> take stones on the opponents side
        if ( current_cup != self.get_house_id(self.current_player()) and
                self.board[current_cup] == 1 and
                current_cup >= self._get_first_cup(self.current_player()) and
                current_cup < self._get_last_cup(self.current_player())):
            opposite_cup = current_cup + self.number_of_cups+1
            if opposite_cup >= len(self.board):
                opposite_cup -= len(self.board)
            if self.board[opposite_cup] > 0:
                self.board[self._get_house(self.current_player())] += self.board[opposite_cup] + self.board[current_cup]
                self.board[opposite_cup] = 0
                self.board[current_cup] = 0

        # All stones empty, opponent takes all his stones
        if self._all_empty_number_of_cups(self.current_player()):
            for b in range(self.number_of_cups):
                self.board[self._get_house(other_player)] += self.board[other_player*self.number_of_cups + other_player + b]
                self.board[other_player*self.number_of_cups + other_player + b] = 0

        if current_cup != self.get_house_id(self.current_player()):
            self.player = 1 if self.current_player() == 0 else 0

        if not self._check_board_consistency(self.board):
            raise ValueError('The board is not consistent, some error must have happened. Old Board: ' + str(old_board) + ", move = " + str(b) +", new Board: " + str(self.get_board()))
        return True

    def get_board(self):
        return list(self.board)

    def game_over(self):
        player_board_one = self._get_player_board(0)
        player_board_two = self._get_player_board(1)

        player_one_empty = True
        for stone in player_board_one[:-1]:
            if stone > 0:
                player_one_empty = False

        player_two_empty = True
        for stone in player_board_two[:-1]:
            if stone > 0:
                player_two_empty = False
        
        scores = self.score()
        if scores[0] >= 36 or scores[1] >=36:
            return True

        return player_one_empty or player_two_empty

    def score(self):
        return [self.board[self.number_of_cups], self.board[2*self.number_of_cups + 1]]

    def allowed_moves(self):
        allowed_moves = []
        player_board = self._get_player_board(self.current_player())
        for b in range(len(player_board)-1):
            if player_board[b] > 0:
                allowed_moves.append(b + self.current_player()*self.number_of_cups + self.current_player())
        return allowed_moves

    def set_board(self, board):
        if len(board) != self.number_of_cups*2 + 2:
            raise ValueError('Passed board size does not match number of number_of_cups = ' + str(self.number_of_cups) + ' used to create the board')

        if not self._check_board_consistency(board):
            raise ValueError('The board is not consistent, cannot use it')

        self.board = list(board)

    def current_player(self):
        return self.player

    def set_current_player(self, player):
        if player >= 0 and player < 2:
            self.player = player
        else:
            raise ValueError('Passed player number is not 0 or 1')

    def current_player_score(self):
        return self.score()[self.current_player()]

    def _get_house(self, player):
        return self._player_houses[player]

    def get_house_id(self, player):
        return self._get_house(player)

    def get_input(self): # Der skal laves en anden function som ai skal bruge siden den ikke skal til at inputte i terminalen men det finder vi ud af 
        while True:
            question = input(f'Player {self.current_player() + 1} choose a cup \n')
            try:
                question = int(question)
                # assert isinstance(question, int)
                if question in [i + 1 for i in range(self.number_of_cups)]:
                    if self.current_player() == 0:
                        question -= 1
                        break
                    elif self.current_player() != 0:
                        question += 6
                        break
            except:
                print("Pick a valid number")
        return question

    def _get_first_cup(self, player):
        return player*self.number_of_cups + player

    def _get_last_cup(self, player):
        return self._get_first_cup(player) + self.number_of_cups - 1

    def _all_empty_number_of_cups(self, player):
        player_board = self._get_player_board(player)
        for stone in player_board[:-1]:
            if stone > 0:
                return False
        return True

    def _check_board_consistency(self, board):
        expected_stones = 2*self.stones*self.number_of_cups
        actual_stones = 0
        for s in board:
            actual_stones += s
        return actual_stones == expected_stones
        
    def _get_player_board(self, player):
        return self.get_board()[player*self.number_of_cups + player : player*self.number_of_cups + player + self.number_of_cups + 1]

    def copy(self):
        board = KalahaBoard(self.number_of_cups, self.stones)
        board.set_board(list(self.board))
        board.set_current_player(self.player)
        return board

class KalahaFight: #(KalahaBoard):
    def __init__(self, number_of_cups, number_of_stones):
        self.number_of_cups = number_of_cups
        self.stones = number_of_stones
    
    def fight(self):
        board = KalahaBoard(self.number_of_cups, self.stones)
        agent1 = MinimaxAgent(3,alpha_beta_pruning=True)
        agent2 = RandomAgent(1)

        last_invalid_player = None
        invalid_count = 0

        x = []
        # y = []
        for i in range(10):
            x_colmun = []
            # y_column = []
            while not board.game_over():
                board.print_board()
                if board.current_player() == 0:
                    #print(f'Player {board.current_player() + 1} choose a cup \n')
                    start_timer = timer()
                    valid = board.move(agent1.get_move(board))
                    end_timer = timer()
                    x_colmun.append(end_timer-start_timer)
                    #column_x = np.append(column_x,(end_timer-start_timer))

                    # valid = board.move(agent1.get_next_move(board))
                    # sleep(0.1)
                else:
                    #print(f'Player {board.current_player() + 1} choose a cup \n')
                    valid = board.move(agent2.get_move(board))
                    # valid = board.move(agent2.get_next_move(board))
                    # sleep(0.1)
                    # valid = board.move(random_move(board))
                if not valid:
                    if last_invalid_player == board.current_player():
                        invalid_count += 1
                    else:
                        invalid_count = 0
                        last_invalid_player = board.current_player()
                if invalid_count > 2:
                    break
                board.print_board()

            if invalid_count > 2:
                if last_invalid_player == 0:
                    # wins_agent1 += 1
                    print("player 1 wins")
                else:
                    # wins_agent2 += 1
                    print("player 2 wins")
            else:
                if board.score()[0] > board.score()[1]:
                    # wins_agent1 += 1
                    print("player 1 wins")
                elif board.score()[0] < board.score()[1]:
                    # wins_agent2 += 1
                    print("player 2 wins")
                else:
                    # draws += 1
                    print("its a draw")
            # y.append([i for i in range(len(x_colmun))])
            x.append(x_colmun)

            #y.append(np.array([i for i in range(len(x_colmun))]))
            board.reset_board()

        ### appending nan values such that all runs are the same length
        max_len = len(max(x,key=len))
        for index,value in enumerate(x):
            for i in range(max_len):
                if len(value)<max_len:
                    x[index].append(np.nan)  
        x_mean = np.asarray(x)
        ### finding the averages of all the runs for plotting
        x_mean = np.nanmean(x,axis=0)
        y = np.arange(0,max_len,1)
        plt.plot(y,x_mean)
        plt.show()

        


def main():
    random.seed(1)
    nr1 = KalahaFight(6, 6)
    nr1.fight()

main()
