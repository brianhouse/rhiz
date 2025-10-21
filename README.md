# Rhiz

A sequencer for Python

## Concept

Markov chain patterns with native python structures

https://github.com/brianhouse/braid/tree/dd03c6c931574bdddae9f0eedb4125e811f7b527


## note offs

- if it's monophonic, you don't need noteoffs.
- if it isn't, then they have to be explicit anyway.
- the only situation you'd want it is if you want a polyphonic instrument to behave monophonically
- the problem is that it really should be customizable by channel



## Next


channel(3).play(pat)  # something like this? 
play(3, pat) # or this?

just need tween

arbitrary = T(0, 127, 4)
pat = C4, C4, {C4, {20: arbitrary}}

//


phase IS micro

an optional third term for probabilities [K, K, (S, K, .1), K]
if there are multiple probabilities, a single third term defines just the first, and the others split? or enforce the right number of probs?

sets with dict and notes do the dict first for paramter locks