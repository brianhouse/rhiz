from random import choice
from .note import _


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
        return "P%s" % list.__repr__(self)


def lcm(a, b):
    gcd, tmp = a, b
    while tmp != 0:
        gcd, tmp = tmp, gcd % tmp
    return a * b // gcd
