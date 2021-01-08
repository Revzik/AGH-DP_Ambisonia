import numpy as np


def b_format(mono_data, phi, theta):
    W = mono_data
    X = mono_data * np.cos(phi) * np.cos(theta)
    Y = mono_data * np.sin(theta) * np.cos(phi)
    Z = mono_data * np.sin(theta)
    return W, X, Y, Z
