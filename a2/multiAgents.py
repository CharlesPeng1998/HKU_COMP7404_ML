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
        alpha, beta = -999999, 999999
        _, action = self.maxValue(gameState, self.depth, alpha, beta)
        
        return action 
    
    def maxValue(self, gameState, depth, alpha, beta):
      if depth <= 0:
        return (self.evaluationFunction(gameState), None)
      if gameState.isWin() or gameState.isLose():
        return (self.evaluationFunction(gameState), None)

      legal_actions = gameState.getLegalActions(0)
      best_value = -999999
      best_action = None

      for action in legal_actions:
        next_state = gameState.generateSuccessor(0, action)
        if gameState.getNumAgents() == 1:
          value, _ = self.maxValue(next_state, depth - 1, alpha, beta)
        else:
          value, _ = self.minValue(next_state, 1, depth, alpha, beta)

        if value > best_value:
          best_value = value
          best_action = action

        if best_value > beta:
          return (best_value, best_action)
        alpha = max(best_value, alpha)
      
      return (best_value, best_action)
      
    def minValue(self, gameState, agentIndex, depth, alpha, beta):
      if depth <= 0:
        return (self.evaluationFunction(gameState), None)
      if gameState.isWin() or gameState.isLose():
        return (self.evaluationFunction(gameState), None)

      legal_actions = gameState.getLegalActions(agentIndex)
      best_value = 999999
      best_action = None
      
      for action in legal_actions:
        next_state = gameState.generateSuccessor(agentIndex, action)
        if agentIndex == gameState.getNumAgents() - 1:
          value, _ = self.maxValue(next_state, depth - 1, alpha, beta)
        else:
          value, _ = self.minValue(next_state, agentIndex + 1, depth, alpha, beta)

        if value < best_value:
          best_value = value
          best_action = action        

        if best_value < alpha:
          return (best_value, best_action)
        beta = min(best_value, beta)
      
      return (best_value, best_action) 
      
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
        return self.maxSearch(gameState, self.depth)[1]
    
    def maxSearch(self, gameState, depth):
      if depth <= 0:
        return (self.evaluationFunction(gameState), None)
      if gameState.isWin() or gameState.isLose():
        return (self.evaluationFunction(gameState), None)

      legal_actions = gameState.getLegalActions(0)
      values = [self.expectedSearch(gameState.generateSuccessor(
          0, action), 1, depth) for action in legal_actions]

      best_value = max(values)
      best_index = [i for i in range(len(values)) if values[i] == best_value]
      choice = random.choice(best_index)

      return (best_value, legal_actions[choice])
      
    def expectedSearch(self, gameState, agentIndex, depth):
      if depth <= 0:
        return self.evaluationFunction(gameState)
      if gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)

      legal_actions = gameState.getLegalActions(agentIndex)

      if agentIndex == gameState.getNumAgents() - 1:
        values = [self.maxSearch(gameState.generateSuccessor(
            agentIndex, action), depth - 1)[0] for action in legal_actions]
      else:
        values = [self.expectedSearch(gameState.generateSuccessor(
            agentIndex, action), agentIndex + 1, depth) for action in legal_actions]

      expected_value = sum(values) / len(values)

      return expected_value

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: 
      In this evaluation function, following values are considered:
      1. Distance to nearest normal ghost (not scared ghost)
      2. Distance to nearest scared ghost
      3. Distance to nearest food
      4. Number of remaining food
      5. Number of remaining capsules
      6. Current game score
      
      Note: The distances mentioned above are just Manhattan distance, not
            the actual distance.
      
      The final evaluation value is the linear combination of values above with
      self-customized coefficient.
    """
    # Return current score if game is over
    if currentGameState.isWin() or currentGameState.isLose():
      return currentGameState.getScore()
    
    ghost_states = currentGameState.getGhostStates()
    normal_ghost_states = list()
    scared_ghost_states = list()
    for ghost_state in ghost_states:
      if ghost_state.scaredTimer == 0:
        normal_ghost_states.append(ghost_state)
      else:
        scared_ghost_states.append(ghost_state)
    
    pacman_pos = currentGameState.getPacmanPosition()
    
    # Distance to nearest normal ghost
    if normal_ghost_states:
      dis_normal_ghost = min([manhattanDistance(
          pacman_pos, ghost_state.getPosition()) for ghost_state in normal_ghost_states])
    else:
      dis_normal_ghost = 999999

    # Distance to nearest scared ghost
    if scared_ghost_states:
      dis_scared_ghost = min([manhattanDistance(
          pacman_pos, ghost_state.getPosition()) for ghost_state in scared_ghost_states])
    else:
      dis_scared_ghost = 0
    
    # Number of remaining food
    num_food = currentGameState.getNumFood()

    # Distance to nearest remaining food
    dis_food = min([manhattanDistance(pacman_pos, food_pos)
                   for food_pos in currentGameState.getFood().asList()])
    
    # Number of capsules
    num_capsule = len(currentGameState.getCapsules())

    # Current game score
    game_score = currentGameState.getScore()

    value = game_score + (-2 * dis_food) + 1 * dis_normal_ghost + \
        (-2 * dis_scared_ghost) + (-30 * num_capsule) + (-10 * num_food)

    return value

# Abbreviation
better = betterEvaluationFunction

