import json
import time

from fem.aggregator import Aggregator
from fem.components import IntegrationPoints
from fem.globaldata import GlobalData
from fem.grid import Grid
import numpy as np
import math
start = time.time()

integration_points = IntegrationPoints(np.array([(-1 / math.sqrt(3), 1), (1 / math.sqrt(3), 1)]))
edges_integration_points = np.array([(-1 / math.sqrt(3), 1), (1 / math.sqrt(3), 1)])

# integration_points = IntegrationPoints(np.array([(-0.77, 5/9), (0, 8/9), (0.77, 5/9)]))
# edges_integration_points = np.array([(-math.sqrt(3/5), 5/9), (0, 8/9), (math.sqrt(3/5), 5/9)])


with open('data.json') as data_file:
    data = json.load(data_file)
    initial_temperature = data["initialTemperature"]
    simulation_time = data["time"]
    dt = data["timeStep"]
    temperature_oo = data["ambientTemperature"]
    alpha = data["alpha"]
    height = data["height"]
    width = data["width"]
    nodes_vertically = data["nodesVertically"]
    nodes_horizontally = data["nodesHorizontally"]
    c = data["specificHeat"]
    k = data["conductivity"]
    ro = data["density"]

global_data = GlobalData(integration_points, edges_integration_points, k, c, ro, alpha, temperature_oo, simulation_time, dt, initial_temperature)

grid = Grid(width, height, nodes_horizontally, nodes_horizontally, global_data)
grid.create_grid()
grid.process_elements()

aggregator = Aggregator(grid, global_data)
aggregator.aggregate()
aggregator.start_simulation()

end = time.time()
print(f'Simulation finished in {end - start}sec')
