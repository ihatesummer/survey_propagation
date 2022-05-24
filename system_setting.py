import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)
N_USER = 10
AP_POSITIONS = np.array([[0, 0], [10, 0]])
N_AP = np.size(AP_POSITIONS, axis=0)
MAX_DISTANCE = 10
ETA = 3
TX_POWER = -15 # dBm
NOISE_POWER = -80 # dBm


def main():
    user_positions = generate_user_positions()
    user2ap_distances, _ = get_distances(user_positions)
    snr = get_snr(user2ap_distances*1000)
    np.save("user_positions.npy", user_positions)
    np.save("user2ap_distances.npy", user2ap_distances)
    np.save("snr.npy", snr)
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


def db2pow(power_dBm):
    return 10**(power_dBm/10) * 0.001


def get_snr(user2ap_distances):
    Rayleigh_coeff = user2ap_distances**(-ETA)
    tx_power_linear = db2pow(TX_POWER)
    noise_power_linear = db2pow(NOISE_POWER)
    snr = Rayleigh_coeff * (tx_power_linear/noise_power_linear)
    return snr


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
