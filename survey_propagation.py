import numpy as np
import json
import time
import os

np.set_printoptions(precision=2)
INFIN = 10**60

def main(nUser, nPilot, max_iter, damping, converge_thresh, seed, save_path):
    if save_path == "debug":
        bDebug = True
    else:
        bDebug = False

    x, neighbor_mapping, x_j0, y, y_normalizer, occupancy = read_files(save_path, seed)
    # for idx, user_list in enumerate(x):
    #     print(f"index {idx}: user(s) {user_list}")
    dim_x = len(x)
    (neighbor_mapping_matrix,
     j_prime_matrix, j0_prime_matrix,
     row_window, j0_window) = preCalculate_matrices(dim_x, nPilot,
                                                    neighbor_mapping, x_j0)

    alpha_tilde = np.zeros(shape=(max_iter, dim_x, nPilot))
    alpha_bar = np.zeros(shape=(max_iter, dim_x, nPilot))
    rho_tilde = np.zeros(shape=(max_iter, dim_x, nPilot))
    rho_bar = np.zeros(shape=(max_iter, dim_x, nPilot))
    allocation = np.zeros(shape=(max_iter, dim_x))

    bFeasibleSolution_found = False
    tic = time.time()
    for t in range(1, max_iter):
        if bDebug:
            print("."*10 + f"t={t}" + "."*10)
        rho_tilde[t], rho_bar[t] = update_rho(y, alpha_tilde[t], alpha_bar[t])
        rho_tilde[t] = damping*rho_tilde[t-1] + (1-damping)*rho_tilde[t]
        rho_bar[t] = damping*rho_bar[t-1] + (1-damping)* rho_bar[t]
        if t < max_iter-1:
            alpha_tilde[t+1], alpha_bar[t+1] = update_alpha(
                neighbor_mapping_matrix, j_prime_matrix, j0_prime_matrix,
                row_window, j0_window, rho_tilde[t], rho_bar[t])
            alpha_tilde[t+1] = damping*alpha_tilde[t] + (1-damping)*alpha_tilde[t+1]
            alpha_bar[t+1] = damping*alpha_bar[t] + (1-damping)*alpha_bar[t+1]

        allocation[t] = make_decision(x, alpha_tilde[t], alpha_bar[t], rho_tilde[t], rho_bar[t])
        (nDuplicate_pilots,
         nDuplicate_users,
         nUnused_pilots,
         nUnassigned_users) = evaluate_decision(x, occupancy, nUser, nPilot, allocation[t], bDebug)
        if nDuplicate_pilots == nDuplicate_users == nUnused_pilots == nUnassigned_users == 0:
        # if nDuplicate_pilots == nDuplicate_users == 0:
            bFeasibleSolution_found = True
            sum_throughput = get_sum_throughput_Mbps(y, allocation[t]) * y_normalizer
        bConverged = check_convergence(
            t, alpha_tilde, alpha_bar, rho_tilde, rho_bar, converge_thresh)
        if bConverged:
            sum_throughput = get_sum_throughput_Mbps(y, allocation[t]) * y_normalizer
            convergence_time = time.time() - tic
            break
    
    if bDebug:
        np.save(os.path.join(save_path, "msg_alpha_tilde.npy"), alpha_tilde)
        np.save(os.path.join(save_path, "msg_alpha_bar.npy"), alpha_bar)
        np.save(os.path.join(save_path, "msg_rho_tilde.npy"), rho_tilde)
        np.save(os.path.join(save_path, "msg_rho_bar.npy"), rho_bar)
        if bConverged:
            print(f"Converged sumrate({t}itr): {sum_throughput:.2f}")
        else:
            if bFeasibleSolution_found:
                print(f"Not converged, feasible sumrate: {sum_throughput:.2f}")
            else:
                print(f"Not converged, no feasible solution")
        return None
    else:
        if bConverged:
            return convergence_time, t, sum_throughput
        else:
            if bFeasibleSolution_found:
                return time.time() - tic, max_iter, sum_throughput
            else:
                return time.time() - tic, max_iter, None


def read_files(save_path, seed):
    with open(os.path.join(save_path, f"seed{seed}-x_neighbors.json"), 'r') as f:
        neighbor_mapping = json.load(f)
    with open(os.path.join(save_path, f"seed{seed}-x_j0.json"), 'r') as f:
        x_j0 = json.load(f)
    occupancy = np.load(os.path.join(save_path, f"seed{seed}-occupancy.npy"))
    x = np.load(os.path.join(save_path, f"seed{seed}-x.npy"))
    y = np.load(os.path.join(save_path, f"seed{seed}-y.npy"))
    y_normalizer = np.max(y)
    y = y / y_normalizer
    return x, neighbor_mapping, x_j0, y, y_normalizer, occupancy


def preCalculate_matrices(dim_x, n_pilot, neighbor_mapping, x_j0):
    neighbor_mapping_matrix = np.zeros((dim_x, dim_x), dtype=int)
    j0_prime_matrix = np.zeros((dim_x, dim_x, dim_x), dtype=int)
    j0_window = np.zeros((dim_x, dim_x, n_pilot), dtype=int)
    for i in range(dim_x):
        neighbor_mapping_matrix[i, neighbor_mapping[i]] = 1
        j0_window[i, x_j0[i], :] = 1
        for j0 in x_j0[i]:
            j0_prime = list(set(neighbor_mapping[j0]) - set(neighbor_mapping[i]))
            j0_prime_matrix[i, j0, j0_prime] = 1
    # print(neighbor_mapping_matrix)
    j_prime_matrix = np.tile(neighbor_mapping_matrix, (dim_x, 1, 1))
    col_window = 1 - np.tile(np.expand_dims(np.eye(dim_x, dtype=int), axis=1), (1, dim_x, 1))
    j_prime_matrix[col_window==0] = 0
    row_window = 1 - np.tile(np.expand_dims(np.eye(dim_x), axis=2), n_pilot)
    return neighbor_mapping_matrix, j_prime_matrix, j0_prime_matrix, row_window, j0_window

def update_rho(y, alpha_tilde_now, alpha_bar_now):
    dim_x, n_pilot = np.shape(y)
    rho_bar_now = np.zeros(shape=(dim_x, n_pilot))
    rho_tilde_now = np.zeros(shape=(dim_x, n_pilot))
    for r in range(n_pilot):
        tic = time.time()
        alpha_tilde_except_r = np.delete(alpha_tilde_now, r, axis=1)
        alpha_bar_except_r = np.delete(alpha_bar_now, r, axis=1)
        y_except_r = np.delete(y, r, axis=1)
        rho_tilde_now[:, r] = y[:, r] + np.sum(
            alpha_tilde_except_r - alpha_bar_except_r, axis=1)
        rho_bar_now[:, r] = y[:, r] - np.max(
            y_except_r + alpha_bar_except_r, axis=1)
    return rho_tilde_now, rho_bar_now


def update_alpha(neighbor_mapping_matrix, j_prime_matrix, j0_prime_matrix,
                 row_window, j0_window, rho_tilde_now, rho_bar_now):
    dim_x, _ = np.shape(rho_tilde_now)
    rho_BarMinusTilde_n = np.minimum(rho_bar_now - rho_tilde_now, 0)
    rho_BarMinusTilde_p = np.maximum(rho_bar_now - rho_tilde_now, 0)
    rho_bar_tile = np.tile(rho_bar_now, (dim_x, 1, 1))
    rho_BarMinusTilde_p_tile = np.tile(rho_BarMinusTilde_p, (dim_x, 1, 1))
    rho_BarMinusTilde_n_tile = np.tile(rho_BarMinusTilde_n, (dim_x, 1, 1))
    j_prime_term_tile = np.matmul(j_prime_matrix, rho_BarMinusTilde_n_tile)
    j0_prime_term_tile = np.matmul(j0_prime_matrix, rho_BarMinusTilde_n_tile)
    
    term1 = np.matmul(neighbor_mapping_matrix, rho_BarMinusTilde_n)
    term2 = -rho_bar_tile + rho_BarMinusTilde_p_tile - j_prime_term_tile
    term2[row_window==0] = INFIN
    alpha_tilde_next = term1 + np.minimum(np.min(term2, axis=1), 0)
    
    term3 = -rho_bar_tile + rho_BarMinusTilde_p_tile - j0_prime_term_tile
    term3[j0_window==0] = INFIN
    alpha_bar_next = np.minimum(np.min(term3, axis=1), 0)

    return alpha_tilde_next, alpha_bar_next


def make_decision(x, alpha_tilde_now, alpha_bar_now,
                  rho_tilde_now, rho_bar_now):
    dim_x = len(x)
    dim_r = np.size(alpha_tilde_now, axis=1)
    allocation = np.zeros(dim_x)

    b_tilde = alpha_tilde_now + rho_tilde_now
    b_bar = alpha_bar_now + rho_bar_now
    for i in range(dim_x):
        if np.max(b_tilde[i, :]) > 0:
            allocation[i] = np.argmax(b_bar[i, :])
        else:
            allocation[i] = None
    for r in range(dim_r):
        if np.count_nonzero(allocation==r) == 0:
            i_argmax = np.argmax(b_tilde[:, r])
            allocation[i_argmax] = r
    return allocation


def evaluate_decision(x, occupancy, nUser, nPilot, current_allocation, bDebug):
    idx_alloc_group = np.argwhere(np.isnan(current_allocation)==False).flatten()
    idx_alloc_pilot = current_allocation[idx_alloc_group].astype(int)
    sorting_by_pilot = idx_alloc_pilot.argsort()
    alloc_table = np.vstack((idx_alloc_pilot[sorting_by_pilot],
                             idx_alloc_group[sorting_by_pilot]))
    assigned_users = x[idx_alloc_group].flatten()

    nPrealloc_users = len(occupancy)
    nUnique_pilots = np.size(np.unique(idx_alloc_pilot))
    nUnique_users = np.size(np.unique(assigned_users))
    nDuplicate_pilots = len(idx_alloc_pilot) - nUnique_pilots
    nDuplicate_users = len(assigned_users) - nUnique_users
    nUnused_pilots = nPilot-len(idx_alloc_pilot)
    nUnassigned_users = nUser-nPrealloc_users-nUnique_users
    if bDebug:
        for i in range(alloc_table.shape[1]):
            pilot_no, assigned_group_idx = alloc_table[:, i]
            preassigned_user_idx = occupancy[pilot_no]
            print(f"Pilot{pilot_no}<= users {preassigned_user_idx}+"
                    f"{x[assigned_group_idx]} (idx {assigned_group_idx})")
        print(f"#duplicate pilot: {nDuplicate_pilots} || "
              f"#duplicate user:  {nDuplicate_users}\n"
              f"#unused pilot:    {nUnused_pilots} || "
              f"#unassigned user: {nUnassigned_users}")

    return nDuplicate_pilots, nDuplicate_users, nUnused_pilots, nUnassigned_users


def check_convergence(t, alpha_tilde, alpha_bar, rho_tilde, rho_bar, converge_thresh):
    alpha_tilde_converged = (np.abs(alpha_tilde[t] - alpha_tilde[t-1]) < converge_thresh).all()
    alpha_bar_converged = (np.abs(alpha_bar[t] - alpha_bar[t-1]) < converge_thresh).all()
    rho_tilde_converged = (np.abs(rho_tilde[t] - rho_tilde[t-1]) < converge_thresh).all()
    rho_bar_converged = (np.abs(rho_bar[t] - rho_bar[t-1]) < converge_thresh).all()

    alpha_converged = alpha_tilde_converged and alpha_bar_converged
    rho_converged = rho_tilde_converged and rho_bar_converged

    return alpha_converged and rho_converged


def get_sum_throughput_Mbps(y, converged_allocation):
    sum_rate = 0
    for i, r in enumerate(converged_allocation):
        if not (np.isnan(converged_allocation[i])):
            sum_rate += y[i, int(r)]
    return sum_rate * 10**-6


if __name__=="__main__":
    main(nUser=9, nPilot=3, max_iter=100, damping=0.5,
         converge_thresh=10**-2, seed=9, save_path="debug")
