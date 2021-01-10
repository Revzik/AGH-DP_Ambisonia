from src.engine.track import MasterTrack, InputTrack
from src.io import player, file


class Mixer:
    def __init__(self, tracks_number):
        self.master = MasterTrack()
        self.tracks = []
        self.player = player.Player()

        for i in range(tracks_number):
            self.tracks.append(InputTrack())

    def update_master(self):
        self.master.reset()
        for t in self.tracks:
            if t.loaded:
                t.encode()
                W, X, Y, Z = t.send()
                self.master.receive(W, X, Y, Z)
        self.master.decode()

    def play(self):
        self.update_master()
        wave, channels, fs = self.master.export()
        self.player.play(wave, channels, fs)

    def stop(self):
        self.player.stop()

    def export(self, path):
        self.update_master()
        wave, channels, fs = self.master.export()
        file.save_wav(path, wave, fs)
