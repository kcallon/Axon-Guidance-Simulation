import sys
import yaml
from axon import Axon
from environment import Environment

def main(config_file, verbose=False):
    gene_dict = config_file['geneInput']
    env_dict = config_file['envInput']
    netrin, slit, shh = env_dict['netrin'], env_dict['slit'], env_dict['shh']
    comm, dcc, robo1, robo2 = gene_dict['Comm'], gene_dict['DCC'], gene_dict['Robo1'], gene_dict['Robo2']
    env = Environment(netrin, slit, shh)

    env.calibrateGrid()
    axon = Axon(comm, dcc, robo1, robo2)

    x, y = env.nrows - 1, 0
    sim_step = 0
    while sim_step < env.max_axon_length:
        x, y = axon.chooseAction(env, x, y, verbose=verbose)
        env.getGridSquare(x, y, full=True).hasAxonShaft = True
        axon.modulateGenes(env.getGridSquare(x, y, full=True))

        if verbose:
            env.print(midline=True)
            print()

        sim_step += 1
        if x == 0: # end state
            break
    
    if verbose:
        print(f'end state - {"max axon length" if sim_step == env.max_axon_length else "crossed out of grid"} - reached!')
        print(f'total rewards gained: {axon.totalReward}')
    else:
        env.print(midline=True)
        

if __name__ == "__main__":
    arg_length = len(sys.argv)

    verbose = False
    if arg_length == 3:
        verbose = sys.argv[2] == '-v'

    if arg_length < 2:
        print("Configuraton file not specified. Please add to the command line argument.")
        exit(1)
    else:
        with open(sys.argv[1], "r") as ymlfile:
            try:
                cfg = yaml.safe_load(ymlfile)
            except yaml.YAMLError as exc:
                print(exc)
        main(cfg, verbose)
