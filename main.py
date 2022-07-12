import system_setting as ss
import survey_propagation as sp
import hungarian as hh
import greedy as gd
import numpy as np
import os

N_REPEAT = 50
MAX_DISTANCE = 10
AP_POSITIONS = np.array([[0, 0], [10, 0]])
MAX_ITER = 300

def main():
    n_user_list = [40, 50, 60, 70, 80]
    sum_rates = np.zeros(shape=(len(n_user_list), N_REPEAT))
    sum_rates_hh = np.zeros(shape=(len(n_user_list), N_REPEAT))
    sum_rates_gd = np.zeros(shape=(len(n_user_list), N_REPEAT))
    for i, n_user in enumerate(n_user_list):
        MAX_ITER = n_user * 5
        print("."*20 + f"n_user: {n_user}" + "."*20)
        save_path = make_folder(n_user)
        n_pilot=int(n_user/2)
        for n_repeat in range(N_REPEAT):
            ss.main(n_user=n_user, n_pilot=n_pilot, n_ap=5,
                    seed=n_repeat, save_path=save_path)
            (convergence_time, n_iter,
             sum_rates[i, n_repeat]) = sp.main(
                n_user=n_user, n_pilot=n_pilot,
                max_iter=MAX_ITER, damping=0.3,
                converge_thresh=10**-2, seed=n_repeat,
                save_path=save_path)
            sum_rates_hh[i, n_repeat] = hh.main(
                n_user=n_user, n_pilot=n_pilot,
                seed=n_repeat, save_path=save_path)
            sum_rates_gd[i, n_repeat] = gd.main(
                n_user=n_user, n_pilot=n_pilot,
                seed=n_repeat, save_path=save_path)
            print(f"Simul#{n_repeat}({convergence_time: .2f}s/{n_iter}itr) - SP: {sum_rates[i, n_repeat]:.4f}, HH:{sum_rates_hh[i, n_repeat]:.4f}, GD:{sum_rates_gd[i, n_repeat]:.4f}")
    
        np.save(f"sumrates_SP_{n_user}users.npy", sum_rates[i, :])
        np.save(f"sumrates_HH_{n_user}users.npy", sum_rates_hh[i, :])
        np.save(f"sumrates_GD_{n_user}users.npy", sum_rates_gd[i, :])


def make_folder(n_user):
    name = f"results_{n_user}users"
    if not os.path.exists(name):
        os.makedirs(name)
    return name


if __name__=="__main__":
    main()
