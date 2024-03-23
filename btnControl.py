import RPi.GPIO as GPIO
from audioFuncs import AudioFuncs
#import padkeydriver
from lcd import LCD
from subprocess import check_output
from serverSetup import StorageSetup
from whatsUI import UI
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
WHATS_MODE = 324
CREATE_MESSAGE_MODE = 3
NUMERIC_MODE = 57

NEXT_GPIO = 21
PAUSE_GPIO = 20
PREVIOUS_GPIO = 16
EXIT_GPIO = 19
LCD_GPIO = 18

TOGGLE_GPIO = 17

class Btn_Logic_Handler:
    def __init__(self, audFun: AudioFuncs, setup: StorageSetup, lcd:LCD):
        self.ui = None
        self.lcd = lcd
        self.AudioFuncs = audFun
        self.StorageSetup = setup
        self.flag = DEV_MODE
        self.folder_index = 0
        self.download_folders = []
        # self.created_folders = []
        self.button_pressed_time = None
        self.playlist_name_create = ""
        self.current_character = ''
        self.current_song = None
        self.current_folder = None
        self.current_created_folder = None
        self.message = ""
        # self.saved_downloaded_folder_index = None
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
                        print("UPPEEEER")
                        self.current_character = self.current_character.upper()
                        self.createPlaylist_mode()
                        
                        
            elif self.isFlag(CREATE_MESSAGE_MODE):
                if self.current_character == '':
                    return
                if GPIO.input(TOGGLE_GPIO) == GPIO.LOW:
                    time.sleep(0.2)
                    if GPIO.input(TOGGLE_GPIO) == GPIO.LOW:
                        self.current_character = 'a'                        
                        self.sendMessage_mode()
                elif GPIO.input(TOGGLE_GPIO) == GPIO.HIGH:
                    time.sleep(0.2)
                    if GPIO.input(TOGGLE_GPIO) == GPIO.HIGH:
                        self.current_character = '0'
                        self.sendMessage_mode()
            
            else:    
                if GPIO.input(TOGGLE_GPIO) == GPIO.LOW:
                    self.StorageSetup.p.audio_set_volume(50)
                elif GPIO.input(TOGGLE_GPIO) == GPIO.HIGH:
                    self.StorageSetup.p.audio_set_volume(96)

        
    def nextBtn(self, channel):
        if self.debouncePassed(channel):
            print("clicked next")
            if self.isFlag(MODE_MODE):
                self.nextFolderPress(self.StorageSetup.folder_keys, "Cloud")
                    
            elif self.isFlag(AUDIO_MODE):
                if self.pressedAndHeld(channel, 0.4):
                    self.AudioFuncs.next_audio()  # Execute the function if pressed for 0.5 seconds or more
                else:
                    self.AudioFuncs.forward()  # Execute the function if pressed less than 0.5 seconds
            
            elif self.isFlag(DOWNLOADED_AUDIO_MODE):
                if self.pressedAndHeld(channel, 0.4):
                    self.AudioFuncs.next_audio()  # Execute the function if pressed for 0.5 seconds or more
                else:
                    self.AudioFuncs.forward()  # Execute the function if pressed less than 0.5 seconds

            elif self.isFlag(CREATED_AUDIO_MODE):
                if self.pressedAndHeld(channel, 0.4):
                    self.AudioFuncs.next_audio()  # Execute the function if pressed for 0.5 seconds or more
                else:
                    self.AudioFuncs.forward()  # Execute the function if pressed less than 0.5 seconds
                    
            elif self.isFlag(DEV_MODE):
                self.nextFolderPress(self.download_folders, "Downloaded")
                
            elif self.isFlag(TO_COPY_TO_MODE):
                self.nextFolderPress(self.download_folders, "Created")
                
            elif self.isFlag(CREATED_MODE):
                self.nextFolderPress(self.download_folders, "Created")
                
            elif self.isFlag(CREATE_PLAYLIST_MODE):
                self.current_character = self.nextAlphabetPress(self.current_character)
                self.createPlaylist_mode()
                
            elif self.isFlag(WHATS_MODE):
                self.ui.incrementIndex()
                self.ui.display_message(self.ui.messageIndex)
                print("index at " + str(self.ui.messageIndex))
                
            elif self.isFlag(CREATE_MESSAGE_MODE):
                self.current_character = self.nextNumAlphaPress(self.current_character)                    
                self.sendMessage_mode()


    def prevBtn(self, channel):
        if self.debouncePassed(channel):
            self.button_pressed_time = time.time()  # Record the start time of the button press 
            print("clicked prev")
            if self.isFlag(MODE_MODE):
                self.prevFolderPress(self.StorageSetup.folder_keys, "Cloud")
                
            elif self.isFlag(AUDIO_MODE):
                print("REACHERRRRR PREV BTN")
                if self.pressedAndHeld(channel, 0.4):
                    self.AudioFuncs.previous_audio()  # Execute the function if pressed for 0.5 seconds or more
                else:
                    self.AudioFuncs.backward()  # Execute the function if pressed less than 0.5 seconds
                
            elif self.isFlag(DOWNLOADED_AUDIO_MODE):
                print("PREVIOUS FROM DOWNLOAD")
                if self.pressedAndHeld(channel, 0.4):
                    self.AudioFuncs.previous_audio()  # Execute the function if pressed for 0.5 seconds or more
                else:
                    self.AudioFuncs.backward()  # Execute the function if pressed less than 0.5 seconds
            elif self.isFlag(CREATED_AUDIO_MODE):
                print("PREVIOUS FROM DOWNLOAD")
                if self.pressedAndHeld(channel, 0.4):
                    self.AudioFuncs.previous_audio()  # Execute the function if pressed for 0.5 seconds or more
                else:
                    self.AudioFuncs.backward()  # Execute the function if pressed less than 0.5 seconds
                    
            elif self.isFlag(DEV_MODE):
                self.prevFolderPress(self.download_folders, "Downloaded")
                print("REACHED PREV Downloads Playlists BTN")
                
            elif self.isFlag(TO_COPY_TO_MODE):
                self.prevFolderPress(self.download_folders, "Created")
                
            elif self.isFlag(CREATED_MODE):
                print("REACHER PREV BTN")
                self.prevFolderPress(self.download_folders, "Created")          
                          
            elif self.isFlag(CREATE_PLAYLIST_MODE):
                self.current_character = self.prevAlphabetPress(self.current_character)
                self.createPlaylist_mode()
                
            elif self.isFlag(WHATS_MODE):
                self.ui.decrementIndex()
                self.ui.display_message(self.ui.messageIndex)
                print("index at " + str(self.ui.messageIndex))
                
            elif self.isFlag(CREATE_MESSAGE_MODE):
                self.current_character = self.prevNumAlphaPress(self.current_character)                    
                self.sendMessage_mode()
                


    def pauseBtn(self, channel):
        if self.debouncePassed(channel):
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

            print("clicked pause")
            if self.isFlag(MODE_MODE):
                self.AudioFuncs.mode = self.AudioFuncs.CLOUD_MODE
                self.AudioFuncs.audio_start(self.getFolderName(self.folder_index),self.folder_index)
                self.flag = AUDIO_MODE
                
            elif self.isFlag(AUDIO_MODE):
                self.AudioFuncs.pause_audio()
                
            elif self.isFlag(DOWNLOADED_AUDIO_MODE):
                if self.pressedAndHeld(channel, 0.6):
                    self.current_song = self.AudioFuncs.downloaded_songs_list[self.StorageSetup.current_audio_index]
                    self.current_folder = self.download_folders[self.folder_index]
                    self.flag = TO_COPY_TO_MODE  # Execute the function if pressed for 0.5 seconds or more
                    self.lcd.lcdDisplay.lcd_clear()
                    self.folder_index = 0
                    self.created_mode()
                else:
                    self.AudioFuncs.pause_audio()
                    
            elif self.isFlag(TO_COPY_TO_MODE):
                self.copySongtoFolder(self.current_folder, self.getCurrentFolder("Created"), self.getCurrentSong())
                self.flag = DEV_MODE
                self.DevMode()
                
            elif self.isFlag(CREATED_AUDIO_MODE):
                self.AudioFuncs.pause_audio()
            
            elif self.isFlag(DEV_MODE):
                self.button_pressed_time = time.time()  # Record the start time of the button press
                self.flag = DOWNLOADED_AUDIO_MODE
                self.AudioFuncs.mode = self.AudioFuncs.DOWNLOADED_MODE
                self.AudioFuncs.downloaded_folder_name = self.download_folders[self.folder_index]
                self.AudioFuncs.audio_start_playlist("Downloaded")
            
            elif self.isFlag(CREATED_MODE):
                self.button_pressed_time = time.time()  # Record the start time of the button press
                if self.isLcdPressed():
                    self.deleteFolder("Created", self.folder_index)
                    self.flag = CREATED_MODE
                    self.created_mode()
                else:
                    self.flag = CREATED_AUDIO_MODE
                    self.AudioFuncs.mode = self.AudioFuncs.CREATED_MODE
                    self.AudioFuncs.downloaded_folder_name = self.download_folders[self.folder_index]
                    try:
                        self.AudioFuncs.audio_start_playlist("Created")
                    except:
                        self.StorageSetup.current_audio_index = 0
                        self.AudioFuncs.audio_start_playlist("Created")
            elif self.isFlag(CREATE_PLAYLIST_MODE):
                self.createPlaylist()
                
            elif self.isFlag(WHATS_MODE):
                self.ui.breakLongMessage()
                self.flag = CREATE_MESSAGE_MODE
                self.lcd.lcdDisplay.lcd_clear()
                self.sendMessage_mode()
                
            elif self.isFlag(CREATE_MESSAGE_MODE):
                self.createMessage()
            


    def exitBtn(self, channel):
        if self.debouncePassed(channel):
            print("clicked exit")       
            if self.isFlag(MODE_MODE):
                self.flag = CREATED_MODE
                self.folder_index = 0
                self.created_mode()
            elif self.isFlag(DEV_MODE):
                if self.pressedAndHeld(channel, 0.8):
                    self.flag = CREATE_PLAYLIST_MODE  # Execute the function if pressed for 0.5 seconds or more
                    self.lcd.lcdDisplay.lcd_clear()
                    self.createPlaylist_mode()
                else:
                    self.flag = MODE_MODE
                    self.mode_mode()
            elif self.isFlag(CREATED_MODE):
                if self.pressedAndHeld(channel, 0.8):
                    self.flag = CREATE_PLAYLIST_MODE  # Execute the function if pressed for 0.5 seconds or more
                    self.lcd.lcdDisplay.lcd_clear()
                    self.createPlaylist_mode()
                else:
                    self.folder_index = 0
                    self.flag = WHATS_MODE
                    self.whatsUIMode()
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
            elif self.isFlag(WHATS_MODE):
                self.flag = DEV_MODE
                self.ui.breakLongMessage()
                self.DevMode()
            


    def lcdBtn(self,channel):
        if self.debouncePassed(channel):
            print("clicked lcd")       
            if self.isFlag(CREATE_MESSAGE_MODE):
                self.message += ' '
                self.sendMessage_mode()
            else:
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
        # self.AudioFuncs.modeInit()
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

    def sendMessage_mode(self):
        self.lcd.lcdDisplay.lcd_display_string("Create Message:",1)
        self.lcd.lcdDisplay.lcd_display_string(self.message + self.current_character,2)
        

    def created_mode(self):
        self.AudioFuncs.audio_stop()
        # self.saved_downloaded_folder_index = self.folder_index
        self.download_folders = os.listdir(r"/home/pi/Desktop/RemoteWebControl/created/")
        # self.created_folders = os.listdir(r"/home/pi/Desktop/RemoteWebControl/created/")
        
        if len(self.download_folders) == 0:
            self.lcd.lcdDisplay.lcd_clear()
            self.lcd.lcdDisplay.lcd_display_string("EMPTY!",2)
            return
        for file in self.download_folders:
            print(file)
        self.AudioFuncs.display_created_folderName(self.download_folders[0]) ################################################
        
        
    def whatsUIMode(self):
        self.flag = WHATS_MODE
        self.lcd.lcdDisplay.lcd_clear()
        self.ui = UI()
        self.ui.display_message(self.ui.messageIndex)
        


####################################################################################
####################################################################################
####################################################################################

    def debouncePassed(self, channel) -> bool:
        if GPIO.input(channel) == GPIO.LOW:
            time.sleep(0.1)
            return GPIO.input(channel) == GPIO.LOW



    def isLcdPressed(self):
        return GPIO.input(LCD_GPIO) == GPIO.LOW
    
    def isFlag(self, mode):
        return self.flag == mode
    
    def deleteFolder(self, mode, index):
        if mode == "Downloaded":
            os.system(f"rm -r downloads/{self.download_folders[index]}")
            print(f"Deleted {self.download_folders[index]}")

        elif mode == "Created":
            self.current_folder = self.download_folders[self.folder_index]
            os.system(f"rm -r created/{shlex.quote(self.current_folder)}")
            print(f"rm -r created/{shlex.quote(self.current_folder)}/")

        

    def deleteSong(self, folder, song):
        os.system(f"rm -r created/{shlex.quote(folder)}/{shlex.quote(song)}")
        print(f"rm -r created/{shlex.quote(folder)}/{shlex.quote(song)}")


    def getCurrentSong(self):
        return self.AudioFuncs.downloaded_songs_list[self.StorageSetup.current_audio_index]

    def getCurrentFolder(self, mode = "Downloaded", index = 0):
        if index == 0:
            if mode == "Created":
                return self.download_folders[self.folder_index]
            elif mode == "Downloaded":
                return self.download_folders[self.folder_index]
        else:
            if mode == "Created":
                return self.download_folders[index]
            elif mode == "Downloaded":
                return self.download_folders[index]

            
    def nextFolderPress(self, folderList, mode):
        try:
            if self.folder_index < len(folderList) - 1:
                self.folder_index += 1
                if mode == "Downloaded":
                    self.AudioFuncs.display_download_folderName(folderList[self.folder_index])
                elif mode == "Created":
                    self.AudioFuncs.display_created_folderName(folderList[self.folder_index])
                elif mode == "Cloud":
                    self.AudioFuncs.display_folderName(folderList[self.folder_index])
            elif self.folder_index == len(folderList) -1:
                self.folder_index = 0
                if mode == "Downloaded":
                    self.AudioFuncs.display_download_folderName(folderList[self.folder_index])
                elif mode == "Created":
                    self.AudioFuncs.display_created_folderName(folderList[self.folder_index])
                elif mode == "Cloud":
                    self.AudioFuncs.display_folderName(folderList[self.folder_index])
        except:
            self.folder_index = 0
            self.nextFolderPress(folderList, mode)

    def prevFolderPress(self, folderList, mode):
        try:
            if self.folder_index > 0:
                self.folder_index -= 1
                if mode == "Downloaded":
                    self.AudioFuncs.display_download_folderName(folderList[self.folder_index])
                elif mode == "Created":
                    self.AudioFuncs.display_created_folderName(folderList[self.folder_index])
                elif mode == "Cloud":
                    self.AudioFuncs.display_folderName(folderList[self.folder_index])
            elif self.folder_index == 0:
                self.folder_index = len(folderList) -1
                if mode == "Downloaded":
                    self.AudioFuncs.display_download_folderName(folderList[self.folder_index])
                elif mode == "Created":
                    self.AudioFuncs.display_created_folderName(folderList[self.folder_index])
                elif mode == "Cloud":
                    self.AudioFuncs.display_folderName(folderList[self.folder_index])
        except:
            self.folder_index = 0
            self.prevFolderPress(folderList, mode)


    def nextAlphabetPress(self, character):
        if GPIO.input(TOGGLE_GPIO) == GPIO.LOW:
            return playlistCreator.incrementAlphaSmall(character)
        elif GPIO.input(TOGGLE_GPIO) == GPIO.HIGH:
            return playlistCreator.incrementAlphaCapital(character)

    def prevAlphabetPress(self, character):
        if GPIO.input(TOGGLE_GPIO) == GPIO.LOW:
            return playlistCreator.decrementAlphaSmall(character)
        elif GPIO.input(TOGGLE_GPIO) == GPIO.HIGH:
            return playlistCreator.decrementAlphaCapital(character)
    
    def prevNumAlphaPress(self, character):
        if GPIO.input(TOGGLE_GPIO) == GPIO.LOW:
            return playlistCreator.decrementAlphaSmall(character)
        elif GPIO.input(TOGGLE_GPIO) == GPIO.HIGH:
            return playlistCreator.decrementNumerical(character)
    
    def nextNumAlphaPress(self, character):
        if GPIO.input(TOGGLE_GPIO) == GPIO.LOW:
            return playlistCreator.incrementAlphaSmall(character)
        elif GPIO.input(TOGGLE_GPIO) == GPIO.HIGH:
            return playlistCreator.incrementNumerical(character)

    def getFolderName(self, index):
        return self.StorageSetup.folder_keys[index][:-1]
    
    def pressedAndHeld(self, channel, timePressed):
        self.button_pressed_time = time.time()
        while GPIO.input(channel) == GPIO.LOW and time.time() - self.button_pressed_time <= timePressed:
            pass  # Wait until the button is released or 0.6 seconds has passed
        return time.time() - self.button_pressed_time > timePressed
    
    def copySongtoFolder(self, currentDownloadFolder, currentCreatedFolder, song):
        cmd = (
                        f"cp downloads/{shlex.quote(currentDownloadFolder)}/{shlex.quote(song)} "
                        f"created/{currentCreatedFolder}")
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



    def createMessage(self):
        if self.current_character == '':
            if self.message == "":
                self.flag = WHATS_MODE
                self.whatsUIMode()
                return
            else:
                self.ui.send_message(self.message)
                self.message = ""
                self.flag = WHATS_MODE
                self.whatsUIMode()
        else:
            self.message = self.message + self.current_character
            self.current_character = ''
            self.sendMessage_mode()



    