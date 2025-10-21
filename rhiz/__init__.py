import atexit, time
from .note import *
from .note import _
from .pattern import Pattern


class Player():

    def __init__(self):
        self.stems = []
        self.rate = 1.0

    def _play(self, channel, pattern, cycles=True, rate=1.0, micro=None):
        self.stems.append(Stem(channel, pattern, cycles, rate, micro))

    def _sync(self):
        start_t = time.perf_counter()
        previous_t = 0.0
        try:
            while len(self.stems):
                t = time.perf_counter() - start_t
                delta_t = t - previous_t
                for stem in self.stems:
                    c = time.perf_counter()
                    if stem.update(delta_t):
                        self.stems.remove(stem)
                    rc = int((time.perf_counter() - c) * 1000)
                    if rc > 1:
                        print("[Warning: update took %dms]\n>>> " % rc, end='')
                previous_t = t
                time.sleep(0.01)
            self.stems.clear()
        except KeyboardInterrupt:
            pass

    def _stop(self):
        pass


class Stem():

    def __init__(self, channel, pattern, cycles, rate=1.0, micro=None):
        self._channel = channel
        self._pattern = Pattern(pattern)
        self.cycles = cycles
        self._rate = rate
        self._micro = micro
        self._cycles = 0
        self._index = -1
        self._last_edge = 0
        self._steps = [_]

    def update(self, delta_t):
        self._cycles += delta_t * self._rate * _player.rate
        if self._cycles >= self.cycles:
            return True
        pos = self._cycles % 1.0
        if self._micro is not None:
            pos = self._micro(pos)
        i = int(pos * len(self._steps))
        if i != self._index or (len(self._steps) == 1 and int(self._cycles) != self._last_edge):  # contingency for whole notes
            self._index = (self._index + 1) % len(self._steps)  # dont skip steps
            if self._index == 0:
                # if isinstance(self.pattern, Tween):  # pattern tweens only happen on an edge
                #     pattern = self.pattern.value()
                # else:
                pattern = self._pattern
                self._steps = pattern.resolve()  # new patterns kick in here
            self._handle_step(self._steps[self._index])
        self._last_edge = int(self._cycles)
        return False

    def _handle_step(self, step):
        if isinstance(step, Note):
            step.play(self._channel)
        else:
            if isinstance(step, set):
                for substep in step:
                    self._handle_step(substep)
            elif isinstance(step, dict):
                pass
            else:
                raise Exception("Got an unexpected step")


_player = Player()
play = _player._play
sync = _player._sync
stop = _player._stop


def tempo(value=False):
    """Convert to a multiplier of 1hz"""
    if value:
        value /= 60.0
        value /= 4.0
        _player.rate = value
    else:
        return _player.rate * 4.0 * 60.0


def _exit_handler():
    stop()
    time.sleep(0.1)  # for midi to finish
    print("\n-------------> X")


atexit.register(_exit_handler)


tempo(115)