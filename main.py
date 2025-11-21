#!venv/bin/python

from rhiz import *

# globs = list(globals().keys())
# for item in globs:
#     print(item)

# print('done')

# exit()

tempo(130)

# my_tween = T(0, 127, 4)
# S({C4, B2}, [{C4, C(20, 20)}, C3], (C4, D4), C(24, 127), feel=ease_out()) * 3 >> 3
# play()


# my_tween = T(0, 127, rate=.25)
# # S(C4, C(10, my_tween)) * 4
# S(C4, T(C4, D4, rate=.25)) * 4  # rate here is awkward, no?
# play()

# p1 = C1, C1, C1, C1
# p2 = D1, D1, D1
# combo = T(p1, p2, .25)
# S(combo) * 4 >> 3


# while True:
#     S(BD, +BD, (BD, [BD, BD, _, _]), (+BD, [+BD, (BD, [BD, BD])])) * 4 >> tanz
#     S(HH, [OH, (HH, [HH, HH])], +HH, [OH, HH], (HH, HH, [HH, HH, HH]), [OH, HH], +HH, OH) * 4 >> tanz
#     S(_, {CL, SD}, ((_, -SD), [_, _, -CL, ]), {CL, SD}) * 4 >> tanz
#     play()


funcc = T(0, 127, .25)

while True:
    print(funcc)
    S(BD, BD, BD, CC42(funcc)) >> tanz
    play()


# while True:
#     S([HH, HH, HH, HH]*8) * 4 >> 3
#     S([BD2, BD2, BD2, BD2]*4) * 4 >> 3
#     play()