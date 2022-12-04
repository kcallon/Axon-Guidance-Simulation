import utils 
import os

def main():
    inputdir = '../configuration_inputs'
    outputdir = '../configuration_outputs'
    exampledir = '../examples'
    logfile = f'{outputdir}/log.txt'
    configs = os.listdir(inputdir)
    os.makedirs(outputdir, exist_ok=True)

    with open(logfile, 'w') as log:
        for config in configs:
            name = os.path.basename(config).split('_')[0]
            inputfile = f'{inputdir}/{config}'
            outputfile = f'{outputdir}/{name}'
            print(f'running sim on {inputfile} with name {name}')
            os.system(f'python sim.py {inputfile} > {outputfile}')

            edit_dist = utils.edit_distance(f'{exampledir}/{name}', outputfile)
            log.write(f'{name}\t{edit_dist}\n')



if __name__ == '__main__':
    main()