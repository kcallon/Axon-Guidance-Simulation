from math import floor, dist
from typing import List, Tuple

class GridSquare:
    def __init__(self) -> None:
        self.netrin = 0
        self.shh = 0
        self.slit = 0
        self.targetLigand = 0
        self.hasAxonShaft = False

class Environment:
    def __init__(self, netrin_input, slit_input, shh_input) -> None:
        self.geneConfig = {
            'netrin': netrin_input,
            'slit': slit_input,
            'shh': shh_input,
            'targetLigand': True
        }

        self.middle = 0.2 #the fraction of cells considered the midline
        self.nrows = 10 + 1 #the number of rows in the standard grid, plus one for the synaptic target
        self.ncols = 10
        self.grid = []
        self.left_midline_edge = floor((0.5 - self.middle / 2) * self.ncols)
        self.right_midline_edge = floor((0.5 + self.middle / 2) * self.ncols)
        self.synapticTargetLocation = (0, self.right_midline_edge + 1 )

        self.initialConcentrations = {
            'netrin': 1,
            'slit': 1,
            'shh': 1,
            'targetLigand': 1
        }
        self.decayRates = {
            'netrin': 0.3,
            'slit': 0.3,
            'shh': 0.3,
            'targetLigand': 0.1
        }

    def inBounds(self, x, y, full = False) -> bool:
        """ returns true if the x, y is within bounds.
        full refers to the full grid (including the secret row with the synaptic target)
        if full=True, the 0th row is valid
        if full=False, the 0th row is invalid
        Args:
            x (int): the x-coordinate
            y (int): the y-coordinate
            full (bool, optional): Defaults to False.

        Returns:
            bool: if the x, y is within the grid 
        """
        x_valid = 0 if full else 1 
        return x >= x_valid and x < self.nrows and y >= 0 and y < self.ncols

    def calibrateGrid(self):
        def concentration(a: Tuple, x: Tuple, rate: float) -> float:
            """ calculates the concentration at x given the initial concentration at location a and a decay rate

            Args:
                a (Tuple): a tuple of (x, y, concentration)
                x (Tuple): a tuple of (x, y) to determine the concentation at 
                rate (float): the decay rate of the concentration

            Returns:
                float: the concentration at x
            """
            C_0 = a[2]
            d = dist(a[0:2], x)
            return C_0 * (rate ** d)     

        def placeSynapticTarget(x, y):
            """Procedural function to place the synaptic target

            Args:
                x : 
                y (_type_): _description_
            """
            row = []
            for j in range(self.ncols):
                square = GridSquare()
                if j == y:
                    square.targetLigand = self.initialConcentrations['targetLigand']
                row.append(square)
            self.grid.insert(x, row)

        def createStandardGrid():
            for i in range(1, self.nrows):
                row = []
                for j in range(self.ncols):
                    square = GridSquare()
                    if self.inMidline(0, j) == "left":
                        edge = (0, self.left_midline_edge, self.initialConcentrations['netrin'])
                        square.netrin = concentration(edge, (0, j), self.decayRates['netrin'])

                        edge = (0, self.left_midline_edge, self.initialConcentrations['shh'])
                        square.shh = concentration(edge, (0, j), self.decayRates['shh'])
                    elif self.inMidline(0, j) == "right":
                        edge = (0, self.right_midline_edge, self.initialConcentrations['netrin'])
                        square.netrin = concentration(edge, (0, j), self.decayRates['netrin'])

                        edge = (0, self.right_midline_edge, self.initialConcentrations['shh'])
                        square.shh = concentration(edge, (0, j), self.decayRates['shh'])
                    elif self.inMidline(0, j) == "middle":
                        square.slit = self.initialConcentrations['slit']
                        square.netrin = self.initialConcentrations['netrin']
                        square.shh = self.initialConcentrations['shh']
                    else:
                        print("something is wrong")

                    row.append(square)
                self.grid.append(row)

        def diffuseTargetLigand(x, y, r):
            # go in a circle around x, y
            # radially diffuse the targetLigand 
            synapticTarget = (self.synapticTargetLocation[0], \
                                self.synapticTargetLocation[1], \
                                self.initialConcentrations['targetLigand'])
            for i in range(x - r, x + r):
                for j in range(y - r, y + r):
                    if self.inBounds(i, j, full=True):
                        square = self.getGridSquare(i, j, full=True)
                        square.targetLigand = concentration(synapticTarget, (i, j), self.decayRates['targetLigand'])



        
        createStandardGrid()
        placeSynapticTarget(self.synapticTargetLocation[0], self.synapticTargetLocation[1])
        diffuseTargetLigand(self.synapticTargetLocation[0], self.synapticTargetLocation[1], self.nrows)

            
    def getGridSquare(self, x, y, full=False) -> GridSquare:
        """get the gridSquare at x, y
        """
        if self.inBounds(x, y, full=full):
            return self.grid[x][y]
        print("warning: trying to access outside of the grid")
        return None
        
    
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

    

    def print(self, midline = False, conc=False):
        """debug function 

        Args:
            conc (bool, optional): if you want to see the concentrations of the cells. Defaults to False.
        """
        if not conc:
            for i in range(self.nrows):
                row = self.grid[i]
                r = []
                if i == 0:
                    r = ['T' if j.targetLigand == self.initialConcentrations['targetLigand'] else 'x' if j.hasAxonShaft else ' ' for j in row]
                else: 
                    r = ['x' if j.hasAxonShaft else ' ' for j in row ]
                if midline:
                    r.insert(self.left_midline_edge, '|')
                    r.insert(self.right_midline_edge + 1, '|')
                print(''.join(r))
                if i == 0:
                    print(''.join(['-' for j in row]) + "--")
        else:
            for row in self.grid:
                # r = [f'[{j.netrin}, {j.shh}, {j.slit}, {j.targetLigand}]' for j in row]
                r = [f'[{j.targetLigand:.1e}]' for j in row]
                if midline:
                    r.insert(self.left_midline_edge, '|')
                    r.insert(self.right_midline_edge + 1, '|')
                print(''.join(r))



        