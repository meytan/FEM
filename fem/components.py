import math
import numpy as np
from typing import List
from fem import integrationpoint


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


class Element:
    def __init__(self, id: int, adjacent_nodes: List[Node]):
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


class IntegrationPoints:
    # Takes values in format [(point value, weight)]
    def __init__(self, values):
        self.integration_points = []
        for eta in values:
            for ksi in values:
                self.integration_points.append(integrationpoint.IntegrationPoint(eta[0], ksi[0], eta[1] * ksi[1]))

    def get(self):
        return self.integration_points


class GlobalData:
    def __init__(self, integration_points: IntegrationPoints, k: float, c: float, ro: float, alpha: float):
        self.k = k
        self.integration_points = integration_points
        self.c = c
        self.ro = ro
        self.alpha = alpha
