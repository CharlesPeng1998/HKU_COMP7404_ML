from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        prev_food_num = len(prevFood.asList())
        new_food_num = len(newFood.asList())

        new_food_pos = newFood.asList()
        new_ghost_pos = [ghostState.getPosition() for ghostState in newGhostStates]

        if len(new_food_pos) == 0:
          min_dis_food = 0.01 
        else:
          min_dis_food = min([manhattanDistance(newPos, food_pos) for food_pos in new_food_pos])
        
        if len(new_ghost_pos) == 0:
          min_dis_ghost = 99999
        else:
          min_dis_ghost = min([manhattanDistance(newPos, ghost_pos) for ghost_pos in new_ghost_pos])

        dis_food_reward = 50 / min_dis_food
        dis_ghost_reward = 0.5 * min_dis_ghost
        eating_reward = 0 
        if new_food_num < prev_food_num:
          eating_reward = 100

        evaluation = dis_food_reward + dis_ghost_reward + eating_reward

        return evaluation
        

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        legal_actions = gameState.getLegalActions(0)
        values = [self.miniMaxSearch(gameState.generateSuccessor(0, action), 1, self.depth) for action in legal_actions]
        max_value = max(values)
        best_index = [i for i in range(len(values)) if values[i] == max_value]
        choice = random.choice(best_index)
        return legal_actions[choice]
 
    def miniMaxSearch(self, gameState, agentIndex, depth):
      """
      Recursive mini-max search algorithm
      """
      if depth == 0:
        return self.evaluationFunction(gameState)

      if gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)

      legal_actions = gameState.getLegalActions(agentIndex)

      next_agent_index = agentIndex + 1 if agentIndex != gameState.getNumAgents() - \
          1 else 0
      next_depth = depth
      if agentIndex == gameState.getNumAgents() - 1:
        next_depth -= 1

      if agentIndex == 0:  # max player's move
        return max([self.miniMaxSearch(gameState.generateSuccessor(agentIndex, action), next_agent_index, next_depth) for action in legal_actions])
      else:  # min player's move
        return min([self.miniMaxSearch(gameState.generateSuccessor(agentIndex, action), next_agent_index, next_depth) for action in legal_actions])


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        legal_actions = gameState.getLegalActions(0)
        alpha_beta = [-999999, 999999]
        if gameState.getNumAgents() == 1:
          values = [self.maxValue(gameState.generateSuccessor(0, action), self.depth - 1, alpha_beta) for action in legal_actions]
        else:
          values = [self.minValue(gameState.generateSuccessor(0, action), 1, self.depth, alpha_beta) for action in legal_actions]
        max_value = max(values)
        best_index = [i for i in range(len(values)) if values[i] == max_value]
        choice = random.choice(best_index)
        return legal_actions[choice]
    
    def maxValue(self, gameState, depth, alpha_beta):
      if depth <= 0:
        return self.evaluationFunction(gameState)
      if gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)
      
      legal_actions = gameState.getLegalActions(0)
      value = -999999

      if gameState.getNumAgents() == 1:
        depth -= 1

      for action in legal_actions:
        next_state = gameState.generateSuccessor(0, action)
        if gameState.getNumAgents() == 1:
          value = max(value, self.maxValue(next_state, depth - 1, alpha_beta))
        else:
          value = max(value, self.minValue(next_state, 1, depth, alpha_beta))
        if value > alpha_beta[1]:
          return value
        alpha_beta[0] = max(value, alpha_beta[0])
      
      return value
      
    def minValue(self, gameState, agentIndex, depth, alpha_beta):
      print("debug in minValue of depth {}".format(depth))
      if depth <= 0:
        return self.evaluationFunction(gameState)
      if gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)
      
      legal_actions = gameState.getLegalActions(agentIndex)

      value = 999999
      
      for action in legal_actions:
        next_state = gameState.generateSuccessor(agentIndex, action)
        if agentIndex == gameState.getNumAgents() - 1:
          value = min(value, self.maxValue(next_state, depth - 1, alpha_beta))
        else:
          value = min(value, self.minValue(next_state, agentIndex + 1, depth, alpha_beta))
        print("debug value of minValue = {}".format(value))
        if value < alpha_beta[0]:
          return value
        alpha_beta[1] = min(value, alpha_beta[1])
      
      print("debug alpha-beta = {}".format(alpha_beta))
      
      return value

      
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

