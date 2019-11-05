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
