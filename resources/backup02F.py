# myAgentP3.py
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
# This file was based on the starter code for student bots, and refined
# by Mesut (Xiaocheng) Yang


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game
from util import nearestPoint
# Added by Wayne
import sys
import time
from functools import wraps

#########
# Agent #
#########
class myAgentP3(CaptureAgent):
    """
    Unfortunately, although I tried many cool ways, the "stupid" way works the best.
    My basic idea is to make clusters for the food and then let the bot to focus on one cluseter
    at the time while searching. The final solution is quite similar to Phase I. I put most time on
    looking for ways how to let the bot be smart enough avoiding the ghost.

    The cooperation is comparatively easy. The machanism is that we select some actions the teammate broadcast, and
    use the corresponding positions he will pass. The selection is based on the least between the
    teammate and its closet ghost.

    The avoidance of ghost is activated only when the bot is close (<=3) to a ghost. The bot will basically
    just avoid the steps that will crash into a ghost by finding what other dots he may can search for. Then,
    if there are no other ways, we will implement the risk that to crash into the ghost on purpose, and during the
    way, try to find a way to escape.
    """

    def registerInitialState(self, gameState):
        """
        This method handles the initial setup of the
        agent to populate useful fields (such as what team
        we're on).

        A distanceCalculator instance caches the maze distances
        between each pair of positions, so your agents can use:
        self.distancer.getDistance(p1, p2)

        IMPORTANT: This method may run for at most 15 seconds.
        """

        # Make sure you do not delete the following line.
        # If you would like to use Manhattan distances instead
        # of maze distances in order to save on initialization
        # time, please take a look at:
        # CaptureAgent.registerInitialState in captureAgents.py.
        CaptureAgent.registerInitialState(self, gameState)
        self.start = gameState.getAgentPosition(self.index)

        # Get Map Attributes
        wallGrid = gameState.getWalls()
        foodGrid = gameState.getFood()
        mapGrid = wallGrid.copy()
        mapLabeled = wallGrid.copy()
        mapWidth = mapGrid.width
        mapHeight = mapGrid.height
        directions = { Directions.NORTH: (0, 1),
                       Directions.SOUTH: (0, -1),
                       Directions.EAST:  (1, 0),
                       Directions.WEST:  (-1, 0)}

        # Function for distance calculation [BFS]
        def distanceToPosition(start, position):
            closed = set()
            fringe = util.PriorityQueue()
            myPosition = start
            initNode = Node(myPosition, [], 0.0)
            nearestNode = None
            fringe.push(initNode, 1)
            while True:
                if fringe.isEmpty():
                    sys.exit("Error calculating distance. myAgentP3:registerInitialState:distanceToPosition")

                node = fringe.pop()
                x, y = node.state
                # print("state: {}; path: {}; cost: {}; get?: {}".format(node.state, node.path, node.cost, foodGrid[x][y]))

                if x == position[0] and y == position[1]:
                    nearestNode = node
                    break

                if node.state not in closed:
                    closed.add(node.state)
                    for direction in directions.keys():
                        step = directions[direction]
                        next_x = x + step[0]
                        next_y = y + step[1]
                        child_state = (next_x, next_y)
                        child_path = node.path + [direction]
                        child_cost = node.cost + 1
                        childNode = Node(child_state, child_path, child_cost)

                        if mapGrid[next_x][next_y] == False and child_state not in closed:
                            fringe.push(childNode, childNode.cost)
            return nearestNode # return the distance

        # Get Teammates Indices
        teammateIndices = [index for index in self.getTeam(gameState) if index != self.index]
        assert len(teammateIndices) == 1
        teammateIndex = teammateIndices[0]

        # Get Ghosts Indices
        ghostIndices = gameState.getGhostTeamIndices()

        # API Links
        self.teammateIndex = teammateIndex
        self.ghostIndices = ghostIndices
        self.distanceCalculator = distanceToPosition



    def chooseAction(self, gameState):
        """
        Picks among actions randomly.
        """
        teammateActions = self.receivedBroadcast
        # Process your teammate's broadcast!
        # Use it to pick a better action for yourself

        # Get legal future actions
        actions = gameState.getLegalActions(self.index)
        filteredActions = actionsWithoutStop(actions)
        filteredNonReActions = actionsWithoutReverse(actionsWithoutStop(actions), gameState, self.index)

        # Randomly choose action
        currentAction = random.choice(actions) # Change this!

        # INSERT YOUR LOGIC HERE
        wallGrid = gameState.getWalls()
        foodGrid = gameState.getFood()
        mapGrid = wallGrid.copy()
        directions = { Directions.NORTH: (0, 1),
                       Directions.SOUTH: (0, -1),
                       Directions.EAST:  (1, 0),
                       Directions.WEST:  (-1, 0)}

        # Slip the map into three parts
        mapWidth = mapGrid.width
        mapHeight = mapGrid.height

        midWidth = mapWidth / 2
        midHeight = mapHeight / 2

        def fewFoodLeft():
            count = 0
            foodList = []
            for x in range(0, mapWidth):
                for y in range(0, mapHeight):
                    if foodGrid[x][y]:
                        count += 1
                        foodList.append((x, y))
                    if count > 5:
                        return False, foodList
            if count <= 5:
                return True, foodList
            return False, foodList

        # Get agent positions
        myPosition = gameState.getAgentPosition(self.index)
        teammatePosition = gameState.getAgentPosition(self.teammateIndex)
        ghostPositions = []
        for i in range(len(self.ghostIndices)):
            ghostPositions.append(gameState.getAgentPosition(self.ghostIndices[i]))

        # Get teammate's predicted positions
        teammatePositions = getFuturePositions(gameState, teammateActions, self.teammateIndex)

        # Consider teammate's positions
        if len(ghostPositions) > 0:
            teammateToGhosts = []
            for i in range(len(ghostPositions)):
                node = self.distanceCalculator(teammatePosition, ghostPositions[i])
                distance = len(node.path)
                teammateToGhosts.append(distance)
            teammateToClosestGhost = min(teammateToGhosts)

            # Cooperation
            if not teammatePositions == None:
                validTMPositions = teammatePositions[:teammateToClosestGhost]

                for position in validTMPositions:
                    x, y = position
                    if foodGrid[x][y]:
                        foodGrid[x][y] = False
        # Situation when there's no ghost
        else:
            result, foodList = fewFoodLeft()
            if result:
                for food in foodList:
                    if self.distanceCalculator(food, teammatePosition) <= 10:
                        x, y = food
                        foodGrid[x][y] = False
            else:
                for position in teammatePositions:
                    x, y = position
                    if foodGrid[x][y]:
                        foodGrid[x][y] = False


        def distanceToPosition(position):
            closed = set()
            fringe = util.PriorityQueue()
            myPosition = gameState.getAgentPosition(self.index)
            initNode = Node(myPosition, [], 0.0)
            nearestNode = None
            fringe.push(initNode, 1)
            while True:
                if fringe.isEmpty():
                    sys.exit("Error finding next action. myAgentP1:102")

                node = fringe.pop()
                x, y = node.state
                # print("state: {}; path: {}; cost: {}; get?: {}".format(node.state, node.path, node.cost, foodGrid[x][y]))

                if x == position[0] and y == position[1]:
                    nearestNode = node
                    break

                if node.state not in closed:
                    closed.add(node.state)
                    for direction in directions.keys():
                        step = directions[direction]
                        next_x = x + step[0]
                        next_y = y + step[1]
                        child_state = (next_x, next_y)
                        child_path = node.path + [direction]
                        child_cost = node.cost + 1
                        childNode = Node(child_state, child_path, child_cost)

                        if mapGrid[next_x][next_y] == False and child_state not in closed:
                            fringe.push(childNode, childNode.cost)
            return len(nearestNode.path)

        def leftEmpty():
            # count = 0
            foodList = []
            for x in range(0, midWidth):
                for y in range(0, mapHeight):
                    if foodGrid[x][y]:
                        # return False
                        # count += 1
                        foodList.append((x, y))
                    # if count > 2:
                    if len(foodList) > 2:
                        return False
            if len(foodList) == 0:
                return True
            for food in foodList:
                if distanceToPosition(food) <= 10:
                    return False
            return True

        def pacmanOnLeft():
            x, y = gameState.getAgentPosition(self.index)
            if x <= midWidth:
                return True
            return False

        if not leftEmpty():
            for x in range(midWidth + 1, mapWidth):
                for y in range(0, mapHeight):
                    foodGrid[x][y] = False
            if pacmanOnLeft():
                for y in range(0, mapHeight):
                    mapGrid[midWidth + 2][y] = True

        if leftEmpty():
            if pacmanOnLeft():
                pass
            else:
                # if
                for y in range(0, mapHeight):
                    mapGrid[midWidth - 2][y] = True

        # Use UCS to find closest path
        def isDeadCornor(x, y):
            if foodGrid[x][y]:
                return False
            wallsCount = 0
            for direction in directions.values():
                next_x = x + direction[0]
                next_y = y + direction[1]
                if foodGrid[x][y]:
                    return False
                if mapGrid[next_x][next_y] == True:
                    wallsCount += 1
            if wallsCount >= 3:
                return True
            return False

        # # Explore dead corner in one direction
        # def exploreDeadCorner(position, direction, path=[]):
        #     x, y = position
        #     if not x in range(mapWidth) or not y in range(mapHeight):
        #         return False, path
        #     if foodGrid[x][y]:
        #         return False, path
        #     wallsCount = 0
        #     for dirc in directions.values():
        #         next_x = x + dirc[0]
        #         next_y = y + dirc[1]
        #         if not next_x in range(mapWidth) or not next_y in range(mapHeight):
        #             continue
        #         if mapGrid[next_x][next_y] == True:
        #             wallsCount += 1
        #     if wallsCount >= 3:
        #         return True, path
        #     if wallsCount >= 2:
        #         path.append(direction)
        #         next_position = (x + direction[0], y + direction[1])
        #         return exploreDeadCorner(next_position, direction, path)
        #     return False, path
        #
        # # Broad meaning dead corner
        # # Only consider direction dead place, no further grid allowed
        # def broadDeadCorner(position):
        #     x, y = position
        #     wallsCount = 0
        #     pathways = []
        #     for direction in directions.values():
        #         next_x = x + direction[0]
        #         next_y = y + direction[1]
        #         if mapGrid[next_x][next_y] == True:
        #             wallsCount += 1
        #         else:
        #             pathways.append(direction)
        #     if wallsCount >= 2:
        #         if wallsCount >= 3:
        #             return []
        #         for direction in pathways:
        #             result, path = exploreDeadCorner((x, y), direction)
        #             if result == True:
        #                 return path
        #
        #     return False


        # See if from start -> end is going to dead corner
        def goToDeadCorner(start, end):
            return False
            # resultStart = broadDeadCorner(start)
            # resultEnd = broadDeadCorner(end)
            #
            # if resultEnd == False:
            #     return False
            # else:
            #     if len(resultEnd) == 0:
            #         return True
            #     pathEnd = resultEnd
            #     if resultStart == False:
            #         return True
            #     else:
            #         if len(resultStart) == 0:
            #             return False
            #         pathStart = resultStart
            #         if len(pathEnd) > len(pathStart):
            #             return False
            #         else:
            #             return True


        # Ghost Avoidance
        toward_ghost = None
        myPosition = gameState.getAgentPosition(self.index)
        for position in ghostPositions:
            node = self.distanceCalculator(myPosition, position)
            if len(node.path) <= 2:
                toward_ghost = node.path[0]
                if toward_ghost in filteredActions:
                    filteredActions.remove(toward_ghost)
                    if len(filteredActions) == 0:
                        return toward_ghost
                    if len(filteredActions) == 1:
                        return filteredActions[0]
                if len(filteredNonReActions) == 1:
                    return filteredNonReActions[0]


        can_broadcast = False

        def findWay(foodGrid):
            closed = set()
            fringe = util.PriorityQueue()
            myPosition = gameState.getAgentPosition(self.index)
            initNode = Node(myPosition, [], 0.0)

            nearestNode = None
            fringe.push(initNode, 1)

            initStep = True
            while True:
                if fringe.isEmpty():
                    nearestNode = None
                    break

                node = fringe.pop()
                x, y = node.state
                # print("state: {}; path: {}; cost: {}; get?: {}".format(node.state, node.path, node.cost, foodGrid[x][y]))

                if foodGrid[x][y]:
                    pass_notion = False
                    if not toward_ghost == None:
                        if len(node.path) > 0:
                            if node.path[0] == toward_ghost:
                                pass_notion = True
                    if not pass_notion:
                        nearestNode = node
                        break


                if node.state not in closed:
                    closed.add(node.state)
                    for direction in directions.keys():
                        step = directions[direction]
                        next_x = x + step[0]
                        next_y = y + step[1]
                        child_state = (next_x, next_y)
                        child_path = node.path + [direction]
                        child_cost = node.cost + 1
                        childNode = Node(child_state, child_path, child_cost)

                        if mapGrid[next_x][next_y] == False and not isDeadCornor(next_x, next_y) and child_state not in closed and not goToDeadCorner((x, y), (next_x, next_y)):
                            fringe.push(childNode, childNode.cost)
            return nearestNode

        nearestNode = findWay(foodGrid)
        if not nearestNode == None:
            path = nearestNode.path
            # print(path)
            currentAction = path[0]
            can_broadcast = True
        else:
            print("Error finding next action. Now to Plan-B")
            foodGrid = gameState.getFood()
            nearestNode = findWay(foodGrid)
            if not nearestNode == None:
                path = nearestNode.path
                # print(path)
                currentAction = path[0]
                can_broadcast = True
            else:
                print("Error finding next action. Now to Plan-C")
                if not toward_ghost == None:
                    if toward_ghost in filteredActions:
                        currentAction = random.choice(filteredActions)
                    else:
                        currentAction = random.choice(actions)
                else:
                    currentAction = random.choice(actions)

        # Summarize future actions
        if can_broadcast:
            nearestNode.path.pop(0)
            futureActions = nearestNode.path
        else:
            futureActions = None
        self.toBroadcast = futureActions

        return currentAction

def actionsWithoutStop(legalActions):
    """
    Filters actions by removing the STOP action
    """
    legalActions = list(legalActions)
    if Directions.STOP in legalActions:
        legalActions.remove(Directions.STOP)
    return legalActions

def actionsWithoutReverse(legalActions, gameState, agentIndex):
    """
    Filters actions by removing REVERSE, i.e. the opposite action to the previous one
    """
    legalActions = list(legalActions)
    reverse = Directions.REVERSE[gameState.getAgentState(agentIndex).configuration.direction]
    if len (legalActions) > 1 and reverse in legalActions:
        legalActions.remove(reverse)
    return legalActions

def getFuturePositions(gameState, plannedActions, agentIndex):
    """
    Returns list of future positions given by a list of actions for a
    specific agent starting form gameState

    NOTE: this does not take into account other agent's movements
    (such as ghosts) that might impact the *actual* positions visited
    by such agent
    """
    if plannedActions is None:
        return None

    planPositions = [gameState.getAgentPosition(agentIndex)]
    for action in plannedActions:
        if action in gameState.getLegalActions(agentIndex):
            gameState = gameState.generateSuccessor(agentIndex, action)
            planPositions.append(gameState.getAgentPosition(agentIndex))
        else:
            print("Action list contained illegal actions")
            break
    return planPositions

class Food:
    def __init__(self, position):
        self.position = position
        self.module = None

    def getPosition(self):
        return self.position

    def getModule(self):
        return self.module


class Module:
    def __init__(self, index):
        self.index = index
        self.nodes = []
        self.edges = []

    def getNodes(self):
        return self.nodes

    def getEdges(self):
        return self.edges

class Node:
    def __init__(self, state, path, cost):
        self.state = state
        self.path = path
        self.cost = cost

# Decorators
def timed(func):
    @wraps(func)
    def timeIt(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        time_spent = "%.2f" % (end_time - start_time)
        print("@TIMEIT: function #{0} takes time #{1}secs".format(func.__name__, time_spent))
    return timeIt
