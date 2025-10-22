#!/usr/bin/env python3

import sys, time, threading, queue, rtmidi
from rtmidi.midiconstants import NOTE_ON, NOTE_OFF, CONTROLLER_CHANGE
from .config import config


class MidiOut(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.interface = config['midi_in']
        self.midi = rtmidi.MidiOut()
        self.queue = queue.Queue()
        self.throttle = config['throttle']
        self.send_note_offs = config['send_note_offs']
        self.note_ons = {}
        available_interfaces = self.midi.get_ports()
        if available_interfaces and self.interface is not None:
            if self.interface not in available_interfaces:
                print(f"Interface index {self.interface} not available")
                print(f"MIDI outputs available: {available_interfaces}")
                exit()
            print(f"MIDI OUT: {self.interface}")
            self.midi.open_port(available_interfaces.index(self.interface))
        else:
            print("MIDI OUT opening virtual interface 'Rhiz'...")
            self.midi.open_virtual_port('Rhiz')
        self.start()

    def send_control(self, channel, control, value):
        self.queue.put((channel, (control, value), None))

    def send_note(self, channel, pitch, velocity):
        if self.send_note_offs:
            if channel in self.note_ons:
                self.queue.put((channel, None, (self.note_ons[channel], 0)))
            self.note_ons[channel] = pitch
        self.queue.put((channel, None, (pitch, velocity)))

    def run(self):
        while True:
            channel, control, note = self.queue.get()
            if control is not None:
                control, value = control
                if isinstance(value, bool):
                    value = 127 if value else 0
                if config['log_midi']:
                    print("MIDI ctrl %s %s %s" % (channel, control, value))
                channel -= 1
                self.midi.send_message([CONTROLLER_CHANGE | (channel & 0xF), control, value])
            if note is not None:
                pitch, velocity = note
                if config['log_midi']:
                    print("MIDI note %s %s %s" % (channel, pitch, velocity))
                channel -= 1
                if velocity:
                    self.midi.send_message([NOTE_ON | (channel & 0xF), pitch & 0x7F, velocity & 0x7F])
                else:
                    self.midi.send_message([NOTE_OFF | (channel & 0xF), pitch & 0x7F, 0])
            if self.throttle > 0:
                time.sleep(self.throttle)


# class MidiIn(threading.Thread):

#     def __init__(self):
#         threading.Thread.__init__(self)
#         self.daemon = True
#         self.interface = config['midi_in']
#         self.midi = rtmidi.MidiIn()
#         self.queue = queue.Queue()
#         self.callbacks = {}
#         self.threads = []
#         available_interfaces = self.midi.get_ports()
#         if available_interfaces and self.interface is not None:
#             if self.interface not in available_interfaces:
#                 print(f"Interface index {self.interface} not available")
#                 print(f"MIDI inputs available: {available_interfaces}")
#                 exit()
#             print(f"MIDI IN: {self.interface}")
#             self.midi.open_port(available_interfaces.index(self.interface))
#         self.start()

#     def run(self):
#         def receive_message(event, data=None):
#             message, deltatime = event
#             if message[0] & 0b11110000 == CONTROLLER_CHANGE:
#                 nop, control, value = message
#                 self.queue.put((control, value / 127.0))
#             elif (message[0] & 0b11110000 == NOTE_ON):
#                 if len(message) < 3:
#                     return  # ?
#                 channel, pitch, velocity = message
#                 channel -= NOTE_ON
#                 if channel < len(self.threads):
#                     thread = self.threads[channel]
#                     thread.note(pitch, velocity)
#         self.midi.set_callback(receive_message)
#         while True:
#             time.sleep(0.1)

#     def perform_callbacks(self):
#         while True:
#             try:
#                 control, value = self.queue.get_nowait()
#             except queue.Empty:
#                 return
#             if control in self.callbacks:
#                 if num_args(self.callbacks[control]) > 0:
#                     self.callbacks[control](value)
#                 else:
#                     self.callbacks[control]()

#     def callback(self, control, f):
#         """For a given control message, call a function"""
#         self.callbacks[control] = f


midi_out = MidiOut()
# midi_in = MidiIn()
