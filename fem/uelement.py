import numpy as np
from fem.components import Element
from fem.globaldata import GlobalData
from fem.integrationpoint import IntegrationPoint


class UniversalElement:

    def __init__(self, element: Element, global_data: GlobalData):
        self.element = element
        self.integration_points = global_data.integration_points
        self.H_matrix = np.zeros((4, 4))
        self.Hbc_matrix = np.zeros((4, 4))
        self.C_matrix = np.zeros((4, 4))
        self.P_vector = np.zeros(4)
        for integration_point in self.integration_points.get():
            self.generate_jacobian(integration_point)
            integration_point.generate_shape_functions_xy_derivatives()

            dndx = integration_point.shape_functions_xy_derivatives[0].transpose() * integration_point.shape_functions_xy_derivatives[0]
            dndy = integration_point.shape_functions_xy_derivatives[1].transpose() * integration_point.shape_functions_xy_derivatives[1]
            H = global_data.k * (dndx + dndy)
            self.H_matrix += H * integration_point.det_jacobian * integration_point.weight


            N_Nt = np.matrix(integration_point.shape_function).transpose() * integration_point.shape_function
            self.C_matrix += global_data.c * global_data.ro * N_Nt * integration_point.det_jacobian * integration_point.weight

        if self.element.boundary_condition:
            for edge in enumerate(self.element.edges):
                if edge[1].boundary_condition:
                    self.Hbc_matrix += edge[1].calculate_hbc(global_data, edge[0])
        for edge in self.element.edges:
            res = edge.calculate_P_vector_entnry(global_data)
            self.P_vector += res

        self.element.set_h_matrix(self.H_matrix)
        self.element.set_hbc_matrix(self.Hbc_matrix)
        self.element.set_c_matrix(self.C_matrix)
        self.element.set_p_vector(self.P_vector)

    def generate_jacobian(self, integration_point: IntegrationPoint):
        x = np.array([node.x for node in self.element.adjacent_nodes])
        y = np.array([node.y for node in self.element.adjacent_nodes])

        x_eta = np.sum(x * integration_point.shape_functions_eta_derivative)
        y_ksi = np.sum(y * integration_point.shape_functions_ksi_derivative)
        x_ksi = np.sum(x * integration_point.shape_functions_ksi_derivative)
        y_eta = np.sum(y * integration_point.shape_functions_eta_derivative)

        integration_point.set_jacobian(np.matrix([[x_ksi, y_ksi], [x_eta, y_eta]]))
