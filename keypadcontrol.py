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

MODE_MODE = 0
AUDIO_MODE = 5
DOWNLOADED_AUDIO_MODE = 10
LAST_PLAYED_MODE = 9
DEV_MODE = 22



NEXT_GPIO = 21
PAUSE_GPIO = 20
PREVIOUS_GPIO = 16
EXIT_GPIO = 19
LCD_GPIO = 18

TOGGLE_GPIO = 17

flag = MODE_MODE


folder_index = 0
download_folders = []
button_pressed_time = None




def Toggle_swtich(channel):
        if GPIO.input(TOGGLE_GPIO) == GPIO.LOW:
            serverSetup.p.audio_set_volume(50)
        elif GPIO.input(TOGGLE_GPIO) == GPIO.HIGH:
            serverSetup.p.audio_set_volume(100)

def nextBtn(channel):
    global button_pressed_time
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
                while GPIO.input(channel) == GPIO.LOW and time.time() - button_pressed_time <= 0.5:
                    pass  # Wait until the button is released or 0.5 seconds has passed
                if time.time() - button_pressed_time > 0.5:
                    audioFuncs.next_audio()  # Execute the function if pressed for 0.5 seconds or more
                else:
                    audioFuncs.forward()  # Execute the function if pressed less than 0.5 seconds
            
            elif flag == DOWNLOADED_AUDIO_MODE:
                while GPIO.input(channel) == GPIO.LOW and time.time() - button_pressed_time <= 0.5:
                    pass  # Wait until the button is released or 0.5 seconds has passed
                if time.time() - button_pressed_time > 0.5:
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



def prevBtn(channel):
    global button_pressed_time
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
                while GPIO.input(channel) == GPIO.LOW and time.time() - button_pressed_time <= 0.5:
                    pass  # Wait until the button is released or 0.5 seconds has passed
                if time.time() - button_pressed_time > 0.5:
                    audioFuncs.previous_audio()  # Execute the function if pressed for 0.5 seconds or more
                else:
                    audioFuncs.backward()  # Execute the function if pressed less than 0.5 seconds

                
            elif flag == DOWNLOADED_AUDIO_MODE:
                print("PREVIOUS FROM DOWNLOAD")
                # Implement the logic for long press
                while GPIO.input(channel) == GPIO.LOW and time.time() - button_pressed_time <= 0.5:
                    pass  # Wait until the button is released or 0.5 seconds has passed
                if time.time() - button_pressed_time > 0.5:
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


def pauseBtn(channel):
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
        time.sleep(0.1)
        if GPIO.input(channel) == GPIO.LOW:
            print("clicked pause")
            if flag == MODE_MODE:
                flag = AUDIO_MODE
                audioFuncs.audio_start(serverSetup.folder_keys[folder_index][:-1],folder_index)
            elif flag == AUDIO_MODE:
                audioFuncs.pause_audio()
            elif flag == DOWNLOADED_AUDIO_MODE:
                audioFuncs.pause_audio()
            elif flag == DEV_MODE:
                flag = DOWNLOADED_AUDIO_MODE
                audioFuncs.mode = audioFuncs.DOWNLOADED_MODE
                audioFuncs.downloaded_folder_name = download_folders[folder_index]
                audioFuncs.audio_start_downloaded()
            

def exitBtn(channel):
    if GPIO.input(channel) == GPIO.LOW:
        time.sleep(0.1)
        if GPIO.input(channel) == GPIO.LOW:
            global flag       
            global folder_index
            print("clicked exit")       

            if flag == MODE_MODE:
                flag = DEV_MODE
                DevMode()
            elif flag == DEV_MODE:
                flag = MODE_MODE
                mode_mode()
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
        lcd.lcdDisplay.lcd_display_string("EMPTY!")
        return
    for file in download_folders:
        print(file)
    random.shuffle(download_folders)
    audioFuncs.display_download_folderName(download_folders[0])


def mode_mode():
    audioFuncs.audio_stop()
    audioFuncs.modeInit()




################## Program Start ##########################

GPIO.setmode(GPIO.BCM)
GPIO.setup(TOGGLE_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(NEXT_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PAUSE_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PREVIOUS_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(EXIT_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LCD_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)



IP = check_output(["hostname", "-I"], encoding="utf8").split()[0]


Toggle_swtich(None)
audioFuncs.init()
mode_mode()

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

    Toggle_swtich(None)
    time.sleep(2)