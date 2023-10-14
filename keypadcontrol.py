import RPi.GPIO as GPIO
import threading
import audioFuncs
import padkeydriver
import lcd

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
            lcd.setBacklight(0)
            audioFuncs.forward()
            
        if pressed_key == padkeydriver.BACKWARD:
            audioFuncs.backward()
            
    threading.Timer(0.3, mainLoop).start()

    


padkeydriver.init()
audioFuncs.audio_thread_function()
audioFuncs.autoNext()
mainLoop()


while True:
    break    
    
