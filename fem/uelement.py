import numpy as np
from fem.components import Element, GlobalData
from fem.integrationpoint import IntegrationPoint


class UniversalElement:

    def __init__(self, element: Element, global_data: GlobalData):
        self.element = element
        self.integration_points = global_data.integration_points
        self.H_matrix = np.zeros((4, 4))
        self.C_matrix = np.zeros((4, 4))
        for integration_point in self.integration_points.get():
            self.generate_jacobian(integration_point)
            integration_point.generate_shape_functions_xy_derivatives()

            dndx = integration_point.shape_functions_xy_derivatives[0].transpose() * integration_point.shape_functions_xy_derivatives[0]
            dndy = integration_point.shape_functions_xy_derivatives[1].transpose() * integration_point.shape_functions_xy_derivatives[1]
            H = global_data.k * (dndx + dndy)
            self.H_matrix += H * integration_point.det_jacobian * integration_point.weight

            N_Nt = np.matrix(integration_point.shape_function).transpose() * integration_point.shape_function
            self.C_matrix += global_data.c * global_data.ro * N_Nt * integration_point.det_jacobian * integration_point.weight

        # if self.element.boundary_condition:
        #     for edge in self.element.edges:
        #         if edge.boundary_condition:
        #             if edge



    def generate_jacobian(self, integration_point: IntegrationPoint):
        x = np.array([node.x for node in self.element.adjacent_nodes])
        y = np.array([node.y for node in self.element.adjacent_nodes])

        x_eta = np.sum(x * integration_point.shape_functions_eta_derivative)
        y_ksi = np.sum(y * integration_point.shape_functions_ksi_derivative)
        x_ksi = np.sum(x * integration_point.shape_functions_ksi_derivative)
        y_eta = np.sum(y * integration_point.shape_functions_eta_derivative)

        integration_point.set_jacobian(np.matrix([[x_eta, y_eta], [x_ksi, y_ksi]]))
