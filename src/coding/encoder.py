import numpy as np


def b_format(mono_data, phi, theta):
    phi = phi * np.pi / 180
    theta = theta * np.pi / 180

    W = mono_data * 0.7071
    X = mono_data * np.cos(phi) * np.cos(theta)
    Y = mono_data * np.sin(phi) * np.cos(theta)
    Z = mono_data * np.sin(theta)

    return W, X, Y, Z
