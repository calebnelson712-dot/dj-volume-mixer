# circuitpython code for the raspberry pi pico
# this reads the 4 knobs and sends the commands to the pc over usb

import board
import digitalio
import time
import usb_cdc

# pin setup for my 4 knobs
# format: data pin, clock pin, button pin, name
KNOBS = [
    {"dt": board.GP2, "clk": board.GP3, "btn": board.GP4, "name": "SPOTIFY"},
    {"dt": board.GP6, "clk": board.GP7, "btn": board.GP8, "name": "DISCORD"},
    {"dt": board.GP10, "clk": board.GP11, "btn": board.GP12, "name": "SYSTEM"},
    {"dt": board.GP14, "clk": board.GP15, "btn": board.GP16, "name": "TBD"}
]

class Knob:
    def __init__(self, dt_pin, clk_pin, btn_pin):
        # setup the rotation pins
        self.dt = digitalio.DigitalInOut(dt_pin)
        self.clk = digitalio.DigitalInOut(clk_pin)
        self.dt.direction = digitalio.Direction.INPUT
        self.clk.direction = digitalio.Direction.INPUT
        
        # setup the button pin (when you press the knob down)
        self.btn = digitalio.DigitalInOut(btn_pin)
        self.btn.direction = digitalio.Direction.INPUT
        self.btn.pull = digitalio.Pull.UP  # button is active low
        
        self.last_dt = self.dt.value
        self.last_btn = self.btn.value
        self.btn_pressed = False
    
    def get_rotation(self):
        current_dt = self.dt.value
        if current_dt != self.last_dt:
            if self.clk.value != current_dt:
                self.last_dt = current_dt
                return "UP"
            else:
                self.last_dt = current_dt
                return "DOWN"
        return None
    
    def check_button(self):
        current_btn = self.btn.value
        if current_btn == 0 and self.last_btn == 1:
            self.btn_pressed = True
        elif current_btn == 1 and self.last_btn == 0 and self.btn_pressed:
            self.btn_pressed = False
            self.last_btn = current_btn
            return True
        self.last_btn = current_btn
        return False

# create the knob objects
my_knobs = [Knob(k["dt"], k["clk"], k["btn"]) for k in KNOBS]

# wait for usb serial to connect to the pc
print("waiting for usb connection...")
while not usb_cdc.data.connected:
    time.sleep(0.1)
print("usb connected! sending commands.")

last_btn_check = 0

# main loop
while True:
    for i, knob in enumerate(my_knobs):
        name = KNOBS[i]["name"]
        
        # check if knob turned
        direction = knob.get_rotation()
        if direction:
            msg = f"{name}_{direction}\n"
            try:
                usb_cdc.data.write(msg.encode())
            except:
                pass
        
        # check if button pressed (only check every 50ms so it doesnt spam check and overload the usb)
        now = time.monotonic()
        if now - last_btn_check > 0.05:
            if knob.check_button():
                msg = f"{name}_MUTE\n"
                try:
                    usb_cdc.data.write(msg.encode())
                except:
                    pass
            last_btn_check = now
    
    time.sleep(0.01)



