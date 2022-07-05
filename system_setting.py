import numpy as np
import matplotlib.pyplot as plt
import json
import os
from itertools import permutations

AP_HEIGHT = 5

def main(n_user, n_resource, ap_positions,
         max_distance, std_hat, seed, save_path):
    np.random.seed(seed)
    user_positions = generate_user_positions(
        n_user, ap_positions, max_distance)
    user_coverages = get_coverages(
        user_positions, ap_positions, max_distance)
    ap2user_distances, _ = get_distances(
        user_positions, ap_positions)
    x = get_x(user_coverages)
    x_neighbors, x_j0 = get_subsets(x)
    y = get_y(x, ap2user_distances, n_resource, std_hat)
    if save_path=="debug":
        plot_positions(user_positions, ap_positions,
                    max_distance, save_path, seed)
    with open(os.path.join(save_path, f"x_{seed}.json"), 'w') as f:
        json.dump(x, f, indent=2) 
    with open(os.path.join(save_path, f"x_neighbors_{seed}.json"), 'w') as f:
        json.dump(x_neighbors, f, indent=2)
    with open(os.path.join(save_path, f"x_j0_{seed}.json"), 'w') as f:
        json.dump(x_j0, f, indent=2)
    np.save(os.path.join(save_path, f"user_positions_{seed}.npy"), user_positions)
    np.save(os.path.join(save_path, f"ap2user_distances_{seed}.npy"), ap2user_distances)
    np.save(os.path.join(save_path, f"y_{seed}.npy"), y)
    np.savetxt(os.path.join(save_path, f"y_{seed}.csv"), y, delimiter=',')


def get_map_boundaries(ap_positions, max_distance):
    x_min = np.min(ap_positions[:, 0]) - max_distance
    x_max = np.max(ap_positions[:, 0]) + max_distance
    y_min = np.min(ap_positions[:, 1]) - max_distance
    y_max = np.max(ap_positions[:, 1]) + max_distance
    return x_min, x_max, y_min, y_max


def is_in_range(user, ap, max_distance):
    distance = np.linalg.norm(user - ap, 2)
    return distance <= max_distance


def generate_user_positions(n_user, ap_positions, max_distance):
    n_ap = np.size(ap_positions, axis=0)
    x_min, x_max, y_min, y_max = get_map_boundaries(
        ap_positions, max_distance)
    user_positions = np.zeros(shape=(n_user, 2))

    n_sample = 0
    n_sample_left = 0
    n_sample_right = 0
    n_sample_both = 0
    while n_sample != n_user:
        pos_x = np.random.uniform(x_min, x_max)
        pos_y = np.random.uniform(y_min, y_max)
        sample = np.array([pos_x, pos_y])

        left = is_in_range(sample, ap_positions[0], max_distance) and not is_in_range(sample, ap_positions[1], max_distance)
        right = is_in_range(sample, ap_positions[1], max_distance) and not is_in_range(sample, ap_positions[0], max_distance)
        both = is_in_range(sample, ap_positions[0], max_distance) and is_in_range(sample, ap_positions[1], max_distance)

        if left:
            if n_sample_left < int(n_user/3):
                user_positions[n_sample] = sample
                n_sample_left += 1
        elif right:
            if n_sample_right < int(n_user/3):
                user_positions[n_sample] = sample
                n_sample_right += 1
        elif both:
            if n_sample_both < n_user - int(n_user/3)*2:
                user_positions[n_sample] = sample
                n_sample_both += 1
        n_sample = n_sample_left + n_sample_right + n_sample_both
        
        # is_covered = False
        # for ap in range(n_ap):
        #     is_covered = is_covered or is_in_range(
        #         sample, ap_positions[ap], max_distance)
        # if is_covered:
        #     user_positions[n_sample] = sample
        #     n_sample += 1

    return user_positions


def get_coverages(user_positions, ap_positions, max_distance):
    n_ap = np.size(ap_positions, axis=0)
    n_user = np.size(user_positions, axis=0)
    user_coverages = np.zeros(shape=(n_user, n_ap), dtype=bool)
    for i, user in enumerate(user_positions):
        for a, ap in enumerate(ap_positions):
            user_coverages[i, a] = is_in_range(user, ap, max_distance)
    return user_coverages


def get_neighbor_indices(x, idx):
    # Neighbors of a single user node
    if type(x[idx]) == int:
        neighbor_idx = []
        for i in range(len(x)):
            if type(x[i]) == list and x[idx] in x[i]:
                neighbor_idx.append(i)
        return neighbor_idx

    # Neighbors of user pair node
    else:
        user1 = x[idx][0]
        user2 = x[idx][1]
        neighbor_idx_user1 = []
        neighbor_idx_user2 = []
        for i in range(len(x)):
            if type(x[i]) == list and user1 in x[i]:
                neighbor_idx_user1.append(i)
            if type(x[i]) == list and user2 in x[i]:
                neighbor_idx_user2.append(i)
        if idx in neighbor_idx_user1:
            neighbor_idx_user1.remove(idx)
        if idx in neighbor_idx_user2:
            neighbor_idx_user2.remove(idx)

        neighbor_idx_both = neighbor_idx_user1 + neighbor_idx_user2
        neighbor_idx_both.sort()
        return neighbor_idx_both


def get_distances(user_positions, ap_positions):
    n_ap = np.size(ap_positions, axis=0)
    n_user = np.size(user_positions, axis=0)
    xy_dist = np.zeros(shape=(n_ap, n_user, 2))
    distances = np.zeros(shape=(n_ap, n_user))
    angles = np.zeros(shape=(n_ap, n_user))

    for ap_idx, ap_position in enumerate(ap_positions):
        xy_dist[ap_idx, :, :] = user_positions - ap_position
        distances[ap_idx, :] = np.linalg.norm(
            xy_dist[ap_idx, :, :], 2, axis=1)
        angles[ap_idx, :] = np.arctan2(
            xy_dist[ap_idx, :, 1], xy_dist[ap_idx, :, 0])
    distances[:, :] = np.sqrt(
        distances[:, :]**2 + AP_HEIGHT**2)
    return distances, angles


def get_x(user_coverages):
    x_both = []
    x_ap0 = []
    x_ap1 = []
    for i, user_is_in in enumerate(user_coverages):
        if np.all(user_is_in):
            x_both.append(i)
        elif user_is_in[0] == True:
            x_ap0.append(i)
        elif user_is_in[1] == True:
            x_ap1.append(i)
    x = x_both
    for i in x_ap0:
        for j in x_ap1:
            x.append([i, j])
    return x


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


def get_G(n_ap, n_user, n_resource):
    G_anr = np.zeros(shape=(n_ap, n_user, n_resource))
    h_real = np.random.normal(
        loc=0, scale=np.sqrt(2)/2, size=(n_ap, n_user, n_resource))
    h_imaginary = np.random.normal(
        loc=0, scale=np.sqrt(2)/2, size=(n_ap, n_user, n_resource))
    for r in range(n_resource):
        G_anr[:, :, r] = h_real[:, :, r]**2 + h_imaginary[:, :, r]**2
    return G_anr


def get_y(x, ap2user_distances, n_resource, std_hat):
    n_ap, n_user = np.shape(ap2user_distances)
    G_anr = get_G(n_ap, n_user, n_resource)
    ap_list = np.linspace(0, n_ap-1, n_ap, dtype=int)
    ap_pair_list = np.array(list(permutations(ap_list, r=2)))
    y = np.zeros(shape=(len(x), n_resource))

    for i in range(len(x)):
        if i < n_user:
            user = i
            for r in range(n_resource):
                sum_term = 0
                for ap in range(n_ap):
                    d_cube = ap2user_distances[ap, user]**3
                    sum_term += G_anr[ap, user, r] / d_cube
                y[i, r] = np.log2(1 + sum_term / (std_hat**2))
        else:
            user1, user2 = x[i]
            for r in range(n_resource):
                comparison_list = [] # for max {a,b} term
                for ap_pair in ap_pair_list:
                    ap1, ap2 = ap_pair
                    snir1 = np.log2(
                        1 + (G_anr[ap1, user1, r]/ap2user_distances[ap1, user1]**3)
                            / (G_anr[ap2, user1, r]/ap2user_distances[ap2, user1]**3 + (std_hat**2)))
                    snir2 = np.log2(
                        1 + (G_anr[ap2, user2, r]/ap2user_distances[ap2, user2]**3)
                            / (G_anr[ap1, user2, r]/ap2user_distances[ap1, user2]**3 + (std_hat**2)))
                    comparison_list.append(snir1 + snir2)
                y[i, r] = np.max(comparison_list)
    return y


def plot_positions(user_positions, ap_positions,
                   max_distance, save_path, seed):
    fig, ax = plt.subplots()
    bs_colors = ['red', 'green', 'blue', 'brown']
    x_min, x_max, y_min, y_max = get_map_boundaries(
        ap_positions, max_distance)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    for i, ap_pos in enumerate(ap_positions):
        ax.plot(ap_pos[0], ap_pos[1], marker="D",
                markersize=8, color=bs_colors[i],
                label=f"$BS_{i}$")
        circle = plt.Circle((ap_pos[0], ap_pos[1]),
                            max_distance,
                            color=bs_colors[i],
                            fill=False)
        ax.add_patch(circle)
    for i, user_pos in enumerate(user_positions):
        ax.plot(user_pos[0], user_pos[1],
                marker=f"${i}$", markersize=8,
                color='black')
    ax.grid()
    plt.gca().set_aspect('equal')
    plt.tight_layout()
    plt.savefig(os.path.join(save_path, f"pos_{seed}.png"))
    plt.show()


if __name__=="__main__":
    main(n_user=30, n_resource=20,
         ap_positions=np.array([[0, 0], [10, 0]]),
         max_distance=10, std_hat=3, seed=0,
         save_path="debug")
