import numpy as np
import json
import time
import os


def main(n_user, n_resource, max_iter, damping, converge_thresh, seed, save_path):
    np.random.seed(seed)
    x, neighbor_mapping, x_j0, y, y_normalizer = read_files(save_path, seed)
    
    # for idx, user_list in enumerate(x):
    #     print(f"index {idx}: user(s) {user_list}")
    dim_x = len(x)
    alpha_tilde = np.zeros(shape=(max_iter, dim_x, n_resource))
    alpha_bar = np.zeros(shape=(max_iter, dim_x, n_resource))
    rho_tilde = np.zeros(shape=(max_iter, dim_x, n_resource))
    rho_bar = np.zeros(shape=(max_iter, dim_x, n_resource))
    allocation = np.zeros(shape=(max_iter, dim_x))

    tic = time.time()
    for t in range(1, max_iter):
        rho_tilde[t], rho_bar[t] = update_rho(
            y, alpha_tilde[t], alpha_bar[t])
        rho_tilde[t] = damping*rho_tilde[t-1] + (1-damping)*rho_tilde[t]
        rho_bar[t] = damping*rho_bar[t-1] + (1-damping)* rho_bar[t]
        if t < max_iter-1:
            alpha_tilde[t+1], alpha_bar[t+1] = update_alpha(
                neighbor_mapping, x_j0, rho_tilde[t], rho_bar[t])
            alpha_tilde[t+1] = damping*alpha_tilde[t] + (1-damping)*alpha_tilde[t+1]
            alpha_bar[t+1] = damping*alpha_bar[t] + (1-damping)*alpha_bar[t+1]
        if save_path=="debug":
            allocation[t] = make_decision(
                x, alpha_tilde[t], alpha_bar[t], rho_tilde[t], rho_bar[t])
            print_allocation(x, t, allocation[t], n_user, n_resource)
            sum_rate = get_sum_rate(y, allocation[t])
            print(f"Sumrate: {sum_rate}")
        is_converged = check_convergence(
            t, alpha_tilde, alpha_bar, rho_tilde, rho_bar, converge_thresh)
        if is_converged:
            convergence_time = time.time() - tic
            allocation[t] = make_decision(
                x, alpha_tilde[t], alpha_bar[t], rho_tilde[t], rho_bar[t])
            sum_rate = get_sum_rate(y, allocation[t])
            if save_path=="debug":
                np.save("msg_alpha_tilde.npy", alpha_tilde[1:t+1, :, :])
                np.save("msg_alpha_bar.npy", alpha_bar[1:t+1, :, :])
                np.save("msg_rho_tilde.npy", rho_tilde[1:t+1, :, :])
                np.save("msg_rho_bar.npy", rho_bar[1:t+1, :, :])
                np.save("allocation.npy", allocation[t, :])
            return convergence_time, t, sum_rate
    return time.time() - tic, max_iter, None


def read_files(save_path, seed):
    with open(os.path.join(save_path, f"x_{seed}.json"), 'r') as f:
        x = json.load(f)
    with open(os.path.join(save_path, f"x_neighbors_{seed}.json"), 'r') as f:
        neighbor_mapping = json.load(f)
    with open(os.path.join(save_path, f"x_j0_{seed}.json"), 'r') as f:
        x_j0 = json.load(f)
    y = np.load(os.path.join(save_path, f"y_{seed}.npy"))
    y_normalizer = np.max(y)
    y = y / y_normalizer
    return x, neighbor_mapping, x_j0, y, y_normalizer


def update_rho(y, alpha_tilde_now, alpha_bar_now):
    dim_x, n_resource = np.shape(y)
    rho_bar_now = np.zeros(shape=(dim_x, n_resource))
    rho_tilde_now = np.zeros(shape=(dim_x, n_resource))

    for r in range(n_resource):
        alpha_tilde_except_r = np.delete(alpha_tilde_now, r, axis=1)
        alpha_bar_row_except_r = np.delete(alpha_bar_now, r, axis=1)
        y_except_r = np.delete(y, r, axis=1)
        rho_tilde_now[:, r] = y[:, r] - np.max(
            y_except_r + alpha_tilde_except_r, axis=1)
        rho_bar_now[:, r] = rho_tilde_now[:, r] + np.sum(
            alpha_bar_row_except_r, axis=1) - y[:, r]
    return rho_tilde_now, rho_bar_now


def update_alpha(neighbor_mapping, x_j0, rho_tilde_now, rho_bar_now):
    dim_x, n_resource = np.shape(rho_tilde_now)
    alpha_tilde_next = np.zeros(shape=(dim_x, n_resource))
    alpha_bar_next = np.zeros(shape=(dim_x, n_resource))
    for i in range(dim_x):
        j0_compare_alpha_tilde = np.zeros(n_resource) # placeholder
        j0_compare_A_i_2 = np.zeros(n_resource) # placeholder
        for j0 in x_j0[i]:
            j0_prime = list(
                set(neighbor_mapping[j0]) - set(neighbor_mapping[i]))
            j0_prime_prime = list(
                set(neighbor_mapping[i]) - set(neighbor_mapping[j0]) - set([j0]))
            comparison_term = - rho_tilde_now[j0, :] \
                 + np.maximum(rho_bar_now[j0, :], 0) \
                 - np.sum(np.minimum(rho_bar_now[j0_prime, :], 0), axis=0)
            j0_compare_alpha_tilde = np.row_stack(
                (j0_compare_alpha_tilde, comparison_term))
            j0_compare_A_i_2 = np.row_stack(
                (j0_compare_A_i_2, - comparison_term 
                 - np.sum(np.minimum(rho_bar_now[j0_prime_prime, :], 0), axis=0)))
        j0_compare_alpha_tilde = np.delete(
            j0_compare_alpha_tilde, 0, axis=0)  # remove placeholder
        alpha_tilde_next[i, :] = np.minimum(
            np.min(j0_compare_alpha_tilde, axis=0), 0)

        jn_compare = np.zeros(n_resource) # placeholder, comparison list for A_ir(1)
        for jn in neighbor_mapping[i]:
            jn_prime = list(
                set(neighbor_mapping[jn]) - set(neighbor_mapping[i]) - set([i]))
            jn_prime_prime = list(
                set(neighbor_mapping[i]) - set(neighbor_mapping[jn]) - set([jn]))
            jn_compare = np.row_stack(
                (jn_compare,
                 + rho_tilde_now[jn, :]
                 - rho_bar_now[jn, :]
                 + np.sum(np.minimum(rho_bar_now[jn_prime, :], 0), axis=0)
                 - np.sum(np.minimum(rho_bar_now[jn_prime_prime, :], 0), axis=0)))
        jn_compare = np.delete(jn_compare, 0, axis=0) # remove placeholder
        j0_compare_A_i_2 = np.delete(j0_compare_A_i_2, 0, axis=0)  # remove placeholder
        if len(neighbor_mapping[i]) != 0:
            A_i_1 = np.max(jn_compare, axis=0)
            neg_sum_term = -np.sum(
                np.minimum(rho_bar_now[neighbor_mapping[i], :], 0),
                axis=0)
        else:
            A_i_1 = np.zeros(n_resource)
            neg_sum_term = np.zeros(n_resource)
        if len(x_j0[i]) != 0:
            A_i_2 = np.max(j0_compare_A_i_2, axis=0)
        else:
            A_i_2 = np.zeros(n_resource)
        alpha_bar_next[i, :] = np.maximum.reduce(
            [A_i_1, A_i_2, neg_sum_term]) + alpha_tilde_next[i, :]
    return alpha_tilde_next, alpha_bar_next


def make_decision(x, alpha_tilde_now, alpha_bar_now,
                  rho_tilde_now, rho_bar_now):
    dim_x = len(x)
    allocation = np.zeros(dim_x)
    b_tilde = np.zeros(dim_x)
    b_bar = np.zeros(dim_x)
    for i in range(dim_x):
        b_tilde[i] = np.max(rho_tilde_now[i] + alpha_tilde_now[i])
        b_bar[i] = np.max(rho_bar_now[i] + alpha_bar_now[i])
        if b_tilde[i] > b_bar[i]:
            allocation[i] = np.argmax(rho_tilde_now[i] + alpha_tilde_now[i])
        else:
            allocation[i] = None
    return allocation


def print_allocation(x, t, current_allocation, n_user, n_resource):
    print("."*10 + f"t={t}" + "."*10)
    used_resource_count = 0
    used_resource_list = np.array([], dtype=int)
    assigned_user_list = np.array([], dtype=int)
    for i in range(len(x)):
        if not (np.isnan(current_allocation[i])):
            print(f"idx {i}, user(s) {x[i]}: resource {int(current_allocation[i])}")
            used_resource_list = np.append(used_resource_list,
                                           int(current_allocation[i]))
            assigned_user_list = np.append(assigned_user_list, x[i])
            used_resource_count += 1
    used_resource_count_unique = np.size(np.unique(used_resource_list))
    n_duplicate_resource = used_resource_count - used_resource_count_unique
    assigned_user_count_unique = np.size(np.unique(assigned_user_list))
    n_duplicate_user = np.size(assigned_user_list) - assigned_user_count_unique
    print(f"#duplicate rsc: {n_duplicate_resource} || " + 
          f"#duplicate usr: {n_duplicate_user}\n" + 
          f"#unused rsc: {n_resource-used_resource_count} || "
          f"#unassigned usr: {n_user-assigned_user_count_unique}")


def check_convergence(t, alpha_tilde, alpha_bar, rho_tilde, rho_bar, converge_thresh):
    alpha_tilde_converged = (np.abs(alpha_tilde[t] - alpha_tilde[t-1]) < converge_thresh).all()
    alpha_bar_converged = (np.abs(alpha_bar[t] - alpha_bar[t-1]) < converge_thresh).all()
    rho_tilde_converged = (np.abs(rho_tilde[t] - rho_tilde[t-1]) < converge_thresh).all()
    rho_bar_converged = (np.abs(rho_bar[t] - rho_bar[t-1]) < converge_thresh).all()

    alpha_converged = alpha_tilde_converged and alpha_bar_converged
    rho_converged = rho_tilde_converged and rho_bar_converged

    return alpha_converged and rho_converged


def get_sum_rate(y, converged_allocation):
    sum_rate = 0
    for i, r in enumerate(converged_allocation):
        if not (np.isnan(converged_allocation[i])):
            sum_rate += y[i, int(r)]
    return sum_rate


if __name__=="__main__":
    convergence_time, n_iter, sum_rate = main(
        n_user=30, n_resource=20, max_iter=1000, damping=0.3,
        converge_thresh=10**-2, seed=0, save_path="debug")
    print(f"converged in {convergence_time}s/{n_iter}itr, sum rate {sum_rate}")
