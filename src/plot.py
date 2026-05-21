import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as mcolors

def profile_interpolation(u, s, s_max, N_res=100, u_min=0):
    """Interpolate the temperature profile to a fixed spatial resolution"""
    u_res = np.zeros((N_res + 1, u.shape[1]))
    for t in range(u.shape[1]):
        for i in range(N_res + 1):
            idx_pre_floor = i * s_max / N_res * (u.shape[0] - 1) / s
            idx_sr = math.floor(idx_pre_floor)
            if idx_sr < u.shape[0]-1:
                u_res[i, t] = u[idx_sr, t] + (u[idx_sr+1, t] - u[idx_sr, t]) * (idx_pre_floor - idx_sr)
            else:
                u_res[i, t] = u_min
    return u_res

def plot_results(time, s_t, u_t, qc_t):
    plt.figure()
    plt.plot(time / 60, s_t * 100, linewidth=2)
    plt.xlim([time[0] / 60, (time[time.size - 1] + 1) / 60])
    plt.ylim([min(s_t) * 100, max(s_t) * 100])
    plt.xlabel("Time [min]", fontsize=14)
    plt.ylabel("Interface position [cm]", fontsize=14)
    plt.xticks(fontsize=16) # Increase font size of x-axis
    plt.yticks(fontsize=16) # Increase font size of y-axis
    plt.show()

    plt.figure()
    plt.plot(time / 60, u_t[0, :], linewidth=2)
    # plt.xlim([time[0] / 60, (time[time.size - 1] + 1) / 60 / 2])
    # plt.ylim(bottom=0)
    plt.xlabel("Time [min]", fontsize=14)
    plt.ylabel("Boundary temperature [C]", fontsize=14)
    plt.xticks(fontsize=16) # Increase font size of x-axis
    plt.yticks(fontsize=16) # Increase font size of y-axis
    plt.show()

    plt.figure()
    plt.plot(time / 60, u_t[0, :], linewidth=2)
    # plt.xlim([time[0] / 60, (time[time.size - 1] + 1) / 60 / 2])
    plt.ylim(bottom = -10, top=0)
    plt.xlabel("Time [min]", fontsize=14)
    plt.ylabel("Boundary temperature [C]", fontsize=14)
    plt.xticks(fontsize=16) # Increase font size of x-axis
    plt.yticks(fontsize=16) # Increase font size of y-axis
    plt.show()

    plt.figure()
    plt.plot(time / 60, qc_t, linewidth=2)
    plt.xlim([time[0] / 60, (time[time.size - 1] + 1) / 60 / 20])
    # plt.ylim(bottom=0)
    plt.xlabel("Time [min]", fontsize=14)
    plt.ylabel("Controlled boundary heat flux [W/m^2]", fontsize=14)
    plt.xticks(fontsize=16) # Increase font size of x-axis
    plt.yticks(fontsize=16) # Increase font size of y-axis
    plt.show()

    plt.figure()
    plt.contour(time / 60, range(u_t.shape[0]), u_t, linewidths=2)
    # plt.xlim([time[0] / 60, (time[time.size - 1] + 1) / 60])
    # plt.ylim([0, u_t.shape[0]])
    plt.xlabel("Time [min]", fontsize=14)
    plt.ylabel("Temperature [C]", fontsize=14)
    plt.xticks(fontsize=16) # Increase font size of x-axis
    plt.yticks(fontsize=16) # Increase font size of y-axis
    plt.show()
    
    
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    # Make data.
    division = 10
    X = time[:math.floor(len(time)/division)] / 60
    Y = range(u_t.shape[0])
    X, Y = np.meshgrid(X, Y)
    Z = u_t[:, :math.floor(len(time)/division)]

    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)

    # Customize the z axis.
    # ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    ax.zaxis.set_major_formatter('{x:.02f}')

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()

def plot_results_ref(time, s_t, u_t, qc_t, s_ref, v_ref, u_ref, qc_ref):
    plt.figure()
    plt.plot(time / 60, s_t * 100, linewidth=2)
    plt.plot(time / 60, s_ref * 100, 'r--', linewidth=2)
    plt.xlim([time[0] / 60, (time[time.size - 1] + 1) / 60])
    plt.ylim([min(s_t) * 100, max(s_t) * 100])
    plt.xlabel("Time [min]", fontsize=14)
    plt.ylabel("Interface position [cm]", fontsize=14)
    plt.xticks(fontsize=16) # Increase font size of x-axis
    plt.yticks(fontsize=16) # Increase font size of y-axis
    plt.show()

    plt.figure()
    plt.plot(time / 60, u_t[0, :], linewidth=2)
    plt.plot(time / 60, u_ref[0, :], 'r--', linewidth=2)
    plt.xlim([time[0] / 60, (time[time.size - 1] + 1) / 60 ])
    # plt.ylim(bottom=0)
    plt.ylim(top=2e2, bottom=np.min(u_ref[0,:]))
    plt.xlabel("Time [min]", fontsize=14)
    plt.ylabel("Boundary temperature [C]", fontsize=14)
    plt.xticks(fontsize=16) # Increase font size of x-axis
    plt.yticks(fontsize=16) # Increase font size of y-axis
    plt.show()

    plt.figure()
    plt.plot(time / 60, qc_t, linewidth=2)
    plt.plot(time / 60, qc_ref, 'r--', linewidth=2)
    plt.xlim([time[0]/60, (time[time.size - 1] + 1) / 60])
    plt.ylim(top=5e4, bottom=np.min(qc_ref))
    # plt.ylim(bottom=0)
    plt.xlabel("Time [min]", fontsize=14)
    plt.ylabel("Controlled boundary heat flux [W/m^2]", fontsize=14)
    plt.xticks(fontsize=16) # Increase font size of x-axis
    plt.yticks(fontsize=16) # Increase font size of y-axis
    plt.show()


    # plt.figure()
    # plt.contour(time / 60, range(u_t.shape[0]), u_t, linewidths=2)
    # # plt.xlim([time[0] / 60, (time[time.size - 1] + 1) / 60])
    # # plt.ylim([0, u_t.shape[0]])
    # plt.xlabel("Time [min]", fontsize=14)
    # plt.ylabel("Temperature [C]", fontsize=14)
    # plt.xticks(fontsize=16) # Increase font size of x-axis
    # plt.yticks(fontsize=16) # Increase font size of y-axis
    # plt.show()

    s_max = 0.16
    N_res = 1000
    tk_sequence = [30, 1 * 600, 10 * 600, 99 * 600]  # Time indices to plot
    # fig, ax = plt.subplots(2, 2, figsize=(10, 8))
    # for idx, tk in enumerate(tk_sequence):
    #     u_ref_2 = profile_interpolation(u_ref[:,tk:tk+1], s_ref[tk], s_max, N_res)
    #     u_t_2 = profile_interpolation(u_t[:,tk:tk+1], s_t[tk], s_max, N_res)
        
    #     ax[idx//2, idx%2].plot(np.linspace(0, s_max, N_res + 1) * 100, u_t_2, linewidth=2)
    #     ax[idx//2, idx%2].plot(np.linspace(0, s_max, N_res + 1) * 100, u_ref_2, 'r--', linewidth=2)
    #     ax[idx//2, idx%2].set_xlim([0, s_max * 100])
    #     ax[idx//2, idx%2].set_ylim(top=max(np.max(u_t_2), np.max(u_ref_2)), bottom=np.min(u_ref_2))
    #     ax[idx//2, idx%2].set_xlabel("Spatial Position [cm]", fontsize=12)
    #     ax[idx//2, idx%2].set_ylabel("Temperature [C]", fontsize=12)
    #     ax[idx//2, idx%2].set_title(f'Time = {time[tk]/60:.2f} min')
    #     ax[idx//2, idx%2].tick_params(axis='x', labelsize=12) # Increase font size of x-axis
    #     ax[idx//2, idx%2].tick_params(axis='y', labelsize=12) # Increase font size of y-axis
    # plt.show()

    fig, ax = plt.subplots(1, 4, figsize=(16, 3),constrained_layout=True)
    for idx, tk in enumerate(tk_sequence):
        u_ref_2 = profile_interpolation(u_ref[:,tk:tk+1], s_ref[tk], s_max, N_res)
        u_t_2 = profile_interpolation(u_t[:,tk:tk+1], s_t[tk], s_max, N_res)
        
        ax[idx].plot(np.linspace(0, s_max, N_res + 1) * 100, u_t_2, linewidth=2)
        ax[idx].plot(np.linspace(0, s_max, N_res + 1) * 100, u_ref_2, 'r--', linewidth=2)
        ax[idx].set_xlim([0, s_max * 100])
        ax[idx].set_ylim(top=max(np.max(u_t_2), np.max(u_ref_2)), bottom=np.min(u_ref_2))
        # ax[idx].set_xlabel("Position [cm]", fontsize=12)
        # if idx == 0:
        #     ax[idx].set_ylabel("Temperature [C]", fontsize=12)
        ax[idx].set_title(f'Time = {time[tk]/60:.2f} [min]')
        ax[idx].tick_params(axis='x', labelsize=12) # Increase font size of x-axis
        ax[idx].tick_params(axis='y', labelsize=12) # Increase font size of y-axis
    fig.supxlabel("Spatial Position [cm]", fontsize=12)
    fig.supylabel("Temperature [$^\circ$C]", fontsize=12)
    plt.tight_layout()
    plt.show()
    
    
    # # Make data.
    # division = 1
    # X = time[:math.floor(len(time)/division)] / 60
    # Y = np.linspace(0, s_max, u_t_2.shape[0])
    # X, Y = np.meshgrid(X, Y)
    # Z = np.zeros((u_t_2.shape[0], math.floor(len(time)/division)))
    # Z_ref = np.zeros((u_ref_2.shape[0], math.floor(len(time)/division)))
    # threshold = 0
    # for t in range(X.shape[1]):
    #     u_t_2 = profile_interpolation(u_t[:,t:t+1], s_t[t], s_max, N_res, threshold-1)
    #     Z[:, t] = u_t_2[:, 0]
    #     u_ref_2 = profile_interpolation(u_ref[:,t:t+1], s_ref[t], s_max, N_res, threshold-1)
    #     Z_ref[:, t] = u_ref_2[:, 0]

    # np.savez_compressed('simulation_results_contour.npz', X=X, Y=Y, Z_t=Z, Z_ref=Z_ref)



def plot_contour(X, Y, Z, Z_ref):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    levels = np.linspace(0, np.max(Z), 11) # 11 levels between -0.5 and 0.5
    contour_1 = axes[0].contourf(X, Y, Z, levels = levels, cmap='viridis') #, norm=norm) #, cmap=cmap, norm=norm)
    fig.colorbar(contour_1, ax=axes[0], label='Temperature (C)')
    axes[0].contour(X, Y, Z, levels=[-1], colors='black', linewidths=1)
    axes[0].set_title('Trackng Control')
    axes[0].set_xlabel('Time [min]')
    axes[0].set_ylabel('Spatial Position [m]')
    levels = np.linspace(0, np.max(Z_ref), 11)
    contour_2 = axes[1].contourf(X, Y, Z_ref, levels = levels, cmap='viridis') #, norm=norm) #, cmap=cmap, norm=norm)
    fig.colorbar(contour_2, ax=axes[1], label='Temperature (C)')
    axes[1].contour(X, Y, Z_ref, levels=[-1], colors='black', linewidths=1)
    axes[1].set_title('Reference')
    axes[1].set_xlabel('Time [min]')
    axes[1].set_ylabel('Spatial Position [m]')  
    plt.tight_layout()
    # Display the plot
    plt.show()

    # Plot the surface.
    # fig, axes = plt.subplots(1, 2, subplot_kw={"projection": "3d"})
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), subplot_kw={"projection": "3d"})
    surf_1 = axes[0].plot_surface(X, Y, Z, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False, vmin=0, vmax=np.max(Z), alpha=0.82)
    axes[0].set_zlim(0, max(np.max(Z), np.max(Z_ref)))
    axes[0].contour(X, Y, Z, levels=[-1], colors='black', linewidths=3)
    # axes[0].zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    # axes[0].zaxis.set_major_formatter('{x:.02f}')
    # Add a color bar which maps values to colors.
    fig.colorbar(surf_1, ax=axes[0], shrink=0.5, aspect=5)
    axes[0].set_title('Tracking Control')
    axes[0].set_xlabel('Time [min]')
    axes[0].set_ylabel('Spatial Position [m]')    
    axes[0].set_zlabel('Temperature [$^\circ$C]')
    surf_2 = axes[1].plot_surface(X, Y, Z_ref, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False, vmin=0, vmax=np.max(Z_ref), alpha=0.82)
    axes[1].set_zlim(0, max(np.max(Z), np.max(Z_ref)))
    axes[1].contour(X, Y, Z_ref, levels=[-1], colors='black', linewidths=3)
    # axes[1].zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    # axes[1].zaxis.set_major_formatter('{x:.02f}')
    # Add a color bar which maps values to colors.
    fig.colorbar(surf_2, ax=axes[1], shrink=0.5, aspect=5)
    axes[1].set_title('Reference')
    axes[1].set_xlabel('Time [min]')
    axes[1].set_ylabel('Spatial Position [m]')    
    axes[1].set_zlabel('Temperature [$^\circ$C]')    
    plt.tight_layout()
    # Display the plot    
    plt.show()