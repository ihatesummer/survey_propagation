import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations
from system_setting import (N_USER, AP_POSITIONS, N_AP,
                            MAX_DISTANCE, ETA,
                            TX_POWER, NOISE_POWER)
N_RESOURCE = 10
N_CASE = 100
np.random.seed(0)


def main():
    user_positions = np.load("user_positions.npy")
    user2ap_distances = np.load("user2ap_distances.npy")
    snr = np.load("snr.npy")

    user_list, user_pair_list = get_user_lists()
    x = merge_user_lists(user_list, user_pair_list)
    idx_test = get_neighbor_indices(x, 20)
    print(idx_test)


def get_user_lists():
    user_list = np.linspace(0, N_USER-1, N_USER, dtype=int)
    perm_idx = permutations(user_list, r=2)
    user_pair_list = np.array(list(perm_idx))
    return user_list, user_pair_list


def get_neighbor_indices(x, idx):
    neighbor_idx = []
    # Neighbors of a single user node
    if idx < N_USER:
        for i in range(N_USER, len(x)):
            if x[idx] in x[i]:
                neighbor_idx.append(i)
        return neighbor_idx

    # Neighbors of user pair node
    else:
        user1 = x[idx][0]
        user2 = x[idx][1]
        user1_neighbor_idx = get_neighbor_indices(x, user1)
        user2_neighbor_idx = get_neighbor_indices(x, user2)
        user1_neighbor_idx.remove(idx)
        user2_neighbor_idx.remove(idx)

        all_neighbor_idx = user1_neighbor_idx + user2_neighbor_idx
        all_neighbor_idx.sort()
        return all_neighbor_idx


def merge_user_lists(user_list, user_pair_list):
    x = []
    for user in user_list:
        x.append(user.tolist())
    for user_pair in user_pair_list:
        x.append(user_pair.tolist())
    return x


if __name__=="__main__":
    main()
