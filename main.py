#!venv/bin/python

from rhiz import *

tempo(60)

# my_tween = T(0, 127, 4)
P({C4, B2}, [C4, C3], (C4, D4), {24: 127}) * 3 >> 3
play()
