import numpy as np
import matplotlib.pyplot as plt
from survey_propagation import n_resource
from system_setting import get_x


def main():
    x = get_x()
    alpha_tilde = np.load("alpha_tilde.npy")
    alpha_bar = np.load("alpha_bar.npy")
    rho_tilde = np.load("rho_tilde.npy")
    rho_bar = np.load("rho_bar.npy")
    print(x)
    show_mp_traj(x, alpha_tilde, alpha_bar, rho_tilde, rho_bar)
    # show_mp_traj_one(1, 6, alpha_tilde, alpha_bar, rho_tilde, rho_bar)


def show_mp_traj(x, alpha_tilde, alpha_bar, rho_tilde, rho_bar):
    n_iter = np.size(alpha_tilde, axis=0)
    dim_x = len(x)
    _, axes = plt.subplots(nrows=dim_x, ncols=4,
                           tight_layout=True)
    axes[0, 0].set_title(r"$\tilde{\alpha}$")
    axes[0, 1].set_title(r"$\bar{\alpha}$")
    axes[0, 2].set_title(r"$\tilde{\rho}$")
    axes[0, 3].set_title(r"$\bar{\rho}$")
    t = np.linspace(0, n_iter-1, n_iter)
    for i in range(dim_x):
        for j in range (n_resource):
            axes[i, 0].plot(t, alpha_tilde[:, i, j], label=f"u{x[i]}--r{j}")
            axes[i, 1].plot(t, alpha_bar[:, i, j], label=f"u{x[i]}--r{j}")
            axes[i, 2].plot(t, rho_tilde[:, i, j], label=f"u{x[i]}--r{j}")
            axes[i, 3].plot(t, rho_bar[:, i, j], label=f"u{x[i]}--r{j}")
        axes[i, 0].set_xlim(xmin=0, xmax=n_iter-1)
        axes[i, 1].set_xlim(xmin=0, xmax=n_iter-1)
        axes[i, 2].set_xlim(xmin=0, xmax=n_iter-1)
        axes[i, 3].set_xlim(xmin=0, xmax=n_iter-1)
        axes[i, 0].legend()
        # axes[i, 1].legend()
        # axes[i, 2].legend()
        # axes[i, 3].legend()
    plt.show()
    plt.savefig("mp_trajectory.png")


def show_mp_traj_one(x_number, resource_number, alpha_tilde, alpha_bar, rho_tilde, rho_bar):
    n_iter = np.size(alpha_tilde, axis=0)
    _, axes = plt.subplots(nrows=1, ncols=2, tight_layout=True)
    axes[0].set_title(r"$\alpha$")
    axes[1].set_title(r"$\rho$")
    t = np.linspace(0, n_iter-1, n_iter)
    axes[0].plot(t, alpha_tilde[:, x_number, resource_number], label=r'$\tilde{\alpha}$')
    axes[0].plot(t, alpha_bar[:, x_number, resource_number], label=r'$\bar{\alpha}$')
    axes[1].plot(t, rho_tilde[:, x_number, resource_number], label=r'$\tilde{\rho}$')
    axes[1].plot(t, rho_bar[:, x_number, resource_number], label=r'$\bar{\rho}$')
    axes[0].set_xlim(xmin=0, xmax=n_iter-1)
    axes[1].set_xlim(xmin=0, xmax=n_iter-1)
    axes[0].legend()
    axes[1].legend()
    plt.show()


if __name__=="__main__":
    main()
