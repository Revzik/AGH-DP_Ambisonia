import numpy as np


def to_stereo(W, X, Y, Z):
    phi_l = -30
    phi_r = 30

    left = W * np.cos(phi_l) + Y * np.sin(phi_l)
    right = W * np.cos(phi_r) + Y * np.sin(phi_r)

    return np.vstack((left, right))
