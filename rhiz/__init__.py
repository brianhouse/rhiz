from .event import *
from .signal import *
from .tween import Tween
from .stem import Stem
import atexit, time


class Player():

    def __init__(self):
        self.stems = []
        self.tweens = []
        self.rate = 1.0

    def add_stem(self, *pattern, rate=1.0, f=None):
        stem = Stem(pattern, rate, f)
        self.stems.append(stem)
        return stem

    def add_tween(self, initial, target, rate=1.0, f=linear(), osc=False, saw=False):
        tween = Tween(initial, target, rate, f, osc, saw)
        self.tweens.append(tween)
        return tween

    def play(self):
        start_t = time.perf_counter()
        previous_t = 0.0
        try:
            while len(self.stems):
                c = time.perf_counter()
                t = c - start_t
                delta_t = t - previous_t
                for tween in self.tweens:
                    if tween.update(delta_t):
                        self.tweens.remove(tween)
                for stem in self.stems:
                    if stem.update(delta_t):
                        self.stems.remove(stem)
                rc = int((time.perf_counter() - c) * 1000)
                if rc > 1:
                    print(f"Warning: update took {rc}ms\n")
                previous_t = t
                time.sleep(0.01)
            self.stems.clear()
        except KeyboardInterrupt:
            pass

    def stop(self):
        pass


player = Player()
play = player.play
stop = player.stop
S = player.add_stem
T = player.add_tween


def tempo(value=False):
    """Convert to a multiplier of 1hz"""
    if value:
        value /= 60.0
        value /= 4.0
        player.rate = value
    else:
        return player.rate * 4.0 * 60.0


def _exit_handler():
    stop()
    time.sleep(0.1)  # for midi to finish
    print("\n-------------> X")


atexit.register(_exit_handler)


tempo(115)
