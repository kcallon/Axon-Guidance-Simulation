from axon import Axon
from environment import Environment

def main():
    env = Environment()

    env.calibrateGrid()
    env.print(midline=True)

    for j in range(env.ncols - 3):
        square = env.getGridSquare(1, j)
        square.hasAxonShaft = True
    square = env.getGridSquare(0, )
    square.hasAxonShaft = True
    print()
    env.print(midline=True)

if __name__ == "main":
    main()