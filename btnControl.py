import RPi.GPIO as GPIO
from audioFuncs import AudioFuncs
#import padkeydriver
from lcd import LCD
from subprocess import check_output
from serverSetup import StorageSetup
import time
import os
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
        
            if self.isFlag(CREATE_PLAYLIST_MODE):
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

                if self.isFlag(MODE_MODE):
                    if self.folder_index < len(self.StorageSetup.folder_keys) - 1:
                        self.folder_index += 1
                        self.AudioFuncs.display_folderName(self.StorageSetup.folder_keys[self.folder_index])
                    elif self.folder_index == len(self.StorageSetup.folder_keys) -1:
                        self.folder_index = 0
                        self.AudioFuncs.display_folderName(self.StorageSetup.folder_keys[self.folder_index])
                        
                elif self.isFlag(AUDIO_MODE):
                    while GPIO.input(channel) == GPIO.LOW and time.time() - self.button_pressed_time <= 0.4:
                        pass  # Wait until the button is released or 0.5 seconds has passed
                    if time.time() - self.button_pressed_time > 0.4:
                        self.AudioFuncs.next_audio()  # Execute the function if pressed for 0.5 seconds or more
                    else:
                        self.AudioFuncs.forward()  # Execute the function if pressed less than 0.5 seconds
                
                elif self.isFlag(DOWNLOADED_AUDIO_MODE):
                    while GPIO.input(channel) == GPIO.LOW and time.time() - self.button_pressed_time <= 0.4:
                        pass  # Wait until the button is released or 0.5 seconds has passed
                    if time.time() - self.button_pressed_time > 0.4:
                        self.AudioFuncs.next_audio()  # Execute the function if pressed for 0.5 seconds or more
                    else:
                        self.AudioFuncs.forward()  # Execute the function if pressed less than 0.5 seconds
                        
                
                elif self.isFlag(CREATED_AUDIO_MODE):
                    while GPIO.input(channel) == GPIO.LOW and time.time() - self.button_pressed_time <= 0.4:
                        pass  # Wait until the button is released or 0.5 seconds has passed
                    if time.time() - self.button_pressed_time > 0.4:
                        self.AudioFuncs.next_audio()  # Execute the function if pressed for 0.5 seconds or more
                    else:
                        self.AudioFuncs.forward()  # Execute the function if pressed less than 0.5 seconds
                        
                elif self.isFlag(DEV_MODE):
                    if self.folder_index < len(self.download_folders) - 1:
                        self.folder_index += 1
                        self.AudioFuncs.display_download_folderName(self.download_folders[self.folder_index])
                    elif self.folder_index == len(self.download_folders) - 1:
                        self.folder_index = 0
                        self.AudioFuncs.display_download_folderName(self.download_folders[self.folder_index])
                        
                elif self.isFlag(TO_COPY_TO_MODE):
                    if self.folder_index < len(self.download_folders) - 1:
                        self.folder_index += 1
                        self.AudioFuncs.display_created_folderName(self.download_folders[self.folder_index])
                    elif self.folder_index == len(self.download_folders) - 1:
                        self.folder_index = 0
                        self.AudioFuncs.display_created_folderName(self.download_folders[self.folder_index])

                
                elif self.isFlag(CREATED_MODE):
                    if self.folder_index < len(self.download_folders) - 1:
                        self.folder_index += 1
                        self.AudioFuncs.display_created_folderName(self.download_folders[self.folder_index])
                    elif self.folder_index == len(self.download_folders) - 1:
                        self.folder_index = 0
                        self.AudioFuncs.display_created_folderName(self.download_folders[self.folder_index])

                elif self.isFlag(CREATE_PLAYLIST_MODE):
                    if GPIO.input(TOGGLE_GPIO) == GPIO.LOW:
                        self.current_character = playlistCreator.incrementAlphaSmall(self.current_character)
                    elif GPIO.input(TOGGLE_GPIO) == GPIO.HIGH:
                        self.current_character = playlistCreator.incrementAlphaCapital(self.current_character)
                    self.createPlaylist_mode()



    def prevBtn(self, channel):
        if GPIO.input(channel) == GPIO.LOW:
            time.sleep(0.1)
            if GPIO.input(channel) == GPIO.LOW:
                self.button_pressed_time = time.time()  # Record the start time of the button press 
                print("clicked prev")
                if self.isFlag(MODE_MODE):
                    if self.folder_index > 0:
                        self.folder_index -= 1
                        self.AudioFuncs.display_folderName(self.StorageSetup.folder_keys[self.folder_index])
                    elif self.folder_index == 0:
                        self.folder_index = len(self.StorageSetup.folder_keys) -1
                        self.AudioFuncs.display_folderName(self.StorageSetup.folder_keys[self.folder_index])

                elif self.isFlag(AUDIO_MODE):
                    print("REACHERRRRR PREV BTN")
                    # Implement the logic for long press
                    while GPIO.input(channel) == GPIO.LOW and time.time() - self.button_pressed_time <= 0.4:
                        pass  # Wait until the button is released or 0.5 seconds has passed
                    if time.time() - self.button_pressed_time > 0.4:
                        self.AudioFuncs.previous_audio()  # Execute the function if pressed for 0.5 seconds or more
                    else:
                        self.AudioFuncs.backward()  # Execute the function if pressed less than 0.5 seconds

                    
                elif self.isFlag(DOWNLOADED_AUDIO_MODE):
                    print("PREVIOUS FROM DOWNLOAD")
                    # Implement the logic for long press
                    while GPIO.input(channel) == GPIO.LOW and time.time() - self.button_pressed_time <= 0.4:
                        pass  # Wait until the button is released or 0.5 seconds has passed
                    if time.time() - self.button_pressed_time > 0.4:
                        self.AudioFuncs.previous_audio()  # Execute the function if pressed for 0.5 seconds or more
                    else:
                        self.AudioFuncs.backward()  # Execute the function if pressed less than 0.5 seconds

                elif self.isFlag(CREATED_AUDIO_MODE):
                    print("PREVIOUS FROM DOWNLOAD")
                    # Implement the logic for long press
                    while GPIO.input(channel) == GPIO.LOW and time.time() - self.button_pressed_time <= 0.4:
                        pass  # Wait until the button is released or 0.5 seconds has passed
                    if time.time() - self.button_pressed_time > 0.4:
                        self.AudioFuncs.previous_audio()  # Execute the function if pressed for 0.5 seconds or more
                    else:
                        self.AudioFuncs.backward()  # Execute the function if pressed less than 0.5 seconds


                elif self.isFlag(DEV_MODE):
                    print("REACHER PREV BTN")
                    if self.folder_index > 0:
                        self.folder_index -= 1
                        self.AudioFuncs.display_download_folderName(self.download_folders[self.folder_index])
                    elif self.folder_index == 0:
                        self.folder_index = len(self.download_folders) - 1
                        self.AudioFuncs.display_download_folderName(self.download_folders[self.folder_index])
                        
                elif self.isFlag(TO_COPY_TO_MODE):
                    if self.folder_index > 0:
                        self.folder_index -= 1
                        self.AudioFuncs.display_created_folderName(self.download_folders[self.folder_index])
                    elif self.folder_index == 0:
                        self.folder_index = len(self.download_folders) - 1
                        self.AudioFuncs.display_created_folderName(self.download_folders[self.folder_index])


                elif self.isFlag(CREATED_MODE):
                    print("REACHER PREV BTN")
                    if self.folder_index > 0:
                        self.folder_index -= 1
                        self.AudioFuncs.display_created_folderName(self.download_folders[self.folder_index])
                    elif self.folder_index == 0:
                        self.folder_index = len(self.download_folders) - 1
                        self.AudioFuncs.display_created_folderName(self.download_folders[self.folder_index])
                        
                elif self.isFlag(CREATE_PLAYLIST_MODE):
                    if GPIO.input(TOGGLE_GPIO) == GPIO.LOW:
                        self.current_character = playlistCreator.decrementAlphaSmall(self.current_character)
                    elif GPIO.input(TOGGLE_GPIO) == GPIO.HIGH:
                        self.current_character = playlistCreator.decrementAlphaCapital(self.current_character)
                    self.createPlaylist_mode()



    def pauseBtn(self, channel):
        if GPIO.input(channel) == GPIO.LOW:
            if self.isFlag(AUDIO_MODE):
                if self.isLcdPressed():
                    self.StorageSetup.downloadPlaylist()
                    
            elif self.isFlag(DOWNLOADED_AUDIO_MODE):
                if self.isLcdPressed():
                    self.deleteFolder("Downloaded", self.folder_index)
                    self.flag = DEV_MODE
                    self.DevMode()
                    
            elif self.isFlag(CREATED_AUDIO_MODE):
                if self.isLcdPressed():
                    self.deleteSong(self.getCurrentFolder(), self.getCurrentSong())
                    self.flag = CREATED_MODE
                    self.created_mode()

            time.sleep(0.1)

            if GPIO.input(channel) == GPIO.LOW:
                print("clicked pause")
                if self.isFlag(MODE_MODE):
                    self.AudioFuncs.mode = self.AudioFuncs.CLOUD_MODE
                    self.AudioFuncs.audio_start(self.getFolderName(self.folder_index),self.folder_index)
                    self.flag = AUDIO_MODE
                    
                elif self.isFlag(AUDIO_MODE):
                    self.AudioFuncs.pause_audio()
                    
                elif self.isFlag(DOWNLOADED_AUDIO_MODE):
                    if self.pressAndHold(channel, 0.6):
                        self.current_song = self.AudioFuncs.downloaded_songs_list[self.StorageSetup.current_audio_index]
                        self.current_folder = self.download_folders[self.folder_index]
                        self.flag = TO_COPY_TO_MODE  # Execute the function if pressed for 0.5 seconds or more
                        self.lcd.lcdDisplay.lcd_clear()
                        self.created_mode()
                    else:
                        self.AudioFuncs.pause_audio()

                elif self.isFlag(TO_COPY_TO_MODE):
                    self.copySongtoFolder(self.current_song, self.getCurrentFolder, self.getCurrentSong())
                    self.flag = DEV_MODE
                    self.DevMode()
                    
                elif self.isFlag(CREATED_AUDIO_MODE):
                    self.AudioFuncs.pause_audio()

                
                elif self.isFlag(DEV_MODE):
                    self.button_pressed_time = time.time()  # Record the start time of the button press
                    
                    
                    self.flag = DOWNLOADED_AUDIO_MODE
                    self.AudioFuncs.mode = self.AudioFuncs.DOWNLOADED_MODE
                    self.AudioFuncs.downloaded_folder_name = self.download_folders[self.folder_index]
                    self.AudioFuncs.audio_start_downloaded()
                
                elif self.isFlag(CREATED_MODE):
                    self.button_pressed_time = time.time()  # Record the start time of the button press
                    if self.isLcdPressed():
                        self.deleteFolder("Created", self.folder_index)
                        # self.current_folder = self.download_folders[self.folder_index]
                        # os.system(f"rm -r created/{shlex.quote(self.current_folder)}")
                        # print(f"rm -r created/{shlex.quote(self.current_folder)}/")
                        self.flag = CREATED_MODE
                        self.created_mode()

                    else:
                        self.flag = CREATED_AUDIO_MODE
                        self.AudioFuncs.mode = self.AudioFuncs.CREATED_MODE
                        self.AudioFuncs.downloaded_folder_name = self.download_folders[self.folder_index]
                        try:
                            self.AudioFuncs.audio_start_created()
                        except:
                            self.StorageSetup.current_audio_index = 0
                            self.AudioFuncs.audio_start_created()

                elif self.isFlag(CREATE_PLAYLIST_MODE):
                    self.createPlaylist()

    def exitBtn(self, channel):
        if GPIO.input(channel) == GPIO.LOW:
            time.sleep(0.1)
            if GPIO.input(channel) == GPIO.LOW:
                print("clicked exit")       

                if self.isFlag(MODE_MODE):
                    self.flag = CREATED_MODE
                    self.created_mode()
                    
                elif self.isFlag(DEV_MODE):
                    self.button_pressed_time = time.time()
                    while GPIO.input(channel) == GPIO.LOW and time.time() - self.button_pressed_time <= 0.8:
                        pass  # Wait until the button is released or 0.5 seconds has passed
                    if time.time() - self.button_pressed_time > 0.8:
                        self.flag = CREATE_PLAYLIST_MODE  # Execute the function if pressed for 0.5 seconds or more
                        self.lcd.lcdDisplay.lcd_clear()
                        self.createPlaylist_mode()
                    else:
                        self.flag = MODE_MODE
                        self.mode_mode()
                        # Execute the function if pressed less than 0.5 seconds
                        
                elif self.isFlag(CREATED_MODE):
                    self.button_pressed_time = time.time()
                    while GPIO.input(channel) == GPIO.LOW and time.time() - self.button_pressed_time <= 0.8:
                        pass  # Wait until the button is released or 0.5 seconds has passed
                    if time.time() - self.button_pressed_time > 0.8:
                        self.flag = CREATE_PLAYLIST_MODE  # Execute the function if pressed for 0.5 seconds or more
                        self.lcd.lcdDisplay.lcd_clear()
                        self.createPlaylist_mode()
                    else:
                        self.flag = DEV_MODE
                        self.DevMode()
                        # Execute the function if pressed less than 0.5 seconds

                elif self.isFlag(CREATE_PLAYLIST_MODE):
                    self.lcd.lcdDisplay.lcd_clear()
                    self.playlist_name_create = ""
                    self.flag = DEV_MODE
                    self.DevMode()

                elif self.isFlag(CREATED_AUDIO_MODE):
                    self.flag = CREATED_MODE
                    self.created_mode()

                elif self.isFlag(AUDIO_MODE):
                    self.flag = MODE_MODE
                    self.mode_mode()
                elif self.isFlag(DOWNLOADED_AUDIO_MODE):
                    self.flag = DEV_MODE
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
            
        self.AudioFuncs.display_download_folderName(self.download_folders[self.folder_index])


    def mode_mode(self):
        self.AudioFuncs.audio_stop()
        self.AudioFuncs.modeInit()
        self.lcd.lcdDisplay.lcd_clear()
        self.StorageSetup.current_audio_index = 0
        self.StorageSetup.getFolders()
        if len(self.StorageSetup.folder_keys) == 0:
            self.lcd.lcdDisplay.lcd_display_string("Cloud Error!",1)
            self.lcd.lcdDisplay.lcd_display_string("Try Dwnlds",2)
        else:
            self.AudioFuncs.display_folderName(self.StorageSetup.folder_keys[0])

        

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


####################################################################################
####################################################################################
####################################################################################


    def isLcdPressed(self):
        return GPIO.input(LCD_GPIO) == GPIO.LOW
    
    def isFlag(self, mode):
        return self.flag == mode
    
    def deleteFolder(self, mode, index):
        if mode == "Created":
            os.system(f"rm -r downloads/{self.download_folders[index]}")
            print(f"Deleted {self.download_folders[index]}")

        elif mode == "Downloaded":
            self.current_folder = self.download_folders[self.folder_index]
            os.system(f"rm -r created/{shlex.quote(self.current_folder)}")
            print(f"rm -r created/{shlex.quote(self.current_folder)}/")

        

    def deleteSong(self, folder, song):
        os.system(f"rm -r created/{shlex.quote(folder)}/{shlex.quote(song)}")
        print(f"rm -r created/{shlex.quote(folder)}/{shlex.quote(song)}")


    def getCurrentSong(self):
        return self.AudioFuncs.downloaded_songs_list[self.StorageSetup.current_audio_index]

    def getCurrentFolder(self):
        return self.download_folders[self.folder_index]
    
    def getFolderName(self, index):
        return self.StorageSetup.folder_keys[index][:-1]
    
    def pressAndHold(self, channel, timePressed):
        self.button_pressed_time = time.time()
        while GPIO.input(channel) == GPIO.LOW and time.time() - self.button_pressed_time <= timePressed:
            pass  # Wait until the button is released or 0.6 seconds has passed
        return time.time() - self.button_pressed_time > timePressed
    
    def copySongtoFolder(self, currentFolder, folder, song):
        cmd = (
                        f"cp downloads/{shlex.quote(currentFolder)}/{shlex.quote(song)} "
                        f"created/{folder}")
        print(cmd)
        os.system(cmd)


    def createPlaylist(self):
        if self.current_character == '':
            if self.playlist_name_create == "":
                self.flag = DEV_MODE
                self.DevMode()
                return
            dir = rf"/home/pi/Desktop/RemoteWebControl/created/{self.playlist_name_create}"
            isExist = os.path.exists(dir)
            if isExist:
                print("folder exists")
            else:
                os.mkdir(dir)
            self.playlist_name_create = ""
            self.flag = DEV_MODE
            self.DevMode()
        else:
            self.playlist_name_create = self.playlist_name_create + self.current_character
            self.current_character = ''
            self.createPlaylist_mode()
