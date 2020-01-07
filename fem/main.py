from fem.components import IntegrationPoints
from fem.globaldata import GlobalData
from fem.grid import Gird
from fem.uelement import UniversalElement
import numpy as np
import math

# integration_points = IntegrationPoints(np.array([(-0.77, 5/9), (0, 8/9), (0.77, 5/9)]))
integration_points = IntegrationPoints(np.array([(-1 / math.sqrt(3), 1), (1 / math.sqrt(3), 1)]))
edges_integration_points = np.array([(-1 / math.sqrt(3), 1), (1 / math.sqrt(3), 1)])
k = 30
c = 700
ro = 7800
alpha = 25

global_data = GlobalData(integration_points, edges_integration_points, k, c, ro, alpha)

grid = Gird(0.1, 0.1, 4, 4)
grid.create_grid()
x = []
for element in grid.elements:
    x.append(UniversalElement(element, global_data))
    print("Element " + str(element.id))
    print("H matrix:")
    print(element.H_matrix)
    print("C matrix:")
    print(element.C_matrix)

all_H_matrix = np.array([[x[6], x[7], x[8]], [x[3], x[4], x[5]], [x[0], x[1], x[2]]])



pass
