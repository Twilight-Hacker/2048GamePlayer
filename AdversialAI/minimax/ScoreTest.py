from PlayerAI import PlayerAI
from Grid import Grid
from Displayer import Displayer
from random import randint
from math import pow

pl = PlayerAI()
display = Displayer()

def constr():
    
    grid = Grid(4)
    
    n=grid.size
    
    for i in range(n):
        for j in range(n):
            tile = pow(2,randint(0,12))
            if(tile==1):
                tile=0
            grid.setCellValue((i,j), tile)
            
    return grid

def con2():
    grid = Grid(4)
    n=grid.size
    
    for i in range(n):
        for j in range(n):
            tile = pow(2,(i+j-1)*2)
            if(tile==1):
                tile=0
            if(tile>1024):
                tile = tile/2
            grid.setCellValue((i,j), tile)
            
    return grid
    

def main(numb):
    for i in xrange(numb):
        marks = []
        grid = constr()
        marks.append(pl.getGridScore(grid))
        display.display(grid)
        print "Marks: " + str(marks) + "\n\n"
        
def master():
        marks = []
        grid = con2()
        marks.append(pl.getGridScore(grid))
        display.display(grid)
        print "Marks: " + str(marks) + "\n\n"

def defined(grid):
        marks = []
        marks.append(pl.getGridScore(grid))
        display.display(grid)
        print "Marks: " + str(marks) + "\n\n"
    

main(10)

master()

gridd = Grid(4)

gridd.map = [ [0,2,4,4], [2,0,4,4], [16,8,32,2], [64,128,256,512] ] 
defined(gridd)
gridd.move(0) #UP 
defined(gridd)
gridd.move(1) #DOWN
defined(gridd)
gridd.move(2) #LEFT
defined(gridd)
gridd.move(3) #RIGHT 
defined(gridd)


