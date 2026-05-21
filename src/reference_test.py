import numpy as np
import matplotlib.pyplot as plt
from parameters import params
import math

## Reference trajectory parameters
rho= 6570.0    # Density [kg/m^3]
Hf= 111961.0   # Latent heat of fusion [J/kg]
kc= 116.0      # Thermal conductivity [W/m/K]
cp= 389.5687   # Specific heat capacity [J/kg/K]
Tm= 420.0        # Melting temperature
epsilon= 1   # Time response of interface acceleration [s]
alp = kc / rho / cp
beta = kc / rho / Hf

# simulation:
N= 20          # Spatial discretization number
min= 100        # Time [min]
dt= 0.1        # Time step [s]

# initial:
s_0= 0.1       # Initial position [m]
v_0= 0.0       # Initial velocity [m/s]
u_0_max= 10.0     # Initial temperature [K]

# control:
c_1= 0.2         # Control gain [1/s]
c_2= 0.2       # Control gain [1/s]
sr= 0.2        # Setpoint [m]

sec = min * 60
time = np.arange(0, sec, dt)
Time_len = len(time)

s_ref_bar = 0.2
omega = 5e-3
delta = 10 / sec
delta_2 = 10 / sec
s_ref_0 = 0.1 # Initial reference position
# v_min = min((s_ref_bar - s_ref_0) / sec * 0.1, delta_2 * (s_ref_bar - s_ref_0))
v_min = (s_ref_bar - s_ref_0) / sec * 3
A = (s_ref_bar - s_ref_0 - v_min / delta_2) / ( delta / (delta**2 + omega**2) + 1 / delta )
N_series = 3
a_n = np.zeros((N_series, Time_len))
def s_ref(t):
    """Reference trajectory function"""
    return s_ref_0 + v_min / delta_2 * (1 - np.exp(-delta_2 * t)) + A * ( (omega * np.sin(omega * t) * np.exp(-delta * t) - delta * (np.cos(omega * t) * np.exp(-delta * t) - 1)) / (delta**2 + omega**2) + (1 - np.exp(-delta * t)) / delta )
def v_ref(t):
        """Reference velocity function"""
        return A * (1 + np.cos(omega * t)) * np.exp(-delta * t) + v_min * np.exp(-delta_2 * t) 
def a_ref(t):
    """Reference acceleration function"""
    return - A * (delta * (1 + v_min + np.cos(omega * t)) + omega * np.sin(omega * t)) * np.exp(-delta * t) - delta_2 * v_min * np.exp(-delta_2 * t)
u_ref = np.zeros((N + 1, Time_len))
a_n[0,:] = np.zeros(Time_len)
a_n[1,:] = - (epsilon * a_ref(time) + v_ref(time)) / beta
qc_ref = - kc * a_n[1,:]
for i in range(2, N_series):
    da_pre_dt = np.diff(a_n[i-2,:], prepend=0) / dt
    a_n[i,:] = (da_pre_dt - v_ref(time) * a_n[i-1,:]) / alp
    qc_ref[:] += - kc * a_n[i,:] / math.factorial(i-1) * ((-s_ref(time))**(i-1))

def plot_reference_trajectory():
    """Plot the reference trajectory over time"""
    plt.figure(figsize=(10, 5))
    plt.plot(time, s_ref(time), label='Reference Trajectory $s_{ref}(t)$', color='blue')
    plt.title('Reference Trajectory Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Position $s_{ref}(t)$')
    plt.grid(True)
    plt.legend()
    plt.show()
def plot_feedforward_control():
    """Plot the reference trajectory over time"""

    plt.figure(figsize=(10, 5))
    plt.plot(time, qc_ref, label='Reference Trajectory $s_{ref}(t)$', color='blue')
    plt.title('Reference Trajectory Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Position $s_{ref}(t)$')
    plt.grid(True)
    plt.legend()
    plt.show()
if __name__ == "__main__":
    plot_reference_trajectory()
    plot_feedforward_control()
