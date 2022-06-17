import numpy as np
import matplotlib.pyplot as plt
from system_setting import (N_USER, AP_POSITIONS,
                            N_AP, MAX_DISTANCE,
                            N_RESOURCE, get_x)

N_CASE = 100
N_ITER = 100
EPS = 10**-6
DAMP = 0.2 # 0 for no damp (full change), 1 for full damp (no change)
np.random.seed(0)


def main():
    # user_positions = np.load("user_positions.npy")
    # user2ap_distances = np.load("ap2user_distances.npy")
    x = get_x()
    y = np.load("y.npy")
    y = y / np.max(y)
    dim_x = len(x)
    print("y,\n", y)
    allocation = np.zeros(shape=(N_ITER, dim_x))
    alpha_tilde = np.zeros(shape=(N_ITER, dim_x, N_RESOURCE))
    alpha_bar = np.zeros(shape=(N_ITER, dim_x, N_RESOURCE))
    rho_tilde = np.zeros(shape=(N_ITER, dim_x, N_RESOURCE))
    rho_bar = np.zeros(shape=(N_ITER, dim_x, N_RESOURCE))

    for t in range(1, N_ITER):
        rho_tilde[t], rho_bar[t] = update_rho(
            y, alpha_tilde[t], alpha_bar[t])
        rho_tilde[t] = DAMP*rho_tilde[t-1] + (1-DAMP)*rho_tilde[t]
        rho_bar[t] = DAMP*rho_bar[t-1] + (1-DAMP)* rho_bar[t]
        # print("rho_tilde,\n", rho_tilde[t])
        # print("rho_bar,\n", rho_bar[t])
        if t == 99:
            np.savetxt(f"rho_tilde_{t}.csv", rho_tilde[t], delimiter=',')
            np.savetxt(f"rho_bar_{t}.csv", rho_bar[t], delimiter=',')
        if t < N_ITER-1:
            alpha_tilde[t+1], alpha_bar[t+1] = update_alpha(
                x, rho_tilde[t], rho_bar[t])
            alpha_tilde[t+1] = DAMP*alpha_tilde[t] + (1-DAMP)*alpha_tilde[t+1]
            alpha_bar[t+1] = DAMP*alpha_bar[t] + (1-DAMP)*alpha_bar[t+1]

            # print("alpha_t ilde,\n", alpha_tilde[t+1, 0])
            # print("alpha_bar,\n", alpha_bar[t+1, 0])
            if t == 98:
                np.savetxt(f"alpha_tilde_{t+1}.csv", alpha_tilde[t+1], delimiter=',')
                np.savetxt(f"alpha_bar_{t+1}.csv", alpha_bar[t+1], delimiter=',')

        allocation[t] = make_decision(x, alpha_tilde[t], alpha_bar[t], rho_tilde[t], rho_bar[t])
        print_allocation(x, t, allocation[t])
        # is_converged = check_convergence(
        #     alpha_tilde[t], alpha_bar[t], rho_tilde[t], rho_bar[t])
        # if is_converged:
        #     print(f"converged at t={t}")
        #     for i in range(dimension_i):
        #         print(f"{x[i]} - {allocation[t, i]}")
        # return
    # show_mp_traj(x, alpha_tilde, alpha_bar, rho_tilde, rho_bar)
    show_mp_traj_one(6, 1, alpha_tilde, alpha_bar, rho_tilde, rho_bar)

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
        if idx in neighbor_idx_1:
            neighbor_idx_1.remove(idx)
        if idx in neighbor_idx_2:
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
    return rho_tilde_now, rho_bar_now


def update_alpha(x, rho_tilde_now, rho_bar_now):
    dim_x = len(x)
    alpha_tilde_next = np.zeros(shape=(dim_x, N_RESOURCE))
    alpha_bar_next = np.zeros(shape=(dim_x, N_RESOURCE))
    for i in range(dim_x):
        i_neighbors = get_neighbor_indices(x, i)
        i_and_i_neighbors = np.array([i] + i_neighbors)
        # print(f"\nx[i] = {x[i]}")
        # print(f"neighbors:")
        # for n in i_neighbors: 
        #     print(f"{x[n]}")
        for r in range(N_RESOURCE):
            # print(f"r={r}")
            # alpha_tilde
            comparison_list = [] # for second min operator w.r.t j0
            for j0 in range(dim_x):
                if j0 not in i_and_i_neighbors:
                    # print(f"j0={j0}, x[j0] = {x[j0]}")
                    sum_term = 0 # for sum w.r.t j0_prime
                    j0_neighbors_except_i_neighbors = list(
                        set(get_neighbor_indices(x, j0)) - set(i_neighbors))
                    j0_neighbors_except_i_neighbors.sort()
                    for j0_prime in j0_neighbors_except_i_neighbors:
                        # print(f"j0'={j0_prime}, x[j0']={x[j0_prime]}")
                        sum_term += min(0, rho_bar_now[j0_prime, r])
                        # print(f"added min(0, {rho_bar_now[j0_prime, r]}) to sum term")
                    comparison_list.append(
                        -rho_tilde_now[j0, r] + max(0, rho_bar_now[j0, r]) - sum_term)
                    # print(f"term1: -rho_tilde[{j0}, {r}]={-rho_tilde_now[j0, r]}")
                    # print(f"term2: max(0, rho_bar[{j0}, {r}]={rho_bar_now[j0, r]})={max(0, rho_bar_now[j0, r])}")
                    # print(f"term3: {-sum_term}")
                    # print(f"comparison list append {-rho_tilde_now[j0, r] + max(0, rho_bar_now[j0, r]) - sum_term}")
            if len(comparison_list) != 0:
                # alpha_tilde_next[i, r] = min(0, min(comparison_list))
                alpha_tilde_next[i, r] = min(comparison_list)
            else:
                alpha_tilde_next[i, r] = 0
            # print(f"min(0, min({comparison_list}))={alpha_tilde_next[i, r]}")

            # alpha_bar
            comparison_list_1 = [] # for A_ir(1)
            for jn in range(dim_x):
                sum_term_11 = 0 # for A_ir(1), first summation
                sum_term_12 = 0 # for A_ir(1), second summation
                if jn in i_neighbors:
                    jn_neighbors_except_i_and_i_neighbors = list(
                        set(get_neighbor_indices(x, jn)) - set(i_and_i_neighbors))
                    jn_neighbors_except_i_and_i_neighbors.sort()
                    for jn_prime in jn_neighbors_except_i_and_i_neighbors:
                        sum_term_11 += min(0, rho_bar_now[jn_prime, r])

                    jn_and_jn_neighbors = np.array([jn] + get_neighbor_indices(x, jn))
                    i_neighbors_except_jn_and_jn_neighbors = list(
                        set(i_neighbors) - set(jn_and_jn_neighbors))
                    i_neighbors_except_jn_and_jn_neighbors.sort()
                    for jn_prime_prime in i_neighbors_except_jn_and_jn_neighbors:
                        sum_term_12 += min(0, rho_bar_now[jn_prime_prime, r])
                    comparison_list_1.append(
                        rho_tilde_now[jn, r] - rho_bar_now[jn, r] + sum_term_11 - sum_term_12)
            
            comparison_list_2 = [] # for A_ir(2)
            for j0 in range(dim_x):
                sum_term_21 = 0 # for A_ir(2), first summation
                sum_term_22 = 0 # for A_ir(2), second summation
                if j0 not in i_and_i_neighbors:
                    j0_neighbors_except_i_neighbors = list(
                        set(get_neighbor_indices(x, j0)) - set(i_neighbors))
                    j0_neighbors_except_i_neighbors.sort()
                    for j0_prime in j0_neighbors_except_i_neighbors:
                        sum_term_21 += min(0, rho_bar_now[j0_prime, r])
                    j0_and_j0_neighbors = np.array([j0] + get_neighbor_indices(x, j0))
                    i_neighbors_except_j0_and_j0_neighbors = list(
                        set(i_neighbors) - set(j0_and_j0_neighbors))
                    for j0_prime_prime in i_neighbors_except_j0_and_j0_neighbors:
                        sum_term_22 += min(0, rho_bar_now[j0_prime_prime, r])
                    comparison_list_2.append(
                        rho_tilde_now[j0, r] - max(0, rho_bar_now[j0, r]) + sum_term_21 - sum_term_22)
            
            if len(comparison_list_1) != 0:
              A_ir_1 = max(comparison_list_1)
            else:
                A_ir_1 = 0

            if len(comparison_list_2) != 0:
                A_ir_2 = max(comparison_list_2)
            else:
                A_ir_2 = 0

            sum_list_3 = 0
            for i_prime in i_neighbors:
                sum_list_3 += min(0, rho_bar_now[i_prime, r])
            # alpha_bar_next[i, r] = max(A_ir_1, A_ir_2, -sum_list_3) + alpha_tilde_next[i, r]
            alpha_bar_next[i, r] = max(A_ir_1, A_ir_2) + alpha_tilde_next[i, r]

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
        # print(i, x[i])
        # print(rho_tilde_now[i] + alpha_tilde_now[i], " -> ", b_tilde[i])
        # print(rho_bar_now[i] + alpha_bar_now[i], " -> ", b_bar[i])
        if b_tilde[i] > b_bar[i]:
            # print("b_tilde>b_bar")
            # print(f"rho_tilde+alpha_tilde={rho_tilde_now[i] + alpha_tilde_now[i]}")
            allocation[i] = np.argmax(rho_tilde_now[i] + alpha_tilde_now[i])
            # print(f"allocation: {allocation[i]}")
        else:
            allocation[i] = None
    return allocation


def print_allocation(x, t, current_allocation):
    print("."*10 + f"t={t}" + "."*10)
    for i in range(len(x)):
        if not (np.isnan(current_allocation[i])):
            print(f"user(s) {x[i]}: resource {current_allocation[i]}")


def check_convergence():
    pass


def show_mp_traj(x, alpha_tilde, alpha_bar, rho_tilde, rho_bar):
    dim_x = len(x)
    _, axes = plt.subplots(nrows=dim_x, ncols=4,
                           tight_layout=True)
    axes[0, 0].set_title(r"$\tilde{\alpha}$")
    axes[0, 1].set_title(r"$\bar{\alpha}$")
    axes[0, 2].set_title(r"$\tilde{\rho}$")
    axes[0, 3].set_title(r"$\bar{\rho}$")
    t = np.linspace(0, N_ITER-1, N_ITER)
    for i in range(dim_x):
        for j in range (N_RESOURCE):
            axes[i, 0].plot(t, alpha_tilde[:, i, j], label=f"u{x[i]}--r{j}")
            axes[i, 1].plot(t, alpha_bar[:, i, j], label=f"u{x[i]}--r{j}")
            axes[i, 2].plot(t, rho_tilde[:, i, j], label=f"u{x[i]}--r{j}")
            axes[i, 3].plot(t, rho_bar[:, i, j], label=f"u{x[i]}--r{j}")
        axes[i, 0].set_xlim(xmin=0, xmax=N_ITER-1)
        axes[i, 1].set_xlim(xmin=0, xmax=N_ITER-1)
        axes[i, 2].set_xlim(xmin=0, xmax=N_ITER-1)
        axes[i, 3].set_xlim(xmin=0, xmax=N_ITER-1)
        axes[i, 0].legend()
        axes[i, 1].legend()
        axes[i, 2].legend()
        axes[i, 3].legend()
    plt.show()


def show_mp_traj_one(x_number, resource_number, alpha_tilde, alpha_bar, rho_tilde, rho_bar):
    _, axes = plt.subplots(nrows=1, ncols=2, tight_layout=True)
    axes[0].set_title(r"$\alpha$")
    axes[1].set_title(r"$\rho$")
    t = np.linspace(0, N_ITER-1, N_ITER)
    axes[0].plot(t, alpha_tilde[:, x_number, resource_number], label=r'$\tilde{\alpha}$')
    axes[0].plot(t, alpha_bar[:, x_number, resource_number], label=r'$\bar{\alpha}$')
    axes[1].plot(t, rho_tilde[:, x_number, resource_number], label=r'$\tilde{\rho}$')
    axes[1].plot(t, rho_bar[:, x_number, resource_number], label=r'$\bar{\rho}$')
    axes[0].set_xlim(xmin=0, xmax=N_ITER-1)
    axes[1].set_xlim(xmin=0, xmax=N_ITER-1)
    axes[0].legend()
    axes[1].legend()
    plt.show()


if __name__=="__main__":
    main()
