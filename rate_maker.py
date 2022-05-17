import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)
N_USER = 100
N_RESOURCE = 10
N_CASE = 100
N_BS = 4
MAX_DISTANCE = 10
ETA = 3
TX_POWER = -15 # dB
NOISE_POWER = -80 # dB
INF = 10**7

def main():
    band_widths = 40*np.ones(N_RESOURCE)
    bs_positions = np.array([[0, 0], [10, 0], [0, 10], [10, 10]]) # hard-coded positions
    user_positions = generate_user_pos(bs_positions)
    user2bs_dist_xy, user2bs_dist_polar = get_distances(user_positions, bs_positions)
    get_snr(user2bs_dist_polar)
    plot_positions(user_positions, bs_positions)
    for i in range(N_CASE):
        continue


def generate_user_pos(bs_positions):
    x_min, x_max, y_min, y_max = get_map_boundaries(bs_positions)
    usr_pos_x = np.random.uniform(x_min, x_max, N_USER)
    usr_pos_y = np.random.uniform(y_min, y_max, N_USER)
    usr_pos = np.column_stack((usr_pos_x, usr_pos_y))

    return usr_pos


def get_map_boundaries(bs_positions):
    x_min = np.min(bs_positions[:, 0]) - MAX_DISTANCE
    x_max = np.max(bs_positions[:, 0]) + MAX_DISTANCE
    y_min = np.min(bs_positions[:, 1]) - MAX_DISTANCE
    y_max = np.max(bs_positions[:, 1]) + MAX_DISTANCE
    return x_min, x_max, y_min, y_max


def get_distances(user_positions, bs_positions):
    xy_dist = np.zeros(shape=(N_BS, N_USER, 2))
    polar_dist = np.zeros(shape=(N_BS, N_USER, 2))

    for bs_idx, bs_position in enumerate(bs_positions):
        xy_dist[bs_idx, :, :] = user_positions - bs_position
        polar_dist[bs_idx, :, 0] = np.linalg.norm(xy_dist[bs_idx, :, :], 2, axis=1)
        polar_dist[bs_idx, :, 1] = np.arctan2(xy_dist[bs_idx, :, 1], xy_dist[bs_idx, :, 0])
    return xy_dist, polar_dist


def get_snr(user_bs_dist_polar):
    Rayleigh_coeff_H = np.zeros((N_BS, N_USER))
    user2bs_distances = user_bs_dist_polar[:, :, 0]
    Rayleigh_coeff_H = np.sqrt(user2bs_distances**(-ETA))
    Rayleigh_coeff_G = (np.abs(Rayleigh_coeff_H))**2
    tx_power_linear = 0.001 * db2pow(TX_POWER)
    noise_power_linear = 0.001 * db2pow(NOISE_POWER)
    snr = Rayleigh_coeff_G * (tx_power_linear/noise_power_linear)
    snr = snr + (INF-snr)*(snr>INF)
    print(snr)


def db2pow(power_db):
    return 10**(power_db/10)

def plot_positions(user_positions, bs_positions):
    fig, ax = plt.subplots()
    bs_colors = ['red', 'green', 'blue', 'brown']
    x_min, x_max, y_min, y_max = get_map_boundaries(bs_positions)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    for i, bs_pos in enumerate(bs_positions):
        ax.plot(bs_pos[0], bs_pos[1], "D",
                markersize=8, color=bs_colors[i], label=f"$BS_{i}$")
        points = np.linspace(bs_pos[0]-MAX_DISTANCE,
                             bs_pos[0]+MAX_DISTANCE,
                             100)
        circle = plt.Circle((bs_pos[0], bs_pos[1]), MAX_DISTANCE,
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
