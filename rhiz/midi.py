import sys, time, threading, queue, rtmidi
from rtmidi.midiconstants import NOTE_ON, NOTE_OFF, CONTROLLER_CHANGE
from .config import config


midi_out = rtmidi.MidiOut()
note_ons = {}


available_interfaces = midi_out.get_ports()
print(f"Available interfaces: {available_interfaces}")
if available_interfaces and config['midi_out'] is not None:
    if config['midi_out'] not in available_interfaces:
        print(f"Interface index {config['midi_out']} not available")
        print(f"MIDI outputs available: {available_interfaces}")
        exit()
    print(f"MIDI OUT: {config['midi_out']}")
    midi_out.open_port(available_interfaces.index(config['midi_out']))
else:
    print("MIDI OUT opening virtual interface 'Rhiz'...")
    midi_out.open_virtual_port('Rhiz')


def send_control(channel, control, value):
    if config['log_midi']:
        print(f"MIDI ctrl {channel} {control} {value}")
    midi_out.send_message([CONTROLLER_CHANGE | (channel - 1 & 0xF), control, value])
    if config['throttle'] > 0:
        time.sleep(config['throttle'] / 1000)


def send_note(channel, pitch, velocity):
    if config['send_note_offs']:
        if channel in note_ons:
            send_note(channel, note_ons[channel], 0)
        note_ons[channel] = pitch
    if config['log_midi']:
        print(f"MIDI note {channel} {pitch} {velocity}")
    if velocity:
        midi_out.send_message([NOTE_ON | (channel - 1 & 0xF), pitch & 0x7F, velocity & 0x7F])
    else:
        midi_out.send_message([NOTE_OFF | (channel - 1 & 0xF), pitch & 0x7F, 0])
    if config['throttle'] > 0:
        time.sleep(config['throttle'] / 1000)

