import rhiz
from .pattern import Pattern
from .event import Note, Control, _
from .tween import Tween


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
        self.cycles += delta_t * self.rate * rhiz.player.rate
        if self.cycles >= self.repeat:
            return True
        pos = self.cycles % 1.0
        if self.f is not None:
            pos = self.f(pos)
        i = int(pos * len(self.steps))
        if i != self.index or (len(self.steps) == 1 and int(self.cycles) != self.last_edge):  # contingency for whole notes
            self.index = (self.index + 1) % len(self.steps)  # dont skip steps
            if self.index == 0:
                # print("pattern", self.pattern, type(self.pattern))
                # if isinstance(self.pattern, Tween):  # pattern tweens only happen on an edge
                #     pattern = self.pattern.value()
                #     print("resolved", pattern)
                # else:
                #     pattern = self.pattern
                self.steps = self.pattern.resolve()  # new patterns kick in here
                print(self.steps)
            self._handle_step(self.steps[self.index])
        self.last_edge = int(self.cycles)
        return False

    def _handle_step(self, step):
        if isinstance(step, Note):
            step.play(self.channel)
        elif isinstance(step, Control):
            value = step.value if not isinstance(step.value, Tween) else step.value.current()
            if value is None:
                raise Exception("No value for CC")
            step.send(self.channel, value)
        elif isinstance(step, set):
            chord = list(step)
            chord.sort(key=lambda e: False if isinstance(e, Control) else True)
            for substep in chord:
                self._handle_step(substep)
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
