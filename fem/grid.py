from fem.components import Node, Element


class Gird:
    def __init__(self, width: float, height: float, nodes_horizontally: int, nodes_vertically: int):
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
        self.nodes = []
        self.elements = []

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
            self.nodes.append(Node(node_id, x*self.element_width, y*self.element_height, boundary_condition=bc))

        for element_id in range(self.elements_number):
            nodes = self.generate_adjacent_nodes_for_element(element_id)
            self.elements.append(Element(element_id, nodes))

    def generate_adjacent_nodes_for_element(self, element_id: int):
        adjacent_nodes = [self.nodes[element_id + (element_id // self.elements_vertically)],
                          self.nodes[element_id + (element_id // self.elements_vertically) + 1],
                          self.nodes[element_id + (element_id // self.elements_vertically) + self.nodes_vertically + 1],
                          self.nodes[element_id + (element_id // self.elements_vertically) + self.nodes_vertically]]

        return adjacent_nodes
