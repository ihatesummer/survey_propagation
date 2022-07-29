import numpy as np
import os
import json
from scipy.optimize import linear_sum_assignment
from system_setting import get_throughput
from itertools import combinations
MAX_ITER = 5

def main(n_user, n_pilot, seed, save_path):
    np.random.seed(seed)
    user_positions = np.load(os.path.join(save_path, f"user_positions_{seed}.npy"))
    beta = np.load(os.path.join(save_path, f"beta_{seed}.npy"))
    allocation = np.zeros(shape=(MAX_ITER, n_user), dtype=int)
    allocation[0, :] = random_assignment(n_user, n_pilot)
    users = np.linspace(0, n_user-1, n_user, dtype=int)
    user_order = np.linspace(0, n_user-1, n_user, dtype=int)
    np.random.shuffle(user_order)
    closest_n_foreach = get_closest_n(user_positions, n_pilot)

    n_identical_assignment = 0
    for t in range(1, MAX_ITER):
        allocation[t] = allocation[t-1]
        for user in user_order:
            neighbors = closest_n_foreach[user]
            non_neighbors = np.array(list(set(users) - set(neighbors)))
            y_hung = get_y_hung(n_pilot, neighbors, non_neighbors, allocation[t], beta)
            user_idx, res_idx = linear_sum_assignment(y_hung, maximize=True)
            for n, r in zip(neighbors[user_idx], res_idx):
                allocation[t, n] = r
        if np.all(allocation[t-1] == allocation[t]):
            n_identical_assignment += 1
            if n_identical_assignment > 10:
                break
    sumrate = get_sumrate_hung(allocation[t], n_pilot, beta)
    return sumrate


def get_closest_n(positions, n):
    n_users = np.size(positions, axis=0)
    closest_n_foreach = np.zeros((n_users, n), dtype=int)
    for i, pos in enumerate(positions):
        distances_to_others = np.linalg.norm(positions - pos, 2, axis=1)
        closest_n = np.argsort(distances_to_others)[:n]
        closest_n_foreach[i] = closest_n
    return np.sort(closest_n_foreach)


def random_assignment(n_user, n_pilot):
    pilots = np.linspace(0, n_pilot-1, n_pilot, dtype=int)
    n_roommate = int(n_user/n_pilot)
    assignment = np.array([])
    for _ in range(n_roommate):
        np.random.shuffle(pilots)
        assignment = np.append(assignment, pilots)
    np.random.shuffle(assignment)
    return assignment


def get_y_hung(n_pilot, neighbors, non_neighbors, current_allocation, beta):
    y = np.zeros(shape=(len(neighbors), n_pilot))
    alloc = current_allocation[non_neighbors]
    for i, user in enumerate(neighbors):
        for r in range(n_pilot):
            roommates = non_neighbors[np.argwhere(alloc==r).reshape(-1)]
            y[i, r] = get_throughput(user, roommates, beta, n_pilot)
    return y


def get_sumrate_hung(current_alloc, n_pilot, beta):
    sumrate = 0
    for r in range(n_pilot):
        r_users = np.argwhere(current_alloc==r).reshape(-1)
        if len(r_users) <= 1:
            continue
        pair_configs = np.array(list(combinations(r_users, len(r_users)-1)))
        for comb in pair_configs:
            room_head = list(set(r_users)-set(comb))[0]
            if len(comb) != 0:
                sumrate += get_throughput(room_head, comb, beta, n_pilot)
    return sumrate


if __name__=="__main__":
    sum_rate = main(
        n_user=10, n_pilot=5,
        seed=0, save_path="debug")
    print(f"Hungarian sumrate: {sum_rate}s")
