# Rhiz

A sequencer for Python

## Concept

Markov chain patterns with native python structures

Timing is < 2ms accurate, which is below the 6ms minimal threshold of human perception

https://github.com/brianhouse/braid/tree/dd03c6c931574bdddae9f0eedb4125e811f7b527


## Next

perhaps phase does make sense


Are arbitrary functions executed?
(Would that allow over the barline stuff?)

the signal/timing/phase functions should be executed in a pattern! so it's all breakpoints, in a sense. does that work? how does the signal anticipate its length? but that would be so much better than sculpting a separate breakpoint and applying it.

hiz double accent? ++BD



current:
+ accent
- ghost
~ noteoff
N all notes off


maybe:
! accent  --- doesn't work! not unary?
~ ghost
N noteoff (becomes monosynth or MPE only)

+ anticipate
- delay

this works, maybe, but how on the backend? it would have to somehow build a signal


use @ instead of >> ?

Binary operators you can repurpose

    +, -, *, /, @, |, &, ^, <<, >>, %

Comparisons (<, >, ==, !=) also overloadable but must return booleans to be sane.

Magic methods that act like operators
__getitem__ (BD[...])
__call__ (BD(...))
__getattr__ (dynamic attributes)
__r*__ reverse versions of all of the above


actually, could do BD>>3 to show pushing it in some direction by some amount


ok, let's go with that. and then maybe >> and << to nudge by amounts?
because we'll have to build a signal anyway if we have

    lin, _, _ exp(2), _, _

//

ok, so @ could be rate, instead of passing it
and | could be phase, might as well include it

>> and << push individual notes...but it also calculates a smooth function between them, so complex curves are indeed possible 

some other symbol to actually send it to the midi channel 

to be consistent, might have to rethink tween; is that still param based?

T(start, target, rate)
T(start, target) @ rate | phase 


//

midi_out in order of preference