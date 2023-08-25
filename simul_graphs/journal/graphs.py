import numpy as np
import matplotlib.pyplot as plt
import scienceplots
plt.style.use(['science','ieee'])

def main():
    nUser_vs_throughput(nUsers = [15, 30, 45, 60, 75, 90])    
    cdf(nUser = 45)
    return

def nUser_vs_throughput(nUsers: list):
    sum_rates = np.zeros(len(nUsers))
    sum_rates_hh = np.zeros(len(nUsers))
    sum_rates_km = np.zeros(len(nUsers))
    sum_rates_gd = np.zeros(len(nUsers))
    for i, nUser in enumerate(nUsers):
        # sum_rates[i] = np.mean(np.nan_to_num(np.loadtxt(f"sumrates_SP_{n_user}users.csv", delimiter=','), nan=0))
        sum_rates[i] = np.nanmean(np.loadtxt(f"sumrates_SP_{nUser}users.csv", delimiter=','))
        sum_rates_hh[i] = np.mean(np.loadtxt(f"sumrates_HH_{nUser}users.csv", delimiter=','))
        sum_rates_km[i] = np.mean(np.loadtxt(f"sumrates_KM_{nUser}users.csv", delimiter=','))
        sum_rates_gd[i] = np.mean(np.loadtxt(f"sumrates_GD_{nUser}users.csv", delimiter=','))

    _, ax = plt.subplots()
    # ax.set_xticks([10, 20, 30])
    ax.plot(nUsers, sum_rates_gd, "--", color="tab:olive", label="Greedy", 
        markersize=6, marker="|")
    ax.plot(nUsers, sum_rates_km, "--", color="tab:brown", label="K-means", 
        markersize=5, marker="x")
    ax.plot(nUsers, sum_rates_hh, "--", color="tab:red", label="Hungarian", 
        markersize=7, marker="1")
    ax.plot(nUsers, sum_rates, "-", color="tab:blue", label="SP", 
        markersize=3, marker="o")
    ax.set_xlim(15, 90)
    # ax.set_ylim(0, 900)
    ax.set_xlabel("Number of users")
    ax.set_ylabel("System throughput [Mbits/sec]")
    # ax.grid()

    handles, labels = plt.gca().get_legend_handles_labels()
    lengend_order = [3,2,1,0]
    ax.legend([handles[idx] for idx in lengend_order],
              [labels[idx] for idx in lengend_order],
              loc='upper left', ncol=1, fontsize=6,
              columnspacing=1, handlelength=3)
    plt.savefig("user_vs_throughput.png")
    plt.savefig("user_vs_throughput.pdf")
    plt.close()

def cdf(nUser: int):
    sum_rates_sp = np.loadtxt(f"sumrates_SP_{nUser}users.csv", delimiter=',')
    sum_rates_sp = sum_rates_sp[~np.isnan(sum_rates_sp)]
    sum_rates_sorted_sp = np.sort(sum_rates_sp)
    sum_rates_sorted_hh = np.sort(np.loadtxt(f"sumrates_HH_{nUser}users.csv", delimiter=','))
    sum_rates_sorted_km = np.sort(np.loadtxt(f"sumrates_KM_{nUser}users.csv", delimiter=','))
    sum_rates_sorted_gd = np.sort(np.loadtxt(f"sumrates_GD_{nUser}users.csv", delimiter=','))

    n_test = len(sum_rates_sorted_hh)
    cdf_bins = np.arange(n_test)/float(n_test-1)
    n_test_sp = len(sum_rates_sorted_sp)
    cdf_bins_sp = np.arange(n_test_sp)/float(n_test_sp-1)

    _, ax = plt.subplots()
    # ax2.set_xticks([100, 200, 300, 400, 500, 600])
    # ax2.set_yticks(np.linspace(0, 1, 11))
    ax.plot(sum_rates_sorted_sp, cdf_bins_sp, "-", color="tab:blue", label="SP")
    ax.plot(sum_rates_sorted_hh, cdf_bins, ':', color="tab:red", label="Hungarian")
    ax.plot(sum_rates_sorted_km, cdf_bins, '-.', color="tab:brown", label="K-means")
    ax.plot(sum_rates_sorted_gd, cdf_bins, '--', color="tab:olive", label="Greedy")
    ax.set_xlim(700, 1100)
    ax.set_ylim(0, 1)
    ax.set_xlabel("System throughput [Mbits/sec]")
    ax.set_ylabel("CDF")
    # ax2.grid()
    ax.legend(loc='upper left', ncol=1, fontsize=6,
              columnspacing=1, handlelength=3)
    plt.savefig("cdf.png")
    plt.savefig("cdf.pdf")
    plt.close()


if __name__=="__main__":
    main()