import numpy as np
from parameters import params
from reference import ReferenceTrajectory


class StefanSolver:
    def __init__(self, control=None, model=None):
        self.control = control
        self.model = model

        self.N = params["simulation"]["N"]
        self.dt = params["simulation"]["dt"]
        self.sec = params["simulation"]["min"] * 60
        self.time = np.arange(0, self.sec, self.dt)
        self.Time_len = len(self.time)

        self.s0 = params["initial"]["s_0"]
        self.v0 = params["initial"]["v_0"]
        self.u0max = params["initial"]["u_0_max"]
        self.u0 = np.array([self.u0max * (1 - i / self.N) for i in range(self.N + 1)])

        self.ref = ReferenceTrajectory(params, self.time)

    def run_simulation(self):
        u_t = np.zeros((self.N + 1, self.Time_len))
        s_t = np.zeros(self.Time_len)
        v_t = np.zeros(self.Time_len)
        qc_t = np.zeros(self.Time_len)
        u_ref = np.zeros((self.N + 1, self.Time_len))

        u_t[:, 0] = self.u0
        s_t[0] = self.s0
        v_t[0] = self.v0

        for k in range(self.Time_len - 1):
            t_k = self.time[k]
            u_ref[:, k] = self.ref.eval_u_ref(self.ref.s_ref(t_k), k)

            if self.control:
                u_err = u_t[:, k] - self.ref.eval_u_ref(s_t[k], k)
                qc_t[k] = self.control.apply_control(
                    s_t[k],
                    s_t[k] - self.ref.s_ref(t_k),
                    u_err,
                    v_t[k] - self.ref.v_ref(t_k),
                ) + self.ref.qc_ref[k]

            du_dt, ds_dt, dv_dt = self.model.compute_update_law(s_t[k], u_t[:, k], v_t[k], qc_t[k])
            u_t[:, k + 1] = u_t[:, k] + self.dt * du_dt
            s_t[k + 1] = s_t[k] + self.dt * ds_dt
            v_t[k + 1] = v_t[k] + self.dt * dv_dt

        return (
            self.time, s_t, u_t, qc_t,
            self.ref.s_ref(self.time), self.ref.v_ref(self.time),
            u_ref, self.ref.qc_ref,
        )
