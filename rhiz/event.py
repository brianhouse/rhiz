from random import random
from .config import config
from .midi import midi_out


class Note():

    def __init__(self, name, n, accent=False, ghost=False, off=False):
        self.name = name
        self.n = n
        self.accent = accent
        self.ghost = ghost
        self.off = off

    def __pos__(self):
        return globals()[f"{self.name}_ACCENT"]

    def __neg__(self):
        return globals()[f"{self.name}_GHOST"]

    def __invert__(self):
        return globals()[f"{self.name}_OFF"]

    def __repr__(self):
        return (self.name if not self.ghost else f"-{self.name}") if not self.accent else f"+{self.name}"

    def play(self, channel):
        if self.n < 0:
            return
        if self.off:
            velocity = 0
        else:
            velocity = 1. - config['accent'] + (self.accent * config['accent']) - (self.ghost * config['ghost'])
            velocity -= random() * config['variance']
        midi_out.send_note(channel, self.n, int(velocity * 127))


class Control():

    def __init__(self, control, value):
        self.control = control
        self.value = value

    def send(self, channel, value):
        midi_out.send_control(channel, self.control, int(value))

    def __repr__(self):
        return f"{self.control}:{self.value}"


_names = "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"


for n in range(0, 128):
    name = _names[n % 12] + str((n // 12) - 1).replace("-1", "N")
    globals()[name] = Note(name, n)
    globals()[name + "_ACCENT"] = Note(name, n, accent=True)
    globals()[name + "_GHOST"] = Note(name, n, ghost=True)
    globals()[name + "_OFF"] = Note(name, n, off=True)


_ = Note("_", -1)

C = Control
