import RPi.GPIO as GPIO
from audioFuncs import AudioFuncs
#import padkeydriver
from lcd import LCD
from datetime import datetime
from subprocess import check_output
from serverSetup import StorageSetup
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

class Btn_Logic_Handler:
    def __init__(self, audFun: AudioFuncs, setup: StorageSetup, lcd:LCD):
        self.lcd = lcd
        self.AudioFuncs = audFun
        self.StorageSetup = setup
        self.flag = DEV_MODE
        self.folder_index = 0
        self.download_folders = []
        self.button_pressed_time = None
        self.playlist_name_create = ""
        self.current_character = ''
        self.current_song = None
        self.current_folder = None
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TOGGLE_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(NEXT_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(PAUSE_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(PREVIOUS_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(EXIT_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(LCD_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(NEXT_GPIO, GPIO.FALLING, callback=self.nextBtn)
        GPIO.add_event_detect(PREVIOUS_GPIO, GPIO.FALLING, callback=self.prevBtn)
        GPIO.add_event_detect(PAUSE_GPIO, GPIO.FALLING, callback=self.pauseBtn)
        GPIO.add_event_detect(EXIT_GPIO, GPIO.FALLING, callback=self.exitBtn)
        GPIO.add_event_detect(TOGGLE_GPIO, GPIO.FALLING, callback=self.Toggle_swtich)
        GPIO.add_event_detect(LCD_GPIO, GPIO.FALLING, callback=self.lcdBtn)

        self.Toggle_swtich(None)
        # self.DevMode()
        
        
        
    def Toggle_swtich(self, channel):
        
            if self.flag == CREATE_PLAYLIST_MODE:
                if self.current_character == '':
                    return
            
                if GPIO.input(TOGGLE_GPIO) == GPIO.LOW:
                    time.sleep(0.2)
                    if GPIO.input(TOGGLE_GPIO) == GPIO.LOW:
                        self.current_character = self.current_character.lower()
                        self.createPlaylist_mode()
                elif GPIO.input(TOGGLE_GPIO) == GPIO.HIGH:
                    time.sleep(0.2)
                    if GPIO.input(TOGGLE_GPIO) == GPIO.HIGH:
                        self.current_character = self.current_character.upper()
                        self.createPlaylist_mode()
            else:    
                if GPIO.input(TOGGLE_GPIO) == GPIO.LOW:
                    self.StorageSetup.p.audio_set_volume(50)
                elif GPIO.input(TOGGLE_GPIO) == GPIO.HIGH:
                    self.StorageSetup.p.audio_set_volume(96)

        
    def nextBtn(self, channel):
        if GPIO.input(channel) == GPIO.LOW:
            time.sleep(0.1)
            if GPIO.input(channel) == GPIO.LOW:
                self.button_pressed_time = time.time()  # Record the start time of the button press
                print("clicked next")

                if self.flag == MODE_MODE:
                    if self.folder_index < len(self.StorageSetup.folder_keys) - 1:
                        self.folder_index += 1
                        self.AudioFuncs.display_folderName(self.StorageSetup.folder_keys[self.folder_index])
                    elif self.folder_index == len(self.StorageSetup.folder_keys) -1:
                        self.folder_index = 0
                        self.AudioFuncs.display_folderName(self.StorageSetup.folder_keys[self.folder_index])
                        
                elif self.flag == AUDIO_MODE:
                    while GPIO.input(channel) == GPIO.LOW and time.time() - self.button_pressed_time <= 0.4:
                        pass  # Wait until the button is released or 0.5 seconds has passed
                    if time.time() - self.button_pressed_time > 0.4:
                        self.AudioFuncs.next_audio()  # Execute the function if pressed for 0.5 seconds or more
                    else:
                        self.AudioFuncs.forward()  # Execute the function if pressed less than 0.5 seconds
                
                elif self.flag == DOWNLOADED_AUDIO_MODE:
                    while GPIO.input(channel) == GPIO.LOW and time.time() - self.button_pressed_time <= 0.4:
                        pass  # Wait until the button is released or 0.5 seconds has passed
                    if time.time() - self.button_pressed_time > 0.4:
                        self.AudioFuncs.next_audio()  # Execute the function if pressed for 0.5 seconds or more
                    else:
                        self.AudioFuncs.forward()  # Execute the function if pressed less than 0.5 seconds
                        
                
                elif self.flag == CREATED_AUDIO_MODE:
                    while GPIO.input(channel) == GPIO.LOW and time.time() - self.button_pressed_time <= 0.4:
                        pass  # Wait until the button is released or 0.5 seconds has passed
                    if time.time() - self.button_pressed_time > 0.4:
                        self.AudioFuncs.next_audio()  # Execute the function if pressed for 0.5 seconds or more
                    else:
                        self.AudioFuncs.forward()  # Execute the function if pressed less than 0.5 seconds
                        
                elif self.flag == DEV_MODE:
                    if self.folder_index < len(self.download_folders) - 1:
                        self.folder_index += 1
                        self.AudioFuncs.display_download_folderName(self.download_folders[self.folder_index])
                    elif self.folder_index == len(self.download_folders) - 1:
                        self.folder_index = 0
                        self.AudioFuncs.display_download_folderName(self.download_folders[self.folder_index])
                        
                elif self.flag == TO_COPY_TO_MODE:
                    if self.folder_index < len(self.download_folders) - 1:
                        self.folder_index += 1
                        self.AudioFuncs.display_created_folderName(self.download_folders[self.folder_index])
                    elif self.folder_index == len(self.download_folders) - 1:
                        self.folder_index = 0
                        self.AudioFuncs.display_created_folderName(self.download_folders[self.folder_index])

                
                elif self.flag == CREATED_MODE:
                    if self.folder_index < len(self.download_folders) - 1:
                        self.folder_index += 1
                        self.AudioFuncs.display_created_folderName(self.download_folders[self.folder_index])
                    elif self.folder_index == len(self.download_folders) - 1:
                        self.folder_index = 0
                        self.AudioFuncs.display_created_folderName(self.download_folders[self.folder_index])

                elif self.flag == CREATE_PLAYLIST_MODE:
                    if GPIO.input(TOGGLE_GPIO) == GPIO.LOW:
                        current_character = playlistCreator.incrementAlphaSmall(current_character)
                    elif GPIO.input(TOGGLE_GPIO) == GPIO.HIGH:
                        current_character = playlistCreator.incrementAlphaCapital(current_character)
                    self.createPlaylist_mode()



    def prevBtn(self, channel):
        if GPIO.input(channel) == GPIO.LOW:
            time.sleep(0.1)
            if GPIO.input(channel) == GPIO.LOW:
                self.button_pressed_time = time.time()  # Record the start time of the button press 
                print("clicked prev")
                if self.flag == MODE_MODE:
                    if self.folder_index > 0:
                        self.folder_index -= 1
                        self.AudioFuncs.display_folderName(self.StorageSetup.folder_keys[self.folder_index])
                    elif self.folder_index == 0:
                        self.folder_index = len(self.StorageSetup.folder_keys) -1
                        self.AudioFuncs.display_folderName(self.StorageSetup.folder_keys[self.folder_index])

                elif self.flag == AUDIO_MODE:
                    print("REACHERRRRR PREV BTN")
                    # Implement the logic for long press
                    while GPIO.input(channel) == GPIO.LOW and time.time() - self.button_pressed_time <= 0.4:
                        pass  # Wait until the button is released or 0.5 seconds has passed
                    if time.time() - self.button_pressed_time > 0.4:
                        self.AudioFuncs.previous_audio()  # Execute the function if pressed for 0.5 seconds or more
                    else:
                        self.AudioFuncs.backward()  # Execute the function if pressed less than 0.5 seconds

                    
                elif self.flag == DOWNLOADED_AUDIO_MODE:
                    print("PREVIOUS FROM DOWNLOAD")
                    # Implement the logic for long press
                    while GPIO.input(channel) == GPIO.LOW and time.time() - self.button_pressed_time <= 0.4:
                        pass  # Wait until the button is released or 0.5 seconds has passed
                    if time.time() - self.button_pressed_time > 0.4:
                        self.AudioFuncs.previous_audio()  # Execute the function if pressed for 0.5 seconds or more
                    else:
                        self.AudioFuncs.backward()  # Execute the function if pressed less than 0.5 seconds

                elif self.flag == CREATED_AUDIO_MODE:
                    print("PREVIOUS FROM DOWNLOAD")
                    # Implement the logic for long press
                    while GPIO.input(channel) == GPIO.LOW and time.time() - self.button_pressed_time <= 0.4:
                        pass  # Wait until the button is released or 0.5 seconds has passed
                    if time.time() - self.button_pressed_time > 0.4:
                        self.AudioFuncs.previous_audio()  # Execute the function if pressed for 0.5 seconds or more
                    else:
                        self.AudioFuncs.backward()  # Execute the function if pressed less than 0.5 seconds


                elif self.flag == DEV_MODE:
                    print("REACHER PREV BTN")
                    if self.folder_index > 0:
                        self.folder_index -= 1
                        self.AudioFuncs.display_download_folderName(self.download_folders[self.folder_index])
                    elif self.folder_index == 0:
                        self.folder_index = len(self.download_folders) - 1
                        self.AudioFuncs.display_download_folderName(self.download_folders[self.folder_index])
                        
                elif self.flag == TO_COPY_TO_MODE:
                    if self.folder_index > 0:
                        self.folder_index -= 1
                        self.AudioFuncs.display_created_folderName(self.download_folders[self.folder_index])
                    elif self.folder_index == 0:
                        self.folder_index = len(self.download_folders) - 1
                        self.AudioFuncs.display_created_folderName(self.download_folders[self.folder_index])


                elif self.flag == CREATED_MODE:
                    print("REACHER PREV BTN")
                    if self.folder_index > 0:
                        self.folder_index -= 1
                        self.AudioFuncs.display_created_folderName(self.download_folders[self.folder_index])
                    elif self.folder_index == 0:
                        self.folder_index = len(self.download_folders) - 1
                        self.AudioFuncs.display_created_folderName(self.download_folders[self.folder_index])
                        
                elif self.flag == CREATE_PLAYLIST_MODE:
                    if GPIO.input(TOGGLE_GPIO) == GPIO.LOW:
                        current_character = playlistCreator.decrementAlphaSmall(current_character)
                    elif GPIO.input(TOGGLE_GPIO) == GPIO.HIGH:
                        current_character = playlistCreator.decrementAlphaCapital(current_character)
                    self.createPlaylist_mode()



    def pauseBtn(self, channel):
        if GPIO.input(channel) == GPIO.LOW:
            if flag == AUDIO_MODE:
                if GPIO.input(LCD_GPIO) == GPIO.LOW:
                    self.StorageSetup.downloadPlaylist()
                    
            elif flag == DOWNLOADED_AUDIO_MODE:
                if GPIO.input(LCD_GPIO) == GPIO.LOW:
                    os.system(f"rm -r downloads/{self.download_folders[self.folder_index]}")
                    print(f"Deleted {self.download_folders[self.folder_index]}")
                    flag = DEV_MODE
                    self.DevMode()
                    
            elif flag == CREATED_AUDIO_MODE:
                if GPIO.input(LCD_GPIO) == GPIO.LOW:
                    current_song = self.AudioFuncs.downloaded_songs_list[self.StorageSetup.current_audio_index]
                    current_folder = self.download_folders[self.folder_index]
                    os.system(f"rm -r created/{shlex.quote(current_folder)}/{shlex.quote(current_song)}")
                    print(f"rm -r created/{shlex.quote(current_folder)}/{shlex.quote(current_song)}")
                    flag = CREATED_MODE
                    self.created_mode()

            time.sleep(0.1)
            if GPIO.input(channel) == GPIO.LOW:
                print("clicked pause")
                if flag == MODE_MODE:
                    flag = AUDIO_MODE
                    self.AudioFuncs.mode = self.AudioFuncs.CLOUD_MODE
                    self.AudioFuncs.audio_start(self.StorageSetup.folder_keys[self.folder_index][:-1],self.folder_index)
                    
                elif flag == AUDIO_MODE:
                    self.AudioFuncs.pause_audio()
                    
                elif flag == DOWNLOADED_AUDIO_MODE:
                    self.button_pressed_time = time.time()
                    while GPIO.input(channel) == GPIO.LOW and time.time() - self.button_pressed_time <= 0.6:
                        pass  # Wait until the button is released or 0.5 seconds has passed
                    if time.time() - self.button_pressed_time > 0.6:
                        current_song = self.AudioFuncs.downloaded_songs_list[self.StorageSetup.current_audio_index]
                        current_folder = self.download_folders[self.folder_index]
                        flag = TO_COPY_TO_MODE  # Execute the function if pressed for 0.5 seconds or more
                        self.lcd.lcdDisplay.lcd_clear()
                        self.created_mode()
                    else:
                        self.AudioFuncs.pause_audio()

                elif flag == TO_COPY_TO_MODE:
                    cmd = (
                        f"cp downloads/{shlex.quote(current_folder)}/{shlex.quote(current_song)} "
                        f"created/{self.download_folders[self.folder_index]}")
                    print(cmd)
                    os.system(cmd)
                    flag = DEV_MODE
                    self.DevMode()
                    
                elif flag == CREATED_AUDIO_MODE:
                    self.AudioFuncs.pause_audio()

                
                elif flag == DEV_MODE:
                    self.button_pressed_time = time.time()  # Record the start time of the button press
                    
                    
                    flag = DOWNLOADED_AUDIO_MODE
                    self.AudioFuncs.mode = self.AudioFuncs.DOWNLOADED_MODE
                    self.AudioFuncs.downloaded_folder_name = self.download_folders[self.folder_index]
                    self.AudioFuncs.audio_start_downloaded()
                
                elif flag == CREATED_MODE:
                    self.button_pressed_time = time.time()  # Record the start time of the button press
                    if GPIO.input(LCD_GPIO) == GPIO.LOW:

                        current_folder = self.download_folders[self.folder_index]
                        os.system(f"rm -r created/{shlex.quote(current_folder)}")
                        print(f"rm -r created/{shlex.quote(current_folder)}/")
                        flag = CREATED_MODE
                        self.created_mode()

                    else:

                        flag = CREATED_AUDIO_MODE
                        self.AudioFuncs.mode = self.AudioFuncs.CREATED_MODE
                        self.AudioFuncs.downloaded_folder_name = self.download_folders[self.folder_index]
                        self.AudioFuncs.audio_start_created()

                
                elif flag == CREATE_PLAYLIST_MODE:
                    if current_character == '':
                        if playlist_name_create == "":
                            flag = DEV_MODE
                            self.DevMode()
                            return
                        dir = rf"/home/pi/Desktop/RemoteWebControl/created/{playlist_name_create}"
                        isExist = os.path.exists(dir)
                        if isExist:
                            print("folder exists")
                        else:
                            os.mkdir(dir)
                        playlist_name_create = ""
                        flag = DEV_MODE
                        self.DevMode()
                    else:
                        playlist_name_create = playlist_name_create + current_character
                        current_character = ''
                        self.createPlaylist_mode()

    def exitBtn(self, channel):
        if GPIO.input(channel) == GPIO.LOW:
            time.sleep(0.1)
            if GPIO.input(channel) == GPIO.LOW:
                print("clicked exit")       

                if flag == MODE_MODE:
                    flag = CREATED_MODE
                    self.created_mode()
                    
                elif flag == DEV_MODE:
                    self.button_pressed_time = time.time()
                    while GPIO.input(channel) == GPIO.LOW and time.time() - self.button_pressed_time <= 0.8:
                        pass  # Wait until the button is released or 0.5 seconds has passed
                    if time.time() - self.button_pressed_time > 0.8:
                        flag = CREATE_PLAYLIST_MODE  # Execute the function if pressed for 0.5 seconds or more
                        self.lcd.lcdDisplay.lcd_clear()
                        self.createPlaylist_mode()
                    else:
                        flag = MODE_MODE
                        self.mode_mode()
                        # Execute the function if pressed less than 0.5 seconds
                        
                elif flag == CREATED_MODE:
                    self.button_pressed_time = time.time()
                    while GPIO.input(channel) == GPIO.LOW and time.time() - self.button_pressed_time <= 0.8:
                        pass  # Wait until the button is released or 0.5 seconds has passed
                    if time.time() - self.button_pressed_time > 0.8:
                        flag = CREATE_PLAYLIST_MODE  # Execute the function if pressed for 0.5 seconds or more
                        self.lcd.lcdDisplay.lcd_clear()
                        self.createPlaylist_mode()
                    else:
                        flag = DEV_MODE
                        self.DevMode()
                        # Execute the function if pressed less than 0.5 seconds

                elif flag == CREATE_PLAYLIST_MODE:
                    self.lcd.lcdDisplay.lcd_clear()
                    playlist_name_create = ""
                    flag = DEV_MODE
                    self.DevMode()

                elif flag == CREATED_AUDIO_MODE:
                    flag = CREATED_MODE
                    self.created_mode()

                elif flag == AUDIO_MODE:
                    flag = MODE_MODE
                    self.mode_mode()
                elif flag == DOWNLOADED_AUDIO_MODE:
                    flag = DEV_MODE
                    self.DevMode()            

    def lcdBtn(self,channel):
        if GPIO.input(channel) == GPIO.LOW:
            time.sleep(0.1)
            if GPIO.input(channel) == GPIO.LOW:
                print("clicked lcd")       
                self.lcd.swapBacklight()
                
                
                    
                    
        
    def DevMode(self):
        self.AudioFuncs.audio_stop()
        self.download_folders = os.listdir(r"/home/pi/Desktop/RemoteWebControl/downloads/")
        if len(self.download_folders) == 0:
            self.lcd.lcdDisplay.lcd_clear()
            self.lcd.lcdDisplay.lcd_display_string("EMPTY!",2)
            return
        for file in self.download_folders:
            print(file)
        self.AudioFuncs.display_download_folderName(self.download_folders[0])


    def mode_mode(self):
        self.AudioFuncs.audio_stop()
        self.AudioFuncs.modeInit()

    def createPlaylist_mode(self):
        self.lcd.lcdDisplay.lcd_display_string("Create Playlist:",1)
        self.lcd.lcdDisplay.lcd_display_string(self.playlist_name_create + self.current_character,2)

    def created_mode(self):
        self.AudioFuncs.audio_stop()
        self.download_folders = os.listdir(r"/home/pi/Desktop/RemoteWebControl/created/")
        if len(self.download_folders) == 0:
            self.lcd.lcdDisplay.lcd_clear()
            self.lcd.lcdDisplay.lcd_display_string("EMPTY!",2)
            return
        for file in self.download_folders:
            print(file)
        self.AudioFuncs.display_created_folderName(self.download_folders[0])

