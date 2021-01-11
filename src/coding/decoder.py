import numpy as np
import scipy.signal as sig


NFFT = 1024
NOVERLAP = 512
WINDOW = 'hann'


def to_simple_stereo(W, X, Y, Z, angle):
    angle = angle * np.pi / 180

    left = W + 0.7071 * (X * np.cos(angle) + Y * np.sin(angle))
    right = W + 0.7071 * (X * np.cos(-angle) + Y * np.sin(-angle))

    return np.vstack((left, right))


def to_uhj_stereo(W, X, Y, Z):
    W_ft = stft(W)
    X_ft = stft(X)
    Y_ft = stft(Y)

    S = 0.9396926 * W_ft + 0.1855740 * X_ft
    D = 1j * (-0.3420201 * W_ft + 0.5098604 * X_ft) + 0.6554516 * Y_ft
    left_ft = (S + D) / 2.0
    right_ft = (S - D) / 2.0

    left = np.real(istft(left_ft))
    right = np.real(istft(right_ft))

    return np.vstack((left, right))


def to_binaural(W, X, Y, Z):
    phi_l = -np.pi / 2
    phi_r = np.pi / 2

    left = X * np.cos(phi_l) + Y * np.sin(phi_l)
    right = X * np.cos(phi_r) + Y * np.sin(phi_r)

    return np.vstack((left, right))


def stft(data):
    _, _, fft = sig.stft(data, nperseg=NFFT, nfft=NFFT, noverlap=NOVERLAP, window=WINDOW)
    return fft


def istft(data):
    _, x = sig.istft(data, nperseg=NFFT, nfft=NFFT, noverlap=NOVERLAP, window=WINDOW)
    return x
