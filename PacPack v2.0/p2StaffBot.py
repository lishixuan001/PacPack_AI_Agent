# p2StaffBot.py
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

# The limit for length of plan. This is fixed, so only the first 400 steps are visible
_LIMIT = 400

# The seed for randomly choosing food to persure. 
# This will be different during test time, please try to generalize
# Restore this to 7 when running preliminary autograder for phase 2
_RANDOMSEED = 7

# The percentage of food that staff bot will try to cover (might cover more)
# This might be different during test time, please try to generalize
# Restore this to 0.4 when running preliminary autograder for phase 2
_PERCENTAGE = 0.4


class PlannedStaffAgent(CaptureAgent):
  """
  This is the Staff bot intended for Phase 2.
  The bot will pick a plan up to _LIMIT steps, and your bot will recieve this information.
  The plan will be very useful to your cooperation. Please make good use of this

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
    # Boolean that signals whether the bot have finished similating the game
    self.__donePlanning = False
    
    self.actionPlan = self.generatePlan(gameState)
    # Make copy so that students cannot modify agent plan
    self.toInitialBroadcast = list(self.actionPlan)
  
    # Which step in the plan is the bot currently at, offsetted by 1
    self.planStep = 0

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
    Simply follow the plan in SELF.PLAN. If memory cannot hold the information anymore, improvise
    """
    if self.planStep < _LIMIT:
      action = self.actionPlan[self.planStep]
      self.planStep += 1
      return action
    else:
      return self.chooseActionPlan(gameState)

  def chooseActionPlan(self, gameState):
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
  
  def generatePlan(self, startGameState):
    '''
    The function that print and return the list of actions
    this bot will perform, starting with the action of the
    bots following turn
    '''
    gs = startGameState
    planActions = []
    step = 0
    while not self.__donePlanning and step < _LIMIT:
      action = self.chooseActionPlan(gs)
      planActions.append(action)
      gs = self.getSuccessor(gs, action)
      step += 1
    return planActions