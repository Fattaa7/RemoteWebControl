import boto3
import vlc
import time
import keyboard
import threading
import serverSetup

def audio_thread_function():
    play_current_audio(serverSetup.current_audio_index)

# Function to play the current audio
def play_current_audio(index):
    if 0 <= index < len(serverSetup.object_keys):
        url = serverSetup.s3.generate_presigned_url('get_object', Params={'Bucket': serverSetup.aws_s3_bucket, 'Key': serverSetup.object_keys[index]})
        serverSetup.p.set_mrl(url)
        serverSetup.p.play()
        str = serverSetup.object_keys[index][:16]
        str2 = serverSetup.object_keys[index][16:]
        print(str)
        print(str2)


def previous_audio():
    if serverSetup.current_audio_index > 0:
        serverSetup.current_audio_index -= 1
        serverSetup.p.stop()
        play_current_audio(serverSetup.current_audio_index)
    elif serverSetup.current_audio_index == 0:
        serverSetup.current_audio_index = len(serverSetup.object_keys) - 1
        serverSetup.p.stop()
        play_current_audio(serverSetup.current_audio_index)


# Function to play the next audio
def next_audio():
    if serverSetup.current_audio_index < len(serverSetup.object_keys) - 1:
        serverSetup.current_audio_index += 1
        serverSetup.p.stop()
        play_current_audio(serverSetup.current_audio_index)
    elif serverSetup.current_audio_index == len(serverSetup.object_keys) -1:
        serverSetup.current_audio_index = 0
        serverSetup.p.stop()
        play_current_audio(serverSetup.current_audio_index)



# Function to pause or resume playback
def pause_audio():
    if serverSetup.p.is_playing() == 1:
        serverSetup.p.pause()
        print("Paused")
    else:
        serverSetup.p.play()
        print("Resumed")

def forward():
    serverSetup.p.set_position(serverSetup.p.get_position() + 0.03)


def backward():
    serverSetup.p.set_position(serverSetup.p.get_position() - 0.03)

def autoNext():
    time.sleep(1)
    if not serverSetup.p.is_playing():
        if serverSetup.p.get_position() > 0.98:
            next_audio()

