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

        # Define constants
        MIN_DIST = 5

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
            return len(nearestNode.path) # return the distance

        # Count the food
        food_positions = []
        for x in range(mapWidth):
            for y in range(mapHeight):
                if foodGrid[x][y]:
                    food_positions.append((x, y))

        # Create Module List
        module_list = []

        # Create Food List
        food_list = []
        for position in food_positions:
            food = Food(position)
            food_list.append(food)

        # Label the lists
        def classifyFood(module_list, food_list, module=Module(0)):
            for food in food_list:
                if food.getModule() == None:
                    # Update Module Cycle
                    module_list.append(module)

                    # Expand new module
                    module = Module(module.index + 1)
                    food.module = module.index
                    module.nodes.append(food)
                    module.edges.append(food)

                    # auto expand module in food_list
                    expand(module, food_list)
                    assert len(module.edges) == 0

                else:
                    # # Show Classification Process
                    # print("pass since already labeled: {}".format(food.getModule()))
                    # print("module #{0} has #{1} nodes #{2} edges".format(module.index, len(module.nodes), len(module.edges)))
                    # print("module_list now have {0} modules\n".format(len(module_list)))
                    pass

            # Abort the first module [Empty]
            module_list.pop(0)
            # Add the last module
            module_list.append(module)
            return None

        # Expand the module
        # @timed
        def expand(module, food_list):
            # print("START: {}".format(module.edges))
            # return situation
            if len(module.edges) == 0:
                return
            new_edges = []
            for food in module.edges:
                for i in food_list:
                    if i in module.nodes:
                        continue
                    if distanceToPosition(food.position, i.position) <= MIN_DIST:
                        i.module = module.index
                        module.nodes.append(i)
                        new_edges.append(i)
            module.edges = new_edges
            # print("END: {}\n".format(module.edges))
            return expand(module, food_list)

        classifyFood(module_list, food_list)

        # Test Explore Complete [covers full map]
        def testComplete():
            count = 0
            for module in module_list:
                count += len(module.nodes)
            if count == len(food_positions):
                print("Explore complete")
            else:
                print("Something wrong")
        # testComplete()

        # Test show modules
        def testModules():
            export_list = []
            for module in module_list:
                lst = []
                for food in module.nodes:
                    lst.append(food.position)
                export_list.append(lst)
            print(export_list)
        # testModules()

        # Test show food list
        def testFood():
            export_list = {}
            for food in food_list:
                export_list[food.position] = food.module
            print(export_list)
        # testFood()

        def findClosestFood(position):
            closed = set()
            fringe = util.PriorityQueue()
            myPosition = position
            initNode = Node(myPosition, [], 0.0)
            nearestNode = None
            fringe.push(initNode, 1)
            while True:
                if fringe.isEmpty():
                    sys.exit("Error calculating distance. myAgentP3:findClosestFood")

                node = fringe.pop()
                x, y = node.state
                # print("state: {}; path: {}; cost: {}; get?: {}".format(node.state, node.path, node.cost, foodGrid[x][y]))

                if foodGrid[x][y] == True:
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
            return nearestNode.state

        def labelMap():
            for x in range(mapWidth):
                for y in range(mapHeight):
                    if mapGrid[x][y] == False:
                        pos = findClosestFood((x, y))
                        labeled = False
                        for food in food_list:
                            if food.position == pos:
                                mapLabeled[x][y] = food.module
                                labeled = True
                                break
                        if labeled == False:
                            sys.exit("Error labeling map; myAgentP3:250")
        labelMap()

        # Test map labeling
        def testMapLabel():
            # Initialize
            export_list = []
            for i in range(len(module_list)):
                export_list.append([])
            # Distribute by module
            for x in range(mapWidth):
                for y in range(mapHeight):
                    if mapGrid[x][y] == False:
                        module = mapLabeled[x][y]
                        export_list[module-1].append([x, y])
            print(export_list)
        # testMapLabel()

        # Get Teammates Indices
        teammateIndices = [index for index in self.getTeam(gameState) if index != self.index]
        assert len(teammateIndices) == 1
        teammateIndex = teammateIndices[0]

        # Get Ghosts Indices
        ghostIndices = gameState.getGhostTeamIndices()

        # API Links
        self.foodGrid = foodGrid
        self.mapGrid = mapGrid
        self.distanceCalculator = distanceToPosition
        self.module_list = module_list
        self.food_list = food_list
        self.mapLabeled = mapLabeled
        self.teammateIndex = teammateIndex
        self.ghostIndices = ghostIndices
        self.directions = directions



    def chooseAction(self, gameState):
        """
        Picks among actions randomly.
        """
        teammateActions = self.receivedBroadcast
        # Process your teammate's broadcast!
        # Use it to pick a better action for yourself

        # Get legal future actions
        actions = gameState.getLegalActions(self.index)
        filteredActions = actionsWithoutReverse(actionsWithoutStop(actions), gameState, self.index)

        # Randomly choose action
        currentAction = random.choice(actions) # Change this!

        # Get food map
        mapGrid = self.mapGrid
        directions = self.directions
        foodGrid = gameState.getFood()

        # Get agent positions
        myPosition = gameState.getAgentPosition(self.index)
        teammatePosition = gameState.getAgentPosition(self.teammateIndex)
        ghostPositions = []
        for i in range(len(self.ghostIndices)):
            ghostPositions.append(gameState.getAgentPosition(self.ghostIndices[i]))

        # Get teammate's predicted positions
        teammatePositions = getFuturePositions(gameState, teammateActions, self.teammateIndex)

        # Consider teammate's positions
        teammateToGhosts = []
        for i in range(len(ghostPositions)):
            teammateToGhosts.append(self.distanceCalculator(teammatePosition, ghostPositions[i]))
        teammateToClosestGhost = min(teammateToGhosts)

        validTMPositions = teammatePositions[:teammateToClosestGhost]

        for position in validTMPositions:
            module = self.mapLabeled[position[0]][position[1]]
            for food in self.module_list[module-1].nodes:
                if food.position == position:
                    self.module_list[module-1].nodes.remove(food)
                    self.foodGrid[position[0]][position[1]] = False

        # # Get APIs
        # teammateIndex = self.teammateIndex
        # mapGrid = self.mapGrid
        # mapLabeled = self.mapLabeled
        # module_list = self.module_list
        # food_list = self.food_list
        # distanceToPosition = self.distanceCalculator

        # Get current module
        module = self.mapLabeled[myPosition[0]][myPosition[1]]
        assert not module == False # Not wall

        # Label walked point on mapLabeled
        # self.mapLabeled[myPosition[0]][myPosition[1]] = None

        # # TEST PRINT
        # print "MODULE #{}".format(module)
        # print myPosition
        # lst = []
        # for food in self.module_list[module-1].nodes:
        #     lst.append(food.position)
        # print lst

        # If caught food, remove it from module_list
        if self.foodGrid[myPosition[0]][myPosition[1]] or self.foodGrid[teammatePosition[0]][teammatePosition[1]]:
            for food in self.module_list[module-1].nodes:
                removed = False
                if food.position == myPosition:
                    self.module_list[module-1].nodes.remove(food)
                    removed = True
                    break
            # if removed == False:
            #     sys.exit("Error deleting food; myAgentP3:351")
            self.foodGrid[myPosition[0]][myPosition[1]] = False
            self.foodGrid[teammatePosition[0]][teammatePosition[1]] = False

        # Find closest food
        def findClosestFood(position):
            closed = set()
            fringe = util.PriorityQueue()
            myPosition = position
            initNode = Node(myPosition, [], 0.0)
            nearestNode = None
            fringe.push(initNode, 1)
            while True:
                if fringe.isEmpty():
                    sys.exit("Error calculating distance. myAgentP3:findClosestFood")

                node = fringe.pop()
                x, y = node.state
                # print("state: {}; path: {}; cost: {}; get?: {}".format(node.state, node.path, node.cost, foodGrid[x][y]))

                if self.foodGrid[x][y] == True:
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

                        if self.mapGrid[next_x][next_y] == False and child_state not in closed:
                            fringe.push(childNode, childNode.cost)
            return nearestNode

        # Explore next module
        next_module = None
        next_food = None
        if len(self.module_list[module-1].nodes) <= 0:
            next_food = findClosestFood(myPosition)
            next_module = self.mapLabeled[next_food.state[0]][next_food.state[1]]
        else:
            next_module = module
        assert not next_module == None
        print "NEXT MODULE #{}\n".format(next_module)

        # Find closest same module
        def findClosestModuleFood(position, module):
            closed = set()
            fringe = util.PriorityQueue()
            myPosition = position
            initNode = Node(myPosition, [], 0.0)
            nearestNode = None
            fringe.push(initNode, 1)
            while True:
                if fringe.isEmpty():
                    sys.exit("Error calculating distance. myAgentP3:findClosestModuleFood")

                node = fringe.pop()
                x, y = node.state
                # print("state: {}; path: {}; cost: {}; get?: {}".format(node.state, node.path, node.cost, foodGrid[x][y]))

                if self.mapLabeled[x][y] == module:
                    for food in self.module_list[module-1].nodes:
                        if food.position == (x, y):
                            nearestNode = node
                            return nearestNode

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

                        if self.mapGrid[next_x][next_y] == False and child_state not in closed:
                            fringe.push(childNode, childNode.cost)
            return nearestNode

        # Determine next action
        if next_module == module:
            return findClosestModuleFood(myPosition, next_module).path[0]
        else:
            assert not next_food == None
            return next_food.path[0]

        # Summarize future actions
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
