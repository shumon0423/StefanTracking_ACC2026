import numpy as np
import math
from parameters import params


class ReferenceTrajectory:
    def __init__(self, params, time):
        ref = params["reference"]
        phys = params["physical"]
        sim = params["simulation"]

        self.omega = ref["omega"]
        self.delta = ref["delta"]
        self.delta_2 = ref["delta_2"]
        self.N_series = ref["N_series"]
        self.alp = phys["alp"]
        self.beta = phys["beta"]
        self.kc = phys["kc"]
        self.epsilon = phys["epsilon"]
        self.N = sim["N"]
        self.dt = sim["dt"]

        self.s_ref_bar = params["control"]["sr"]
        self.s_ref_0 = params["initial"]["s_0"] * 1.1
        sec = sim["min"] * 60

        self.v_min = (self.s_ref_bar - self.s_ref_0) / sec * 12
        self.A = (self.s_ref_bar - self.s_ref_0 - self.v_min / self.delta_2) / (
            self.delta / (self.delta**2 + self.omega**2) + 1 / self.delta
        )

        self.time = time
        self._compute_coefficients()

    def s_ref(self, t):
        return (
            self.s_ref_0
            + self.v_min / self.delta_2 * (1 - np.exp(-self.delta_2 * t))
            + self.A * (
                (self.omega * np.sin(self.omega * t) * np.exp(-self.delta * t)
                 - self.delta * (np.cos(self.omega * t) * np.exp(-self.delta * t) - 1))
                / (self.delta**2 + self.omega**2)
                - (np.exp(-self.delta * t) - 1) / self.delta
            )
        )

    def v_ref(self, t):
        return (
            self.A * (1 + np.cos(self.omega * t)) * np.exp(-self.delta * t)
            + self.v_min * np.exp(-self.delta_2 * t)
        )

    def a_ref(self, t):
        return (
            -self.A * (self.delta * (1 + np.cos(self.omega * t)) + self.omega * np.sin(self.omega * t))
            * np.exp(-self.delta * t)
            - self.delta_2 * self.v_min * np.exp(-self.delta_2 * t)
        )

    def _compute_coefficients(self):
        time = self.time
        self.a_n = np.zeros((self.N_series, len(time)))
        self.a_n[1, :] = -(self.epsilon * self.a_ref(time) + self.v_ref(time)) / self.beta
        self.qc_ref = -self.kc * self.a_n[1, :].copy()
        for i in range(2, self.N_series):
            da_prev_dt = np.diff(self.a_n[i - 2, :], prepend=0) / self.dt
            self.a_n[i, :] = (da_prev_dt - self.v_ref(time) * self.a_n[i - 1, :]) / self.alp
            self.qc_ref += (
                -self.kc * self.a_n[i, :] / math.factorial(i - 1) * ((-self.s_ref(time)) ** (i - 1))
            )

    def eval_u_ref(self, s, k):
        """Evaluate reference temperature profile at all N+1 grid points for interface at s, time step k."""
        u = np.zeros(self.N + 1)
        for i in range(self.N + 1):
            x = s * (i / self.N - 1)
            u[i] = sum(self.a_n[n, k] * x**n / math.factorial(n) for n in range(self.N_series))
        return u
