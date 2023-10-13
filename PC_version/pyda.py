import boto3
import vlc
import time
import keyboard
import audioFuncs
import serverSetup
import audioFuncs




# Define keypress actions
keyboard.add_hotkey('1', lambda: audioFuncs.previous_audio(), suppress=True)
keyboard.add_hotkey('2', lambda: audioFuncs.next_audio(), suppress=True)
keyboard.add_hotkey('3', lambda: audioFuncs.pause_audio(), suppress=True)
keyboard.add_hotkey('5', lambda: audioFuncs.forward(), suppress=True)
keyboard.add_hotkey('4', lambda: audioFuncs.backward(), suppress=True)



audioFuncs.play_current_audio(serverSetup.current_audio_index)


# Event loop to keep the script running2
while True:
    audioFuncs.autoNext()



