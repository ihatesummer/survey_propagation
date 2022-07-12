import numpy as np
import os
import json
from system_setting import get_coverages, get_G, STD_HAT
from scipy.optimize import linear_sum_assignment


def main(n_user, n_resource, max_distance, ap_positions, seed, save_path):
    np.random.seed(seed)
    user_positions = np.load(os.path.join(save_path, f"user_positions_{seed}.npy"))
    ap2user_distances = np.load(os.path.join(save_path, f"ap2user_distances_{seed}.npy"))
    with open(os.path.join(save_path, f"x_{seed}.json"), 'r') as f:
        x = json.load(f)
    y = np.load(os.path.join(save_path, f"y_{seed}.npy"))
    user_coverages = get_coverages(user_positions, ap_positions, max_distance)
    idx_center, idx_left, idx_right = get_census(user_coverages)

    n_ap = np.size(ap_positions, axis=0)
    resources = np.linspace(0, n_resource-1, n_resource, dtype=int)
    G_anr = get_G(n_ap, n_user, n_resource)

    sum_rate_1 = 0
    double_alloc_1 = {}
    # left+center
    users_lc = np.sort(np.concatenate((idx_center, idx_left)))
    y_lc = get_y_single(ap2user_distances[0, users_lc], n_resource, G_anr[0, users_lc, :])
    user_idx_lc, resource_idx_lc = linear_sum_assignment(y_lc, maximize=True)
    for usr, res in zip(user_idx_lc, resource_idx_lc):
        if np.all(user_coverages[users_lc[usr]]):
            sum_rate_1 += y[x.index(users_lc[usr]), res]
        else:
            double_alloc_1[res] = users_lc[usr]
    # right
    users_r = np.sort(idx_right)
    res_r = np.array([], dtype=int)
    for i, user in enumerate(users_lc[user_idx_lc]):
        if np.all(user_coverages[user]==[True, False]):
            res_r = np.append(res_r, resource_idx_lc[i])
    y_r = get_y_single(ap2user_distances[1, users_r], n_resource, G_anr[1, users_r, :])
    user_idx_r, resource_idx_r = linear_sum_assignment(y_r[:, res_r], maximize=True)
    for usr, res in zip(user_idx_r, resource_idx_r):
        double_alloc_1[res_r[res]] = [double_alloc_1[res_r[res]], users_r[usr]]
    for res, user_pair in double_alloc_1.items():
        sum_rate_1 += y[x.index(user_pair), res]

    sum_rate_2 = 0
    double_alloc_2 = {}
    # right+center
    users_rc = np.sort(np.concatenate((idx_center, idx_right)))
    y_rc = get_y_single(ap2user_distances[1, users_rc], n_resource, G_anr[1, users_rc, :])
    user_idx_rc, resource_idx_rc = linear_sum_assignment(y_rc, maximize=True)
    for usr, res in zip(user_idx_rc, resource_idx_rc):
        if np.all(user_coverages[users_rc[usr]]):
            sum_rate_2 += y[x.index(users_rc[usr]), res]
        else:
            double_alloc_2[res] = users_rc[usr]
    # left
    users_l = np.sort(idx_left)
    res_l = np.array([], dtype=int)
    for i, user in enumerate(users_rc[user_idx_rc]):
        if np.all(user_coverages[user]==[False, True]):
            res_l = np.append(res_l, resource_idx_rc[i])
    y_l = get_y_single(ap2user_distances[0, users_l], n_resource, G_anr[0, users_l, :])
    user_idx_l, resource_idx_l = linear_sum_assignment(y_l[:, res_l], maximize=True)
    for usr, res in zip(user_idx_l, resource_idx_l):
        double_alloc_2[res_l[res]] = [users_l[usr], double_alloc_2[res_l[res]]]
    for res, user_pair in double_alloc_2.items():
        sum_rate_2 += y[x.index(user_pair), res]

    return max(sum_rate_1, sum_rate_2)


def get_census(user_coverages):
    idx_center, idx_left, idx_right = [], [], []
    for i in range(np.size(user_coverages, axis=0)):
        if np.all(user_coverages[i]):
            idx_center.append(i)
        elif np.all(user_coverages[i] == [True, False]):
            idx_left.append(i)
        elif np.all(user_coverages[i] == [False, True]):
            idx_right.append(i)
    return idx_center, idx_left, idx_right


def get_y_single(ap2user_distances, n_resource, G_anr):
    n_user = np.size(ap2user_distances)
    y = np.zeros(shape=(n_user, n_resource))
    for i in range(n_user):
        for r in range(n_resource):
            d_cube = ap2user_distances[i]**3
            y[i, r] = np.log2(1 + G_anr[i, r] / d_cube / (STD_HAT**2))
    return y


if __name__=="__main__":
    sum_rate = main(
        n_user=8, n_resource=6, max_distance=10,
        ap_positions=np.array([[0, 0], [10, 0]]),
        seed=0, save_path="debug")
    print(f"Heuristic Hungarian sumrate: {sum_rate}s")
