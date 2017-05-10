from BaseAI import BaseAI
import time
from collections import deque
from operator import add
from copy import deepcopy

class PlayerAI(BaseAI):
    
    '''
    Continue grading moves until clocker runs out
    Upon time up, return the current best move
    
    Order moves as the grading proceeds
    Process is on UDLR order, breadth first
    
    Upon completion of every level, reorder the moves and scores panel
    
    Create starting search nodes UDLR, depth 1, Cmove=mastermove, add to FIFO fringe
    start loop (fringe empty)
    start loop (depth)
    reset newScores list
    for every node score grid
        add score to correct newscores list item (based on mastermove)
        update scca scores (add newScores)
        call timelimiter
        create new nodes UDLR with the same master move, depth +1, add to fringe for all moves
        end loop (depth)
        run minimiser for every item in fringe (at depth+1)
            create grid with new entry 2
            score grid with new entry 2
            create grid with new entry 4
            score grid with new entry 4
            create node with smallest score grid and add to fringe on depth +1
    depth = depth+2 (because there are 2 increases)
    debug print depth
    end loop (fringe empty)
    return scca.getBest()
    '''
    
    class gMove():
        UP, DOWN, LEFT, RIGHT = range(4)
    
    class autosort():
        
        def __init__(self):
            self.scores = [1,5,2,6]
        
        def addScores(self, newScores):
            self.scores = map(add, self.scores, newScores)
        
        def getBest(self):
            return self.scores.index(max(self.scores))
        
        def invalidateMove(self, cMove):
            self.scores[cMove] = -100000000
        
        def resetScores(self):
            self.scores = [1,5,2,6]
            
    class SearchNode():
        
        def __init__(self, master, cMove, cDepth, grid, PlayerMove=True):
            self.mastermove = master
            self.depth = cDepth
            self.move = cMove
            if(PlayerMove):
                self.grid = deepcopy(grid)
                self.valid = self.grid.move(cMove)
            else:
                self.grid = grid
                self.valid = True
            
        def isValid(self):
            return self.valid
        
        def getGrid(self):
            return self.grid
        
        def getDepth(self):
            return self.depth
        
        def getMaster(self):
            return self.mastermove
        
    @staticmethod
    def gridPartition(grid, ind, col=False):
        part = []
        
        n = grid.size
        
        if(col):
            for i in range(n):
                part.append(grid.getCellValue((ind, i)))
        else:
            for i in range(n):
                part.append(grid.getCellValue((i, ind)))
        
        return part
        
    @staticmethod
    def manhattanDistance(lis):
        sumd = 0
        
        for i in range(1,len(lis)):
            if(lis[i-1]==0):
                continue
            sumd= sumd + (lis[i] / lis[i-1])
        
        return sumd

    @staticmethod
    def gridDistance(grid):
        score = 0
        
        n = grid.size
        
        for i in range(n):
            score = score + PlayerAI.manhattanDistance(PlayerAI.gridPartition(grid, i))
            score = score + PlayerAI.manhattanDistance(PlayerAI.gridPartition(grid, i, True))
        
        
        return score
        
    global scca
    scca = autosort()
    
    def getMove(self, grid):
        
        moves = grid.getAvailableMoves()
        if (not moves):
            return None
        
        global timer 
        timer = time.clock()
        global clocker
        clocker = 0
        global GOTIME
        GOTIME = False
        
        global scca
        scca.resetScores()
        
        try:
            return PlayerAI.getBestMove(grid,moves)
        except Exception:
            return scca.getBest()
    
    
    @staticmethod
    def timeLimiter():
        global moves
        global timer
        global clocker
        global GOTIME
        
        clocker = time.clock()-timer
        
        if(clocker>=0.09):
            GOTIME = True
    
    
    @staticmethod
    def getGridScorer(grid, currDepth):
        score = PlayerAI.getGridScore(grid)
        return score
    
    @staticmethod
    def getBestMove(grid, validMoves):
        
        global scca
        global GOTIME
        
        currentDepth = 1
        
        fringe = deque([])
        
        if(PlayerAI.gMove.UP in validMoves):
            S1=PlayerAI.SearchNode(PlayerAI.gMove.UP, PlayerAI.gMove.UP, currentDepth, grid)
            if(S1.isValid()):
                fringe.append(S1)
        else:
            scca.invalidateMove(PlayerAI.gMove.UP)
        if(PlayerAI.gMove.DOWN in validMoves):
            S1=PlayerAI.SearchNode(PlayerAI.gMove.DOWN, PlayerAI.gMove.DOWN, currentDepth, grid)
            if(S1.isValid()):
                fringe.append(S1)
        else:
            scca.invalidateMove(PlayerAI.gMove.DOWN)
        if(PlayerAI.gMove.LEFT in validMoves):
            S1=PlayerAI.SearchNode(PlayerAI.gMove.LEFT, PlayerAI.gMove.LEFT, currentDepth, grid)
            if(S1.isValid()):
                fringe.append(S1)
        else:
            scca.invalidateMove(PlayerAI.gMove.LEFT)
        if(PlayerAI.gMove.RIGHT in validMoves):
            S1=PlayerAI.SearchNode(PlayerAI.gMove.RIGHT, PlayerAI.gMove.RIGHT, currentDepth, grid)
            if(S1.isValid()):
                fringe.append(S1)
        else:
            scca.invalidateMove(PlayerAI.gMove.RIGHT)
        
        currentNode = fringe.popleft()
        depthLimit = currentDepth
        while(len(fringe)!=0):
            newScores = [0,0,0,0]
            while(currentNode.getDepth()==depthLimit):
                score = PlayerAI.getGridScorer(currentNode.getGrid(), depthLimit)
                newScores[currentNode.getMaster()] += score
                
                S1=PlayerAI.SearchNode(currentNode.getMaster(), PlayerAI.gMove.UP, 1+currentNode.getDepth(), currentNode.getGrid())
                if(S1.isValid()):
                    fringe.append(S1)
                S1=PlayerAI.SearchNode(currentNode.getMaster(), PlayerAI.gMove.DOWN, 1+currentNode.getDepth(), currentNode.getGrid())
                if(S1.isValid()):
                    fringe.append(S1)
                S1=PlayerAI.SearchNode(currentNode.getMaster(), PlayerAI.gMove.LEFT, 1+currentNode.getDepth(), currentNode.getGrid())
                if(S1.isValid()):
                    fringe.append(S1)
                S1=PlayerAI.SearchNode(currentNode.getMaster(), PlayerAI.gMove.RIGHT, 1+currentNode.getDepth(), currentNode.getGrid())
                if(S1.isValid()):
                    fringe.append(S1)
                
                PlayerAI.timeLimiter()
                if(GOTIME):
                    return scca.getBest()
                currentNode = fringe.popleft()
            scca.addScores(newScores)
            PlayerAI.timeLimiter()
            if(GOTIME):
                return scca.getBest()
            n = currentNode.getGrid().size
            while(currentNode.getDepth()==(1+depthLimit)):
                cells = currentNode.getGrid().getAvailableCells()
                if(len(cells)<=n/3):
                    minScore = 100000
                    for cell in cells:
                        if(cell==(n-1,n-1)):
                            continue
                        grid2 = deepcopy(currentNode.getGrid())
                        grid2.setCellValue(cell, 2)
                        score = PlayerAI.getGridScorer(grid2, 1+depthLimit)
                        if(score<minScore):
                            minGrid = grid2
                            minScore = score
                        grid4 = deepcopy(currentNode.getGrid())
                        grid4.setCellValue(cell, 4)
                        score = PlayerAI.getGridScorer(grid4, 1+depthLimit)
                        if(score<minScore):
                            minGrid = grid4
                            minScore = score
                else:
                    minGrid = currentNode.getGrid().clone()
                    minGrid.setCellValue(cells[len(cells)-1], 2)
                fringe.append(PlayerAI.SearchNode(currentNode.getMaster(), 0, 1+currentNode.getDepth(), minGrid, False))
                PlayerAI.timeLimiter()
                if(GOTIME):
                    return scca.getBest()
                currentNode = fringe.popleft()
            
            depthLimit = depthLimit + 2
        return scca.getBest()



    

        
            
    @staticmethod
    def getGridScore(grid): #389-399 328-343
        moves = grid.getAvailableMoves()
        if(not moves):
            return 0
        
        score = 0
        
        maxT =  grid.getMaxTile()
        score = score + maxT*maxT*len(moves)
        
        n = grid.size
        
        for i in range(n):
            for j in range(n):
                curr = grid.getCellValue((i,j))
                if(curr==0):
                    if(i>0) & (i<n-1):
                        prevT = grid.getCellValue((i-1,j))
                        nextT = grid.getCellValue((i+1,j))
                        if(nextT==0) | (prevT==0):
                            continue
                        if(prevT==nextT):
                            score = score + prevT*prevT
                        x = prevT/nextT
                        if(x<=4) | (x>=0.25):
                            score = score + maxT*5
                        else:
                            score = score - maxT*5
                    else:
                        score = score + maxT*(n-i)*(n-j)
                    if(j>0) & (j<n-1):
                        prevT = grid.getCellValue((i,j-1))
                        nextT = grid.getCellValue((i,j+1))
                        if(nextT==0) | (prevT==0):
                            continue
                        if(prevT==nextT):
                            score = score + prevT*prevT
                        x = prevT/nextT
                        if(x<=4) | (x>=0.25):
                            score = score + maxT*5
                        else:
                            score = score - maxT*5
                    else:
                        score = score + maxT
                else:
                    score = score + curr*curr*2
                    if(i>0):
                        prevT = grid.getCellValue((i-1,j))
                        x = prevT/curr
                        if(x>1):
                            score = score - prevT*prevT
                        elif(x==1):
                            score = score + curr*curr
                        else:
                            score = score + prevT*prevT
                    if(j>0):
                        prevT = grid.getCellValue((i,j-1))
                        x = prevT/curr
                        if(x>1):
                            score = score - prevT*prevT
                        elif(x==1):
                            score = score + curr*curr
                        else:
                            score = score + prevT*prevT
        return score




