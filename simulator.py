# simulator.py
# this just pretends to be the pico so i can test the pc controller without the actual hardware.
# it sends a bunch of fake commands to the handle_cmd function we wrote earlier.

import time
from pc_controller import handle_cmd

print("starting simulator...")
print("open spotify and discord before running this.")
print("watch your volume mixer.")
time.sleep(2)

# list of fake inputs to send
fake_inputs = [
    "SPOTIFY_UP",
    "SPOTIFY_DOWN",
    "SPOTIFY_MUTE",
    "DISCORD_UP",
    "DISCORD_DOWN",
    "DISCORD_MUTE",
    "SYSTEM_UP",
    "SYSTEM_DOWN"
]

for cmd in fake_inputs:
    print(f"\nfaking hardware input: {cmd}")
    handle_cmd(cmd)
    # wait a bit so you can actually see the sliders move
    time.sleep(1.5)

print("\ndone. if the sliders moved, it works.")
