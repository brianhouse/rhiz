import atexit, time
from .event import *
from .event import _
from .signal import *
from .pattern import Pattern


class Player():

    def __init__(self):
        self.stems = []
        self.tweens = []
        self.rate = 1.0

    def _add_stem(self, *pattern, rate=1.0, f=None):
        stem = Stem(pattern, rate, f)
        self.stems.append(stem)
        return stem

    def _add_tween(self, initial, target, rate=1.0, f=linear(), osc=False, saw=False):
        tween = Tween(initial, target, rate, f, osc, saw)
        self.tweens.append(tween)
        return tween

    def _play(self):
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

    def _stop(self):
        pass


class Stem():

    def __init__(self, pattern, rate, f):
        self._channel = 1
        self._repeat = 1
        self._pattern = Pattern(pattern)
        self._rate = rate
        self._f = f
        self._cycles = 0
        self._index = -1
        self._last_edge = 0
        self._steps = [_]

    def update(self, delta_t):
        self._cycles += delta_t * self._rate * _player.rate
        if self._cycles >= self._repeat:
            return True
        pos = self._cycles % 1.0
        if self._f is not None:
            pos = self._f(pos)
        i = int(pos * len(self._steps))
        if i != self._index or (len(self._steps) == 1 and int(self._cycles) != self._last_edge):  # contingency for whole notes
            self._index = (self._index + 1) % len(self._steps)  # dont skip steps
            if self._index == 0:
                # if isinstance(self.pattern, Tween):  # pattern tweens only happen on an edge
                #     pattern = self.pattern.value()
                # else:
                pattern = self._pattern
                self._steps = pattern.resolve()  # new patterns kick in here
                print(self._steps)
            self._handle_step(self._steps[self._index])
        self._last_edge = int(self._cycles)
        return False

    def _handle_step(self, step):
        if isinstance(step, Note):
            step.play(self._channel)
        elif isinstance(step, Control):
            step.send(self._channel, step.value if not isinstance(step.value, Tween) else step.value.value())
        elif isinstance(step, set):
            chord = list(step)
            chord.sort(key=lambda e: False if isinstance(e, Control) else True)
            for substep in chord:
                self._handle_step(substep)
        elif isinstance(step, Tween):
            self._handle_step(step.value())
        else:
            raise Exception(f"Got an unexpected step ({step})")

    def __mul__(self, repeat):
        assert isinstance(repeat, int)
        self._repeat = repeat
        return self

    def __rshift__(self, channel):
        assert isinstance(channel, int) and channel > 0 and channel < 16
        self._channel = channel
        return self


class Tween():

    def __init__(self, initial, target, rate, f=linear(), osc=False, saw=False):
        self._repeat = 1
        self._initial = initial
        self._target = target
        self._rate = rate
        self._f = f
        self._osc = osc
        self._saw = saw
        self._cycles = 0
        self._pos = 0

    def update(self, delta_t):
        self._cycles += delta_t * self._rate * _player.rate
        if self._cycles >= self._repeat:
            if self._saw:
                self._cycles = 0
            elif self._osc:
                target = self._target
                self._target = self._initial
                self._initial = target
                self._cycles = 0
            else:
                return True
        self._pos = self._cycles % 1.0
        self._pos = self._f(self._pos)
        return False

    def value(self):
        return (self._pos * (self._target - self._initial)) + self._initial

    def __repr__(self):
        return f"|{self._initial}>{self._target}|"


_player = Player()
play = _player._play
stop = _player._stop
S = _player._add_stem
T = _player._add_tween


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