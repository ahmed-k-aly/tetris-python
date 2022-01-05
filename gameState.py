class gameState():
    """
    Class that defines what a gameState is consisted of
    """
    def __init__(self, mainBoard, previousGameStatesList, directions):
        self.mainBoard = mainBoard
        self.space = mainBoard.blockMat
        self.piece = mainBoard.piece
        self.score = mainBoard.score
        self.level = mainBoard.level
        self.lines = mainBoard.lines
        self.nextPieces = mainBoard.nextPieces
        self.previousObservations = previousGameStatesList 
        self.previousObservations.append(self) # add current observation
        self.directions = directions

    def isStartingMenu(self):
        """
        Returns true if we're at the starting menu
        """
        return len(self.previousObservations) == 0

    def getLevel(self):
        return self.level

    def getLinesRemoved(self):
        return self.lines

    def getScore(self):
        return self.score

    def getPreviousObservation(self):
        if len(self.previousObservations) == 1: # first observation
            return None # no observation yet
        return self.previousObservations[-2]

    def getPreviousObservations(self):
        return self.previousObservations

    def getLastAction(self):
        return self.piece.lastMoveType

    def getMovingPieceType(self):
        return self.piece.type

    def getMovingPieceStatus(self):
        return self.piece.type

    def getMovingPiecePosition(self):
        return (self.piece.colNum, self.piece.rowNum)

    def getLegalSuccessorPositions(self):
        """ 
        Function that returns the possible transition positions.
        """
        if self.isTerminal():
            return("TERMINAL_STATE")
        futurePositions = []
        pos = self.getMovingPiecePosition()  # piece xy vector
        for direction in self.directions:  # loop over all directions
            transformation = self.directions[direction]  # get direction vector
            # add direction vector on current position
            dx, dy = tuple(map(lambda i, j: i + j, pos, transformation))
            try:
                if self.space[dx][dy] == 'empty':  # If position is empty, it's legal
                    futurePositions.append((dx, dy))
            except IndexError:  # If new position is out of bounds, continue.
                continue
        return futurePositions

    def getLegalActions(self):
        """ 
        Function that returns the possible actions our 
        agent is allowed to perform.
        """
        if self.isTerminal() or self.isStartingMenu() : # if we hit a terminal state (game over)
            return([]) # return empty list

        actions = ['R_rotate', 'L_rotate']  # rotate left, rotate right
        successorStates = self.getLegalSuccessorPositions()
        pos = self.getMovingPiecePosition()
        for direction in self.directions:
            transformation = self.directions[direction]
            dx, dy = tuple(map(lambda i, j: i + j, pos, transformation)) # adds transformation tuple on position tuple (vector addition)
            if (dx, dy) in successorStates:
                actions.append(direction)
        return actions

    def isTerminal(self):
        """ 
        returns if the current gameState is a terminal state
        """
        return self.piece.gameOverCondition
