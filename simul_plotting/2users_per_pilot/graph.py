import numpy as np
import matplotlib.pyplot as plt
from main import N_REPEAT

def main():
    n_user_list = [10, 20, 30, 40, 50, 60, 70, 80]
    sum_rates = np.zeros(len(n_user_list))
    sum_rates_hh = np.zeros(len(n_user_list))
    sum_rates_gd = np.zeros(len(n_user_list))
    for i, n_user in enumerate(n_user_list):
        sum_rates[i] = np.mean(np.nan_to_num(np.load(f"sumrates_SP_{n_user}users.npy"), nan=0))
        sum_rates_hh[i] = np.mean(np.load(f"sumrates_HH_{n_user}users.npy"))
        sum_rates_gd[i] = np.mean(np.load(f"sumrates_GD_{n_user}users.npy"))

    _, axes = plt.subplots(nrows=1, ncols=2,
                           tight_layout=True)
    axes[1].set_xticks([10, 30, 50, 70])
    axes[1].plot(n_user_list, sum_rates, "-*", color="red",label="SP")
    axes[1].plot(n_user_list, sum_rates_hh, ":*", color="blue", label="Hungarian_heuristic")
    axes[1].plot(n_user_list, sum_rates_gd, "--*", color="green", label="Greedy")
    axes[1].set_xlim(10, 80)
    axes[1].set_ylim(0, 900)
    axes[1].set_xlabel("Number of users")
    axes[1].set_ylabel("Sum rate [bps/Hz]")
    axes[1].grid()
    axes[1].legend()

    n_test = np.size(np.load(f"sumrates_SP_{n_user}users.npy"))
    wanted_n_user=50
    sumrates_sorted = {"sp": np.sort(np.load(f"sumrates_SP_{wanted_n_user}users.npy")),
                       "hh": np.sort(np.load(f"sumrates_HH_{wanted_n_user}users.npy")),
                       "gd": np.sort(np.load(f"sumrates_GD_{wanted_n_user}users.npy"))}
    cdf_bins = np.arange(n_test)/float(n_test-1)
    axes[0].set_xticks([100, 200, 300, 400, 500, 600])
    axes[0].set_yticks(np.linspace(0, 1, 11))
    axes[0].plot(sumrates_sorted["sp"], cdf_bins, label="SP", color='red')
    axes[0].plot(sumrates_sorted["hh"], cdf_bins, ':', color='blue', label="Hungarian_heuristic")
    axes[0].plot(sumrates_sorted["gd"], cdf_bins, '--', color='green', label="Greedy")
    axes[0].set_xlim(0, 600)
    axes[0].set_ylim(0, 1)
    axes[0].set_xlabel("Sum rate [bps/Hz]")
    axes[0].set_ylabel("CDF")
    axes[0].grid()
    axes[0].legend()
    plt.show()
    return


if __name__=="__main__":
    main()