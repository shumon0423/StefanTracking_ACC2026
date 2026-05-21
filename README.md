# Safe Control of the Stefan PDE with High-Order Moving Boundary

## Overview

This repository provides a simulation environment for exploring the safe control of the Stefan problem, which is a mathematical model of a moving boundary problem that appears in phase change problems, such as melting and solidification. The Stefan PDE with a high-order moving boundary is a challenging control problem. This project implements a numerical solver and control strategies to simulate and control the system safely.

## Features

* **Second-Order Stefan Model:** Implements a mathematical model for the melting of zinc.

* **Control Strategies:** Includes two different control strategies for manipulating the heat flux at the boundary.

* **Numerical Solver:** A solver to run the simulation with the chosen model and control strategy.

* **Condition Checks:** Includes checks for Neumann stability, setpoint, and gain conditions to ensure the simulation runs under valid conditions.

* **Visualization:** Generates plots for the interface position, boundary temperature, controlled boundary heat flux, and a 3D surface plot of the temperature profile.

## Repository Structure

The repository is organized as follows:

```
/HighOrderStefan_CDC2025
│─ src/                # Source code
│   │─ main.py         # Main execution script
│   │─ solve.py        # Numerical solver
│   │─ model.py        # Stefan model
│   │─ control.py      # Control logic
│   │─ check.py        # Conditions' satisfaction
│   │─ parameters.py   # Used parameters
│   │─ plot.py         # Visualization
│─ config/             # Configuration files
│   │─ parameters.yaml # Parameters
│─ README.md           # Overview
│─ requirements.txt    # Dependencies

```

## Installation

1. **Clone the repository:**

   ```bash
   git clone [https://github.com/shumon0423/HighOrderStefan_CDC2025.git](https://github.com/shumon0423/HighOrderStefan_CDC2025.git)
   cd HighOrderStefan_CDC2025
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

To run the simulation, execute the `main.py` script from the `src` directory:

```bash
python src/main.py
```

You can choose the model and control strategy to use by modifying the `main.py` file:

```python
def main():

    model_type = StefanSecondOrderModel()  # Change to StefanSecondOrderModel() for different behavior
    # 🔹 Choose control strategy here
    control_strategy = ControlStrategy2()  # Change to ControlStrategy2() for different behavior
    # Initialize the state with the selected control strategy
    system = StefanSolver(control=control_strategy, model=model_type)
```

The script will then run the simulation and generate a series of plots.

## Configuration

The simulation parameters can be configured in the `config/parameters.yaml` file. These include physical constants, simulation settings, initial conditions, and control gains.

**Example `parameters.yaml`:**

```yaml
physical:
  rho: 6570.0    # Density [kg/m^3]
  Hf: 111961.0   # Latent heat of fusion [J/kg]
  kc: 116.0      # Thermal conductivity [W/m/K]
  cp: 389.5687   # Specific heat capacity [J/kg/K]
  Tm: 420.0      # Melting temperature
  epsilon: 1     # Time response of interface acceleration [s]

simulation:
  N: 20          # Spatial discretization number
  min: 100       # Time [min]
  dt: 0.1        # Time step [s]

initial:
  s_0: 0.1       # Initial position [m]
  v_0: 0.0       # Initial velocity [m/s]
  u_0_max: 10.0  # Initial temperature [K]

control:
  c_1: 0.2       # Control gain [1/s]
  c_2: 0.2       # Control gain [1/s]
  sr: 0.2        # Setpoint [m]
```
<!-- 
## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or find any bugs.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details. -->
