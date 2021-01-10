import numpy as np
import simpleaudio as sa

from src.io import open_wav
from src.coding import encoder, decoder


MONO = 'mono'
STEREO = 'stereo'
BINAURAL = 'binaural'


class Track:
    def __init__(self):
        self.loaded = False

        self.wave = None
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
        self.fs = 0


class InputTrack(Track):
    def __init__(self):
        super().__init__()

    def load(self, path):
        self.wave, self.channels, self.fs = open_wav.load_wav(path)
        self.loaded = True
        if self.channels == 1:
            self.type = MONO
        else:
            self.type = STEREO

        print('Loaded track from {}, track type: {}, track sample rate: {}'.
              format(path, self.type, self.fs))

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


class MasterTrack(Track):
    def __init__(self):
        super().__init__()

        self.channels = 2
        self.type = STEREO
        self.inputs = []

    def update(self):
        self.reset()
        for i in self.inputs:
            self.W += i.W
            self.X += i.X
            self.Y += i.Y
            self.Z += i.Z
        self.decode()

    def decode(self):
        if self.type == STEREO:
            self.wave = decoder.to_stereo(self.W, self.X, self.Y, self.Z)
        else:
            self.wave = decoder.to_binaural(self.W, self.X, self.Y, self.Z)

    def play(self):
        pass

    def save(self):
        pass
