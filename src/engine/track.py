from src.io import open_wav
from src.coding import encoder


class Track:
    def __init__(self):
        self.loaded = False

        self.wave = None
        self.gain = 0
        self.fs = 0

        self.W = None
        self.X = None
        self.Y = None
        self.Z = None

        self.phi = 0
        self.theta = 0

    def load(self, path):
        try:
            self.wave, self.fs = open_wav.load(path)
            self.loaded = True
        except Exception as e:
            print(e)
            self.loaded = False
