import numpy as np
from parameters import params


class ModelBase:
    """Abstract base class for model types"""
    def compute_update_law(self, s, u, v):
        """Override this method in subclasses"""
        raise NotImplementedError("Model type must implement compute_update_law")

class StefanSecondOrderModel(ModelBase):
    """Defines the mathematical model for melting zinc."""
    
    def __init__(self):
        self.kc = params["physical"]["kc"]  # Thermal conductivity
        self.alp = params["physical"]["kc"] / params["physical"]["rho"] / params["physical"]["cp"]
        self.beta = params["physical"]["kc"] / params["physical"]["rho"] / params["physical"]["Hf"]
        self.epsilon = params["physical"]["epsilon"]
        self.N = params["simulation"]["N"]
    
    def compute_update_law(self, s, u, v, qc):
        """
        Computes the update law for the system.
        :param s: Current interface position
        :param u_profile: Temperature profile
        :param v: Interface velocity
        :return: Updated velocity and interface position
        """
        du_dt = np.zeros(self.N + 1) 
        dx = s / self.N
        ds_dt = v
        # Update temperature
        ufic = u[1] + 2 * dx * qc / self.kc
        du_dt[0] = (self.alp / dx / dx) * (u[1] - 2 * u[0] + ufic)

        for i in range(1, self.N):
            du_dt[i] = (self.alp / dx / dx) * (u[i + 1] - 2 * u[i] + u[i - 1]) + ds_dt * i * (u[i + 1] - u[i - 1]) / (2 * s)

        du_dt[self.N] = 0
        # Compute new velocity based on temperature gradient
        dv_dt = -v / self.epsilon - self.beta * (3 * u[self.N] - 4 * u[self.N-1] + u[self.N-2]) / (2 * dx ) / self.epsilon

        return du_dt, ds_dt, dv_dt
