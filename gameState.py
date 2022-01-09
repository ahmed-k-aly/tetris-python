import copy
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
        self.gameState = mainBoard.gameStatus
    
    def generateSuccessorState(self, action):
        mainBoard = copy.deepcopy(self.mainBoard)
        previousGameStatesList = copy.deepcopy(self.previousObservations)
        if mainBoard.gameStatus == 'firstStart':
            if action == 'restart':
                mainBoard.restart()
        elif mainBoard.gameStatus == 'running':
            if mainBoard.gamePause == False:
                # move piece
                if mainBoard.piece.status == 'uncreated':
                    #Create newPiece
                    mainBoard.piece.status = 'moving'
                    mainBoard.piece.spawn()
                if action == 'right':
                    if mainBoard.piece.movCollisionCheck('down'):
                        mainBoard.piece.status = 'collided'
                        mainBoard.piece.createNextMove('noMove')
                    elif mainBoard.piece.movCollisionCheck('downRight'):
                        mainBoard.piece.createNextMove('down')
                    else:
                        mainBoard.piece.createNextMove('downRight')
                elif action == 'left':
                    if mainBoard.piece.movCollisionCheck('down'):
                        mainBoard.piece.status = 'collided'
                        mainBoard.piece.createNextMove('noMove')
                    elif mainBoard.piece.movCollisionCheck('downLeft'):
                        mainBoard.piece.createNextMove('down')
                    else:
                        mainBoard.piece.createNextMove('downLeft')
                elif action == 'down':
                    if mainBoard.piece.movCollisionCheck('down'):
                        mainBoard.piece.createNextMove('noMove')
                        mainBoard.piece.status = 'collided'
                    else:
                        mainBoard.piece.createNextMove('down')
                elif action == 'noMove':
                    mainBoard.piece.createNextMove('noMove')
                #mainBoard.piece.applyFastMove() # initiate move
                #mainBoard.piece.slowMoveAction() # initiate move
                mainBoard.checkAndApplyGameOver()
                if mainBoard.gameStatus != 'gameOver':
                    if mainBoard.piece.status == 'moving': # piece is moving
                        if action == 'up':	
                            mainBoard.piece.rotate('CW')
                        if action == 'z':	
                            mainBoard.piece.rotate('cCW')
                    elif mainBoard.piece.status == 'collided':			
                        if mainBoard.lineClearStatus == 'idle':
                            for i in range(0,4):
                                mainBoard.blockMat[mainBoard.piece.blocks[i].currentPos.row][mainBoard.piece.blocks[i].currentPos.col] = mainBoard.piece.type
                            mainBoard.clearedLines = mainBoard.getCompleteLines()
                            mainBoard.updateScores()
                        elif mainBoard.lineClearStatus == 'clearRunning':
                            mainBoard.lineClearAnimation()
                        else:
                            mainBoard.dropFreeBlocks()
                            mainBoard.prepareNextSpawn()
        else: # 'gameOver'
            if action == 'restart':
                mainBoard.restart()
        return gameState(mainBoard, previousGameStatesList, self.directions)

    
    def getStateSpace(self):
        return self.space

    def isStartingMenu(self):
        """
        Returns true if we're at the starting menu
        """
        return self.gameState == 'firstStart'

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
    
    def getNextPiece(self):
        return self.nextPieces[-1]



    def getLegalActions(self):
        """ 
        Function that returns the possible actions our 
        agent is allowed to perform.
        """
        if self.isTerminal() or self.isStartingMenu() : # if we hit a terminal state (game over)
            return([]) # return empty list

        actions = ['R_rotate', 'L_rotate','down','up','downRight','downLeft','noMove']
        return actions
    
    def isTerminal(self):
        """ 
        returns if the current gameState is a terminal state
        """
        return self.gameState == 'gameOver'

    def isGameRunning(self):
        return self.gameState == 'running'