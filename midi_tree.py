
"""
Requirements:
    pip install python-rtmidi serial numpy
Run like:
    python midi_tree.py
"""

import math
import numpy as np
import time
from matplotlib import pyplot as plt
import rtmidi
from rtmidi import midiutil
from ledcontroller import LEDController


def generate_color_map(N):
    arr = np.arange(N)/N
    N_up = int(math.ceil(N/7)*7)
    arr.resize(N_up)
    arr = arr.reshape(7, N_up//7).T.reshape(-1)
    ret = plt.cm.hsv(arr)
    n = ret[:, 3].size
    a = n//2
    b = n-a
    for i in range(3):
        ret[0:n//2, i] *= np.arange(0.2, 1, 0.8/a)
    ret[n//2:, 3] *= np.arange(1, 0.1, -0.9/b)
#     print(ret)
    return ret


class MidiHandler(object):
    """Docstring for MidiHandler """

    def __init__(self):
        """@todo: to be defined """
        self.colors = generate_color_map(128)
        self.list = []
        self.fader_value = 127
        self.notes = np.zeros((60, 3), dtype=np.uint8)
        self.ledcontroller = LEDController(60, port="/dev/led_tree")
        self.ledcontroller.all_off()
        self.mode = "COLOR"

#    def set_color_by_note(self, note):

    def __call__(self, event, data=None):
        event, deltatime = event
        command = event[0]
        note = event[1]

        note = note % len(self.notes)
        velocity = event[2] #  [0 ... 127]
        if command == 176:
            self.fader_value = velocity
        if command == 144:
            print("note pressed")
            #  print(event, self.colors[note], velocity, deltatime)
            self.list.append({"time": deltatime, "event": event})
            self.notes[:, 0] = min(np.uint8(self.colors[note][0] * self.fader_value * 2), 254)
            self.notes[:, 1] = min(np.uint8(self.colors[note][1] * self.fader_value * 2), 254)
            self.notes[:, 2] = min(np.uint8(self.colors[note][2] * self.fader_value * 2), 254)
                #self.set_color_by_note()

            print(self.notes[note])
        if command == 128:
            print("note off")
            self.notes[:, 0] = 0
            self.notes[:, 1] = 0
            self.notes[:, 2] = 0

        if command == 128 or command == 144:
            self.ledcontroller.set_config(self.notes)


midi_in = rtmidi.MidiIn()
midiutil.list_input_ports()

midiin, port = midiutil.open_midiinput()

midihandler = MidiHandler()
midiin.set_callback(midihandler)

try:
    while True:
        time.sleep(1.0)

except KeyboardInterrupt:
    print()
finally:
    midiin.close_port()
    print(midihandler.list)
