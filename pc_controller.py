# my dj volume mixer pc controller
# i made this so i can control spotify, discord, and my pc volume with physical knobs later.

import time
import subprocess
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

# app names to look for in windows
SPOTIFY_APP = "Spotify.exe"
DISCORD_APP = "Discord.exe"
STEP = 0.05 # i want it to change by 5% each time i turn the knob

# changes volume for a specific app like spotify or discord
def change_vol(app, amount):
    sessions = AudioUtilities.GetAllSessions()
    for s in sessions:
        if s.Process and s.Process.name().lower() == app.lower():
            vol = s._ctl.QueryInterface(ISimpleAudioVolume)
            curr = vol.GetMasterVolume()
            new_vol = max(0.0, min(1.0, curr + amount))
            vol.SetMasterVolume(new_vol, None)
            print(f"changed {app} to {int(new_vol * 100)}%")
            return
    print(f"couldnt find {app}. make sure its open and making sound.")

# changes system volume by simulating keyboard presses (this actually works)
def change_sys_vol(amount):
    try:
        if amount > 0:
            # simulate pressing volume up key
            subprocess.run(["powershell", "-Command", "(New-Object -ComObject WScript.Shell).SendKeys([char]175)"], 
                         shell=False, capture_output=True, timeout=1)
        else:
            # simulate pressing volume down key
            subprocess.run(["powershell", "-Command", "(New-Object -ComObject WScript.Shell).SendKeys([char]174)"], 
                         shell=False, capture_output=True, timeout=1)
        print("adjusted system volume")
    except Exception as e:
        print(f"system vol error: {e}")

# mutes the whole pc using keyboard simulation
def mute_sys():
    try:
        # simulate pressing mute key
        subprocess.run(["powershell", "-Command", "(New-Object -ComObject WScript.Shell).SendKeys([char]173)"], 
                     shell=False, capture_output=True, timeout=1)
        print("toggled system mute")
    except Exception as e:
        print(f"system mute error: {e}")

# mutes or unmutes a specific app
def mute_app(app):
    sessions = AudioUtilities.GetAllSessions()
    for s in sessions:
        if s.Process and s.Process.name().lower() == app.lower():
            vol = s._ctl.QueryInterface(ISimpleAudioVolume)
            is_muted = vol.GetMute()
            vol.SetMute(not is_muted, None)
            if not is_muted:
                print(f"muted {app}")
            else:
                print(f"unmuted {app}")
            return
    print(f"couldnt find {app} to mute.")

# this is where i route the commands from my future hardware to the right function
def handle_cmd(cmd):
    if cmd == "SPOTIFY_UP":
        change_vol(SPOTIFY_APP, STEP)
    elif cmd == "SPOTIFY_DOWN":
        change_vol(SPOTIFY_APP, -STEP)
    elif cmd == "SPOTIFY_MUTE":
        mute_app(SPOTIFY_APP)
        
    elif cmd == "DISCORD_UP":
        change_vol(DISCORD_APP, STEP)
    elif cmd == "DISCORD_DOWN":
        change_vol(DISCORD_APP, -STEP)
    elif cmd == "DISCORD_MUTE":
        mute_app(DISCORD_APP)
        
    elif cmd == "SYSTEM_UP":
        change_sys_vol(STEP)
    elif cmd == "SYSTEM_DOWN":
        change_sys_vol(-STEP)
    elif cmd == "SYSTEM_MUTE":
        mute_sys()
        
    # i havent decided what dial 4 will do yet
    elif cmd in ["TBD_UP", "TBD_DOWN", "TBD_MUTE"]:
        print("dial 4 is TBD, i'll figure it out later.")
        
    else:
        print(f"idk what {cmd} is.")
        print("try: SPOTIFY_UP, DISCORD_MUTE, SYSTEM_DOWN, etc.")

# main loop to listen for my commands
if __name__ == "__main__":
    print("starting my dj volume mixer controller...")
    print("dial 1: spotify | dial 2: discord | dial 3: system | dial 4: tbd")
    print("type a command to test it out. ctrl+c to quit.")
    
    try:
        while True:
            cmd = input("\nenter command: ").strip().upper()
            if cmd:
                handle_cmd(cmd)
    except KeyboardInterrupt:
        print("\nstopping the mixer.")
    except Exception as e:
        print(f"\nweird error: {e}")
    