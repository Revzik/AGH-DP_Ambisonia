from src.engine.track import Track, MonoTrack, MasterTrack


class Mixer:
    def __init__(self):
        self.master = None
        self.tracks = []

