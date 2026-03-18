# N64 MIDI Controller

Turn an N64 controller into a live musical instrument. Button presses send MIDI notes, the joystick sends continuous control signals, and a 3D visualizer responds to your input in real time.

---

## What it does

- **Buttons** (A, B, C-buttons, Z, L, R, Start) trigger MIDI note on/off messages
- **D-pad** triggers MIDI notes on a separate channel (mapped to drum-style sounds)
- **Joystick** sends MIDI CC messages for continuous X/Y control
- A **controller display window** shows a live outline of the N64 controller with buttons highlighted as you press them
- A **3D visualizer window** renders a spinning point-cloud cube that reacts to your input — buttons spin it, the joystick warps it, and the d-pad shifts its color

If no physical controller is detected, a keyboard fallback is available.

---

## Requirements

### Hardware
- An N64 controller with a USB adapter (or similar HID joystick)
- A virtual MIDI loopback cable (Windows: [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html); macOS/Linux have built-in options)

### Software dependencies

```
pygame
mido
python-rtmidi
PyOpenGL
glfw
```

Install with:

```bash
pip install -r requirements.txt
```

---

## MIDI setup

On Windows, this project requires a virtual MIDI loopback port. The default port name expected is `N64 Controller 1`.

1. Download and install [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)
2. Create a new port named `N64 Controller`
3. loopMIDI will name it `N64 Controller 1` — this matches what the code expects

On macOS or Linux, you can create a virtual MIDI port through the OS and update the port name in `outport.py` accordingly.

---

## MIDI mappings

### Buttons → Notes (Channel 0) (These can be changed in the code)

| Button  | MIDI Note | Pitch |
|---------|-----------|-------|
| A       | 60        | C4    |
| B       | 62        | D4    |
| C-Up    | 64        | E4    |
| C-Down  | 65        | F4    |
| C-Left  | 67        | G4    |
| C-Right | 69        | A4    |
| Z       | 71        | B4    |
| L       | 72        | C5    |
| R       | 74        | D5    |
| Start   | 76        | E5    |

### D-pad → Notes (Channel 2)

| Direction | MIDI Note | Sound   |
|-----------|-----------|---------|
| Up        | 36        | Kick    |
| Down      | 40        | Clap    |
| Left      | 44        | Hi-hat  |
| Right     | 46        | Crash   |

### Joystick → CC (Channel 1)

| Axis | CC Number | Range   |
|------|-----------|---------|
| X    | 1         | 0–127   |
| Y    | 2         | 0–127   |

---

## Keyboard fallback

If no controller is connected, the keyboard can be used instead:

| Key          | Action              |
|--------------|---------------------|
| A            | A button            |
| B            | B button            |
| Z            | Z button            |
| R            | R button            |
| L            | L button            |
| S            | Start               |
| U            | C-Up                |
| D            | C-Down              |
| Q            | C-Left              |
| E            | C-Right             |
| Arrow keys   | Joystick            |
| 1 / 2        | D-pad left / right  |
| 3 / 4        | D-pad up / down     |

---

## Visualizer controls

The 3D visualizer responds to the controller in real time:

| Input     | Effect                            |
|-----------|-----------------------------------|
| A         | Spin faster on X axis             |
| B         | Spin in reverse on X axis         |
| R         | Spin on Z axis                    |
| Z         | Spin in reverse on Z axis         |
| C-Up      | Spin on Y axis                    |
| C-Down    | Spin in reverse on Y axis         |
| C-Left    | Spin in reverse on Y axis         |
| C-Right   | Spin on Y axis                    |
| Start     | Stop all rotation                 |
| D-pad     | Flash a color (up/down/left/right each have a distinct hue) |
| Joystick  | Warp/wave distortion on the point cloud |

---

## Project structure

```
project/
├── main.py                        # Entry point and main loop
├── controllers/
│   ├── n64_controller.py          # N64 joystick input + MIDI output
│   └── keyboard_controller.py     # Keyboard fallback input
├── midi/
│   └── outport.py                 # MIDI message sending logic
└── windows/
    ├── display.py                 # Pygame controller display window
    └── visualizer.py             # GLFW + OpenGL 3D visualizer window
```

---

## Running the project

```bash
cd src
python main.py
```

Make sure your virtual MIDI port is running before launching.
