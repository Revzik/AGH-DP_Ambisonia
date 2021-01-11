import simpleaudio as sa
import numpy as np


class Player:
    def __init__(self):
        self.play_obj = None

    def play(self, wave, channels, fs):
        wave = np.array(wave.T * 32767, dtype=np.int16, order='C')
        self.play_obj = sa.play_buffer(wave, channels, 2, fs)

    def stop(self):
        if self.play_obj is not None and self.play_obj.is_playing:
            self.play_obj.stop()
