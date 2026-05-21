import numpy as np
from parameters import params
import math

class StefanSolver:
    def __init__(self, control=None, model=None):
        """Initialize model with optional control strategy"""
        self.control = control
        self.model = model
        
        # Simulation parameters
        self.N = params["simulation"]["N"]
        self.dt = params["simulation"]["dt"]
        self.sec = params["simulation"]["min"] * 60
        self.time = np.arange(0, self.sec, self.dt)
        self.Time_len = len(self.time)

        # Initial conditions
        self.s0 = params["initial"]["s_0"]
        self.v0 = params["initial"]["v_0"]
        self.u0max = params["initial"]["u_0_max"]
        self.u0 = np.array([self.u0max * (1 - i / self.N) for i in range(self.N + 1)])

        # Reference trajectory parameters
        self.s_ref_bar = params["control"]["sr"]
        self.s_ref_0 = params["initial"]["s_0"] * 1.1
        self.omega = params["reference"]["omega"]
        self.delta = params["reference"]["delta"]
        self.delta_2 = params["reference"]["delta_2"]
        self.N_series = params["reference"]["N_series"]
        # self.v_min = (params[] - self.s_ref_0) / self.sec * 12

    def run_simulation(self):
        """Run simulation with closed-loop control"""
        u_t = np.zeros((self.N + 1, self.Time_len))
        s_t = np.zeros(self.Time_len)
        v_t = np.zeros(self.Time_len)
        qc_t = np.zeros(self.Time_len)

        u_t[:, 0] = self.u0
        s_t[0] = self.s0
        v_t[0] = self.v0
        # s_ref = np.zeros(self.Time_len)

        v_min = (self.s_ref_bar - self.s_ref_0) / self.sec * 12
        A = (self.s_ref_bar - self.s_ref_0 - v_min / self.delta_2) / ( self.delta / (self.delta**2 + self.omega**2) + 1 / self.delta )
        a_n = np.zeros((self.N_series, self.Time_len))
        def s_ref(t):
            """Reference trajectory function"""
            return self.s_ref_0 + v_min / self.delta_2 * (1 - np.exp(-self.delta_2 * t)) + A * ( (self.omega * np.sin(self.omega * t) * np.exp(-self.delta * t) - self.delta * (np.cos(self.omega * t) * np.exp(-self.delta * t) - 1)) / (self.delta**2 + self.omega**2) - (np.exp(-self.delta * t) - 1) / self.delta )
        def v_ref(t):
            """Reference velocity function"""
            return A * (1 + np.cos(self.omega * t)) * np.exp(-self.delta * t) + v_min * np.exp(-self.delta_2 * t) 
        def a_ref(t):
            """Reference acceleration function"""
            return - A * (self.delta * (1 + np.cos(self.omega * t)) + self.omega * np.sin(self.omega * t)) * np.exp(-self.delta * t) - self.delta_2 * v_min * np.exp(-self.delta_2 * t)
        # def a_n_func(n, t):
        #     """Coefficient function for reference temperature profile"""
        #     if n == 0:
        #         return 0
        #     elif n == 1:
        #         return - (self.epsilon * a_ref(t) + v_ref(t)) / self.beta
        #     else:
        #         return (np.gradient(a_n_func(n-2, t), self.dt) - v_ref(t) * a_n_func(n-1, t)) / self.alp
        # def u_ref_func(x, a_n, s_ref, t):
        #     """Reference temperature profile function"""
        #     return sum([(a_n[n,:] * (x - s_ref(t)) **n) / math.factorial(n) for n in range(self.N_series)])
        self.alp = params["physical"]["kc"] / params["physical"]["rho"] / params["physical"]["cp"]
        self.beta = params["physical"]["kc"] / params["physical"]["rho"] / params["physical"]["Hf"]
        self.epsilon = params["physical"]["epsilon"]
        self.kc = params["physical"]["kc"]
        u_ref = np.zeros((self.N + 1, self.Time_len))
        u_ref_2 = np.zeros((self.N + 1, self.Time_len))
        a_n[0,:] = np.zeros(self.Time_len)
        a_n[1,:] = - (self.epsilon * a_ref(self.time) + v_ref(self.time)) / self.beta
        qc_ref = - self.kc * a_n[1,:]
        for i in range(2, self.N_series):
            da_pre_dt = np.diff(a_n[i-2,:], prepend=0) / self.dt
            a_n[i,:] = (da_pre_dt - v_ref(self.time) * a_n[i-1,:]) / self.alp
            qc_ref[:] += - self.kc * a_n[i,:] / math.factorial(i-1) * (( - s_ref(self.time))**(i-1))

        for k in range(self.Time_len - 1):
            for i in range(self.N + 1):
                u_ref[i,k] = sum([(a_n[n,k] * (s_t[k] * (i / self.N - 1) ) **n) / math.factorial(n) for n in range(self.N_series)])
                u_ref_2[i,k] = sum([(a_n[n,k] * (s_ref(self.time[k]) * (i / self.N - 1) ) **n) / math.factorial(n) for n in range(self.N_series)])
            # 🔹 Apply control strategy at each time step
            if self.control:
                qc_t[k] = self.control.apply_control(s_t[k], s_t[k] - s_ref(self.time[k]), u_t[:self.N+1, k] - u_ref[:,k], v_t[k] - v_ref(self.time[k])) + qc_ref[k]

            # Compute update law
            du_dt, ds_dt, dv_dt = self.model.compute_update_law(s_t[k], u_t[:, k], v_t[k], qc_t[k])
            u_t[:, k + 1] = u_t[:, k] + self.dt * du_dt
            s_t[k + 1] = s_t[k] + self.dt * ds_dt
            v_t[k + 1] = v_t[k] + self.dt * dv_dt
        


        return self.time, s_t, u_t, qc_t, s_ref(self.time), v_ref(self.time), u_ref_2, qc_ref
