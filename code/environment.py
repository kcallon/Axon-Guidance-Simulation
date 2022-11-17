from math import floor
from typing import List

class GridSquare:
    def __init__(self) -> None:
        self.netrin = 0
        self.shh = 0
        self.slit = 0
        self.hasAxonShaft = False

class Environment:
    def __init__(self) -> None:
        self.geneConfig = {
            'netrin': True,
            'slit': True,
            'shh': True,
        }

        self.middle = 0.2 #the fraction of cells considered the midline
        self.nrows = 2
        self.ncols = 10
        self.grid = []

        self.initialConcentrations = {
            'netrin': 1,
            'slit': 1,
            'shh': 1,
        }

    def inBounds(self, x, y):
        return x >= 0 and x < self.nrows and y > 0 and y < self.ncols

    def calibrateGrid(self):
        def concentration(a, b, x ):
            return (a[1] - b[1]) / (a[0] - b[0]) * x

        for i in range(self.nrows):
            row = []
            for j in range(self.ncols):
                square = GridSquare()
                if self.inMidline(0, j) == "left":
                    left_edge = (0, 0) # (column, concentration) tuple
                    right_edge = ((0.5 - (self.middle / 2)) * self.ncols, self.initialConcentrations['netrin'])
                    square.netrin = concentration(left_edge, right_edge, j)

                    right_edge = ((0.5 - (self.middle / 2)) * self.ncols, self.initialConcentrations['shh'])
                    square.shh = concentration(left_edge, right_edge, j)

                elif self.inMidline(0, j) == "middle":
                    square.slit = self.initialConcentrations['slit']
                    square.netrin = self.initialConcentrations['netrin']
                    square.shh = self.initialConcentrations['shh']
                else:
                    pass

                row.append(square)
            self.grid.append(row)
            
    def getGridSquare(self, x, y) -> GridSquare:
        return self.grid[x][y]
    
    def inMidline(self, x, y) -> str:
        """Check if an x, y cell is in the midline
        Midline is the middle 20% of the Environment

        Args:
            x (int)
            y (int) 
        
        Returns: 
            string: "left", "right", or "middle"
        """
        assert x >= 0 and x < self.nrows, "x is not within the environment scope"
        assert y >= 0 and y < self.ncols, "y is not within the environment scope"

        left = y < (0.5 - (self.middle / 2)) * self.ncols
        right = y > (0.5 + (self.middle / 2)) * self.ncols - 1

        if left: return "left"
        elif right: return "right"
        return "middle"

    def getLegalMoves(self, x, y) -> List:
        actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        #apply actions to x, y tuple
        potential_successors = []
        for action in actions:
            potential_successors.append(tuple([sum(tup) for tup in zip((x, y), action)]))
        #if any are outside of the bounds of the grid, get rid of them
        successors = [a for a in potential_successors if self.inBounds(a[0], a[1]) and not self.getGridSquare(a[0], a[1]).hasAxonShaft]
        #if any already have an axon in them, get rid 
        return successors

    def print(self, midline = False, conc=False):
        """debug function 

        Args:
            conc (bool, optional): if you want to see the concentrations of the cells. Defaults to False.
        """
        if not conc:
            for row in self.grid:
                r = ['[x]' if j.hasAxonShaft else '[ ]' for j in row ]
                # r = ['[x]' if self.inMidline(0, j) == "middle" else '[ ]' for j in range(len(row)) ]
                if midline:
                    r.insert(floor((0.5 - (self.middle / 2)) * self.ncols), '|')
                    r.insert(floor((0.5 + (self.middle / 2)) * self.ncols) + 1, '|')
                print(''.join(r))
        else:
            for row in self.grid:
                r = [f'[{j.netrin}, {j.shh}, {j.slit}]' for j in row]
                if midline:
                    r.insert(floor((0.5 - (self.middle / 2)) * self.ncols), '|')
                    r.insert(floor((0.5 + (self.middle / 2)) * self.ncols) + 1, '|')
                print(''.join(r))



        