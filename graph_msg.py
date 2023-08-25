import numpy as np
import matplotlib.pyplot as plt
import os


def main(n_pilot=3, conv_t=35, seed=0):
    x = np.load(os.path.join("debug", f"seed{seed}-x.npy"))
    alpha_tilde = np.load(os.path.join("debug", f"msg_alpha_tilde.npy"))
    alpha_bar = np.load(os.path.join("debug", f"msg_alpha_bar.npy"))
    rho_tilde = np.load(os.path.join("debug", f"msg_rho_tilde.npy"))
    rho_bar = np.load(os.path.join("debug", f"msg_rho_tilde.npy"))
    show_mp_traj(x, alpha_tilde, alpha_bar, rho_tilde, rho_bar, n_pilot, conv_t)
    # show_mp_traj_one(0, 0, alpha_tilde, alpha_bar, rho_tilde, rho_bar)


def show_mp_traj(x, alpha_tilde, alpha_bar, rho_tilde, rho_bar, n_pilot, conv_t):
    n_iter = np.size(alpha_tilde, axis=0)
    dim_x = len(x)

    t = np.linspace(0, n_iter-1, n_iter)
    for i in range(dim_x):
        _, axes = plt.subplots(nrows=2, ncols=2,
                           tight_layout=True)
        axes[0, 0].set_title(r"$\tilde{\alpha}$")
        axes[0, 1].set_title(r"$\bar{\alpha}$")
        axes[1, 0].set_title(r"$\tilde{\rho}$")
        axes[1, 1].set_title(r"$\bar{\rho}$")
        for j in range (n_pilot):
            axes[0, 0].plot(t, alpha_tilde[:, i, j], label=f"u{x[i]}--r{j}", alpha=0.6)
            axes[0, 1].plot(t, alpha_bar[:, i, j], label=f"u{x[i]}--r{j}", alpha=0.6)
            axes[1, 0].plot(t, rho_tilde[:, i, j], label=f"u{x[i]}--r{j}", alpha=0.6)
            axes[1, 1].plot(t, rho_bar[:, i, j], label=f"u{x[i]}--r{j}", alpha=0.6)
        axes[0, 0].legend()
        axes[0, 1].legend()
        axes[1, 0].legend()
        axes[1, 1].legend()
        axes[0, 1].set_xlim(0, conv_t)
        axes[0, 0].set_xlim(0, conv_t)
        axes[1, 0].set_xlim(0, conv_t)
        axes[1, 1].set_xlim(0, conv_t)
        plt.show()
        plt.savefig(f"msg_trajectory_{i}.png")
        plt.close()
    


def show_mp_traj_one(x_number, pilot_number, alpha_tilde, alpha_bar, rho_tilde, rho_bar):
    n_iter = np.size(alpha_tilde, axis=0)
    _, axes = plt.subplots(nrows=1, ncols=2, tight_layout=True)
    axes[0].set_title(r"$\alpha$")
    axes[1].set_title(r"$\rho$")
    t = np.linspace(0, n_iter-1, n_iter)
    axes[0].plot(t, alpha_tilde[:, x_number, pilot_number], label=r'$\tilde{\alpha}$')
    axes[0].plot(t, alpha_bar[:, x_number, pilot_number], label=r'$\bar{\alpha}$')
    axes[1].plot(t, rho_tilde[:, x_number, pilot_number], label=r'$\tilde{\rho}$')
    axes[1].plot(t, rho_bar[:, x_number, pilot_number], label=r'$\bar{\rho}$')
    axes[0].set_xlim(xmin=0, xmax=n_iter-1)
    axes[1].set_xlim(xmin=0, xmax=n_iter-1)
    axes[0].legend()
    axes[1].legend()
    plt.show()


if __name__=="__main__":
    main()
