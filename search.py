# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions

    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def mySolverUCS(solver, visited):
    ds = util.PriorityQueue()
    ds.push(item=(solver.getStartState(), [], 0), priority=0)
    while not ds.isEmpty():
        currentPath, path, cost = ds.pop()
        if currentPath not in visited:
            visited.append(currentPath)
            if solver.isGoalState(currentPath):
                return path
            for i in solver.getSuccessors(currentPath):
                ds.push(
                    (i[0], path + [i[1]], cost + i[2]),
                    priority=solver.getCostOfActions(path + [i[1]]),
                )


def mySolverAstar(solver, visited, huerstic):
    ds = util.PriorityQueue()
    ds.push(
        item=(solver.getStartState(), [], 0),
        priority=huerstic(solver.getStartState(), solver),
    )
    while not ds.isEmpty():
        currentPath, path, cost = ds.pop()
        if currentPath not in visited:
            visited.append(currentPath)
            if solver.isGoalState(currentPath):
                return path
            for i in solver.getSuccessors(currentPath):
                ds.push(
                    (i[0], path + [i[1]], cost + i[2]),
                    priority=cost + i[2] + huerstic(i[0], solver),
                )


def mySolverb(currentNode, solver, visited):
    pathQueue = [[currentNode]]
    queue = util.Queue()
    queue.push([currentNode])
    visited.append(currentNode[0])
    while len(queue.list) > 0:
        currentPath = queue.pop()
        path = pathQueue.pop(0)
        if solver.isGoalState(currentPath[0][0]):
            return path
        else:
            for i in solver.getSuccessors(currentPath[0][0]):
                if i[0] not in visited:
                    visited.append(i[0])
                    queue.push([i])
                    pathQueue.append(path + [i])
                else:
                    pass


def mySolver(stack, currentNode, solver, visited):
    stack.push(currentNode)
    visited.push(currentNode[0])
    if solver.isGoalState(currentNode[0]):
        return True
    for i in solver.getSuccessors(currentNode[0]):
        if i[0] not in visited.list:
            if mySolver(stack, i, solver, visited):
                return True
            else:
                stack.pop()
    return False
    # stack.pop()


def getDirection(stackList):
    result = []
    for i in stackList:
        result.append(i[1])
    return result


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    stack = util.Stack()
    visited = util.Stack()
    mySolver(
        stack,
        [problem.getStartState(), "South", 1],
        problem,
        visited,
    )

    return getDirection(stack.list[1::])


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    value = mySolverb(
        [problem.getStartState(), "South", 1],
        problem,
        [],
    )
    return getDirection(value[1::])


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    return mySolverUCS(problem, [])


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    return mySolverAstar(problem, [], heuristic)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
