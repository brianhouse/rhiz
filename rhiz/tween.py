import types
import rhiz
from .pattern import Pattern, blend
from .signal import linear
from .event import Note
from random import random


class Tween():

    def __init__(self, initial, target, osc=False, saw=False):
        self.initial = initial
        self.target = target
        assert type(self.initial) is type(self.target)
        self.repeat = 1
        self.rate = 1
        self.phase = 0
        self.f = linear()
        self.osc = osc
        self.saw = saw
        self.cycles = 0
        self.pos = 0
        self._current = None

    def update(self, delta_t):
        self.cycles += delta_t * self.rate * rhiz.player.rate
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
        self.pos = (self.cycles + self.phase) % 1.0
        self.pos = self.f(self.pos)
        self._current = None
        return False

    def current(self):
        if not self._current:
            if isinstance(self.target, int) or isinstance(self.target, float):
                self._current = (self.pos * (self.target - self.initial)) + self.initial
                if isinstance(self.target, int):
                    self._current = round(self._current)
            elif isinstance(self.target, Note):
                self._current = self.initial if random() > self.pos else self.target
            elif isinstance(self.target, types.FunctionType):
                self._current = (self.initial(self.pos) + self.target(self.pos)) / 2
            elif isinstance(self.target, Pattern) or isinstance(self.target, tuple) or isinstance(self.target, list):
                self._current = blend(self.initial, self.target, self.pos)
            else:
                raise Exception(f"Unknown Tween type ({type(self.target)}) {self.target}")
        return self._current

    def __matmul__(self, rate):
        self.rate = rate
        return self

    def __mul__(self, value):
        if isinstance(value, int):
            self.repeat = value
        elif isinstance(value, types.FunctionType):
            self.f = value
        else:
            raise Exception("Unknown multiplier")
        return self

    def __mod__(self, phase):
        assert isinstance(phase, float) or isinstance(phase, int) and 0 <= phase <= 1
        self.phase = phase
        return self

    def __repr__(self):
        return f"|{self.current()}|"

