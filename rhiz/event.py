from .config import config
from .midi import send_note, send_control
from random import randint


class Note():

    def __init__(self, name, n, accent=False, ghost=False, off=False):
        self.name = name
        self.n = n
        self.accent = accent
        self.ghost = ghost
        self.off = off

    def __pos__(self):
        return notes[f"{self.name}_ACCENT"]

    def __neg__(self):
        return notes[f"{self.name}_GHOST"]

    def __invert__(self):
        return notes[f"{self.name}_OFF"]

    def __lshift__(self, value):
        print("anticipate", value, "tatums")
        return self

    def __rrshift__(self, value):
        print("delay", value, "tatums")
        return self

    def __repr__(self):
        return (self.name if not self.ghost else f"-{self.name}") if not self.accent else f"+{self.name}"

    def play(self, channel):
        if self.n < 0:
            return
        if self.off:
            velocity = 0
        else:
            velocity = 127 - config['accent'] + (self.accent * config['accent']) - (self.ghost * config['ghost'])
            velocity -= randint(0, config['variance'])
        send_note(channel, self.n, int(velocity))


_names = "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"
notes = {}

for n in range(0, 128):
    name = _names[n % 12] + str((n // 12) - 1).replace("-1", "N")
    notes[name] = Note(name, n)
    notes[name + "_ACCENT"] = Note(name, n, accent=True)
    notes[name + "_GHOST"] = Note(name, n, ghost=True)
    notes[name + "_OFF"] = Note(name, n, off=True)

_ = Note("_", -1)


class Control():

    def __init__(self, control, value):
        self.control = control
        self.value = value

    def send(self, channel, value):
        send_control(channel, self.control, round(value))

    def __repr__(self):
        return f"{self.control}:{self.value}"


class ControlFactory():

    def __init__(self, control):
        self.control = control

    def __call__(self, value):
        return Control(self.control, value)


controls = {}

for c in range(0, 128):
    name = f"CC{c}"
    controls[name] = ControlFactory(c)

