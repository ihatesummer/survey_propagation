import system_setting as ss
import survey_propagation as sp
import numpy as np
import os
import matplotlib.pyplot as plt

N_REPEAT = 100

def main():
    n_resource = 50
    n_user_list = [10, 20, 30, 40, 50]
    sum_rates = np.zeros(shape=(len(n_user_list), N_REPEAT))
    for i, n_user in enumerate(n_user_list):
        print("."*20 + f"n_user: {n_user}" + "."*20)
        save_path = make_folder(n_user)
        for n_repeat in range(N_REPEAT):
            ss.main(n_user=n_user,
                    n_resource=n_resource,
                    ap_positions=np.array([[0, 0], [10, 0]]),
                    max_distance=10,
                    std_hat=3,
                    seed=n_repeat,
                    save_path=save_path)
            (convergence_time, n_iter,
             sum_rates[i, n_repeat]) = sp.main(
                n_user=n_user, n_resource=n_resource,
                max_iter=n_user*3, damping=0.3,
                converge_thresh=10**-2, seed=n_repeat,
                save_path=save_path)
            print(f"r{n_repeat} converged in {convergence_time:.2f}s({n_iter}itr), sum rate {sum_rates[i, n_repeat]:.2f}")
    fig, ax = plt.subplots()
    ax.semilogy(n_user_list, np.nanmean(sum_rates, axis=1), "-*")
    ax.set_xlabel("No. users")
    ax.set_ylabel("Sum rate")
    plt.show()
    np.save("sum_rates", sum_rates)


def make_folder(n_user):
    name = f"results_{n_user}users"
    if not os.path.exists(name):
        os.makedirs(name)
    return name


if __name__=="__main__":
    main()
