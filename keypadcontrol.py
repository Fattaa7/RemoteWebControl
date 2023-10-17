import RPi.GPIO as GPIO
import threading
import audioFuncs
import padkeydriver
import lcd
from datetime import datetime
from subprocess import check_output
import serverSetup
import time
import os


MODE_MODE = 0
AUDIO_MODE = 5
LAST_PLAYED_MODE = 9
DEV_MODE = 22

flag = LAST_PLAYED_MODE
folder_index = 0

IP = check_output(["hostname", "-I"], encoding="utf8").split()[0]



def DevMode():
    print("Buttooon!")
    lcd.init()
    lcd.lcdDisplay.lcd_display_string("IP Address is:",1)
    lcd.lcdDisplay.lcd_display_string("" + str(IP),2)
    while True:
        continue

def play_last_played_song():
    global flag
    with open('output.txt', 'r') as f:
        folder_name_read = f.readline().rstrip()  # Read the first line
        file_name_read = f.readline().rstrip()  # Read the second line
        serverSetup.current_audio_index = int(file_name_read)
        audioFuncs.audio_start(serverSetup.folder_keys[int(folder_name_read)][:-1],int(folder_name_read))
        flag = AUDIO_MODE
    

def looping_on_mode():
    #serverSetup.getFolders()
    audioFuncs.audio_stop()
    audioFuncs.modeInit()
    if flag == LAST_PLAYED_MODE:
        play_last_played_song()
    elif flag == MODE_MODE:
        while flag == MODE_MODE:
            modeLoop()
            time.sleep(0.3)
        audioFuncs.audio_start(serverSetup.folder_keys[folder_index][:-1],folder_index)


def mainLoop():
    global flag
    global main_timer
    pressed_key = padkeydriver.read_keypad()
    if pressed_key is not None:
        print("Pressed key:", pressed_key)
        if pressed_key == padkeydriver.PREVIOUS:
            audioFuncs.previous_audio()
            
        if pressed_key == padkeydriver.NEXT:
            flag = MODE_MODE
            return
            #looping_on_mode()
            audioFuncs.next_audio()
            
        if pressed_key == padkeydriver.PAUSE_PLAY:
            audioFuncs.pause_audio()
            
        if pressed_key == padkeydriver.FORWARD:
            lcd.swapBacklight()
            audioFuncs.forward()
            
        if pressed_key == padkeydriver.BACKWARD:
            audioFuncs.backward()
            #audioFuncs.audio_thread_function("gustixa")
    
    # if flag == 5:    
    #         main_timer = threading.Timer(0.3, mainLoop)
    #         main_timer.start()

def modeLoop():
    pressed_key = padkeydriver.read_keypad()
    global flag
    global folder_index
    if pressed_key is not None:
        print("Pressed key:", pressed_key)
        if pressed_key == padkeydriver.PREVIOUS:
            if folder_index > 0:
                folder_index -= 1
                audioFuncs.display_folderName(serverSetup.folder_keys[folder_index])
            elif folder_index == 0:
                folder_index = len(serverSetup.folder_keys) -1
                audioFuncs.display_folderName(serverSetup.folder_keys[folder_index])

        if pressed_key == padkeydriver.NEXT:
            if folder_index < len(serverSetup.folder_keys) - 1:
                folder_index += 1
                audioFuncs.display_folderName(serverSetup.folder_keys[folder_index])
            elif folder_index == len(serverSetup.folder_keys) -1:
                folder_index = 0
                audioFuncs.display_folderName(serverSetup.folder_keys[folder_index])

        if pressed_key == padkeydriver.PAUSE_PLAY:
            flag = AUDIO_MODE
            



padkeydriver.init()
audioFuncs.init()

while True:
    looping_on_mode()
    while flag == AUDIO_MODE:
        mainLoop()
        time.sleep(0.3)




# def Toggle_swtich():
#         if GPIO.input(TOGGLE_GPIO) == GPIO.LOW:
#             lcd.setBacklight(0)
#         elif GPIO.input(TOGGLE_GPIO) == GPIO.HIGH:
#             lcd.setBacklight(1)
#         threading.Timer(0.3,Toggle_swtich).start()

#BUTTON_GPIO = 17
# TOGGLE_GPIO = 27

# def button_pressed_callback(channel):
#     print("Button pressed!")
#    # lcd.swapBacklight()
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=button_pressed_callback, bouncetime=200)

# GPIO.setup(TOGGLE_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
