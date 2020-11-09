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
from util import PriorityQueue
import heapq

class Wrapper:
    """
    Wrapper class for util.Stack and util.Queue, allowing all data structures to have the same push method
    """
    def __init__(self, frontier):
        self.frontier = frontier
        self.list = frontier.list

    def push(self, item, priority):
        self.frontier.push(item)

    def pop(self):
        return self.frontier.pop()

    def isEmpty(self):
        return self.frontier.isEmpty()

    def update(self, item, priority):
        pass

class QueueWrapper(PriorityQueue):
    """
    Wrapper class for PriorityQueue to overload the update method as now item is the tuple (state, steps) and not 'state'
    """
    def __init__(self, frontier):
        self.frontier = frontier
        PriorityQueue.__init__(self)        # super-class initializer

    def update(self, item, priority):
        # Overloading PriorityQueue update() function
        for index, (p, c, i) in enumerate(self.heap):
            if i[0] == item[0]:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)

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
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """

    #initialize stack (frontier)
    frontier = Wrapper(util.Stack())
    return graphSearch(problem, frontier)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    #initialize frontier with start set
    frontier = Wrapper(util.Queue())
    return graphSearch(problem, frontier)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    frontier = QueueWrapper(util.PriorityQueue())
    return graphSearch(problem, frontier)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    frontier = QueueWrapper(util.PriorityQueueWithFunction(heuristic))
    return graphSearch(problem, frontier, heuristic)
    #util.raiseNotDefined()

def graphSearch(problem, frontier, heuristic=nullHeuristic):
    startState = problem.getStartState()
    steps = list('')
    frontier.push((startState,steps), 0 + heuristic(startState, problem))
    explored = set()

    if problem.isGoalState(startState): return []

    visited = {startState: 0 + heuristic(startState, problem)}

    while not frontier.isEmpty():
        state, steps = frontier.pop()
        #print(f'state is {state}')
        if problem.isGoalState(state):
            return steps
        explored.add(state)
        for successor, action, cost in problem.getSuccessors(state):
            pathCost = (problem.getCostOfActions((steps + [action])) + heuristic(successor, problem))
        #    print(f'{successor} heuristic is ', heuristic(successor, problem))
            if visited.get(successor, 0) > pathCost:
#                print(f'\n{successor} in visited with pathcost\n', visited.get(successor, 0), visited)
                frontier.update((successor, (steps + [action])), pathCost)
                visited[successor] = pathCost
#                print('\nupdated visited\n', visited, f'pathcost is {pathCost}')
            if successor not in explored and successor not in visited:
                frontier.push((successor, (steps + [action])), pathCost)
                visited[successor] = pathCost



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
