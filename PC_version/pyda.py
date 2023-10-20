import boto3
import vlc
import time
import keyboard
import audioFuncs
import serverSetup
import audioFuncs
import urllib
import socket
import os

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

current_directory = os.getcwd()
folderName = "output"

folder_path = os.path.join(current_directory, folderName)

filed = os.listdir(folder_path)

for file in filed:
    print(file)
    

vlc_instance = vlc.Instance()
media = vlc_instance.media_new_path(f'{folder_path}/{filed[5]}')  # Replace 'path_to_your_mp3_file.mp3' with the actual path to your MP3 file
serverSetup.p.set_media(media)

serverSetup.p.play()
# serverSetup.init()

# serverSetup.downloadPlaylist()

# # Define keypress actions
# keyboard.add_hotkey('1', lambda: audioFuncs.previous_audio(), suppress=True)
# keyboard.add_hotkey('2', lambda: audioFuncs.next_audio(), suppress=True)
# keyboard.add_hotkey('3', lambda: audioFuncs.pause_audio(), suppress=True)
# keyboard.add_hotkey('5', lambda: audioFuncs.forward(), suppress=True)
# keyboard.add_hotkey('4', lambda: audioFuncs.backward(), suppress=True)



# audioFuncs.play_current_audio(serverSetup.current_audio_index)


# # Event loop to keep the script running2
while True:
 #   audioFuncs.autoNext()
    continue



