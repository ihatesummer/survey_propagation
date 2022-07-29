import numpy as np
import os
import json
from system_setting import get_throughput, AREA_SIZE
KP = 100

def main(n_user, n_pilot, seed, save_path):
    np.random.seed(seed)
    n_centroids = int(n_user / n_pilot)
    points_x = np.random.uniform(0, AREA_SIZE[0], KP)
    points_y = np.random.uniform(0, AREA_SIZE[1], KP)
    points = np.column_stack((points_x, points_y))
    print(points)
    centroids = np.random.randint(0, KP, n_centroids)
    print(centroids)

if __name__=="__main__":
    sum_throughput = main(
        n_user=9, n_pilot=3,
        seed=0, save_path="debug")
    print(f"K-means sumThroughput: {sum_throughput}s")

