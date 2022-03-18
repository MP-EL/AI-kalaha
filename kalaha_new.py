from time import sleep
import numpy as np
from timeit import default_timer as timer
from copy import deepcopy

import sys, signal


def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit()
signal.signal(signal.SIGINT, signal_handler)

class HumanAgent:
    def __init__(self):
        pass
    
    def get_move(self, board): 
        while True:
            question = input(f'Player {board.current_player() + 1} choose a cup \n')
            try:
                question = int(question)
                # assert isinstance(question, int)
                if question in [i + 1 for i in range(board.number_of_cups)]:
                    if board.current_player() == 0:
                        question -= 1
                        break
                    elif board.current_player() != 0:
                        question += 6
                        break
            except:
                print("Pick a valid number")
        return question

class RandomAgent:
    def __init__(self):
        pass
    
    def get_move(self,board):
        return np.random.choice(board.allowed_moves())

class MaxAgent:
    def __init__(self):
        pass
    def get_move(self, board):
        player = board.current_player()
        get_board = board.get_board()
        if player == 0:
            part = get_board[0:6]
        elif player == 1:
            part = get_board[7:-1]
            part = part.reverse()
        moves = board.allowed_moves()
        index = np.argmax(part)
        return moves[index]

class MinimaxAgent:
    def __init__(self, max_depth=5, alpha_beta_pruning=True):
        self.max_depth = max_depth
        self.alpha_beta_pruning = alpha_beta_pruning
    
    def heuristic(self, board):
        player = board.current_player()
        if player == self.original_player:
            return board.score()[player] - board.score()[~player]
        else:
            return board.score()[~player] - board.score()[player]

    def get_move(self, board):
        """Gets the best move by performing minimax to retrieve the highest value move.
        Args:
            board (KalahaBoard): KalahaBoard class (Use the class in this script).
        Returns:
            int: the current best move retrieved from the minimax algo.
        """
        moves_and_scores = []
        moves = board.allowed_moves()
        self.original_player = board.current_player()
        #If there is only 1 legal move pick that move.
        if len(moves) == 1:
            return moves[0]
        #for every legal move run the minimax algo recursively to test all moves down to the desired depth.
        for move in moves:
            moves_and_scores.append([self._minimax(board, False, 0, move, float('-inf'), float('inf')), move])
        #get max value of the minimax outputs. 
        max_score = max([i[0] for i in moves_and_scores])

        best_moves = []
        #choose all moves that are equal to max_score
        for move_and_score in moves_and_scores:
            if move_and_score[0] == max_score:
                best_moves.append(move_and_score[1])
        #Choose a random move from the max_score moves (For some reason this makes it much stronger than when choosing the first move with the highest score).
        rand = np.random.choice([i for i in best_moves])
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
            return self.heuristic(board)
            # return board.score()[board.current_player()]
        
        #Make a copy of the board to test the moves on.
        # new_board = board.copy()
        new_board = deepcopy(board)
        new_board.move(move)
        moves = new_board.allowed_moves()
        
        #find the max value from the minimax output and perform alpha beta pruning.
        if is_max_player:
            best_value = -100
            for move in moves:
                best_value = np.max([best_value, self._minimax(new_board, False, current_depth + 1, move, alpha, beta)])
                if self.alpha_beta_pruning:
                    
                    alpha = np.max([best_value, alpha])
                    if beta <= alpha:
                        return best_value
        #The same as above but with the min part of minimax instead of max
        else:
            best_value = 100
            for move in moves:
                best_value = np.min([best_value, self._minimax(new_board, True, current_depth + 1, move, alpha, beta)])
                if self.alpha_beta_pruning:
                    beta = np.min([best_value, beta])
                    if beta <= alpha: 
                        return best_value
        return best_value

class KalahaBoard:
    def __init__(self, number_of_cups, number_of_stones, visual = False):
        self.number_of_cups = number_of_cups
        self.stones = number_of_stones
        self.visual = visual
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
        if self.visual:
            # os.system('cls' if os.name == 'nt' else 'clear')
            BP1 = self.board[0:self.number_of_cups + 1]
            BP2 = self.board[1+self.number_of_cups: self.number_of_cups*2 + 2]
            # print(BP1)
            # print(BP2)
            if self.current_player() == 0:
                print("allowed moves", [i + 1 for i in self.allowed_moves()])
            else:
                print("allowed moves", self.allowed_moves())
            BP2.reverse()
            print(f"\nPocket # :  {'  '.join([str(i + 1) for i in range(self.number_of_cups)][::-1])}")
            print('P2 -->', BP2[:1], BP2[1:self.number_of_cups+1])
            print('P1 --> ', '  ', BP1[0:self.number_of_cups],BP1[self.number_of_cups:])
            print(f"Pocket # :  {'  '.join([str(i + 1) for i in range(self.number_of_cups)])}")
            BP2.reverse()
        else:
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
        if self._are_the_cups_empty(self.current_player()):
            for b in range(self.number_of_cups):
                self.board[self._get_house(other_player)] += self.board[other_player*self.number_of_cups + other_player + b]
                self.board[other_player*self.number_of_cups + other_player + b] = 0

        if current_cup != self.get_house_id(self.current_player()):
            self.player = 1 if self.current_player() == 0 else 0

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

    def _get_first_cup(self, player):
        return player*self.number_of_cups + player

    def _get_last_cup(self, player):
        return self._get_first_cup(player) + self.number_of_cups - 1

    def _are_the_cups_empty(self, player):
        player_board = self._get_player_board(player)
        for stone in player_board[:-1]:
            if stone > 0:
                return False
        return True
        
    def _get_player_board(self, player):
        return self.get_board()[player*self.number_of_cups + player : player*self.number_of_cups + player + self.number_of_cups + 1]

    def copy(self):
        board = KalahaBoard(self.number_of_cups, self.stones)
        # board.set_board(list(self.board))
        board.set_current_player(self.player)
        return board

class KalahaFight: #(KalahaBoard):
    def __init__(self, number_of_cups, number_of_stones):
        self.number_of_cups = number_of_cups
        self.stones = number_of_stones
    
    def fight(self):
        board = KalahaBoard(self.number_of_cups, self.stones, visual=True)
        agent2 = MinimaxAgent(4,alpha_beta_pruning=True)
        # agent2 = MinimaxAgent(4,alpha_beta_pruning=True)
        # agent2 = RandomAgent()
        agent1 = HumanAgent()
        p1 = 0
        p2 = 0
        games = 0
        for i in range(20):
            timers = []
            while not board.game_over():
                board.print_board()
                
                if board.current_player() == 0:
                    start_timer = timer()
                    valid = board.move(agent1.get_move(board))
                    end_timer = timer()
                    timers.append(end_timer - start_timer)
                else:
                    valid = board.move(agent2.get_move(board))
                
            if board.score()[0] > board.score()[1]:
                print("player 1 wins")
                p1 += 1
                games += 1
            elif board.score()[0] < board.score()[1]:
                print("player 2 wins")
                p2 += 1
                games += 1
            else:
                print("its a draw")
                games += 1
            print(f"Game took {np.sum(timers):.2f} seconds")
            board.reset_board()
        print(f"P1 win %: {(p1 / games):.2f}")
        print(f"P2 win %: {(p2 / games):.2f}")
        print(f"Draw   %: {((games - (p1 + p2)) / games):.2f}")

def main():
    nr1 = KalahaFight(6, 6)
    nr1.fight()

main()
