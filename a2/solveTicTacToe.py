#################################################################################
#     File Name           :     solveTicTacToe.py
#     Created By          :     Chen Guanying 
#     Creation Date       :     [2017-03-18 19:17]
#     Last Modified       :     [2017-03-18 19:17]
#     Description         :      
#################################################################################

import copy
from warnings import simplefilter
import util 
import sys
import random
import time
from optparse import OptionParser

class GameState:
    """
      Game state of 3-Board Misere Tic-Tac-Toe
      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your search agents. Please do not remove anything, 
      however.
    """
    def __init__(self):
        """
          Represent 3 boards with lists of boolean value 
          True stands for X in that position
        """
        self.boards = [[False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False]]

    def generateSuccessor(self, action):
        """
          Input: Legal Action
          Output: Successor State
        """
        suceessorState = copy.deepcopy(self)
        ASCII_OF_A = 65
        boardIndex = ord(action[0]) - ASCII_OF_A
        pos = int(action[1])
        suceessorState.boards[boardIndex][pos] = True
        return suceessorState

    # Get all valid actions in 3 boards
    def getLegalActions(self, gameRules):
        """
          Input: GameRules
          Output: Legal Actions (Actions not in dead board) 
        """
        ASCII_OF_A = 65
        actions = []
        for b in range(3):
            if gameRules.deadTest(self.boards[b]): continue
            for i in range(9):
                if not self.boards[b][i]:
                    actions.append( chr(b+ASCII_OF_A) + str(i) )
        return actions

    # Print living boards
    def printBoards(self, gameRules):
        """
          Input: GameRules
          Print the current boards to the standard output
          Dead boards will not be printed
        """
        titles = ["A", "B", "C"]
        boardTitle = ""
        boardsString = ""
        for row in range(3):
            for boardIndex in range(3):
                # dead board will not be printed
                if gameRules.deadTest(self.boards[boardIndex]): continue
                if row == 0: boardTitle += titles[boardIndex] + "      "
                for i in range(3):
                    index = 3 * row + i
                    if self.boards[boardIndex][index]: 
                        boardsString += "X "
                    else:
                        boardsString += str(index) + " "
                boardsString += " "
            boardsString += "\n"
        print(boardTitle)
        print(boardsString)


class GameRules:
    """
      This class defines the rules in 3-Board Misere Tic-Tac-Toe. 
      You can add more rules in this class, e.g the fingerprint (patterns).
      However, please do not remove anything.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """
        {}
        
    def deadTest(self, board):
        """
          Check whether a board is a dead board
        """
        if board[0] and board[4] and board[8]:
            return True
        if board[2] and board[4] and board[6]:
            return True
        for i in range(3):
            #check every row
            row = i * 3
            if board[row] and board[row+1] and board[row+2]:
                return True
            #check every column
            if board[i] and board[i+3] and board[i+6]:
                return True
        return False

    def isGameOver(self, boards):
        """
          Check whether the game is over  
        """
        return self.deadTest(boards[0]) and self.deadTest(boards[1]) and self.deadTest(boards[2])

class MonoidValue():
    """
    THe misere quotient of a certain layout of tic-tac-toe board.
    """
    def __init__(self, pow_a, pow_b, pow_c, pow_d):
        self.pow_a = pow_a
        self.pow_b = pow_b
        self.pow_c = pow_c
        self.pow_d = pow_d
        self.simplify()
    
    def __mul__(self, other):
        if isinstance(other, MonoidValue):
            ret = MonoidValue(self.pow_a + other.pow_a, self.pow_b + other.pow_b,
                              self.pow_c + other.pow_c, self.pow_d + other.pow_d)
            ret.simplify()
            return ret
        else:
            raise ValueError("Incorrect operand type for '*' operator!") 
    
    def __eq__(self, other):
        if isinstance(other, MonoidValue):
            return (self.pow_a == other.pow_a and self.pow_b == other.pow_b and self.pow_c == other.pow_c and self.pow_d == other.pow_d)
        else:
            raise ValueError("Incorrect operand type for '==' operator!")
    
    def __str__(self):
        """
        For print debug.
        """
        if self.pow_a == 0 and self.pow_b == 0 and self.pow_c == 0 and self.pow_d == 0:
            return "1"
        ret = ""
        if self.pow_a != 0:
            ret += "a{}".format(self.pow_a)
        if self.pow_b != 0:
            ret += "b{}".format(self.pow_b)
        if self.pow_c != 0:
            ret += "c{}".format(self.pow_c)
        if self.pow_d != 0:
            ret += "d{}".format(self.pow_d)
        return ret
    
    def simplify(self):
        while True:
            simplified = False
            if self.pow_a >= 2:
                self.pow_a -= 2
                simplified = True
            if self.pow_b >= 3:
                self.pow_b -= 2
                simplified = True
            if self.pow_b >=2 and self.pow_c >= 1:
                self.pow_b -= 2
                simplified = True
            if self.pow_c >= 3:
                self.pow_c -= 1
                self.pow_a += 1
                simplified = True
            if self.pow_b >= 2 and self.pow_d >= 1:
                self.pow_b -= 2
                simplified = True
            if self.pow_c >= 1 and self.pow_d >= 1:
                self.pow_c -= 1
                self.pow_a += 1
                simplified = True
            if self.pow_d >= 2:
                self.pow_d -= 2
                self.pow_c += 2
                simplified = True
            
            if not simplified:
                break

def rotateBoard(board):
    """
    Rotate given board for 90 degrees.
    """
    new_board = copy.deepcopy(board)
    for i in range(3):
        for j in range(i):
            new_board[i * 3 + j], new_board[j * 3 + i] = new_board[j * 3 + i], new_board[i * 3 + j]
    
    for j in range(3):
        new_board[j], new_board[2 * 3 + j] = new_board[2 * 3 + j], new_board[j] 
    
    return new_board

def rightLeftFlipBoard(board):
    """
    Right-left flip the board.
    """
    new_board = copy.deepcopy(board)
    for i in range(3):
        new_board[i * 3], new_board[i * 3 + 2] = new_board[i * 3 + 2], new_board[i * 3]
    return new_board

def upDownFlipBoard(board):
    """
    Up-down flip the board.
    """
    new_board = copy.deepcopy(board)
    for j in range(3):
        new_board[j], new_board[2 * 3 + j] = new_board[2 * 3 + j], new_board[j] 
    return new_board


class TicTacToeAgent():
    """
      When move first, the TicTacToeAgent should be able to chooses an action to always beat 
      the second player.

      You have to implement the function getAction(self, gameState, gameRules), which returns the 
      optimal action (guarantee to win) given the gameState and the gameRules. The return action
      should be a string consists of a letter [A, B, C] and a number [0-8], e.g. A8. 

      You are welcome to add more helper functions in this class to help you. You can also add the
      helper function in class GameRules, as function getAction() will take GameRules as input.
      
      However, please don't modify the name and input parameters of the function getAction(), 
      because autograder will call this function to check your algorithm.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """
        self.p_position_values = [MonoidValue(1, 0, 0, 0), MonoidValue(
            0, 2, 0, 0), MonoidValue(0, 1, 1, 0), MonoidValue(0, 0, 2, 0)]
        self.max_depth = 2

    @staticmethod
    def getBoardMisereQuotient(board):
        for i in range(4):
            rot_board = rotateBoard(board)
            for j in range(3):
                if j == 0:
                    test_board = rot_board
                elif j == 1:
                    test_board = rightLeftFlipBoard(rot_board)
                elif j == 2:
                    test_board = upDownFlipBoard(rot_board)

                if test_board == [False, False, False, False, False, False, False, False, False]:
                    return MonoidValue(0, 0, 1, 0)
                elif test_board == [False, False, False, False, True, False, False, False, False]:
                    return MonoidValue(0, 0, 2, 0)
                elif test_board == [True, True, False, False, False, False, False, False, False]:
                    return MonoidValue(1, 0, 0, 1)
                elif test_board == [True, False, True, False, False, False, False, False, False]:
                    return MonoidValue(0, 1, 0, 0)
                elif test_board == [True, False, False, False, True, False, False, False, False]:
                    return MonoidValue(0, 1, 0, 0)
                elif test_board == [True, False, False, False, False, True, False, False, False]:
                    return MonoidValue(0, 1, 0, 0)
                elif test_board == [True, False, False, False, False, False, False, False, True]:
                    return MonoidValue(1, 0, 0, 0)
                elif test_board == [False, True, False, True, False, False, False, False, False]:
                    return MonoidValue(1, 0, 0, 0)
                elif test_board == [False, True, False, False, True, False, False, False, False]:
                    return MonoidValue(0, 1, 0, 0)
                elif test_board == [False, True, False, False, False, False, False, True, False]:
                    return MonoidValue(1, 0, 0, 0)
                elif test_board == [True, True, False, True, False, False, False, False, False]:
                    return MonoidValue(0, 1, 0, 0)
                elif test_board == [True, True, False, False, True, False, False, False, False]:
                    return MonoidValue(1, 1, 0, 0)
                elif test_board == [True, True, False, False, False, True, False, False, False]:
                    return MonoidValue(0, 0, 0, 1)
                elif test_board == [True, True, False, False, False, False, True, False, False]:
                    return MonoidValue(1, 0, 0, 0)
                elif test_board == [True, True, False, False, False, False, False, True, False]:
                    return MonoidValue(0, 0, 0, 1)
                elif test_board == [True, True, False, False, False, False, False, False, True]:
                    return MonoidValue(0, 0, 0, 1)
                elif test_board == [True, False, True, False, True, False, False, False, False]:
                    return MonoidValue(1, 0, 0, 0)
                elif test_board == [True, False, True, False, False, False, True, False, False]:
                    return MonoidValue(1, 1, 0, 0)
                elif test_board == [True, False, True, False, False, False, False, True, False]:
                    return MonoidValue(1, 0, 0, 0)
                elif test_board == [True, False, False, False, True, True, False, False, False]:
                    return MonoidValue(1, 0, 0, 0)
                elif test_board == [False, True, False, True, True, False, False, False, False]:
                    return MonoidValue(1, 1, 0, 0)
                elif test_board == [False, True, False, True, False, True, False, False, False]:
                    return MonoidValue(0, 1, 0, 0)
                elif test_board == [True, True, False, True, True, False, False, False, False]:
                    return MonoidValue(1, 0, 0, 0)
                elif test_board == [True, True, False, True, False, True, False, False, False]:
                    return MonoidValue(1, 0, 0, 0)
                elif test_board == [True, True, False, True, False, False, False, False, True]:
                    return MonoidValue(1, 0, 0, 0)
                elif test_board == [True, True, False, False, True, True, False, False, False]:
                    return MonoidValue(0, 1, 0, 0)
                elif test_board == [True, True, False, False, True, False, True, False, False]:
                    return MonoidValue(0, 1, 0, 0)
                elif test_board == [True, True, False, False, False, True, True, False, False]:
                    return MonoidValue(0, 1, 0, 0)
                elif test_board == [True, True, False, False, False, True, False, True, False]:
                    return MonoidValue(1, 1, 0, 0)
                elif test_board == [True, True, False, False, False, True, False, False, True]:
                    return MonoidValue(1, 1, 0, 0)
                elif test_board == [True, True, False, False, False, False, True, True, False]:
                    return MonoidValue(0, 1, 0, 0)
                elif test_board == [True, True, False, False, False, False, True, False, True]:
                    return MonoidValue(0, 1, 0, 0)
                elif test_board == [True, True, False, False, False, False, False, True, True]:
                    return MonoidValue(1, 0, 0, 0)
                elif test_board == [True, False, True, False, True, False, False, True, False]:
                    return MonoidValue(0, 1, 0, 0)
                elif test_board == [True, False, True, False, False, False, True, False, True]:
                    return MonoidValue(1, 0, 0, 0)
                elif test_board == [True, False, False, False, True, True, False, True, False]:
                    return MonoidValue(0, 1, 0, 0)
                elif test_board == [False, True, False, True, False, True, False, True, False]:
                    return MonoidValue(1, 0, 0, 0)
                elif test_board == [True, True, False, True, False, True, False, False, True]:
                    return MonoidValue(0, 1, 0, 0)
                elif test_board == [True, True, False, False, True, True, True, False, False]:
                    return MonoidValue(1, 0, 0, 0)
                elif test_board == [True, True, False, False, False, True, True, True, False]:
                    return MonoidValue(1, 0, 0, 0)
                elif test_board == [True, True, False, False, False, True, True, False, True]:
                    return MonoidValue(1, 0, 0, 0)
                elif test_board == [True, True, False, True, False, True, False, True, True]:
                    return MonoidValue(1, 0, 0, 0)
                elif test_board == [True, True, False, True, False, True, False, True, False]:
                    return MonoidValue(0, 1, 0, 0)

        return MonoidValue(0, 0, 0, 0)
    
    def isP_Position(self, gameState):
        quotient = MonoidValue(0, 0, 0, 0)

        for board in gameState.boards:
            board_quotient = self.getBoardMisereQuotient(board)        
            quotient = quotient * board_quotient

        if quotient in self.p_position_values:
            return True
        else:
            return False
    
    def evaluation(self, gameState, gameRules, max_player_turn):
        game_over = gameRules.isGameOver(gameState.boards)
        is_p_position = self.isP_Position(gameState)

        if max_player_turn:  # if it is Max's turn
            if game_over:
                return 100 
            if is_p_position:
                return -10
            else:
                return 5 
        else:  # if it is Min's turn
            if game_over:
                return -100 
            if is_p_position:
                return 10
            else:
                return -5 

    def maxSearch(self, gameState, gameRules, depth):
        if depth == self.max_depth:
            return (self.evaluation(gameState, gameRules, True), None)
        if gameRules.isGameOver(gameState.boards):
            return (self.evaluation(gameState, gameRules, True), None)
        
        legal_actions = gameState.getLegalActions(gameRules)
        best_value = -999999
        best_action = None

        for action in legal_actions:
            next_state = gameState.generateSuccessor(action)
            value = self.minSearch(next_state, gameRules, depth)

            if value > best_value:
                best_value = value
                best_action = action
        
        return (best_value, best_action)
    
    def minSearch(self, gameState, gameRules, depth):
        if gameRules.isGameOver(gameState.boards):
            return self.evaluation(gameState, gameRules, False)
        
        legal_actions = gameState.getLegalActions(gameRules)
        best_value = 999999

        for action in legal_actions:
            next_state = gameState.generateSuccessor(action)
            value, _ = self.maxSearch(next_state, gameRules, depth + 1)

            if value < best_value:
                best_value = value

        return best_value

    def getAction(self, gameState, gameRules):
        _, best_action = self.maxSearch(gameState, gameRules, 1)
        return best_action


class randomAgent():
    """
      This randomAgent randomly choose an action among the legal actions
      You can set the first player or second player to be random Agent, so that you don't need to
      play the game when debugging the code. (Time-saving!)
      If you like, you can also set both players to be randomAgent, then you can happily see two 
      random agents fight with each other.
    """
    def getAction(self, gameState, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return random.choice(actions)


class keyboardAgent():
    """
      This keyboardAgent return the action based on the keyboard input
      It will check whether the input actions is legal or not.
    """
    def checkUserInput(self, gameState, action, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return action in actions

    def getAction(self, gameState, gameRules):
        action = input("Your move: ")
        while not self.checkUserInput(gameState, action, gameRules):
            print("Invalid move, please input again")
            action = input("Your move: ")
        return action 

class Game():
    """
      The Game class manages the control flow of the 3-Board Misere Tic-Tac-Toe
    """
    def __init__(self, numOfGames, muteOutput, randomAI, AIforHuman):
        """
          Settings of the number of games, whether to mute the output, max timeout
          Set the Agent type for both the first and second players. 
        """
        self.numOfGames  = numOfGames
        self.muteOutput  = muteOutput
        self.maxTimeOut  = 30 

        self.AIforHuman  = AIforHuman
        self.gameRules   = GameRules()
        self.AIPlayer    = TicTacToeAgent()

        if randomAI:
            self.AIPlayer = randomAgent()
        else:
            self.AIPlayer = TicTacToeAgent()
        if AIforHuman:
            self.HumanAgent = randomAgent()
        else:
            self.HumanAgent = keyboardAgent()

    def run(self):
        """
          Run a certain number of games, and count the number of wins
          The max timeout for a single move for the first player (your AI) is 30 seconds. If your AI 
          exceed this time limit, this function will throw an error prompt and return. 
        """
        numOfWins = 0;
        for i in range(self.numOfGames):
            gameState = GameState()
            agentIndex = 0 # 0 for First Player (AI), 1 for Second Player (Human)
            while True:
                if agentIndex == 0: 
                    timed_func = util.TimeoutFunction(self.AIPlayer.getAction, int(self.maxTimeOut))
                    try:
                        start_time = time.time()
                        action = timed_func(gameState, self.gameRules)
                    except util.TimeoutFunctionException:
                        print("ERROR: Player %d timed out on a single move, Max %d Seconds!" % (agentIndex, self.maxTimeOut))
                        return False

                    if not self.muteOutput:
                        print("Player 1 (AI): %s" % action)
                else:
                    action = self.HumanAgent.getAction(gameState, self.gameRules)
                    if not self.muteOutput:
                        print("Player 2 (Human): %s" % action)
                gameState = gameState.generateSuccessor(action)
                if self.gameRules.isGameOver(gameState.boards):
                    break
                if not self.muteOutput:
                    gameState.printBoards(self.gameRules)

                agentIndex  = (agentIndex + 1) % 2
            if agentIndex == 0:
                print("****player 2 wins game %d!!****" % (i+1))
            else:
                numOfWins += 1
                print("****Player 1 wins game %d!!****" % (i+1))

        print("\n****Player 1 wins %d/%d games.**** \n" % (numOfWins, self.numOfGames))


def test():
    agent = TicTacToeAgent()
    test_num = 5
    for i in range(test_num):
        print('Test {}'.format(i))
        boards = list()
        for i in range(3):
            board = [random.choice([True, False, False]) for i in range(9)]
            boards.append(board)

        for k in range(len(boards)): 
            quotient = agent.getBoardMisereQuotient(boards[k])
            print('board{} = {}, quotient = {}'.format(k, boards[k], quotient))
        
        game_state = GameState()
        game_state.boards = boards
        print("The boards are P = {}".format(agent.isP_Position(game_state)))
        print("--------------------------------------------------")


if __name__ == "__main__":
    """
      main function
      -n: Indicates the number of games
      -m: If specified, the program will mute the output
      -r: If specified, the first player will be the randomAgent, otherwise, use TicTacToeAgent
      -a: If specified, the second player will be the randomAgent, otherwise, use keyboardAgent
    """
    # Uncomment the following line to generate the same random numbers (useful for debugging)
    # random.seed(1)  
    parser = OptionParser()
    parser.add_option("-n", dest="numOfGames", default=1, type="int")
    parser.add_option("-m", dest="muteOutput", action="store_true", default=False)
    parser.add_option("-r", dest="randomAI", action="store_true", default=False)
    parser.add_option("-a", dest="AIforHuman", action="store_true", default=False)
    (options, args) = parser.parse_args()
    ticTacToeGame = Game(options.numOfGames, options.muteOutput, options.randomAI, options.AIforHuman)
    ticTacToeGame.run()
