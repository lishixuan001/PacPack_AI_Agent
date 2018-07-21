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

#########
# Agent #
#########
class myAgentP3(CaptureAgent):
    """
    YOUR DESCRIPTION HERE
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

    # def chooseAction(self, gameState):
    #     """
    #     Picks among actions randomly.
    #     """
    #     teammateActions = self.receivedBroadcast
    #     # Process your teammate's broadcast!
    #     # Use it to pick a better action for yourself
    #
    #     actions = gameState.getLegalActions(self.index)
    #
    #     filteredActions = actionsWithoutReverse(actionsWithoutStop(actions), gameState, self.index)
    #
    #     currentAction = random.choice(actions) # Change this!
    #     futureActions = None
    #
    #     self.toBroadcast = futureActions
    #     return currentAction

    def chooseAction(self, gameState):
        """
        Picks among the actions with the highest Q(s,a).
        """
        actions = gameState.getLegalActions(self.index)
        action = None

        # You can profile your evaluation time by uncommenting these lines
        # start = time.time()
        # values = [self.evaluate(gameState, a) for a in actions]
        # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)
        # INSERT YOUR LOGIC HERE
        wallGrid = gameState.getWalls()
        foodGrid = gameState.getFood()
        mapGrid = wallGrid.copy()
        directions = {Directions.NORTH: (0, 1),
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
                        foodList.append([x, y])
            if count <= 5:
                return True, foodList
            return False, foodList

        judge, foodList = fewFoodLeft()
        if judge:
            foodNotConsidered = 0
            for position in foodList:
                foodNearbyCount = 0
                x, y = position
                for m in range(x - 4, x + 4):
                    for n in range(y - 4, y + 4):
                        if m <= 0 or n <= 0:
                            continue
                        if m >= mapWidth or n >= mapHeight:
                            continue
                        if foodGrid[m][n]:
                            foodNearbyCount += 1
                if foodNearbyCount == 0:
                    if foodNotConsidered >= 2:
                        break
                    foodNotConsidered += 1
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
                    if gameState.hasFood(x, y):
                        # return False
                        # count += 1
                        foodList.append((x, y))
                    # if count > 2:
                    if len(foodList) > 2:
                        return False
            if len(foodList) == 0:
                return True
            for food in foodList:
                if distanceToPosition(food) <= 5:
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
            if gameState.hasFood(x, y):
                return False
            wallsCount = 0
            for direction in directions.values():
                next_x = x + direction[0]
                next_y = y + direction[1]
                if gameState.hasFood(next_x, next_y):
                    return False
                if mapGrid[next_x][next_y] == True:
                    wallsCount += 1
            if wallsCount >= 3:
                return True
            return False

        closed = set()
        fringe = util.PriorityQueue()

        myPosition = gameState.getAgentPosition(self.index)
        initNode = Node(myPosition, [], 0.0)

        nearestNode = None
        fringe.push(initNode, 1)

        initStep = True
        while True:
            if fringe.isEmpty():
                sys.exit("Error finding next action. myAgentP1:102")

            node = fringe.pop()
            x, y = node.state
            # print("state: {}; path: {}; cost: {}; get?: {}".format(node.state, node.path, node.cost, foodGrid[x][y]))

            if foodGrid[x][y]:
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

                    if mapGrid[next_x][next_y] == False and not isDeadCornor(next_x, next_y) and child_state not in closed:
                        fringe.push(childNode, childNode.cost)

        if nearestNode != None:
            path = nearestNode.path
            # print(path)
            return path[0]
        else:
            sys.exit("Error finding next action. myAgentP1:132")

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

class Node:
    def __init__(self, state, path, cost):
        self.state = state
        self.path = path
        self.cost = cost
