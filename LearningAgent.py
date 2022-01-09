""" 
Q-Learning Agent. 
features could be defined as number of empty spots at each line, location of empty spots at each line, falling object,
and next object. 
gameState could be defined as all of the information needed for the feature + score + currentLevel + possible actions
"""
import random
import util
import json
import pprint
import numpy as np
class ApproximateQAgent():
    '''
    Module used for an approximateQAgent with features. This class implements
    Approximate Q Learning. Extend it to implement specific agents. Only override
    getFeatures(), rewardFunction(), final(), and getWeights() Functions.
    '''

    def __init__(self, gameState):
        self.weights = util.Counter(self.getWeights())
        self.previousAction = None
        self.maxEpisodes = 150
        self.currEpisode = 0
        self.training = True #if self.maxEpisodes >= self.currEpisode else False
        self.alpha = 0.7
        if self.training:
            self.epsilon = 0.4
            self.discount = 0.8
        else:
            self.epsilon = 0.0
            self.discount = 0.0
        # Turn off learning parameters by changing discount and epsilon to be zero
        

    def getQValue(self, gameState, action):
        '''
        Takes a gamestate and an action and returns the Q value for the state-action pair.
        '''
        features = self.getFeatures(gameState, action)  # get features
        weights = self.weights
        QValue = 0
        for feature in features:  # loop through features
            if features[feature] == None:
                continue
            try:
                QValue += features[feature] * weights[feature]  # implement equation
            except:
                print("Error with feature: {}\n".format(feature))
                continue
        return QValue

    def update(self, gameState, action, nextGameState, reward):
        """
        updates weights based on transition (used for training)
        """
        QValueOldState = self.getQValue(gameState, action)  # current state QValue
        QValueNextState = self.getValue(nextGameState)  # next state value
        difference = (reward + (self.discount * QValueNextState)) - QValueOldState
        features = self.getFeatures(gameState, action)
        for feature in features:  # loop through features
            self.weights[feature] += (self.alpha * difference * features[feature])  # implement equations

    def chooseAction(self, gameState):
        if util.flipCoin(self.epsilon):
            action = random.choice(gameState.getLegalActions())
        else:
            action = self.computeActionFromQValues(gameState)
        return action


    def getPolicy(self, gameState):
        '''
        Returns the optimal action according to the policy.
        '''
        return self.computeActionFromQValues(gameState)

    def computeActionFromQValues(self, gameState):
        """
        Compute the best action to take in a state.  Note that if there
        are no legal actions, which is the case at the terminal state,
        you should return None.
        """
        
        possibleActions = gameState.getLegalActions()
        if len(possibleActions) == 0:
            return None
        QValues = util.Counter()
        for action in possibleActions:  # loop through possible actions
            QValue = self.getQValue(gameState, action)
            QValues[action] = QValue
        return QValues.argMax()

    def computeValueFromQValues(self, gameState):
        """
        Returns max_action Q(state,action)
        where the max is over legal actions.  Note that if
        there are no legal actions, which is the case at the
        terminal state, you should return a value of 0.0.
        """
        compareList = []  # Put all possible action combinations for one state and get max
        possibleActions = gameState.getLegalActions()
        if len(possibleActions) == 0:# terminal state check
            return 0.0
        for action in possibleActions:  # Loop through legal actions
            QValue = self.getQValue(gameState, action)
            compareList.append(QValue)  # Add QValues of all legal actions for that state in compareList
        return max(compareList)  # Return the top

    def getValue(self, gameState):
        '''
        Returns value of a state
        '''
        return self.computeValueFromQValues(gameState)

    def getWeights(self):
        '''
        Gets the weights for features. Override in specific agents
        '''
        pass

    def getFeatures(self, gameState, action):
        '''
        Generate features for agent. Override in specific agents.
        '''
        pass

    def rewardFunction(self, gameState, successorState):
        '''
        Function used to generate reward. Override in specific agents
        '''
        pass

    def final(self, gameState):
        '''
        Called after game concludes (used for learning). Override in later classes
        '''
        pass


class TetrisQAgent(ApproximateQAgent):
    '''
    Tetris Approximate Q Agent
    '''

    def __init__(self, gameState):
        ApproximateQAgent.__init__(self, gameState)

    def getWeights(self):
        '''
        Gets the weights for features. Weights are hardcoded in after training
        '''
        # transform json dict to counter object
        try:
            with open('Weight.json') as json_file: # if weight file exists, use it.
                weights = json.load(json_file)
                return weights
        except Exception:
            return {}
    
    def final(self, gameState):
        self.currEpisode += 1
        #if self.currEpisode > self.maxEpisodes: # if training is over
         #   self.maxEpisodes += 100
        with open("Weight.json", 'w') as json_file:
            json.dump(self.weights, json_file)


    def getFeatures(self, gameState, action):
        '''
        Gets features for the offensive agent
        '''
        features = util.Counter()
        features['bias'] = 1.0 # incorporate external factors as bias
        piece = gameState.getMovingPieceType()
        # select piece type
        # if piece == 'I':
        #     features['I'] = 1.0
        # elif piece == 'O':
        #     features['O'] = 1.0
        # elif piece == 'T':
        #     features['T'] = 1.0
        # elif piece == 'S':
        #     features['S'] = 1.0
        # elif piece == 'Z':
        #     features['Z'] = 1.0
        # elif piece == 'J':
        #     features['J'] = 1.0
        # elif piece == 'L':
        #     features['L'] = 1.0
        features[piece] = 1.0
        #features[piece + " " + gameState.getNextPiece()] = 1.0 # this piece + next piece
        features['position'] = gameState.getMovingPiecePosition()[0]
        #self._getCellsFeatures(gameState, piece, features)
        #self._getLineFeatures(gameState, features)
        features['smoothnessColumns'] = self._smoothnessColumns(gameState)
        #features['smoothnessRows'] = self._smoothnessRows(gameState)
        #print(features['smoothnessColumns'])
        features.divideAll(100.0)
        while self.weights[features.argMax()] > 10000: # buffer
            self.weights.divideAll(100)
        return features
    
    

    def _smoothnessRows(self, gameState):
        ''' 
        Calculates the smoothness of the Rows by calculating
        the standard deviation of the width of the rows
        '''
        space = gameState.getStateSpace()
        rowWidths = []
        # calculate heights of each column
        i = 0
        for x in range(len(space[i])):
            i+=1
            rowWidth = 0
            for y in range(len(space)):
                rowWidth += 1 if space[y][x] == 'empty' else 0.0
            rowWidths.append(rowWidth) # append height of each column
        return np.std(rowWidths) # calculate stdDeviation

    
    
    def _smoothnessColumns(self, gameState):
        ''' 
        Calculates the smoothness of the columns by calculating
        the standard deviation of the height of the columns
        '''
        space = gameState.getStateSpace()
        colHeights = []
        # calculate heights of each column
        for x in range(len(space)):
            colHeight = 0
            for y in range(len(space[x])):
                colHeight += 1 if space[x][y] != 'empty' else 0.0
            colHeights.append(colHeight) # append height of each column
        return np.std(colHeights) # calculate stdDeviation

    def _getNumEmptySpots(self, gameState, features):
        """ 
        Feature that gets the number of empty spots in the entire board,
        """
        space = gameState.getStateSpace()
        for x in range(len(space)):
            for y in range(len(space[x])):
                features['numEmptySpots'] += 1.0 if space[x][y] == 'empty' else 0.0

    def _getNumEmptySpotsPerLine(self, gameState, features):
        """ 
        Feature that gets the number of empty spots per line
        """
        space = gameState.getStateSpace()
        for i in range(len(space)):
            for j in range(len(space[i])):
                features[str(i)] += 1.0 if space[i][j] == 'empty' else 0.0
                features[str(j)] += 1.0 if space[i][j] == 'empty' else 0.0

    def _getLineFeatures(self, gameState, features):
        space = gameState.getStateSpace()
        x,y = gameState.getMovingPiecePosition()
        for j in range(len(space[x])):
            cell = space[x][j]
            if cell == 'empty':
                cellString = str(x) + str(j)
                features[cellString] = 1.0
        for i in range(len(space)):
            try:
                cell = space[i][y]
            except IndexError:
                continue
            if cell == 'empty':
                cellString = str(i) + str(y)
                features[cellString] = 1.0

    def getIfeatures(self, gameState, piece):
        """ 
        Method that returns the features for the 'I' shaped piece.
        """
        features = util.Counter()
        if piece != 'I': # check if we're an I piece
            return features
        features[piece] = 1.0


    def _getCellsFeatures(self, gameState, piece, features):
        """ 
        Helper method that gets the status of each cell for the given piece and gameState. 
        A cell's value is 1.0 if it's empty, 0 otherwise.
        """
        space = gameState.getStateSpace()
        for i in range(len(space)):
            for j in range(len(space[i])):
                cell = space[i][j]
                if cell == "empty":
                    cellString = str(i) + str(j) # concatenate strings
                    features[piece + cellString] = 1.0
        return features


    def getOfeatures(self, piece):
        pass
    def getTfeatures(self, piece):
        pass
    def getSfeatures(self, piece):
        pass
    def getZfeatures(self, piece):
        pass
    def getJfeatures(self, piece):
        pass
    def getLfeatures(self, piece):
        pass

    def rewardFunction(self, gameState, successorState):
        # Rewards for increasing score
        reward = 0
        reward += successorState.getScore() - gameState.getScore()
        reward += 100*(successorState.getLinesRemoved() - gameState.getLinesRemoved())
        if (successorState.getLinesRemoved() - gameState.getLinesRemoved()) == 0:
            # if no lines were removed, take points off
            reward += -1.0
        reward -= 10000/(successorState.getScore()+1)
        if self._smoothnessColumns(successorState) < self._smoothnessColumns(gameState):
            reward += 100
        if self._smoothnessColumns(successorState) == 0.0:
            # lines were removed, reward greatly
            reward += 1000000
        if successorState.isTerminal():
            reward += -12345
        return reward
    
    def chooseAction(self, gameState):
        legalActions = gameState.getLegalActions() # get legal action
        if gameState.getPreviousObservation() is None: # if first move, start game
            self.previousAction = 'restart'
            return 'restart'
        if not gameState.isGameRunning(): # if game is not running
            self.previousAction = 'restart'
            return 'restart'
        
        previousGameState = gameState.getPreviousObservation()
        currentGameState = previousGameState.generateSuccessorState(self.previousAction)
        
        # training function
        reward = self.rewardFunction(previousGameState, gameState) # generate reward
        self.update(previousGameState, self.previousAction, gameState, reward) # do TD update
        
        if util.flipCoin(self.epsilon):
            action = random.choice(legalActions)
        else:
            action = self.computeActionFromQValues(gameState)
        if action is None:
            action = 'restart'
        self.previousAction = action
        return action
