from .event import *
from .event import _
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
        try:
            t = time.perf_counter()
            while len(self.stems):
                delta_t = time.perf_counter() - t
                t = time.perf_counter()
                for tween in self.tweens:
                    if tween.update(delta_t):
                        self.tweens.remove(tween)
                for stem in self.stems:
                    if stem.update(delta_t):
                        self.stems.remove(stem)
                update_elapsed_ms = int((time.perf_counter() - t) * 1000)
                if update_elapsed_ms > 1:
                    print(f"Warning: update took {update_elapsed_ms}ms")
                _timed_sleep()
            self.stems.clear()
        except KeyboardInterrupt:
            exit()
        except Exception as e:
            print(e)
            exit()

    def stop(self):
        exit()


def _timed_sleep(duration=0.001):
    sleep_start_t = time.perf_counter()
    time.sleep(duration)
    sleep_elapsed_ms = int((time.perf_counter() - sleep_start_t) * 1000)
    if sleep_elapsed_ms >= config['sleep_warning']:
        print(f"Warning: sleep() took {sleep_elapsed_ms}ms")


def _exit_handler():
    # panic()
    time.sleep(0.1)  # for midi to finish
    print("\n-------------> X")


atexit.register(_exit_handler)


def tempo(value=False):
    """Convert to a multiplier of 1hz"""
    if value:
        value /= 60.0
        value /= 4.0
        player.rate = value
    else:
        return player.rate * 4.0 * 60.0


player = Player()
play = player.play
stop = player.stop
S = player.add_stem
T = player.add_tween


tempo(115)
