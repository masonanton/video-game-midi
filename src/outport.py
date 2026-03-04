# WINDOWS DOES NOT SUPPORT VIRTUAL MIDIS
# Therefore, must use a virtual loopback MIDI Cable
# I used loopMIDI - https://www.tobias-erichsen.de/software/loopmidi.html
# Created a new MIDI port named N64 Controller

import mido

NOTE_MAP = {
    "A": 60,  # C4
    "B": 62,  # D4
    "CUP": 64,  # E4
    "CDOWN": 65,  # F4
    "CLEFT": 67,  # G4
    "CRIGHT": 69,  # A4
    "Z": 71,  # B4
    "L": 72,  # C5
    "R": 74,  # D5
    "START": 76,  # E5
    "UPHAT": 77,  # F5
    "DOWNHAT": 79,  # G5
    "LEFTHAT": 81,  # A5
    "RIGHTHAT": 83,  # B5
}

# Axis control change channels
AXIS_CC = {
    "x": 1,
    "y": 2,
}

class Outport:
    def __init__(self):
        # We open an outport with the name that loopMIDI has assigned to it
        # Hardcoded for now
        self.outport = mido.open_output('N64 Controller 1')

    def send_button_down(self, button_name):
        message = mido.Message('note_on', note=NOTE_MAP[button_name])
        self.outport.send(message)

    def send_button_up(self, button_name):
        message = mido.Message('note_off', note=NOTE_MAP[button_name])
        self.outport.send(message)

    def send_axis_movement(self):
        pass

    def send_hats_movement(self):
        pass