import numpy as np
from parameters import params

class CheckBase:
    def __init__(self):

        # Physical parameters
        self.epsilon = params["physical"]["epsilon"]
        self.alp = params["physical"]["kc"] / params["physical"]["rho"] / params["physical"]["cp"]
        self.beta = params["physical"]["kc"] / params["physical"]["rho"] / params["physical"]["Hf"]
        
        # Simulation parameters
        self.N = params["simulation"]["N"]
        self.dt = params["simulation"]["dt"]

        # Control parameters
        self.s_r = params["control"]["sr"]
        self.c_1 = params["control"]["c_1"]
        self.c_2 = params["control"]["c_2"]

        # Initial conditions
        self.s0 = params["initial"]["s_0"]
        self.v0 = params["initial"]["v_0"]
        self.u0max = params["initial"]["u_0_max"]
        self.u0 = np.array([self.u0max * (1 - i / self.N) for i in range(self.N + 1)])

    def stability(self):
        """Check Neumann stability condition"""
        test = self.s0**2 / (2 * self.alp) / self.N**2 - self.dt
        return test > 0
    
    def setpoint(self):
        """Check setpoint condition"""
        test = self.s_r - ( self.s0 + self.epsilon * self.v0 + self.beta * self.s0 * np.trapz(self.u0) / self.N / self.alp )
        return test > 0
    
    def gain(self):
        """Check gain condition"""
        if self.c_1 <= 0 or self.c_2 < self.c_1:
            test = -1
        else:
            cond = self.alp * self.epsilon - 12 * self.s_r**2
            s_r_under = self.s0 + self.epsilon * self.v0 + self.beta * self.s0 * np.trapz(self.u0) / self.N / self.alp
            c_2_bar = self.c_1 * (self.s_r - s_r_under) / (s_r_under - self.s0)
            if cond >= 0: 
                test = self.c_1 + c_2_bar - self.c_2
            else:
                test = self.c_1 + min(c_2_bar, (self.alp * self.epsilon * self.c_1 + self.alp) / (12 * self.s_r * self.s_r - self.alp * self.epsilon)) - self.c_2
        return test > 0