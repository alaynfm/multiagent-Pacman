# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        score = 0
        minimo = 0
        for food in newFood:
            path = util.manhattanDistance(food, newPos)
            if path > minimo:
                minimo = path
                score = score + (1 / path)

        for ghost in newGhostStates:
            ghostpos = ghost.getPosition()
            manhattan = util.manhattanDistance(newPos, ghostpos)
            if manhattan > 1:
                score = score + (1 / manhattan)
            else:
                if ghost.scaredTimer >= 1:
                    score = score + (1 / manhattan)
                else:
                    score = -999999999

        if action == 'Stop':
            score = score - 999

        return score + successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        value,action = self.value(gameState,0,self.depth)
        return action

    def value(self,gameState,agentIndex,profundidad):
        if profundidad == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState),Directions.STOP
        else:
            if agentIndex == gameState.getNumAgents():
                agentIndex= 0
            if agentIndex == gameState.getNumAgents() - 1:
                profundidad = profundidad - 1
            if agentIndex == 0:
                return self.maxValue(gameState,agentIndex,profundidad)
            else:
                return self.expValue(gameState,agentIndex,profundidad)
    def maxValue(self,gameState,agentIndex, profundidad ):
        v = -99999999999
        vaction = gameState.getLegalActions(agentIndex)[0]
        for action in gameState.getLegalActions(agentIndex):
            v_point, v_action = self.value(gameState.generateSuccessor(agentIndex,action),agentIndex + 1 , profundidad)
            if v_point>v:
                v = v_point
                vaction = action
        return v,vaction

    def expValue(self,gameState,agentIndex, profundidad ):
        score = 0
        vaction=gameState.getLegalActions(agentIndex)[0]
        for action in gameState.getLegalActions(agentIndex):
            v_point,v_action=self.value(gameState.generateSuccessor(agentIndex, action),agentIndex+1,profundidad)
            score +=v_point*1/len(gameState.getLegalActions(agentIndex))
        return (score, vaction)






def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    score = 400
    foodList = newFood.asList()
    for food in foodList:
        difCoord = abs(food[0] - newPos[0]) + abs(food[1] - newPos[1])

        if (difCoord == 0):
            score = score + 10
        else:
            if (difCoord == 1):
                score = score + 8
            else:
                if (difCoord == 2):
                    score = score + 6
                else:
                    if (difCoord == 3):
                        score = score + 4
                    else:
                        if (difCoord == 4):
                            score = score + 3
                        else:
                            if (difCoord == 5):
                                score = score + 2
                            else:
                                if (difCoord == 6):
                                    score = score + 1
    randScore = random.randrange(10)
    score = score + randScore
    "#Esta es la linea nueva que cambia todo"
    if (newScaredTimes[0] == 0):
        for ghost in newGhostStates:
            ghPos = ghost.getPosition()
            difCoord = abs(ghPos[0] - newPos[0]) + abs(ghPos[1] - newPos[1])
            if (difCoord == 0):
                score = score - 40
            else:
                if (difCoord == 1):
                    score = score - 300
                else:
                    if (difCoord == 2):
                        score = score - 220
                    else:
                        if (difCoord == 3):
                            score = score - 160
                        else:
                            if (difCoord == 4):
                                score = score - 40
    else:
        for ghost in newGhostStates:
            ghPos = ghost.getPosition()
            difCoord = abs(ghPos[0] - newPos[0]) + abs(ghPos[1] - newPos[1])
            if (difCoord == 0):
                f = 12
            else:
                if (difCoord == 1):
                    f = 11
                else:
                    if (difCoord == 2):
                        f = 10
                    else:
                        if (difCoord == 3):
                            f = 9
                        else:
                            if (difCoord == 4):
                                f = 8
                            else:
                                f = 1
            score = score + (f*(newScaredTimes[0]/2))

    comidasRestantes = len(foodList)
    puntosFuerzaRestantes = len(currentGameState.getCapsules())
    score = score + (120-(comidasRestantes*2)) + puntosFuerzaRestantes*4.2
    return score + scoreEvaluationFunction(currentGameState)

# Abbreviation
better = betterEvaluationFunction
