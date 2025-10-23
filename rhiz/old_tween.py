import collections, math
from random import random
from .signal import linear
from .pattern import Pattern, blend, euc, add, xor
from .core import driver


class Tween(object):

    def __init__(self, target_value, cycles, signal_f=linear(), on_end=None, osc=False, saw=False, start_value=None):
        self.target_value = target_value
        self.cycles = cycles
        self.signal_f = signal_f
        self.end_f = on_end
        self.osc = osc
        self.saw = saw
        self.start_value = start_value
        self.finished = False

    def start(self, thread, start_value):
        self.thread = thread
        self.start_value = start_value if self.start_value is None else self.start_value    # needed for osc
        self.start_cycle = float(math.ceil(self.thread._cycles)) # tweens always start on next cycle

    @property
    def value(self):
        if self.finished:
            return self.target_value
        return self.calc_value(self.signal_position)

    @property
    def signal_position(self): # can reference this to see where we are on the signal function
        return self.signal_f(self.position)

    @property
    def position(self): # can reference this to see where we are in the tween
        if self.cycles == 0.0:
            return 1.0
        position = (self.thread._cycles - self.start_cycle) / self.cycles
        if position <= 0.0:
            position = 0.0
        if position >= 1.0:
            position = 1.0
            if self.end_f is not None:
                try:
                    self.end_f()
                except Exception as e:
                    print("[Error tween.on_end: %s]" % e)
            if self.osc or self.saw:
                if self.osc:
                    sv = self.target_value
                    self.target_value = self.start_value
                    self.start_value = sv
                self.start_cycle = self.thread._cycles - ((self.thread._cycles - self.start_cycle) - self.cycles)
                position = abs(1 - position)
            else:
                self.finished = True
                print('finished is true')
        return position


class ScalarTween(Tween):

    def calc_value(self, position):
        value = (position * (self.target_value - self.start_value)) + self.start_value
        return value


class PatternTween(Tween):

    def calc_value(self, position):
        return blend(self.start_value, self.target_value, position)


def tween(value, cycles, signal_f=linear(), on_end=None, osc=False, saw=False, start=None):
    if type(value) == int or type(value) == float:
        return ScalarTween(value, cycles, signal_f, on_end, osc, saw, start)
    if type(value) == tuple:
        return ChordTween(value, cycles, signal_f, on_end, osc, saw, start)
    if type(value) == list: # careful, lists are always patterns
        value = Pattern(value)
    if type(value) == Pattern:
        return PatternTween(value, cycles, signal_f, on_end, osc, saw, start)

def osc(start, value, cycles, signal_f=linear(), on_end=None):
    return tween(value, cycles, signal_f, on_end, True, False, start)

def saw(start, value, cycles, signal_f=linear(), on_end=None, saw=True):
    return tween(value, cycles, signal_f, on_end, False, True, start)