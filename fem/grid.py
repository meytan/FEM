from fem.components import Node, Element
from typing import List

from fem.globaldata import GlobalData
from fem.uelement import UniversalElement


class Grid:
    def __init__(self, width: float, height: float, nodes_horizontally: int, nodes_vertically: int,
                 global_data: GlobalData):
        self.global_data = global_data
        self.width: float = width
        self.height: float = height
        self.nodes_horizontally: int = nodes_horizontally
        self.nodes_vertically: int = nodes_vertically
        self.element_width: float = self.width / (self.nodes_horizontally - 1)
        self.element_height: float = self.height / (self.nodes_vertically - 1)
        self.nodes_number: int = self.nodes_horizontally * self.nodes_vertically
        self.elements_number: int = (nodes_horizontally - 1) * (nodes_vertically - 1)
        self.elements_horizontally: int = nodes_horizontally - 1
        self.elements_vertically: int = nodes_vertically - 1
        self.nodes: List[Node] = []
        self.elements: List[Element] = []

    def create_grid(self):

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
            self.nodes.append(Node(node_id, x*self.element_width, y*self.element_height,
                                   self.global_data.initial_temperature, boundary_condition=bc))

        for element_id in range(self.elements_number):
            nodes = self.generate_adjacent_nodes_for_element(element_id)
            self.elements.append(Element(element_id, nodes))

    def generate_adjacent_nodes_for_element(self, element_id: int):

        adjacent_nodes = [self.nodes[element_id + (element_id // self.elements_vertically)],
                          self.nodes[element_id + (element_id // self.elements_vertically) + self.nodes_vertically],
                          self.nodes[element_id + (element_id // self.elements_vertically) + self.nodes_vertically + 1],
                          self.nodes[element_id + (element_id // self.elements_vertically) + 1]]
        return adjacent_nodes

    def process_elements(self):
        for element in self.elements:
            UniversalElement(element, self.global_data)

