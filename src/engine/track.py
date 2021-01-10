import numpy as np

from src.io import file
from src.coding import encoder, decoder


MONO = 'mono'
STEREO = 'stereo'
BINAURAL = 'binaural'


class Track:
    def __init__(self):
        self.loaded = False

        self.wave = None
        self.length = 1
        self.channels = 1
        self.gain = 0
        self.fs = 0
        self.type = MONO

        self.W = None
        self.X = None
        self.Y = None
        self.Z = None

        self.phi = 0
        self.theta = 0
        self.stereo_angle = 30

    def reset(self):
        self.wave = None
        self.W = None
        self.X = None
        self.Y = None
        self.Z = None
        self.fs = 44100


class InputTrack(Track):
    def __init__(self):
        super().__init__()

    def load(self, path):
        try:
            self.wave, self.channels, self.fs = file.load_wav(path)
            self.length = self.wave.size
            self.loaded = True
            if self.channels == 1:
                self.type = MONO
            else:
                self.type = STEREO

            print('Loaded track from {}, track type: {}, track sample rate: {}'.
                  format(path, self.type, self.fs))
        except Exception as e:
            self.loaded = False
            raise e

    def encode(self):
        if self.type == MONO:
            self.W, self.X, self.Y, self.Z = encoder.b_format(self.wave, self.phi, self.theta)
        else:
            W_l, X_l, Y_l, Z_l = encoder.b_format(self.wave[:, 0], self.phi - self.stereo_angle, self.theta)
            W_r, X_r, Y_r, Z_r = encoder.b_format(self.wave[:, 0], self.phi + self.stereo_angle, self.theta)
            self.W = W_l + W_r
            self.X = X_l + X_r
            self.Y = Y_l + Y_r
            self.Z = Z_l + Z_r

    def send(self):
        return self.W * dB(self.gain), self.X * dB(self.gain), self.Y * dB(self.gain), self.Z * dB(self.gain)


class MasterTrack(Track):
    def __init__(self):
        super().__init__()

        self.channels = 2
        self.type = STEREO
        self.fs = 44100

    def decode(self):
        if self.type == STEREO:
            self.wave = decoder.to_stereo(self.W, self.X, self.Y, self.Z)
        else:
            self.wave = decoder.to_binaural(self.W, self.X, self.Y, self.Z)

    def export(self):
        return self.wave * dB(self.gain), self.channels, self.fs

    def reset(self):
        self.length = 1
        self.wave = np.zeros((self.length, self.channels))
        self.W = np.zeros(self.length)
        self.X = np.zeros(self.length)
        self.Y = np.zeros(self.length)
        self.Z = np.zeros(self.length)
        self.fs = 44100

    def receive(self, W, X, Y, Z):
        master_length = self.length
        track_length = W.size

        if master_length < track_length:
            self.W = np.pad(self.W, (0, track_length - master_length), 'constant')
            self.X = np.pad(self.X, (0, track_length - master_length), 'constant')
            self.Y = np.pad(self.Y, (0, track_length - master_length), 'constant')
            self.Z = np.pad(self.Z, (0, track_length - master_length), 'constant')

        self.W[:track_length] += W
        self.X[:track_length] += X
        self.Y[:track_length] += Y
        self.Z[:track_length] += Z


def dB(value):
    return np.power(10, value / 10)
