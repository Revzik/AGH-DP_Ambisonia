import scipy.io.wavfile as wav
import numpy as np


def load_wav(path):
    fs, data = wav.read(path)
    channels = 1
    if len(data.shape) == 2:
        channels = data.shape[1]

    if data.dtype == np.int16:
        data = np.array(data / 2 ** 16, dtype=np.float32)
    if data.dtype == np.int32:
        data = np.array(data / 2 ** 32, dtype=np.float32)
    elif data.dtype == np.uint8:
        data = np.array((data - 128) / 256, dtype=np.float32)

    return data, channels, fs


def save_wav(path, data, fs):
    wav.write(path, fs, data.T)
