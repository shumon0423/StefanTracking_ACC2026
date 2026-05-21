from model import StefanSecondOrderModel
from control import ControlStrategy1, ControlStrategy2
from solve import StefanSolver
from check import CheckBase
from plot import plot_results, plot_results_ref
import numpy as np

def main():

    model_type = StefanSecondOrderModel()  # Change to StefanSecondOrderModel() for different behavior
    # 🔹 Choose control strategy here
    control_strategy = ControlStrategy2()  # Change to ControlStrategy2() for different behavior
    # Initialize the state with the selected control strategy
    system = StefanSolver(control=control_strategy, model=model_type)

    # Check stability, setpoint, and gain conditions
    check = CheckBase()

    if not check.stability():
        print("Warning: Stability condition not met!")

    if not check.setpoint():
        print("Warning: Setpoint condition not met!")

    if not check.gain():
        print("Warning: Gain condition not met!")

    # Run simulation with closed-loop control
    time, s_t, u_t, qc_t, s_ref, v_ref, u_ref, qc_ref = system.run_simulation()
    np.savez_compressed('simulation_results.npz', time=time, s_t=s_t, u_t=u_t, qc_t=qc_t, s_ref=s_ref, v_ref=v_ref, u_ref=u_ref, qc_ref=qc_ref)

    # Plot results
    # plot_results(time, s_t, u_t, qc_t)
    plot_results_ref(time, s_t, u_t, qc_t, s_ref, v_ref, u_ref, qc_ref)

if __name__ == "__main__":
    main()
