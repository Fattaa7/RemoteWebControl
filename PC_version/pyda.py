import boto3
import vlc
import time
import keyboard
import audioFuncs
import serverSetup
import audioFuncs
import urllib
import socket

def get_ip_address():
    try:
        # Get the hostname
        host_name = socket.gethostname()
        # Get the IP address corresponding to the hostname
        ip_address = socket.gethostbyname(host_name)
        return ip_address
    except Exception as e:
        print(f"Error: {e}")
        return "Not Found"

# Call the function
ip_address = get_ip_address()
print(f"The IP address of the Raspberry Pi is: {ip_address}")


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



