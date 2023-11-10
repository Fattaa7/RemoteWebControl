import RPi.GPIO as GPIO
import audioFuncs
#import padkeydriver
import lcd
from datetime import datetime
from subprocess import check_output
import serverSetup
import time
import os
import random
import playlistCreator
import shlex

MODE_MODE = 0
AUDIO_MODE = 5
DOWNLOADED_AUDIO_MODE = 10
LAST_PLAYED_MODE = 9
DEV_MODE = 22
CREATE_PLAYLIST_MODE = 54
CREATED_MODE = 99
CREATED_AUDIO_MODE = 77
TO_COPY_TO_MODE = 44

NEXT_GPIO = 21
PAUSE_GPIO = 20
PREVIOUS_GPIO = 16
EXIT_GPIO = 19
LCD_GPIO = 18

TOGGLE_GPIO = 17

flag = DEV_MODE


folder_index = 0
download_folders = []
button_pressed_time = None

playlist_name_create = ""
current_character = ''
current_song = None
current_folder = None

def Toggle_swtich(channel):
    
        if flag == CREATE_PLAYLIST_MODE:
            global current_character
            if current_character == '':
                return
        
            if GPIO.input(TOGGLE_GPIO) == GPIO.LOW:
                time.sleep(0.2)
                if GPIO.input(TOGGLE_GPIO) == GPIO.LOW:
                    current_character = current_character.lower()
                    createPlaylist_mode()
            elif GPIO.input(TOGGLE_GPIO) == GPIO.HIGH:
                time.sleep(0.2)
                if GPIO.input(TOGGLE_GPIO) == GPIO.HIGH:
                    current_character = current_character.upper()
                    createPlaylist_mode()
        else:    
            if GPIO.input(TOGGLE_GPIO) == GPIO.LOW:
                serverSetup.p.audio_set_volume(50)
            elif GPIO.input(TOGGLE_GPIO) == GPIO.HIGH:
                serverSetup.p.audio_set_volume(96)

def nextBtn(channel):
    global button_pressed_time
    global current_character
    global playlist_name_create
    if GPIO.input(channel) == GPIO.LOW:
        time.sleep(0.1)
        if GPIO.input(channel) == GPIO.LOW:
            button_pressed_time = time.time()  # Record the start time of the button press
            global flag       
            global folder_index
            print("clicked next")

            if flag == MODE_MODE:
                if folder_index < len(serverSetup.folder_keys) - 1:
                    folder_index += 1
                    audioFuncs.display_folderName(serverSetup.folder_keys[folder_index])
                elif folder_index == len(serverSetup.folder_keys) -1:
                    folder_index = 0
                    audioFuncs.display_folderName(serverSetup.folder_keys[folder_index])
                    
            elif flag == AUDIO_MODE:
                while GPIO.input(channel) == GPIO.LOW and time.time() - button_pressed_time <= 0.4:
                    pass  # Wait until the button is released or 0.5 seconds has passed
                if time.time() - button_pressed_time > 0.4:
                    audioFuncs.next_audio()  # Execute the function if pressed for 0.5 seconds or more
                else:
                    audioFuncs.forward()  # Execute the function if pressed less than 0.5 seconds
            
            elif flag == DOWNLOADED_AUDIO_MODE:
                while GPIO.input(channel) == GPIO.LOW and time.time() - button_pressed_time <= 0.4:
                    pass  # Wait until the button is released or 0.5 seconds has passed
                if time.time() - button_pressed_time > 0.4:
                    audioFuncs.next_audio()  # Execute the function if pressed for 0.5 seconds or more
                else:
                    audioFuncs.forward()  # Execute the function if pressed less than 0.5 seconds
                    
            
            elif flag == CREATED_AUDIO_MODE:
                while GPIO.input(channel) == GPIO.LOW and time.time() - button_pressed_time <= 0.4:
                    pass  # Wait until the button is released or 0.5 seconds has passed
                if time.time() - button_pressed_time > 0.4:
                    audioFuncs.next_audio()  # Execute the function if pressed for 0.5 seconds or more
                else:
                    audioFuncs.forward()  # Execute the function if pressed less than 0.5 seconds
                    
            elif flag == DEV_MODE:
                if folder_index < len(download_folders) - 1:
                    folder_index += 1
                    audioFuncs.display_download_folderName(download_folders[folder_index])
                elif folder_index == len(download_folders) - 1:
                    folder_index = 0
                    audioFuncs.display_download_folderName(download_folders[folder_index])
                    
            elif flag == TO_COPY_TO_MODE:
                if folder_index < len(download_folders) - 1:
                    folder_index += 1
                    audioFuncs.display_created_folderName(download_folders[folder_index])
                elif folder_index == len(download_folders) - 1:
                    folder_index = 0
                    audioFuncs.display_created_folderName(download_folders[folder_index])

            
            elif flag == CREATED_MODE:
                if folder_index < len(download_folders) - 1:
                    folder_index += 1
                    audioFuncs.display_created_folderName(download_folders[folder_index])
                elif folder_index == len(download_folders) - 1:
                    folder_index = 0
                    audioFuncs.display_created_folderName(download_folders[folder_index])

            elif flag == CREATE_PLAYLIST_MODE:
                if GPIO.input(TOGGLE_GPIO) == GPIO.LOW:
                    current_character = playlistCreator.incrementAlphaSmall(current_character)
                elif GPIO.input(TOGGLE_GPIO) == GPIO.HIGH:
                    current_character = playlistCreator.incrementAlphaCapital(current_character)
                createPlaylist_mode()



def prevBtn(channel):
    global button_pressed_time
    global current_character
    global playlist_name_create
    if GPIO.input(channel) == GPIO.LOW:
        time.sleep(0.1)
        if GPIO.input(channel) == GPIO.LOW:
            button_pressed_time = time.time()  # Record the start time of the button press
            global flag       
            global folder_index
            
            print("clicked prev")
            if flag == MODE_MODE:
                if folder_index > 0:
                    folder_index -= 1
                    audioFuncs.display_folderName(serverSetup.folder_keys[folder_index])
                elif folder_index == 0:
                    folder_index = len(serverSetup.folder_keys) -1
                    audioFuncs.display_folderName(serverSetup.folder_keys[folder_index])

            elif flag == AUDIO_MODE:
                print("REACHERRRRR PREV BTN")
                # Implement the logic for long press
                while GPIO.input(channel) == GPIO.LOW and time.time() - button_pressed_time <= 0.4:
                    pass  # Wait until the button is released or 0.5 seconds has passed
                if time.time() - button_pressed_time > 0.4:
                    audioFuncs.previous_audio()  # Execute the function if pressed for 0.5 seconds or more
                else:
                    audioFuncs.backward()  # Execute the function if pressed less than 0.5 seconds

                
            elif flag == DOWNLOADED_AUDIO_MODE:
                print("PREVIOUS FROM DOWNLOAD")
                # Implement the logic for long press
                while GPIO.input(channel) == GPIO.LOW and time.time() - button_pressed_time <= 0.4:
                    pass  # Wait until the button is released or 0.5 seconds has passed
                if time.time() - button_pressed_time > 0.4:
                    audioFuncs.previous_audio()  # Execute the function if pressed for 0.5 seconds or more
                else:
                    audioFuncs.backward()  # Execute the function if pressed less than 0.5 seconds

            elif flag == CREATED_AUDIO_MODE:
                print("PREVIOUS FROM DOWNLOAD")
                # Implement the logic for long press
                while GPIO.input(channel) == GPIO.LOW and time.time() - button_pressed_time <= 0.4:
                    pass  # Wait until the button is released or 0.5 seconds has passed
                if time.time() - button_pressed_time > 0.4:
                    audioFuncs.previous_audio()  # Execute the function if pressed for 0.5 seconds or more
                else:
                    audioFuncs.backward()  # Execute the function if pressed less than 0.5 seconds


            elif flag == DEV_MODE:
                print("REACHER PREV BTN")
                if folder_index > 0:
                    folder_index -= 1
                    audioFuncs.display_download_folderName(download_folders[folder_index])
                elif folder_index == 0:
                    folder_index = len(download_folders) - 1
                    audioFuncs.display_download_folderName(download_folders[folder_index])
                    
            elif flag == TO_COPY_TO_MODE:
                if folder_index > 0:
                    folder_index -= 1
                    audioFuncs.display_created_folderName(download_folders[folder_index])
                elif folder_index == 0:
                    folder_index = len(download_folders) - 1
                    audioFuncs.display_created_folderName(download_folders[folder_index])


            elif flag == CREATED_MODE:
                print("REACHER PREV BTN")
                if folder_index > 0:
                    folder_index -= 1
                    audioFuncs.display_created_folderName(download_folders[folder_index])
                elif folder_index == 0:
                    folder_index = len(download_folders) - 1
                    audioFuncs.display_created_folderName(download_folders[folder_index])
                    
            elif flag == CREATE_PLAYLIST_MODE:
                if GPIO.input(TOGGLE_GPIO) == GPIO.LOW:
                    current_character = playlistCreator.decrementAlphaSmall(current_character)
                elif GPIO.input(TOGGLE_GPIO) == GPIO.HIGH:
                    current_character = playlistCreator.decrementAlphaCapital(current_character)
                createPlaylist_mode()



def pauseBtn(channel):
    global button_pressed_time
    global current_character
    global playlist_name_create
    global current_song
    global current_folder
    if GPIO.input(channel) == GPIO.LOW:
        global flag       
        global folder_index
        if flag == AUDIO_MODE:
            if GPIO.input(LCD_GPIO) == GPIO.LOW:
                serverSetup.downloadPlaylist()
                
        elif flag == DOWNLOADED_AUDIO_MODE:
            if GPIO.input(LCD_GPIO) == GPIO.LOW:
                os.system(f"rm -r downloads/{download_folders[folder_index]}")
                print(f"Deleted {download_folders[folder_index]}")
                flag = DEV_MODE
                DevMode()
                
        elif flag == CREATED_AUDIO_MODE:
            if GPIO.input(LCD_GPIO) == GPIO.LOW:
                current_song = audioFuncs.downloaded_songs_list[serverSetup.current_audio_index]
                current_folder = download_folders[folder_index]
                os.system(f"rm -r created/{shlex.quote(current_folder)}/{shlex.quote(current_song)}")
                print(f"rm -r created/{shlex.quote(current_folder)}/{shlex.quote(current_song)}")
                flag = CREATED_MODE
                created_mode()

        time.sleep(0.1)
        if GPIO.input(channel) == GPIO.LOW:
            print("clicked pause")
            if flag == MODE_MODE:
                flag = AUDIO_MODE
                audioFuncs.mode = audioFuncs.CLOUD_MODE
                audioFuncs.audio_start(serverSetup.folder_keys[folder_index][:-1],folder_index)
                
            elif flag == AUDIO_MODE:
                audioFuncs.pause_audio()
                
            elif flag == DOWNLOADED_AUDIO_MODE:
                button_pressed_time = time.time()
                while GPIO.input(channel) == GPIO.LOW and time.time() - button_pressed_time <= 0.6:
                    pass  # Wait until the button is released or 0.5 seconds has passed
                if time.time() - button_pressed_time > 0.6:
                    current_song = audioFuncs.downloaded_songs_list[serverSetup.current_audio_index]
                    current_folder = download_folders[folder_index]
                    flag = TO_COPY_TO_MODE  # Execute the function if pressed for 0.5 seconds or more
                    lcd.lcdDisplay.lcd_clear()
                    created_mode()
                else:
                    audioFuncs.pause_audio()

            elif flag == TO_COPY_TO_MODE:
                cmd = (
                    f"cp downloads/{shlex.quote(current_folder)}/{shlex.quote(current_song)} "
                    f"created/{download_folders[folder_index]}")
                print(cmd)
                os.system(cmd)
                flag = DEV_MODE
                DevMode()
                
            elif flag == CREATED_AUDIO_MODE:
                audioFuncs.pause_audio()

            
            elif flag == DEV_MODE:
                button_pressed_time = time.time()  # Record the start time of the button press
                
                
                flag = DOWNLOADED_AUDIO_MODE
                audioFuncs.mode = audioFuncs.DOWNLOADED_MODE
                audioFuncs.downloaded_folder_name = download_folders[folder_index]
                audioFuncs.audio_start_downloaded()
            
            elif flag == CREATED_MODE:
                button_pressed_time = time.time()  # Record the start time of the button press
                if GPIO.input(LCD_GPIO) == GPIO.LOW:

                    current_folder = download_folders[folder_index]
                    os.system(f"rm -r created/{shlex.quote(current_folder)}")
                    print(f"rm -r created/{shlex.quote(current_folder)}/")
                    flag = CREATED_MODE
                    created_mode()

                else:

                    flag = CREATED_AUDIO_MODE
                    audioFuncs.mode = audioFuncs.CREATED_MODE
                    audioFuncs.downloaded_folder_name = download_folders[folder_index]
                    audioFuncs.audio_start_created()

            
            elif flag == CREATE_PLAYLIST_MODE:
                if current_character == '':
                    if playlist_name_create == "":
                        flag = DEV_MODE
                        DevMode()
                        return
                    dir = rf"/home/pi/Desktop/RemoteWebControl/created/{playlist_name_create}"
                    isExist = os.path.exists(dir)
                    if isExist:
                        print("folder exists")
                    else:
                        os.mkdir(dir)
                    playlist_name_create = ""
                    flag = DEV_MODE
                    DevMode()
                else:
                    playlist_name_create = playlist_name_create + current_character
                    current_character = ''
                    createPlaylist_mode()

def exitBtn(channel):
    global button_pressed_time
    global playlist_name_create
    if GPIO.input(channel) == GPIO.LOW:
        time.sleep(0.1)
        if GPIO.input(channel) == GPIO.LOW:
            global flag       
            global folder_index
            print("clicked exit")       

            if flag == MODE_MODE:
                flag = CREATED_MODE
                created_mode()
                
            elif flag == DEV_MODE:
                button_pressed_time = time.time()
                while GPIO.input(channel) == GPIO.LOW and time.time() - button_pressed_time <= 0.8:
                    pass  # Wait until the button is released or 0.5 seconds has passed
                if time.time() - button_pressed_time > 0.8:
                    flag = CREATE_PLAYLIST_MODE  # Execute the function if pressed for 0.5 seconds or more
                    lcd.lcdDisplay.lcd_clear()
                    createPlaylist_mode()
                else:
                    flag = MODE_MODE
                    mode_mode()
                    # Execute the function if pressed less than 0.5 seconds
                    
            elif flag == CREATED_MODE:
                button_pressed_time = time.time()
                while GPIO.input(channel) == GPIO.LOW and time.time() - button_pressed_time <= 0.8:
                    pass  # Wait until the button is released or 0.5 seconds has passed
                if time.time() - button_pressed_time > 0.8:
                    flag = CREATE_PLAYLIST_MODE  # Execute the function if pressed for 0.5 seconds or more
                    lcd.lcdDisplay.lcd_clear()
                    createPlaylist_mode()
                else:
                    flag = DEV_MODE
                    DevMode()
                    # Execute the function if pressed less than 0.5 seconds

            elif flag == CREATE_PLAYLIST_MODE:
                lcd.lcdDisplay.lcd_clear()
                playlist_name_create = ""
                flag = DEV_MODE
                DevMode()

            elif flag == CREATED_AUDIO_MODE:
                flag = CREATED_MODE
                created_mode()

            elif flag == AUDIO_MODE:
                flag = MODE_MODE
                mode_mode()
            elif flag == DOWNLOADED_AUDIO_MODE:
                flag = DEV_MODE
                DevMode()            

def lcdBtn(channel):
   if GPIO.input(channel) == GPIO.LOW:
        time.sleep(0.1)
        if GPIO.input(channel) == GPIO.LOW:
            global flag       
            global folder_index
            print("clicked lcd")       
            lcd.swapBacklight()

################## Modes - Screens #######################

def DevMode():
    # lcd.init()
    # lcd.lcdDisplay.lcd_display_string("IP Address is:",1)
    # lcd.lcdDisplay.lcd_display_string("" + str(IP),2)
    global download_folders
    global folder_index
    audioFuncs.audio_stop()
    folder_index = 0
    download_folders = os.listdir(r"/home/pi/Desktop/RemoteWebControl/downloads/")
    if len(download_folders) == 0:
        lcd.lcdDisplay.lcd_clear()
        lcd.lcdDisplay.lcd_display_string("EMPTY!",2)
        return
    for file in download_folders:
        print(file)
    audioFuncs.display_download_folderName(download_folders[0])


def mode_mode():
    audioFuncs.audio_stop()
    audioFuncs.modeInit()

def createPlaylist_mode():
    global playlist_name_create
    global current_character
    lcd.lcdDisplay.lcd_display_string("Create Playlist:",1)
    lcd.lcdDisplay.lcd_display_string(playlist_name_create + current_character,2)

def created_mode():
    global download_folders
    global folder_index
    audioFuncs.audio_stop()
    folder_index = 0
    download_folders = os.listdir(r"/home/pi/Desktop/RemoteWebControl/created/")
    if len(download_folders) == 0:
        lcd.lcdDisplay.lcd_clear()
        lcd.lcdDisplay.lcd_display_string("EMPTY!",2)
        return
    for file in download_folders:
        print(file)
    audioFuncs.display_created_folderName(download_folders[0])


# def to_copy_to_mode():
#     global download_folders
#     global folder_index


################## Program Start ##########################

GPIO.setmode(GPIO.BCM)
GPIO.setup(TOGGLE_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(NEXT_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PAUSE_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PREVIOUS_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(EXIT_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LCD_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)





Toggle_swtich(None)
audioFuncs.init()
DevMode()

GPIO.add_event_detect(NEXT_GPIO, GPIO.FALLING, callback=nextBtn)
GPIO.add_event_detect(PREVIOUS_GPIO, GPIO.FALLING, callback=prevBtn)
GPIO.add_event_detect(PAUSE_GPIO, GPIO.FALLING, callback=pauseBtn)
GPIO.add_event_detect(EXIT_GPIO, GPIO.FALLING, callback=exitBtn)
GPIO.add_event_detect(TOGGLE_GPIO, GPIO.FALLING, callback=Toggle_swtich)
GPIO.add_event_detect(LCD_GPIO, GPIO.FALLING, callback=lcdBtn)


# if GPIO.input(TOGGLE_GPIO) == GPIO.LOW:
    # print("THIS IS LOW")
    # lcd.setBacklight(0)



while True:

    if flag != CREATE_PLAYLIST_MODE:
        Toggle_swtich(None)
    time.sleep(2)