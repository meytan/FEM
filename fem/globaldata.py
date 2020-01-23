

class GlobalData:
    def __init__(self, integration_points, edges_integration_points, k: float, c: float, ro: float, alpha: float,
                 temperature_oo: float, time: float, dt: float, initial_temperature: float):
        self.k = k
        self.integration_points = integration_points
        self.edges_integration_points = edges_integration_points
        self.c = c
        self.ro = ro
        self.alpha = alpha
        #temperatura otoczenia
        self.temerature_oo = temperature_oo
        self.dt = dt
        self.time = time
        self.initial_temperature = initial_temperature
