# Axon-Guidance-Simulation

A project by Kate Callon and Hannah Cussen for Stanford CS221's final project.

# Setup

The first time, run `conda env create -f environment.yml -p ./axon-env` to create the conda environment on your machine.

To develop, use `conda activate ./axon-env` to start the conda environment.

# Running the Simulation

To run the simulation from the root directory, first make sure you are in the conda environment. Then, run the command

```
python code/sim.py configuration_inputs/CONFIG_FILE -v
```

Where CONFIG_FILE is one of the .yml files in the configuration_inputs directory. `-v` is an optional argument allowing verbose output.

## Other Scripts

### Understanding the Environment: Visualizing Concentrations

To use the Jupyter Notebook `concentration_visualization/visualize_concentrations.ipynb`, run the script:

```
python code/dump_concentrations.py configuration_inputs/CONFIG_FILE
```

This script dumps the concentrations of every ligand into the corresponsding `.csv` in the `concentration_visualization` directory. This is useful for debugging concentrations, especially if your configuration file is turning some of the ligands off.

### Understanding Simulation Output

To run the simulation on all files in `configuration_inputs`, run the script:

```
python code/run_sims_compare_output.py
```

This script creates the `configuration_outputs` directory. Then, it runs the simulation on every config file in `configuration_inputs` and places the output into a file in the `configuration_outputs`. Finally, it finds the Levenshtein distance between the simulation output and the corresponding ground truth file in `examples` and logs that to `configuration_outputs/log.txt`.
