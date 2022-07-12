import numpy as np
import matplotlib.pyplot as plt
from main import N_REPEAT

def main():
    n_user_list = [10, 20, 30, 40, 50, 60, 70, 80]
    sum_rates = np.zeros(len(n_user_list))
    sum_rates_hh = np.zeros(len(n_user_list))
    sum_rates_gd = np.zeros(len(n_user_list))
    for i, n_user in enumerate(n_user_list):
        sum_rates[i] = np.nanmean(np.load(f"sumrates_SP_{n_user}users.npy"))
        sum_rates_hh[i] = np.mean(np.load(f"sumrates_HH_{n_user}users.npy"))
        sum_rates_gd[i] = np.mean(np.load(f"sumrates_GD_{n_user}users.npy"))

    plt.plot(n_user_list, sum_rates, "-*", label="SP")
    plt.plot(n_user_list, sum_rates_hh, "-*", label="Hungarian_heuristic")
    plt.plot(n_user_list, sum_rates_gd, "-*", label="Greedy")
    plt.xlim(10, 60)
    plt.legend()
    plt.grid()
    plt.show()



if __name__=="__main__":
    main()