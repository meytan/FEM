import math
from typing import List
import numpy as np

from fem import integrationpoint
from fem.globaldata import GlobalData


class Node:
    def __init__(self, id, x, y, boundary_condition=False, temperature=0):
        self.id = id
        self.x = x
        self.y = y
        self.temperature = temperature
        self.boundary_condition = boundary_condition


class Edge:
    def __init__(self, node1: Node, node2: Node):
        self.nodes = [node1, node2]
        self.length = math.sqrt((node2.x - node1.x) ** 2 + (node2.y - node1.y) ** 2)
        if node1.boundary_condition is True and node2.boundary_condition is True:
            self.boundary_condition = True
        else:
            self.boundary_condition = False

#               pow 1
#       ----------------------
#  pow 0|                    |
#       |                    |pow 2
#       ----------------------
#               pow 3
#
    def calculate_hbc(self, global_data: GlobalData, pow: int):

        def n1(ksi):
            return 0.5 * (1-ksi)

        def n2(ksi):
            return 0.5 * (1+ksi)

        detJ = self.length / 2
        hbc = np.zeros((4, 4))

        tmp_matrix = np.zeros((2, 2))
        for integration_point in global_data.edges_integration_points:
            ksi = integration_point[0]
            weight = integration_point[1]
            shape_fun = np.matrix((n1(ksi), n2(ksi)))

            tmp_matrix += global_data.alpha * shape_fun.transpose() * shape_fun * weight

        tmp_matrix *= detJ

        if pow == 0:
            hbc[3][3] = tmp_matrix[0][0]
            hbc[3][0] = tmp_matrix[0][1]
            hbc[0][3] = tmp_matrix[1][0]
            hbc[0][0] = tmp_matrix[1][1]
        if pow == 1:

            hbc[2][2] = tmp_matrix[0][0]
            hbc[2][3] = tmp_matrix[0][1]
            hbc[3][2] = tmp_matrix[1][0]
            hbc[3][3] = tmp_matrix[1][1]
        if pow == 2:

            hbc[1][1] = tmp_matrix[0][0]
            hbc[1][2] = tmp_matrix[0][1]
            hbc[2][1] = tmp_matrix[1][0]
            hbc[2][2] = tmp_matrix[1][1]
        if pow == 3:

            hbc[0][0] = tmp_matrix[0][0]
            hbc[0][1] = tmp_matrix[0][1]
            hbc[1][0] = tmp_matrix[1][0]
            hbc[1][1] = tmp_matrix[1][1]

        return hbc


class Element:
    def __init__(self, id: int, adjacent_nodes: List[Node]):
        self.H_matrix = None
        self.C_matrix = None
        self.id = id
        self.adjacent_nodes = adjacent_nodes
        self.edges: List[Edge] = [
            Edge(adjacent_nodes[0], adjacent_nodes[1]),
            Edge(adjacent_nodes[1], adjacent_nodes[2]),
            Edge(adjacent_nodes[3], adjacent_nodes[2]),
            Edge(adjacent_nodes[0], adjacent_nodes[3])
        ]
        if [x for x in self.edges if x.boundary_condition is True]:
            self.boundary_condition = True
        else:
            self.boundary_condition = False

    def set_h_matrix(self, h_matrix):
        self.H_matrix = h_matrix

    def set_c_matrix(self, c_matrix):
        self.C_matrix = c_matrix


class IntegrationPoints:
    # Takes values in format [(point value, weight)]
    def __init__(self, values):
        self.integration_points = []
        for eta in values:
            for ksi in values:
                self.integration_points.append(integrationpoint.IntegrationPoint(eta[0], ksi[0], eta[1] * ksi[1]))

    def get(self):
        return self.integration_points


