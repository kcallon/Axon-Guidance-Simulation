from axon import Axon
from environment import Environment

N_SIMULATION_STEPS = 10

def main():
    env = Environment()

    env.calibrateGrid()
    axon = Axon()

    x, y = 1, 0
    for i in range(N_SIMULATION_STEPS):
        env.getGridSquare(x, y).hasAxonShaft = True
        move = axon.chooseAction(env, x, y)
        # axon.modulateGenes(env.getGridSquare(x, y))
        x, y = move
        env.print(midline=True)
        print()

if __name__ == "__main__":
    main()