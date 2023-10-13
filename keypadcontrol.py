import boto3
import vlc
import RPi.GPIO as GPIO
import time
import drivers
import threading
from time import sleep, strftime
import audioFuncs
import padkeydriver
import urllib
import socket

def get_ip_address():
    try:  
        # Get the hostname
        host_name = socket.gethostname()
        # Get the IP address corresponding to the hostname
        ip_address = socket.gethostbyname(host_name)
        return ip_address
    except Exception as e:
        audioFuncs.lcdDisplay.lcd_display_string("No IP found", 1)
        return "Not Found"

# Call the function
ip_address = get_ip_address()


def mainLoop():
    pressed_key = padkeydriver.read_keypad()
    if pressed_key is not None:
        print("Pressed key:", pressed_key)
        if pressed_key == '9':
            audioFuncs.previous_audio()
        if pressed_key == '3':
            audioFuncs.next_audio()
        if pressed_key == '6':
            audioFuncs.pause_audio()
        if pressed_key == '+':
            audioFuncs.forward()
        if pressed_key == '=':
            audioFuncs.backward()
    threading.Timer(0.3, mainLoop).start()

    


padkeydriver.init()
audioFuncs.audio_thread_function()
audioFuncs.autoNext()
mainLoop()


while True:
    break    
    
