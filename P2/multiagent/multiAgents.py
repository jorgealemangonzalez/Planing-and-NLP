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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        capsules = currentGameState.getCapsules()


        "*** YOUR CODE HERE ***"
        FoodList = newFood.asList()
        ghostList = currentGameState.getGhostPositions()
        score= 0
        minFood = 9999999
        minCapsule = 999999999
        minGhost = 9999999

        for foodPos in FoodList:
          minFood = min(minFood,abs(util.manhattanDistance(newPos,foodPos))) #distancia minima desde la proxima posicion al food mas cercano
        for ghostPos in ghostList:
          minGhost = min(minGhost,abs(util.manhattanDistance(newPos,ghostPos)))
        for capsule in capsules:
            minCapsule = min(minCapsule,abs(util.manhattanDistance(newPos,capsule))) 
        if minCapsule < minGhost:
            score += ((minGhost/minFood)/10) 
        if not minCapsule:
            minCapsule = 1
        score += (minGhost/minFood) + successorGameState.getScore() + (1/minCapsule)


        return score





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
        """
        "*** YOUR CODE HERE ***"

        def MAX(state, depth):
            bestValue = -1000000000
            if depth <= 0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            for action in state.getLegalActions(0):
                bestValue = max(bestValue,MIN(state.generateSuccessor(0,action), depth-1))

            return bestValue


        def MIN(state, depth):

            def ghostsMoves(ghostState,ghost):
                bestValue = 1000000000
                if depth <= 0 or ghostState.isLose() or ghostState.isWin():
                    return self.evaluationFunction(ghostState)
                if ghost >= state.getNumAgents():
                    return MAX(ghostState, depth - 1)
                for action in state.getLegalActions(ghost):
                    bestValue = min(bestValue, ghostsMoves(ghostState.generateSuccessor(ghost, action), ghost + 1))
                return bestValue

            return ghostsMoves(state,1)

        """To obtain the action without passing it in all min and max calls"""
        callDepth = self.depth * 2  # The depth is defined by 1 move of each agent : min and max. 
        bestAction = None
        bestValue = -100000000
        for action in gameState.getLegalActions(0):
            value = MIN(gameState.generateSuccessor(0,action),callDepth-1)
            if bestValue < value:
                bestValue = value
                bestAction = action

        return bestAction
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

        #alpha --> for maximizer
        #beta --> for minimizer
        def MAX(state, depth,alpha,beta): #valor maximo!
            bestValue = -1000000000
            if depth <= 0 or state.isWin() or state.isLose(): #si es terminal o final
                return self.evaluationFunction(state)

            for action in state.getLegalActions(0):
                bestValue = max(bestValue,MIN(state.generateSuccessor(0,action), depth,alpha,beta,1))  #calculamos Min de todos los sucesores
                if bestValue > beta: #cortamos rama
                    break
                alpha = max(alpha,bestValue) #actualizamos valor de alpha 
            return bestValue


        def MIN(state, depth,alpha,beta,ghostindex): #valor minimo
            bestValue = 1000000000
            if depth <= 0 or state.isLose() or state.isWin():
                return self.evaluationFunction(state)
            for action in state.getLegalActions(ghostindex): #todas las acciones del indice especificado
                if ghostindex == (state.getNumAgents()-1): #si es ultimo , disminuimos profundidad i max de los estados 
                    bestValue = min(bestValue,MAX(state.generateSuccessor(ghostindex,action),depth-1,alpha,beta))#maximizamos        
                else: # es un fantasma cualquiera, por lo tanto minimizamos
                    bestValue = min(bestValue, MIN(state.generateSuccessor(ghostindex, action),depth,alpha,beta, ghostindex + 1))#seguimos a la misma profundidad
                if bestValue < alpha: #podamos
                        break
                beta = min(beta,bestValue)
            return bestValue


        """To obtain the action without passing it in all min and max calls"""
        bestAction = None
        bestValue = -100000000
        alpha = -1000000000000000000
        beta = 100000000000000000
        for action in gameState.getLegalActions(0): #para todas las acciones del estado
            value = MIN(gameState.generateSuccessor(0,action),self.depth,alpha,beta,1)#minimo de la profundidad especificada y por todas las acciones
            if bestValue < value: #guardamos mejor accion
                bestValue = value
                bestAction = action
            alpha = max(alpha,bestValue)
            if bestValue > beta: #si obtenemos un valor mayor que nuestra beta, podamos
                break
        return bestAction
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

        def MAX(state, depth):
            bestValue = -1000000000
            if depth <= 0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            for action in state.getLegalActions(0):
                bestValue = max(bestValue, MIN(state.generateSuccessor(0, action), depth - 1))

            return bestValue

        def MIN(state, depth):

            def ghostsMoves(ghostState, ghost):
                bestValue = 1000000000
                if depth <= 0 or ghostState.isLose() or ghostState.isWin():
                    return self.evaluationFunction(ghostState)
                if ghost >= state.getNumAgents():
                    return MAX(ghostState, depth - 1)
                average = 0.0
                legalMoves = state.getLegalActions(ghost)
                for action in legalMoves:
                    average += (1.0/len(legalMoves)) * ghostsMoves(ghostState.generateSuccessor(ghost, action), ghost + 1)
                return average

            return ghostsMoves(state, 1)
        """To obtain the action without passing it in all min and max calls"""
        callDepth = self.depth * 2  #The depth is defined by 1 move of each agent : min and max.
        bestAction = None
        bestValue = -100000000
        for action in gameState.getLegalActions(0):
            value = MIN(gameState.generateSuccessor(0, action), callDepth - 1)
            if bestValue < value:
                bestValue = value
                bestAction = action

        return bestAction
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pacmanActions = currentGameState.getLegalPacmanActions()
    pacmanPos = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    ghostList = currentGameState.getGhostPositions()
    capsules = currentGameState.getCapsules()


    score = 0.0
    minFood = 99999999
    minGhost = 99999999
    minCapsule = 99999999

    for foodPos in foodList:
        minFood = min(minFood,abs(util.manhattanDistance(pacmanPos,foodPos))) #distancia minima desde la proxima posicion al food mas cercano
    for ghostPos in ghostList:
        minGhost = min(minGhost,abs(util.manhattanDistance(pacmanPos,ghostPos)))
    for capsule in capsules:
        minCapsule = min(minCapsule,abs(util.manhattanDistance(pacmanPos,capsule))) 
    if not minCapsule:
        minCapsule = 1
    score = (minGhost/minFood) + currentGameState.getScore() + (minGhost/minCapsule)

    return score

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

