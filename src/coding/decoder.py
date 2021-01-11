import numpy as np
import scipy.signal as sig
import scipy.io as spio
import os.path as p

from src.engine import track


NFFT = 1024
NOVERLAP = 512
WINDOW = 'hann'
HRTF = p.join('resources', 'hrtfs', 'hrir_021.mat')
HRTF_FS = 44100


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
    h_length = round(200 * float(track.FS) / HRTF_FS)

    # stft test
    # nfft = h_length
    # noverlap = h_length // 2
    # wave_length = int(np.ceil(W.size / noverlap) * noverlap)

    phis   = np.array([-125, -55,  0, 55, 125, 180,  0,   0], dtype=np.float32) * np.pi / 180
    thetas = np.array([   0,   0,  0,  0,   0,   0, 90, -45], dtype=np.float32) * np.pi / 180
    p_idx  =          [  23,  23, 13,  3,   3,  13, 13,  13]
    t_idx  =          [   9,   9,  9,  9,   9,   9, 25,   0]

    hrtf = spio.loadmat(HRTF)

    left = np.zeros(W.size)
    right = np.zeros(W.size)
    for i in range(phis.size):
        w_ft = W + 0.7071 * (
               X * np.cos(phis[i]) * np.cos(thetas[i]) +
               Y * np.sin(phis[i]) * np.cos(thetas[i]) +
               Z * np.sin(thetas[i]))

        hrtf_l = sig.resample(hrtf['hrir_l'][p_idx[i], t_idx[i], :], h_length)
        hrtf_r = sig.resample(hrtf['hrir_r'][p_idx[i], t_idx[i], :], h_length)

        left += sig.convolve(w_ft, hrtf_l, mode='same')
        right += sig.convolve(w_ft, hrtf_r, mode='same')

        # stft test
        # w_ft = stft(W + 0.7071 * (
        #             X * np.cos(phis[i]) * np.cos(thetas[i]) +
        #             Y * np.sin(phis[i]) * np.cos(thetas[i]) +
        #             Z * np.sin(thetas[i])),
        #             nfft=nfft, noverlap=noverlap)
        #
        # hrtf_l = sig.resample(hrtf['hrir_l'][p_idx[i], t_idx[i], :], h_length)
        # hrtf_r = sig.resample(hrtf['hrir_r'][p_idx[i], t_idx[i], :], h_length)
        #
        # Hrtf_l = np.array(fft(hrtf_l))[:h_length // 2 + 1][np.newaxis].T
        # Hrtf_r = np.array(fft(hrtf_r))[:h_length // 2 + 1][np.newaxis].T
        #
        # left += np.real(istft(Hrtf_l * w_ft, nfft, noverlap))
        # right += np.real(istft(Hrtf_r * w_ft, nfft, noverlap))

    return np.vstack((left, right)) / 4


def fft(data):
    return np.fft.fft(data)


def stft(data, nfft=NFFT, noverlap=NOVERLAP):
    _, _, fft = sig.stft(data, nperseg=nfft, nfft=nfft, noverlap=noverlap, window=WINDOW)
    return fft


def istft(data, nfft=NFFT, noverlap=NOVERLAP):
    _, x = sig.istft(data, nperseg=nfft, nfft=nfft, noverlap=noverlap, window=WINDOW)
    return x
