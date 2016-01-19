# Tile problem (an improved representation)
#
# Author: Michel Gagnon
#         michel.gagnon@polytml.ca
#
# The problem consists in a grid that should be covered by tiles.
# Some squares in the grid are obstacles that cannot be covered by a tile
# Three types of tile can be used: a single square, a 2X2 square, or a rectangle
# that covers two adjacent squares.
# We must cover the grid by minimizing the number of tiles

from node import *
from state import *
from breadthfirst_search import *
from depthfirst_search import *
from bestfirst_search import *
from astar_search import *
from iterative_deepening_astar import *
from branch_and_bound import *

import numpy as np
import copy

class TileState(State):
    def __init__(self,(dimX,dimY),obstacles):
        self.dimensions = (dimX,dimY)
        self.obstacles = obstacles
        self.grid = self._createGrid(dimX,dimY,obstacles)
        self.counter = 0  # Will be used to identify each tile with a different id
        self.emptyCells = dimX*dimY - len(obstacles)

    def equals(self,state):
        return self.grid == state.grid

    def show(self):
        for row in self.grid:
            for cell in row:
                if cell == -1:
                    print '**',
                else:
                    print '{:2}'.format(cell),
            print

    def executeAction(self,(action,x,y)):
        self.counter += 1
        if action == 'addSmallSquare':
            self.grid[x][y] = self.counter
            self.emptyCells -= 1
        elif action == 'addBigSquare':
            self.grid[x][y] = self.counter
            self.grid[x+1][y] = self.counter
            self.grid[x][y+1] = self.counter
            self.grid[x+1][y+1] = self.counter
            self.emptyCells -= 4
        elif action == 'addHorizontalRectangle':
            self.grid[x][y] = self.counter
            self.grid[x][y+1] = self.counter
            self.emptyCells -= 2
        elif action == 'addVerticalRectangle':
            self.grid[x][y] = self.counter
            self.grid[x+1][y] = self.counter
            self.emptyCells -= 2
        else:
            raise Exception('Erreur')

    def possibleActions(self):
        actions = []
        (dimX,dimY) = self.dimensions
        for i in range(dimX):
            for j in range(dimY):
                if self.grid[i][j] == 0:
                    actions.append(('addSmallSquare',i,j))
                    if j < dimY-1 and self.grid[i][j+1] == 0:
                        actions.append(('addHorizontalRectangle',i,j))
                    if i < dimX-1 and self.grid[i+1][j] == 0:
                        actions.append(('addVerticalRectangle',i,j))
                    if i < dimX-1 and j < dimY-1 and self.grid[i][j+1] == 0 and self.grid[i+1][j] == 0 and self.grid[i+1][j+1] == 0:
                        actions.append(('addBigSquare',i,j))
        return actions

    def cost(self,(action,i,j)):
        if action == 'addSmallSquare':
            return 4
        elif action == 'addBigSquare':
            return 1
        else:
            return 2

    def isGoal(self):
        return self.emptyCells == 0


    def heuristic(self):
        return self._heuristic2()



    ### Private methods ####

    def _heuristic1(self):
        costBigSquare =  self.emptyCells / 4
        rest = self.emptyCells % 4
        addCost = [0,4,2,6]
        return costBigSquare + addCost[rest]

    # This heuristic counts the number of squares in each isolated region,
    # computes the value of heuristic1 for each region and returns the sum 
    # of these values
    def _heuristic2(self):
        isolatedRegions = self._isolatedRegions()
        value = 0
        for r in isolatedRegions:
            costBigSquare = r / 4
            rest = r % 4
            addCost = [0,4,2,6]
            value += costBigSquare + addCost[rest]
        return value

    # Returns a list of values that correspond to the number of empty cells in each 
    # isolated region of the grid
    def _isolatedRegions(self):
        grid = copy.deepcopy(self.grid)
        regions = []
        (dimX,dimY) = self.dimensions
        for i in range(dimX):
            for j in range(dimY):
                r = self._findRegion(grid,i,j)
                if r > 0:
                    regions.append(r)
        return regions

    # If cells at position (i,j) is empty, we count the number of empty cells in its region
    def _findRegion(self,grid,i,j):
        if grid[i][j] != 0:
            return 0
        else:
            return self._countCellsRegion(grid,i,j)

    # Count the number of empty cells in some isolated region of the grid, starting from position (i,j)
    def _countCellsRegion(self,grid,i,j):
        if i >= 0 and j >= 0 and i < self.dimensions[0] and j < self.dimensions[1] and grid[i][j] == 0:
            grid[i][j] = 1
            return (1 + self._countCellsRegion(grid,i+1,j) 
                     + self._countCellsRegion(grid,i,j+1) 
                     + self._countCellsRegion(grid,i-1,j) 
                     + self._countCellsRegion(grid,i,j-1))
        else:
            return 0
            

    def _createGrid(self,dimX,dimY,obstacles):
        grid = [ [0 for y in range(dimY)] for x in range(dimX) ]
        for i in range(dimX):
            for j in range(dimY):
                if (i,j) in obstacles:
                    grid[i][j] = -1
        return grid



#solution = iterative_deepening_astar_search(TileState((3,4),[(1,2)]))
solution = branch_and_bound_search(TileState((3,4),[(1,2)]))

solution.state.show()
print solution.extractSolution()

