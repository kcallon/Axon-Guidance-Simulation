import sys
import yaml
from axon import Axon
from environment import Environment

MAX_AXON_LENGTH = 25


def main(config_file):
    gene_dict = config_file['geneInput']
    env_dict = config_file['envInput']
    netrin, slit, shh = env_dict['netrin'], env_dict['slit'], env_dict['shh']
    comm, dcc, robo = gene_dict['Comm'], gene_dict['DCC'], gene_dict['Robo']
    env = Environment(netrin, slit, shh)

    env.calibrateGrid()
    axon = Axon(comm, dcc, robo)

    x, y = env.nrows - 1, 0
    for i in range(MAX_AXON_LENGTH):
        x, y = axon.chooseAction(env, x, y, verbose=True)
        env.getGridSquare(x, y, full=True).hasAxonShaft = True
        axon.modulateGenes(env.getGridSquare(x, y, full=True))
    
        env.print(midline=True)
        print()

        if x == 0:
            break
    # env.print(midline=True, conc=True)
        

if __name__ == "__main__":
    arg_length = len(sys.argv)
    if arg_length < 2:
        print("Configuraton file not specified. Please add to the command line argument.")
        exit(1)
    else:
        with open(sys.argv[1], "r") as ymlfile:
            try:
                cfg = yaml.safe_load(ymlfile)
            except yaml.YAMLError as exc:
                print(exc)
        main(cfg)
