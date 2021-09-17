"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    from game import Directions
    frontier = util.Stack()
    explored_states_set = set()
    nodes_list = list()
    actions_list = list()

    start_node = tuple([problem.getStartState(), Directions.STOP, 0, -1])
    frontier.push(start_node)
    nodes_list.append(start_node)

    # Start searching
    while not frontier.isEmpty():
        expand_node = frontier.pop()

        # If goal arrived, retrieve actions list
        if problem.isGoalState(expand_node[0]):
            current_node = expand_node
            while current_node[3] != -1:
                actions_list.append(current_node[1])
                current_node = nodes_list[current_node[3]]
            break

        # Make sure this is a graph search algorithm 
        if expand_node[0] in explored_states_set:
            continue
        explored_states_set.add(expand_node[0])
        successors = problem.getSuccessors(expand_node[0])
        for successor in successors:
            if successor[0] in explored_states_set:
                continue
            successor_node = tuple([successor[0], successor[1], len(nodes_list), expand_node[2]])
            nodes_list.append(successor_node)
            frontier.push(successor_node)

    return actions_list[::-1]

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    from game import Directions
    frontier = util.Queue()
    explored_states_set = set()
    nodes_list = list()
    actions_list = list()

    start_node = tuple([problem.getStartState(), Directions.STOP, 0, -1])
    frontier.push(start_node)
    nodes_list.append(start_node)

    # Start searching
    while not frontier.isEmpty():
        expand_node = frontier.pop()

        # If goal arrived, retrieve actions list
        if problem.isGoalState(expand_node[0]):
            current_node = expand_node
            while current_node[3] != -1:
                actions_list.append(current_node[1])
                current_node = nodes_list[current_node[3]]
            break

        # Make sure this is a graph search algorithm 
        if expand_node[0] in explored_states_set:
            continue
        explored_states_set.add(expand_node[0])
        successors = problem.getSuccessors(expand_node[0])
        for successor in successors:
            if successor[0] in explored_states_set:
                continue
            successor_node = tuple([successor[0], successor[1], len(nodes_list), expand_node[2]])
            nodes_list.append(successor_node)
            frontier.push(successor_node)

    return actions_list[::-1]

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    from game import Directions
    frontier = util.PriorityQueue()
    explored_states_set = set()
    nodes_list = list()
    actions_list = list()

    start_node = tuple([problem.getStartState(), Directions.STOP, 0, -1, 0])
    frontier.push(start_node, 0)
    nodes_list.append(start_node)

    # Start searching
    while not frontier.isEmpty():
        expand_node = frontier.pop()

        # If goal arrived, retrieve actions list
        if problem.isGoalState(expand_node[0]):
            current_node = expand_node
            while current_node[3] != -1:
                actions_list.append(current_node[1])
                current_node = nodes_list[current_node[3]]
            break

        # Make sure this is a graph search algorithm 
        if expand_node[0] in explored_states_set:
            continue
        explored_states_set.add(expand_node[0])
        successors = problem.getSuccessors(expand_node[0])
        for successor in successors:
            if successor[0] in explored_states_set:
                continue
            successor_node = tuple([successor[0], successor[1], len(nodes_list), expand_node[2], expand_node[4] + successor[2]])
            nodes_list.append(successor_node)
            frontier.push(successor_node, expand_node[4] + successor[2])

    return actions_list[::-1]

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    from game import Directions
    frontier = util.PriorityQueue()
    explored_states_set = set()
    nodes_list = list()
    actions_list = list()

    start_state_hvalue = heuristic(problem.getStartState(), problem)
    start_node = tuple([problem.getStartState(), Directions.STOP, 0, -1, 0])
    frontier.push(start_node, start_state_hvalue)
    nodes_list.append(start_node)

    # Start searching
    while not frontier.isEmpty():
        expand_node = frontier.pop()

        # If goal arrived, retrieve actions list
        if problem.isGoalState(expand_node[0]):
            current_node = expand_node
            while current_node[3] != -1:
                actions_list.append(current_node[1])
                current_node = nodes_list[current_node[3]]
            break

        # Make sure this is a graph search algorithm 
        if expand_node[0] in explored_states_set:
            continue
        explored_states_set.add(expand_node[0])
        successors = problem.getSuccessors(expand_node[0])
        for successor in successors:
            if successor[0] in explored_states_set:
                continue
            successor_gvalue = expand_node[4] + successor[2]
            successor_hvalue = heuristic(successor[0], problem)
            successor_node = tuple([successor[0], successor[1], len(nodes_list), expand_node[2], successor_gvalue])
            nodes_list.append(successor_node)
            frontier.push(successor_node, successor_gvalue + successor_hvalue)

    return actions_list[::-1]

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
