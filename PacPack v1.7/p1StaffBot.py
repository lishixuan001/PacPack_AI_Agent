# p1StaffBot.py
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
# This file was based on the starter code for student bots, and refined by Mesut (Xiaocheng) Yang


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game
from util import nearestPoint

#################
# Agent #
#################

# The seed for randomly choosing food to persure. 
# This will be different during test time, please try to generalize
# Restore this to 10 when running preliminary autograder for phase 1
_RANDOMSEED = 10

# The percentage of food that staff bot will try to cover (might cover more)
# Restore this to 0.2 when running preliminary autograder for phase 1
_PERCENTAGE = 0.2


class PickyStaffAgent(CaptureAgent):
  """
  This is the Staff bot intended for Phase 1.
  The bot will randomly choose a subset of food to capture. 
  Unlike in Phase 1, you will no longer have access to its plan.

  Please do not modify anything other than _RANDOMSEED and _PERCENTAGE
  All code will be evaluated remotely
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on).
    """

    '''
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py.
    '''
    CaptureAgent.registerInitialState(self, gameState)
    self.start = gameState.getAgentPosition(self.index)
    self.__foodList = self.pickFoodList(gameState)
    

  def pickFoodList(self, gameState):
    """
    Pick the list of food that the Phase 1 staffBot will attempt to capture eventually. 
    He will ignore food that is not in this list
    """
    fullFoodList = self.getFood(gameState).asList()
    n = len(fullFoodList)
    foodListLength = int(n * _PERCENTAGE)
    foodSet = set()

    random.seed(_RANDOMSEED)
    while len(foodSet) < foodListLength:
      foodSet.add(fullFoodList[random.randint(0, n)])

    return list(foodSet)

  def chooseAction(self, gameState):
    """
    The actual chooseAction, used in planning stage: Picks among the actions with the highest Q(s,a).
    """

    # First, update SELF.__FOODLIST
    curPos = gameState.getAgentState(self.index).getPosition()
    if (curPos in self.__foodList):
      self.__foodList.remove(curPos)

    actions = gameState.getLegalActions(self.index)

    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

    foodLeft = len(gameState.getFood().asList())

    return random.choice(bestActions)

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights

  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    fullFoodList = self.getFood(successor).asList()  
    features['successorScore'] = -len(fullFoodList)

    # Compute distance to the nearest food

    if len(self.__foodList) > 0: # This should always be True,  but better safe than sorry
      myPos = successor.getAgentState(self.index).getPosition()
      minDistance = min([self.getMazeDistance(myPos, food) for food in self.__foodList])
      features['distanceToFood'] = minDistance
    return features

  def getWeights(self, gameState, action):
    return {'successorScore': 100, 'distanceToFood': -1}


