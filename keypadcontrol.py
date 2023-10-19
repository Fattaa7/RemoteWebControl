import RPi.GPIO as GPIO
import threading
import audioFuncs
#import padkeydriver
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



NEXT_GPIO = 21
PAUSE_GPIO = 20
PREVIOUS_GPIO = 16
EXIT_GPIO = 19
LCD_GPIO = 18

TOGGLE_GPIO = 17


flag = MODE_MODE
folder_index = 0


GPIO.setmode(GPIO.BCM)

GPIO.setup(TOGGLE_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(NEXT_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PAUSE_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PREVIOUS_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(EXIT_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LCD_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)



IP = check_output(["hostname", "-I"], encoding="utf8").split()[0]


def Toggle_swtich(channel):
        if GPIO.input(TOGGLE_GPIO) == GPIO.LOW:
            print("THIS IS LOW")
            serverSetup.p.audio_set_volume(50)
        elif GPIO.input(TOGGLE_GPIO) == GPIO.HIGH:
            print("THIS IS HIGG")
            serverSetup.p.audio_set_volume(100)

def nextBtn(channel):
    if GPIO.input(channel) == GPIO.LOW:
        time.sleep(0.1)
        if GPIO.input(channel) == GPIO.LOW:
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
                    audioFuncs.next_audio()
            


def prevBtn(channel):
    if GPIO.input(channel) == GPIO.LOW:
        time.sleep(0.1)
        if GPIO.input(channel) == GPIO.LOW:
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
                    audioFuncs.previous_audio()
            

def pauseBtn(channel):
    if GPIO.input(channel) == GPIO.LOW:
        time.sleep(0.1)
        if GPIO.input(channel) == GPIO.LOW:
            global flag       
            global folder_index
            print("clicked pause")
            if flag == MODE_MODE:
                    flag = AUDIO_MODE
                    audioFuncs.audio_start(serverSetup.folder_keys[folder_index][:-1],folder_index)
            elif flag == AUDIO_MODE:
                    audioFuncs.pause_audio()
            

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
                looping_on_mode()
            elif flag == AUDIO_MODE:
                flag = MODE_MODE
                looping_on_mode()            

def lcdBtn(channel):
   if GPIO.input(channel) == GPIO.LOW:
        time.sleep(0.1)
        if GPIO.input(channel) == GPIO.LOW:
            global flag       
            global folder_index
            print("clicked lcd")       
            lcd.swapBacklight()

def DevMode():
    print("Buttooon!")
    lcd.init()
    lcd.lcdDisplay.lcd_display_string("IP Address is:",1)
    lcd.lcdDisplay.lcd_display_string("" + str(IP),2)


def looping_on_mode():
    #serverSetup.getFolders()
    audioFuncs.audio_stop()
    audioFuncs.modeInit()



counter = 0

#padkeydriver.init()
audioFuncs.init()
looping_on_mode()

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
    time.sleep(2)
    if GPIO.input(TOGGLE_GPIO) == GPIO.LOW:
        serverSetup.p.audio_set_volume(50)
    elif GPIO.input(TOGGLE_GPIO) == GPIO.HIGH:
        serverSetup.p.audio_set_volume(100)




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
