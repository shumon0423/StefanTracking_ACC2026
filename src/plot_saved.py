import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib import cm
from plot import plot_results, plot_results_ref, plot_contour

def main():
    # Load the data from the file
    data = np.load('simulation_results.npz')

    # Access the individual arrays
    time, s_t, u_t, qc_t, s_ref, v_ref, u_ref, qc_ref = data['time'], data['s_t'], data['u_t'], data['qc_t'], data['s_ref'], data['v_ref'], data['u_ref'], data['qc_ref']
    plot_results_ref(time, s_t, u_t, qc_t, s_ref, v_ref, u_ref, qc_ref)

def contour():
    # Load the data from the file
    data = np.load('simulation_results_contour.npz')
    X, Y, Z, Z_ref = data['X'], data['Y'], data['Z_t'], data['Z_ref']
    t_init = 30  # initial time index to skip
    indices = np.linspace(t_init, X.shape[1] - 1, num=600).astype(int)
    # space_indices = np.linspace(0, X.shape[0] - 2, num=100).astype(int)
    X, Y, Z, Z_ref = X[:, indices], Y[:, indices], Z[:, indices], Z_ref[:, indices]
    # X, Y, Z, Z_ref = X[space_indices, :], Y[space_indices, :], Z[space_indices, :], Z_ref[space_indices, :]
    print(X.shape, Y.shape, Z.shape, Z_ref.shape)
    plot_contour(X, Y, Z, Z_ref)

if __name__ == "__main__":
    main()
    # contour()