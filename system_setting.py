import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations, combinations


np.random.seed(0)
N_USER = 3
AP_POSITIONS = np.array([[0, 0], [10, 0]])
N_AP = np.size(AP_POSITIONS, axis=0)
N_RESOURCE = 2
MAX_DISTANCE = 10
ETA = 3
TX_POWER = -15 # dBm
NOISE_POWER = -80 # dBm
STD_HAT = 3


def main():
    user_positions = generate_user_positions()
    ap2user_distances, _ = get_distances(user_positions)
    x = get_x()
    y = get_y(x, ap2user_distances)
    for i in range(len(x)):
        print(f"user(s) {x[i]}: y_avg:{np.mean(y, axis=1)[i]}")
    np.save("user_positions.npy", user_positions)
    np.save("ap2user_distances.npy", ap2user_distances)
    np.save("y.npy", y)
    plot_positions(user_positions)


def get_map_boundaries():
    x_min = np.min(AP_POSITIONS[:, 0]) - MAX_DISTANCE
    x_max = np.max(AP_POSITIONS[:, 0]) + MAX_DISTANCE
    y_min = np.min(AP_POSITIONS[:, 1]) - MAX_DISTANCE
    y_max = np.max(AP_POSITIONS[:, 1]) + MAX_DISTANCE
    return x_min, x_max, y_min, y_max


def generate_user_positions():
    x_min, x_max, y_min, y_max = get_map_boundaries()
    pos_x = np.random.uniform(x_min, x_max, N_USER)
    pos_y = np.random.uniform(y_min, y_max, N_USER)
    user_positions = np.column_stack((pos_x, pos_y))

    return user_positions


def get_distances(user_positions):
    xy_dist = np.zeros(shape=(N_AP, N_USER, 2))
    distances = np.zeros(shape=(N_AP, N_USER))
    angles = np.zeros(shape=(N_AP, N_USER))

    for ap_idx, ap_position in enumerate(AP_POSITIONS):
        xy_dist[ap_idx, :, :] = user_positions - ap_position
        distances[ap_idx, :] = np.linalg.norm(
            xy_dist[ap_idx, :, :], 2, axis=1)
        angles[ap_idx, :] = np.arctan2(
            xy_dist[ap_idx, :, 1], xy_dist[ap_idx, :, 0])
    return distances, angles


def get_x():
    x = []
    user_list = np.linspace(0, N_USER-1, N_USER, dtype=int)
    user_pair_list = np.array(list(combinations(user_list, r=2)))
    for user in user_list:
        x.append(user.tolist())
    for user_pair in user_pair_list:
        x.append(user_pair.tolist())
    return x


def get_G():
    G_anr = np.zeros(shape=(N_AP, N_USER, N_RESOURCE))
    h_real = np.random.normal(
        loc=0, scale=np.sqrt(2)/2, size=(N_AP, N_USER, N_RESOURCE))
    h_imaginary = np.random.normal(
        loc=0, scale=np.sqrt(2)/2, size=(N_AP, N_USER, N_RESOURCE))
    for r in range(N_RESOURCE):
        G_anr[:, :, r] = h_real[:, :, r]**2 + h_imaginary[:, :, r]**2
    return G_anr


def get_y(x, ap2user_distances):
    G_anr = get_G()
    ap_list = np.linspace(0, N_AP-1, N_AP, dtype=int)
    ap_pair_list = np.array(list(permutations(ap_list, r=2)))
    y = np.zeros(shape=(len(x), N_RESOURCE))

    for i in range(len(x)):
        if i < N_USER:
            user = i
            for r in range(N_RESOURCE):
                sum_term = 0
                for ap in range(N_AP):
                    d_cube = ap2user_distances[ap, user]**3
                    sum_term += G_anr[ap, user, r] / d_cube
                y[i, r] = np.log2(1 + sum_term / (STD_HAT**2))
        else:
            user1, user2 = x[i]
            for r in range(N_RESOURCE):
                comparison_list = [] # for max {a,b} term
                for ap_pair in ap_pair_list:
                    ap1, ap2 = ap_pair
                    snir1 = np.log2(
                        1 + (G_anr[ap1, user1, r]/ap2user_distances[ap1, user1]**3)
                            / (G_anr[ap2, user1, r]/ap2user_distances[ap2, user1]**3 + 1))
                    snir2 = np.log2(
                        1 + (G_anr[ap2, user2, r]/ap2user_distances[ap2, user2]**3)
                            / (G_anr[ap1, user2, r]/ap2user_distances[ap1, user2]**3 + 1))
                    comparison_list.append(snir1 + snir2)
                y[i, r] = np.max(comparison_list)
    return y


# def db2pow(power_dBm):
#     return 10**(power_dBm/10) * 0.001


# def get_snr(user2ap_distances):
#     user2ap_distances *= 1000
#     Rayleigh_coeff = user2ap_distances**(-ETA)
#     tx_power_linear = db2pow(TX_POWER)
#     noise_power_linear = db2pow(NOISE_POWER)
#     snr = Rayleigh_coeff * (tx_power_linear/noise_power_linear)
#     return snr


def plot_positions(user_positions):
    fig, ax = plt.subplots()
    bs_colors = ['red', 'green', 'blue', 'brown']
    x_min, x_max, y_min, y_max = get_map_boundaries()
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    for i, ap_pos in enumerate(AP_POSITIONS):
        ax.plot(ap_pos[0], ap_pos[1], marker="D",
                markersize=8, color=bs_colors[i],
                label=f"$BS_{i}$")
        circle = plt.Circle((ap_pos[0], ap_pos[1]),
                            MAX_DISTANCE,
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
    plt.savefig("APs_and_users.png")
    plt.show()


if __name__=="__main__":
    main()
