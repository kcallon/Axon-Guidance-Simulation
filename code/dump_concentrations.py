import sys
import yaml
from environment import Environment

def main(config_file):
    env_dict = config_file['envInput']
    netrin, slit, shh = env_dict['netrin'], env_dict['slit'], env_dict['shh']

    env = Environment(netrin, slit, shh)

    original_stdout = sys.stdout
    
    env.calibrateGrid()
    ligands = ['netrin', 'slit', 'shh', 'target']

    for ligand in ligands:
        with open(f'concentration_visualization/{ligand}.csv', 'w') as f:
            sys.stdout = f
            env.print(midline=False, conc=True, ligand = ligand)

    sys.stdout = original_stdout

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