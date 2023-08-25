import numpy as np
import matplotlib.pyplot as plt


def main():
    n_user_list = [15, 30, 45, 60, 75]
    wanted_n_user=30
    sumrates_sorted = {"sp": np.sort(np.loadtxt(f"sumrates_SP_{wanted_n_user}users.csv"))*3,
                       "hh": np.sort(np.loadtxt(f"sumrates_HH_{wanted_n_user}users.csv"))*3,
                       "gd": np.sort(np.loadtxt(f"sumrates_GD_{wanted_n_user}users.csv"))*3}
    # sumrates_sorted["sp"] = sumrates_sorted["sp"][~np.isnan(sumrates_sorted["sp"])]
    _, ax = plt.subplots(tight_layout=True)
    n_test_sp = np.size(sumrates_sorted["sp"])
    n_test_hh = np.size(sumrates_sorted["hh"])
    n_test_gd = np.size(sumrates_sorted["gd"])
    cdf_bins_sp = np.arange(n_test_sp)/float(n_test_sp-1)
    cdf_bins_hh = np.arange(n_test_hh)/float(n_test_hh-1)
    cdf_bins_gd = np.arange(n_test_gd)/float(n_test_gd-1)
    ax.plot(sumrates_sorted["sp"], cdf_bins_sp, color='red', label="SP")
    ax.plot(sumrates_sorted["hh"], cdf_bins_hh, ':', color='blue', label="Hungarian")
    ax.plot(sumrates_sorted["gd"], cdf_bins_gd, '--', color='green', label="Greedy")
    ax.set_yticks(np.linspace(0, 1, 11))
    major_ticks = [600, 700, 800, 900, 1000, 1100, 1200]
    # minor_ticks = [700, 900, 1100]
    ax.set_xticks(major_ticks)
    # ax.set_xticks(minor_ticks, minor=True)
    ax.set_xlim(600, 1200)
    ax.set_ylim(0, 1)
    ax.set_xlabel("System throughput [Mbps/Hz]")
    ax.set_ylabel("CDF")
    # ax.grid(which='minor', alpha=0.5)
    ax.grid(which='major', alpha=1)
    ax.legend()
    plt.show()
    # plt.savefig("cdf.pdf")
    # plt.savefig("cdf.png")
    return


if __name__=="__main__":
    main()