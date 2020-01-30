import numpy as np

from fem.globaldata import GlobalData
from fem.grid import Grid

class Aggregator:
    def __init__(self, grid: Grid, global_data: GlobalData):
        self.grid = grid
        self.global_data = global_data
        self.global_H_matrix = np.zeros((grid.nodes_number, grid.nodes_number))
        self.global_C_matrix = np.zeros((grid.nodes_number, grid.nodes_number))
        self.global_P_vector = np.zeros(grid.nodes_number)
        self.global_temperature_vector= None

    def aggregate(self):
        for element in self.grid.elements:
            for x in enumerate(element.get_transpose_indexes_for_global_matrix()):
                for y in enumerate(x[1]):
                    self.global_H_matrix[y[1][0]][y[1][1]] += (element.H_matrix + element.Hbc_matrix)[x[0]][y[0]]
                    self.global_C_matrix[y[1][0]][y[1][1]] += element.C_matrix[x[0]][y[0]] 
            for x in enumerate([node.id for node in element.adjacent_nodes]):
                self.global_P_vector[x[1]] += element.P_vector[x[0]]

    def start_simulation(self):
        print("Time     Min. Temp.          Max. Temp.")
        for time in range(0, self.global_data.time, self.global_data.dt):
            self.global_temperature_vector = [node.temperature for node in self.grid.nodes]
            c_matrix_dt = self.global_C_matrix / self.global_data.dt
            new_H_matrix = np.matrix(self.global_H_matrix + c_matrix_dt)
            c_matrix_dt_temperature = np.matrix(self.global_temperature_vector) * np.matrix(c_matrix_dt)
            new_P_vector = np.matrix(self.global_P_vector) + c_matrix_dt_temperature
            new_temperatures = np.array(new_P_vector * np.linalg.inv(new_H_matrix))
            print(f'{time+self.global_data.dt}: {new_temperatures.min()} --- {new_temperatures.max()}')
            for node in enumerate(self.grid.nodes):
                node[1].temperature = new_temperatures[0][node[0]]
            pass

