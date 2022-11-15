from axon import Axon
from environment import Environment

env = Environment()

env.calibrateGrid()
env.print(midline=True, conc=True)