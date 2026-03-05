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

AXIS_CHANNELS = {
    "x": 1,
    "y": 2,
}

# convert axis (-1 to 1 ranged value) to midi (0 to 127)
def axis_to_midi(value):
    return int((value + 1) / 2 * 127) 

class Outport:
    def __init__(self):
        # We open an outport with the name that loopMIDI has assigned to it
        # Hardcoded for now
        self.outport = mido.open_output('N64 Controller 1')

        # we keep track of previous axis position
        # this allows us to avoid sending redundant messages when the axis does not move
        self.prev_x_midi = 0.0
        self.prev_y_midi = 0.0

        # we also keep track of prev hats to know which notes off to send
        self.prev_hats = [0,0]

    def send_button_down(self, button_name):
        message = mido.Message('note_on', channel=0, note=NOTE_MAP[button_name])
        self.outport.send(message)

    def send_button_up(self, button_name):
        message = mido.Message('note_off', channel=0, note=NOTE_MAP[button_name])
        self.outport.send(message)

    def send_axis_movement(self, axis):
        x, y = axis
        x_midi = axis_to_midi(x)
        y_midi = axis_to_midi(y)
        
        if x_midi != self.prev_x_midi:
            self.outport.send(mido.Message('control_change', channel=0, control=AXIS_CHANNELS['x'], value=x_midi))
            self.prev_x_midi = x_midi
        
        if y_midi != self.prev_y_midi:
            self.outport.send(mido.Message('control_change', channel=0, control=AXIS_CHANNELS['y'], value=y_midi))
            self.prev_y_midi = y_midi

    def send_hats_movement(self, hats):
        x, y = hats
        prev_x, prev_y = self.prev_hats

        if x == 1 and prev_x != 1:
            self.outport.send(mido.Message('note_on', channel=0, note=NOTE_MAP["RIGHTHAT"]))
        elif x != 1 and prev_x == 1:
            self.outport.send(mido.Message('note_off', channel=0, note=NOTE_MAP["RIGHTHAT"]))

        if x == -1 and prev_x != -1:
            self.outport.send(mido.Message('note_on', channel=0, note=NOTE_MAP["LEFTHAT"]))
        elif x != -1 and prev_x == -1:
            self.outport.send(mido.Message('note_off', channel=0, note=NOTE_MAP["LEFTHAT"]))

        if y == 1 and prev_y != 1:
            self.outport.send(mido.Message('note_on', channel=0, note=NOTE_MAP["UPHAT"]))
        elif y != 1 and prev_y == 1:
            self.outport.send(mido.Message('note_off', channel=0, note=NOTE_MAP["UPHAT"]))

        if y == -1 and prev_y != -1:
            self.outport.send(mido.Message('note_on', channel=0, note=NOTE_MAP["DOWNHAT"]))
        elif y != -1 and prev_y == -1:
            self.outport.send(mido.Message('note_off', channel=0, note=NOTE_MAP["DOWNHAT"]))

        self.prev_hats = hats
