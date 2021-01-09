import numpy as np


def to_stereo(W, X, Y, Z):
    phi_l = -30
    phi_r = 30

    left = X * np.cos(phi_l) + Y * np.sin(phi_l)
    right = X * np.cos(phi_r) + Y * np.sin(phi_r)

    return np.vstack((left, right))


def to_headphones(W, X, Y, Z):
    phi_l = -90
    phi_r = 90

    left = X * np.cos(phi_l) + Y * np.sin(phi_l)
    right = X * np.cos(phi_r) + Y * np.sin(phi_r)

    return np.vstack((left, right))
