import numpy as np
import simpleaudio as sa
from PyQt5.QtWidgets import QFileDialog

from src.io import open_wav
from src.coding import encoder, decoder


class Track:
    def __init__(self):
        self.loaded = False

        self.wave = None
        self.channels = 1
        self.gain = 0
        self.fs = 0

        self.W = None
        self.X = None
        self.Y = None
        self.Z = None

        self.phi = 0
        self.theta = 0

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

    def load(self):
        try:
            dialog = QFileDialog()
            dialog.setFileMode(QFileDialog.ExistingFile)
            dialog.setNameFilter("Wave files (*.wav)")
            if dialog.exec_():
                path = dialog.selectedFiles()
                self.wave, self.fs = open_wav.load_wav(path[0])
                self.loaded = True
        except Exception as e:
            print(e)
            self.loaded = False

    def encode(self):
        pass


class MonoTrack(InputTrack):
    def __init__(self):
        super().__init__()

        self.channels = 1

    def encode(self):
        self.W, self.X, self.Y, self.Z = encoder.b_format(self.wave, self.phi, self.theta)


class StereoTrack(InputTrack):
    def __init__(self):
        super().__init__()

        self.channels = 2
        self.stereo_angle = 30

    def encode(self):
        W_l, X_l, Y_l, Z_l = encoder.b_format(self.wave[:, 0], self.phi - self.stereo_angle, self.theta)
        W_r, X_r, Y_r, Z_r = encoder.b_format(self.wave[:, 0], self.phi + self.stereo_angle, self.theta)
        self.W = W_l + W_r
        self.X = X_l + X_r
        self.Y = Y_l + Y_r
        self.Z = Z_l + Z_r


class MasterTrack(Track):
    def __init__(self):
        super().__init__()

        self.channels = 1
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
        self.wave = decoder.to_stereo(self.W, self.X, self.Y, self.Z)

    def play(self):
        pass

    def save(self):
        pass
