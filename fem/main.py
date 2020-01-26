from fem.aggregator import Aggregator
from fem.components import IntegrationPoints
from fem.globaldata import GlobalData
from fem.grid import Grid
from fem.uelement import UniversalElement
import numpy as np
import math

#integration_points = IntegrationPoints(np.array([(-0.77, 5/9), (0, 8/9), (0.77, 5/9)]))
integration_points = IntegrationPoints(np.array([(-1 / math.sqrt(3), 1), (1 / math.sqrt(3), 1)]))
edges_integration_points = np.array([(-1 / math.sqrt(3), 1), (1 / math.sqrt(3), 1)])
#edges_integration_points = np.array([(-math.sqrt(3/5), 5/9), (0, 8/9), (math.sqrt(3/5), 5/9)])

k = 25
c = 700
ro = 7800
alpha = 300
temperature_oo = 1200
initial_temperature = 100
time = 500
dt = 50

global_data = GlobalData(integration_points, edges_integration_points, k, c, ro, alpha, temperature_oo, time, dt, initial_temperature)

grid = Grid(0.1, 0.1, 4, 4, global_data)
grid.create_grid()
grid.process_elements()

aggregator = Aggregator(grid, global_data)
aggregator.aggregate()
aggregator.start_simulation()


print(1)
