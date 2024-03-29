import numpy as np
import os
from system_setting import get_throughput
from hungarian import get_sumThroughput_hung_Mbps as get_sumThroughput_greedy_Mbps
MAX_ITER = 10

def main(n_user, n_pilot, seed, save_path):
    np.random.seed(seed)
    user_positions = np.load(os.path.join(save_path, f"seed{seed}-user_pos.npy"))
    beta = np.load(os.path.join(save_path, f"seed{seed}-beta.npy"))
    allocation = np.zeros(shape=(MAX_ITER, n_user), dtype=int)
    allocation[0, :] = random_assignment(n_user, n_pilot)
    for t in range(1, MAX_ITER):
        allocation[t] = allocation[t-1]
        current_rates = get_rates_all(allocation[t], beta, n_pilot)
        lowest_rate_user = np.argmin(current_rates)
        lowest_rate_user_alloc_pilot = allocation[t, lowest_rate_user]
        new_rsc = get_new_pilot(lowest_rate_user, lowest_rate_user_alloc_pilot, allocation[t], n_pilot, beta)
        allocation[t, lowest_rate_user] = new_rsc
        sumThroughput = get_sumThroughput_greedy_Mbps(allocation[t], n_pilot, beta)
    return sumThroughput


def random_assignment(n_user, n_pilot):
    pilots = np.linspace(0, n_pilot-1, n_pilot, dtype=int)
    rand_assign = np.random.choice(pilots, size=n_user)
    idx = np.linspace(0, n_user-1, n_user, dtype=int)
    for pilot in pilots:
        rand_idx = np.random.choice(idx, 1)
        rand_assign[rand_idx] = pilot
    return rand_assign


def get_rates_all(allocation, beta, n_pilot):
    rates = np.zeros(len(allocation))
    for i in range(len(allocation)):
        r = allocation[i]
        neighbors = np.argwhere(allocation==r).reshape(-1)
        neighbors = np.delete(neighbors, np.argwhere(neighbors==i))
        rates[i] = get_throughput(i, neighbors, beta, n_pilot)
    return rates


def get_new_pilot(lowest_user, lowest_pilot, allocation, n_pilot, beta):
    pilots = np.linspace(0, n_pilot-1, n_pilot, dtype=int)
    pilot_comparison = np.zeros(n_pilot)
    for pilot in pilots:
        pilot_assigned_users = np.argwhere(allocation==pilot).reshape(-1)
        if lowest_user in pilot_assigned_users:
            pilot_assigned_users = np.delete(pilot_assigned_users,
                                             np.argwhere(pilot_assigned_users == lowest_user))
        pilot_comparison[pilot] = np.sum(beta[pilot_assigned_users])

    return np.argmin(np.abs(pilot_comparison))


if __name__=="__main__":
    sum_rate = main(
        n_user=9, n_pilot=3,
        seed=0, save_path="debug")
    print(f"Greedy sumThroughput: {sum_rate}Mbps")
