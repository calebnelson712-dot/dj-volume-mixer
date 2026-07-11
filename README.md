# DJ Volume Mixer

a physical volume mixer with 4 rotary knobs to control individual app volumes on windows. each knob controls a different app (spotify, discord, system volume) and you can press the knob down to mute it.

## what it does

- **knob 1:** spotify volume control
- **knob 2:** discord volume control  
- **knob 3:** system/master volume
- **knob 4:** tbd (haven't decided yet)

## how it works

the project has two parts:

1. **pc_controller.py** - a python script that runs on your pc and hooks into the windows audio api using pycaw to change app volumes

2. **pico_controller.py** - circuitpython code for the raspberry pi pico that reads the rotary encoders and sends commands over usb serial to the pc

## files

- `pc_controller.py` - the main pc controller (tested and working)
- `pico_controller.py` - the hardware code for the raspberry pi pico
- `simulator.py` - a test script that fakes hardware inputs so you can test without the actual hardware

## how to run it

**requirements:**
- python 3.x
- pycaw (`pip install pycaw`)

**to test the pc controller:**
```bash
python pc_controller.py
