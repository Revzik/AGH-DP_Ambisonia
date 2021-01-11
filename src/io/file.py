import scipy.io.wavfile as wav
import scipy.signal as sps
import numpy as np


def load_wav(path, target_fs=None):
    fs, data = wav.read(path)
    channels = 1
    length = data.size
    if len(data.shape) == 2 and data.shape[1] == 2:
        channels = 2
        length = data.shape[0]

    if data.dtype == np.int16:
        data = np.array(data / 2 ** 16, dtype=np.float32)
    elif data.dtype == np.int32:
        data = np.array(data / 2 ** 32, dtype=np.float32)
    elif data.dtype == np.uint8:
        data = np.array((data - 128) / 256, dtype=np.float32)

    if target_fs is None or fs == target_fs:
        return data, channels, fs

    number_of_samples = round(length * float(target_fs) / fs)
    new_data = sps.resample(data, number_of_samples, axis=0)

    return new_data, channels, fs


def save_wav(path, data, fs):
    wav.write(path, fs, data.T)
