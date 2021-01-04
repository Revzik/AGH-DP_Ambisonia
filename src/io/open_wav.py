import scipy.io.wavfile as wav
import scipy.signal as sig
import numpy as np


def load_wav(path):
    fs, data = wav.read(path)
    channels = 1
    if len(data.shape) == 2:
        channels = data.shape[1]

    if data.dtype == np.int32:
        data = np.array(data / 32768, dtype=np.int16)
    elif data.dtype == np.uint8:
        data = np.array((data - 128) * 256, dtype=np.int16)
    elif data.dtype == np.float32:
        data = np.array(data * 32768, dtype=np.int16)

    return data, channels, fs


def load(path):
    data, channels, fs = load_wav(path)

    if channels > 1:
        data = data[:, 0]

    return data, fs
