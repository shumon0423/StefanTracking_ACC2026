import numpy as np
from parameters import params

class ControlBase:
    """Abstract base class for control strategies"""
    def apply_control(self, s, u_t, v_t, h):
        """Override this method in subclasses"""
        raise NotImplementedError("Control strategy must implement apply_control")

class ControlStrategy1(ControlBase):
    """First control strategy"""
    def __init__(self):
        self.c_1 = params["control"]["c_1"]
        self.kc = params["physical"]["kc"]
        self.alp = params["physical"]["kc"] / params["physical"]["rho"] / params["physical"]["cp"]
        self.beta = params["physical"]["kc"] / params["physical"]["rho"] / params["physical"]["Hf"]
        self.N = params["simulation"]["N"]

    def apply_control(self, s, s_tilde, u_t, v_t):
        """Modify heat flux at each step"""
        dx = s / self.N
        return -self.kc * self.c_1 * (dx * np.trapz(u_t) / self.alp + s_tilde / self.beta)

class ControlStrategy2(ControlBase):
    """Second control strategy"""
    def __init__(self):
        self.c_1 = params["control"]["c_1"]
        self.c_2 = params["control"]["c_2"]
        self.kc = params["physical"]["kc"]
        self.epsilon = params["physical"]["epsilon"]
        self.alp = params["physical"]["kc"] / params["physical"]["rho"] / params["physical"]["cp"]
        self.beta = params["physical"]["kc"] / params["physical"]["rho"] / params["physical"]["Hf"]
        self.N = params["simulation"]["N"]

    def apply_control(self, s, s_tilde, u_t, v_t):
        """Alternative control logic"""
        dx = s / self.N
        return -self.kc * (self.c_2 * dx * np.trapz(u_t) / self.alp 
                           + self.c_1 * s_tilde / self.beta
                           + self.c_2 * self.epsilon * v_t / self.beta)
    
