from .config import config
from .event import _, notes, controls
from .signal import plot, show_plots, linear, ease_in, ease_out, ease_in_out, ease_out_in, timeseries, breakpoints, cross
from .tween import Tween
from .stem import Stem
import atexit, time, sys, os


class Player():

    def __init__(self):
        self.stems = []
        self.tweens = []
        self.rate = 1.0

    def add_stem(self, *pattern):
        stem = Stem(pattern)
        self.stems.append(stem)
        return stem

    def add_tween(self, initial, target, osc=False, saw=False):
        tween = Tween(initial, target, osc, saw)
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
            print(exc(e))
            exit()

    def stop(self):
        exit()


def _timed_sleep(duration=0.001):
    sleep_start_t = time.perf_counter()
    if config['overdrive']:
        while time.perf_counter() - sleep_start_t < duration:
            pass
    else:
        time.sleep(duration)
    sleep_elapsed_ms = int((time.perf_counter() - sleep_start_t) * 1000)
    if sleep_elapsed_ms > config['sleep_warning']:
        print(f"Warning: sleep() took {sleep_elapsed_ms}ms")


def _exit_handler():
    # panic()
    time.sleep(0.1)  # for midi to finish
    print("\n-------------> X")


atexit.register(_exit_handler)


def exc(e):
    return "%s <%s:%s> %s" % (sys.exc_info()[0].__name__, os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1], sys.exc_info()[2].tb_lineno, e)


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


__all__ = ["play", "stop", "tempo", "S", "T", "_", "plot", "show_plots", "linear", "ease_in", "ease_out", "ease_in_out", "ease_out_in", "timeseries", "breakpoints", "cross"]
for name, note in notes.items():
    globals()[name] = note
__all__.extend(notes)
for name, control in controls.items():
    globals()[name] = control
__all__.extend(controls)


if 'map' in config:
    mappings = {}
    for key, value in config['map'].items():
        if isinstance(value, (int, float)):
            pass
        elif isinstance(value, str) and value in __all__ and value in globals():
            value = globals()[value]
        else:
            print("Unknown mapping")
        globals()[key] = value
        mappings[key] = value
    __all__.extend(mappings)


tempo(115)
