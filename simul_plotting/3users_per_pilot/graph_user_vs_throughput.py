import numpy as np
import matplotlib.pyplot as plt


def main():
    n_user_list = [15, 30, 45, 60, 75]
    sum_rates = np.zeros(len(n_user_list))
    sum_rates_hh = np.zeros(len(n_user_list))
    sum_rates_gd = np.zeros(len(n_user_list))
    for i, n_user in enumerate(n_user_list):
        sum_rates[i] = np.mean(np.nan_to_num(np.load(f"sumrates_SP_{n_user}users.npy"), nan=0))
        sum_rates[i] = np.nanmean(np.load(f"sumrates_SP_{n_user}users.npy"))
        sum_rates_hh[i] = np.mean(np.load(f"sumrates_HH_{n_user}users.npy"))
        sum_rates_gd[i] = np.mean(np.load(f"sumrates_GD_{n_user}users.npy"))

    _, ax = plt.subplots(tight_layout=True)
    ax.set_xticks([15, 30, 45, 60, 75])
    ax.plot(n_user_list, sum_rates*3, "-*", color="red",label="SP")
    ax.plot(n_user_list, sum_rates_hh*3, ":*", color="blue", label="Hungarian")
    ax.plot(n_user_list, sum_rates_gd*3, "--*", color="green", label="Greedy")
    ax.set_xlim(15, 75)
    ax.set_ylim(300, 2500)
    ax.set_xlabel("Number of users")
    ax.set_ylabel("System throughput[Mbps/Hz]")
    ax.grid()
    ax.legend()
    plt.savefig("user_vs_throughput.pdf")
    plt.savefig("user_vs_throughput.png")
    return


if __name__=="__main__":
    main()