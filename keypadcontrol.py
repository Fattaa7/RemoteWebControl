import RPi.GPIO as GPIO
import threading
import audioFuncs
import padkeydriver
import lcd
from datetime import datetime
from subprocess import check_output
import serverSetup
import time

folder_index = 0
IP = check_output(["hostname", "-I"], encoding="utf8").split()[0]

flag = 0

BUTTON_GPIO = 17
TOGGLE_GPIO = 27

def button_pressed_callback(channel):
    print("Button pressed!")
   # lcd.swapBacklight()
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=button_pressed_callback, bouncetime=200)

GPIO.setup(TOGGLE_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def mode():
    print("Buttooon!")
    lcd.init()
    lcd.lcdDisplay.lcd_display_string("IP Address is:",1)
    lcd.lcdDisplay.lcd_display_string("" + str(IP),2)
    while True:
        continue

def Toggle_swtich():
        if GPIO.input(TOGGLE_GPIO) == GPIO.LOW:
            lcd.setBacklight(0)
        elif GPIO.input(TOGGLE_GPIO) == GPIO.HIGH:
            lcd.setBacklight(1)
        threading.Timer(0.3,Toggle_swtich).start()

def display_element(filed_name):
    lcd.lcdDisplay.lcd_clear()
    file_name = filed_name
    str1 = file_name[:16]
    lcd.lcdDisplay.lcd_display_string(str1, 1)
    str2 = file_name[16:]
    if len(str2) > 1:
        lcd.long_string(lcd.lcdDisplay,str2,2)

def init():
    serverSetup.getFolders()
    lcd.init()
    display_element(serverSetup.folder_keys[0][:-1])
    


def mainLoop():
    pressed_key = padkeydriver.read_keypad()
    if pressed_key is not None:
        print("Pressed key:", pressed_key)
        if pressed_key == padkeydriver.PREVIOUS:
            audioFuncs.previous_audio()
            
        if pressed_key == padkeydriver.NEXT:
            audioFuncs.next_audio()
            
        if pressed_key == padkeydriver.PAUSE_PLAY:
            audioFuncs.pause_audio()
            
        if pressed_key == padkeydriver.FORWARD:
            lcd.swapBacklight()
            audioFuncs.forward()
            
        if pressed_key == padkeydriver.BACKWARD:
            audioFuncs.backward()
            audioFuncs.audio_thread_function("gustixa")
            
    threading.Timer(0.3, mainLoop).start()

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
            flag = 5
            

# if GPIO.input(TOGGLE_GPIO) == GPIO.LOW:
#     mode()






padkeydriver.init()
audioFuncs.init()
audioFuncs.modeInit()

while flag != 5:
    modeLoop()
    time.sleep(0.3)


audioFuncs.audio_thread_function(serverSetup.folder_keys[folder_index][:-1])
audioFuncs.autoNext()
#Toggle_swtich()
mainLoop()


while True:
    break    
    
