from . import tween
from .event import _
from .signal import ease_in, ease_out
from random import choice, random


class Pattern(list):

    def __init__(self, value=[_]):
        list.__init__(self, value)

    def resolve(self):
        """Choose a path through the Markov chain"""
        return self._unroll(self._traverse(self))

    def _traverse(self, pattern):
        """Resolve a subbranch of the pattern"""
        steps = []
        for step in pattern:
            while isinstance(step, tuple):
                step = choice(step)
            if isinstance(step, list):
                step = self._traverse(step)
            if isinstance(step, tween.Tween):
                step = self._traverse(step.current())
            steps.append(step)
        return steps

    def _unroll(self, pattern, divs=None, r=None):
        """Unroll a compacted form to a pattern with lcm steps"""
        if divs is None:
            divs = self._get_divs(pattern)
            r = []
        elif r is None:
            r = []
        for step in pattern:
            if isinstance(step, list):
                self._unroll(step, (divs // len(pattern)), r)
            else:
                r.append(step)
                for i in range((divs // len(pattern)) - 1):
                    r.append(_)
        return r

    def _get_divs(self, pattern):
        """Find lcm for a subpattern"""
        subs = [(self._get_divs(step) if isinstance(step, list) else 1) * len(pattern) for step in pattern]
        divs = subs[0]
        for step in subs[1:]:
            divs = lcm(divs, step)
        return divs

    def __repr__(self):
        return f"P{list.__repr__(self)}"


def blend(pattern_1, pattern_2, balance=0.5):
    """Probabalistically blend two Patterns"""
    pattern, p1_steps, p2_steps, p1_div, p2_div = prep(pattern_1, pattern_2)
    for i, cell in enumerate(pattern):
        if i % p1_div == 0 and i % p2_div == 0:
            if random() > balance:
                pattern[i] = p1_steps[int(i / p1_div)]
            else:
                pattern[i] = p2_steps[int(i / p2_div)]
        elif i % p1_div == 0:
            if random() > ease_out()(balance):     # avoid empty middle from linear blend
                pattern[i] = p1_steps[int(i / p1_div)]
        elif i % p2_div == 0:
            if random() <= ease_in()(balance):
                pattern[i] = p2_steps[int(i / p2_div)]
    pattern = Pattern(pattern)
    return pattern


def prep(pattern_1, pattern_2):
    if not isinstance(pattern_1, Pattern):
        pattern_1 = Pattern(pattern_1)
    if not isinstance(pattern_2, Pattern):
        pattern_2 = Pattern(pattern_2)
    p1_steps = pattern_1.resolve()
    p2_steps = pattern_2.resolve()
    pattern = [_] * lcm(len(p1_steps), len(p2_steps))
    p1_div = len(pattern) / len(p1_steps)
    p2_div = len(pattern) / len(p2_steps)
    return pattern, p1_steps, p2_steps, p1_div, p2_div


def lcm(a, b):
    gcd, tmp = a, b
    while tmp != 0:
        gcd, tmp = tmp, gcd % tmp
    return a * b // gcd
