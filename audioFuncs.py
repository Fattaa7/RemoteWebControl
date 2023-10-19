import threading
import time
import serverSetup
import lcd
from time import sleep
import os

#select_folder = "liked"
SET = 1
NOT_SET = 0
full_name_flag = NOT_SET
folder_index = 0

def init():
    lcd.init()
    
def setFullNameFlag(value):
    global full_name_flag
    full_name_flag = value

def modeInit():
    serverSetup.current_audio_index = 0
    serverSetup.getFolders()
    display_folderName(serverSetup.folder_keys[0])
    


def audio_start(select_folder, fldr_indx):
    global folder_index
    folder_index = fldr_indx
    serverSetup.folder_selected = select_folder
    serverSetup.init()
    play_current_audio(serverSetup.current_audio_index)
    autoNext()

def audio_stop():
    serverSetup.p.stop()


# Function to play the current audio
def play_current_audio(index):
    if 0 <= index < len(serverSetup.object_keys):
        file_name = serverSetup.object_keys[index]
        folder_name = serverSetup.folder_selected
        key = f"{folder_name}/{file_name}"  # Adjust the 'Key' to include the folder path
        # with open('output.txt', 'w') as f:
            # f.write(str(folder_index) + '\n')  # Writing folder_name on the first line
            # f.write(str(serverSetup.current_audio_index))
        print(key)
        url = serverSetup.s3.generate_presigned_url('get_object', Params={'Bucket': serverSetup.aws_s3_bucket, 'Key': file_name})
        serverSetup.p.set_mrl(url, ':network-caching=1000')
        serverSetup.p.play()
        display_SongName(file_name,folder_name)
        



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
    # place a flag here to check on the loop option
    if not serverSetup.p.is_playing():
        if serverSetup.p.get_position() > 0.98:
            #Add check if loop is enabled
            #if no then next audio
            #if yes then play current audio again
            next_audio()
    threading.Timer(1, autoNext).start()
        
    


#display folder name without the '/' in the end of the name
def display_folderName(filed_name):
    lcd.lcdDisplay.lcd_clear()
    file_name = filed_name[:-1]
    #file_name = "Playlist: " + file_name
    str1 = file_name[:16]
    lcd.lcdDisplay.lcd_display_string("Playlist: ", 1)
    lcd.lcdDisplay.lcd_display_string(str1, 2)
    # str2 = file_name[16:]
    # if len(str2) > 0:
    #     lcd.long_string(lcd.lcdDisplay,str2,2)


#display song name without the folder name in the beginning and without the ".mp3" in the end
def display_SongName(file_name, folder_name):
    lcd.lcdDisplay.lcd_clear()
    str_value = file_name[len(folder_name) + 1:-4]  # Adjust the string to remove the folder prefix
    print(str_value)
    str1 = str_value[:16]
    lcd.lcdDisplay.lcd_display_string(str1, 1)
    str2 = str_value[16:]
    #lcd.swapBacklight()
    if len(str2) > 0:
        if full_name_flag == SET:
            lcd.long_string(lcd.lcdDisplay,str2,2)
        elif full_name_flag == NOT_SET:
            lcd.lcdDisplay.lcd_display_string(str2,2)

