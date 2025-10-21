#!venv/bin/python

from rhiz import *

tempo(60)

# pat = {C4, B2}, [C4, C3], (C4, D4), {24: 127}
pat = C4, [C4, C4], C4, [C4, C4]

play(2, pat)

sync()