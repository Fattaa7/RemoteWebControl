import threading
import serverSetup
import lcd
import os

#select_folder = "liked"
SET = 1
NOT_SET = 0

DOWNLOADED_MODE = 7
CLOUD_MODE = 0


full_name_flag = NOT_SET #flag for future use
folder_index = 0
mode = CLOUD_MODE

downloaded_folder_name = ""
downloaded_songs_list = []
path_dir = "/home/pi/Desktop/RemoteWebControl/downloads"

def init():
    lcd.init()
    
def setFullNameFlag(value):
    global full_name_flag
    full_name_flag = value

def modeInit():
    lcd.lcdDisplay.lcd_clear()
    serverSetup.current_audio_index = 0
    serverSetup.getFolders()
    if len(serverSetup.folder_keys) == 0:
        lcd.lcdDisplay.lcd_display_string("Cloud Error!",1)
        lcd.lcdDisplay.lcd_display_string("Try Dwnlds",2)
    else:
        display_folderName(serverSetup.folder_keys[0])
    

def audio_start(select_folder, fldr_indx):
    global folder_index
    folder_index = fldr_indx
    serverSetup.folder_selected = select_folder
    serverSetup.init()
    play_current_audio(serverSetup.current_audio_index)
    autoNext()

def audio_start_downloaded():
    global downloaded_songs_list
    downloaded_songs_list = os.listdir(rf"{path_dir}/{downloaded_folder_name}")
    for i in downloaded_songs_list:
        print(i)
    play_current_audio_downloaded(downloaded_songs_list[0])
    autoNext()
    
def audio_stop():
    serverSetup.p.stop()

def play_current_audio_downloaded(song):
    print("reaching the play/downloading part")
    #media = serverSetup.vlc_instance.media_new_path(f"{path_dir}/{downloaded_folder_name}/{song}")
    print(f"{path_dir}/{downloaded_folder_name}/{song}")
    serverSetup.p.set_mrl(f"{path_dir}/{downloaded_folder_name}/{song}")
    serverSetup.p.play()
    display_SongName_Download(song)

# Function to play the current audio
def play_current_audio(index):
    if 0 <= index < len(serverSetup.object_keys):
        file_name = serverSetup.object_keys[index]
        folder_name = serverSetup.folder_selected
        key = f"{folder_name}/{file_name}"  # Adjust the 'Key' to include the folder path
        print(key)
        url = serverSetup.s3.generate_presigned_url('get_object', Params={'Bucket': serverSetup.aws_s3_bucket, 'Key': file_name})
        serverSetup.p.set_mrl(url, ':network-caching=1000')
        serverSetup.p.play()
        display_SongName(file_name,folder_name)
        
def previous_audio():
    if serverSetup.current_audio_index > 0:
        serverSetup.current_audio_index -= 1
        serverSetup.p.stop()
        if mode == DOWNLOADED_MODE:
            play_current_audio_downloaded(downloaded_songs_list[serverSetup.current_audio_index])
        else:
            play_current_audio(serverSetup.current_audio_index)
    elif serverSetup.current_audio_index == 0:
        serverSetup.p.stop()
        if mode == DOWNLOADED_MODE:
            serverSetup.current_audio_index = len(downloaded_songs_list) - 1
            print(serverSetup.current_audio_index)
            play_current_audio_downloaded(downloaded_songs_list[serverSetup.current_audio_index])
        else:
            serverSetup.current_audio_index = len(serverSetup.object_keys) - 1
            play_current_audio(serverSetup.current_audio_index)

# Function to play the next audio
def next_audio():
    if mode == DOWNLOADED_MODE:
        if serverSetup.current_audio_index < len(downloaded_songs_list) - 1:
            serverSetup.current_audio_index += 1
            serverSetup.p.stop()
            play_current_audio_downloaded(downloaded_songs_list[serverSetup.current_audio_index])
        elif serverSetup.current_audio_index == len(downloaded_songs_list) - 1:
            serverSetup.current_audio_index = 0
            serverSetup.p.stop()
            play_current_audio_downloaded(downloaded_songs_list[serverSetup.current_audio_index])
            
    elif mode == CLOUD_MODE:
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
    str1 = file_name[:16]
    lcd.lcdDisplay.lcd_display_string("Cloud Playlist: ", 1)
    lcd.lcdDisplay.lcd_display_string(str1, 2)

def display_download_folderName(filed_name):
    lcd.lcdDisplay.lcd_clear()
    #file_name = "Playlist: " + file_name
    str1 = filed_name[:16]
    lcd.lcdDisplay.lcd_display_string("DwnLded Plylist:", 1)
    lcd.lcdDisplay.lcd_display_string(str1, 2)

def display_SongName_Download(song):
    lcd.lcdDisplay.lcd_clear()
    str_value = song[:-4]  # Adjust the string to remove the folder prefix
    print(str_value)
    str1 = str_value[:16]
    lcd.lcdDisplay.lcd_display_string(str1, 1)
    str2 = str_value[16:32]
    #lcd.swapBacklight()
    if len(str2) > 0:
        if full_name_flag == SET:
            lcd.long_string(lcd.lcdDisplay,str2,2)
        elif full_name_flag == NOT_SET:
            lcd.lcdDisplay.lcd_display_string(str2,2)

#display song name without the folder name in the beginning and without the ".mp3" in the end
def display_SongName(file_name, folder_name):
    lcd.lcdDisplay.lcd_clear()
    str_value = file_name[len(folder_name) + 1:-4]  # Adjust the string to remove the folder prefix
    print(str_value)
    str1 = str_value[:16]
    lcd.lcdDisplay.lcd_display_string(str1, 1)
    str2 = str_value[16:32]
    if len(str2) > 0:
        if full_name_flag == SET:
            lcd.long_string(lcd.lcdDisplay,str2,2)
        elif full_name_flag == NOT_SET:
            lcd.lcdDisplay.lcd_display_string(str2,2)

