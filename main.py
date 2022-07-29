import system_setting as ss
import survey_propagation as sp
import hungarian as hh
import greedy as gd
import k_means as km
import numpy as np
import os


N_REPEAT = 10
AP_POSITIONS = np.array([[0, 0], [10, 0]])

def main():
    n_user_list = [15, 30, 45, 60, 75, 90]
    sum_rates = np.zeros(shape=(len(n_user_list), N_REPEAT))
    sum_rates_hh = np.zeros(shape=(len(n_user_list), N_REPEAT))
    sum_rates_gd = np.zeros(shape=(len(n_user_list), N_REPEAT))
    sum_rates_km = np.zeros(shape=(len(n_user_list), N_REPEAT))
    for i, n_user in enumerate(n_user_list):
        max_iter = n_user * 5
        print("."*20 + f"n_user: {n_user}" + "."*20)
        save_path = make_folder(n_user)
        n_pilot=int(n_user/3)
        for n_repeat in range(N_REPEAT):
            ss.main(n_user=n_user, n_pilot=n_pilot, n_ap=100,
                    seed=n_repeat, save_path=save_path)
            (convergence_time, n_iter,
             sum_rates[i, n_repeat]) = sp.main(n_user, n_pilot, max_iter,
                                               damping=0.3, converge_thresh=10**-2,
                                               seed=n_repeat, save_path=save_path)
            sum_rates_hh[i, n_repeat] = hh.main(n_user, n_pilot, seed=n_repeat, save_path=save_path)
            sum_rates_gd[i, n_repeat] = gd.main(n_user, n_pilot, seed=n_repeat, save_path=save_path)
            sum_rates_km[i, n_repeat] = km.main(n_user, n_pilot, seed=n_repeat, save_path=save_path)
            print(f"Simul#{n_repeat} - " +
                  f"SP({convergence_time:.2f}s/{n_iter}itr): {sum_rates[i, n_repeat]:.2f}, " + 
                  f"HH:{sum_rates_hh[i, n_repeat]:.2f}, " +
                  f"GD:{sum_rates_gd[i, n_repeat]:.2f}, " +
                  f"KM:{sum_rates_km[i, n_repeat]:.2f}")
    
            np.save(f"sumrates_SP_{n_user}users.npy", sum_rates[i, :n_repeat+1])
            np.save(f"sumrates_HH_{n_user}users.npy", sum_rates_hh[i, :n_repeat+1])
            np.save(f"sumrates_GD_{n_user}users.npy", sum_rates_gd[i, :n_repeat+1])
            np.save(f"sumrates_KM_{n_user}users.npy", sum_rates_km[i, :n_repeat+1])
            np.savetxt(f"sumrates_SP_{n_user}users.csv", sum_rates[i, :n_repeat+1], delimiter=',')
            np.savetxt(f"sumrates_HH_{n_user}users.csv", sum_rates_hh[i, :n_repeat+1], delimiter=',')
            np.savetxt(f"sumrates_GD_{n_user}users.csv", sum_rates_gd[i, :n_repeat+1], delimiter=',')
            np.savetxt(f"sumrates_KM_{n_user}users.csv", sum_rates_km[i, :n_repeat+1], delimiter=',')


def make_folder(n_user):
    pathname = os.path.join("simul_outputs", f"{n_user}users")
    if not os.path.exists(pathname):
        os.makedirs(pathname)
    return pathname


if __name__=="__main__":
    main()
