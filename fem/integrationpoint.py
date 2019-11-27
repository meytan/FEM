import numpy as np


class IntegrationPoint:
    def __init__(self, eta: float, ksi: float, weight: float):
        self.eta = eta
        self.ksi = ksi
        self.weight = weight
        self.shape_function = self.generate_shape_functions()
        self.shape_functions_eta_derivative = self.generate_shape_functions_eta_derivative()
        self.shape_functions_ksi_derivative = self.generate_shape_functions_ksi_derivative()
        self.jacobian = 0
        self.det_jacobian = 0
        self.inverse_jacobian = 0
        self.shape_functions_xy_derivatives = 0

    def generate_shape_functions(self) -> np.array:
        n1 = 0.25 * (1 - self.ksi) *(1 - self.eta)
        n2 = 0.25 * (1 + self.ksi) *(1 - self.eta)
        n3 = 0.25 * (1 + self.ksi) *(1 + self.eta)
        n4 = 0.25 * (1 - self.ksi) *(1 + self.eta)
        return np.array([n1, n2, n3, n4])

    def generate_shape_functions_ksi_derivative(self) -> np.array:
        n1_ksi = -0.25 * (1 - self.eta)
        n2_ksi = 0.25 * (1 - self.eta)
        n3_ksi = 0.25 * (1 + self.eta)
        n4_ksi = -0.25 * (1 + self.eta)
        return np.array([n1_ksi, n2_ksi, n3_ksi, n4_ksi])

    def generate_shape_functions_eta_derivative(self) -> np.array:
        n1_eta = -0.25 * (1 - self.ksi)
        n2_eta = -0.25 * (1 + self.ksi)
        n3_eta = 0.25 * (1 + self.ksi)
        n4_eta = 0.25 * (1 - self.ksi)
        return np.array([n1_eta, n2_eta, n3_eta, n4_eta])

    def set_jacobian(self, jacobian: np.matrix):
        self.jacobian = jacobian
        self.det_jacobian = np.linalg.det(jacobian)
        self.inverse_jacobian = np.linalg.inv(jacobian)

    def generate_shape_functions_xy_derivatives(self):
        shape_functions_etaksi_derivatives = np.matrix(
            [self.shape_functions_eta_derivative, self.shape_functions_ksi_derivative])
        self.shape_functions_xy_derivatives = self.inverse_jacobian * shape_functions_etaksi_derivatives
