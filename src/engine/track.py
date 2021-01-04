import numpy as np
import simpleaudio as sa
from PyQt5.QtWidgets import QFileDialog

from src.io import open_wav
from src.coding import encoder


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


class MonoTrack(Track):
    def __init__(self):
        super().__init__()

        self.channels = 1

    def load(self):
        try:
            dialog = QFileDialog()
            dialog.setFileMode(QFileDialog.ExistingFile)
            dialog.setNameFilter("Wave files (*.wav)")
            if dialog.exec_():
                path = dialog.selectedFiles()
                self.wave, self.fs = open_wav.load(path[0])
                self.loaded = True
        except Exception as e:
            print(e)
            self.loaded = False

    def encode(self):
        self.W, self.X, self.Y, self.Z = encoder.b_format(self.wave, self.phi, self.theta)


class MasterTrack(Track):
    def __init__(self):
        super().__init__()

        self.channels = 1

    def save(self):
        pass

    def decode(self):
        pass

    def play(self):

