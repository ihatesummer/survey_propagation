import numpy as np
import matplotlib.pyplot as plt
plt.style.use(['science','ieee'])


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

    _, axes = plt.subplots(nrows=1, ncols=2,
                           tight_layout=True)
    axes[1].set_xticks([15, 30, 45, 60, 75])
    axes[1].plot(n_user_list, sum_rates*3, "-*", color="red",label="SP")
    axes[1].plot(n_user_list, sum_rates_hh*3, ":*", color="blue", label="Hungarian")
    axes[1].plot(n_user_list, sum_rates_gd*3, "--*", color="green", label="Greedy")
    axes[1].set_xlim(15, 75)
    axes[1].set_ylim(300, 2500)
    axes[1].set_xlabel("Number of users")
    axes[1].set_ylabel("System throughput[Mbps/Hz]")
    axes[1].grid()
    axes[1].legend()

    wanted_n_user=30
    sumrates_sorted = {"sp": np.sort(np.loadtxt(f"sumrates_SP_{wanted_n_user}users.csv"))*3,
                       "hh": np.sort(np.loadtxt(f"sumrates_HH_{wanted_n_user}users.csv"))*3,
                       "gd": np.sort(np.loadtxt(f"sumrates_GD_{wanted_n_user}users.csv"))*3}
    # sumrates_sorted["sp"] = np.sort(np.nan_to_num(sumrates_sorted["sp"], nan=300))
    sumrates_sorted["sp"] = sumrates_sorted["sp"][~np.isnan(sumrates_sorted["sp"])]
    n_test_sp = np.size(sumrates_sorted["sp"])
    n_test_hh = np.size(sumrates_sorted["hh"])
    n_test_gd = np.size(sumrates_sorted["gd"])
    cdf_bins_sp = np.arange(n_test_sp)/float(n_test_sp-1)
    cdf_bins_hh = np.arange(n_test_hh)/float(n_test_hh-1)
    cdf_bins_gd = np.arange(n_test_gd)/float(n_test_gd-1)
    axes[0].set_xticks([200, 300, 400])
    axes[0].set_yticks(np.linspace(0, 1, 11))
    axes[0].plot(sumrates_sorted["sp"], cdf_bins_sp, color='red', label="SP")
    axes[0].plot(sumrates_sorted["hh"], cdf_bins_hh, ':', color='blue', label="Hungarian")
    axes[0].plot(sumrates_sorted["gd"], cdf_bins_gd, '--', color='green', label="Greedy")
    major_ticks = [600, 800, 1000, 1200]
    minor_ticks = [700, 900, 1100]
    axes[0].set_xticks(major_ticks)
    axes[0].set_xticks(minor_ticks, minor=True)
    axes[0].set_xlim(600, 1200)
    axes[0].set_ylim(0, 1)
    axes[0].set_xlabel("System throughput [Mbps/Hz]")
    axes[0].set_ylabel("CDF")
    axes[0].grid(which='minor', alpha=0.5)
    axes[0].grid(which='major', alpha=1)
    axes[0].legend()
    # plt.show()
    plt.savefig("result.pdf")
    plt.savefig("result.png")
    return

if __name__=="__main__":
    main()
