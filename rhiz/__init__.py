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


class Stem():

    def __init__(self, pattern, rate, f):
        self.channel = 1
        self.repeat = 1
        self.pattern = Pattern(pattern)
        self.rate = rate
        self.f = f
        self.cycles = 0
        self.index = -1
        self.last_edge = 0
        self.steps = [_]

    def update(self, delta_t):
        self.cycles += delta_t * self.rate * player.rate
        if self.cycles >= self.repeat:
            return True
        pos = self.cycles % 1.0
        if self.f is not None:
            pos = self.f(pos)
        i = int(pos * len(self.steps))
        if i != self.index or (len(self.steps) == 1 and int(self.cycles) != self.last_edge):  # contingency for whole notes
            self.index = (self.index + 1) % len(self.steps)  # dont skip steps
            if self.index == 0:
                # if isinstance(self.pattern, Tween):  # pattern tweens only happen on an edge
                #     pattern = self.pattern.value()
                # else:
                pattern = self.pattern
                self.steps = pattern.resolve()  # new patterns kick in here
                print(self.steps)
            self._handle_step(self.steps[self.index])
        self.last_edge = int(self.cycles)
        return False

    def _handle_step(self, step):
        if isinstance(step, Note):
            step.play(self.channel)
        elif isinstance(step, Control):
            step.send(self.channel, step.value if not isinstance(step.value, Tween) else step.value.current())
        elif isinstance(step, set):
            chord = list(step)
            chord.sort(key=lambda e: False if isinstance(e, Control) else True)
            for substep in chord:
                self._handle_step(substep)
        elif isinstance(step, Tween):
            self._handle_step(step.current())
        else:
            raise Exception(f"Got an unexpected step ({step})")

    def __mul__(self, repeat):
        assert isinstance(repeat, int)
        self.repeat = repeat
        return self

    def __rshift__(self, channel):
        assert isinstance(channel, int) and channel > 0 and channel < 16
        self.channel = channel
        return self


class Tween():

    def __init__(self, initial, target, rate, f=linear(), osc=False, saw=False):
        self.repeat = 1
        self.initial = initial
        self.target = target
        self.rate = rate
        self.f = f
        self.osc = osc
        self.saw = saw
        self.cycles = 0
        self.pos = 0

    def update(self, delta_t):
        self.cycles += delta_t * self.rate * player.rate
        if self.cycles >= self.repeat:
            if self.saw:
                self.cycles = 0
            elif self.osc:
                target = self.target
                self.target = self.initial
                self.initial = target
                self.cycles = 0
            else:
                return True
        self.pos = self.cycles % 1.0
        self.pos = self.f(self.pos)
        return False

    def current(self):
        return (self.pos * (self.target - self.initial)) + self.initial

    def __repr__(self):
        return f"|{self.initial}>{self.target}|"


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