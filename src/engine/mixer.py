from src.engine.track import MasterTrack, InputTrack


class Mixer:
    def __init__(self, tracks_number):
        self.master = MasterTrack()
        self.tracks = []

        for i in range(tracks_number):
            self.tracks.append(InputTrack())
            self.tracks[i].phi = 15 * i
            self.tracks[i].theta = 15 * i
