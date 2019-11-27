from fem.components import IntegrationPoints, GlobalData
from fem.grid import Gird
from fem.uelement import UniversalElement
import numpy as np
import math

# integration_points = IntegrationPoints(np.array([(-0.77, 5/9), (0, 8/9), (0.77, 5/9)]))
integration_points = IntegrationPoints(np.array([(-1 / math.sqrt(3), 1), (1 / math.sqrt(3), 1)]))
k = 30
c = 700
ro = 7800
alpha = 25

global_data = GlobalData(integration_points, k, c, ro, alpha)

grid = Gird(0.1, 0.1, 4, 4)
grid.create_grid()
x = []
for element in grid.elements:
    x.append(UniversalElement(element, global_data))

pass
