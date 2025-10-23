#!venv/bin/python

from rhiz import *

tempo(240)


# my_tween = T(0, 127, 4)
# S({C4, B2}, [{C4, C(20, 20)}, C3], (C4, D4), C(24, 127), feel=ease_out()) * 3 >> 3
# play()


my_tween = T(0, 127, rate=.25)
# S(C4, C(10, my_tween)) * 4
S(C4, T(C4, D4, rate=.25)) * 4  # rate here is awkward, no?
play()
