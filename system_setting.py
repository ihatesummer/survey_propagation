import numpy as np
import matplotlib.pyplot as plt
import json
import os
from itertools import combinations

np.set_printoptions(precision=2)

AREA_SIZE = (200, 200)  # meter
AP_HEIGHT = 10  # meter
USER_HEIGHT = 1.5  # meter
STD_SH = 4  # dB
CARRIER_FREQ = 2*(10**3) # MHz
#   L = 46.3 + 33.9*np.log10(CARRIER_FREQ) \
#           - 13.82*np.log10(AP_HEIGHT) \
#           - (1.1*np.log10(CARRIER_FREQ) - 0.7)*USER_HEIGHT \
#           + 1.56*np.log10(CARRIER_FREQ) - 0.8
#   D0, D1 = 10, 50  # m
OMEGA = 100/10**(-9.2) # 0.1/(6.3624*10**(-13)) # 0.1 / (7.2*10**-13)
BW = 20*10**6


def main(nUser: int, nPilot: int, nAP: int, seed: int, save_path: str):
    np.random.seed(seed)

    user_positions = generate_positions(nUser)
    ap_positions = generate_positions(nAP)
    user2ap_distances = get_distances(
        user_positions, ap_positions, is_wrapped=True)
    path_loss = get_path_loss(user2ap_distances)
    beta = get_largeScale_coeff(path_loss)
    random_n_users = get_random_users(nUser, nPilot)
    # worst_users = get_worst_users(beta, n_pilot)
    occupancy = preallocate(random_n_users, nPilot)
    x = get_x(nUser, random_n_users)
    x_neighbors, x_j0 = get_subsets(x)
    y = get_y(x, occupancy, nPilot, beta)

    if save_path == "debug":
        plot_positions(user_positions, ap_positions, occupancy, save_path, seed)

    with open(os.path.join(save_path, f"seed{seed}-x_neighbors.json"), 'w') as f:
        json.dump(x_neighbors, f, indent=2)
    with open(os.path.join(save_path, f"seed{seed}-x_j0.json"), 'w') as f:
        json.dump(x_j0, f, indent=2)

    # For fast read/write
    np.save(os.path.join(save_path, f"seed{seed}-user_pos.npy"), user_positions)
    np.save(os.path.join(save_path, f"seed{seed}-ap_pos.npy"), ap_positions)
    np.save(os.path.join(save_path, f"seed{seed}-occupancy.npy"), occupancy)
    np.save(os.path.join(save_path, f"seed{seed}-beta.npy"), beta)
    np.save(os.path.join(save_path, f"seed{seed}-x.npy"), x)
    np.save(os.path.join(save_path, f"seed{seed}-y.npy"), y)

    # For accessibility
    np.savetxt(os.path.join(save_path, f"seed{seed}-user_pos.csv"), user_positions, '%.4f', delimiter=',')
    np.savetxt(os.path.join(save_path, f"seed{seed}-ap_pos.csv"), ap_positions, '%.4f', delimiter=',')
    np.savetxt(os.path.join(save_path, f"seed{seed}-occupancy.csv"), occupancy, '%d', delimiter=',')
    np.savetxt(os.path.join(save_path, f"seed{seed}-beta.csv"), beta, '%.4f', delimiter=',')
    np.savetxt(os.path.join(save_path, f"seed{seed}-x.csv"), x, '%d', delimiter=',')
    np.savetxt(os.path.join(save_path, f"seed{seed}-y.csv"), y, '%.4f', delimiter=',')


def generate_positions(n_user):
    x_min, y_min = (0, 0)
    x_max, y_max = AREA_SIZE
    pos_x = np.random.uniform(x_min, x_max, size=n_user)
    pos_y = np.random.uniform(y_min, y_max, size=n_user)
    if np.var(pos_x)<100 or np.var(pos_y)<100:
        generate_positions(n_user)
    return np.column_stack((pos_x, pos_y))


def get_distances(user_positions, ap_positions, is_wrapped):
    n_user = np.size(user_positions, axis=0)
    n_ap = np.size(ap_positions, axis=0)
    user_pos_3d = np.column_stack(
        (user_positions, np.ones(n_user)*USER_HEIGHT))
    ap_pos_3d = np.column_stack(
        (ap_positions, np.ones(n_ap)*AP_HEIGHT))
    distances = np.zeros(shape=(n_user, n_ap))
    for i in range(n_user):
        for j in range(n_ap):
            if is_wrapped:
                dx = abs(user_pos_3d[i, 0] - ap_pos_3d[j, 0])
                dx = min(dx, AREA_SIZE[0]-dx)
                dy = abs(user_pos_3d[i, 1] - ap_pos_3d[j, 1])
                dy = min(dy, AREA_SIZE[1]-dy)
                dz = user_pos_3d[i, 2] - ap_pos_3d[j, 2]
                xyz_offsets = np.array([dx, dy, dz])
            else:
                xyz_offsets = user_pos_3d[i] - ap_pos_3d[j]
            distances[i, j] = np.linalg.norm(xyz_offsets, 2)
    return distances


def get_path_loss(user2ap_distances):
    n_user, n_ap = np.shape(user2ap_distances)
    path_loss = np.zeros(shape=(n_user, n_ap))
    for i in range(n_user):
        for j in range(n_ap):
            dmk = user2ap_distances[i, j]
            #path_loss[i, j] = - L - 15*np.log10(max(D1, dmk)) \
            #   - 20*np.log10(max(D0, dmk))
            path_loss[i, j]=-30.5-36.7*np.log10(dmk)
    return path_loss

def get_largeScale_coeff(path_loss):
    n_user, n_ap = np.shape(path_loss)
    #z = np.random.normal(size=np.shape(path_loss))
    zk = np.random.normal(size=n_user)
    zm = np.random.normal(size=n_ap)
        # return path_loss*10**(STD_SH*z/10)
    for i in range(n_user):
        for j in range(n_ap):
            z=(0.5**0.5)*(zk[i]+zm[j])
    return 10**((path_loss+STD_SH*z)/10)


def get_random_users(n_user, n_pilot):
    user_list = np.linspace(0, n_user-1, n_user, dtype=int)
    return np.random.choice(user_list, n_pilot, replace=False)


def get_worst_users(beta, n_pilot):
    potential_rate = np.sum(beta, axis=1)
    return np.argsort(potential_rate)[:n_pilot]


def preallocate(worst_users, n_pilot):
    pilots = np.zeros(n_pilot, dtype=int)
    for i, user in enumerate(worst_users):
        pilots[i] = user
    return pilots


def get_x(n_user, worst_users):
    all_users = np.linspace(0, n_user-1, n_user, dtype=int)
    x = list(set(all_users) - set(worst_users))
    n_pilot = len(worst_users)
    if n_user % n_pilot != 0:
        print("ERROR: invalid (n_user, n_pilot) comination")
    else:
        n_group_member = int(n_user / n_pilot)
        return np.array(list(combinations(x, n_group_member-1)))


def get_throughput(k, roommates, beta, n_pilot):
    return BW * (1-n_pilot/200)*(np.log2(1+get_sinr(k, roommates, beta, n_pilot)))


def get_sinr(user, roommates, beta, n_pilot):
    gamma = get_gamma(user, roommates, beta, n_pilot)
    ds = OMEGA * np.sum(gamma)**2
    bu = OMEGA * np.sum(gamma*np.sum(beta, axis=0))
    ui = 0
    for roommate in roommates:
        ui += OMEGA * np.sum(gamma/beta[user] * beta[roommate]) ** 2
    return ds / (bu + ui + np.sum(gamma))


def get_gamma(user, roommates, beta, n_pilot):
    return n_pilot*OMEGA * beta[user]**2 / (n_pilot*OMEGA*(np.sum(beta[roommates], axis=0)+beta[user])+1)


def get_neighbor_indices(x, idx):
    users = x[idx]
    neighbor_idx = []
    for i in range(len(x)):
        if len(np.intersect1d(users, x[i])):
            neighbor_idx.append(i)
    if idx in neighbor_idx:
        neighbor_idx.remove(idx)
    if idx in neighbor_idx:
        neighbor_idx.remove(idx)

    neighbor_idx.sort()
    return neighbor_idx


def get_subsets(x):
    dim_x = len(x)
    x_neighbors = [None] * dim_x
    for i in range(dim_x):
        x_neighbors[i] = get_neighbor_indices(x, i)

    x_j0 = [None] * dim_x
    for i in range(dim_x):
        i_and_i_neighbors = np.array([i] + x_neighbors[i])
        j0 = []
        for j in range(dim_x):
            if j not in i_and_i_neighbors:
                j0.append(j)
        x_j0[i] = j0

    return x_neighbors, x_j0


def get_y(x, occupancy, n_pilot, beta):
    y = np.zeros(shape=(len(x), n_pilot))
    for i in range(len(x)):
        for r in range(n_pilot):
            roommates = np.concatenate(([occupancy[r]], x[i].reshape(-1)))
            roommate_configs = np.array(list(combinations(roommates, len(roommates)-1)))
            for comb in roommate_configs:
                room_head = list(set(roommates)-set(comb))[0]
                y[i, r] += get_throughput(room_head, comb, beta, n_pilot)
    return y


def plot_positions(user_positions, ap_positions, occupancy,
                   save_path, seed):
    _, ax = plt.subplots()
    x_min, y_min = 0, 0
    x_max, y_max = AREA_SIZE
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    
    ax.scatter(ap_positions[:, 0], ap_positions[:, 1], 10, 'gray', 'x',label='APs')
    ax.scatter(user_positions[:, 0], user_positions[:, 1], 40, 'black', 'o',
               alpha=0.7, label='Users')
    for i in range(user_positions.shape[0]):
        ax.text(user_positions[i, 0], user_positions[i, 1], str(i), fontsize=12)
    for i in range(occupancy.shape[0]):
        ax.text(user_positions[occupancy[i], 0]+1, user_positions[occupancy[i], 1]-5,
                'pilot'+str(i), fontsize=12, color='tab:red')

    ax.grid(alpha=0.5)
    ax.legend(loc='upper center', ncol=2, bbox_to_anchor=(0.5, 1.1))
    plt.gca().set_aspect('equal')
    # plt.tight_layout()
    plt.savefig(os.path.join(save_path, f"seed{seed}-pos.png"))
    plt.show()
    plt.close()


if __name__ == "__main__":
    main(nUser=9, nPilot=3, nAP=100, seed=9, save_path="debug")
