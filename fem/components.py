import numpy as np

class Node:
    def __init__(self, id, x, y, boundary_condition=False, temperature=0):
        self.id = id
        self.x = x
        self.y = y
        self.temperature = temperature
        self.boundary_condition = boundary_condition


class Element:
    def __init__(self, id, adjacent_nodes):
        self.id = id
        self.adjacent_nodes = adjacent_nodes

class Universal_Element:
    def set_params(ksi, eta):
        self.ksi = ksi
        self.eta = eta
        
    def generate_shape_functions():
        n1 = 0.25 * (1 - self.ksi)*(1 - self.eta)
        n2 = 0.25 * (1 + self.ksi)*(1 - self.eta)
        n3 = 0.25 * (1 + self.ksi)*(1 + self.eta)
        n4 = 0.25 * (1 - self.ksi)*(1 + self.eta)
        n1_ksi = -0.25 * (1 - self.eta)
        n2_ksi = 0.25 * (1 - self.eta)
        n3_ksi = 0.25 * (1 + self.eta)
        n4_ksi = -0.25 * (1 + self.eta)
        n1_eta = -0.25 * (1 - self.ksi)
        n2_eta = -0.25 * (1 + self.ksi)
        n3_eta = 0.25 * (1 + self.ksi)
        n4_eta = 0.25 * (1 - self.ksi)
        self.shape_functions = np.array([n1, n2, n3 ,n4])
        self.shape_functions_ksi_derivative = np.array([n1_ksi, n2_ksi, n3_ksi ,n4_ksi])
        self.shape_functions_eta_derivative = np.array([n1_eta, n2_eta, n3_eta ,n4_eta])



class Gird:
    def __init__(self, width, height, nodes_horizontally, nodes_vertically):
        self.width = width
        self.height = height
        self.nodes_horizontally = nodes_horizontally
        self.nodes_vertically = nodes_vertically
        self.element_width = self.width / self.nodes_horizontally
        self.element_height = self.height / self.nodes_vertically
        self.nodes_number = self.nodes_horizontally * self.nodes_vertically
        self.elements_number = (nodes_horizontally - 1) * (nodes_vertically - 1)
        self.elements_horizontally = nodes_horizontally - 1
        self.elements_vertically = nodes_vertically - 1

    def create_grid(self):
        self.nodes = []
        self.elements = []
        for node_id in range(self.nodes_number):
            x = node_id // self.nodes_vertically
            y = node_id % self.nodes_vertically
            if (
                x == 0
                or y == 0
                or x == self.nodes_horizontally - 1
                or y == self.nodes_vertically - 1
            ):
                bc = True
            else:
                bc = False
            self.nodes.append(Node(node_id, x, y, boundary_condition=bc))

        for element_id in range(self.elements_number):
            nodes = self.generate_adjacent_nodes_for_element(element_id)
            self.elements.append(Element(element_id, nodes))

    def generate_adjacent_nodes_for_element(self, element_id):
        adjacent_nodes = []
        adjacent_nodes.append(
            element_id
            + (element_id // self.elements_vertically))

        adjacent_nodes.append(
            element_id
            + (element_id // self.elements_vertically) + 1)

        adjacent_nodes.append(
            element_id
            + (element_id // self.elements_vertically)
            + self.nodes_vertically
            + 1
        )

        adjacent_nodes.append(
            element_id
            + (element_id // self.elements_vertically)
            + self.nodes_vertically
        )
        return adjacent_nodes

