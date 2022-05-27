import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations
from system_setting import (N_USER, AP_POSITIONS,
                            N_AP, MAX_DISTANCE)
N_RESOURCE = 10
N_CASE = 100
N_ITER = 10
EPS = 10**-6
np.random.seed(0)


def main():
    user_positions = np.load("user_positions.npy")
    user2ap_distances = np.load("user2ap_distances.npy")
    snr = np.load("snr.npy")

    user_list, user_pair_list = get_user_lists()
    x = merge_user_lists(user_list, user_pair_list)
    dimension_i = len(x)
    y = get_y(x, user_positions, snr)
    allocation = np.zeros(shape=(N_ITER, dimension_i))
    alpha_tilde = np.zeros(shape=(N_ITER, dimension_i, N_RESOURCE))
    alpha_bar = np.zeros(shape=(N_ITER, dimension_i, N_RESOURCE))
    rho_tilde = np.zeros(shape=(N_ITER, dimension_i, N_RESOURCE))
    rho_bar = np.zeros(shape=(N_ITER, dimension_i, N_RESOURCE))

    for t in range(1, N_ITER):
        rho_tilde[t], rho_bar[t] = update_rho(
            y, alpha_tilde[t], alpha_bar[t])
        # if t < N_ITER-1:
        #     alpha_tilde[t+1] = update_alpha_tilde()
        #     alpha_bar[t+1] = update_alpha_bar()
        # allocation[t] = make_decision()

        # is_converged = check_convergence(
        #     alpha_tilde[t], alpha_bar[t], rho_tilde[t], rho_bar[t])
        # if is_converged:
        #     print(f"converged at t={t}")
        #     for i in range(dimension_i):
        #         print(f"{x[i]} - {allocation[t, i]}")
        return


def get_user_lists():
    user_list = np.linspace(0, N_USER-1, N_USER, dtype=int)
    perm_idx = permutations(user_list, r=2)
    user_pair_list = np.array(list(perm_idx))
    return user_list, user_pair_list


def merge_user_lists(user_list, user_pair_list):
    x = []
    for user in user_list:
        x.append(user.tolist())
    for user_pair in user_pair_list:
        x.append(user_pair.tolist())
    return x


def get_y(x, user_positions, snr):
    y = np.zeros(shape=(len(x), N_RESOURCE))
    for i in range(len(x)):
        if i < N_USER:
            within_AP_range = np.zeros(N_AP, dtype=bool)
            for j in range(N_AP):
                within_AP_range[j] = check_range(AP_POSITIONS[j], user_positions[i])
            # print(within_AP_range)
        else:
            user_1, user_2 = x[i]
            # print(user_1, user_2)
    return y


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
        neighbor_idx_1 = get_neighbor_indices(x, user1)
        neighbor_idx_2 = get_neighbor_indices(x, user2)
        neighbor_idx_1.remove(idx)
        neighbor_idx_2.remove(idx)

        neighbor_idx_both = [user1, user2] + neighbor_idx_1 + neighbor_idx_2
        neighbor_idx_both.sort()
        return neighbor_idx_both


def check_range(ap_position, user_position):
    distance = np.linalg.norm(ap_position - user_position, 2)
    return MAX_DISTANCE >= distance


def update_rho(y, alpha_tilde_now, alpha_bar_now):
    dim_x = np.size(y, axis=0)
    rho_bar_now = np.zeros(shape=(dim_x, N_RESOURCE))
    rho_tilde_now = np.zeros(shape=(dim_x, N_RESOURCE))
    for i in range(dim_x):
        for r in range(N_RESOURCE):
            alpha_tilde_row_except_ir = np.delete(
                alpha_tilde_now[i], r)
            y_row_except_ir = np.delete(y[i], r)
            rho_tilde_now[i, r] = y[i, r] - np.max(
                y_row_except_ir + alpha_tilde_row_except_ir)
            
            alpha_bar_row_except_ir = np.delete(
                alpha_bar_now[i], r)
            rho_bar_now[i, r] = rho_tilde_now[i, r] + \
                np.sum(alpha_bar_row_except_ir) - y[i, r]
    return rho_bar_now, rho_tilde_now


def update_alpha():
    pass


def make_decision():
    pass


def check_convergence():
    pass


if __name__=="__main__":
    main()
