# Safe Control of the Stefan PDE with High-Order Moving Boundary

## Overview

This repository provides a simulation environment for exploring the safe control of the Stefan problem, which is a mathematical model of a moving boundary problem that appears in phase change problems, such as melting and solidification. The Stefan PDE with a high-order moving boundary is a challenging control problem. This project implements a numerical solver and control strategies to simulate and control the system safely.

## Features

* **Second-Order Stefan Model:** Implements a mathematical model for the melting of zinc.

* **Reference Trajectory:** `ReferenceTrajectory` class encapsulates the desired interface position, velocity, and feedforward heat flux, including the Taylor-series coefficient computation for the reference temperature profile.

* **Control Strategies:** Two feedback control strategies (`ControlStrategy1`, `ControlStrategy2`) for tracking the reference trajectory via boundary heat flux.

* **Numerical Solver:** `StefanSolver` runs the closed-loop simulation with any model/control pair.

* **Condition Checks:** Verifies Neumann stability, setpoint, and gain conditions before running.

* **Visualization:** Plots interface position, boundary temperature, controlled heat flux, and spatial temperature profiles at selected time snapshots.

## Repository Structure

```
/StefanTracking_ACC2026
│─ src/                # Source code
│   │─ main.py         # Main execution script
│   │─ solve.py        # Numerical solver (uses ReferenceTrajectory)
│   │─ model.py        # Stefan second-order model
│   │─ control.py      # Control strategies
│   │─ reference.py    # ReferenceTrajectory class (s_ref, v_ref, feedforward)
│   │─ check.py        # Stability, setpoint, and gain condition checks
│   │─ parameters.py   # Loads config/parameters.yaml; exposes derived alp, beta
│   │─ plot.py         # Visualization
│   │─ plot_saved.py   # Reload and re-plot saved simulation results
│─ config/             # Configuration files
│   │─ parameters.yaml # All tunable parameters
│─ README.md           # Overview
│─ requirements.txt    # Dependencies
```

## Installation

1. **Clone the repository:**

   ```bash
   git clone [https://github.com/shumon0423/StefanTracking_ACC2026.git](https://github.com/shumon0423/StefanTracking_ACC2026.git)
   cd StefanTracking_ACC2026
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   The required packages are:

   * numpy>=1.24

   * PyYAML>=6.0.1

   * matplotlib~=3.9.2

## Usage

Run the simulation from the project root or from inside `src/`:

```bash
python src/main.py
```

To switch control strategy, edit the two lines at the top of `main()` in `src/main.py`:

```python
model_type = StefanSecondOrderModel()
control_strategy = ControlStrategy2()  # or ControlStrategy1()
```

To re-plot a previously saved result without re-running the simulation:

```bash
python src/plot_saved.py
```

Simulation output is saved to `simulation_results.npz` in the working directory.

## Configuration

All tunable parameters live in `config/parameters.yaml`. `parameters.py` loads this file and also computes the derived quantities `alp = kc / rho / cp` and `beta = kc / rho / Hf`, which are available to every module via `params["physical"]["alp"]` and `params["physical"]["beta"]`.

```yaml
physical:
  rho: 6570.0    # Density [kg/m^3]
  Hf: 111961.0   # Latent heat of fusion [J/kg]
  kc: 116.0      # Thermal conductivity [W/m/K]
  cp: 389.5687   # Specific heat capacity [J/kg/K]
  Tm: 420.0      # Melting temperature [K]
  epsilon: 10    # Interface acceleration time constant [s]

simulation:
  N: 20          # Spatial discretization points
  min: 100       # Simulation duration [min]
  dt: 0.1        # Time step [s]

initial:
  s_0: 0.1       # Initial interface position [m]
  v_0: 0.0       # Initial interface velocity [m/s]
  u_0_max: 10.0  # Peak initial temperature [K]

control:
  c_1: 0.002     # Control gain [1/s]
  c_2: 0.002     # Control gain [1/s]
  sr: 0.15       # Setpoint (target interface position) [m]

reference:
  omega: 0.002   # Reference trajectory frequency [rad/s]
  delta: 0.0004  # Exponential decay rate [1/s]
  delta_2: 0.004 # Secondary decay rate [1/s]
  N_series: 5    # Taylor series terms for reference temperature profile
```
<!-- 
## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or find any bugs.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details. -->
