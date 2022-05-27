import enum
import numpy as np
N_ITER = 10
a = np.linspace(0, 9, 10)
for t in range(1, N_ITER):
    print(np.delete(a, t))