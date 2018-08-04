# myAgentP2.py
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


class myAgentP2(CaptureAgent):
    """
    Students' Names: Shixuan Wayne Li
    Phase Number: 2
    Description of Bot:
        a) First split the screen into left & right, and detect the position of the Pacman
        b) Let Pacman to finish searching every dot on the left side, then move on to the right sideself.
           Note that leftSide is empty when there is less than 2 food on the left side and each food has
           distance <= 5 from the pacman
        c) The searching algorithm is UCS. Cost for every step is 1
        d) We also consider the situation when there are only few food left (count <= 5). Then we filter
           out the ones with on neighboring foods (radius = 5; max amount = 2) from the map.
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

        otherAgentActions = self.receivedInitialBroadcast
        teammateIndices = [index for index in self.getTeam(gameState) if index != self.index]
        assert len(teammateIndices) == 1
        teammateIndex = teammateIndices[0]
        otherAgentPositions = getFuturePositions(gameState, otherAgentActions, teammateIndex)

        # Screen features
        wallGrid = gameState.getWalls()
        foodGrid = gameState.getFood()
        mapGrid = wallGrid.copy()
        mapWidth = mapGrid.width
        mapHeight = mapGrid.height

        # Count the food
        originFoodList = []
        for x in range(mapWidth):
            for y in range(mapHeight):
                if foodGrid[x][y]:
                    originFoodList.append((x, y))

        # You can process the broadcast here!
        self.originFoodList = originFoodList
        self.otherAgentActions = otherAgentActions
        self.otherAgentPositions = otherAgentPositions

        # KMeans
        teammateEats = otherAgentPositions[:len(originFoodList) * 2]
        for food in originFoodList:
            if food in teammateEats:
                originFoodList.remove(food)

        # Get best K - Elbow Analysis
        k_attemps = range(1, 10)
        errors = []
        for k in k_attemps:
            k_m = KMeans(k)
            k_m.fit(originFoodList)
            error = 0
            for m in range(len(k_m.classes)):
                points = k_m.classes[m]
                centroid = k_m.centroids[m]
                for point in points:
                    error += k_m.euclidean(point, centroid)
            errors.append(error)

        # Elbow Analysis (0.1)
        bestK = 0
        for k in range(len(errors) - 1):
            if (errors[k] - errors[k + 1]) < errors[k] * 0.06:
                bestK = k
                break

        km = KMeans(bestK)
        km.fit(originFoodList)

        # Gather clusters
        clusters = []
        for i in range(len(km.classes)):
            clusters.append(km.classes[i])

        centroids = []

        for i in range(len(km.centroids)):
            centroids.append([km.centroids[i], clusters[i], i])

        self.centroids = centroids


    def chooseAction(self, gameState):
        """
        Picks among actions randomly.
        """
        actions = gameState.getLegalActions(self.index)

        # Teammate Positions
        # teammateActions = self.otherAgentActions
        teammatePositions = self.otherAgentPositions
        # print(len(teammateActions))
        # print(len(teammatePositions))
        # print(gameState.data.time)

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

        foodCount = 0
        for x in range(mapWidth):
            for y in range(mapHeight):
                if foodGrid[x][y]:
                    foodCount += 1


        # Get current time
        currTime = gameState.data.time

        def manhattanDistance(x, y ):
            return abs( x[0] - y[0] ) + abs( x[1] - y[1] )

        myPosition = gameState.getAgentPosition(self.index)

        for i in range(len(self.centroids)):
            for j in range(len(self.centroids[i][1])):
                print(len(self.centroids[i][1]))
                if self.centroids[i][1][j] == myPosition:
                    self.centroids[i][1].pop(j)
                    break

        centroids = [centroid for centroid in self.centroids]
        centroids.sort(key=lambda x: manhattanDistance(myPosition, x[0]))

        curr_cluster = None
        for i in range(len(centroids)):
            cluster = centroids[i][1]
            if len(cluster) > 0:
                curr_cluster = cluster

        for x in range(mapWidth):
            for y in range(mapHeight):
                foodGrid[x][y] = False

        for point in curr_cluster:
            x, y = point
            foodGrid[x][y] = True

        # print("foodCount: {}".format(foodCount))
        # print("curr_cluster: {}".format(len(curr_cluster)))

        def fewFoodLeft():
            count = 0
            foodList = []
            for x in range(0, mapWidth):
                for y in range(0, mapHeight):
                    if foodGrid[x][y]:
                        count += 1
                        foodList.append([x, y])
                    if count > 5:
                        return False, foodList
            if count <= 5:
                return True, foodList
            return False, foodList

        if foodCount <= 5:
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
                # return Directions.STOP
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

class Node:
    def __init__(self, state, path, cost):
        self.state = state
        self.path = path
        self.cost = cost

class KMeans:
    def __init__(self, k=3, tolerance=0.0001, max_iterations=500):
        self.k = k
        self.tolerance = tolerance
        self.max_iterations = max_iterations

    def euclidean(self, q, p):
        sumNum = 0
        for i in range(len(q)):
            sumNum += (q[i] - p[i]) ** 2
        return sumNum ** 0.5

    def fit(self, dataset):
        self.centroids = {}

        #initialize the centroids, the first 'k' elements in the dataset will be our initial centroids
        for i in range(self.k):
            self.centroids[i] = dataset[i]

        #begin iterations
        for i in range(self.max_iterations):
            self.classes = {}
            for i in range(self.k):
                self.classes[i] = []

            #find the distance between the point and cluster; choose the nearest centroid
            for data in dataset:
                distances = []
                # distances = [np.linalg.norm(data - self.centroids[centroid]) for centroid in self.centroids]
                for centroid in self.centroids:
                    distance = self.euclidean(data, self.centroids[centroid])
                    distances.append(distance)
                classification = distances.index(min(distances))
                self.classes[classification].append(data)

            previous = dict(self.centroids)

            #average the cluster datapoints to re-calculate the centroids
            for classification in self.classes:
                datapile = self.classes[classification]
                numlen = len(datapile)
                if numlen > 0:
                    xmean = sum(data[0] for data in datapile) / float(numlen)
                    ymean = sum(data[1] for data in datapile) / float(numlen)
                    self.centroids[classification] = [xmean, ymean]

            isOptimal = True

            for centroid in self.centroids:
                prev_centroid = previous[centroid]
                curr_centroid = self.centroids[centroid]

                difference = (curr_centroid[0] - prev_centroid[0]) / prev_centroid[0] * 100 + (curr_centroid[1] - prev_centroid[1]) / prev_centroid[1] * 100
                if difference > self.tolerance:
                    isOptimal = False

            if isOptimal:
                break

