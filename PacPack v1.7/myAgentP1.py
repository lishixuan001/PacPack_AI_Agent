# myAgentP1.py
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
from game import Actions
import game
from util import nearestPoint
import sys

#########
# Agent #
#########


class myAgentP1(CaptureAgent):
    """
    Students' Names: Shixuan Wayne Li
    Phase Number: 1
    Description of Bot:
        a) First split the screen into left & right, and detect the position of the Pacman
        b) Let Pacman to finish searching every dot on the left side, then move on to the right side
        c) The searching algorithm is UCS. Cost for every step is 1
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


        # def foodDensityList():
        #     foodList = []
        #     for x in range(0, mapWidth):
        #         for y in range(0, mapHeight):
        #             if foodGrid[x][y]:
        #                 count = 0
        #                 for m in range(x - 4, x + 4):
        #                     for n in range(y - 4, y + 4):
        #                         if m <= 0 or n <= 0:
        #                             continue
        #                         if m >= mapWidth or n >= mapHeight:
        #                             continue
        #                         if foodGrid[m][n]:
        #                             count += 1
        #                 foodList.append([(x, y), count])
        #     return foodList

        # foodDensities = foodDensityList()
        # if len(foodDensities) == 0:
        #     sys.exit("No Food Detected; myAgentP1:138")
        # elif len(foodDensities) <= 2:
        #     for food in foodDensities:
        #         x, y = food[0][0], food[0][1]
        #         foodGrid[x][y] = False
        # else:
        #     for food in foodDensities[:2]:
        #         x, y = food[0][0], food[0][1]
        #         foodGrid[x][y] = False

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


    def evaluate(self, gameState, action):
        """
        Computes a linear combination of features and feature weights
        """
        features = self.getFeatures(gameState, action)
        weights = self.getWeights(gameState, action)
        return features * weights

    def getFeatures(self, gameState, action):
        features = util.Counter()

        ### Useful information you can extract from a GameState (pacman.py) ###
        successorGameState = gameState.generateSuccessor(self.index, action)
        newPos = successorGameState.getAgentPosition(self.index)
        oldFood = gameState.getFood()
        newFood = successorGameState.getFood()
        ghostIndices = self.getOpponents(successorGameState)

        # Determines how many times the agent has already been in the newPosition in the last 20 moves
        numRepeats = sum([1 for x in self.observationHistory[-20:] if x.getAgentPosition(self.index) == newPos])

        foodPositions = oldFood.asList()
        foodDistances = [self.getMazeDistance(newPos, foodPosition) for foodPosition in foodPositions]
        closestFood = min( foodDistances ) + 1.0

        ghostPositions = [successorGameState.getAgentPosition(ghostIndex) for ghostIndex in ghostIndices]
        ghostDistances = [self.getMazeDistance(newPos, ghostPosition) for ghostPosition in ghostPositions]
        ghostDistances.append( 1000 )
        closestGhost = min( ghostDistances ) + 1.0

        teammateIndices = [index for index in self.getTeam(gameState) if index != self.index]
        assert len(teammateIndices) == 1, "Teammate indices: {}".format(self.getTeam(gameState))
        teammateIndex = teammateIndices[0]
        teammatePos = successorGameState.getAgentPosition(teammateIndex)
        teammateDistance = self.getMazeDistance(newPos, teammatePos) + 1.0

        pacmanDeath = successorGameState.data.num_deaths

        features['successorScore'] = self.getScore(successorGameState)

        # CHANGE YOUR FEATURES HERE

        return features

    def getWeights(self, gameState, action):
        # CHANGE YOUR WEIGHTS HERE
        return {'successorScore': 100}

class Node:
    def __init__(self, state, path, cost):
        self.state = state
        self.path = path
        self.cost = cost








































# END File
