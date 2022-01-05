""" 
Q-Learning Agent. 
features could be defined as number of empty spots at each line, location of empty spots at each line, falling object,
and next object. 
gameState could be defined as all of the information needed for the feature + score + currentLevel + possible actions
"""
import random
import util

class ApproximateQAgent():
    '''
    Module used for an approximateQAgent with features. This class implements
    Approximate Q Learning. Extend it to implement specific agents. Only override
    getFeatures(), rewardFunction(), final(), and getWeights() Functions.
    '''

    def __init__(self, gameState):
        self.weights = util.Counter(self.getWeights())
        # Turn off learning parameters by changing discount and epsilon to be zero
        self.alpha = 0.7
        self.epsilon = 1.0
        self.discount = 0.0
        

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
        
        possibleActions = gameState.getLegalActions(self.index)
        if gameState.isTerminal():
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
        possibleActions = gameState.getLegalActions(self.index)
        if gameState.isTerminal():# terminal state check
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
        return {}

    def getFeatures(self, gameState, action):
        '''
        Gets features for the offensive agent
        '''
        features = util.Counter()
        features['score'] = gameState.getScore()
        return features

    def rewardFunction(self, gameState, successorState):
        # Rewards for increasing score
        reward = successorState.getScore() - gameState.getScore()
        return reward
    
    def chooseAction(self, gameState):
        legalActions = gameState.getLegalActions() # get legal actions
        print(legalActions)
        if gameState.getPreviousObservation() is None: # if first move, choose randomly
            return random.choice(legalActions)
        if util.flipCoin(self.epsilon):
            action = random.choice(legalActions)
        else:
            action = self.computeActionFromQValues(gameState)
        if action is None:
            action = 'restart'
        return action
