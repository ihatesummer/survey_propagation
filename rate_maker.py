import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)
N_USER = 100
N_RESOURCE = 10
N_CASE = 100

AP_POSITIONS = np.array([[0, 0], [10, 0], [0, 10], [10, 10]])
N_AP = np.size(AP_POSITIONS, axis=0)
MAX_DISTANCE = 10
ETA = 3
TX_POWER = -15 # dB
NOISE_POWER = -80 # dB
INF = 10**7


def main():
    user_positions = generate_user_pos()
    user2ap_dist_l2, _ = get_distances(user_positions)
    get_snr(user2ap_dist_l2)
    plot_positions(user_positions)


def generate_user_pos():
    x_min, x_max, y_min, y_max = get_map_boundaries()
    usr_pos_x = np.random.uniform(x_min, x_max, N_USER)
    usr_pos_y = np.random.uniform(y_min, y_max, N_USER)
    usr_pos = np.column_stack((usr_pos_x, usr_pos_y))

    return usr_pos


def get_map_boundaries():
    x_min = np.min(AP_POSITIONS[:, 0]) - MAX_DISTANCE
    x_max = np.max(AP_POSITIONS[:, 0]) + MAX_DISTANCE
    y_min = np.min(AP_POSITIONS[:, 1]) - MAX_DISTANCE
    y_max = np.max(AP_POSITIONS[:, 1]) + MAX_DISTANCE
    return x_min, x_max, y_min, y_max


def get_distances(user_positions):
    xy_dist = np.zeros(shape=(N_AP, N_USER, 2))
    dist_l2 = np.zeros(shape=(N_AP, N_USER))
    angle = np.zeros(shape=(N_AP, N_USER))

    for ap_idx, ap_position in enumerate(AP_POSITIONS):
        xy_dist[ap_idx, :, :] = user_positions - ap_position
        dist_l2[ap_idx, :] = np.linalg.norm(xy_dist[ap_idx, :, :], 2, axis=1)
        angle[ap_idx, :] = np.arctan2(xy_dist[ap_idx, :, 1], xy_dist[ap_idx, :, 0])
    return dist_l2, angle


def get_snr(user2ap_dist_l2):
    Rayleigh_coeff_H = np.sqrt(user2ap_dist_l2**(-ETA))
    Rayleigh_coeff_G = (np.abs(Rayleigh_coeff_H))**2
    tx_power_linear = 0.001 * db2pow(TX_POWER)
    noise_power_linear = 0.001 * db2pow(NOISE_POWER)
    snr = Rayleigh_coeff_G * (tx_power_linear/noise_power_linear)
    print(snr)
    snr = snr + (INF-snr)*(snr>INF)


def db2pow(power_db):
    return 10**(power_db/10)


def plot_positions(user_positions):
    fig, ax = plt.subplots()
    bs_colors = ['red', 'green', 'blue', 'brown']
    x_min, x_max, y_min, y_max = get_map_boundaries()
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    for i, ap_pos in enumerate(AP_POSITIONS):
        ax.plot(ap_pos[0], ap_pos[1], "D",
                markersize=8, color=bs_colors[i], label=f"$BS_{i}$")
        points = np.linspace(ap_pos[0]-MAX_DISTANCE,
                             ap_pos[0]+MAX_DISTANCE,
                             100)
        circle = plt.Circle((ap_pos[0], ap_pos[1]), MAX_DISTANCE,
                            color=bs_colors[i], fill=False)
        ax.add_patch(circle)
    for i, user_pos in enumerate(user_positions):
        ax.plot(user_pos[0], user_pos[1],
                marker=f"${i}$", markersize=8, color='black')
    ax.grid()
    # ax.legend()
    plt.gca().set_aspect('equal')
    plt.tight_layout()
    plt.show()


if __name__=="__main__":
    main()
