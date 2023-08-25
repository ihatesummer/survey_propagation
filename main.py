import numpy as np
import os
import system_setting
import survey_propagation as sp
import hungarian as hh
import greedy as gd
import k_means as km

N_EXPERIMENT = 10
EXPERIMENT_NUMBER_OFFSET = 0
N_AP = 100

def main():
    nUsers = [9]

    sumrate_log_sp = np.zeros(shape=(len(nUsers), N_EXPERIMENT)) # survey propagation
    sumrate_log_hh = np.zeros(shape=(len(nUsers), N_EXPERIMENT)) # heuristic implementation of Hungarian
    sumrate_log_gd = np.zeros(shape=(len(nUsers), N_EXPERIMENT)) # greedy
    sumrate_log_km = np.zeros(shape=(len(nUsers), N_EXPERIMENT)) # heuristic implementation of K-means

    for i, nUser in enumerate(nUsers):
        print("."*20 + f"{nUser} users" + "."*20)
        save_path = os.path.join("simul_outputs", "journal",
                                f"{nUser}users,seed{EXPERIMENT_NUMBER_OFFSET}-{N_EXPERIMENT}")
        make_folder(save_path)

        max_iter = nUser * 10
        nPilot = int(nUser/3)
        for n_repeat in range(N_EXPERIMENT):
            seed = n_repeat
            system_setting.main(nUser, nPilot, N_AP, seed, save_path)

            (convergence_time, n_iter,
             sumrate_log_sp[i, n_repeat]) = sp.main(nUser, nPilot, max_iter,
                                               damping=0.5, converge_thresh=10**-2,
                                               seed=seed, save_path=save_path)
            sumrate_log_hh[i, n_repeat] = hh.main(nUser, nPilot, seed, save_path)
            sumrate_log_gd[i, n_repeat] = gd.main(nUser, nPilot, seed, save_path)
            sumrate_log_km[i, n_repeat] = km.main(nUser, nPilot, seed, save_path)

            print(f"Simul#{seed}:" +
                  f"SP({convergence_time:.2f}s/{n_iter}itr): {sumrate_log_sp[i, n_repeat]:.2f}, " + 
                  f"HH:{sumrate_log_hh[i, n_repeat]:.2f}, " +
                  f"GD:{sumrate_log_gd[i, n_repeat]:.2f}, " +
                  f"KM:{sumrate_log_km[i, n_repeat]:.2f}")
    
            np.savetxt(f"sumrates_SP_{nUser}users.csv", sumrate_log_sp[i, :n_repeat+1], delimiter=',')
            np.savetxt(f"sumrates_HH_{nUser}users.csv", sumrate_log_hh[i, :n_repeat+1], delimiter=',')
            np.savetxt(f"sumrates_GD_{nUser}users.csv", sumrate_log_gd[i, :n_repeat+1], delimiter=',')
            np.savetxt(f"sumrates_KM_{nUser}users.csv", sumrate_log_km[i, :n_repeat+1], delimiter=',')


def make_folder(pathname):
    if not os.path.exists(pathname):
        os.makedirs(pathname)


if __name__=="__main__":
    main()
