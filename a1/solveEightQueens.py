import random
import copy
from optparse import OptionParser
import util

class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        """
        Value 1 indicates the position of queen
        """
        self.numberOfRuns = numberOfRuns
        self.verbose = verbose
        self.lectureCase = [[]]
        if lectureExample:
            self.lectureCase = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    def solve(self):
        solutionCounter = 0
        for i in range(self.numberOfRuns):
            if self.search(Board(self.lectureCase), self.verbose).getNumberOfAttacks() == 0:
                solutionCounter += 1
        print("Solved: %d/%d" % (solutionCounter, self.numberOfRuns))

    def search(self, board, verbose):
        """
        Hint: Modify the stop criterion in this function
        """
        newBoard = board
        i = 0 
        while True:
            if verbose:
                print("iteration %d" % i)
                print(newBoard.toString())
                print("# attacks: %s" % str(newBoard.getNumberOfAttacks()))
                print(newBoard.getCostBoard().toString(True))
            currentNumberOfAttacks = newBoard.getNumberOfAttacks()
            if currentNumberOfAttacks == 0:
                break
            (newBoard, newNumberOfAttacks, newRow, newCol) = newBoard.getBetterBoard()
            if currentNumberOfAttacks <= newNumberOfAttacks:
                i += 1
            else:
                i = 0
            if i > 100:
                break
        return newBoard

class Board:
    def __init__(self, squareArray = [[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray

    @staticmethod
    def initBoardWithRandomQueens():
        tmpSquareArray = [[ 0 for i in range(8)] for j in range(8)]
        for i in range(8):
            tmpSquareArray[random.randint(0,7)][i] = 1
        return tmpSquareArray
          
    def toString(self, isCostBoard=False):
        """
        Transform the Array in Board or cost Board to printable string
        """
        s = ""
        for i in range(8):
            for j in range(8):
                if isCostBoard: # Cost board
                    cost = self.squareArray[i][j]
                    s = (s + "%3d" % cost) if cost < 9999 else (s + "  q")
                else: # Board
                    s = (s + ". ") if self.squareArray[i][j] == 0 else (s + "q ")
            s += "\n"
        return s 

    def getCostBoard(self):
        """
        First Initalize all the cost as 9999. 
        After filling, the position with 9999 cost indicating the position of queen.
        """
        costBoard = Board([[ 9999 for i in range(8)] for j in range(8)])
        for r in range(8):
            for c in range(8):
                if self.squareArray[r][c] == 1:
                    for rr in range(8):
                        if rr != r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = 0
                            testboard.squareArray[rr][c] = 1
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard

    def getBetterBoard(self):
        """
        This function should return a tuple containing containing four values
        the new Board object, the new number of attacks, 
        the Column and Row of the new queen  
        For exmaple: 
            return (betterBoard, minNumOfAttack, newRow, newCol)
        The datatype of minNumOfAttack, newRow and newCol should be int
        """
        # current_attacks = self.getNumberOfAttacks()
        # better_board, min_num_attacks, new_col, new_row = copy.deepcopy(self), current_attacks, None, None
        # candidate_move = []
        # for col in range(8):
        #     for row in range(8):
        #         if self.squareArray[row][col] == 1:
        #             self.squareArray[row][col] = 0
        #             for rr in range(8):
        #                 if rr != row:
        #                     self.squareArray[rr][col] = 1
        #                     num_attacks = self.getNumberOfAttacks()
        #                     if num_attacks < min_num_attacks:
        #                         better_board = copy.deepcopy(self)
        #                         min_num_attacks = num_attacks
        #                         new_col = col
        #                         new_row = rr
        #                     self.squareArray[rr][col] = 0
        #             self.squareArray[row][col] = 1
        
        # return (better_board, min_num_attacks, new_row, new_col)
        current_num_attacks = self.getNumberOfAttacks() 
        cost_board = self.getCostBoard().squareArray
        min_num_attacks = 9999
        for row in range(8):
            for col in range(8):
                if cost_board[row][col] < min_num_attacks:
                    min_num_attacks = cost_board[row][col]

        candidate_move = list()
        for row in range(8):
            for col in range(8):
                if cost_board[row][col] == min_num_attacks:
                    candidate_move.append((row, col))

        new_row, new_col = random.choice(candidate_move) 
        new_board = copy.deepcopy(self)
        for row in range(8):
            if new_board.squareArray[row][new_col] == 1:
                new_board.squareArray[row][new_col] = 0
                new_board.squareArray[new_row][new_col] = 1
                break
        return (new_board, min_num_attacks, new_row, new_col)
        
    def getNumberOfAttacks(self):
        """
        This function should return the number of attacks of the current board
        The datatype of the return value should be int
        """
        cnt = 0
        for col in range(8):
            for row in range(8):
                if self.squareArray[row][col] == 1:
                    for i in range(col + 1, 8):
                        if self.squareArray[row][i] == 1:
                            cnt += 1
                        if row - i + col >= 0 and self.squareArray[row - i + col][i] == 1:
                            cnt += 1
                        if row + i - col < 8 and self.squareArray[row + i - col][i] == 1:
                            cnt += 1
                    break 
        return cnt


if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    random.seed(1)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    EightQueensAgent = SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)
    EightQueensAgent.solve()
