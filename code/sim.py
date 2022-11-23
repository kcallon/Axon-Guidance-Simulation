from axon import Axon
from environment import Environment

N_SIMULATION_STEPS = 25

def main():
    env = Environment()

    env.calibrateGrid()
    axon = Axon()

    x, y = env.nrows - 1, 0
    for i in range(N_SIMULATION_STEPS):
        x, y = axon.chooseAction(env, x, y, verbose=True)
        env.getGridSquare(x, y, full=True).hasAxonShaft = True
        axon.modulateGenes(env.getGridSquare(x, y, full=True))
    
        env.print(midline=True)
        print()

        if (x, y) == env.synapticTargetLocation:
            print("end state")
            break
        

if __name__ == "__main__":
    main()