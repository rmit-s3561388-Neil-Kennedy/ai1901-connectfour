from connectfour.agents.computer_player import RandomAgent
import random

class CellData(object):
    def __init__(self, EmptySpaceIR, EmptySpaceIL, EmptySpaceOR, EmptySpaceOL, OnesToRight, TwosToRight, OnesToLeft, TwosToLeft):
        self.EmptySpaceIR = EmptySpaceIR
        self.EmptySpaceIL = EmptySpaceIL
        self.EmptySpaceOR = EmptySpaceOR
        self.EmptySpaceOL = EmptySpaceOL
        self.OnesToRight = OnesToRight
        self.TwosToRight = TwosToRight
        self.OnesToLeft = OnesToLeft
        self.TwosToLeft = TwosToLeft

class StudentAgent(RandomAgent):
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 1

    def get_move(self, board):
        return self.calculateBestMove(board)
    
    def calculateBestMove(self, board):
        #Not using MinMax this only searchs a depth of two so maximum searches is 7^2
        first_moves = board.valid_moves()
        vals = []
        numTotalValues = []
        moves = []
        #evaluate our moves
        for first_move in first_moves:
            #get the board after each move
            first_state = board.next_state(self.id, first_move[1])
            #Add this move to the list of all moves array
            moves.append( first_move )
            #get the value of this move
            moveValue = self.evaluateMove(self.id, first_state, first_move)

            #get the next moves for this board state
            second_valid_moves = first_state.valid_moves()
            nextvals = []
            #evaluate the moves that can happen after us
            for second_move in second_valid_moves:
                #get the board state for the next move, then get the value and add it
                if self.id == 1:
                    second_state = first_state.next_state(1, second_move[1])
                    value = self.evaluateMove(2, second_state, second_move)
                    nextvals.append(value)
                else:
                    second_state = first_state.next_state(2, second_move[1])
                    value = self.evaluateMove(1, second_state, second_move)
                    nextvals.append(value)

            #Is the value of each one of the next moves(for the opposition) greater than our move
            TotalValueMoves = 0
            for value in nextvals:
                if moveValue != 64: #if our move is a winning move it doesn't matter what happens next
                    if value > moveValue: #dont add values unless they are better than our move
                        #add the value of each next move to get the total cost
                        TotalValueMoves += value
            
            #numTotalValues represents the total cost of each next move for the current move
            numTotalValues.append(TotalValueMoves)
            #add the current move value to the array
            vals.append(moveValue)

        #get the minimum value(represents the outcome with the least good moves for the opposition)
        minValue = 0
        if len(numTotalValues) > 0:
            minValue = min(numTotalValues)
        indexMoves = []
        index = 0
        maxValue = -1
        selectionIndex = 0
        #there may be more than one outcome that has the same cost as each other, so get the one that has the best move for us
        for value in numTotalValues:
            if value == minValue:
                if vals[index] > maxValue:
                    maxValue = vals[index]
                    selectionIndex = index
            index += 1

        #return the best move
        bestMove = moves[selectionIndex]
        return bestMove
           

    def evaluateMove(self, playerTurn, board, move):
        ScoreHorizontal = 0
        ScoreDiagonalForward = 0 #right,up and left,down
        ScoreDiagonalBackward = 0 #right,down and left,up
        ScoreVertical = 0

        #what column and row did we last move too with what value
        column = move[1]
        row = move[0]

        #look horizontal right 3 squares
        rightValueH = self.calculateRightValue(board,row,column)
        #look horizontal left 3 square
        leftValueH = self.calculateLeftValue(board,row,column)
        #look diagonal right up 3 squares
        rightValueU = self.calculateDiagonalRightUpValue(board,row,column)
        #look diagonal left down 3 squares
        leftValueD = self.calculateDiagonalLeftDownValue(board,row,column)
        #look diagonal left up 3 squares
        leftValueU = self.calculateDiagonalLeftUpValue(board,row,column)
        #look diagonal right down 3 squares
        rightValueD = self.calculateDiagonalRightDownValue(board,row,column)
        #look down 3 sqaures
        downValue = self.calculateDownValue(board,row,column)
        #look up 3 squares *just to find how close we are to the boundary
        upValue = self.calculateUpValue(board,row,column)
        
        ##format the data from the left and right values
        HorizontalData = self.parseCellData(rightValueH, leftValueH)
        DiagonalForwardData = self.parseCellData(rightValueU, leftValueD)
        DiagonalBackwardData = self.parseCellData(rightValueD, leftValueU)
        VerticalData = self.parseCellData(downValue, upValue)

        #Horizontal score--------------------------------------------------------
        ScoreHorizontal = self.evaluateCellScore(playerTurn,HorizontalData)
        #Diagonal Search---------------------------------------------------------
        ScoreDiagonalForward = self.evaluateCellScore(playerTurn,DiagonalForwardData)
        ScoreDiagonalBackward = self.evaluateCellScore(playerTurn,DiagonalBackwardData)
        #Vertical Search---------------------------------------------------------
        ScoreVertical = self.evaluateCellScore(playerTurn,VerticalData)
        #------------------------------------------------------------------------
        MaxValue = max(ScoreHorizontal,ScoreDiagonalForward,ScoreDiagonalBackward,ScoreVertical)

        #Return the value of all directions
        return ScoreHorizontal+ScoreDiagonalForward+ScoreDiagonalBackward+ScoreVertical

    #look right 3 squares
    def calculateRightValue(self, board, row, column):
        rightValue = 0
        for offsetR in range(1,4):
            NewColumn = column + offsetR
            if NewColumn < board.width:
                newCellvalue = board.board[row][NewColumn]
                #create right value integer
                if offsetR == 1:
                    rightValue += newCellvalue * 100
                elif offsetR == 2:
                    rightValue += newCellvalue * 10
                elif offsetR == 3:
                    rightValue += newCellvalue * 1
            else: #Out of bounds
                #create right value integer
                if offsetR == 1:
                    rightValue += 3 * 100
                elif offsetR == 2:
                    rightValue += 3 * 10
                elif offsetR == 3:
                    rightValue += 3 * 1
        return rightValue

    #look left 3 squares
    def calculateLeftValue(self, board, row, column):
        leftValue = 0
        for offsetL in range(1,4):
            NewColumn = column - offsetL
            if NewColumn >= 0:
                newCellvalue = board.board[row][NewColumn]
                #create left value integer
                if offsetL == 1:
                    leftValue += newCellvalue * 100
                elif offsetL == 2:
                    leftValue += newCellvalue * 10
                elif offsetL == 3:
                    leftValue += newCellvalue * 1
            else: #Out of bounds
                #create left value integer
                if offsetL == 1:
                    leftValue += 3 * 100
                elif offsetL == 2:
                    leftValue += 3 * 10
                elif offsetL == 3:
                    leftValue += 3 * 1
        return leftValue
    
    #look down 3 squares
    def calculateDownValue(self, board, row, column):
        downValue = 0
        for offsetD in range(1,4):
            NewRow = row + offsetD
            if NewRow < board.height:
                newCellvalue = board.board[NewRow][column]
                #create left value integer
                if offsetD == 1:
                    downValue += newCellvalue * 100
                elif offsetD == 2:
                    downValue += newCellvalue * 10
                elif offsetD == 3:
                    downValue += newCellvalue * 1
            else: #Out of bounds
                #create left value integer
                if offsetD == 1:
                    downValue += 3 * 100
                elif offsetD == 2:
                    downValue += 3 * 10
                elif offsetD == 3:
                    downValue += 3 * 1
        return downValue
    
    #look up 3 squares
    def calculateUpValue(self, board, row, column):
        upValue = 0
        for offsetU in range(1,4):
            NewRow = row - offsetU
            if NewRow >= 0:
                newCellvalue = board.board[NewRow][column]
                #create left value integer
                if offsetU == 1:
                    upValue += newCellvalue * 100
                elif offsetU == 2:
                    upValue += newCellvalue * 10
                elif offsetU == 3:
                    upValue += newCellvalue * 1
            else: #Out of bounds
                #create left value integer
                if offsetU == 1:
                    upValue += 3 * 100
                elif offsetU == 2:
                    upValue += 3 * 10
                elif offsetU == 3:
                    upValue += 3 * 1
        return upValue
    
    #look diagonally right up 3 squares
    def calculateDiagonalRightUpValue(self, board, row, column):
        rightValue = 0
        for offsetR in range(1,4):
            NewColumn = column + offsetR
            NewRow = row - offsetR
            if NewColumn < board.width and NewRow >= 0:
                newCellvalue = board.board[NewRow][NewColumn]
                #create right value integer
                if offsetR == 1:
                    rightValue += newCellvalue * 100
                elif offsetR == 2:
                    rightValue += newCellvalue * 10
                elif offsetR == 3:
                    rightValue += newCellvalue * 1
            else: #Out of bounds
                #create right value integer
                if offsetR == 1:
                    rightValue += 3 * 100
                elif offsetR == 2:
                    rightValue += 3 * 10
                elif offsetR == 3:
                    rightValue += 3 * 1
        return rightValue
    
    #look diagonally right up 3 squares
    def calculateDiagonalLeftUpValue(self, board, row, column):
        leftValue = 0
        for offsetL in range(1,4):
            NewColumn = column - offsetL
            NewRow = row - offsetL
            if NewColumn >= 0 and NewRow >= 0:
                newCellvalue = board.board[NewRow][NewColumn]
                #create right value integer
                if offsetL == 1:
                    leftValue += newCellvalue * 100
                elif offsetL == 2:
                    leftValue += newCellvalue * 10
                elif offsetL == 3:
                    leftValue += newCellvalue * 1
            else: #Out of bounds
                #create right value integer
                if offsetL == 1:
                    leftValue += 3 * 100
                elif offsetL == 2:
                    leftValue += 3 * 10
                elif offsetL == 3:
                    leftValue += 3 * 1
        return leftValue
    
    #look diagonallly left down 3 squares
    def calculateDiagonalLeftDownValue(self, board, row, column):
        rightValue = 0
        for offsetR in range(1,4):
            NewColumn = column - offsetR
            NewRow = row + offsetR
            if NewColumn >= 0 and NewRow < board.height:
                newCellvalue = board.board[NewRow][NewColumn]
                #create left value integer
                if offsetR == 1:
                    rightValue += newCellvalue * 100
                elif offsetR == 2:
                    rightValue += newCellvalue * 10
                elif offsetR == 3:
                    rightValue += newCellvalue * 1
            else: #Out of bounds
                #create left value integer
                if offsetR == 1:
                    rightValue += 3 * 100
                elif offsetR == 2:
                    rightValue += 3 * 10
                elif offsetR == 3:
                    rightValue += 3 * 1
        return rightValue
    
    #look diagonally right down 3 square
    def calculateDiagonalRightDownValue(self, board, row, column):
        rightValue = 0
        for offsetR in range(1,4):
            NewColumn = column + offsetR
            NewRow = row + offsetR
            if NewColumn < board.width and NewRow < board.height:
                newCellvalue = board.board[NewRow][NewColumn]
                #create left value integer
                if offsetR == 1:
                    rightValue += newCellvalue * 100
                elif offsetR == 2:
                    rightValue += newCellvalue * 10
                elif offsetR == 3:
                    rightValue += newCellvalue * 1
            else: #Out of bounds
                #create left value integer
                if offsetR == 1:
                    rightValue += 3 * 100
                elif offsetR == 2:
                    rightValue += 3 * 10
                elif offsetR == 3:
                    rightValue += 3 * 1
        return rightValue

    #Populates the CellData used for calculating the score
    def parseCellData(self, rightValue, leftValue):
        Data = CellData(0,0,0,0,0,0,0,0);
        #Right check-----------------------
        #1 one to right
        if (rightValue >= 100 and rightValue < 200 and rightValue != 110 and rightValue != 111) or (rightValue >= 10 and rightValue < 20 and rightValue != 11) or (rightValue == 1):
            Data.OnesToRight = 1
            if rightValue == 100:
                Data.EmptySpaceOR = 2
            elif rightValue == 10 or rightValue == 101 or rightValue == 102 or rightValue == 103:
                Data.EmptySpaceOR = 1
        #2 ones to right
        if (rightValue == 110 or rightValue == 112 or rightValue == 113 or rightValue == 11):
            Data.OnesToRight = 2
            if rightValue == 110:
                Data.EmptySpaceOR = 1
        #3 ones to right
        if (rightValue == 111):
            Data.OnesToRight = 3
            Data.EmptySpaceOR = 0
        #1 two to right
        if (rightValue >= 200 and rightValue < 300 and rightValue != 220 and rightValue != 222) or (rightValue >= 20 and rightValue < 30 and rightValue != 22) or (rightValue == 2):
            Data.TwosToRight = 1
            if rightValue == 200:
                Data.EmptySpaceOR = 2
            elif rightValue == 20 or rightValue == 201 or rightValue == 202 or rightValue == 203:
                Data.EmptySpaceOR = 1
        #2 twos to right
        if (rightValue == 220 or rightValue == 221 or rightValue == 223 or rightValue == 22):
            Data.TwosToRight = 2
            if rightValue == 220:
                Data.EmptySpaceOR = 1
        #3 twos to right
        if (rightValue == 222):
            Data.TwosToRight = 3
            Data.EmptySpaceOR = 0
        #Left check-----------------------
        #1 one to left
        if (leftValue >= 100 and leftValue < 200 and leftValue != 110 and leftValue != 111) or (leftValue >= 10 and leftValue < 20 and leftValue != 11) or (leftValue == 1):
            Data.OnesToLeft = 1
            if leftValue == 100:
                Data.EmptySpaceOL = 2
            elif leftValue == 10 or leftValue == 101 or leftValue == 102 or leftValue == 103:
                Data.EmptySpaceOL = 1
        #2 ones to left
        if (leftValue == 110 or leftValue == 112 or leftValue == 113 or leftValue == 11):
            Data.OnesToLeft = 2
            if leftValue == 110:
                Data.EmptySpaceOL = 1
        #3 ones to left
        if (leftValue == 111):
            Data.OnesToLeft = 3
            Data.EmptySpaceOL = 0
        #1 two to left
        if (leftValue >= 200 and leftValue < 300 and leftValue != 220 and leftValue != 222) or (leftValue >= 20 and leftValue < 30 and leftValue != 22) or (leftValue == 2):
            Data.TwosToLeft = 1
            if leftValue == 200:
                Data.EmptySpaceOL = 2
            elif leftValue == 20 or leftValue == 202 or leftValue == 202 or leftValue == 203:
                Data.EmptySpaceOL = 1
        #2 twos to left
        if (leftValue == 220 or leftValue == 221 or leftValue == 223 or leftValue == 22):
            Data.TwosToLeft = 2
            if leftValue == 220:
                Data.EmptySpaceOL = 1
        #3 twos to left
        if (leftValue == 222):
            Data.TwosToLeft = 3
            Data.EmptySpaceOL = 0
        #Right empty check-----------------------
        if rightValue >= 10 and rightValue < 100:
            Data.EmptySpaceIR = 1
        elif rightValue >= 1 and rightValue < 10:
            Data.EmptySpaceIR = 2
        elif rightValue == 0:
            Data.EmptySpaceIR = 3
        #Left empty check-----------------------
        if leftValue >= 10 and leftValue < 100:
            Data.EmptySpaceIL = 1
        elif leftValue >= 1 and leftValue < 10:
            Data.EmptySpaceIL = 2
        elif leftValue == 0:
            Data.EmptySpaceIL = 3
        return Data

    #calculate the largest value of this cell
    def evaluateCellScore(self, id, CellData):
        Score = 0
        #WINNING MOVES-------------------------
        if CellData.OnesToRight == 3 or CellData.OnesToLeft == 3: #-xxx?111 or 111?xxx
            if id == 1:
                Score = 64
        elif CellData.OnesToRight == 2 and CellData.EmptySpaceIR == 0 and CellData.OnesToLeft == 1 and CellData.EmptySpaceIL == 0: #-xx1?11x
            if id == 1:
                Score = 64
        elif CellData.OnesToLeft == 2 and CellData.EmptySpaceIL == 0 and CellData.OnesToRight == 1 and CellData.EmptySpaceIR == 0: #-xx2?22x
            if id == 1:
                Score = 64
        elif CellData.TwosToRight == 3 or CellData.TwosToLeft == 3: #-xxx?111 or 111?xxx
            if id == 2:
                Score = 64
        elif CellData.TwosToRight == 2 and CellData.EmptySpaceIR == 0 and CellData.TwosToLeft == 1 and CellData.EmptySpaceIL == 0: #-xx1?11x
            if id == 2:
                Score = 64
        elif CellData.TwosToLeft == 2 and CellData.EmptySpaceIL == 0 and CellData.TwosToRight == 1 and CellData.EmptySpaceIR == 0: #-xx2?22x
            if id == 2:
                Score = 64
        #MORE VALUABLE MOVES--------------------
        elif CellData.OnesToRight == 2 and CellData.EmptySpaceOR >= 1: #-xxx?110
            if id == 1:
                Score = 8
        elif CellData.TwosToRight == 2 and CellData.EmptySpaceOR >= 1: #-xxx?220
            if id == 2:
                Score = 8
        elif CellData.OnesToRight == 2 and CellData.EmptySpaceIL >= 1: #-xx0?11x
            if id == 1:
                Score = 8
        elif CellData.TwosToRight == 2 and CellData.EmptySpaceIL >= 1: #-xx0?22x
            if id == 2:
                Score = 8
        elif CellData.OnesToLeft == 2 and CellData.EmptySpaceOL >= 1: #-011?xxx
            if id == 1:
                Score = 8
        elif CellData.TwosToLeft == 2 and CellData.EmptySpaceOL >= 1: #-022?xxx
            if id == 2:
                Score = 8
        elif CellData.OnesToLeft == 2 and CellData.EmptySpaceIR >= 1: #-x11?0xx
            if id == 1:
                Score = 8
        elif CellData.TwosToLeft == 2 and CellData.EmptySpaceIR >= 1: #-x22?0xx
            if id == 2:
                Score = 8
        elif CellData.OnesToRight == 1 and (CellData.EmptySpaceOR == 1 or CellData.EmptySpaceOR == 2) and CellData.OnesToLeft == 1: #-xx1?10x
            if id == 1:
                Score = 8
        elif CellData.TwosToRight == 1 and (CellData.EmptySpaceOR == 1 or CellData.EmptySpaceOR == 2) and CellData.TwosToLeft == 1: #-xx2?20x
            if id == 2:
                Score = 8
        elif CellData.OnesToLeft == 1 and (CellData.EmptySpaceOL == 1 or CellData.EmptySpaceOL == 2) and CellData.OnesToRight == 1: #-x01?1xx
            if id == 1:
                Score = 8
        elif CellData.TwosToLeft == 1 and (CellData.EmptySpaceOL == 1 or CellData.EmptySpaceOL == 2) and CellData.TwosToRight == 1: #-x02?2xx
            if id == 2:
                Score = 8
        #SLIGHTLY VALUABLE MOVES------------------
        elif CellData.OnesToRight == 1 and CellData.EmptySpaceOR >= 1 and CellData.EmptySpaceIL >= 1: #-xx0?10x
            if id == 1:
                Score = 1
        elif CellData.OnesToLeft == 1 and CellData.EmptySpaceOL >= 1 and CellData.EmptySpaceIR >= 1: #-x01?0xx
            if id == 1:
                Score = 1
        elif CellData.OnesToRight == 1 and CellData.EmptySpaceOR >= 2: #-xxx?100
            if id == 1:
                Score = 1
        elif CellData.TwosToRight == 1 and CellData.EmptySpaceOR >= 2: #-xxx?200
            if id == 2:
                Score = 1
        elif CellData.OnesToLeft == 1 and CellData.EmptySpaceOL >= 2: #-001?xxx
            if id == 1:
                Score = 1
        elif CellData.TwosToLeft == 1 and CellData.EmptySpaceOL >= 2: #-002?xxx
            if id == 2:
                Score = 1
        elif CellData.OnesToRight == 1 and CellData.EmptySpaceIL >= 2: #-x00?1xx
            if id == 1:
                Score = 1
        elif CellData.TwosToRight == 1 and CellData.EmptySpaceIL >= 2: #-x00?2xx
            if id == 2:
                Score = 1
        elif CellData.OnesToLeft == 1 and CellData.EmptySpaceIR >= 2: #-xx1?00x
            if id == 1:
                Score = 1
        elif CellData.TwosToLeft == 1 and CellData.EmptySpaceIR >= 2: #-xx2?00x
            if id == 2:
                Score = 1
        return Score

